---
name: demo-rca-orchestrator
description: >-
  Unified entry point for AI Platform Demo RCA.
  Routes to the correct component-specific RCA skill based on error context:
  workload errors → demo-workload-rca, endpoint/serverless errors →
  demo-serverless-rca, pipeline errors → demo-pipeline-rca.
  Follows the SRE Knowledge Layer pattern — injects component-specific
  troubleshooting context at query time.
  Use when the user asks to "debug demo", "demo error", "demo RCA",
  "데모 에러", "데모 장애", "데모 트러블슈팅", "demo-rca-orchestrator",
  "AI 플랫폼 데모 에러", "어디서 에러나는지 모르겠어",
  "데모 환경 장애 분석", "demo troubleshoot",
  or encounters an error in the Demo environment but is unsure which
  component is affected. Also use as a starting point when the
  specific component is not yet identified.
  Do NOT use for production environment troubleshooting.
metadata:
  author: "thaki"
  version: "1.0.0"
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

## Phase 1 — 컴포넌트 식별

에러가 발생한 컴포넌트를 식별합니다. 확실하지 않으면 DB에서 최근 실패 건을 조회합니다.

### Prerequisites

```bash
# Demo 클러스터 전환
kubectx tkai-demo

# DB 포트포워딩 (demo-db-connect 스킬 참조)
kubectl -n postgresql port-forward svc/postgresql 15432:5432
```

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

### 판별 기준 상세

- **UI에서 "Workloads" 메뉴**: → `demo-workload-rca`
- **UI에서 "Serverless" 또는 "Endpoints" 메뉴**: → `demo-serverless-rca`
- **UI에서 "Pipeline Builder" 메뉴**: → `demo-pipeline-rca`
- **에러 메시지에 `kfp_run_id` 포함**: → `demo-pipeline-rca`
- **에러 메시지에 `HSO` 또는 `httpscaledobject` 포함**: → `demo-serverless-rca`
- **에러 메시지에 `helm` 또는 `deployment` 포함**: → 추가 확인 필요 (workload/endpoint 모두 Helm 사용)

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
