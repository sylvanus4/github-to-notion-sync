---
name: alphaear-news
description: >-
  Fetch real-time financial news from 10+ sources (Weibo, Zhihu, WallstreetCN,
  Hacker News, etc.) and Polymarket prediction market data. Use when the user
  needs hot finance news, unified trend reports from multiple sources, or
  Polymarket finance prediction data. Do NOT use for stock price data (use
  weekly-stock-update or alphaear-stock). Do NOT use for sentiment scoring
  (use alphaear-sentiment). Do NOT use for finance-specific web search queries
  (use alphaear-search). Korean triggers: "핫뉴스", "뉴스 수집", "폴리마켓", "뉴스 트렌드".
---

# AlphaEar News

## Overview

Fetch real-time hot financial news from 10+ sources (CN, US, KR-relevant), generate unified trend reports, and retrieve Polymarket prediction market data. News is stored in SQLite (`data/signal_flux.db`) via `scripts/database_manager.py`.

## Prerequisites

- Python 3.10+
- `requests`, `loguru`
- `scripts/database_manager.py` (SQLite — `data/signal_flux.db`)
- Network access to NewsNow API and Polymarket gamma-api

## Workflow

1. **Initialize**: Create `DatabaseManager` (auto-creates SQLite DB at `data/signal_flux.db`), then instantiate `NewsNowTools(db)` or `PolymarketTools(db)`.
2. **Fetch hot news**: Call `NewsNowTools.fetch_hot_news(source_id, count)` — see `references/sources.md` for valid `source_id` values.
3. **Unified trends**: Call `NewsNowTools.get_unified_trends(sources)` to aggregate top news from multiple sources.
4. **Polymarket data**: Call `PolymarketTools.get_market_summary(limit)` for prediction market summaries.
5. **US/KR fallback**: If Reuters, Bloomberg, or CNBC content is needed and not available via NewsNow, use the `parallel-web-search` skill to supplement with web search results.
6. **Storage**: Fetched news is saved to the SQLite `daily_news` table by the tools.

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
| DB connection failure | Exception raised | Verify `data/signal_flux.db` is writable and not locked |
| Invalid `source_id` | Empty items | Check `references/sources.md` for valid IDs |

## Troubleshooting

- **Empty results**: Verify `source_id` spelling; some sources may be rate-limited.
- **Stale data**: Built-in 5-minute cache; force fresh fetch by waiting or clearing cache.
- **Missing US/KR sources**: NewsNow focuses on CN sources; use `parallel-web-search` for Reuters/Bloomberg/CNBC/KR finance.

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing

| User query pattern | This skill vs other |
|--------------------|---------------------|
| Hot headlines / multi-source trends / Polymarket | **This skill** (`alphaear-news`) |
| Raw OHLCV / ticker history | `alphaear-stock` or `weekly-stock-update` — **not** this skill |
| Sentiment score only | `alphaear-sentiment` — **not** this skill |
| Broad macro synthesis | `alphaear-deepear-lite` orchestration |

### Data source attribution (required)

Every headline, market line, or Polymarket stat must cite origin: `(출처: NewsNow → daily_news DB, source_id=…)`, `(출처: Polymarket gamma-api)`, or `(출처: parallel-web-search 보충 — Reuters/CNBC 등)`. Include `source_id` or URL when available.

### Korean output

Summaries for Korean users: natural Korean; name sources in-line (위챗/웨이보/폴리마켓 등 적절히 병기).

### Fallback protocol

On NewsNow timeout/empty: state `NewsNow 1차 수집 실패 → 캐시/재시도 또는 parallel-web-search로 보충` before presenting partial results. On Polymarket failure: say `Polymarket API 사용 불가 — 예측시장 섹션 생략` explicitly.
