---
name: tab-technical-analysis
description: >-
  Pre-compute technical analysis indicators for all tracked tickers via POST
  /technical-analysis/batch-compute. Use when computing TA, '기술적 분석 계산',
  'tab-technical-analysis'. Do NOT use for Turtle indicators (use
  tab-turtle-refresh), Bollinger Bands (use tab-bollinger-refresh), or
  single-ticker analysis (use GET /technical-analysis).
---

# tab-technical-analysis

## Purpose

Pre-computes technical analysis indicators (SMA 20/55/200, RSI, MACD, Stochastic, ADX, Williams %R, CCI, Ultimate Oscillator, ROC, Bull/Bear Power, Pivot Points) for all tracked tickers. Calls `POST /technical-analysis/batch-compute` which processes all active tickers in the background.

## When to Use

- compute technical analysis
- 기술적 분석 계산
- tab-technical-analysis
- batch TA compute

## When NOT to Use

- On-demand single-ticker analysis — use GET /technical-analysis
- Turtle indicators — use tab-turtle-refresh
- Bollinger Bands — use tab-bollinger-refresh

## Workflow

1. Ensure backend is running and PostgreSQL has stock data
2. Call `POST /api/v1/technical-analysis/batch-compute`
3. Backend processes all active tickers in background
4. Indicators are persisted for subsequent queries

## API Endpoints Used

- `POST /api/v1/technical-analysis/batch-compute` — triggers batch computation of SMA 20/55/200, RSI, MACD, Stochastic, ADX, Williams %R, CCI, Ultimate Oscillator, ROC, Bull/Bear Power, and Pivot Points for all tracked tickers

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Background job started; technical indicators are pre-computed and stored for all active tickers.
