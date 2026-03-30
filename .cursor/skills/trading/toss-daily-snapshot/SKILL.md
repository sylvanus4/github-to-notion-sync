---
name: toss-daily-snapshot
version: 1.0.0
description: >-
  Archive a daily snapshot of the Toss Securities account state (positions,
  account summary, watchlist, completed orders) to outputs/toss/ for historical
  tracking and equity curve analysis. Compares today vs yesterday to detect
  new/closed positions and daily P&L changes.
  Use when the user asks to "snapshot toss", "archive toss portfolio",
  "daily snapshot", "토스 일일 스냅샷", "포트폴리오 저장", "toss snapshot",
  "save toss state", or when invoked by the today/morning pipeline.
  Do NOT use for live trading (use tossinvest-trading).
  Do NOT use for real-time portfolio queries without archiving (use tossinvest-cli).
  Do NOT use for trade journal logging (use toss-trade-journal).
triggers:
  - daily snapshot
  - archive toss
  - toss snapshot
  - save toss state
  - 토스 일일 스냅샷
  - 포트폴리오 저장
  - 토스 상태 저장
  - 포지션 아카이브
tags: [trading, brokerage, snapshot, toss-securities, portfolio, archival]
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "trading"
---

# toss-daily-snapshot

Archive daily Toss Securities account state to `outputs/toss/` for historical tracking, equity curve generation, and day-over-day comparison.

## When to Use

- End-of-day or start-of-day portfolio archival
- Building a historical equity curve
- Comparing today's holdings vs yesterday
- Pipeline integration: called by `today` (Phase 1.5) or `morning-ship`

## When NOT to Use

- For live read-only queries without saving → use `tossinvest-cli`
- For trade logging after execution → use `toss-trade-journal`
- For risk assessment → use `toss-risk-monitor`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session (`tossctl auth status`)

## Workflow

### Step 1: Verify Auth

```bash
tossctl auth status --output json
```

If session expired, prompt user to re-authenticate via `tossinvest-setup`.

### Step 2: Create Output Directory

```bash
mkdir -p outputs/toss
```

### Step 3: Capture Snapshots

Run all four captures and save to date-stamped files:

```bash
DATE=$(date +%Y-%m-%d)

tossctl portfolio positions --output json > "outputs/toss/positions-${DATE}.json"
tossctl account summary --output json > "outputs/toss/summary-${DATE}.json"
tossctl watchlist list --output json > "outputs/toss/watchlist-${DATE}.json"
tossctl orders completed --output json > "outputs/toss/completed-${DATE}.json"
```

### Step 4: Day-over-Day Comparison

1. Load today's `positions-{date}.json` and yesterday's
2. Identify:
   - **New positions**: in today but not yesterday
   - **Closed positions**: in yesterday but not today
   - **P&L changes**: per-position unrealized P&L delta
3. Calculate daily return: `(today_total - yesterday_total) / yesterday_total`

### Step 5: Update Equity Curve

Append today's data point to `outputs/toss/equity-curve.json`:

```json
{
  "date": "2026-03-24",
  "total_assets": 15234567,
  "cash": 2345678,
  "invested": 12888889,
  "unrealized_pnl": 456789,
  "daily_return_pct": 0.85,
  "positions_count": 12
}
```

If `equity-curve.json` does not exist, create it as an array with today's entry.

### Step 6: Report

Present a Korean summary:

```
📸 Toss 일일 스냅샷 (2026-03-24)
━━━━━━━━━━━━━━━━━━━━━━━━
총 자산: ₩15,234,567 (전일 대비 +0.85%)
현금: ₩2,345,678
투자 중: ₩12,888,889
미실현 손익: +₩456,789

신규 진입: AAPL, 005930
청산 완료: TSLA
보유 종목 수: 12
```

## Output Files

| File | Content |
|------|---------|
| `outputs/toss/positions-{date}.json` | All current holdings with quantities, avg price, P&L |
| `outputs/toss/summary-{date}.json` | Account totals: assets, cash, buying power |
| `outputs/toss/watchlist-{date}.json` | Current watchlist items |
| `outputs/toss/completed-{date}.json` | Completed orders for the day |
| `outputs/toss/equity-curve.json` | Cumulative daily data points for charting |

## Examples

```
User: 오늘 토스 스냅샷 찍어줘
Agent: toss-daily-snapshot 실행 → outputs/toss/snapshot-2026-03-24.json 저장 완료

User: toss daily snapshot
Agent: (runs the full workflow, presents summary with daily changes)

User: /today (with skip-toss not set)
Agent: Phase 1.5에서 자동으로 toss-daily-snapshot 실행
```

## Error Handling

| Error | Action |
|-------|--------|
| `No active session` | Prompt `tossctl auth login` |
| Yesterday's snapshot missing | Skip comparison, log today as first entry |
| `Rate limited` | Wait 30s, retry each command sequentially |
| Write permission error | Check `outputs/toss/` directory permissions |
