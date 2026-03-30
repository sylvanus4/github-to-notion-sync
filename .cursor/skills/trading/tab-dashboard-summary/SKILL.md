---
description: "Fetch aggregated dashboard data in a single API call via GET /dashboard/agent-summary. Use when fetching dashboard overview, '대시보드 요약', 'tab-dashboard-summary', 'agent dashboard'. Do NOT use for individual market breadth (use tab-market-breadth), individual market environment (use tab-market-environment), or stock analysis (use daily-stock-check)."
---

# tab-dashboard-summary

## Purpose

Fetch a consolidated dashboard overview in a single API call — summary statistics, recent events, top movers, and market regime — optimized for agent consumption.

## When to Use

- dashboard overview
- 대시보드 요약
- tab-dashboard-summary
- agent dashboard summary
- quick project status

## When NOT to Use

- Market breadth details — use tab-market-breadth
- Market environment regime analysis — use tab-market-environment
- Daily stock analysis — use daily-stock-check

## Workflow

1. Call `GET /api/v1/dashboard/agent-summary` to fetch all dashboard data
2. Response includes: summary (total_stocks, total_events, active_signals, avg_car), recent_events (last 5), top_movers (top 5 by absolute CAR), market_regime (current regime label from market environment)

## Endpoints Used

- `GET /api/v1/dashboard/agent-summary` — all-in-one dashboard for agents
- `GET /api/v1/dashboard/summary` — basic summary stats (total stocks, events, signals, avg CAR)
- `GET /api/v1/dashboard/recent-events` — recent events
- `GET /api/v1/dashboard/top-movers` — top movers by CAR

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL

## Output

Single JSON response with summary, events, movers, and market regime suitable for agent processing.
