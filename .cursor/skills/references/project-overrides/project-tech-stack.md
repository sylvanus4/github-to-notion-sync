# Project Tech Stack — AI Stock Analytics

> Override for cloud-platform tech stack references.
> Source: `docs/policies/01-product-identity.md` (POL-001), `frontend/package.json`

## Frontend

| Library | Version | Purpose |
|---------|---------|---------|
| React | 19 | UI framework |
| TypeScript | 5.x | Type safety |
| Vite | 7 | Build tool |
| Tailwind CSS | 4 | Styling |
| Radix UI | latest | Headless components |
| TanStack Query | 5 | Server state |
| Zustand | 5 | Client state |
| i18next | 25 | Internationalization |
| lucide-react | latest | Icons (only allowed icon lib) |
| Recharts | 2 | Charts |
| Zod | 3 | Schema validation |
| react-hook-form | 7 | Form management |

## Backend

| Library | Version | Purpose |
|---------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | latest | Web framework |
| SQLAlchemy | 2.x | ORM |
| Alembic | latest | Migrations |
| PostgreSQL | 16 | Database |
| Redis | 7 | Caching |
| Pydantic | 2.x | Data validation |
| yfinance | latest | Stock data |
| OpenAI SDK | latest | LLM analysis |

## E2E Testing

| Library | Version | Purpose |
|---------|---------|---------|
| Playwright | latest | Browser automation |
| Vitest | latest | Unit tests |

## NOT Used

- Go (Fiber) backend
- NATS JetStream / Valkey
- Keycloak
- ArgoCD / Kueue / GPU Operator / Traefik
- VictoriaMetrics / VictoriaLogs
- k0s / Slinky (Slurm-on-K8s)
- Docker Compose for dev (direct local)
