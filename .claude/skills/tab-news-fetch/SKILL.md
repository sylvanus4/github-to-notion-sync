---
name: tab-news-fetch
description: >-
  Fetch news from all sources via POST /news/fetch, query latest with GET
  /news/latest, and get aggregated summary via GET /news/summary. Use when
  fetching news, '뉴스 수집', 'tab-news-fetch', 'news fetch'. Do NOT use for
  AlphaEar news aggregation (use alphaear-news), sentiment scoring (use
  alphaear-sentiment), or stock price sync (use tab-stock-sync).
---

# tab-news-fetch

## Purpose

Trigger news collection from all configured sources and query aggregated news data with sentiment distribution.

## When to Use

- fetch news
- 뉴스 수집
- tab-news-fetch
- news summary
- collect latest news

## When NOT to Use

- AlphaEar multi-source news aggregation — use alphaear-news
- Sentiment analysis on text — use alphaear-sentiment
- Stock price sync — use tab-stock-sync

## Workflow

1. Call `POST /api/v1/news/fetch` to trigger news collection from all sources
2. Optionally include `symbols` in request body to also fetch ticker-specific news from Yahoo Finance
3. Query latest with `GET /api/v1/news/latest` (params: limit, source_type, language, sentiment_label, ticker)
4. Get aggregated overview with `GET /api/v1/news/summary` (param: days)
5. Analyze news for a specific topic with `POST /api/v1/news/analyze?topic=...`

## Endpoints Used

- `POST /api/v1/news/fetch` — trigger batch news collection (body: optional sources list, symbols list)
- `GET /api/v1/news/latest` — latest articles with filters
- `GET /api/v1/news/search?q=...` — full-text search across articles
- `GET /api/v1/news/summary` — aggregate stats: count by source, sentiment distribution (param: days)
- `POST /api/v1/news/analyze?topic=...` — fetch + analyze news for a topic in one call
- `GET /api/v1/news/sources` — per-source stats

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL

## Output

News articles fetched, stored, and queryable with sentiment analysis.
