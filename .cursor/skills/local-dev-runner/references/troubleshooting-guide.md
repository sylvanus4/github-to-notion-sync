# Local Dev Runner — Troubleshooting Guide

Detailed solutions for common startup and runtime issues.

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
