# Security Expert — Reference

## OWASP Top 10 for LLM — Detailed Matrix

| ID | Threat | Detection approach | Mitigation |
|----|--------|--------------------|-----------|
| LLM01 | Prompt Injection | Test with adversarial prompts, check for system prompt leakage | Input/output filtering, prompt hardening, context separation |
| LLM02 | Sensitive Info Disclosure | Scan LLM inputs/outputs for PII/secrets patterns | Pre-processing PII scrub, output sanitization, tokenization |
| LLM03 | Training Data Poisoning | N/A for inference-only (applies to fine-tuning) | Validate training data, monitor model drift |
| LLM04 | Model Denial of Service | Load test with large/complex prompts | Token limits, rate limiting, timeout enforcement |
| LLM05 | Improper Output Handling | Inject via LLM output (SQL, XSS, command) | Treat LLM output as untrusted, escape before use |
| LLM06 | Excessive Agency | Review tool/API permissions granted to LLM | Least privilege, approval gates, scope limits |
| LLM07 | System Prompt Leakage | Prompt extraction attacks | Defense-in-depth, avoid secrets in prompts |
| LLM08 | Vector DB Security | Unauthorized access, poisoned embeddings | ACL on collections, embedding validation |
| LLM09 | Misinformation | Hallucination in RAG responses | Retrieval quality checks, confidence scores, citations |
| LLM10 | Unbounded Consumption | Cost explosion from excessive API calls | Budget caps, usage monitoring, circuit breakers |

## FastAPI Security Patterns

### JWT Validation

```python
from jose import jwt, JWTError

async def verify_token(token: str, settings: Settings) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
        if payload.get("exp") < time.time():
            raise HTTPException(401, "Token expired")
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, storage_uri=redis_url)

@app.get("/api/v1/resource")
@limiter.limit("100/minute")
async def get_resource(request: Request):
    ...
```

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # NOT ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Multi-Tenant Security

### Tenant Isolation Checklist

- [ ] Every DB query includes `WHERE tenant_id = :tenant_id`
- [ ] Tenant ID extracted from JWT (not from request body/params)
- [ ] Cross-tenant data access returns 404 (not 403, to prevent enumeration)
- [ ] Qdrant collections scoped per tenant or filtered by tenant metadata
- [ ] Redis keys namespaced with tenant ID
- [ ] File storage (MinIO) buckets or prefixes per tenant

### RBAC Roles

| Role | Permissions |
|------|-----------|
| admin | Full CRUD, user management, system config |
| manager | Read all, write own team resources |
| agent | Read assigned resources, write feedback |
| viewer | Read-only access |

## Dependency Scanning Commands

```bash
# Python
pip audit
safety check --json

# Node (frontend)
cd frontend && npm audit --json

# Go (call-manager)
cd services/call-manager && govulncheck ./...

# Container images
trivy image <image-name>:<tag>
```

## Security Headers (to verify)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
X-XSS-Protection: 0  (rely on CSP instead)
Referrer-Policy: strict-origin-when-cross-origin
```
