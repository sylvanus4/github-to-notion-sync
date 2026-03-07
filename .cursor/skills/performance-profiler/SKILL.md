---
name: performance-profiler
description: Measure API endpoint latency (p50/p95/p99), analyze PostgreSQL slow queries, profile frontend bundle size, and evaluate against SLO targets. Use when the user asks about performance issues, latency problems, slow queries, bundle optimization, or SLO compliance. Do NOT use for database schema design (use db-expert), code-level optimization (use backend-expert or frontend-expert), or infrastructure scaling review (use sre-devops-expert).
metadata:
  version: "1.0.0"
  category: review
---

# Performance Profiler

Measures and analyzes performance across the full stack — API endpoints, database queries, and frontend assets.

## When to Use

- Investigating latency complaints or slow responses
- Pre-release performance validation against SLO targets
- After schema or query changes to measure impact
- Frontend bundle size monitoring after dependency changes
- As part of the `/incident-response` workflow when the issue is performance-related

## SLO Targets (from docs/08-quality-testing/)

| Metric | Target | Service |
|--------|--------|---------|
| STT latency | p95 < 2s | stt-pipeline (8011) |
| Recommendation latency | p95 < 3s | llm-inference (8014) via orchestration |
| Summary generation | p95 < 10s | summary-crm (8016) |
| API response (general) | p95 < 500ms | all REST endpoints |
| Availability | 99.5% | system-wide |
| WebSocket connection | < 1s | call-manager (8010) |
| Knowledge search | p95 < 2s | rag-engine (8013) |

## Execution Steps

### Step 1: API Endpoint Profiling

Measure response times for critical endpoints. Services must be running locally.

For each endpoint, run N requests and collect timing:

```bash
for i in $(seq 1 20); do
  curl -o /dev/null -s -w "%{time_total}\n" http://localhost:PORT/ENDPOINT
done | sort -n
```

**Critical endpoints to profile:**

| Endpoint | Service | Port | SLO |
|----------|---------|------|-----|
| `GET /health` | all services | various | < 100ms |
| `POST /api/v1/auth/login` | admin | 8018 | < 500ms |
| `GET /api/v1/knowledge/search?q=test` | knowledge-manager | 8015 | < 2s |
| `POST /api/v1/orchestration/process` | orchestration | 8020 | < 3s |
| `GET /api/v1/analytics/dashboard` | analytics | 8022 | < 500ms |
| `GET /api/v1/calls` | call-manager | 8010 | < 500ms |

Calculate p50, p95, p99 from collected data:
- p50: median (50th percentile)
- p95: 95th percentile
- p99: 99th percentile

### Step 2: Database Query Analysis

Connect to the local PostgreSQL and identify slow queries:

```bash
docker compose exec postgres psql -U postgres -d agent_assist -c "
  SELECT query, calls, mean_exec_time, max_exec_time, total_exec_time
  FROM pg_stat_statements
  ORDER BY mean_exec_time DESC
  LIMIT 20;
"
```

If `pg_stat_statements` is not enabled, analyze key queries manually:

```bash
docker compose exec postgres psql -U postgres -d agent_assist -c "
  EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
  SELECT * FROM calls WHERE tenant_id = 'test' ORDER BY created_at DESC LIMIT 10;
"
```

Look for:
- Sequential scans on large tables (missing index)
- Nested loops with high row counts
- Sort operations without index support
- Excessive buffer reads

### Step 3: Frontend Bundle Analysis

```bash
cd frontend && npm run build 2>&1
```

Analyze the output for:
- Total bundle size (target: < 2 MB gzipped)
- Largest chunks and their contents
- Tree-shaking effectiveness
- Lazy-loaded vs eager-loaded routes

If `rollup-plugin-visualizer` or similar is configured:
```bash
cd frontend && npx vite-bundle-analyzer
```

### Step 4: Memory and Connection Analysis

Check for resource leaks:

```bash
# PostgreSQL connection count
docker compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# PgBouncer stats
docker compose exec pgbouncer psql -p 5434 -U postgres -c "SHOW POOLS;"

# Redis memory
docker compose exec redis redis-cli -p 6379 INFO memory | head -10

# Redis connection count
docker compose exec redis redis-cli -p 6379 CLIENT LIST | wc -l
```

### Step 5: Compare Against SLO

For each measured metric, compare against the SLO target and flag violations.

## Examples

### Example 1: API latency investigation
User says: "The knowledge search is slow"
Actions:
1. Profile `GET /api/v1/knowledge/search` endpoint with 20 requests
2. Calculate p50/p95/p99 and compare against SLO (<2s)
3. If SLO violated, analyze database queries for missing indexes
Result: Performance Profile Report with latency breakdown and optimization suggestions

### Example 2: Pre-release performance validation
User says: "Check performance before release"
Actions:
1. Profile all critical endpoints against SLO targets
2. Run database query analysis for slow queries
3. Check frontend bundle size against 2MB target
Result: Full-stack performance report with SLO compliance status

## Troubleshooting

### Services not running for profiling
Cause: Local dev stack not started
Solution: Use local-dev-runner to start all services first

### pg_stat_statements not available
Cause: Extension not enabled in local PostgreSQL
Solution: Run `CREATE EXTENSION IF NOT EXISTS pg_stat_statements;`

## Output Format

```
Performance Profile Report
==========================
Date: [YYYY-MM-DD HH:MM]
Environment: local development

API Latency (20 requests each):
  Endpoint                          p50      p95      p99      SLO      Status
  ──────────────────────────────── ──────── ──────── ──────── ──────── ──────
  GET  /health (admin)              12ms     18ms     25ms    <100ms   ✓ PASS
  POST /api/v1/auth/login           89ms     145ms    210ms   <500ms   ✓ PASS
  GET  /api/v1/knowledge/search     850ms    1.8s     2.4s    <2s      ⚠ WARN
  POST /api/v1/orchestration        1.2s     2.8s     3.5s    <3s      ✓ PASS

Database:
  Slow queries (mean > 100ms):
    1. [query excerpt] — mean: 250ms, calls: 1,200
       → Suggestion: Add index on (tenant_id, created_at)
    2. [query excerpt] — mean: 180ms, calls: 500
       → Suggestion: Rewrite as CTE

  Connections: [N] active / [M] idle / [K] pool max

Frontend Bundle:
  Total: [X] MB (gzipped: [Y] MB)
  Largest chunks:
    1. vendor.js — [X] KB
    2. index.js — [X] KB
  Status: ✓ Under 2 MB target

Resource Usage:
  PostgreSQL connections: [N] / [MAX]
  Redis memory: [X] MB / [MAX] MB
  Redis clients: [N]

SLO Compliance: [N]/[M] targets met
Violations: [list]

Optimization Recommendations:
  1. [Priority] [Recommendation]
  2. [Priority] [Recommendation]
```

## Integration with Other Skills

- **mission-control**: Called for performance-related goals
- **db-expert**: Escalate slow queries for schema/index optimization
- **backend-expert**: Escalate API latency issues for code-level optimization
- **frontend-expert**: Escalate bundle size issues for splitting/lazy-loading
- **sre-devops-expert**: Feed SLO compliance data into operational reviews
