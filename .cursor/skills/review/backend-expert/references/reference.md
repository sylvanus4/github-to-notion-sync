# Backend Expert — Reference

## FastAPI Service Template

Standard structure for each Python service:

```
services/<service-name>/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app factory
│   ├── config.py          # Pydantic Settings
│   ├── dependencies.py    # Dependency injection
│   ├── routers/
│   │   └── v1/
│   │       └── <resource>.py
│   ├── models/
│   │   ├── domain.py      # SQLAlchemy models
│   │   └── schemas.py     # Pydantic schemas
│   ├── services/
│   │   └── <resource>_service.py
│   └── exceptions.py      # Domain exceptions
├── tests/
├── Dockerfile
└── pyproject.toml
```

## Shared Library (`agent-assist-common`)

Key modules available from `shared/python/`:

- **`base_settings`** — Pydantic `BaseSettings` subclass with common fields (DB URL, Redis URL, log level)
- **`middleware`** — Request-ID injection, CORS, error handling middleware
- **`auth`** — JWT verification, role-based access decorators
- **`database`** — Async SQLAlchemy engine/session factory, health check query
- **`logging`** — Structlog configuration (JSON formatter, request-id binding)
- **`rate_limit`** — Slowapi limiter with Redis backend

## Error Model Template

```python
from enum import Enum
from pydantic import BaseModel

class ErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    CONFLICT = "CONFLICT"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"

class ErrorDetail(BaseModel):
    field: str | None = None
    message: str

class ErrorResponse(BaseModel):
    code: ErrorCode
    message: str
    details: list[ErrorDetail] = []
    request_id: str | None = None
```

## Inter-Service Communication Pattern

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=0.5, max=5))
async def call_service(client: httpx.AsyncClient, url: str, payload: dict) -> dict:
    response = await client.post(url, json=payload, timeout=10.0)
    response.raise_for_status()
    return response.json()
```

## Health Check Pattern

```python
@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"status": "ready"}
```

## Configuration Pattern

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {"env_prefix": "SVC_"}

    database_url: str
    redis_url: str = "redis://localhost:6379"
    log_level: str = "INFO"
    cors_origins: list[str] = ["*"]
```
