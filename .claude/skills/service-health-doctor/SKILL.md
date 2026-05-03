---
name: service-health-doctor
description: >-
  Diagnose and recover the local development stack — check health of all 24+
  microservices, detect port conflicts, analyze error logs, and auto-restart
  failed services. Use when the user reports service issues, asks to check
  health, or needs to troubleshoot the dev stack. Do NOT use for starting the
  full stack from scratch (use local-dev-runner) or reviewing infrastructure
  configuration (use sre-devops-expert). Korean triggers: "리뷰", "분석", "체크",
  "리포트".
disable-model-invocation: true
---

# Service Health Doctor

Diagnoses and recovers the local development stack (24 microservices + 5 infrastructure components).

## When to Use

- A service fails to start or returns errors
- The user says "X service is down" or "something is broken"
- As part of the `/incident-response` workflow (called by mission-control)
- After `git pull` or dependency changes that may break services

## Service Registry

5 infrastructure components (Docker) and 24 application services with HTTP `/health` endpoints. For the full registry with ports and tiers, see [references/service-registry.md](references/service-registry.md).

## Execution Steps

### Step 1: Run Status Script

```bash
bash scripts/dev-status.sh
```

Parse the output to categorize services as UP / HEALTHY / STARTING / DOWN.

### Step 2: Diagnose DOWN Services

For each DOWN service, investigate in order:

#### 2a. Port Conflict Detection

```bash
lsof -i :PORT
```

If another process occupies the port, report the PID and process name. Suggest:
- Kill the conflicting process: `kill -9 PID`
- Or use an alternative port

#### 2b. Docker Infrastructure Check

For Docker services (postgres, redis, qdrant, minio):

```bash
docker compose ps
docker compose logs --tail=30 SERVICE_NAME
```

Common issues and fixes:
- **Container not running**: `docker compose up -d SERVICE_NAME`
- **Volume corruption**: `docker compose down -v && docker compose up -d`
- **Port already bound**: another Docker stack or local process

#### 2c. Application Service Logs

For Python services, check the terminal or log output for:
- `ModuleNotFoundError` → dependency not installed → `pip install -e services/SERVICE`
- `ConnectionRefusedError` to postgres/redis → infrastructure not running
- `Address already in use` → port conflict (see 2a)
- `JWT_SECRET_KEY` missing → `.env` not sourced → `set -a && . .env && set +a`

For call-manager (Go):
- `cannot find module` → `cd services/call-manager && go mod download`
- Connection errors → check postgres/redis in Docker

#### 2d. Dependency Chain Analysis

Services have startup dependencies:

```
Infrastructure (postgres, redis, qdrant, minio)
  └── Tier 1: pii-redaction, feedback, nlp-state, vad-diarization
  └── Tier 2: rag-engine, knowledge-manager, memory-service, stt-pipeline
  └── Tier 3: llm-inference, summary-crm, orchestration, analytics
  └── Tier 4: call-manager, admin, ingress-telephony, routing-engine
  └── Tier 5: frontend, esl-bridge, channels
```

If a Tier 1 service is down, check infrastructure first.

### Step 3: Auto-Recovery Actions

Apply fixes in order of safety:

1. **Start missing Docker containers**: `docker compose up -d SERVICE`
2. **Restart crashed services**: re-run the uvicorn command
3. **Re-install dependencies**: `pip install -e services/SERVICE` or `npm ci`
4. **Source environment**: `set -a && . .env && set +a`

Never perform destructive actions (dropping databases, removing volumes) without user confirmation.

### Step 4: Verify Recovery

After applying fixes, re-run:

```bash
bash scripts/dev-status.sh
```

Confirm previously DOWN services are now UP/HEALTHY.

## Examples

### Example 1: Service health check
User says: "Check if all services are healthy"
Actions:
1. Run `bash scripts/dev-status.sh`
2. Categorize services as UP/HEALTHY/DOWN
3. For DOWN services, diagnose cause and apply auto-recovery
Result: Service Health Report with recovery actions taken

### Example 2: Specific service failure
User says: "The RAG engine won't start"
Actions:
1. Check port 8013 for conflicts
2. Verify infrastructure dependencies (postgres, redis, qdrant)
3. Check logs for import errors or missing dependencies
Result: Root cause identified with fix applied or manual action recommended

## Troubleshooting

### dev-status.sh script not found
Cause: Running from wrong directory or script missing
Solution: Run from repository root; ensure `scripts/dev-status.sh` exists

### Docker infrastructure not running
Cause: Docker daemon stopped or containers not started
Solution: Run `docker compose up -d` for required infrastructure (postgres, redis, qdrant, minio)

### Port already in use
Cause: Another process or service binding to the same port
Solution: Use `lsof -i :PORT` to find PID, then `kill -9 PID` or change service port

## Output Format

```
Service Health Report
=====================
Date: [YYYY-MM-DD HH:MM]

Status Summary: [N]/[TOTAL] services healthy

Infrastructure:
  PostgreSQL (5433)     ✓ UP
  Redis (6379)          ✓ UP
  Qdrant (6333)         ✗ DOWN → container stopped → fixed: docker compose up -d qdrant
  MinIO (9000)          ✓ UP

Application Services:
  admin (8018)          ✓ HEALTHY
  call-manager (8010)   ✗ DOWN → port conflict (PID 12345 node) → action required
  stt-pipeline (8011)   ✓ HEALTHY
  ...

Actions Taken:
  1. Started qdrant container
  2. Reinstalled services/admin dependencies

Remaining Issues:
  1. call-manager: port 8010 occupied by PID 12345 (node process)
     → Suggest: kill -9 12345 or change CM port

Recovery: [N] fixed, [M] need manual intervention
```

## Known Issues / Common False Alarms

| Symptom | Cause | Action |
|---------|-------|--------|
| OTEL trace export errors (`Failed to export to localhost:4317`) | No OTEL collector running in local dev | Harmless — `dev-start.sh` unsets the endpoint automatically. Ignore these log lines. |
| PII redaction (`:8031`) is DOWN | PII service not started or crashed | **Not a blocker.** RAG engine falls back to unmasked queries when PII is unavailable. |
| RAG engine slow first request (10–30 s) | `sentence-transformers` model loading at startup via `warmup()` | Wait for the first request to complete; subsequent requests are fast. |
| RAG engine hangs on macOS with `Lock blocking` | abseil mutex deadlock with Python 3.12 | Upgrade to Python 3.13+. See `local-dev-runner` Known Issues. |
| Chatbot returns 401 | Missing `INTERNAL_API_KEY` in `.env` | Set `INTERNAL_API_KEY` and restart call-manager. |

## Integration with Other Skills

- **mission-control**: Called during `/incident-response` workflow
- **local-dev-runner**: Complementary — runner starts services, doctor diagnoses failures
- **sre-devops-expert**: Escalate persistent issues for infrastructure review
- **backend-expert**: Escalate application-level errors for code review
