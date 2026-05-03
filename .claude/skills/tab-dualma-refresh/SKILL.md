---
name: tab-dualma-refresh
description: >-
  Daily refresh of DualMA strategy indicators via daily_stock_check --source
  db script. Use when refreshing DualMA, '이중이평선 갱신', 'tab-dualma-refresh'. Do
  NOT use for DualMA backtesting (use POST /dualma/backtest/run), Turtle
  indicators (use tab-turtle-refresh), or stock price sync (use
  tab-stock-sync).
---

# tab-dualma-refresh

## Purpose

Refreshes DualMA (Dual Moving Average) strategy indicators for all tickers using the `daily_stock_check.py` script with DB source. Computes SMA crossover signals, RSI, MACD, and generates buy/sell signals.

## When to Use

- refresh dualma
- 이중이평선 갱신
- tab-dualma-refresh
- dual moving average refresh

## When NOT to Use

- DualMA backtesting — use `POST /dualma/backtest/run`
- Turtle indicators — use tab-turtle-refresh
- Stock price sync — use tab-stock-sync

## Workflow

1. Ensure backend is running and PostgreSQL has stock data
2. Run `python scripts/daily_stock_check.py --source db` to compute SMA crossover, RSI, MACD, buy/sell signals for all DB tickers
3. Signals are available for DualMA strategy views

## Scripts / Endpoints Used

- `scripts/daily_stock_check.py --source db` — primary batch path: computes all DualMA signals for all tickers from PostgreSQL data
- `POST /api/v1/dualma/indicators/backfill` — per-ticker backfill (requires `ticker_symbol`, `start_date`, `end_date`); not used for batch refresh

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

DualMA indicators and buy/sell signals refreshed for all tickers.
