---
name: demo-rca-orchestrator
description: >-
  Unified entry point for AI Platform Demo RCA.
  Routes to the correct component-specific RCA skill based on error context:
  workload errors → demo-workload-rca, endpoint/serverless errors →
  demo-serverless-rca, pipeline errors → demo-pipeline-rca,
  text generation errors → demo-text-generation-rca,
  devspace errors → demo-devspace-rca, tabular/ML Studio errors →
  demo-tabular-rca, benchmark errors → demo-benchmark-rca,
  volume/storage errors → demo-volume-rca.
  Follows the SRE Knowledge Layer pattern — injects component-specific
  troubleshooting context at query time.
  Use when the user asks to "debug demo", "demo error", "demo RCA",
  "데모 에러", "데모 장애", "데모 트러블슈팅", "demo-rca-orchestrator",
  "AI 플랫폼 데모 에러", "어디서 에러나는지 모르겠어",
  "데모 환경 장애 분석", "demo troubleshoot",
  "devspace error", "devspace 에러", "tabular error", "ML Studio 에러",
  "benchmark error", "벤치마크 에러", "volume error", "볼륨 에러",
  "storage error", "스토리지 에러",
  or encounters an error in the Demo environment but is unsure which
  component is affected. Also use as a starting point when the
  specific component is not yet identified.
  Do NOT use for production environment troubleshooting.
metadata:
  author: "thaki"
  version: "3.0.0"
  category: "infra"
  platforms: [darwin]
---

# Demo RCA Orchestrator

AI Platform Demo 환경의 에러를 컴포넌트별로 라우팅하여 올바른 RCA 스킬로 안내하는 통합 진입점입니다.

## SRE Knowledge Layer 접근법

SRE 컨설팅 내용에 따라, 하나의 범용 트러블슈팅 대신 **컴포넌트별 지식 계층(Knowledge Layer)을 쿼리 시점에 주입**합니다. 이를 통해:
- 각 컴포넌트의 정확한 Watcher 로직과 임계값이 적용됩니다
- 불필요한 정보 없이 해당 장애에 집중할 수 있습니다
- 새로운 장애 유형 추가 시 해당 스킬만 업데이트하면 됩니다

## Phase 0 — Pre-flight (한 번에 실행)

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

### 사용자 프로젝트 네임스페이스 찾기

사용자 이메일로 프로젝트 네임스페이스를 조회합니다. Demo 환경의 네임스페이스 패턴: `project-{uuid}`

```sql
SELECT p.id, p.name, ns.name AS namespace
FROM projects p
  JOIN namespaces ns ON p.namespace_id = ns.id
  JOIN project_members pm ON pm.project_id = p.id
  JOIN users u ON u.id = pm.user_id
WHERE u.email = '{USER_EMAIL}'
  AND p.deleted_at IS NULL;
```

또는 kubectl로 직접 확인:

```bash
kubectl get ns | grep project-
```

## Phase 1 — 컴포넌트 식별

에러가 발생한 컴포넌트를 식별합니다. 확실하지 않으면 DB에서 최근 실패 건을 조회합니다.

### 빠른 진단: 최근 실패 건 조회

> **주의**: `updated_at`, `created_at` 컬럼은 **bigint (epoch milliseconds)** 타입입니다. `to_timestamp()` 사용 시 `/1000` 변환 필수.

```sql
-- Workload 실패
SELECT 'WORKLOAD' as component, id, name, status, LEFT(status_message, 200) AS msg,
       to_timestamp(updated_at/1000) as failed_at
FROM workloads
WHERE status IN ('failed','error') AND deleted_at IS NULL
ORDER BY updated_at DESC LIMIT 5;

-- Endpoint 실패
SELECT 'ENDPOINT' as component, id, name, status, LEFT(status_message, 200) AS msg,
       to_timestamp(updated_at/1000) as failed_at
FROM endpoints
WHERE status IN ('failed','error') AND deleted_at IS NULL
ORDER BY updated_at DESC LIMIT 5;

-- Pipeline 실패
SELECT 'PIPELINE' as component, id, pipeline_name, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at/1000) as failed_at
FROM pipeline_runs
WHERE status = 'failed'
ORDER BY updated_at DESC LIMIT 5;

-- DevSpace 실패
SELECT 'DEVSPACE' as component, id, name, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at) as failed_at
FROM devspaces
WHERE status = 'failed' AND deleted_at IS NULL
ORDER BY updated_at DESC LIMIT 5;

-- Tabular (ML Studio) 실패
SELECT 'TABULAR' as component, id, name, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at) as failed_at
FROM tabular_experiments
WHERE status = 'failed'
ORDER BY updated_at DESC LIMIT 5;

-- Benchmark 실패
SELECT 'BENCHMARK' as component, id, name, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at) as failed_at
FROM benchmark_runs
WHERE status = 'failed'
ORDER BY updated_at DESC LIMIT 5;

-- Volume (Storage) 실패
SELECT 'VOLUME' as component, id, name, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at) as failed_at
FROM storage_volumes
WHERE status = 'ERROR'
ORDER BY updated_at DESC LIMIT 5;

-- Snapshot 실패
SELECT 'SNAPSHOT' as component, id, name, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at) as failed_at
FROM volume_snapshots
WHERE status = 'ERROR'
ORDER BY updated_at DESC LIMIT 5;

-- Restore 실패
SELECT 'RESTORE' as component, id, status, LEFT(error_message, 200) AS err,
       to_timestamp(updated_at) as failed_at
FROM restore_jobs
WHERE status = 'FAILED'
ORDER BY updated_at DESC LIMIT 5;
```

### 현재 비정상 상태 리소스 조회

```sql
-- 현재 creating/starting 상태에서 멈춘 리소스 (15분 초과)
-- updated_at은 bigint epoch ms이므로 now()도 epoch ms로 변환
SELECT 'WORKLOAD' as type, id, name, status,
       to_timestamp(updated_at/1000) as last_updated,
       ROUND((EXTRACT(epoch FROM now())*1000 - updated_at)/60000) AS minutes_stuck
FROM workloads
WHERE status IN ('creating', 'starting', 'building', 'pulling') AND deleted_at IS NULL
  AND updated_at < EXTRACT(epoch FROM now())*1000 - 900000

UNION ALL

SELECT 'ENDPOINT' as type, id, name, status,
       to_timestamp(updated_at/1000) as last_updated,
       ROUND((EXTRACT(epoch FROM now())*1000 - updated_at)/60000) AS minutes_stuck
FROM endpoints
WHERE status IN ('creating', 'starting') AND deleted_at IS NULL
  AND updated_at < EXTRACT(epoch FROM now())*1000 - 900000

ORDER BY minutes_stuck DESC;
```

## Phase 2 — 컴포넌트별 라우팅

| 에러 컴포넌트 | 라우팅 대상 | 주요 판별 기준 |
|--------------|-----------|---------------|
| **Workloads** (컨테이너, 배치, 학습) | `demo-workload-rca` | `workloads` 테이블, `k8s_deployment_name` |
| **Serverless / Endpoints** (모델 서빙) | `demo-serverless-rca` | `endpoints` 테이블, HSO, KEDA |
| **Pipeline Builder** (KFP 파이프라인) | `demo-pipeline-rca` | `pipeline_runs` 테이블, `kfp_run_id` |
| **Text Generation** (LLM 파인튜닝) | `demo-text-generation-rca` | `text_generation_experiments` 테이블, TrainJob |
| **DevSpace** (개발 환경) | `demo-devspace-rca` | `devspaces` 테이블, Deployment, PVC |
| **Tabular / ML Studio** (테이블 학습) | `demo-tabular-rca` | `tabular_experiments` 테이블, TrainJob, `training_mode` |
| **Benchmark** (모델 벤치마크) | `demo-benchmark-rca` | `benchmark_runs` 테이블, K8s Job, `lm-eval` |
| **Volume / Storage** (스토리지) | `demo-volume-rca` | `storage_volumes`, `volume_snapshots`, `restore_jobs` 테이블, PVC |

### 판별 기준 상세

- **UI에서 "Workloads" 메뉴**: → `demo-workload-rca`
- **UI에서 "Serverless" 또는 "Endpoints" 메뉴**: → `demo-serverless-rca`
- **UI에서 "Pipeline Builder" 메뉴**: → `demo-pipeline-rca`
- **UI에서 "Text Generation" 메뉴**: → `demo-text-generation-rca`
- **UI에서 "DevSpace" 메뉴**: → `demo-devspace-rca`
- **UI에서 "ML Studio" 또는 "Tabular" 메뉴**: → `demo-tabular-rca`
- **UI에서 "Benchmark" 메뉴**: → `demo-benchmark-rca`
- **UI에서 "Volume" 또는 "Storage" 메뉴**: → `demo-volume-rca`
- **에러 메시지에 `kfp_run_id` 포함**: → `demo-pipeline-rca`
- **에러 메시지에 `HSO` 또는 `httpscaledobject` 포함**: → `demo-serverless-rca`
- **에러 메시지에 `helm` 또는 `deployment` 포함**: → 추가 확인 필요 (workload/endpoint 모두 Helm 사용)
- **에러 메시지에 `TrainJob` 포함**: → `tabular_experiments` 또는 `text_generation_experiments` 확인
- **에러 메시지에 `lm-eval` 또는 `benchmark` 포함**: → `demo-benchmark-rca`
- **에러 메시지에 `PVC`, `VolumeSnapshot`, `StorageClass` 포함**: → `demo-volume-rca`
- **에러 메시지에 `devspace` 또는 `IDE` 포함**: → `demo-devspace-rca`

## Phase 2.5 — Source Code Change Analysis

컴포넌트별 RCA 라우팅과 병행하여, 최근 소스코드 변경사항을 분석하여 코드 변경이 장애의 원인인지 판단합니다.

### 2.5.1 최근 변경 이력 (Last 14 Days)

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/workload/ \
  backend/go/internal/runner/endpoint/ \
  backend/go/internal/runner/pipeline/ \
  backend/go/internal/runner/devspace/ \
  backend/go/internal/runner/mlstudio/tabular/ \
  backend/go/internal/runner/benchmark/ \
  backend/go/internal/runner/storage/ \
  backend/go/internal/k8sclient/
```

### 2.5.2 핵심 파일 소유자 및 최근 수정자 확인

```bash
# Workload watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/workload/status_watcher.go \
  | sort | uniq -c | sort -rn

# Endpoint watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/endpoint/watcher_sync.go \
  | sort | uniq -c | sort -rn

# Pipeline watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/pipeline/watcher.go \
  | sort | uniq -c | sort -rn

# DevSpace watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/devspace/devspace_watcher.go \
  | sort | uniq -c | sort -rn

# Tabular watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/mlstudio/tabular/tabular_watcher.go \
  | sort | uniq -c | sort -rn

# Benchmark watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/benchmark/watcher.go \
  | sort | uniq -c | sort -rn

# Storage volume watcher 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/storage/volume_watcher.go \
  | sort | uniq -c | sort -rn
```

### 2.5.3 장애 시점과 코드 변경 시점 상관관계

1. Phase 1의 DB 쿼리에서 확인한 장애 발생 시각(`failed_at`)을 기준으로 합니다
2. 해당 시각 전후 커밋 확인:
   ```bash
   git -C ai-platform log --since="{ERROR_DATE} -3 days" \
     --until="{ERROR_DATE}" \
     --format="%h | %an | %ad | %s" --date=iso -- \
     backend/go/internal/runner/ \
     backend/go/internal/k8sclient/
   ```
3. 커밋 상세 확인:
   ```bash
   git -C ai-platform show {COMMIT_HASH} --stat
   ```

### 2.5.4 Helm Chart 변경 확인

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

## Phase 3 — 공통 인프라 점검

컴포넌트 특정 RCA 전에, 공통 인프라 문제를 먼저 배제합니다.

### 3.1 Task Runner 상태

```bash
kubectl get pods -n ai-platform -l app=ai-platform-backend-go
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=50 | grep -i "error\|panic\|fatal"
```

### 3.2 NATS JetStream 상태

```bash
kubectl get pods -n nats
kubectl exec -n nats svc/nats -- nats stream ls
kubectl exec -n nats svc/nats -- nats consumer ls {STREAM_NAME}
```

### 3.3 PostgreSQL 상태

```bash
kubectl get pods -n postgresql
kubectl logs -n postgresql -l cnpg.io/cluster=postgresql --tail=20
```

### 3.4 GPU 노드 가용성

```bash
kubectl get nodes -o custom-columns='NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu,STATUS:.status.conditions[?(@.type=="Ready")].status'
kubectl top nodes
```

## Phase 4 — 최종 리포트에 대한 참조

종합 RCA 리포트: `outputs/demo-rca/2026-04-25/ai-platform-demo-rca-report.md`

이 리포트에는 아키텍처 다이어그램, 장애 유형별 매트릭스, 전체 명령어 레퍼런스,
그리고 SRE Knowledge Layer 연계 방안이 포함되어 있습니다.

## Source Code Reference

- Workload Watcher: `ai-platform/backend/go/internal/runner/workload/status_watcher.go`
- Endpoint Watcher: `ai-platform/backend/go/internal/runner/endpoint/watcher_sync.go`
- Pipeline Watcher: `ai-platform/backend/go/internal/runner/pipeline/watcher.go`
- K8s Client: `ai-platform/backend/go/internal/k8sclient/`
- DB Connection: `.cursor/skills/infra/demo-db-connect/SKILL.md`
- SRE Reference: `outputs/sre-email-response/2026-04-23/tenant-aware-aiops-proposal.md`
