# Environment Variables & Manual Startup Guide

## Environment Variables

`.env.example`에서 `.env`로 복사 후 필수 값 설정:

| Variable | Required | Notes |
|----------|----------|-------|
| `POSTGRES_PASSWORD` | Yes | Database password |
| `REDIS_PASSWORD` | Yes | Redis password |
| `JWT_SECRET_KEY` | Yes | JWT signing key |
| `INTERNAL_API_KEY` | Yes | Used by call-manager for RAG/memory inter-service calls. Without this, the chatbot fails with 401. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | No | Commented out by default. Only needed when running an OTEL collector (e.g. Jaeger). |

## Step-by-Step Manual Startup

### 1. Environment Setup

```bash
# .env 파일이 없으면 생성
cp .env.example .env
# 필수 값 설정: POSTGRES_PASSWORD, REDIS_PASSWORD, JWT_SECRET_KEY, INTERNAL_API_KEY 등
```

### 2. Infrastructure (Docker)

```bash
# 포트 충돌 확인 후 인프라 시작
make dev-infra
# PostgreSQL(5433), PgBouncer(5434), Redis(6379), Qdrant(6333), MinIO(9000)
```

### 3. Database Migration

```bash
make db-migrate
```

### 4. Python Dependencies

```bash
# uv를 사용한 공유 라이브러리 + 서비스 설치
pip install -e shared/python
for svc in services/*/; do pip install -e "$svc" 2>/dev/null; done
```

### 5. Backend Services

각 Python 서비스는 동일한 패턴으로 실행:

```bash
cd services/<service-name> && uvicorn app.main:app --host 0.0.0.0 --port <PORT> &
```

서비스별 포트는 `.env.example` 참조.

### 6. Call Manager (Go)

```bash
cd services/call-manager && go run ./cmd/server &
```

### 7. Frontend

```bash
cd frontend && npm run dev
```
