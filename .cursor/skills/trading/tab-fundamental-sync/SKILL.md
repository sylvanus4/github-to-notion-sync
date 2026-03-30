---
description: "Sync quarterly financial statements from Yahoo Finance via POST /financial-statements/sync. Use when syncing fundamentals, '재무제표 동기화', 'tab-fundamental-sync'. Do NOT use for stock price sync (use tab-stock-sync) or manual financial analysis."
---

# tab-fundamental-sync

## Purpose

This skill syncs quarterly financial statements (income statement, balance sheet, cash flow) from Yahoo Finance. It calls `POST /financial-statements/sync` for all tracked tickers.

## When to Use

- sync fundamentals
- 재무제표 동기화
- tab-fundamental-sync
- financial statements sync

## When NOT to Use

- stock price sync (use tab-stock-sync)
- manual financial analysis

## Workflow

1. Ensure backend server is running on port 4567
2. Call `POST /api/v1/financial-statements/sync` for all tracked tickers
3. Endpoint fetches quarterly income statement, balance sheet, and cash flow from Yahoo Finance and persists to database

## API Endpoints Used

- `POST /api/v1/financial-statements/sync` — syncs quarterly financial statements for all tickers

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with financial statements schema

## Output

Updated financial_statements (or equivalent) table with quarterly income statement, balance sheet, and cash flow data for all tracked tickers.
