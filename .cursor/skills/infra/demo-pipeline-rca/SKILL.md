---
name: demo-pipeline-rca
description: >-
  Systematic RCA for AI Platform Demo Pipeline Builder errors.
  Guides through KFP run status checks, block-level debugging via
  block_statuses and block_pods JSON parsing, "Run not found" handling,
  and per-block pod log retrieval.
  Use when the user asks to "debug pipeline", "pipeline error",
  "pipeline failed", "pipeline RCA", "파이프라인 에러", "파이프라인 장애",
  "파이프라인 원인 분석", "demo-pipeline-rca", "KFP error", "KFP run failed",
  "파이프라인 빌더 트러블슈팅", "block failed", "블록 실패",
  or encounters a failed/stuck pipeline in the AI Platform Demo environment.
  Do NOT use for Workload errors (use demo-workload-rca).
  Do NOT use for Serverless/Endpoint errors (use demo-serverless-rca).
  Do NOT use for production environment troubleshooting.
metadata:
  author: "thaki"
  version: "2.1.0"
  category: "infra"
  platforms: [darwin]
---

# Demo Pipeline Builder RCA

Pipeline Builder 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.

Pipeline Watcher는 10초 간격으로 KFP(Kubeflow Pipelines) 서버에서 실행 상태를 가져와
DB의 `pipeline_runs` 테이블에 동기화합니다. 최대 5개 파이프라인을 동시에 체크합니다.

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
| tkai_agents | `PGPASSWORD=tkai_password psql -h localhost -p 15432 -U tkai_user -d tkai_agents` |

## Step 1 — DB에서 파이프라인 실행 상태 확인

```sql
SELECT id, pipeline_id, status, error_message,
       kfp_run_id, block_statuses, block_pods,
       created_at, completed_at, updated_at
FROM pipeline_runs
WHERE id = '{PIPELINE_RUN_ID}'
   OR pipeline_id = '{PIPELINE_ID}';
```

또는 최근 실패한 파이프라인 조회:

> **주의**: `created_at`, `completed_at`, `updated_at` 컬럼은 **bigint (epoch milliseconds)** 타입입니다. `to_timestamp()` 사용 시 `/1000` 변환 필수.

```sql
SELECT id, status, error_message, kfp_run_id,
       to_timestamp(created_at/1000) as created_time,
       to_timestamp(completed_at/1000) as completed_time
FROM pipeline_runs
WHERE status = 'failed'
ORDER BY created_at DESC
LIMIT 10;
```

### 주요 status 값

| status | 의미 |
|--------|------|
| `running` | KFP에서 실행 중 |
| `completed` | 모든 블록 성공 완료 |
| `failed` | KFP 실행 실패 또는 Run Not Found |
| `terminated` | 사용자 취소 |

## Step 2 — block_statuses 분석 (블록별 상태)

`block_statuses`는 JSON으로 각 블록의 개별 상태를 저장합니다.

```sql
-- block_statuses JSON 파싱
SELECT id,
       jsonb_each_text(block_statuses::jsonb) as block_status
FROM pipeline_runs
WHERE id = '{PIPELINE_RUN_ID}';
```

```sql
-- 실패한 블록만 추출
SELECT id, key as block_id, value as block_status
FROM pipeline_runs,
     jsonb_each_text(block_statuses::jsonb)
WHERE id = '{PIPELINE_RUN_ID}'
  AND value != 'completed'
  AND value != 'running';
```

### Block ID 해석

Watcher의 `resolveBlockIDs()` 함수가 KFP의 type 기반 키를 실제 `block_id`로 변환합니다:
- `__type__load_dataset` → 실제 UUID block_id
- `__type__sft` → SFT 학습 블록의 UUID
- 중복 타입은 `_2`, `_3` 접미사 추가

## Step 3 — block_pods 분석 (블록별 Pod 정보)

`block_pods`는 JSON으로 각 블록이 실행된 Pod 정보를 저장합니다.

```sql
-- block_pods JSON 파싱
SELECT id,
       key as block_id,
       value->>'pod_name' as pod_name,
       value->>'namespace' as namespace,
       value->>'container_name' as container_name,
       value->>'status' as pod_status
FROM pipeline_runs,
     jsonb_each(block_pods::jsonb)
WHERE id = '{PIPELINE_RUN_ID}';
```

### 블록 Pod 로그 조회

```bash
# block_pods에서 추출한 pod_name으로 로그 확인
kubectl logs {POD_NAME} -n {NAMESPACE} -c {CONTAINER_NAME}

# 이전 로그 (크래시된 경우)
kubectl logs {POD_NAME} -n {NAMESPACE} -c {CONTAINER_NAME} --previous

# Pod 상세 (Events 확인)
kubectl describe pod {POD_NAME} -n {NAMESPACE}
```

## Step 4 — KFP Run Not Found 처리

**Watcher 감지**: KFP API 응답이 404인 경우 자동으로 `failed` 처리

```sql
-- "Run not found" 에러 확인
SELECT id, status, error_message, kfp_run_id
FROM pipeline_runs
WHERE error_message LIKE '%not found%'
ORDER BY created_at DESC;
```

| error_message | 원인 | 조치 |
|--------------|------|------|
| `KFP run not found (deleted or expired from KFP server)` | KFP 서버에서 Run이 삭제/만료됨 | KFP 서버 상태 확인, Run retention 설정 점검 |

```bash
# KFP 서버 상태 확인
kubectl get pods -n kubeflow | grep -i pipeline

# KFP API 서버 로그
kubectl logs -n kubeflow -l app=ml-pipeline --tail=100
```

## Step 5 — KFP Proxy 연결 확인

Pipeline Watcher는 KFP Proxy를 통해 KFP 서버와 통신합니다.

```bash
# KFP Proxy 상태 확인
kubectl get pods -n ai-platform -l app=kfp-proxy

# KFP Proxy 로그
kubectl logs -n ai-platform -l app=kfp-proxy --tail=100

# Task Runner 로그에서 Pipeline 관련 에러
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=200 | grep -i "pipeline\|kfp\|error"
```

## Step 5.5 — Istio AuthorizationPolicy 검사 (403 Forbidden 에러)

`error_message`에 `(403) Reason: Forbidden` 또는 `server: istio-envoy`가 포함된 경우,
Istio 서비스 메시의 RBAC 정책이 KFP 통신을 차단하고 있을 가능성이 높습니다.

```sql
-- 403 에러 파이프라인 조회
SELECT id, LEFT(error_message, 300) AS err, kfp_run_id
FROM pipeline_runs
WHERE error_message LIKE '%403%' OR error_message LIKE '%Forbidden%'
ORDER BY updated_at DESC LIMIT 10;
```

```bash
# 1. 글로벌 deny-all 정책 존재 여부 확인
kubectl get authorizationpolicy -n istio-system

# 2. KFP 프로필 네임스페이스의 AuthorizationPolicy 확인
#    (파이프라인이 실행되는 네임스페이스, e.g. yunjae-park-kf-profile)
kubectl get authorizationpolicy -n {KF_PROFILE_NAMESPACE}

# 3. Task Runner의 ServiceAccount 확인
kubectl get deployment ai-platform-backend-go-task-runner -n ai-platform \
  -o jsonpath='{.spec.template.spec.serviceAccountName}'

# 4. Task Runner SA에 대한 ALLOW 규칙이 KFP 네임스페이스에 존재하는지 확인
kubectl get authorizationpolicy -A -o json | python3 -c "
import json,sys
data = json.load(sys.stdin)
for item in data.get('items',[]):
    ns = item['metadata']['namespace']
    name = item['metadata']['name']
    spec = json.dumps(item.get('spec',{}))
    if 'ai-platform' in spec:
        print(f'{ns}/{name}: includes ai-platform reference')
"
```

| 진단 결과 | 원인 | 조치 |
|-----------|------|------|
| `global-deny-all` 존재 + ai-platform ALLOW 없음 | Istio RBAC가 ai-platform → KFP 네임스페이스 통신 차단 | KFP 프로필 네임스페이스에 ai-platform 네임스페이스 허용 AuthorizationPolicy 추가 |
| `kfp_run_id`가 `pending-*` 형태 | KFP Run이 생성조차 되지 않음 (Proxy 접근 차단) | KFP Proxy → KFP API 서버 간 AuthorizationPolicy 확인 |

## Step 6 — 일반적인 블록별 장애 원인

### 6.1 데이터 로딩 블록 (load_dataset)

| 증상 | 원인 | 조치 |
|------|------|------|
| Pod OOMKilled | 데이터셋 크기 대비 메모리 부족 | 리소스 limit 증가 |
| S3 접근 에러 | S3 인증 실패 | S3 credential Secret 확인 |
| 데이터셋 없음 | 경로 오류 | 데이터셋 ID/경로 검증 |

### 6.2 학습 블록 (SFT, DPO, GRPO, CPT, GKD)

| 증상 | 원인 | 조치 |
|------|------|------|
| CUDA OOM | GPU 메모리 부족 | batch_size 줄이기, gradient_checkpointing 활성화 |
| Pod Pending | GPU 노드 부족 | GPU 가용성 확인 |
| 모델 다운로드 실패 | HF 토큰/네트워크 문제 | HF Secret, 네트워크 접근성 확인 |
| NaN loss | 학습률/데이터 문제 | hyperparameter 점검 |

### 6.3 모델 저장/병합 블록

| 증상 | 원인 | 조치 |
|------|------|------|
| S3 업로드 실패 | S3 인증/용량 | S3 설정 확인 |
| 디스크 부족 | PVC 용량 초과 | PVC 크기 증가 |

## Step 7 — 파이프라인 재실행

파이프라인 실패 원인을 해결한 후:

1. UI에서 동일 파이프라인 재실행
2. 또는 DB에서 status를 수동 초기화 (주의 필요):
   ```sql
   -- 관리자 전용, 운영 승인 필요
   UPDATE pipeline_runs
   SET status = 'running', error_message = NULL, completed_at = NULL
   WHERE id = '{PIPELINE_RUN_ID}';
   ```

## Step 8 — Source Code Change Analysis

RCA 분석 시 최근 소스코드 변경사항을 함께 확인하여 코드 변경이 장애의 원인인지 판단합니다.

### 8.1 최근 변경 이력 (Last 14 Days)

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/pipeline/ \
  backend/go/internal/kfp/
```

### 8.2 핵심 파일 소유자 및 최근 수정자 확인

```bash
# watcher.go 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/pipeline/watcher.go \
  | sort | uniq -c | sort -rn

# 핵심 함수 변경 이력 (KFP 상태 동기화 로직)
git -C ai-platform log --since="30 days ago" -p \
  -S "syncRunStatus" -- backend/go/internal/runner/pipeline/watcher.go

# KFP Proxy 변경 이력
git -C ai-platform log --since="30 days ago" -p \
  -S "GetRun" -- backend/go/internal/kfp/
```

### 8.3 장애 시점과 코드 변경 시점 상관관계

1. Step 1의 DB 쿼리에서 확인한 장애 발생 시각(`completed_at` 또는 `updated_at`, epoch ms → `to_timestamp()`)을 기준으로 합니다
2. 해당 시각 전후 커밋 확인:
   ```bash
   git -C ai-platform log --since="{ERROR_DATE} -3 days" \
     --until="{ERROR_DATE}" \
     --format="%h | %an | %ad | %s" --date=iso -- \
     backend/go/internal/runner/pipeline/ \
     backend/go/internal/kfp/
   ```
3. 커밋 상세 확인:
   ```bash
   git -C ai-platform show {COMMIT_HASH} --stat
   ```

### 8.4 Helm Chart 변경 확인

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

| 상수 | 값 | 용도 |
|------|------|------|
| `PipelineWatchInterval` | 10초 | KFP 상태 동기화 주기 |
| `PipelineWatchMaxConcurrency` | 5 | 동시 KFP API 호출 수 |

## Source Code Reference

- Pipeline Watcher: `ai-platform/backend/go/internal/runner/pipeline/watcher.go`
- KFP Proxy: `ai-platform/backend/go/internal/kfp/`
- Pipeline Model: `ai-platform/backend/go/internal/server/model/pipeline/`

---

## Git 커밋 귀인 분석 (필수)

> **반드시 수행**: "언제 누가 어떤 작업을 했는데 문제가 발생한 것인지?" 질문에 답해야 합니다.

RCA 완료 후 근본 원인과 관련된 코드/설정 변경의 커밋 이력을 추적하여 인과 관계 타임라인을 작성합니다.

### 관련 파일 커밋 이력 조회

```bash
git -C ai-platform log --since="30 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/pipeline/ \
  backend/go/internal/kfp/

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
   `outputs/demo-rca/{date}/pipeline-rca.md`에 저장
2. `md-to-notion` 스킬 또는 Notion MCP `notion-create-pages`로
   "AI Platform Demo 환경 RCA 리포트" (ID: `34e9eddc34e680f78eacfea0a60270b3`) 하위에 업로드
3. 생성된 노션 페이지 URL을 사용자에게 제공

> **참고**: pipe 테이블은 Notion에서 렌더링되지 않으므로 HTML `<table>` 태그로 변환하여 업로드합니다.
