---
description: "Daily refresh of Bollinger Bands signals via POST /bollinger-bands/daily-refresh across 4 methods. Use when refreshing Bollinger, '볼린저 밴드 갱신', 'tab-bollinger-refresh'. Do NOT use for Bollinger backtesting (use strategy-comparison), Turtle indicators (use tab-turtle-refresh), or stock price sync (use tab-stock-sync)."
---

# tab-bollinger-refresh

## Purpose

Refreshes Bollinger Bands signals for all tracked symbols using 4 methods (standard, Keltner, Donchian, and envelope). Calls `POST /bollinger-bands/daily-refresh` which computes indicators and signals in the background.

## When to Use

- refresh bollinger
- 볼린저 밴드 갱신
- tab-bollinger-refresh
- bollinger daily refresh

## When NOT to Use

- Bollinger backtesting — use strategy-comparison
- Turtle indicators — use tab-turtle-refresh
- Stock price sync — use tab-stock-sync

## Workflow

1. Ensure backend is running and PostgreSQL has stock data
2. Call `POST /api/v1/bollinger-bands/daily-refresh`
3. Backend computes Bollinger indicators and signals for all 4 methods
4. Signals are persisted for dashboard and strategy views

## API Endpoints Used

- `POST /api/v1/bollinger-bands/daily-refresh` — computes Bollinger Bands indicators and signals (standard, Keltner, Donchian, envelope methods) for all tracked symbols in background

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Background job completed; Bollinger Bands signals refreshed for all tracked symbols across 4 methods.
