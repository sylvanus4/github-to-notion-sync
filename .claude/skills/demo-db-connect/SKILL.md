---
name: demo-db-connect
description: >-
  Connect to TKAI Demo environment PostgreSQL databases via kubectl
  port-forward. Two databases exist: ai_platform_db (AI Platform core, 105
  tables) and tkai_agents (Agent Studio). Both run on the same CNPG cluster in
  the postgresql namespace. Use when the user asks to "connect demo DB", "demo
  database", "demo postgres", "demo DB 접속", "데모 DB", "데모 데이터베이스", "AI Platform
  DB", "ai_platform_db", "에이전트 스튜디오 DB", "tkai_agents", "demo-db-connect", or
  needs to access the Demo cluster's PostgreSQL for troubleshooting or data
  inspection. Do NOT use for dev environment DB (use dev-specific kubeconfig
  context). Do NOT use for cluster context switching only (use
  kube-cluster-switch). Do NOT use for production DB access.
---

# Demo DB Connect

## Architecture Overview

Demo 환경의 PostgreSQL은 `postgresql` 네임스페이스에서 **CloudNativePG(CNPG)** 오퍼레이터가 관리하는 단일 클러스터로 운영됩니다. 이 클러스터 안에 용도별 데이터베이스가 분리되어 있습니다.

| DB명 | 용도 | 테이블 수 | 네임스페이스 | 서비스 |
|------|------|-----------|-------------|--------|
| `ai_platform_db` | **AI Platform 코어** (컴퓨트, 스토리지, 모델서빙, IAM, 빌링 등) | 105 | `postgresql` | `svc/postgresql` |
| `tkai_agents` | Agent Studio (에이전트, 워크플로우, 도구) | ~30 | `postgresql` | `svc/postgresql` |
| `airflow` | Airflow 메타데이터 | - | `postgresql` | `svc/postgresql` |
| `mcp` | MCP 서비스 | - | `postgresql` | `svc/postgresql` |

> **주의**: `ai-platform` 네임스페이스에는 DB 서비스가 없습니다. DB 설정은 해당 네임스페이스의 ConfigMap/Secret에 있지만, 실제 PostgreSQL 서비스는 `postgresql` 네임스페이스입니다.

## Constraints

- **Freedom level: Low** — production-adjacent environment; follow exact step sequences
- VPN connection is **required** before any kubectl command
- Do NOT run DDL mutations (DROP, ALTER, TRUNCATE) without explicit user approval
- Credentials reference `.secrets/infra-runbooks/TKAI-시크릿.md` — never echo passwords in chat output
- Port 5432 conflicts: if another port-forward or local PostgreSQL is running, use an alternate local port (e.g., `15432:5432`)

## Prerequisites

| Tool | Check command | Install |
|------|---------------|---------|
| kubectl | `kubectl version --client` | `brew install kubectl` |
| kubecm | `kubecm version` | `brew install kubecm` |
| kubectx | `kubectx --help` | `brew install kubectx` |
| psql | `psql --version` | `brew install libpq && brew link --force libpq` |

## Procedure

### Step 1 — Register kubeconfig (one-time)

Check if the `tkai-demo` context already exists:

```bash
kubecm list | grep -i demo
```

If not registered, merge the demo kubeconfig:

```bash
kubecm add -f ~/.kube/tkai-demo.config \
  --config ~/.kube/config \
  --context-name tkai-demo \
  --cover
```

### Step 2 — Switch context

```bash
kubectx tkai-demo
```

Verify:

```bash
kubectl cluster-info
```

### Step 3 — Confirm PostgreSQL service

PostgreSQL은 `postgresql` 네임스페이스의 CNPG 클러스터입니다:

```bash
kubectl -n postgresql get svc
```

Expected: `postgresql` (rw, port 5432), `postgresql-r` (read-only), `postgresql-ro` (read-only)

DB 접속 정보 확인 (ai-platform 네임스페이스의 ConfigMap):

```bash
kubectl -n ai-platform get configmap ai-platform-backend-go-server-config \
  -o jsonpath='{.data}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for k in sorted(data):
    if 'DATABASE' in k or 'DB' in k:
        print(f'{k} = {data[k]}')"
```

### Step 4 — Port-forward

```bash
kubectl -n postgresql port-forward svc/postgresql 15432:5432
```

> 로컬 PostgreSQL이 5432를 사용하므로 `15432` 사용을 권장합니다. 백그라운드로 실행하려면 끝에 `&`를 추가하세요.

### Step 5 — Connect with psql

**AI Platform DB** (핵심 플랫폼 데이터 — 대부분의 경우 이것을 사용):

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db
```

테이블 목록 확인:

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db -c "\dt+ public.*"
```

**Agent Studio DB**:

```bash
PGPASSWORD=tkai_password psql -h localhost -p 15432 -U tkai_user -d tkai_agents
```

### Credentials reference

소스: `.secrets/infra-runbooks/TKAI-시크릿.md`, K8s Secret/ConfigMap

| 용도 | DB명 | 사용자 | 비밀번호 | K8s Secret |
|------|------|--------|----------|------------|
| AI Platform | `ai_platform_db` | `postgres` | `password` | `postgresql-secret` (ns: `ai-platform`) |
| Agent Studio | `tkai_agents` | `tkai_user` | `tkai_password` | `postgresql-secret` (ns: `tkai-agents`) |
| Airflow | `airflow` | `airflow` | `airflow` | - |
| MCP | `mcp` | `mcp_user` | `mcp_password` | - |

## AI Platform DB 테이블 카테고리 (105 tables)

| 카테고리 | 주요 테이블 |
|----------|-------------|
| IAM/사용자 | `users`, `groups`, `roles`, `permissions`, `user_groups`, `role_permissions` |
| 프로젝트/워크스페이스 | `projects`, `workspaces`, `project_members` |
| 컴퓨트/GPU | `gpu_nodes`, `gpu_devices`, `gpu_pools`, `gpu_pool_gpus` |
| 컨테이너/서빙 | `containers`, `container_ports`, `container_volumes`, `container_env_vars` |
| 모델 서빙 | `model_serving_deployments`, `model_serving_endpoints`, `model_serving_api_keys` |
| 스토리지 | `storage_volumes`, `storage_pvc`, `storage_classes` |
| 빌링/미터링 | `billing_accounts`, `billing_plans`, `billing_usage_records`, `metering_records` |
| 모니터링/알림 | `monitoring_dashboards`, `monitoring_alerts`, `alert_rules`, `alert_notifications` |
| 이미지/레지스트리 | `container_images`, `image_registries`, `image_registry_credentials` |
| 파이프라인/스케줄링 | `pipelines`, `pipeline_runs`, `schedules` |
| 클러스터/노드 | `clusters`, `cluster_nodes`, `node_pools` |
| 네트워크/보안 | `network_policies`, `secrets`, `ssh_keys`, `api_keys` |
| 감사/로깅 | `audit_logs`, `activity_logs` |

## Troubleshooting

| 증상 | 원인 | 해결 |
|------|------|------|
| `Unable to connect to the server` | VPN 미연결 | VPN 연결 후 재시도 |
| `error: context "tkai-demo" not found` | kubeconfig 미등록 | Step 1 실행 |
| `bind: address already in use` | 로컬 포트 충돌 | `lsof -i :15432`로 확인 후 종료, 또는 다른 포트 사용 |
| `FATAL: password authentication failed` | 크리덴셜 불일치 | `.secrets/infra-runbooks/TKAI-시크릿.md` 확인 |
| `FATAL: database "X" does not exist` | DB명 오타 | `\l`로 DB 목록 확인 |
| `port-forward` 끊김 | 네트워크 불안정 또는 Pod 재시작 | 다시 `port-forward` 실행 |
| `ai-platform` ns에 postgres svc 없음 | DB는 `postgresql` ns에 있음 | `kubectl -n postgresql get svc` 사용 |
