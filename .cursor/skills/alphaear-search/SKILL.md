---
name: alphaear-search
description: >-
  Perform finance-specific web searches (Jina/DDG/Baidu) and local RAG search.
  Use when the user needs finance info from the web, local document store
  (daily_news DB), or multi-engine aggregation. Do NOT use for general web
  research (use parallel-web-search). Do NOT use for stock price data (use
  alphaear-stock or weekly-stock-update). Do NOT use for news aggregation (use
  alphaear-news). Korean triggers: "검색", "주식", "뉴스", "문서".
metadata:
  version: "1.0.0"
  category: "data-collection"
  author: "alphaear"
---
# AlphaEar Search

## Overview

Finance-specific web and local search. Supports Jina, DuckDuckGo, and Baidu engines plus local RAG over the `daily_news` database. Use as a complement to general parallel-web-search when the context is finance.

## Prerequisites

- Python 3.10+
- `duckduckgo-search`, `requests`
- `scripts/database_manager.py` (search cache & local news)
- Optional: `JINA_API_KEY` for Jina Search engine

## Workflow

1. **Check cache**: Use the **Search Cache Relevance Prompt** in `references/PROMPTS.md` to decide if prior search results are still relevant.
2. **Web search**: Call `SearchTools.search(query, engine, max_results)` or `SearchTools.search_list(...)` for List[Dict].
3. **Multi-engine**: Call `SearchTools.aggregate_search(query)` to combine results from multiple engines.
4. **Local RAG**: Use `engine='local'` or `scripts/hybrid_search.py` to search the local `daily_news` database.

## Examples

| Trigger | Action | Result |
|---------|--------|--------|
| "Search for 英伟达财报" | `search(query, engine="jina"\|"ddg"\|"baidu")` | JSON summary or List[Dict] |
| "Aggregate finance views on X" | `aggregate_search(query)` | Combined results from multiple engines |
| "Search local news for policy" | `search(query, engine="local")` | RAG results from daily_news DB |
| "Is cached result still valid?" | Search Cache Relevance prompt | `{reuse: bool, index, reason}` |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Jina 429 rate limit | Wait 30s, retry | Reduce request frequency or configure JINA_API_KEY |
| Network timeout | Empty or partial results | Retry with fallback engine (ddg/baidu) |
| Local DB empty | No RAG results | Ensure daily_news populated; use web search instead |
| Cache expired | Fresh search performed | Adjust `SEARCH_CACHE_TTL` if needed |

## Troubleshooting

- **Jina vs DDG**: Jina returns LLM-friendly output; use DDG for English/international queries.
- **General research**: For non-finance queries, delegate to parallel-web-search.
- **Local search**: `scripts/hybrid_search.py` uses vector + BM25 over `daily_news`.

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing

| User query pattern | This skill vs other |
|--------------------|---------------------|
| Finance web + `daily_news` RAG | **This skill** |
| General non-finance research | `parallel-web-search` |
| OHLCV / tickers | `alphaear-stock` / `weekly-stock-update` |
| Curated hot news lists | `alphaear-news` |

### Data source attribution (required)

Tag each result batch: `(출처: Jina Search)`, `(출처: DuckDuckGo)`, `(출처: Baidu)`, `(출처: PostgreSQL daily_news 로컬 RAG)`, `(출처: 검색 캐시)`. Multi-engine: list each engine’s contribution.

### Korean output

Korean queries → Korean synthesis; keep proper nouns and tickers in standard form.

### Fallback protocol

Jina 429/timeout → `Jina 제한 — DDG/Baidu로 재검색`. Local DB empty → `daily_news RAG 결과 없음 — 웹 엔진으로 대체`. Say so explicitly in the user-facing reply.
