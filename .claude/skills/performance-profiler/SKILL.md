---
name: performance-profiler
description: Measure API latency (p50/p95/p99), Core Web Vitals, PostgreSQL slow queries, and frontend bundle size. Evaluate against SLO targets with regression grading (A-F).
disable-model-invocation: true
---

# Performance Profiler

Full-stack performance measurement and analysis.

## SLO Targets

| Metric | Target | Scope |
|--------|--------|-------|
| API response (general) | p95 < 500ms | all REST endpoints |
| WebSocket connection | < 1s | real-time services |
| Knowledge search | p95 < 2s | RAG endpoints |
| Availability | 99.5% | system-wide |

## Profiling Steps

### 1. API Endpoint Profiling
Measure response times for critical endpoints using `curl -w` or `hey`:
```bash
hey -n 100 -c 10 http://localhost:8080/api/v1/endpoint
```

### 2. Database Query Analysis
```sql
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

### 3. Frontend Bundle Analysis
```bash
cd frontend && pnpm build -- --report
```
Check for: total bundle size, largest chunks, tree-shaking effectiveness.

### 4. Core Web Vitals
Measure TTFB, FCP, LCP, CLS, INP via Lighthouse or browser DevTools.

## Regression Grading

| Grade | Criteria |
|-------|----------|
| A | All metrics within SLO, no regression |
| B | Minor regression (<10%), still within SLO |
| C | Moderate regression (10-25%), approaching SLO limit |
| D | SLO breach on non-critical paths |
| F | SLO breach on critical paths |

## Output Format

1. Executive summary with overall grade
2. Per-metric results vs SLO targets
3. Regression analysis (vs baseline if available)
4. Top bottlenecks ranked by impact
5. Optimization recommendations

Do NOT use for: schema design (use db-expert), code optimization (use backend-expert/frontend-expert).
