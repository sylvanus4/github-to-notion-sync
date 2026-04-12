---
name: canary-monitor
description: >-
  Post-deploy production monitoring loop that periodically captures screenshots,
  console errors, network failures, and performance metrics, comparing against
  a baseline. Uses 2-consecutive-confirmation before alerting to prevent false
  alarms. Use when the user asks for "canary monitor", "post-deploy check",
  "canary-monitor", "deploy monitoring", "배포 후 모니터링", "카나리 모니터",
  "배포 확인", or wants post-deploy verification. Do NOT use for pre-merge
  validation (use release-commander), IaC review (use iac-review-agent), or
  infrastructure drift detection (use infra-drift-detector).
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Canary Monitor — Post-Deploy Verification Loop

Automated monitoring loop that runs after deployment to catch regressions before users do.

## Usage

```
/canary-monitor http://localhost:3000              # monitor with default settings
/canary-monitor https://staging.example.com        # monitor staging
/canary-monitor --baseline                         # capture fresh baseline
/canary-monitor --duration 10m                     # monitor for 10 minutes (default: 5m)
/canary-monitor --interval 30s                     # check every 30 seconds (default: 60s)
/canary-monitor --pages /,/dashboard,/settings     # specific pages to monitor
/canary-monitor --manifest canary-manifest.yaml    # use a multi-page manifest
/canary-monitor --budget strict                    # enforce performance budgets
/canary-monitor --logs                             # capture browser + server logs
/canary-monitor --alert slack                      # send structured alerts to Slack
```

## Concepts

### Baseline Manifest

A saved snapshot of the "known good" state:
- Screenshot of each monitored page
- Console error count (expected: 0)
- Network failure count (expected: 0)
- Core Web Vitals: TTFB, FCP, LCP
- HTTP status codes for key endpoints

Baselines are stored in `output/canary-baselines/` as JSON + screenshots.

### 2-Consecutive-Confirmation

To prevent false alarms from transient issues (network hiccup, cold start):

1. First detection: mark as "suspicious", do NOT alert
2. Wait one interval, re-check
3. Second consecutive detection of the same issue: confirm as regression, alert
4. If second check passes: clear the suspicious flag, continue monitoring

## Workflow

### Step 1: Establish or Load Baseline

If `--baseline` flag is set OR no baseline exists:
1. Navigate to each monitored page via browser MCP
2. Capture: screenshot, console errors, network requests, performance metrics
3. Save baseline manifest to `output/canary-baselines/{domain}-baseline.json`

If baseline exists:
1. Load from `output/canary-baselines/{domain}-baseline.json`

### Step 2: Start Monitoring Loop

```
Canary Monitor Started
======================
Target: [URL]
Pages: [list]
Duration: [Xm] | Interval: [Xs]
Baseline: [loaded from file / freshly captured]
```

### Step 3: Per-Interval Check

For each monitored page:

1. **Navigate** to the page via browser MCP
2. **Capture screenshot** for visual comparison
3. **Check console** for new errors (errors not in baseline)
4. **Check network** for failed requests (4xx/5xx not in baseline)
5. **Measure CWV**: TTFB, FCP, LCP
6. **Compare against baseline**:
   - New console errors: flag
   - New network failures: flag
   - LCP regression > 20%: flag
   - TTFB regression > 50%: flag
   - Visual difference: flag (if screenshot differs significantly)

### Step 4: Apply 2-Consecutive-Confirmation

For each flagged item:
- If first occurrence: mark as "suspicious"
- If same item flagged on consecutive check: CONFIRM as regression
- If cleared on follow-up: remove suspicious flag

### Step 5: Alert on Confirmed Regressions

When a regression is confirmed (2 consecutive detections):

```
⚠️ CANARY ALERT
===============
Page: [URL]
Issue: [description]
First detected: [timestamp]
Confirmed: [timestamp]

Details:
  Console errors: [new error messages]
  Network failures: [failed URLs with status codes]
  CWV regression: LCP [baseline] → [current] (+[X]%)

Recommendation: [investigate / rollback / ignore]
```

### Step 6: Monitoring Complete Report

After the monitoring duration expires:

```
Canary Monitor Report
=====================
Target: [URL]
Duration: [Xm] | Checks: [N]
Pages monitored: [list]

Results:
  Page             Status    Console  Network  LCP      Notes
  ────────────     ──────    ───────  ───────  ───────  ─────
  /                ✓ PASS    0 new    0 new    1.2s     Stable
  /dashboard       ⚠ WARN   2 new    0 new    2.8s     LCP +15%
  /settings        ✗ FAIL   0 new    1 new    1.5s     API 500

Confirmed Regressions: [N]
Suspicious (unconfirmed): [N]
Clean Pages: [N]

Baseline Refresh: [recommended if all clean for 5+ checks]
```

### Step 7: Baseline Refresh

If all pages pass clean for the entire monitoring duration:
- Offer to refresh the baseline with current state
- Previous baseline archived with timestamp

## Configuration Defaults

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--duration` | 5m | Total monitoring time |
| `--interval` | 60s | Time between checks |
| `--pages` | `/` | Pages to monitor (comma-separated) |
| `--manifest` | none | Path to YAML manifest file |
| `--budget` | standard | Budget enforcement level: relaxed, standard, strict |
| `--alert` | none | Alert channel: slack, log-only |
| `--logs` | false | Enable browser + server log capture |
| LCP regression threshold | 20% | Flag if LCP increases by this % |
| TTFB regression threshold | 50% | Flag if TTFB increases by this % |
| Console error tolerance | 0 | New errors above baseline |

## Multi-Page Manifest

Instead of passing `--pages` as a comma list, define a YAML manifest for repeatable, version-controlled canary runs.

### Manifest Format

Save as `canary-manifest.yaml` in the project root or `output/canary-baselines/`:

```yaml
target: https://staging.example.com
duration: 10m
interval: 30s
budget: strict

pages:
  - path: /
    label: Landing Page
    budget:
      lcp: 2500
      fcp: 1800
      ttfb: 800
    critical: true
    auth: false

  - path: /dashboard
    label: Dashboard
    budget:
      lcp: 3000
      fcp: 2000
      ttfb: 1000
    critical: true
    auth: true
    auth_cookie: session_token

  - path: /api/health
    label: Health Endpoint
    type: api
    expected_status: 200
    expected_body_contains: '"status":"ok"'
    critical: true

  - path: /settings
    label: Settings Page
    budget:
      lcp: 3500
    critical: false
    auth: true

  - path: /docs
    label: Documentation
    critical: false
```

### Manifest Fields

| Field | Type | Description |
|---|---|---|
| `path` | string | URL path to monitor |
| `label` | string | Human-readable name for reports |
| `budget` | object | Per-page performance budgets (overrides global) |
| `critical` | boolean | If true, failure triggers immediate alert; if false, warning only |
| `auth` | boolean | Whether page requires authentication |
| `auth_cookie` | string | Cookie name to inject for authenticated pages |
| `type` | string | `page` (default) or `api` for JSON endpoint checks |
| `expected_status` | number | Expected HTTP status for API-type pages |
| `expected_body_contains` | string | Substring that must appear in API response body |

### Usage

```
/canary-monitor --manifest canary-manifest.yaml
```

When a manifest is used, `--pages`, `--duration`, and `--interval` flags are ignored (manifest values take precedence).

## Performance Budgets

Define per-metric thresholds that trigger alerts when exceeded, independent of baseline comparison.

### Budget Levels

| Level | Enforcement | Use Case |
|---|---|---|
| `relaxed` | Warn only, never fail | Early development, internal tools |
| `standard` | Warn on first breach, fail on 2-consecutive | Staging, pre-production |
| `strict` | Fail immediately on any budget breach | Production, SLA-bound pages |

### Default Budgets (when no manifest overrides)

| Metric | Relaxed | Standard | Strict | Unit |
|---|---|---|---|---|
| LCP | 4000 | 2500 | 1800 | ms |
| FCP | 3000 | 1800 | 1200 | ms |
| TTFB | 1500 | 800 | 400 | ms |
| Console errors (new) | 5 | 2 | 0 | count |
| Network failures (new) | 3 | 1 | 0 | count |
| JS bundle size | — | 500 | 350 | KB |
| Total transfer size | — | 3000 | 2000 | KB |

### Budget Report Section

Added to the final monitoring report:

```
Performance Budget Report
=========================
Budget level: strict

Page             LCP     Budget  Status   FCP     Budget  Status   TTFB    Budget  Status
────────────     ─────   ──────  ──────   ─────   ──────  ──────   ─────   ──────  ──────
/                1.2s    1.8s    ✓ PASS   0.9s    1.2s    ✓ PASS   0.3s    0.4s    ✓ PASS
/dashboard       2.1s    1.8s    ✗ OVER   1.5s    1.2s    ✗ OVER   0.6s    0.4s    ✗ OVER
/settings        1.4s    3.5s    ✓ PASS   1.0s    1.2s    ✓ PASS   0.4s    0.4s    ✓ PASS

Budget violations: 3 (2 critical pages)
```

## Structured Alerts

Replace plain-text alerts with structured, machine-readable alerts that integrate with Slack and incident management.

### Alert Format

```json
{
  "alert_id": "canary-2026-04-10-001",
  "severity": "critical",
  "target": "https://staging.example.com",
  "page": "/dashboard",
  "page_label": "Dashboard",
  "critical_page": true,
  "timestamp": "2026-04-10T14:05:00Z",
  "confirmed_at": "2026-04-10T14:06:00Z",
  "issues": [
    {
      "type": "performance_budget",
      "metric": "LCP",
      "baseline": 1800,
      "current": 3200,
      "budget": 1800,
      "delta_pct": 77.8
    },
    {
      "type": "console_error",
      "message": "TypeError: Cannot read properties of undefined",
      "source": "dashboard.js:142",
      "count": 3
    }
  ],
  "recommendation": "investigate",
  "rollback_suggested": false
}
```

### Severity Classification

| Severity | Condition |
|---|---|
| `critical` | Critical page has confirmed regression OR budget breach in strict mode |
| `warning` | Non-critical page regression OR budget breach in standard mode |
| `info` | Suspicious (unconfirmed) OR minor metric degradation |

### Slack Alert Integration

When `--alert slack` is used, post structured alerts to the configured Slack channel:

```
🚨 Canary Alert — critical

Target: https://staging.example.com
Page: /dashboard (Dashboard)

Issues:
  • LCP budget exceeded: 3.2s (budget: 1.8s, +78%)
  • 3 new console errors: TypeError at dashboard.js:142

Confirmed at: 14:06 UTC (first seen 14:05 UTC)
Recommendation: Investigate — possible regression in latest deploy

Alert ID: canary-2026-04-10-001
```

Alert channel routing:
- `critical` severity → #hotfix-alert
- `warning` severity → #release-control
- `info` severity → logged only, no Slack post

### Alert History

All alerts are appended to `outputs/canary-alerts/{domain}-alerts.jsonl` for trend analysis.

## Log Capture

When `--logs` is enabled, capture browser and server logs during each check interval for post-incident analysis.

### Captured Log Types

| Source | Method | Storage |
|---|---|---|
| Browser console | `browser_console_messages` via browser MCP | Per-check snapshot |
| Browser network | `browser_network_requests` via browser MCP | Failed requests only |
| Server logs (if accessible) | `kubectl logs` or `docker logs` for the deployed service | Tail last 50 lines per check |
| Application errors | Parse structured error responses from API endpoints | Full response body |

### Log Storage

Logs are stored per monitoring session:

```
outputs/canary-logs/{domain}/{date}/
├── check-001/
│   ├── console.json      # Browser console messages
│   ├── network.json      # Failed network requests
│   └── server.log        # Server-side log tail
├── check-002/
│   ├── ...
└── session-summary.json  # Aggregated log stats
```

### Session Summary

After monitoring completes, generate a log summary:

```json
{
  "session_id": "canary-2026-04-10-staging",
  "total_checks": 10,
  "unique_console_errors": 3,
  "unique_network_failures": 1,
  "server_error_lines": 12,
  "error_timeline": [
    {"check": 3, "timestamp": "...", "new_errors": ["TypeError at dashboard.js:142"]},
    {"check": 4, "timestamp": "...", "new_errors": []}
  ],
  "top_errors": [
    {"message": "TypeError: Cannot read properties of undefined", "occurrences": 7, "source": "dashboard.js:142"},
    {"message": "Failed to fetch /api/metrics", "occurrences": 3, "source": "network"}
  ]
}
```

### Log Retention

- Keep logs for 7 days by default
- Logs associated with confirmed regressions are preserved indefinitely (moved to `outputs/incidents/`)
- Run `canary-monitor --prune-logs` to manually clean up old sessions

## Examples

### Example 1: Post-deploy quick check

User runs `/canary-monitor http://localhost:3000` after deploying a new feature.

Actions:
1. Load existing baseline
2. Monitor `/` for 5 minutes with 60s intervals
3. 5 clean checks — all pass
4. Report: all clear, suggest baseline refresh

### Example 2: Staging regression detection

User runs `/canary-monitor https://staging.example.com --pages /,/api/health,/dashboard --duration 10m`.

Actions:
1. Load baseline for staging domain
2. Check 1: `/dashboard` has 2 new console errors (suspicious)
3. Check 2: same 2 errors persist → CONFIRMED regression
4. Alert with error details and recommendation
5. Remaining checks run for other pages
6. Final report with 1 confirmed regression

## Error Handling

| Scenario | Action |
|----------|--------|
| Page unreachable | Mark as network failure, apply 2-consecutive rule |
| Browser timeout | Retry once, then mark as failure |
| No baseline found | Capture fresh baseline before starting monitoring |
| All pages fail | Stop monitoring early, report as critical failure |
