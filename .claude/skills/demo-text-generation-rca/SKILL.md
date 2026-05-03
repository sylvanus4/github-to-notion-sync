---
name: demo-text-generation-rca
description: "Text Generation 실험 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다."
---

# Demo Text Generation RCA

Text Generation 실험 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.

Text Generation Watcher는 10초 간격(기본값)으로 TrainJob 상태를 가져와
DB의 `text_generation_experiments` 테이블에 동기화합니다.
멀티스텝 실험(SFT, DPO, GRPO, CPT, GKD)을 지원하며, 각 스텝별 TrainJob을 순차 생성합니다.

## Pre-flight (한 번에 실행)

VPN 연결 상태에서 아래 블록을 순서대로 실행합니다. 이미 활성 상태이면 건너뜁니다.

```bash
# 1. 클러스터 컨텍스트 전환
kubectx tkai-demo

# 2. DB 포트포워딩 (백그라운드, 이미 열려 있으면 건너뛰기)
lsof -i :15432 >/dev/null 2>&1 && echo "Port 15432 already forwarded" \
  || kubectl -n postgresql port-forward svc/postgresql 15432:5432 &
```

### DB 접속 Quick Reference

| DB | 커맨드 |
|----|--------|
| ai_platform_db | `PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db` |

## Step 1 — DB에서 실험 상태 확인

```sql
SELECT id, name, status, error_message, current_step, total_steps,
       base_model_id, base_model_name, total_gpus,
       k8s_namespace, k8s_chain_id,
       to_timestamp(created_at) as created_time,
       to_timestamp(started_at) as started_time,
       to_timestamp(completed_at) as completed_time,
       step_message
FROM text_generation_experiments
WHERE id = '{EXPERIMENT_ID}';
```

또는 최근 실패/실행 중인 실험 조회:

> **주의**: `created_at`, `started_at`, `completed_at`, `updated_at` 컬럼은 **bigint (epoch seconds)** 타입입니다.

```sql
SELECT id, name, status, error_message, current_step, total_steps,
       base_model_name, total_gpus, k8s_namespace,
       to_timestamp(created_at) as created_time,
       step_message
FROM text_generation_experiments
WHERE status IN ('failed', 'running', 'creating', 'queued')
ORDER BY created_at DESC
LIMIT 10;
```

### 주요 status 값

| status | 의미 |
|--------|------|
| `pending` | 생성 직후, 이벤트 발행 대기 |
| `queued` | NATS 이벤트 수신, TrainJob 생성 대기 |
| `creating` | TrainJob 생성 중 |
| `running` | TrainJob 실행 중 (Watcher가 동기화) |
| `completed` | 모든 스텝 성공 완료 |
| `failed` | TrainJob 실패 또는 타임아웃 |
| `terminated` | 사용자 취소 |

## Step 2 — steps_config 분석 (멀티스텝 구성)

`steps_config`는 JSONB로 각 스텝의 학습 방법과 하이퍼파라미터를 저장합니다.

```sql
SELECT id, name, current_step, total_steps,
       jsonb_pretty(steps_config) as steps_detail
FROM text_generation_experiments
WHERE id = '{EXPERIMENT_ID}';
```

### StepConfig 필드

| 필드 | 의미 |
|------|------|
| `method` | 학습 방법 (sft, dpo, grpo, cpt, gkd) |
| `training_strategy` | 학습 전략 (full, lora, qlora) |
| `dataset_id` | 학습 데이터셋 UUID |
| `num_epochs` | 에포크 수 |
| `batch_size` | 배치 사이즈 |
| `learning_rate` | 학습률 |
| `pod_name` | 해당 스텝 Pod 이름 (실행 후 채워짐) |
| `status` | 스텝별 상태 |

```sql
-- 현재 스텝의 pod_name 확인
SELECT id,
       steps_config->((current_step-1)::int)->>'pod_name' as current_pod,
       steps_config->((current_step-1)::int)->>'method' as current_method,
       steps_config->((current_step-1)::int)->>'status' as step_status
FROM text_generation_experiments
WHERE id = '{EXPERIMENT_ID}';
```

## Step 3 — TrainJob 상태 확인 (K8s)

```bash
# 실험의 모든 TrainJob 조회 (label selector)
kubectl get trainjobs -n {NAMESPACE} -l experiment-id={EXPERIMENT_ID}

# TrainJob 상세 (Events, Conditions 확인)
kubectl describe trainjob {TRAINJOB_NAME} -n {NAMESPACE}

# TrainJob의 Pod 목록
kubectl get pods -n {NAMESPACE} -l experiment-id={EXPERIMENT_ID}

# 현재 스텝의 Pod 로그
kubectl logs {POD_NAME} -n {NAMESPACE} --tail=200

# 이전 로그 (크래시된 경우)
kubectl logs {POD_NAME} -n {NAMESPACE} --previous

# Pod 상세 (OOMKilled, Evicted 등 확인)
kubectl describe pod {POD_NAME} -n {NAMESPACE}
```

### TrainJob Status 해석

Watcher가 `ResolveCurrentStepStatus()`로 판단하는 상태:

| TrainJob Status | Watcher 동작 |
|-----------------|-------------|
| `Succeeded` | 다음 스텝 TrainJob 생성 또는 실험 완료 처리 |
| `Failed` | Pod 장애 분류 후 실험 실패 처리 |
| `Running` | 진행률 업데이트 |
| `Pending` | 대기 (GPU 할당, Kueue 큐잉 등) |
| `Missing` | TrainJob이 클러스터에서 사라짐 (Kueue eviction 등) |
| `Unknown` | 10회 연속 시 실험 실패 처리 |

## Step 4 — 장애 분류 (FailureClassification)

Watcher는 Pod 상태를 검사하여 장애를 분류합니다.
우선순위: Evicted > Preempted > OOMKilled > Unknown

```bash
# Pod의 종료 상태 확인
kubectl get pod {POD_NAME} -n {NAMESPACE} -o jsonpath='{.status.reason}'
kubectl get pod {POD_NAME} -n {NAMESPACE} -o jsonpath='{.status.containerStatuses[0].state.terminated.reason}'

# OOMKilled 여부 빠른 확인
kubectl get pod {POD_NAME} -n {NAMESPACE} -o jsonpath='{range .status.containerStatuses[*]}{.name}: {.state.terminated.reason}{"\n"}{end}'
```

| FailureCategory | 원인 | 조치 |
|-----------------|------|------|
| `evicted` | 노드 리소스 압박 또는 Kueue가 더 높은 우선순위 작업에 자리를 양보 | Kueue 큐 우선순위 확인, 노드 리소스 상태 점검 |
| `preempted` | 더 높은 우선순위 워크로드에 의해 선점됨 | PriorityClass 설정 확인 |
| `oom_killed` | 컨테이너 메모리 초과 | memory limit 증가, batch_size 축소, gradient_checkpointing 활성화 |
| `job_missing` | TrainJob이 클러스터에서 삭제됨 (Kueue, 수동 삭제 등) | Kueue Workload 상태, 수동 삭제 여부 확인 |

## Step 5 — Kueue 연동 확인

TrainJob은 Kueue를 통해 스케줄링됩니다. 타임아웃 전에 Kueue 상태를 확인합니다.

```bash
# Workload 상태 확인
kubectl get workloads -n {NAMESPACE} -l experiment-id={EXPERIMENT_ID}

# Workload 상세 (Conditions, admission 상태)
kubectl describe workload -n {NAMESPACE} -l experiment-id={EXPERIMENT_ID}

# LocalQueue 상태 (대기 중인 워크로드 수)
kubectl get localqueue -n {NAMESPACE}

# ClusterQueue 상태 (리소스 할당 현황)
kubectl get clusterqueue
```

| Kueue 증상 | 원인 | 조치 |
|-----------|------|------|
| Workload `Pending` 지속 | GPU 리소스 부족 | ClusterQueue 용량, 노드 GPU 가용성 확인 |
| Workload `Evicted` | 더 높은 우선순위 Workload가 자원 점유 | PriorityClass 확인, 재실행 대기 |
| Workload `Admitted` but Pod `Pending` | 스케줄러가 노드 배치 실패 | 노드 taint/toleration, nodeSelector 확인 |

## Step 6 — NATS 이벤트 흐름 확인

Text Generation은 Transactional Outbox 패턴으로 이벤트를 발행합니다.

```sql
-- 실험의 이벤트 이력 확인
SELECT id, event_type, status, retry_count, error_message,
       to_timestamp(created_at) as created_time,
       to_timestamp(published_at) as published_time
FROM text_generation_experiment_events
WHERE experiment_id = '{EXPERIMENT_ID}'
ORDER BY created_at;
```

### 이벤트 타입

| event_type | 발생 시점 |
|-----------|----------|
| `experiment.created` | 실험 생성 시 (API Server → Outbox) |
| `experiment.started` | 실행 시작 시 |
| `experiment.step_updated` | 스텝 전환 시 |
| `experiment.completed` | 완료 시 |
| `experiment.failed` | 실패 시 |
| `experiment.deleted` | 삭제 시 |

| 증상 | 원인 | 조치 |
|------|------|------|
| 이벤트 `status=pending` 장시간 | Event Worker가 이벤트를 발행하지 못함 | Event Worker Pod 상태, NATS 연결 확인 |
| 이벤트 `status=failed` | 발행 실패 (NATS 연결 오류 등) | NATS 서버 상태, retry_count 확인 |
| `experiment.created` 이벤트 없음 | API Server에서 Outbox INSERT 실패 | API Server 로그 확인 |

```bash
# Event Worker 상태
kubectl get pods -n ai-platform -l app=ai-platform-backend-go -l component=event-worker

# NATS 연결 확인
kubectl get pods -n nats
kubectl logs -n nats -l app.kubernetes.io/name=nats --tail=50

# Task Runner 로그에서 Text Generation 관련 에러
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=200 | grep -i "textgen\|text.gen\|text_gen\|error"
```

## Step 7 — 일반적인 장애 원인 매트릭스

### 7.1 실험이 `pending`/`queued`/`creating`에서 멈춤

| 증상 | 원인 | 조치 |
|------|------|------|
| `pending` 지속 | Outbox 이벤트 미발행 | Step 6 NATS 흐름 확인 |
| `queued` 지속 | Task Runner가 이벤트 미수신 | Task Runner Pod, NATS consumer 확인 |
| `creating` 지속 | TrainJob 생성 실패 | Task Runner 로그, K8s API 권한 확인 |

### 7.2 학습 중 실패 (SFT, DPO, GRPO, CPT, GKD)

| 증상 | 원인 | 조치 |
|------|------|------|
| CUDA OOM | GPU 메모리 부족 | batch_size 줄이기, gradient_checkpointing 활성화, qlora 전환 |
| Pod OOMKilled | CPU 메모리 부족 (데이터 로딩 등) | memory limit 증가 |
| Pod Pending | GPU 노드 부족 | GPU 가용성 확인, Kueue 큐 상태 점검 |
| NaN loss / divergence | 학습률/데이터 문제 | learning_rate 낮추기, 데이터셋 검증 |
| 모델 다운로드 실패 | S3/HF 인증 문제 | S3 Secret, HF Token 확인 |
| `step_message`: timeout | MaxRunDuration(2h) 초과 | 학습 시간 조정, 에포크 수 줄이기 |

### 7.3 멀티스텝 전환 실패

| 증상 | 원인 | 조치 |
|------|------|------|
| Step 1 완료 후 Step 2 미시작 | 다음 TrainJob 생성 실패 | Task Runner 로그, 이전 스텝 output_path 확인 |
| `current_step` < `total_steps` + `failed` | 중간 스텝 실패 | 실패 스텝의 Pod 로그 확인 |

### 7.4 모델 프로모션/저장 실패

| 증상 | 원인 | 조치 |
|------|------|------|
| 실험 완료 but 모델 미등록 | MLflow 등록 실패 | MLflow 서버 상태, 로그 확인 |
| `final_model_path` 비어있음 | 모델 저장 실패 | S3 접근 권한, 스토리지 용량 확인 |

## Step 8 — Task Runner 로그 확인

```bash
# Task Runner Pod 확인
kubectl get pods -n ai-platform -l app=ai-platform-backend-go

# Text Generation 관련 로그 필터링
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=500 | grep -i "text.gen\|textgen\|text_gen"

# 에러만 필터링
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=500 | grep -i "error\|failed\|panic" | grep -i "text.gen\|textgen"
```

## Step 9 — Source Code Change Analysis

RCA 분석 시 최근 소스코드 변경사항을 함께 확인하여 코드 변경이 장애의 원인인지 판단합니다.

### 9.1 최근 변경 이력 (Last 14 Days)

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/mlstudio/textgeneration/ \
  backend/go/internal/runner/mlstudio/common/
```

### 9.2 핵심 파일 소유자 및 최근 수정자 확인

```bash
# watcher.go 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/mlstudio/textgeneration/watcher.go \
  | sort | uniq -c | sort -rn

# 핵심 함수 변경 이력 (스텝 상태 판단 로직)
git -C ai-platform log --since="30 days ago" -p \
  -S "ResolveCurrentStepStatus" -- backend/go/internal/runner/mlstudio/textgeneration/watcher.go

# 장애 분류 로직 변경 이력
git -C ai-platform log --since="30 days ago" -p \
  -S "ClassifyFailure" -- backend/go/internal/runner/mlstudio/common/failure_classifier.go

# TrainJob 빌더 변경 이력
git -C ai-platform log --since="30 days ago" -p \
  -S "BuildTrainJob" -- backend/go/internal/runner/mlstudio/textgeneration/trainjob_builder.go
```

### 9.3 장애 시점과 코드 변경 시점 상관관계

1. Step 1의 DB 쿼리에서 확인한 장애 발생 시각(`completed_at` 또는 `updated_at`, epoch seconds → `to_timestamp()`)을 기준으로 합니다
2. 해당 시각 전후 커밋 확인:
   ```bash
   git -C ai-platform log --since="{ERROR_DATE} -3 days" \
     --until="{ERROR_DATE}" \
     --format="%h | %an | %ad | %s" --date=iso -- \
     backend/go/internal/runner/mlstudio/textgeneration/ \
     backend/go/internal/runner/mlstudio/common/
   ```
3. 커밋 상세 확인:
   ```bash
   git -C ai-platform show {COMMIT_HASH} --stat
   ```

### 9.4 Helm Chart 변경 확인

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/charts/
```

### 코드 변경 → 장애 상관관계 판단 기준

| 조건 | 판단 |
|------|------|
| 장애 발생 3일 이내에 관련 파일 커밋 있음 | **높은 상관관계** — 변경 내용 상세 리뷰 필요 |
| 장애 발생 7일 이내에 관련 파일 커밋 있음 | **중간 상관관계** — 변경 내용 확인 |
| 14일 이내 커밋 없음 | **낮은 상관관계** — 인프라/설정 원인 가능성 높음 |
| Helm chart 변경 있음 | **배포 설정 변경** — values 비교 필요 |

> 깊은 소유권 분석이 필요한 경우 `codebase-archaeologist` 스킬을 참고하세요.

## Watcher Thresholds Reference

| 설정 | 환경변수 | 기본값 | 용도 |
|------|---------|--------|------|
| WatchInterval | `TEXT_GENERATION_WATCH_INTERVAL` | 10s | TrainJob 상태 동기화 주기 |
| MaxRunDuration | `TEXT_GENERATION_MAX_RUN_DURATION` | 2h | 실험 최대 실행 시간 (초과 시 failed) |
| MaxUnknownStatusRetries | `TEXT_GENERATION_MAX_UNKNOWN_RETRIES` | 10 | Unknown 상태 연속 허용 횟수 |
| DefaultCPULimit | `TEXT_GENERATION_DEFAULT_CPU_LIMIT` | 1 | TrainJob 기본 CPU limit |
| DefaultMemoryLimit | `TEXT_GENERATION_DEFAULT_MEMORY_LIMIT` | 1Gi | TrainJob 기본 메모리 limit |
| RuntimeName | `TEXT_GENERATION_RUNTIME_NAME` | llm-training | ClusterTrainingRuntime 이름 |
| Namespace | `TEXT_GENERATION_NAMESPACE` | ai-platform | TrainJob 생성 네임스페이스 |

## Source Code Reference

- Text Generation Watcher: `ai-platform/backend/go/internal/runner/mlstudio/textgeneration/watcher.go`
- Text Generation Handlers: `ai-platform/backend/go/internal/runner/mlstudio/textgeneration/handlers.go`
- TrainJob Builder: `ai-platform/backend/go/internal/runner/mlstudio/textgeneration/trainjob_builder.go`
- Event Handlers: `ai-platform/backend/go/internal/runner/mlstudio/textgeneration/handlers_events.go`
- Failure Classifier: `ai-platform/backend/go/internal/runner/mlstudio/common/failure_classifier.go`
- Config: `ai-platform/backend/go/internal/config/taskrunner.go` (TextGenerationRunnerConfig)
- DB Schema: `ai-platform/backend/go/migrations/000013_create_mlstudio_tables.up.sql`
- State Transitions: `ai-platform/backend/go/docs/common/mlstudio/text-generation/text_generation_state_transitions.md`
- Watcher Design: `ai-platform/backend/go/docs/runner/mlstudio/text-generation/text_generation_watcher.md`
- Event Publisher: `ai-platform/backend/go/docs/event_worker/mlstudio/text-generation/README.md`

---

## Git 커밋 귀인 분석 (필수)

> **반드시 수행**: "언제 누가 어떤 작업을 했는데 문제가 발생한 것인지?" 질문에 답해야 합니다.

RCA 완료 후 근본 원인과 관련된 코드/설정 변경의 커밋 이력을 추적하여 인과 관계 타임라인을 작성합니다.

### 관련 파일 커밋 이력 조회

```bash
git -C ai-platform log --since="30 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/mlstudio/textgeneration/ \
  backend/go/internal/runner/mlstudio/common/

gh api repos/{OWNER}/{REPO}/commits?path={FILE_PATH}&per_page=10
```

### 커밋 귀인 타임라인 작성

| 순서 | 날짜 | 누가 | 어디서 | 무슨 작업 | 영향 |
|------|------|------|--------|-----------|------|
| 1 | YYYY-MM-DD | 작업자 | 파일/레포 | 변경 내용 | 영향 분석 |

**핵심 커밋**에는 SHA, Author, Date, Message, 파일, 변경 내용을 상세히 기록합니다.

### 인과 관계 요약

```
[시점1] 작업 A (작업자)
     ↓
[시점2] 작업 B (작업자)
     ↓
[시점3] ⚠️ 핵심 원인 커밋 (작업자)
     ↓
[실행 시] 에러 발생
```

### 핵심 판단

- **직접 원인**: 어떤 커밋이 근본 원인인지
- **전파 경로**: 어떻게 현재 환경에 전파되었는지
- **ThakiCloud 팀 책임**: 리뷰/검증 부재 여부

---

## 노션 업로드 (필수)

RCA 리포트 완료 후 반드시 아래 절차를 수행합니다:

1. RCA 전체 내용(에러 요약 + 근본 원인 + 커밋 귀인 타임라인 + 해결 방안 + 재발 방지)을
   `outputs/demo-rca/{date}/text-generation-rca.md`에 저장
2. `md-to-notion` 스킬 또는 Notion MCP `notion-create-pages`로
   "AI Platform Demo 환경 RCA 리포트" (ID: `34e9eddc34e680f78eacfea0a60270b3`) 하위에 업로드
3. 생성된 노션 페이지 URL을 사용자에게 제공

> **참고**: pipe 테이블은 Notion에서 렌더링되지 않으므로 HTML `<table>` 태그로 변환하여 업로드합니다.
