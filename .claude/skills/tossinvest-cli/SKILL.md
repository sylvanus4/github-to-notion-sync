---
name: tossinvest-cli
description: >-
  Execute read-only tossctl commands for Toss Securities — account info,
  portfolio positions, stock quotes, order history, watchlist, and data
  export. Use when the user asks to "check toss account", "toss portfolio",
  "toss quote", "토스 계좌", "토스 포트폴리오", "토스 시세", "토스 주문내역", or needs read-only
  data from Toss Securities. Do NOT use for live trading operations like
  buy/sell/cancel/amend (use tossinvest-trading). Do NOT use for setup,
  installation, or authentication (use tossinvest-setup). Do NOT use for
  non-Toss brokerage queries (use tab-kiwoom for Kiwoom Securities).
---

# tossinvest-cli

Run read-only tossctl commands against Toss Securities: account summaries, portfolio positions, stock quotes, order history, watchlist, and CSV export.

## When to Use

Use when the user asks to check their Toss Securities account, view portfolio positions or allocation, get stock quotes, view pending or completed orders, check their watchlist, or export data to CSV.

## When NOT to Use

- For installing or authenticating tossctl → use `tossinvest-setup`
- For placing, canceling, or amending orders → use `tossinvest-trading`
- For Kiwoom Securities data → use `tab-kiwoom`
- For Yahoo Finance stock data → use `weekly-stock-update`

## Prerequisites

- tossctl installed and in PATH
- Active authenticated session (`tossctl auth status` shows valid session)
- For Korean market data: KRX trading hours awareness (09:00-15:30 KST)

## Commands Reference

### Account

```bash
# List all linked accounts
tossctl account list
tossctl account list --output json

# Account summary (balances, buying power)
tossctl account summary
tossctl account summary --output json
```

Output fields (summary): total asset value, cash balance, invested amount, unrealized P&L, buying power.

### Portfolio

```bash
# Current positions
tossctl portfolio positions
tossctl portfolio positions --output json

# Allocation breakdown
tossctl portfolio allocation
tossctl portfolio allocation --output json
```

Output fields (positions): symbol, name, quantity, average price, current price, P&L, P&L percentage, market value.

### Stock Quotes

```bash
# Single quote
tossctl quote get AAPL
tossctl quote get 005930          # Samsung Electronics (KRX code)

# Batch quotes (multiple symbols)
tossctl quote batch AAPL MSFT GOOGL TSLA
tossctl quote batch 005930 000660 035420

# With JSON output
tossctl quote get AAPL --output json
tossctl quote batch AAPL MSFT --output json
```

Output fields: symbol, name, price, change, change percentage, volume, market status.

### Order History

```bash
# Pending (open) orders
tossctl orders list
tossctl orders list --output json

# Completed orders
tossctl orders completed
tossctl orders completed --market us    # US market only
tossctl orders completed --market kr    # Korean market only
tossctl orders completed --output json
```

Output fields: order ID, symbol, side (buy/sell), quantity, price, status, submitted time.

### Watchlist

```bash
# View watchlist
tossctl watchlist list
tossctl watchlist list --output json
```

### Data Export

```bash
# Export positions to CSV
tossctl export positions
tossctl export positions --output json  # JSON format instead

# Export order history to CSV
tossctl export orders
tossctl export orders --market us
tossctl export orders --market kr
```

CSV files are written to stdout by default. Redirect to save:

```bash
tossctl export positions > ~/positions.csv
tossctl export orders --market us > ~/us-orders.csv
```

## Output Formats

All commands support `--output` flag:
- `text` (default): human-readable table format
- `json`: machine-readable JSON

Always prefer `--output json` when parsing results programmatically.

## Examples

### Example 1: Portfolio overview

User: "토스 포트폴리오 보여줘"

Actions:
1. Check auth → `tossctl auth status --output json`
2. Fetch positions → `tossctl portfolio positions --output json`
3. Present holdings with P&L in Korean

### Example 2: Batch quote check

User: "AAPL, TSLA, 005930 시세 조회해줘"

Actions:
1. Fetch quotes → `tossctl quote batch AAPL TSLA 005930 --output json`
2. Present price, change, volume in a formatted table

### Example 3: Export order history

User: "이번 달 주문내역 CSV로 저장해줘"

Actions:
1. Export → `tossctl export orders > ~/toss-orders-2026-03.csv`
2. Confirm file saved

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `No active session` | Authentication expired | Run `tossctl auth login` |
| `Rate limited` | Too many API requests | Wait 30s and retry |
| `Network error` | Connectivity issue | Check internet connection |
| `Invalid symbol` | Unrecognized ticker | Verify symbol format (US tickers or KRX numeric codes) |

## Integration with Daily Pipeline

tossctl read-only data can feed into the daily trading analysis pipeline:

1. `tossctl portfolio positions --output json` → current holdings for analysis
2. `tossctl orders completed --output json` → execution history for performance tracking
3. `tossctl quote batch <symbols> --output json` → real-time prices for watchlist stocks
4. `tossctl export positions > outputs/toss-positions-$(date +%Y-%m-%d).csv` → daily snapshot
