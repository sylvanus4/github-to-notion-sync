---
name: sre-devops-expert
description: >-
  Design and review CI/CD pipelines, Helm charts, Kubernetes manifests, Docker
  Compose configs, runbooks, SLO definitions, and rollback procedures. Use when
  the user asks about deployment, infrastructure, runbooks, alerting, or
  operational readiness. Do NOT use for running CI locally (use
  ci-quality-gate), managing the local dev stack (use local-dev-runner), or
  backend API code review (use backend-expert). Korean triggers: "리뷰", "배포",
  "설계", "파이프라인".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# SRE / DevOps Expert

Specialist for the infrastructure at `infra/` (Helm/K8s), `docker-compose.yml` (local infra), `docker-compose.services.yml` (app services), `.github/workflows/` (CI/CD), and `Makefile`.

## Infrastructure Inventory

| Component | Location | Technology |
|-----------|----------|-----------|
| Local infra | `docker-compose.yml` | PostgreSQL 16, PgBouncer, Redis 7, Qdrant, MinIO |
| App services | `docker-compose.services.yml` | 14 Python + 1 Go + 1 React containers |
| Helm charts | `infra/helm/` | Kubernetes deployment (primary) |
| K8s manifests | `infra/k8s/` | Supplementary raw manifests |
| Observability | `infra/observability/` | Prometheus, Grafana, Loki, OTel, Alertmanager |
| CI/CD | `.github/workflows/` | GitHub Actions |
| Scripts | `scripts/` | Build, deploy, utility scripts |

## CI/CD Pipeline Review

### Checklist

- [ ] Lint → Test → Build → Push → Deploy stages in order
- [ ] Tests run in parallel where independent
- [ ] Docker images tagged with git SHA (not just `latest`)
- [ ] Multi-stage Dockerfiles (builder + runtime for small images)
- [ ] Secret management via GitHub Secrets or external vault (not hardcoded)
- [ ] Branch protection: main requires passing CI + review
- [ ] Caching: pip/npm/go module caches in CI
- [ ] Security scan: container image scanning (Trivy, Snyk)

## Docker / Compose Review

### Checklist

- [ ] Base images pinned to specific versions (not `latest`)
- [ ] Non-root user in Dockerfiles (`USER 1000`)
- [ ] Health checks defined in compose and Dockerfiles
- [ ] Resource limits set (`mem_limit`, `cpus`)
- [ ] `.dockerignore` excludes dev files, tests, docs
- [ ] Environment variables via `.env` file (not hardcoded in compose)
- [ ] Volume mounts for persistent data (PostgreSQL, MinIO, Qdrant)

## Kubernetes / Helm Review

### Checklist

- [ ] Resource requests and limits on all containers
- [ ] Liveness and readiness probes configured
- [ ] Pod disruption budgets for critical services
- [ ] Horizontal Pod Autoscaler based on CPU/memory or custom metrics
- [ ] Network policies restrict inter-service traffic
- [ ] Secrets managed via Sealed Secrets, External Secrets, or Vault
- [ ] Ingress with TLS termination
- [ ] Rolling update strategy with `maxSurge` / `maxUnavailable`

## SLO / Alerting Design

### Template

| Service | SLI | SLO Target | Alert threshold |
|---------|-----|-----------|----------------|
| call-manager | Request success rate | 99.9% | < 99.5% for 5m |
| stt-pipeline | p99 latency | < 500ms | > 1s for 5m |
| rag-engine | Query success rate | 99.5% | < 99% for 5m |
| frontend | LCP | < 2.5s | > 4s for 5m |

### Alerting Rules

- **Critical**: Page on-call (PagerDuty/Slack) — SLO burn rate > 10x
- **Warning**: Slack notification — SLO burn rate > 2x
- **Info**: Dashboard only — approaching budget

## Rollback Procedure

1. Identify the failing deployment (service name, version)
2. Check if database migration was applied
3. If no migration: `kubectl rollout undo deployment/<service>`
4. If migration applied: assess backward compatibility
5. If migration is backward-compatible: rollback app, keep schema
6. If migration is NOT backward-compatible: run Alembic downgrade, then rollback app
7. Verify health endpoints return 200
8. Notify team in Slack

## Examples

### Example 1: Deployment readiness review
User says: "Is our Kubernetes setup production-ready?"
Actions:
1. Review Helm charts for resource limits, probes, and HPA
2. Check CI/CD pipeline for security scanning and image tagging
3. Verify rollback procedures and SLO definitions
Result: Operations Review Report with readiness checklist and gaps

### Example 2: Docker Compose review
User says: "Review our Docker Compose configuration"
Actions:
1. Check base image pinning, health checks, and resource limits
2. Verify non-root users and .dockerignore
3. Review volume mounts and environment variable management
Result: Container configuration review with specific improvement items

## Troubleshooting

### Helm chart rendering errors
Cause: Template syntax errors or missing values
Solution: Run `helm template . --debug` to identify the specific template error

### Docker build fails
Cause: Base image not available or multi-stage build issue
Solution: Check image availability, verify `FROM` tags, and test each build stage

## Output Format

```
Operations Review Report
========================
Scope: [CI/CD / Docker / K8s / Runbook / Full]

1. CI/CD Pipeline
   Status: [Healthy / Needs improvement]
   Issues:
   - [Stage]: [Issue] → [Fix]

2. Container Configuration
   Images: [N reviewed]
   Issues:
   - [Service]: [Issue] → [Fix]

3. Kubernetes Readiness
   Probes: [Configured / Missing for N services]
   Resource limits: [Set / Missing]
   HPA: [Configured / Not configured]

4. SLO Coverage
   Services with SLOs: [N / total]
   Alerting: [Configured / Partial / None]

5. Runbook Status
   Documented procedures: [N]
   Missing:
   - [Scenario]: needs runbook

6. Priority Actions
   1. [Action] — [Impact: High, Effort: Low]
   2. [Action] — [Impact: High, Effort: Medium]
```

## Templates

For a ready-to-use runbook template, see [templates/runbook-template.md](templates/runbook-template.md).
