---
name: tab-market-environment
description: >-
  Refresh and query market environment (regime, breadth, news, signals) via
  POST /market-environment/refresh and GET /market-environment/summary,
  /details, /history, /regime/timeline. Use when checking market environment,
  '시장 환경 분석', 'tab-market-environment', 'market environment check'. Do NOT use
  for market breadth only (use tab-market-breadth), news only (use
  tab-news-fetch), or stock price sync (use tab-stock-sync).
---

# tab-market-environment

## Purpose

Refresh and query the aggregated market environment assessment combining breadth, news sentiment, active signals, and regime classification (risk_on/risk_off/neutral).

## When to Use

- market environment check
- 시장 환경 분석
- tab-market-environment
- market regime check
- what is the current market regime

## When NOT to Use

- Market breadth only — use tab-market-breadth
- News fetch only — use tab-news-fetch
- Stock price sync — use tab-stock-sync

## Workflow

1. Call `POST /api/v1/market-environment/refresh` to compute fresh breadth snapshot + summary
2. Read aggregated summary with `GET /api/v1/market-environment/summary`
3. Get detailed component breakdown with `GET /api/v1/market-environment/details`
4. View historical regime data with `GET /api/v1/market-environment/history`
5. View regime transitions with `GET /api/v1/market-environment/regime/timeline`
6. Check sector rotation with `GET /api/v1/market-environment/sector-rotation/current`

## Endpoints Used

- `POST /api/v1/market-environment/refresh` — trigger fresh computation and return summary
- `GET /api/v1/market-environment/summary` — aggregated regime + breadth + news + signals
- `GET /api/v1/market-environment/details` — detailed component breakdown (breadth, news by source, signals by type, freshness)
- `GET /api/v1/market-environment/history` — historical snapshots (params: start_date, end_date, limit)
- `GET /api/v1/market-environment/regime/timeline` — regime transition timeline
- `GET /api/v1/market-environment/sector-rotation/current` — sector strength and classification

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with breadth, news, and signal data

## Output

Market environment summary with regime classification and component details.
