---
name: tab-hot-stock-discovery
description: >-
  Discover hottest untracked stocks from NASDAQ/KOSPI/KOSDAQ 100 via POST
  /admin/discover-hot-stocks. Use when discovering hot stocks, '핫 종목 발견',
  'tab-hot-stock-discovery'. Do NOT use for stock screening (use
  tab-screening) or stock price sync (use tab-stock-sync).
---

# tab-hot-stock-discovery

## Purpose

Discovers the hottest untracked stocks from NASDAQ 100, KOSPI 100, and KOSDAQ 100 by calling `POST /admin/discover-hot-stocks`. Results are saved as JSON in the outputs/ directory.

## When to Use

- discover hot stocks
- 핫 종목 발견
- tab-hot-stock-discovery
- find new stocks

## When NOT to Use

- Stock screening (use tab-screening)
- Stock price sync (use tab-stock-sync)

## Workflow

1. Ensure backend server is running on port 4567
2. Call `POST /api/v1/admin/discover-hot-stocks` with query parameters: `indices` (default: nasdaq, kospi, kosdaq), `top` (default: 1), `days` (default: 1)
3. Endpoint fetches constituents, filters out tracked tickers, and ranks by turnover
4. Results are saved as JSON in outputs/ directory

## API Endpoints Used

- `POST /api/v1/admin/discover-hot-stocks` — discovers hottest untracked stocks from configured indices (NASDAQ/KOSPI/KOSDAQ 100)

## Dependencies

- Requires backend server running on port 4567
- Requires access to index constituent data

## Output

JSON file in outputs/ directory containing discovered hot stocks with configurable top_n and lookback days.
