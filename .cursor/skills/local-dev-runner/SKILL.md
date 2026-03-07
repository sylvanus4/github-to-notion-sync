---
name: local-dev-runner
description: Start, stop, and manage the full local development environment on macOS. Use when the user asks to run the project locally, start/stop services, or set up the development stack from scratch. Do NOT use for diagnosing specific service failures after startup (use service-health-doctor) or reviewing infrastructure configuration (use sre-devops-expert).
metadata:
  version: "1.0.0"
  category: execution
---

# Local Development Runner

로컬 macOS 환경에서 프로젝트 전체 스택을 실행하고 관리하는 스킬.

## Prerequisites

| Tool    | Minimum Version | Check Command          |
|---------|----------------|------------------------|
| Docker  | 20+            | `docker --version`     |
| Node.js | 18+            | `node --version`       |
| npm     | 9+             | `npm --version`        |
| Python  | 3.13+          | `python3 --version`    |
| Go      | 1.22+          | `go version`           |
| uv      | 0.4+           | `uv --version`         |

## Architecture Overview

```
┌─────────────────── Docker (Infrastructure) ───────────────────┐
│  PostgreSQL:5433  PgBouncer:5434  Redis:6379                  │
│  Qdrant:6333,6334  MinIO:9000,9001                            │
└───────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌────── Tier 1 (Stateless) ──┐  ┌── Tier 2 (Data) ────────────┐
│ pii-redaction    :8031     │  │ rag-engine           :8013   │
│ nlp-state        :8012     │  │ knowledge-manager    :8015   │
│ analytics        :8022     │  │ memory-service       :8019   │
│ feedback         :8017     │  │ summary-crm          :8016   │
│ routing-engine   :8028     │  └──────────────────────────────┘
└────────────────────────────┘
         ↓                    ↓
┌────── Tier 3 (AI/ML) ─────┐  ┌── Tier 4 (Business) ────────┐
│ llm-inference    :8014     │  │ orchestration        :8020   │
│ stt-pipeline     :8011     │  │ admin                :8018   │
│ vad-diarization  :8024     │  │ ingress-telephony    :8023   │
│ tts-service      :(none)   │  │ chat/email/sms-channel       │
└────────────────────────────┘  │   :8025/:8026/:8027          │
                                └──────────────────────────────┘
         ↓
┌────── Tier 5 (Gateway + Frontend) ───────────────────────────┐
│ call-manager (Go)  :8010                                      │
│ frontend (Vite)    :5173                                      │
└───────────────────────────────────────────────────────────────┘
```

## Startup Script

전체 스택 시작은 `scripts/dev-start.sh` 스크립트를 사용:

```bash
# 전체 스택 시작
bash scripts/dev-start.sh

# 중지
bash scripts/dev-stop.sh

# 상태 확인
bash scripts/dev-status.sh
```

## Environment Variables

Required: `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, `JWT_SECRET_KEY`, `INTERNAL_API_KEY`. Copy from `.env.example` to `.env`. For the full variable list, see [references/startup-guide.md](references/startup-guide.md).

## Step-by-Step Manual Startup

7 sequential steps: Environment Setup, Infrastructure (Docker), DB Migration, Python Dependencies, Backend Services, Call Manager (Go), Frontend. For detailed commands, see [references/startup-guide.md](references/startup-guide.md).

## Health Check

모든 Python 서비스는 `/health` 엔드포인트를 제공:

```bash
# 개별 서비스 확인
curl -sf http://localhost:<PORT>/health

# 전체 서비스 상태 확인
bash scripts/dev-status.sh
```

## Cleanup Before Start

중복 프로세스를 방지하기 위해 시작 전 항상 정리:

```bash
# 1. 해당 포트를 점유한 프로세스 확인
lsof -i :<PORT> | grep LISTEN

# 2. 다른 프로젝트의 Docker 컨테이너가 포트를 점유하면 중지
docker stop <container-name>

# 3. 기존 uvicorn 프로세스 종료
pkill -f "uvicorn.*<service-port>"
```

## Known Issues

### 1. abseil mutex deadlock (macOS, Python 3.12)

`grpcio` + `onnxruntime` (via `sentence-transformers`) deadlock on macOS with Python 3.12. The RAG engine hangs with `[mutex.cc : 452] RAW: Lock blocking` on startup. **Fix**: Use Python 3.13+. The `dev-start.sh` script additionally unsets `OTEL_EXPORTER_OTLP_ENDPOINT` to avoid gRPC initialization.

### 2. OTEL trace export noise

When `OTEL_EXPORTER_OTLP_ENDPOINT` is set but no collector is running, all services log repeated retry errors to `localhost:4317`. This is harmless but noisy. `dev-start.sh` unsets this variable automatically.

### 3. PII service down ≠ RAG failure

The PII redaction service (`:8031`) is optional. When it is unavailable, the RAG engine logs a warning and proceeds with the unmasked query — it no longer returns a 500 error.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | `lsof -i :<port>` 로 확인 후 `kill <pid>` |
| Docker compose fails | `docker compose down` 후 재시작 |
| Python import error | `pip install -e shared/python` 재실행 |
| DB connection error | PostgreSQL, PgBouncer 컨테이너 상태 확인 |
| Redis connection refused | Redis 컨테이너 상태 및 비밀번호 확인 |
| Frontend build error | `cd frontend && rm -rf node_modules && npm install` |
| RAG engine hangs on macOS | Python 3.12 abseil deadlock — upgrade to Python 3.13+ |
| OTEL retry noise in logs | Unset `OTEL_EXPORTER_OTLP_ENDPOINT` or use `dev-start.sh` (handled automatically) |
| Chatbot returns 401 | Ensure `INTERNAL_API_KEY` is set in `.env` |
| RAG 500 from PII service | PII fallback is enabled; check RAG logs for warnings |

## Related Scripts

- `scripts/dev-start.sh` - 전체 스택 시작 (정리 → 인프라 → 서비스 → 프론트엔드)
- `scripts/dev-stop.sh` - 전체 스택 중지
- `scripts/dev-status.sh` - 모든 서비스 헬스체크
