---
description: "Refresh and query market breadth data via POST /market-breadth/refresh and GET /market-breadth/latest, /trend, /composite, /alerts. Use when refreshing breadth, 'market breadth refresh', '마켓 브레드스 갱신', 'tab-market-breadth'. Do NOT use for market environment analysis (use tab-market-environment), Turtle indicators (use tab-turtle-refresh), or stock price sync (use tab-stock-sync)."
---

# tab-market-breadth

## Purpose

Refresh market breadth data and query breadth metrics (composite score, trend, component health, alerts) via dedicated API endpoints.

## When to Use

- market breadth refresh
- 마켓 브레드스 갱신
- tab-market-breadth
- check breadth alerts
- breadth composite score

## When NOT to Use

- Market environment regime analysis — use tab-market-environment
- Turtle indicators — use tab-turtle-refresh
- Stock price sync — use tab-stock-sync

## Workflow

1. Call `POST /api/v1/market-breadth/refresh` to compute and store a new breadth snapshot
2. Read latest with `GET /api/v1/market-breadth/latest`
3. Check trend direction with `GET /api/v1/market-breadth/trend`
4. Get full component breakdown with `GET /api/v1/market-breadth/composite`
5. Check threshold alerts with `GET /api/v1/market-breadth/alerts`

## Endpoints Used

- `POST /api/v1/market-breadth/refresh` — compute and store new breadth snapshot from yfinance
- `GET /api/v1/market-breadth/latest` — latest snapshot with regime classification
- `GET /api/v1/market-breadth/history` — historical snapshots for charting (params: start_date, end_date, limit)
- `GET /api/v1/market-breadth/trend` — SMA, momentum, direction analysis (param: lookback)
- `GET /api/v1/market-breadth/composite` — full component breakdown with health flags
- `GET /api/v1/market-breadth/alerts` — threshold breach alerts (danger <30, caution <45, strong >70, extreme >85)

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL

## Output

Market breadth snapshot refreshed and available via multiple query endpoints.
