# Per-Axis Failure Alerting Protocol

Standard failure handling for all 6-axis orchestrators and the dispatcher.
Each axis follows this protocol independently; the dispatcher aggregates
failure counts for escalation decisions.

## Failure Classification

### Severity Levels

| Level | Label | Description | Alert Channel |
|-------|-------|-------------|---------------|
| S1 | CRITICAL | Axis cannot start (missing prerequisites, auth failure) | `#효정-의사결정` |
| S2 | DEGRADED | One or more phases failed but others completed | `#효정-할일` |
| S3 | WARNING | Non-blocking issue (stale data, slow response) | `#효정-할일` (threaded) |
| S4 | INFO | Expected skip (market closed, no new data) | Logged only, no Slack |

## Per-Axis Error Handling

Each axis orchestrator MUST implement this pattern:

### 1. Phase-Level Try-Continue

Each phase within an axis runs independently. If Phase N fails, record the
error and continue to Phase N+1 (unless Phase N+1 depends on Phase N's output).

```
Phase 1: [TRY] → Success ✓
Phase 2: [TRY] → FAIL → record error → continue
Phase 3: [TRY] → Success ✓ (if independent of Phase 2)
```

### 2. Error Record Format

Each axis writes failed phases to its output directory:

**File**: `outputs/axis/{axis-name}/{date}/errors.json`

```json
{
  "axis": "investment",
  "axis_number": 2,
  "date": "2026-04-07",
  "severity": "S2",
  "errors": [
    {
      "phase": "Phase 2: Screening",
      "error_type": "API_TIMEOUT",
      "message": "Backend /admin/screen-stocks timed out after 60s",
      "timestamp": "2026-04-07T07:15:23+09:00",
      "recovery_attempted": true,
      "recovery_result": "Retry 1/3 also timed out. Skipped.",
      "impact": "Screening results unavailable; downstream analysis uses previous day's data"
    }
  ],
  "phases_completed": 5,
  "phases_total": 7,
  "overall_status": "DEGRADED"
}
```

### 3. Slack Alert Template

For S1 and S2 failures, post to the designated Slack channel.

**S2 (DEGRADED) — posted to `#효정-할일`:**

```
⚠️ [Axis 2: Investment] DEGRADED — 5/7 phases completed

Failed phases:
• Phase 2 (Screening): API_TIMEOUT — backend /admin/screen-stocks timed out
• Impact: Screening skipped, using yesterday's data

Successful phases:
✅ Phase 1 (Stock Sync) ✅ Phase 3 (Turtle) ✅ Phase 4 (Bollinger)
✅ Phase 5 (Report) ✅ Phase 7 (Slack Post)

📄 Error log: outputs/axis/investment/2026-04-07/errors.json
```

**S1 (CRITICAL) — posted to `#효정-의사결정`:**

```
🚨 [Axis 1: Recruitment] CRITICAL — Cannot start

Error: GitHub API authentication failed (401 Unauthorized)
Impact: Entire recruitment axis skipped for today
Required action: Check GITHUB_TOKEN expiration

📄 Error log: outputs/axis/recruitment/2026-04-07/errors.json
```

### 4. Retry Policy

| Error Type | Retries | Backoff | Fallback |
|------------|---------|---------|----------|
| API_TIMEOUT | 2 | 10s, 30s | Use previous day's data |
| AUTH_FAILURE | 0 | — | Mark axis CRITICAL, alert |
| MISSING_DATA | 0 | — | Mark phase SKIPPED |
| RATE_LIMIT | 3 | 30s, 60s, 120s | Reduce batch size |
| NETWORK_ERROR | 2 | 5s, 15s | Skip phase |
| SCRIPT_ERROR | 0 | — | Log traceback, continue |

## Dispatcher-Level Aggregation

The `axis-dispatcher` collects all `errors.json` files after each dispatch
cycle and applies escalation rules:

### Escalation Matrix

| Condition | Action |
|-----------|--------|
| 1 axis DEGRADED | Include in briefing, no escalation |
| 2 axes DEGRADED | Post warning to `#효정-할일` |
| 3+ axes DEGRADED | Escalate to `#효정-의사결정` |
| 1 axis CRITICAL | Post alert to `#효정-할일` |
| 2+ axes CRITICAL | Escalate to `#효정-의사결정` with full error dump |
| GM axis fails | Emergency fallback: post raw axis summaries |

### Dispatch Manifest Error Section

The dispatcher's manifest (`dispatch-{routine}.json`) includes an error
summary section:

```json
{
  "errors": {
    "total_errors": 2,
    "critical_count": 0,
    "degraded_count": 1,
    "warning_count": 1,
    "per_axis": {
      "life": { "status": "GREEN", "errors": [] },
      "recruitment": { "status": "GREEN", "errors": [] },
      "investment": { "status": "YELLOW", "errors": [{"phase": "Phase 2", "severity": "S2"}] },
      "learning": { "status": "GREEN", "errors": [] },
      "sidepm": { "status": "GREEN", "errors": [] },
      "gm": { "status": "GREEN", "errors": [] }
    },
    "escalation_triggered": false
  }
}
```

## Circuit Breaker

If an axis fails with S1 severity for 3 consecutive days:

1. Auto-disable the axis in `outputs/axis/automation-levels.json` (set to -1)
2. Post a persistent alert to `#효정-의사결정`
3. The axis remains disabled until a human resets the level to 0

This prevents wasting compute on a permanently broken axis.

## Integration Points

- Each `axis-*.SKILL.md` references this document for error handling
- The `axis-dispatcher.SKILL.md` references this for aggregation rules
- `axis-gm` reads `errors.json` from all axes during Phase 1 (cross-axis scan)
- All error files are keyed by date for idempotent re-runs
