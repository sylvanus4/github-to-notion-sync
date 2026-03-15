---
description: "Daily refresh of Turtle Trading indicators via POST /turtle/indicators/daily-refresh. Use when refreshing Turtle indicators, '터틀 지표 갱신', 'tab-turtle-refresh'. Do NOT use for Turtle backtesting (use POST /turtle/backtest/run), Bollinger Bands (use tab-bollinger-refresh), or stock price sync (use tab-stock-sync)."
---

# tab-turtle-refresh

## Purpose

Refreshes Turtle Trading indicators (Moving Averages + Donchian Channels) for all active instruments. Calls `POST /turtle/indicators/daily-refresh` which backfills indicators for the last 5 days.

## When to Use

- refresh turtle indicators
- 터틀 지표 갱신
- tab-turtle-refresh
- turtle daily refresh

## When NOT to Use

- Turtle backtesting — use POST /turtle/backtest/run
- Bollinger Bands — use tab-bollinger-refresh
- Stock price sync — use tab-stock-sync

## Workflow

1. Ensure backend is running and PostgreSQL has stock data
2. Call `POST /api/v1/turtle/indicators/daily-refresh`
3. Backend backfills MA and Donchian indicators for last 5 days
4. Indicators are available for Turtle strategy views

## API Endpoints Used

- `POST /api/v1/turtle/indicators/daily-refresh` — backfills Turtle Trading indicators (Moving Averages + Donchian Channels) for all active instruments over the last 5 days

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Background job completed; Turtle indicators refreshed for all active instruments with 5-day backfill.
