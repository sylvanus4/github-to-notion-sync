---
description: "Daily stock price sync from Yahoo Finance to PostgreSQL for all tracked tickers via weekly_stock_update.py script. Use when syncing prices, '주식 데이터 동기화', 'tab-stock-sync'. Do NOT use for stock analysis (use daily-stock-check), CSV downloads (use stock-csv-downloader), or fundamental data (use tab-fundamental-sync)."
---

# tab-stock-sync

## Purpose

Syncs stock price data from Yahoo Finance into PostgreSQL for all tracked tickers using the `weekly_stock_update.py` script. Fetches the last 7 days of OHLCV data and upserts into the database.

## When to Use

- sync stock prices
- 주식 데이터 동기화
- tab-stock-sync
- fetch latest prices

## When NOT to Use

- Stock analysis (use daily-stock-check)
- CSV downloads (use stock-csv-downloader)
- Fundamental data (use tab-fundamental-sync)

## Workflow

1. Ensure backend server is running on port 4567
2. Run `python scripts/weekly_stock_update.py --days 7` to fetch and upsert OHLCV data for all tracked tickers
3. Verify sync with `python scripts/weekly_stock_update.py --status`

## API Endpoints Used

- `POST /api/v1/stock-prices/fetch-latest` — fetches latest OHLCV data for a ticker and upserts into the database

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Updated stock_prices table with latest 7-day OHLCV data for all tracked tickers.
