---
name: demo-tabular-rca
description: >-
  Systematic RCA for AI Platform Demo Tabular (ML Studio) experiment errors.
  Guides through multi-step experiment lifecycle analysis using DB status
  queries, steps_config JSONB inspection, TrainJob/Kueue K8s status, and
  failure classification — grounded in actual Go backend source code
  (tabular_watcher.go, handlers_events.go, handlers_trainjob.go,
  step_config.go).
---

# Demo Tabular (ML Studio) Experiment RCA

AI Platform Demo 환경에서 Tabular 실험 (ML Studio) 에러 발생 시 체계적 원인 분석 가이드.

> **Template**: `demo-text-generation-rca` 구조 기반 (동일한 TrainJob + multi-step + Kueue 패턴)
> **Source**: `ai-platform/backend/go/internal/runner/mlstudio/tabular/`

## Pre-flight

```bash
# 1. Demo 클러스터 접속
kubectx demo

# 2. DB 포트포워딩 (CNPG → ai_platform_db)
kubectl port-forward -n postgresql svc/cnpg-ai-platform-rw 5432:5432 &

# 3. DB 접속
PGPASSWORD=$(kubectl get secret -n postgresql cnpg-ai-platform-app -o jsonpath='{.data.password}' | base64 -d)
psql -h localhost -U app -d ai_platform_db
```

## Step 1: DB 상태 확인

### 1.1 Failed 실험 조회

```sql
SELECT
  id,
  name,
  status,
  error_message,
  training_mode,
  current_step,
  total_steps,
  k8s_namespace,
  train_job_id,
  to_timestamp(created_at) AS created,
  to_timestamp(updated_at) AS updated,
  ROUND((EXTRACT(EPOCH FROM now()) - updated_at) / 60) AS mins_since_update
FROM tabular_experiments
WHERE status = 'failed'
ORDER BY updated_at DESC
LIMIT 20;
```

> **Timestamp 형식**: `tabular_experiments`는 epoch **seconds** 사용 (`time.Now().Unix()`)

### 1.2 Stuck Running 실험 조회

```sql
SELECT
  id,
  name,
  status,
  training_mode,
  current_step,
  total_steps,
  k8s_namespace,
  train_job_id,
  to_timestamp(created_at) AS created,
  to_timestamp(updated_at) AS updated,
  ROUND((EXTRACT(EPOCH FROM now()) - updated_at) / 60) AS mins_since_update
FROM tabular_experiments
WHERE status = 'running'
  AND (EXTRACT(EPOCH FROM now()) - updated_at) > 7200
ORDER BY updated_at ASC;
```

> **7200초 = 2시간**: `TABULAR_MAX_RUN_DURATION` 기본값

### 1.3 Steps Config 분석

```sql
SELECT
  id,
  name,
  training_mode,
  current_step,
  total_steps,
  steps_config::text
FROM tabular_experiments
WHERE id = '<EXPERIMENT_ID>';
```

`steps_config` JSONB 구조:
```json
[
  {"step_index": 1, "step_name": "preprocessing", "status": "succeeded", "output_path": "...", "train_job_name": "..."},
  {"step_index": 2, "step_name": "training", "status": "running", "output_path": "...", "train_job_name": "..."},
  {"step_index": 3, "step_name": "shap_analysis", "status": "pending", "output_path": "...", "train_job_name": ""},
  {"step_index": 4, "step_name": "report_generation", "status": "pending", "output_path": "...", "train_job_name": ""}
]
```

### 1.4 상태 분포 조회

```sql
SELECT status, COUNT(*) AS cnt
FROM tabular_experiments
WHERE cluster_id = (SELECT id FROM clusters WHERE name = 'demo' LIMIT 1)
GROUP BY status
ORDER BY cnt DESC;
```

## Step 2: Training Mode별 Step Pipeline

Tabular 실험은 `training_mode`에 따라 다른 step pipeline을 가짐:

| Training Mode | Steps (순서) | Total Steps |
|---------------|-------------|-------------|
| **basic** | Preprocessing → Training → SHAP Analysis → Report Generation | 4 |
| **automl** | Preprocessing → **Hyperparameter Tuning** → Training → SHAP Analysis → Report Generation | 5 |
| **flaml** | Preprocessing → **FLAML AutoML** → Training → SHAP Analysis → Report Generation | 5 |
| **autogluon** | Preprocessing → **AutoGluon AutoML** → Training → SHAP Analysis → Report Generation | 5 |

> **Source**: `step_config.go` — `StepNamesForMode()`, `BuildStepsConfigForMode()`
> Handler는 **1번째 step의 TrainJob만 생성**. 이후 step의 TrainJob은 **Watcher가 이전 step 성공 시 자동 생성**.

## Step 3: K8s TrainJob 상태 확인

### 3.1 해당 실험의 TrainJob 조회

```bash
# experiment-id 라벨로 TrainJob 조회
kubectl get trainjobs -n <NAMESPACE> -l experiment-id=<EXPERIMENT_ID> -o wide

# TrainJob 상세
kubectl describe trainjob <TRAINJOB_NAME> -n <NAMESPACE>

# TrainJob 소유 Pod 확인
kubectl get pods -n <NAMESPACE> -l experiment-id=<EXPERIMENT_ID> -o wide
```

### 3.2 Kueue Workload 상태 확인

```bash
# Kueue Workload 조회
kubectl get workloads -n <NAMESPACE> -l experiment-id=<EXPERIMENT_ID>

# Kueue Workload 상세 (admission, eviction 상태)
kubectl describe workload <WORKLOAD_NAME> -n <NAMESPACE>
```

> **Kueue 타임아웃**: Watcher가 `kueue.IsKueueTimeoutReached()` 호출 → admission 대기 시간 초과 시 실험 failed 처리

### 3.3 Pod 로그 확인

```bash
# 현재 실행 중인 Pod 로그
kubectl logs <POD_NAME> -n <NAMESPACE> --tail=100

# 종료된 Pod 로그 (이전 컨테이너)
kubectl logs <POD_NAME> -n <NAMESPACE> --previous --tail=100

# Pod 이벤트
kubectl get events -n <NAMESPACE> --field-selector involvedObject.name=<POD_NAME> --sort-by='.lastTimestamp'
```

## Step 4: Failure Decision Tree

### 4.1 `error_message` 패턴별 원인 분석

#### Timeout 관련

| error_message 패턴 | 원인 | 조치 |
|-------------------|------|------|
| `experiment exceeded maximum run duration` | `MaxRunDuration` (기본 2h) 초과 | 데이터셋 크기 확인, GPU 리소스 증설, `TABULAR_MAX_RUN_DURATION` 환경변수 조정 |
| `kueue admission timeout` / Kueue 관련 | Kueue 큐에서 admission 대기 시간 초과 | `kubectl get clusterqueues`, GPU 리소스 가용성 확인, 우선순위 확인 |

#### TrainJob 실패 관련

| error_message 패턴 | 원인 | 조치 |
|-------------------|------|------|
| `Evicted` 포함 | 노드 리소스 부족으로 Pod Eviction | `kubectl describe node`, 메모리/디스크 pressure 확인 |
| `Preempted` 포함 | Kueue/스케줄러에 의한 선점 | 우선순위 설정 확인, 다른 워크로드와 리소스 경합 확인 |
| `OOMKilled` 포함 | 컨테이너 메모리 한도 초과 | 리소스 requests/limits 확인, 데이터셋 크기 대비 메모리 적정성 |
| `step <N> failed` | 특정 step의 TrainJob 실패 | 해당 step Pod 로그 확인, `steps_config` JSONB에서 실패 step 특정 |

#### TrainJob Missing 관련

| error_message 패턴 | 원인 | 조치 |
|-------------------|------|------|
| `TrainJob missing` / `job not found` | TrainJob이 K8s에서 사라짐 (Kueue eviction, 수동 삭제) | Kueue Workload 이벤트 확인, `kubectl get events -n <NS>` |

#### Handler-level 실패

| error_message 패턴 | 원인 | 조치 |
|-------------------|------|------|
| `namespace not found` | 프로젝트 네임스페이스 미존재 | `kubectl get ns <NS>`, 프로젝트 설정 확인 |
| `failed to create TrainJob` | K8s TrainJob 생성 실패 | TrainJob CRD 설치 확인, RBAC 권한 확인 |
| `failed to initialize steps_config` | DB에 steps_config 저장 실패 | DB 연결 상태, 스키마 확인 |
| `failed to create MLflow run` | MLflow 서버 연결 실패 | MLflow 서비스 상태 확인, 네트워크 연결 |
| `failed to create data source secret` | K8s Secret 생성 실패 | RBAC, Secret 크기 제한 확인 |

#### Unknown Status 관련

| error_message 패턴 | 원인 | 조치 |
|-------------------|------|------|
| `unknown status retries exceeded` | TrainJob 상태를 `MaxUnknownStatusRetries` (기본 10회) 연속으로 판별 불가 | K8s API 서버 상태 확인, TrainJob CRD 상태 확인 |

### 4.2 Step별 실패 분석 Flow

```
1. DB에서 current_step 확인
2. steps_config JSONB에서 실패한 step 특정
   └─ step.status == "failed" 인 항목 찾기
3. 해당 step의 train_job_name으로 K8s TrainJob 조회
   ├─ TrainJob 존재? → Pod 로그 확인
   │   ├─ OOMKilled → 메모리 증설
   │   ├─ Evicted → 노드 리소스 확인
   │   ├─ Exit code != 0 → 학습 코드/데이터 문제
   │   └─ ImagePullBackOff → 이미지 레지스트리 확인
   └─ TrainJob 없음? → Kueue eviction 또는 수동 삭제
       └─ kubectl get events -n <NS> 확인
4. 이전 step 출력 확인
   └─ step의 output_path (S3) 에 결과물 존재하는지 확인
```

## Step 5: Multi-step Experiment Lifecycle

### 5.1 정상 흐름 (Basic mode, 4 steps)

```
[NATS: tabular.experiment.created]
  → Handler: steps_config 초기화 (4 steps)
  → Handler: MLflow parent run 생성
  → Handler: Step 1 TrainJob 생성 (preprocessing)
  → DB: status = 'running', current_step = 1

[Watcher: step 1 TrainJob Succeeded]
  → Watcher: Step 1 status = 'succeeded'
  → Watcher: Step 2 TrainJob 생성 (training)
  → DB: current_step = 2

[Watcher: step 2 TrainJob Succeeded]
  → ... (반복)

[Watcher: 마지막 step Succeeded]
  → DB: status = 'completed'
```

### 5.2 Step Transition 로직 (Watcher)

Watcher `syncTrainJobStatuses()` 핵심 분기:

| TrainJob Status | Watcher 동작 |
|-----------------|-------------|
| **Succeeded** | `handleStepCompleted` → 마지막 step이면 `completed`, 아니면 다음 step TrainJob 생성 |
| **Failed** | `handleStepFailed` → 실패 원인 분류 (Evicted/Preempted/OOMKilled), 실험 `failed` 처리 |
| **Running / Pending** | progress 업데이트, Pod name 캐싱 |
| **Missing** | `handleTrainJobMissing` → Kueue eviction 가능성, 실험 `failed` 처리 |
| **Unknown** | `handleUnknownStatus` → 연속 카운트 증가, threshold 초과 시 `failed` |

## Step 6: NATS Event 흐름

| Event | Trigger | Handler 동작 |
|-------|---------|-------------|
| `tabular.experiment.created` | UI에서 실험 생성 | `HandleExperimentCreated`: steps_config 초기화, MLflow run 생성, 1번째 step TrainJob 생성 |
| `tabular.experiment.cancelled` | UI에서 실험 취소 | `HandleExperimentCancelled`: TrainJob 삭제, DB `cancelled` |
| `tabular.experiment.deleted` | UI에서 실험 삭제 | `HandleExperimentDeleted`: TrainJob + 스토리지 + MLflow 정리, DB `deleted` |
| `tabular.reconciliation.requested` | 관리자 수동 트리거 | 실험 상태 재동기화 |

### NATS 디버깅

```bash
# Task Runner Pod 로그에서 NATS 이벤트 처리 확인
kubectl logs -n ai-platform deployment/task-runner --tail=200 | grep -i "tabular"

# 특정 실험 ID로 필터
kubectl logs -n ai-platform deployment/task-runner --tail=500 | grep "<EXPERIMENT_ID>"
```

## Step 7: Common Failure Matrix

| 증상 | DB 상태 | K8s 상태 | 원인 | 해결 |
|------|---------|---------|------|------|
| 실험이 running에서 멈춤 | `running`, `updated_at` 2시간+ 전 | TrainJob Running or Missing | MaxRunDuration 초과 (Watcher가 다음 cycle에 처리) 또는 Watcher 미동작 | Task Runner Pod 상태 확인, Watcher 로그 확인 |
| Step 1에서 바로 실패 | `failed`, `current_step=1` | TrainJob Failed or Missing | 전처리 코드 에러, 데이터 접근 실패, 이미지 문제 | Pod 로그 확인, 데이터소스 Secret 확인 |
| 중간 step에서 실패 | `failed`, `current_step=N` (N>1) | TrainJob Failed | 이전 step 출력물 문제, 메모리 부족 | S3 output_path 확인, 리소스 limits 확인 |
| 실험 생성 후 변화 없음 | `pending` or `creating` | TrainJob 없음 | Handler 실패 (NATS 미수신, 네임스페이스 문제) | NATS 연결 확인, Task Runner 로그 확인 |
| 실험 삭제 후 잔여 리소스 | `deleted` | TrainJob/Pod 존재 | 삭제 Handler 실패 | 수동 K8s 리소스 정리 |

## Step 8: Task Runner 로그 확인

```bash
# Task Runner Deployment 확인
kubectl get deployment task-runner -n ai-platform

# Tabular 관련 로그
kubectl logs -n ai-platform deployment/task-runner --tail=500 | grep -iE "(tabular|mlstudio)"

# Watcher 동작 로그
kubectl logs -n ai-platform deployment/task-runner --tail=500 | grep -iE "(syncTrainJobStatuses|handleStep|tabular_watcher)"

# 에러 로그만
kubectl logs -n ai-platform deployment/task-runner --tail=1000 | grep -iE "(tabular.*error|tabular.*fail)"
```

## Watcher Thresholds Reference

| 설정 | 환경변수 | 기본값 | 용도 |
|------|---------|--------|------|
| WatchInterval | `TABULAR_WATCH_INTERVAL` | 10s | TrainJob 상태 동기화 주기 |
| MaxRunDuration | `TABULAR_MAX_RUN_DURATION` | 2h | 실험 최대 실행 시간 (초과 시 failed) |
| MaxUnknownStatusRetries | `TABULAR_MAX_UNKNOWN_RETRIES` | 10 | Unknown 상태 연속 허용 횟수 (초과 시 failed) |

> 환경변수 확인: `kubectl get deployment task-runner -n ai-platform -o jsonpath='{.spec.template.spec.containers[0].env}' | jq .`

## Source Code Change Analysis

최근 코드 변경이 Tabular 장애에 영향을 미쳤는지 확인:

```bash
# Tabular runner 관련 최근 변경
git -C ai-platform/backend/go log --oneline -20 -- internal/runner/mlstudio/tabular/

# Watcher 변경
git -C ai-platform/backend/go log --oneline -10 -- internal/runner/mlstudio/tabular/tabular_watcher.go

# Handler 변경
git -C ai-platform/backend/go log --oneline -10 -- internal/runner/mlstudio/tabular/handlers_events.go

# TrainJob 빌더 변경
git -C ai-platform/backend/go log --oneline -10 -- internal/runner/mlstudio/tabular/handlers_trainjob.go

# Step config 변경
git -C ai-platform/backend/go log --oneline -10 -- internal/runner/mlstudio/tabular/step_config.go

# Common 유틸리티 변경 (공유 로직)
git -C ai-platform/backend/go log --oneline -10 -- internal/runner/mlstudio/common/
```

## Source Code Reference

| 파일 | 역할 |
|------|------|
| `ai-platform/backend/go/internal/runner/mlstudio/tabular/tabular_watcher.go` | Watcher: TrainJob 상태 동기화, step 전환, timeout/Kueue 감지, 실패 분류 |
| `ai-platform/backend/go/internal/runner/mlstudio/tabular/handlers_events.go` | NATS Handler: 실험 생성 (steps_config 초기화, MLflow, 1번째 TrainJob), 취소, 삭제 |
| `ai-platform/backend/go/internal/runner/mlstudio/tabular/handlers_trainjob.go` | TrainJob 빌더: step별 TrainJobSpec 구성 (env vars, volumes, resources) |
| `ai-platform/backend/go/internal/runner/mlstudio/tabular/step_config.go` | Step Pipeline: 4가지 training mode별 step 구성 정의 |
| `ai-platform/backend/go/internal/runner/mlstudio/common/` | 공통 유틸: DB 쿼리 빌더, 상태 업데이트, TrainJob 상태 해석, Kueue 연동 |
| `ai-platform/backend/go/internal/config/taskrunner.go` | 설정: Watcher 간격, 타임아웃, 재시도 횟수 환경변수 매핑 |

---

## Git 커밋 귀인 분석 (필수)

> **반드시 수행**: "언제 누가 어떤 작업을 했는데 문제가 발생한 것인지?" 질문에 답해야 합니다.

RCA 완료 후 근본 원인과 관련된 코드/설정 변경의 커밋 이력을 추적하여 인과 관계 타임라인을 작성합니다.

### 관련 파일 커밋 이력 조회

```bash
git -C ai-platform log --since="30 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/mlstudio/tabular/ \
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
   `outputs/demo-rca/{date}/tabular-rca.md`에 저장
2. `md-to-notion` 스킬 또는 Notion MCP `notion-create-pages`로
   "AI Platform Demo 환경 RCA 리포트" (ID: `34e9eddc34e680f78eacfea0a60270b3`) 하위에 업로드
3. 생성된 노션 페이지 URL을 사용자에게 제공

> **참고**: pipe 테이블은 Notion에서 렌더링되지 않으므로 HTML `<table>` 태그로 변환하여 업로드합니다.
