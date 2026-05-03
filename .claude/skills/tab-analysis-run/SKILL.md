---
name: tab-analysis-run
description: >-
  Run event study analysis (CAR), generate reports, and query patterns. Use
  when running analysis, '분석 실행', 'tab-analysis-run', 'event study', 'generate
  daily report'. Do NOT use for event detection (use tab-event-detect), stock
  screening (use tab-screening), or technical analysis (use
  tab-technical-analysis).
disable-model-invocation: true
---

# tab-analysis-run

## Purpose

Runs event study analysis and generates reports. Calls two endpoints sequentially: `POST /analysis/run` for event study (CAR calculation) and `POST /reports/generate` for daily report creation. Optionally queries `GET /patterns` to retrieve aggregated pattern data.

## When to Use

- run analysis
- 분석 실행
- tab-analysis-run
- event study analysis
- generate daily report

## When NOT to Use

- Event detection (use tab-event-detect)
- Stock screening (use tab-screening)
- Technical analysis (use tab-technical-analysis)

## Workflow

1. Ensure backend server and PostgreSQL are running
2. Call `POST /api/v1/analysis/run` to execute event study (CAR calculation)
3. Call `POST /api/v1/reports/generate` to create daily report
4. Call `GET /api/v1/patterns` to query aggregated patterns (read-only, does not recompute)

## API Endpoints Used

- `POST /api/v1/analysis/run` — Runs event study analysis (CAR calculation)
- `POST /api/v1/reports/generate` — Generates daily report
- `GET /api/v1/patterns` — Queries aggregated pattern data (read-only)

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Event study results (CAR), generated daily report, and refreshed pattern aggregation
