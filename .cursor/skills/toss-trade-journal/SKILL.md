---
name: toss-trade-journal
version: 1.0.0
description: >-
  Log executed trades with full context (signal source, entry reasoning, market
  conditions), track cumulative P&L, win rate, and strategy performance.
  Generate monthly trade journal reports as .docx via anthropic-docx.
  Use when the user asks to "log trade", "trade journal", "매매 일지",
  "거래 기록", "trading performance", "승률 분석", "P&L report",
  or when invoked after tossinvest-trading completes an order.
  Do NOT use for placing orders (use tossinvest-trading).
  Do NOT use for portfolio snapshots (use toss-daily-snapshot).
  Do NOT use for risk assessment (use toss-risk-monitor).
triggers:
  - trade journal
  - log trade
  - trading performance
  - win rate
  - trade log
  - 매매 일지
  - 거래 기록
  - 승률 분석
  - 매매 성과
  - P&L 리포트
  - 거래 로그
tags: [trading, journal, performance, toss-securities, analytics]
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "trading"
---

# toss-trade-journal

Log trades with context and track cumulative performance analytics.

## When to Use

- After `tossinvest-trading` completes an order (auto-log)
- Reviewing monthly/weekly trading performance
- Analyzing win rate by strategy, sector, or time
- Generating a formal trade journal document

## When NOT to Use

- For placing orders → use `tossinvest-trading`
- For daily snapshots → use `toss-daily-snapshot`
- For risk checks → use `toss-risk-monitor`

## Prerequisites

- `tossctl` installed and in PATH
- Trade data from `tossinvest-trading` execution or manual entry

## Data Model

Each journal entry in `outputs/toss/journal-{YYYY-MM}.json`:

```json
{
  "id": "2026-03-24-001",
  "timestamp": "2026-03-24T10:30:00+09:00",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 10,
  "price": 178.50,
  "total_cost": 1785.00,
  "currency": "USD",
  "order_id": "toss-order-12345",
  "signal_source": "daily-stock-check/STRONG_BUY",
  "strategy": "turtle-trading",
  "thesis": "SMA20 crossed above SMA55, RSI 45, entering uptrend",
  "market_context": {
    "market_regime": "risk-on",
    "vix": 14.2,
    "sp500_change": "+0.8%"
  },
  "tags": ["momentum", "us-tech"],
  "exit": null
}
```

When a position is closed, update the entry's `exit` field:

```json
{
  "exit": {
    "timestamp": "2026-04-02T14:15:00+09:00",
    "price": 185.20,
    "quantity": 10,
    "pnl": 67.00,
    "pnl_pct": 3.75,
    "holding_days": 9,
    "exit_reason": "target-hit"
  }
}
```

## Workflow

### Mode A: Log a Trade

1. Capture order details from `tossinvest-trading` output or user input
2. Optionally fetch market context via `tossctl account summary --output json`
3. Ask user for thesis/reasoning (or use pipeline signal description)
4. Append entry to `outputs/toss/journal-{YYYY-MM}.json`
5. Confirm with a Korean summary

### Mode B: Analyze Performance

1. Load all journal files from `outputs/toss/journal-*.json`
2. Filter closed trades (those with `exit` field)
3. Compute analytics:

| Metric | Calculation |
|--------|------------|
| Win rate | Closed trades with positive P&L / total closed |
| Average win | Mean P&L of winning trades |
| Average loss | Mean P&L of losing trades |
| Profit factor | Total wins / Total losses |
| Average holding period | Mean holding_days of closed trades |
| Best trade | Highest single P&L |
| Worst trade | Lowest single P&L |

4. Break down by:
   - **Strategy**: turtle-trading, bollinger, dualma, manual
   - **Sector**: tech, healthcare, finance, etc.
   - **Market**: US vs KR
   - **Month**: monthly P&L curve

### Mode C: Generate Monthly Report

1. Run Mode B analytics for the target month
2. Generate `.docx` via `anthropic-docx` skill with:
   - Executive summary
   - Monthly P&L chart description
   - Trade log table (all entries)
   - Win/loss analysis
   - Strategy performance comparison
   - Lessons learned (from `exit_reason` patterns)
3. Save to `outputs/toss/journal-report-{YYYY-MM}.docx`

## Report Format (Korean)

```
📊 매매 일지 분석 (2026-03)
━━━━━━━━━━━━━━━━━━━━━━━━
총 거래: 24건 (매수 15 / 매도 9)
청산 완료: 9건
승률: 66.7% (6승 3패)
평균 수익: +₩45,200 / 평균 손실: -₩28,100
수익 팩터: 3.22
평균 보유 기간: 7.3일

전략별 승률:
- Turtle Trading: 75.0% (3/4)
- Bollinger: 60.0% (3/5)

최고 거래: NVDA +12.3% (+₩156,000)
최악 거래: TSLA -5.1% (-₩42,300)
```

## Examples

```
User: 오늘 체결 내역 저널에 기록해줘
Agent: toss-trade-journal 실행 → 3건 기록 완료
  - NVDA 매수 5주 @ $875.20
  - AAPL 매도 10주 @ $178.50 (수익률 +12.3%)
  - SOFI 매수 20주 @ $14.80

User: 이번 달 성과 분석해줘
Agent: 2026년 3월 거래 분석:
  - 총 거래: 12건 (매수 7, 매도 5)
  - 승률: 80% (4/5)
  - 평균 수익률: +8.7%

User: /tossinvest-journal
Agent: (runs full journal sync + monthly report)
```

## Error Handling

| Error | Action |
|-------|--------|
| Journal file does not exist | Create new file for current month |
| Duplicate order_id | Skip logging, warn user |
| No closed trades for analysis | Report open positions only, suggest patience |
