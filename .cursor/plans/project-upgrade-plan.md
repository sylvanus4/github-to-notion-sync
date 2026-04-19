# Project Upgrade Plan — AI Model Event Stock Analytics

> **Date**: 2026-03-06
> **Scope**: Full-stack upgrade across 7 domains
> **Skills applied**: backend-expert, frontend-expert, db-expert, security-expert, performance-profiler, qa-test-expert, sre-devops-expert
> **Estimated effort**: ~8-10 weeks (solo developer)

---

## Executive Summary

This plan synthesizes audit findings from 7 engineering skill domains against the current codebase (184 Python files, 193 TS/TSX files, 60+ DB models, 43+ services) and product roadmap (PRD V1.1–V1.3). It addresses **52 improvement items** organized into **7 phases**, prioritized by risk (security/reliability first) and product impact (roadmap alignment second).

### Current State Snapshot

| Dimension | Current | Target |
|-----------|---------|--------|
| Backend test coverage | ~35% | ≥ 70% |
| Frontend test coverage | ~40% lines / 30% branches | ≥ 70% lines / 60% branches |
| E2E test scenarios | 21 specs (not in CI) | 21+ specs running in CI |
| CI pipeline | Lint + test only | Lint → test → coverage → E2E → security scan → build |
| Security posture | Basic auth, no CSRF, in-memory rate limiter | CSRF protection, Redis rate limiter, security headers, secret scanning |
| API client resilience | No timeout, no retry | Timeout + exponential retry + request dedup |
| Monitoring | Console logs only | Sentry + structured logging + SLO dashboards |
| Performance | No profiling, no SLO | SLO targets defined, bundle optimized, query indexed |

---

## Phase 1: Security Hardening (Priority: Critical)

> **Effort**: ~1 week
> **Rationale**: Security gaps are existential risks. Must fix before any feature work.
> **Skills**: security-expert, backend-expert

### 1.1 Redis-Backed Rate Limiter

**Problem**: Current `RateLimitStore` is process-local. Multi-worker deployments share no state, allowing limit bypass.

**Changed files**:
- `backend/app/middleware/rate_limit.py` — Replace in-memory dict with Redis INCR + EXPIRE
- `backend/app/core/cache.py` — Add rate-limit-specific Redis operations
- `backend/tests/test_rate_limit.py` (new) — Unit tests for Redis-backed limiter

**Done criteria**:
- [ ] Rate limiter uses Redis when `REDIS_URL` is configured
- [ ] Falls back to in-memory when Redis is unavailable
- [ ] Tests verify multi-key expiry and sliding window behavior

### 1.2 Security Headers Middleware

**Problem**: No security headers (CSP, X-Frame-Options, HSTS, X-Content-Type-Options).

**Changed files**:
- `backend/app/middleware/security_headers.py` (new) — SecurityHeadersMiddleware
- `backend/app/main.py` — Register middleware
- `backend/tests/test_security_headers.py` (new) — Verify headers on responses

**Done criteria**:
- [ ] All responses include: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`, `Content-Security-Policy`
- [ ] Headers configurable via settings

### 1.3 CSRF Protection

**Problem**: No CSRF protection for state-changing endpoints.

**Changed files**:
- `backend/app/middleware/csrf.py` (new) — Double-submit cookie pattern
- `backend/app/main.py` — Register CSRF middleware
- `frontend/src/lib/api.ts` — Send CSRF token header

**Done criteria**:
- [ ] POST/PUT/DELETE requests require valid CSRF token
- [ ] Token auto-set via cookie and sent as header
- [ ] GET/HEAD/OPTIONS exempt

### 1.4 Secret Scanning in CI

**Problem**: No automated secret detection. `alembic.ini` previously had hardcoded credentials.

**Changed files**:
- `.github/workflows/ci.yml` — Add gitleaks scan step
- `.gitleaksignore` (new) — False positive patterns

**Done criteria**:
- [ ] CI fails if secrets detected in code or git history
- [ ] Known false positives documented in `.gitleaksignore`

### 1.5 Input Sanitization Framework

**Problem**: No centralized input validation beyond Pydantic model checks. XSS vectors possible in event descriptions and report content.

**Changed files**:
- `backend/app/core/sanitizer.py` (new) — HTML sanitization, SQL injection patterns
- `backend/app/schemas/` — Add sanitization validators to text fields in event/report schemas

**Done criteria**:
- [ ] All user-facing text fields sanitized before storage
- [ ] HTML tags stripped except safe subset (bold, italic, links)

### 1.6 JWT Token Rotation & Refresh

**Problem**: JWT refresh token exists but no rotation strategy. Token theft allows indefinite access.

**Changed files**:
- `backend/app/services/auth_service.py` — Implement refresh token rotation (one-time use)
- `backend/app/api/v1/auth.py` — Add `/auth/refresh` endpoint with rotation
- `frontend/src/lib/api.ts` — Add 401 response interceptor with auto-refresh

**Done criteria**:
- [ ] Each refresh token is single-use; old tokens invalidated on rotation
- [ ] Frontend transparently refreshes expired access tokens
- [ ] Refresh token family detection (revoke all on reuse)

---

## Phase 2: Database & Data Integrity (Priority: High)

> **Effort**: ~1 week
> **Rationale**: Data layer weaknesses affect every feature built on top.
> **Skills**: db-expert, backend-expert

### 2.1 Foreign Key Index Audit

**Problem**: PostgreSQL does NOT auto-index FK columns. Missing indexes cause full table scans on JOINs.

**Changed files**:
- `backend/alembic/versions/xxxx_add_fk_indexes.py` (new) — Migration to add indexes on all FK columns
- `docs/adr/003-fk-index-strategy.md` (new) — ADR documenting index decisions

**Done criteria**:
- [ ] All FK columns across 60+ models have corresponding indexes
- [ ] `CREATE INDEX CONCURRENTLY` used for large tables
- [ ] Migration is reversible

### 2.2 Query Performance Baseline

**Problem**: No query performance monitoring. Cannot detect slow queries or regressions.

**Changed files**:
- `backend/app/middleware/slow_query.py` (new) — Log queries exceeding 100ms threshold
- `backend/app/database.py` — Enable `pg_stat_statements` extension
- `backend/app/config.py` — Add `SLOW_QUERY_THRESHOLD_MS` setting (default: 100)

**Done criteria**:
- [ ] Queries exceeding threshold logged with duration, SQL text, and caller context
- [ ] `pg_stat_statements` enabled in development and production PostgreSQL

### 2.3 Alembic Migration Safety Framework

**Problem**: No guardrails against dangerous migration operations (DROP COLUMN on live tables, ADD NOT NULL without DEFAULT).

**Changed files**:
- `backend/alembic/migration_linter.py` (new) — Pre-commit hook that checks migration files for dangerous operations
- `.pre-commit-config.yaml` (update or new) — Register migration linter hook

**Done criteria**:
- [ ] Linter flags: DROP TABLE, DROP COLUMN, ALTER TYPE on enum, ADD NOT NULL without DEFAULT
- [ ] Pre-commit hook runs on `alembic/versions/*.py` changes

### 2.4 Database Connection Health Monitoring

**Problem**: Pool exhaustion is silent. No visibility into connection pool utilization.

**Changed files**:
- `backend/app/core/metrics.py` — Add pool_size, pool_checkedin, pool_checkedout metrics
- `backend/app/api/v1/router.py` or `backend/app/main.py` — Expose pool metrics at `/metrics` endpoint

**Done criteria**:
- [ ] `/metrics` endpoint includes `db_pool_size`, `db_pool_active`, `db_pool_idle`
- [ ] Alert-ready thresholds: warn at 80% pool utilization

### 2.5 Redis Cache Key Standardization

**Problem**: Cache keys are ad-hoc. No naming convention leads to collisions and hard debugging.

**Changed files**:
- `backend/app/core/cache.py` — Enforce key pattern: `app:<domain>:<entity>:<id>` via helper functions
- `backend/app/services/` — Update all cache usages to use standardized key builder

**Done criteria**:
- [ ] All cache keys follow `app:<domain>:<entity>:<id>` pattern
- [ ] Key builder function with type-safe arguments
- [ ] TTL mandatory on all cache writes

---

## Phase 3: CI/CD & DevOps Hardening (Priority: High)

> **Effort**: ~1 week
> **Rationale**: CI gaps mean bugs ship undetected. Deployment has no rollback safety.
> **Skills**: sre-devops-expert, ci-quality-gate

### 3.1 CI Coverage Enforcement

**Problem**: CI runs tests but doesn't enforce coverage thresholds. Coverage can silently regress.

**Changed files**:
- `.github/workflows/ci.yml` — Add `--cov --cov-fail-under=60` to pytest, `--coverage` to Vitest with threshold check

**Done criteria**:
- [ ] Backend CI fails if coverage drops below 60% (progressive target toward 70%)
- [ ] Frontend CI fails if coverage drops below 50% (progressive target toward 70%)

### 3.2 E2E Tests in CI

**Problem**: 21 Playwright specs exist but never run in CI. Regressions in user flows go undetected.

**Changed files**:
- `.github/workflows/ci.yml` — Add E2E job with docker-compose up + Playwright
- `e2e/playwright.config.ts` — Ensure CI-compatible settings (headless, retry 2)

**Done criteria**:
- [ ] E2E tests run on every PR
- [ ] Uses docker-compose to start backend + DB
- [ ] Failure produces trace artifacts for debugging

### 3.3 Docker Image Security

**Problem**: Dockerfiles don't enforce non-root user. No container image scanning.

**Changed files**:
- `Dockerfile` — Add `USER 1000:1000` after install steps
- `backend/Dockerfile` — Add `USER 1000:1000`
- `.github/workflows/ci.yml` — Add Trivy container scan step

**Done criteria**:
- [ ] Production container runs as non-root
- [ ] CI scans Docker image for CVEs (fail on CRITICAL/HIGH)

### 3.4 Docker Resource Limits

**Problem**: No memory/CPU limits in docker-compose. Runaway process can starve host.

**Changed files**:
- `docker-compose.yml` — Add `deploy.resources.limits` for each service

**Done criteria**:
- [ ] Backend: 512MB memory limit, 0.5 CPU
- [ ] PostgreSQL: 1GB memory limit
- [ ] Redis: 256MB memory limit
- [ ] Frontend dev: 512MB memory limit

### 3.5 Git Branch Protection & Merge Checks

**Problem**: No branch protection rules documented or enforced.

**Changed files**:
- `docs/adr/004-branch-protection.md` (new) — ADR for branch protection rules
- `.github/CODEOWNERS` (new) — Define code ownership

**Done criteria**:
- [ ] `main` requires: passing CI, at least 1 review (self-review for solo dev)
- [ ] Direct push to `main` blocked
- [ ] CODEOWNERS for critical paths (security, DB, config)

---

## Phase 4: Frontend Architecture & Performance (Priority: High)

> **Effort**: ~1.5 weeks
> **Rationale**: Frontend is user-facing. Performance and resilience directly impact UX.
> **Skills**: frontend-expert, performance-profiler, ux-expert

### 4.1 API Client Resilience

**Problem**: Axios client has no timeout, no retry, no request deduplication. Flaky network = broken UX.

**Changed files**:
- `frontend/src/lib/api.ts` — Add timeout (30s), exponential retry (3 attempts), request dedup
- `frontend/src/lib/api.test.ts` (new) — Test retry and timeout behavior

**Done criteria**:
- [ ] All API calls timeout after 30s
- [ ] Retryable errors (5xx, network) retried 3 times with exponential backoff
- [ ] Duplicate in-flight requests to same endpoint are deduped

### 4.2 Error Boundary Per Route

**Problem**: Single top-level ErrorBoundary. Error in one page crashes the entire app.

**Changed files**:
- `frontend/src/App.tsx` — Wrap each route-level Suspense with per-route ErrorBoundary
- `frontend/src/components/RouteErrorBoundary.tsx` (new) — Route-specific error display with retry

**Done criteria**:
- [ ] Error in `/turtle` page does not affect `/dashboard`
- [ ] Error boundary shows "retry" button + error details
- [ ] Errors reported to Sentry (when configured)

### 4.3 Loading Skeletons

**Problem**: Pages show blank screen during data loading. Poor perceived performance.

**Changed files**:
- `frontend/src/components/ui/skeleton.tsx` — Skeleton component (if not in shadcn/ui)
- `frontend/src/pages/Dashboard.tsx` — Add skeleton loader
- `frontend/src/pages/Events.tsx` — Add skeleton loader
- Other high-traffic pages — Add skeleton loaders

**Done criteria**:
- [ ] Dashboard, Events, Stocks pages show skeleton during load
- [ ] Skeleton matches layout of loaded content
- [ ] Loading states accessible (aria-busy, screen reader text)

### 4.4 Bundle Size Optimization

**Problem**: No vendor chunk splitting. No compression. Bundle likely exceeds 2MB target.

**Changed files**:
- `frontend/vite.config.ts` — Add `manualChunks` for vendor splitting (react, recharts, lucide)
- `frontend/vite.config.ts` — Add `vite-plugin-compression` for gzip/brotli
- `frontend/package.json` — Add `rollup-plugin-visualizer` for analysis

**Done criteria**:
- [ ] Vendor chunks separated: `react`, `recharts`, `tanstack-query`, `shadcn`
- [ ] Gzipped bundle < 1.5 MB
- [ ] Bundle analysis report generated on build

### 4.5 Frontend SLO Targets

**Problem**: No performance targets defined or measured for frontend.

**Changed files**:
- `frontend/src/lib/web-vitals.ts` (new) — Core Web Vitals reporting
- `frontend/src/main.tsx` — Initialize web-vitals reporting
- `docs/adr/005-frontend-slo.md` (new) — SLO definitions

**Done criteria**:
- [ ] LCP < 2.5s, INP < 200ms, CLS < 0.1 targets defined
- [ ] `web-vitals` library reports to console in dev, to analytics endpoint in production

### 4.6 Accessibility Baseline (WCAG 2.1 AA)

**Problem**: No accessibility audit performed. Unknown compliance level.

**Changed files**:
- `frontend/src/components/ui/` — Fix common a11y issues (missing labels, color contrast)
- `e2e/tests/accessibility.spec.ts` (new) — Automated a11y test with axe-core

**Done criteria**:
- [ ] All form inputs have labels
- [ ] Color contrast ratio >= 4.5:1
- [ ] Keyboard navigation works for all interactive elements
- [ ] axe-core reports zero critical violations

---

## Phase 5: Observability & Monitoring (Priority: High)

> **Effort**: ~1 week
> **Rationale**: Cannot operate what you cannot observe. Monitoring is prerequisite for reliability.
> **Skills**: sre-devops-expert, performance-profiler, backend-expert

### 5.1 Sentry Integration

**Problem**: Errors only in console. No external monitoring. `ErrorBoundary.tsx` has a TODO for this.

**Changed files**:
- `frontend/package.json` — Add `@sentry/react`
- `frontend/src/main.tsx` — Initialize Sentry SDK
- `frontend/src/components/ErrorBoundary.tsx` — Replace TODO with `Sentry.captureException()`
- `backend/requirements.txt` — Add `sentry-sdk[fastapi]`
- `backend/app/main.py` — Initialize Sentry for backend
- `backend/app/config.py` — Add `SENTRY_DSN` setting

**Done criteria**:
- [ ] Frontend and backend errors reported to Sentry
- [ ] Source maps uploaded for readable stack traces
- [ ] Environment and release tagged on events

### 5.2 Structured Logging

**Problem**: Logging uses basic Python logging. No structured format for log aggregation.

**Changed files**:
- `backend/requirements.txt` — Add `structlog`
- `backend/app/core/logging.py` — Replace with structlog configuration (JSON in production, colored in dev)
- `backend/app/middleware/logging.py` — Add `request_id` to all log entries

**Done criteria**:
- [ ] All logs include: `timestamp`, `level`, `request_id`, `service`, `message`
- [ ] JSON format in production, human-readable in development
- [ ] `request_id` header propagated and logged

### 5.3 API SLO Dashboard Data

**Problem**: `/metrics` endpoint exists but provides minimal data. No SLO visibility.

**Changed files**:
- `backend/app/core/metrics.py` — Add histogram-based latency tracking per endpoint
- `backend/app/middleware/logging.py` — Record request duration in metrics

**Done criteria**:
- [ ] `/metrics` exposes per-endpoint: request_count, error_count, latency_p50/p95/p99
- [ ] Prometheus-compatible format

### 5.4 Health Check Enhancement

**Problem**: `/health` checks DB and Redis but doesn't report data source health (Yahoo Finance, Alpha Vantage).

**Changed files**:
- `backend/app/main.py` — Enhance health check to include data source status
- `backend/app/services/data_source_health.py` — Add health probe methods

**Done criteria**:
- [ ] `/health` includes: `db`, `redis`, `yahoo_finance`, `alpha_vantage` status
- [ ] Each component status: `ok`, `degraded`, or `unavailable`
- [ ] Overall status is worst-of-components

---

## Phase 6: Test Coverage & Quality (Priority: Medium-High)

> **Effort**: ~1.5 weeks
> **Rationale**: Current 35% backend / 40% frontend coverage is too low for reliable refactoring.
> **Skills**: qa-test-expert, e2e-testing

### 6.1 Backend Service Test Coverage Push

**Problem**: 35% coverage. Many service modules have zero tests.

**Changed files**:
- `backend/tests/unit/services/` — Add missing service tests (target: 15-20 new test files)

**Priority gaps (uncovered services)**:
1. `analytics_service.py` — Core analysis engine
2. `event_study_service.py` — Event study methodology
3. `report_generation_service.py` — Report creation
4. `impact_score.py` — Impact Score calculation
5. `unified_stock_service.py` — Stock data aggregation
6. `external_stock_api.py` — External API calls (mock Yahoo/Alpha Vantage)
7. `auth_service.py` — Auth edge cases (token expiry, role escalation)

**Done criteria**:
- [ ] Backend coverage >= 60%
- [ ] All public service methods have at least 1 happy path + 1 error path test
- [ ] Edge cases: empty data, null values, boundary conditions

### 6.2 Frontend Component Test Coverage Push

**Problem**: 40% line coverage. Many page components and complex components untested.

**Changed files**:
- `frontend/src/pages/*.test.tsx` — Add page-level render tests (target: 10+ new test files)

**Priority gaps (uncovered pages)**:
1. `Dashboard.tsx` — Main dashboard rendering
2. `Analysis.tsx` / `AnalysisResult.tsx` — Analysis workflow
3. `Patterns.tsx` — Pattern Library
4. `StrategyComparison.tsx` — Strategy comparison
5. `StockPriceDetail.tsx` — Stock detail view
6. `EventDetail.tsx` — Event detail view

**Done criteria**:
- [ ] Frontend coverage >= 60% lines / 50% branches
- [ ] Every page component has at least a smoke render test
- [ ] Loading, error, and empty states tested

### 6.3 Integration Test Suite

**Problem**: No dedicated integration tests verifying cross-service data flow.

**Changed files**:
- `backend/tests/integration/` (new directory)
- `backend/tests/integration/test_analysis_pipeline.py` (new) — Event → Analysis → Report flow
- `backend/tests/integration/test_data_fallback.py` (new) — Yahoo Finance → Alpha Vantage fallback

**Done criteria**:
- [ ] End-to-end analysis pipeline tested (create event → run analysis → verify results)
- [ ] Data source fallback tested (primary failure → secondary succeeds)
- [ ] Tests use testcontainers or docker-compose for DB

### 6.4 Flaky Test Detection

**Problem**: No mechanism to detect or quarantine flaky tests.

**Changed files**:
- `backend/pyproject.toml` — Add `pytest-repeat` for flakiness detection
- `.github/workflows/ci.yml` — Add nightly flaky test detection job (runs tests 5x)

**Done criteria**:
- [ ] Nightly job runs full test suite 5x and reports any inconsistent results
- [ ] Flaky tests documented in `KNOWN_ISSUES.md` until fixed

---

## Phase 7: Product Feature Upgrades (Priority: Medium)

> **Effort**: ~2-3 weeks
> **Rationale**: Aligned with PRD V1.3 and NEXT roadmap items.
> **Skills**: backend-expert, frontend-expert, db-expert

### 7.1 Multi-Factor Event Study Models (PRD FR-4)

**Problem**: Only single-factor (market model) analysis. Academic credibility requires Fama-French and CAPM variants.

**Changed files**:
- `backend/app/services/event_study_service.py` — Add `MarketModel`, `FamaFrench3`, `FamaFrench5` factor options
- `backend/app/schemas/analysis.py` — Add `model_type` enum to analysis request
- `backend/app/models/analysis.py` — Add `model_type` column to `AnalysisRun`
- `frontend/src/pages/Analysis.tsx` — Add model selection dropdown
- `backend/alembic/versions/xxxx_add_model_type.py` (new) — Migration

**Done criteria**:
- [ ] Users can select Market Model, Fama-French 3-Factor, or Fama-French 5-Factor
- [ ] Factor data sourced from Kenneth French data library
- [ ] Results page shows factor loadings alongside CAR

### 7.2 Automated Event Detection (RSS + Keywords)

**Problem**: Events manually cataloged. Catalog becomes stale without automation.

**Changed files**:
- `backend/app/services/event_detection/` (new directory)
  - `rss_fetcher.py` — RSS feed parser for major AI labs
  - `keyword_matcher.py` — Keyword-based relevance scoring
  - `event_creator.py` — Auto-create event records with "pending" status
- `backend/app/tasks/event_detection_task.py` (new) — ARQ task for periodic detection
- `backend/app/config.py` — Add `EVENT_DETECTION_FEEDS`, `EVENT_DETECTION_INTERVAL`

**Done criteria**:
- [ ] RSS feeds from OpenAI, Google DeepMind, Anthropic, Meta AI, NVIDIA parsed
- [ ] Keyword matching with configurable relevance threshold
- [ ] Auto-created events marked "pending_review" for manual approval
- [ ] Runs every 30 minutes via ARQ scheduler

### 7.3 Slippage-Adjusted Backtest Reporting

**Problem**: Backtest results don't account for real trading costs (spread, slippage, commission).

**Changed files**:
- `backend/app/services/turtle/backtest_service.py` — Add slippage/commission parameters
- `backend/app/services/dualma/backtest_service.py` — Add slippage/commission parameters
- `backend/app/schemas/turtle/backtest.py` — Add `slippage_bps`, `commission_bps` fields
- `frontend/src/components/turtle/BacktestForm.tsx` — Add slippage/commission inputs

**Done criteria**:
- [ ] Backtest accepts slippage (basis points) and commission rate
- [ ] P&L adjusted for transaction costs
- [ ] Results show gross vs net returns

### 7.4 Event Catalog Export Enhancement

**Problem**: Basic CSV/JSON export exists but lacks filtering options and metadata.

**Changed files**:
- `backend/app/api/v1/events.py` — Add query params: `date_from`, `date_to`, `org`, `event_type` to export
- `frontend/src/pages/Events.tsx` — Add filter UI before export

**Done criteria**:
- [ ] Export respects active filters
- [ ] CSV includes all event metadata + Impact Score
- [ ] JSON export includes nested analysis results (optional param)

---

## Cross-Cutting Improvements

### API Standardization

| Item | Current | Target |
|------|---------|--------|
| Pagination | Inconsistent (some limit/offset, some none) | Standardized `limit`/`offset` with `meta.total` on all list endpoints |
| Error responses | Mixed formats | Unified `{"error": {"code": "...", "message": "...", "details": [...]}}` |
| Request IDs | Not tracked | UUID per request, returned in `X-Request-ID` header |
| API timeout | No server-side | 60s server-side timeout, 408 on exceed |

### Documentation Debt

| Item | Action |
|------|--------|
| API documentation | Generate OpenAPI spec with detailed examples and error codes |
| Architecture diagram | Create C4 model (Context, Container, Component) |
| Runbook | Create incident response runbook for data pipeline failures |
| ADRs | Document key architecture decisions (auth strategy, data fallback, factor models) |

---

## Phase Dependency Graph

```
Phase 1 (Security) ─────────────────────────────────────────┐
     │                                                       │
Phase 2 (Database) ──────────┐                               │
     │                       │                               │
Phase 3 (CI/CD) ─────────────┤                               │
     │                       │                               │
Phase 5 (Observability) ─────┤  ← All foundation phases      │
                             │    must complete before        │
Phase 4 (Frontend) ──────────┤    product features            │
                             │                               │
Phase 6 (Testing) ───────────┘                               │
                                                             │
Phase 7 (Features) ──────────────────────────────────────────┘
                    ← Depends on all foundation phases
```

**Critical path**: Phase 1 → Phase 3 → Phase 5 → Phase 7

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Redis-backed rate limiter breaks existing behavior | Medium | High | Feature flag, fallback to in-memory |
| FK index migration locks tables | Low | High | `CREATE INDEX CONCURRENTLY`, off-peak deploy |
| Sentry increases latency | Low | Medium | Async transport, sample rate 10% initially |
| Bundle optimization breaks lazy loading | Medium | Medium | Build verification, E2E tests |
| Fama-French data source unavailable | Medium | Medium | Cache factor data locally, retry with backoff |
| Automated event detection generates noise | High | Low | "pending_review" status, configurable threshold |

---

## Rollback Strategy

Each phase produces independent, committable units:
1. **Per-phase commits**: Each sub-task (e.g., 1.1, 1.2) is a separate commit
2. **Feature flags**: Rate limiter, CSRF, event detection behind config toggles
3. **Migration safety**: All Alembic migrations have `downgrade()` implemented
4. **CI as gatekeeper**: No merge without passing CI (after Phase 3 completion)

---

## Verification Commands

```bash
# Backend lint + test
cd backend && ruff check . && ruff format --check . && pytest tests/ -v --cov=app --cov-fail-under=60

# Frontend lint + test
cd frontend && pnpm run lint && tsc --noEmit && pnpm run test:run --coverage

# E2E tests
cd e2e && npx playwright test

# Security scan
gitleaks detect --source . --verbose

# Docker build smoke test
docker build -t stock-analytics:test .

# Bundle analysis
cd frontend && pnpm run build && npx vite-bundle-analyzer
```

---

## Success Metrics (Post-Upgrade)

| Metric | Before | After | Measurement |
|--------|--------|-------|-------------|
| Backend test coverage | ~35% | ≥ 60% | `pytest --cov` |
| Frontend test coverage | ~40% | ≥ 60% | `vitest --coverage` |
| E2E scenarios in CI | 0 | 21+ | CI pipeline |
| Security scan findings | Unknown | 0 critical/high | Trivy + gitleaks |
| API p95 latency | Unknown | < 500ms | Performance profiling |
| Bundle size (gzipped) | Unknown | < 1.5 MB | Build output |
| LCP | Unknown | < 2.5s | web-vitals |
| Error visibility | Console only | Sentry + structured logs | Sentry dashboard |
| Event detection | Manual | Automated (30-min interval) | ARQ task logs |
| Analysis models | 1 (Market Model) | 3 (Market, FF3, FF5) | Feature availability |
