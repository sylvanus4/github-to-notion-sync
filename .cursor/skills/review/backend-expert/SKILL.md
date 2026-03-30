---
name: backend-expert
description: >-
  Design and review FastAPI microservices, Pydantic models, async patterns,
  error handling, and observability. Use when the user asks about backend API
  design, service architecture, error models, or observability setup. Do NOT use
  for database schema design or migration review (use db-expert),
  deployment/infrastructure concerns (use sre-devops-expert), or frontend code
  (use frontend-expert). Korean triggers: "백엔드", "리뷰", "배포", "설계".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# Backend Expert

Specialist for the FastAPI + Python 3.11+ microservices platform. The repo has 19 Python services under `services/` plus 1 Go service (`services/call-manager/`). Shared library at `shared/python/` (`agent-assist-common`).

## Service Inventory

19 Python services + 1 Go service (`call-manager`) under `services/`. For the full service list with ports, see [references/service-inventory.md](references/service-inventory.md).

## API Design Review

### Checklist

- [ ] RESTful resource naming (plural nouns, no verbs in paths)
- [ ] Pydantic v2 models for request/response with `model_config`
- [ ] Proper HTTP status codes (201 for create, 204 for delete, 409 for conflict)
- [ ] Pagination via `limit`/`offset` or cursor-based for large collections
- [ ] API versioning strategy consistent across services
- [ ] Request validation via Pydantic (not manual checks)
- [ ] Response envelope: `{"data": ..., "meta": {...}}` or direct model

### Error Model

Use the shared error model from `agent-assist-common`:

```python
# Standard error response
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "Human-readable description",
        "details": [...]  # optional field-level errors
    }
}
```

- Map domain exceptions to HTTP codes in exception handlers
- Never leak stack traces to clients
- Include `request_id` in error responses for tracing

## Async Patterns

- [ ] All I/O operations use `async`/`await`
- [ ] `httpx.AsyncClient` for inter-service calls (not `requests`)
- [ ] Database queries via `asyncpg` / SQLAlchemy async session
- [ ] Background tasks use FastAPI `BackgroundTasks` or Celery
- [ ] Connection pools sized for expected concurrency
- [ ] Graceful shutdown handles in-flight requests

## Observability

- [ ] Structured logging via `structlog` (JSON in production)
- [ ] `request_id` propagated across service calls
- [ ] Health endpoint at `/health` (liveness) and `/ready` (readiness)
- [ ] Metrics endpoint or push to Prometheus
- [ ] Slow query / slow endpoint logging (> 1s threshold)
- [ ] Rate limiting via `slowapi` on public endpoints

## Examples

### Example 1: API design review
User says: "Review the admin service API design"
Actions:
1. Read `services/admin/app/` route definitions and Pydantic models
2. Apply the API Design Review checklist
3. Check error handling and async patterns
Result: Structured report with compliance score and prioritized fixes

### Example 2: New endpoint review
User says: "Is this endpoint design correct for creating knowledge articles?"
Actions:
1. Review the endpoint against RESTful naming, Pydantic validation, and error model
2. Check async safety and health endpoint impact
Result: Specific findings with code-level fix suggestions

## Troubleshooting

### Shared library import errors
Cause: `agent-assist-common` not installed or outdated
Solution: Run `pip install -e shared/python` to reinstall the shared library

### Service port conflicts
Cause: Another process occupies the expected port
Solution: Check with `lsof -i :PORT` and kill the conflicting process

## Output Format

```
Backend Design Review
=====================
Service: [service name]
Scope: [API / Architecture / Observability]

1. API Design
   Compliance: [XX%]
   Issues:
   - [Endpoint]: [Issue] → [Fix]

2. Error Handling
   Coverage: [Complete / Partial / Missing]
   Gaps:
   - [Scenario]: [Missing handler] → [Recommendation]

3. Async Safety
   Rating: [Safe / Has risks / Blocking calls detected]
   Findings:
   - [File:Line]: [Issue] → [Fix]

4. Observability
   Logging: [Structured / Unstructured / Missing]
   Health checks: [Present / Missing]
   Tracing: [Propagated / Not propagated]

5. Priority Actions
   1. [Action] (Impact: High, Effort: Low)
   2. [Action] (Impact: High, Effort: Medium)
```

## Additional Resources

For FastAPI patterns, shared library conventions, and error model templates, see [references/reference.md](references/reference.md).
