---
name: demo-rca-live
description: >-
  Live AI Platform Demo environment monitor that logs into the demo site,
  navigates Workloads / Serverless / Pipeline Builder pages, detects UI-visible
  errors and anomalies, cross-references with kubectl and psql backend data,
  and generates a timestamped Markdown report with root-cause analysis and
  resolution proposals. Composes demo-rca-orchestrator, demo-workload-rca,
  demo-serverless-rca, demo-pipeline-rca, and demo-db-connect.
  Use when the user asks to "live RCA", "demo RCA live", "demo-rca-live",
  "실시간 데모 점검", "데모 라이브 RCA", "데모 문제 수집", "데모 환경 체크",
  "라이브 데모 모니터링", "AI 플랫폼 데모 상태 점검",
  "데모 에러 수집 및 리포트", or wants an end-to-end live health check
  of the AI Platform Demo environment with a consolidated report.
  Do NOT use for production environment monitoring.
  Do NOT use for static RCA without live checks (use demo-rca-orchestrator).
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "infra"
  platforms: [darwin]
---

# Demo RCA Live

AI Platform Demo 환경에 실시간으로 접속하여 UI + 인프라 + DB를 종합 점검하고,
발견된 문제와 해결 방안을 타임스탬프 리포트로 생성합니다.

## Output

`outputs/demo-rca-live/{YYYY-MM-DD}/report-{HHmmss}.md`

하루에 여러 번 실행해도 파일이 중복되지 않도록 시분초를 포함합니다.

## Execution — 6-Phase Pipeline

### Phase 0 — Pre-flight (한 번에 실행)

VPN 연결 상태에서 아래 블록을 순서대로 실행합니다. 이미 활성 상태이면 건너뜁니다.

```bash
# 1. VPN 연결 확인
curl -s -o /dev/null -w '%{http_code}' https://suite-demo.thakicloud.net/desktop

# 2. 클러스터 컨텍스트 전환
kubectx tkai-demo

# 3. DB 포트포워딩 (백그라운드, 이미 열려 있으면 건너뛰기)
lsof -i :15432 >/dev/null 2>&1 && echo "Port 15432 already forwarded" \
  || kubectl -n postgresql port-forward svc/postgresql 15432:5432 &
```

#### DB 접속 Quick Reference

| DB | 커맨드 |
|----|--------|
| ai_platform_db | `PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db` |
| tkai_agents | `PGPASSWORD=tkai_password psql -h localhost -p 15432 -U tkai_user -d tkai_agents` |

#### 로그인 정보

`.secrets/infra-runbooks/Demo-웹-로그인.md` 참조

### Phase 1 — Infrastructure Pre-flight

인프라 기본 상태를 먼저 확인합니다. 여기서 치명적 장애가 있으면 이후 단계에 영향을 줍니다.

#### 1.1 핵심 서비스 상태 확인

```bash
# Backend API server
kubectl get pods -n ai-platform -l app=ai-platform-backend-go -o wide

# NATS JetStream
kubectl get pods -n nats

# PostgreSQL CNPG
kubectl get pods -n postgresql

# GPU 노드 가용성
kubectl get nodes -o custom-columns='NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu,STATUS:.status.conditions[?(@.type=="Ready")].status'
```

### Phase 2 — DB Scan (Failed / Stuck Resources)

`demo-rca-orchestrator`의 SQL 쿼리를 실행하여 현재 실패 또는 멈춘 리소스를 수집합니다.

#### 2.1 최근 실패 리소스

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' <<'SQL'
SELECT 'WORKLOAD' as component, id::text, name, status, status_message,
       to_timestamp(updated_at/1000)::text as failed_at
FROM workloads
WHERE status = 'failed' AND deleted_at IS NULL
ORDER BY updated_at DESC LIMIT 10;
SQL
```

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' <<'SQL'
SELECT 'ENDPOINT' as component, id::text, name, status, status_message,
       to_timestamp(updated_at/1000)::text as failed_at
FROM endpoints
WHERE status = 'failed' AND deleted_at IS NULL
ORDER BY updated_at DESC LIMIT 10;
SQL
```

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' <<'SQL'
SELECT 'PIPELINE' as component, id::text, 'pipeline_run' as name,
       status, error_message as status_message,
       to_timestamp(updated_at/1000)::text as failed_at
FROM pipeline_runs
WHERE status = 'failed'
ORDER BY updated_at DESC LIMIT 10;
SQL
```

#### 2.2 Stuck 리소스 (creating/starting > 15분)

> **주의**: `updated_at`, `created_at` 컬럼은 **bigint (epoch milliseconds)** 타입입니다.

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' <<'SQL'
SELECT type, id::text, name, status, created::text, stuck_duration::text FROM (
  SELECT 'WORKLOAD' as type, id, name, status,
         to_timestamp(created_at/1000) as created,
         NOW() - to_timestamp(created_at/1000) as stuck_duration
  FROM workloads
  WHERE status IN ('creating', 'starting') AND deleted_at IS NULL
    AND created_at < EXTRACT(EPOCH FROM NOW() - INTERVAL '15 minutes') * 1000
  UNION ALL
  SELECT 'ENDPOINT' as type, id, name, status,
         to_timestamp(created_at/1000) as created,
         NOW() - to_timestamp(created_at/1000) as stuck_duration
  FROM endpoints
  WHERE status = 'creating' AND deleted_at IS NULL
    AND created_at < EXTRACT(EPOCH FROM NOW() - INTERVAL '15 minutes') * 1000
) sub
ORDER BY stuck_duration DESC;
SQL
```

#### 2.3 전체 리소스 상태 분포

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' <<'SQL'
SELECT 'WORKLOADS' as resource, status, count(*) as cnt
FROM workloads WHERE deleted_at IS NULL
GROUP BY status
UNION ALL
SELECT 'ENDPOINTS' as resource, status, count(*) as cnt
FROM endpoints WHERE deleted_at IS NULL
GROUP BY status
UNION ALL
SELECT 'PIPELINES' as resource, status, count(*) as cnt
FROM pipeline_runs
GROUP BY status
ORDER BY resource, status;
SQL
```

### Phase 3 — Browser UI Scan

`cursor-ide-browser` MCP를 사용하여 데모 사이트에 로그인하고 주요 화면을 순회합니다.

#### 3.1 로그인

1. `browser_navigate` → `https://suite-demo.thakicloud.net/desktop`
2. `browser_snapshot` → 로그인 페이지 확인
3. `browser_fill` username field → `aidev.humain`
4. `browser_fill` password field → `AIplatform1!`
5. 로그인 버튼 클릭 (`browser_click`)
6. `browser_snapshot` → 대시보드 도착 확인

#### 3.2 Workloads 페이지 점검

1. Workloads 메뉴 네비게이션
2. `browser_snapshot` + `browser_take_screenshot` → 화면 상태 캡처
3. 에러 배지, "Failed" 상태, 경고 아이콘 탐색
4. 에러가 있는 항목 클릭 → 상세 페이지 snapshot

#### 3.3 Serverless (Endpoints) 페이지 점검

1. Serverless/Endpoints 메뉴 네비게이션
2. `browser_snapshot` + `browser_take_screenshot`
3. "Failed", "Error", "Creating" 장기 체류 항목 탐색
4. 에러 항목 상세 확인

#### 3.4 Pipeline Builder 페이지 점검

1. Pipeline Builder 메뉴 네비게이션
2. `browser_snapshot` + `browser_take_screenshot`
3. 실패 파이프라인 런 탐색
4. 에러 상세 확인

### Phase 4 — K8s Deep Dive (Per Issue)

Phase 2/3에서 발견된 각 문제에 대해 컴포넌트별 RCA 스킬의 명령어를 실행합니다.

#### Workload 이슈 심층 분석 (demo-workload-rca 참조)

```bash
# 워크로드의 K8s 네임스페이스와 디플로이먼트 이름 조회
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' -c \
  "SELECT id, name, status, status_message, k8s_deployment_name,
          (SELECT ns.name FROM namespaces ns
           JOIN projects p ON p.namespace_id = ns.id
           JOIN workloads w2 ON w2.project_id = p.id
           WHERE w2.id = workloads.id) as namespace
   FROM workloads WHERE status = 'failed' AND deleted_at IS NULL
   ORDER BY updated_at DESC LIMIT 5;"
```

각 실패 워크로드에 대해:

```bash
kubectl get pods -n {NAMESPACE} -l app={DEPLOYMENT_NAME} -o wide
kubectl describe pod {POD_NAME} -n {NAMESPACE} | tail -30
kubectl logs {POD_NAME} -n {NAMESPACE} --previous --tail=50 2>/dev/null || echo "No previous logs"
kubectl logs {POD_NAME} -n {NAMESPACE} --tail=50
```

#### Endpoint 이슈 심층 분석 (demo-serverless-rca 참조)

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' -c \
  "SELECT id, name, status, status_message, endpoint_type
   FROM endpoints WHERE status = 'failed' AND deleted_at IS NULL
   ORDER BY updated_at DESC LIMIT 5;"
```

각 실패 엔드포인트에 대해:

```bash
kubectl get pods -n {NAMESPACE} | grep {ENDPOINT_NAME}
kubectl get httpscaledobject -n {NAMESPACE} | grep {ENDPOINT_NAME}
```

#### Pipeline 이슈 심층 분석 (demo-pipeline-rca 참조)

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -t -A -F '|' -c \
  "SELECT id, pipeline_id, status, error_message,
          kfp_run_id, block_statuses::text
   FROM pipeline_runs WHERE status = 'failed'
   ORDER BY updated_at DESC LIMIT 5;"
```

### Phase 5 — Report Generation

모든 수집 데이터를 종합하여 타임스탬프 리포트를 생성합니다.

#### 출력 경로

```bash
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)
OUTDIR="outputs/demo-rca-live/${DATE}"
mkdir -p "${OUTDIR}"
REPORT="${OUTDIR}/report-${TIME}.md"
```

#### 리포트 구조

```markdown
# AI Platform Demo — Live RCA Report

- **일시**: {YYYY-MM-DD HH:MM:SS KST}
- **클러스터**: tkai-demo
- **실행자**: agent (demo-rca-live)

## 1. 인프라 상태 요약

| 서비스 | 상태 | 비고 |
|--------|------|------|
| Backend API | ✅/❌ | ... |
| NATS JetStream | ✅/❌ | ... |
| PostgreSQL | ✅/❌ | ... |
| GPU Nodes | ✅/❌ | 가용 GPU: N개 |

## 2. 리소스 상태 분포

| 리소스 | running | creating | failed | stopped | 합계 |
|--------|---------|----------|--------|---------|------|
| Workloads | ... | ... | ... | ... | ... |
| Endpoints | ... | ... | ... | ... | ... |
| Pipelines | ... | ... | ... | ... | ... |

## 3. 발견된 문제 목록

### Issue #1: {컴포넌트} — {이름}

- **상태**: failed
- **status_message**: ...
- **발견 경로**: DB scan / UI scan
- **K8s 상태**: ...
- **Pod 로그 (요약)**: ...

#### 근본 원인 분석

...

#### 해결 방안

1. ...
2. ...

### Issue #2: ...

## 4. Stuck 리소스 (creating/starting > 15분)

| 유형 | ID | 이름 | 상태 | 체류 시간 |
|------|-----|------|------|-----------|
| ... | ... | ... | ... | ... |

## 5. UI 관찰 사항

- Workloads 페이지: ...
- Serverless 페이지: ...
- Pipeline Builder 페이지: ...

## 6. 권장 조치 요약

| 우선순위 | 조치 | 대상 | 예상 효과 |
|---------|------|------|-----------|
| P1 (즉시) | ... | ... | ... |
| P2 (금일) | ... | ... | ... |
| P3 (개선) | ... | ... | ... |
```

## Resolution Strategies Reference

### 공통 해결 전략

| 문제 유형 | 1차 시도 | 2차 시도 |
|-----------|---------|---------|
| `ImagePullBackOff` | 이미지 경로 확인, `imagePullSecrets` 점검 | 레지스트리 접근 테스트 (`curl -v`) |
| `CrashLoopBackOff` | `--previous` 로그 분석, exit code 확인 | 리소스 제한 조정, 환경변수 점검 |
| `OOMKilled` | `resources.limits.memory` 증가 | 애플리케이션 메모리 프로파일링 |
| `Unschedulable` | 노드 리소스 확인 (`kubectl top nodes`) | 리소스 요청 조정 또는 노드 스케일업 |
| `CreateContainerConfigError` | ConfigMap/Secret 존재 여부 확인 | 마운트 경로, 키 이름 점검 |
| Helm 실패 | `helm history` 확인, 롤백 가능 여부 판단 | `helm upgrade --install --force` |
| NATS 유실 | Task Runner 재시작, Consumer 상태 확인 | NATS 서비스 재배포 |
| HSO 미생성 | KEDA 상태 확인, Operator 로그 | KEDA 재설치 |
| KFP Run Not Found | `kfp_run_id` 유효성, KFP 서비스 상태 | KFP 컴포넌트 재시작 |
| PVC Pending | StorageClass 확인, PV 가용량 | 다른 StorageClass 시도 |
| Deployment 5분 미가용 | Pod Events, Readiness Probe 확인 | Probe 설정 조정, 타임아웃 증가 |

## Constraints

- **Freedom level: Low** — Demo 환경은 프로덕션 인접 환경
- 절대 DDL 변경(DROP, ALTER) 실행 금지
- 절대 `kubectl delete` 실행 금지 (리포트에 권장 조치로만 기록)
- DB 비밀번호를 리포트에 포함하지 않음
- 브라우저 세션은 점검 후 반드시 unlock (`browser_lock action: "unlock"`)

## Composed Skills

| 스킬 | 용도 |
|------|------|
| `demo-rca-orchestrator` | Phase 2 SQL 쿼리, 컴포넌트 라우팅 로직 |
| `demo-workload-rca` | Phase 4 워크로드 심층 분석 절차 |
| `demo-serverless-rca` | Phase 4 엔드포인트 심층 분석 절차 |
| `demo-pipeline-rca` | Phase 4 파이프라인 심층 분석 절차 |
| `demo-db-connect` | Phase 1 DB 포트포워딩 절차 |
| `cursor-ide-browser` MCP | Phase 3 브라우저 UI 스캔 |
