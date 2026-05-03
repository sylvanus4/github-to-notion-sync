---
name: local-dev-setup
description: Go backend local development environment setup — Docker DB/NATS, migrations, seed data, RSA keys, port-forwarding, .env, and Caddy HTTPS.
disable-model-invocation: true
---

Set up the complete Go backend local development environment.

## Setup Pipeline (Sequential)

1. **Docker Services**: Start PostgreSQL, NATS, Redis via Docker Compose
2. **Database Migration**: Run Alembic/goose migrations
3. **Seed Data**: Insert initial data (admin user, default tenants, roles)
4. **RSA Key Generation**: Generate JWT signing keys if not present
5. **Infrastructure Port-Forward**: Set up kubectl port-forward for remote services
6. **Environment Config**: Update .env with local service URLs
7. **Caddy HTTPS**: Configure Caddy reverse proxy for local HTTPS

## Prerequisites

- Docker Desktop running
- Go 1.22+ installed
- kubectl configured with cluster access
- Caddy installed (`brew install caddy`)

## Verification

After setup, verify:
```bash
curl -k https://localhost:8443/health
docker ps  # All containers running
psql -h localhost -U postgres -d ai_platform_db -c "SELECT 1"
```

## Rules

- Never overwrite existing .env without backup
- Generate new RSA keys only if missing
- Report each step's success/failure
