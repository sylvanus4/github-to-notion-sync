---
description: "Search A-Share/HK/US stock tickers and retrieve OHLCV price history"
---

# AlphaEar Stock

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-stock/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a ticker code or company name, use `search_ticker` first, then `get_stock_price`
- If `$ARGUMENTS` contains date range (e.g., "2025-01-01 to 2025-06-30"), pass as `start_date`/`end_date`
- If `$ARGUMENTS` mentions "search" only, run `search_ticker` and return matches
- If `$ARGUMENTS` is empty, ask user for a ticker or company name

### Step 2: Execute

Follow the workflow in the skill:

1. Initialize `DatabaseManager` and `StockTools`
2. Search ticker if name/code provided
3. Fetch OHLCV data for the resolved ticker

### Step 3: Report

Present results with:
- Ticker code and full name
- OHLCV data table (last N days or requested range)
- Latest price and change percentage
