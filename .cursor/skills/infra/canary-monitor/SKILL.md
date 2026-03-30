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
  version: "1.0.0"
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
| LCP regression threshold | 20% | Flag if LCP increases by this % |
| TTFB regression threshold | 50% | Flag if TTFB increases by this % |
| Console error tolerance | 0 | New errors above baseline |

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
