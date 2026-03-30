---
description: "Run multi-factor stock screening via POST /admin/screen-stocks combining P/E, RSI, volume, MA signals. Use when screening stocks, '종목 스크리닝', 'tab-screening'. Do NOT use for hot stock discovery (use tab-hot-stock-discovery), daily stock analysis (use daily-stock-check), or technical analysis only (use tab-technical-analysis)."
---

# tab-screening

## Purpose

Runs multi-factor stock screening on all tracked tickers. Calls `POST /admin/screen-stocks` with configurable thresholds (P/E max, RSI bounds, volume spike ratio). Screening combines fundamental data (P/E, market cap, FCF yield) with technical signals (RSI, MA crossovers, volume spikes) to generate BUY/SELL/NEUTRAL signals.

## When to Use

- screen stocks
- 종목 스크리닝
- tab-screening
- multi-factor screen

## When NOT to Use

- Hot stock discovery (use tab-hot-stock-discovery)
- Daily stock analysis (use daily-stock-check)
- Technical analysis only (use tab-technical-analysis)

## Workflow

1. Ensure backend server and PostgreSQL are running
2. Call `POST /api/v1/admin/screen-stocks` with optional threshold parameters
3. Wait for screening job to complete
4. Receive BUY/SELL/NEUTRAL signals for all tracked tickers

## API Endpoints Used

- `POST /api/v1/admin/screen-stocks` — Runs multi-factor screening with configurable P/E max, RSI bounds, volume spike ratio; combines fundamental and technical data to produce signals

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

BUY/SELL/NEUTRAL screening signals for all tracked tickers based on combined fundamental and technical criteria
