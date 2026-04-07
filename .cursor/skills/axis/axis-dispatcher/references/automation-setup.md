# Cursor Automations Setup — 6-Axis Dispatcher

Configuration guide for setting up recurring axis-dispatcher runs via
Cursor Automations cloud agents.

## Prerequisites

- Active Cursor subscription with cloud agent access
- Slack integration connected at [cursor.com/dashboard](https://cursor.com/dashboard)
- GitHub connection for repository access

## Automations to Create

Create these at [cursor.com/automations/new](https://cursor.com/automations/new).

### 1. Morning Routine (Weekdays 07:00 KST)

| Field | Value |
|-------|-------|
| **Name** | `6-Axis Morning Dispatch` |
| **Trigger** | Scheduled — cron `0 22 * * 0-4` (UTC, = 07:00 KST Mon-Fri) |
| **Repository** | `hyojunguy/ai-model-event-stock-analytics` |
| **Tools** | Send to Slack, Read Slack Channels, MCP |
| **Environment** | Enabled (needs Python for scripts) |
| **Memory** | Enabled (track patterns across runs) |

**Prompt:**

```
You are the 6-Axis Morning Dispatcher for the ai-model-event-stock-analytics project.

## Goal
Execute the morning routine of the 6-Axis Personal Assistant system.

## Execution Order
1. Read and invoke axis-life SKILL.md (Phase 0 — Life First)
2. In parallel, invoke: axis-recruitment, axis-investment, axis-learning, axis-sidepm (Phase 1)
3. After Phase 1, invoke axis-gm (Phase 2 — GM Aggregation)
4. Post consolidated briefing to #효정-할일 (Phase 3)

## Output Format
Write dispatch manifest to outputs/axis/gm/{today}/dispatch-morning.json.
Post a structured Slack thread to #효정-할일 with:
- Main: 6-axis status grid
- Reply 1: Top priorities
- Reply 2: Pending decisions
- Reply 3: Errors (if any)

## Error Handling
If an axis fails, record the error, post an alert to #효정-할일, and continue
running remaining axes. If 3+ axes fail, escalate to #효정-의사결정.
```

### 2. Evening Routine (Weekdays 17:00 KST)

| Field | Value |
|-------|-------|
| **Name** | `6-Axis Evening Dispatch` |
| **Trigger** | Scheduled — cron `0 8 * * 1-5` (UTC, = 17:00 KST Mon-Fri) |
| **Repository** | `hyojunguy/ai-model-event-stock-analytics` |
| **Tools** | Send to Slack, Read Slack Channels, MCP |
| **Environment** | Enabled |
| **Memory** | Enabled |

**Prompt:**

```
You are the 6-Axis Evening Dispatcher for the ai-model-event-stock-analytics project.

## Goal
Execute the evening routine of the 6-Axis Personal Assistant system.

## Execution Order
1. axis-life evening (Phase 0)
2. Parallel: axis-investment EOD, axis-sidepm EOD shipping, axis-learning paper processing, axis-recruitment follow-ups (Phase 1)
3. axis-gm daily digest (Phase 2)
4. Consolidated EOD briefing to #효정-할일 (Phase 3)

## Output Format
Write dispatch manifest to outputs/axis/gm/{today}/dispatch-evening.json.
Post EOD summary to #효정-할일.

## Error Handling
Same as morning — isolate failures, alert, continue.
```

### 3. Weekly Routine (Friday 17:30 KST)

| Field | Value |
|-------|-------|
| **Name** | `6-Axis Weekly Review` |
| **Trigger** | Scheduled — cron `30 8 * * 5` (UTC, = 17:30 KST Friday) |
| **Repository** | `hyojunguy/ai-model-event-stock-analytics` |
| **Tools** | Send to Slack, Read Slack Channels, MCP |
| **Environment** | Enabled |
| **Memory** | Enabled |

**Prompt:**

```
You are the 6-Axis Weekly Review Dispatcher.

## Goal
After the Friday evening routine completes, execute the weekly review phases.

## Execution Order
1. Check that dispatch-evening.json exists for today (Friday evening ran)
2. Parallel: axis-learning weekly progress, axis-sidepm weekly report (Phase W1)
3. axis-gm weekly OKR, improvement recs, executive briefing (Phase W2)
4. Post weekly summary to #효정-할일, sync to Notion (Phase W3)

## Output Format
Write dispatch manifest to outputs/axis/gm/{today}/dispatch-weekly.json.
Post weekly summary thread to #효정-할일.
```

## Verification After Setup

After creating automations:

1. Go to [cursor.com/automations](https://cursor.com/automations)
2. Verify all 3 automations appear with correct schedules
3. Run the morning automation manually once to verify
4. Check `#효정-할일` for the test briefing
5. Verify `outputs/axis/gm/{date}/dispatch-morning.json` was created

## Timezone Notes

- All cron expressions are in **UTC**
- KST = UTC + 9 hours
- `0 22 * * 0-4` UTC = Monday–Friday 07:00 KST
- `0 8 * * 1-5` UTC = Monday–Friday 17:00 KST
- `30 8 * * 5` UTC = Friday 17:30 KST

## Fallback for Local Execution

If Cursor Automations are unavailable, run manually:

```bash
# From the project root, start a Cursor agent with:
# "Run the axis-dispatcher morning routine"
```

Or use a local cron job that opens Cursor:

```bash
# Example launchd plist for macOS (advanced)
# ~/Library/LaunchAgents/com.thaki.axis-morning.plist
```
