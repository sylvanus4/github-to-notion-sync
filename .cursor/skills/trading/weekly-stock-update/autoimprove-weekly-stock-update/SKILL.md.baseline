---
name: weekly-stock-update
description: >-
  Fetch the last week of stock prices from Yahoo Finance and upsert into
  PostgreSQL for all tracked tickers. Optionally sync quarterly financial
  statements (--fundamentals). Use when the user asks to update recent stock
  data, refresh weekly prices, sync latest prices to DB, sync financial
  statements, or run a quick stock update. Do NOT use for historical backfill or
  gap-fill from investing.com (use stock-csv-downloader). Do NOT use for stock
  analysis, trading signals, or Slack posting (use daily-stock-check). Korean
  triggers: "주식", "테스트", "체크", "동기화".
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Weekly Stock Update

Fetch recent stock prices from Yahoo Finance (yfinance) and batch upsert them into PostgreSQL. Covers all configured tickers with a single lightweight script — no browser automation required. With `--fundamentals`, also syncs quarterly financial statements (income, balance sheet, cash flow) and computed metrics (P/E, ROE, FCF yield, etc.).

## Prerequisites

- Python dependencies installed (`yfinance`, `sqlalchemy`, `asyncpg`)
- PostgreSQL running and migrated (`alembic upgrade head`)

## Quick Start

```bash
cd backend
python scripts/weekly_stock_update.py                    # All tickers, last 10 days
python scripts/weekly_stock_update.py --fundamentals     # Prices + financial statements
python scripts/weekly_stock_update.py --status           # Show DB coverage
python scripts/weekly_stock_update.py --dry-run          # Preview without DB write
```

## Workflow

### Step 1: Check Current Coverage

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

Shows record count, first date, and last date for each of the 21 tickers.

### Step 2: Run Update

```bash
cd backend
python scripts/weekly_stock_update.py
```

For specific tickers only:

```bash
python scripts/weekly_stock_update.py --ticker NVDA AAPL 005930
```

For a custom lookback window (e.g., 2 weeks):

```bash
python scripts/weekly_stock_update.py --days 14
```

### Step 3: Verify Results

Re-run `--status` to confirm the last date has advanced:

```bash
python scripts/weekly_stock_update.py --status
```

Or query via API (if the server is running):

```bash
curl http://localhost:4567/api/v1/stock-prices/NVDA?limit=5
```

## CLI Arguments

| Argument | Description | Default |
|---|---|---|
| `--ticker` | One or more ticker symbols | All 21 tickers |
| `--days` | Lookback window in days | 10 |
| `--dry-run` | Preview without writing to DB | Off |
| `--status` | Show DB coverage and exit | Off |
| `--delay` | Seconds between API calls | 0.5 |
| `--fundamentals` | Also sync quarterly financial statements | Off |

## How It Works

1. Reads the ticker list from `TICKER_SLUG_MAP` in `download_stock_csv.py`
2. Converts KRX tickers to yfinance format (e.g., `005930` to `005930.KS`)
3. Calls `yfinance` for each ticker with a 10-day lookback window
4. Batch upserts into PostgreSQL using `INSERT ... ON CONFLICT DO UPDATE` on the `uq_ticker_date` constraint
5. Prints a summary report

Re-running is always safe — the upsert prevents duplicates and updates existing records.

## Output Format

The script prints a per-ticker progress log and a final summary:

```
HH:MM:SS [INFO] [UPDATE] 21 tickers, 2026-02-13 ~ 2026-02-23
HH:MM:SS [INFO] [1/21] NVDA (NVIDIA)...
HH:MM:SS [INFO]   → success: Upserted 7 records (2026-02-14 ~ 2026-02-21)
...
==================================================
Summary: 21 tickers processed
  Success: 21 | No data: 0
  Total records upserted: 147
==================================================
```

The `--status` flag outputs a coverage table:

```
Symbol     Name                      Records        First         Last
----------------------------------------------------------------------
NVDA       NVIDIA                       1250   2021-01-04   2026-02-21
...
```

## Examples

### Example 1: Weekly refresh of all tickers

User says: "Update stock prices for the last week"

Actions:
1. Run `python scripts/weekly_stock_update.py --status` to check current coverage
2. Run `python scripts/weekly_stock_update.py` to fetch and upsert last 10 days
3. Run `python scripts/weekly_stock_update.py --status` to confirm dates advanced

Result: All 21 tickers updated with the latest trading data.

### Example 2: Update specific tickers after a long weekend

User says: "Refresh NVDA and Samsung data for the past 2 weeks"

Actions:
1. Run `python scripts/weekly_stock_update.py --ticker NVDA 005930 --days 14`
2. Run `python scripts/weekly_stock_update.py --status --ticker NVDA 005930` to verify

Result: NVDA and Samsung Electronics updated with 14 days of price data.

## Troubleshooting

### No data returned for a KRX ticker

Cause: yfinance uses `.KS` suffix for KRX tickers. The script handles this automatically, but the ticker may be delisted or the market may be closed.

Solution: Verify the ticker exists on Yahoo Finance (e.g., search `005930.KS` on finance.yahoo.com). If the issue persists, fall back to `stock-csv-downloader` for that ticker.

### yfinance rate limiting

Cause: Too many rapid requests to Yahoo Finance.

Solution: Increase the delay between calls: `--delay 2`. For very large batches, consider splitting into groups.

## Integration

- **Script**: `backend/scripts/weekly_stock_update.py`
- **Ticker source**: `backend/scripts/download_stock_csv.py` (`TICKER_SLUG_MAP`)
- **Yahoo client**: `backend/app/services/external_stock_api.py` (`YahooFinanceClient`)
- **Financials collector**: `backend/scripts/financial_data_collector.py` (used by `--fundamentals`)
- **DB models**: `backend/app/models/stock_price.py` (`Ticker`, `StockPrice`), `backend/app/models/llm_agents/models.py` (`FinancialStatement`)
- **API endpoints**: `GET /api/v1/financial-statements/{symbol}` — view synced financial data in the UI
- **Related skill**: `stock-csv-downloader` (for historical backfill via investing.com)
