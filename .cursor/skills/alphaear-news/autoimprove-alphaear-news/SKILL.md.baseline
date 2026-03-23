---
name: alphaear-news
description: >-
  Fetch real-time financial news from 10+ sources (Weibo, Zhihu, WallstreetCN,
  Hacker News, etc.) and Polymarket prediction market data. Use when the user
  needs hot finance news, unified trend reports from multiple sources, or
  Polymarket finance prediction data. Do NOT use for stock price data (use
  weekly-stock-update or alphaear-stock). Do NOT use for sentiment scoring (use
  alphaear-sentiment). Korean triggers: "뉴스", "리포트", "주식", "시장".
metadata:
  version: "1.0.0"
  category: "data-collection"
  author: "alphaear"
---
# AlphaEar News

## Overview

Fetch real-time hot financial news from 10+ sources (CN, US, KR-relevant), generate unified trend reports, and retrieve Polymarket prediction market data. News is stored in PostgreSQL via `scripts/database_manager.py`.

## Prerequisites

- Python 3.10+
- `requests`, `loguru`
- `scripts/database_manager.py` (PostgreSQL connection)
- Network access to NewsNow API and Polymarket gamma-api

## Workflow

1. **Initialize**: Create `DatabaseManager` with PostgreSQL connection, then instantiate `NewsNowTools(db)` or `PolymarketTools(db)`.
2. **Fetch hot news**: Call `NewsNowTools.fetch_hot_news(source_id, count)` — see `references/sources.md` for valid `source_id` values.
3. **Unified trends**: Call `NewsNowTools.get_unified_trends(sources)` to aggregate top news from multiple sources.
4. **Polymarket data**: Call `PolymarketTools.get_market_summary(limit)` for prediction market summaries.
5. **US/KR fallback**: If Reuters, Bloomberg, or CNBC content is needed and not available via NewsNow, use the `parallel-web-search` skill to supplement with web search results.
6. **Storage**: Fetched news is saved to PostgreSQL `daily_news` table by the tools.

## Examples

| Trigger | Action | Result |
|--------|--------|--------|
| "Get hot finance news from wallstreetcn" | `fetch_hot_news("wallstreetcn", 15)` | List of 15 trending headlines with URLs |
| "Unified trends from weibo, zhihu, cls" | `get_unified_trends(["weibo","zhihu","cls"])` | Markdown report aggregating top items per source |
| "Polymarket prediction markets" | `get_market_summary(10)` | Formatted report of top 10 active prediction markets |
| "US market news today" | `fetch_hot_news("hackernews", 10)` + `parallel-web-search` for Reuters/CNBC | Combined CN + US-relevant headlines |

## Sources Reference

Full source list: `references/sources.md`. Key IDs:

- **Finance**: `cls`, `wallstreetcn`, `xueqiu`
- **General**: `weibo`, `zhihu`, `baidu`, `toutiao`, `thepaper`
- **Tech / US**: `hackernews`, `36kr`, `ithome`, `v2ex`, `juejin`
- **US/KR market supplement**: Use `parallel-web-search` for Reuters, Bloomberg, CNBC, or KR finance sites when needed.

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| NewsNow API timeout | Returns empty or stale cache | Retry after 5 min; cache expires in 300s |
| Polymarket 4xx/5xx | Returns `[]` | Check gamma-api status; retry later |
| DB connection failure | Exception raised | Verify PostgreSQL is running and credentials |
| Invalid `source_id` | Empty items | Check `references/sources.md` for valid IDs |

## Troubleshooting

- **Empty results**: Verify `source_id` spelling; some sources may be rate-limited.
- **Stale data**: Built-in 5-minute cache; force fresh fetch by waiting or clearing cache.
- **Missing US/KR sources**: NewsNow focuses on CN sources; use `parallel-web-search` for Reuters/Bloomberg/CNBC/KR finance.
