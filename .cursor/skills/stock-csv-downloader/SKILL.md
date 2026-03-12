---
name: stock-csv-downloader
description: >-
  Download historical stock price CSVs from investing.com and import into the
  database. Use when the user asks to download stock data, fetch stock CSVs,
  update stock prices from investing.com, or refresh historical price data. Do
  NOT use for quick weekly price updates from Yahoo Finance (use
  weekly-stock-update). Do NOT use for stock analysis, trading signals, or Slack
  posting (use daily-stock-check). Korean triggers: "주식", "체크", "데이터", "데이터베이스".
metadata:
  version: "1.0"
  category: "generation"
  author: "thaki"
---
# Stock CSV Downloader

Download per-ticker historical CSVs from investing.com via Playwright and import them into PostgreSQL using the existing CSV import pipeline.

## Prerequisites

- Python Playwright installed: `pip install playwright && playwright install chromium`
- Backend dependencies installed
- Database running and migrated (`alembic upgrade head`)

## Quick Start

```bash
cd backend
python scripts/download_stock_csv.py --ticker NVDA --import   # Single ticker
python scripts/download_stock_csv.py --gap-fill --import       # Fill all gaps
python scripts/download_stock_csv.py --list                    # List tickers
python scripts/download_stock_csv.py --status                  # DB coverage
```

## How It Works

The script uses Playwright to open investing.com in a headless browser, extracts the `instrument_id` from the page's `__NEXT_DATA__`, then calls the `api.investing.com` historical data API directly from the browser context. The JSON response is converted to the standard investing.com CSV format.

## Workflow

### Step 1: Check Coverage

See what data is already in the database and which tickers have gaps:

```bash
python scripts/download_stock_csv.py --status
```

Output shows first/last date, record count, missing weekdays, and coverage percentage for each ticker since 2021-01-01.

### Step 2–4: Download and Import

**Gap-fill (recommended):** `--gap-fill --import` fills missing dates. **Full download:** `--ticker X Y --start-date --end-date` or `--all`. Add `--import` for auto-import. Manual: `python scripts/import_csv.py data/latest --directory`. Files → `data/latest/`.

### Step 5: Verify

```bash
# Check imported data via API
curl http://localhost:4567/api/v1/stock-prices/tickers
curl http://localhost:4567/api/v1/stock-prices/NVDA?limit=5
```

## CLI Arguments

| Argument | Description | Example |
|---|---|---|
| `--ticker` | One or more ticker symbols | `--ticker NVDA AAPL` |
| `--all` | Download all configured tickers | `--all` |
| `--list` | List available tickers | `--list` |
| `--status` | Show DB coverage for all tickers | `--status` |
| `--gap-fill` | Detect and fill missing dates in DB | `--gap-fill --import` |
| `--gap-fill-from` | Start date for gap analysis (default: 2021-01-01) | `--gap-fill-from 2023-01-01` |
| `--output-dir` | Output directory (relative to project root) | `--output-dir data/3` |
| `--start-date` | Start date (YYYY-MM-DD) | `--start-date 2025-01-01` |
| `--end-date` | End date (YYYY-MM-DD) | `--end-date 2026-02-22` |
| `--import` | Auto-import CSVs to database after download | `--import` |
| `--no-headless` | Show browser window (debugging) | `--no-headless` |
| `--delay` | Seconds between downloads (default: 3) | `--delay 5` |

The database uses upsert (`ON CONFLICT DO UPDATE`); re-downloading overlapping ranges is safe.

## Ticker Mapping

21 tickers pre-configured (18 international, 3 KRX). Abridged mapping: [references/ticker-mapping.md](references/ticker-mapping.md). Full slugs: [references/reference.md](references/reference.md)

## Examples

### Example 1: Gap-fill missing data

User says: "Fill gaps in our NVDA and AAPL stock data since 2023"

Actions:
1. Run `python scripts/download_stock_csv.py --status` to verify current coverage
2. Run `python scripts/download_stock_csv.py --gap-fill --ticker NVDA AAPL --gap-fill-from 2023-01-01 --import`
3. Re-run `--status` to confirm coverage

Result: Missing dates downloaded and imported; no duplicates (upsert).

### Example 2: First-time bulk download

User says: "Download all stock data from investing.com and import to DB"

Actions:
1. Run `python scripts/download_stock_csv.py --list` to confirm tickers
2. Run `python scripts/download_stock_csv.py --gap-fill --import` (or `--all --import` for full overwrite)
3. Use `--delay 5` for large batches to avoid rate limits

Result: CSV files in `data/latest/`, data in PostgreSQL.

## Troubleshooting

### Anti-bot / CAPTCHA blocks

Cause: investing.com detects automated requests.

Solution: Use `--no-headless` to debug and solve CAPTCHAs manually; increase `--delay` (e.g., 10); download in smaller batches instead of `--all`.

### instrument_id not found

Cause: Page structure changed; `__NEXT_DATA__` no longer contains instrument ID.

Solution: Use `--no-headless` to inspect DOM. Check network requests to `api.investing.com` for the ID.

## Integration

- **Download script**: `backend/scripts/download_stock_csv.py`
- **Import script**: `backend/scripts/import_csv.py` (existing)
- **CSV parser**: `backend/app/services/csv_parser_service.py` (existing)
- **DB models**: `backend/app/models/stock_price.py` — `Ticker`, `StockPrice`
