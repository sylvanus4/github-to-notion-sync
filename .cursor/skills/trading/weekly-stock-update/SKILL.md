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
python scripts/weekly_stock_update.py --delay 2          # Slower pacing (rate-limit safety)
```

## Workflow

### Execution order and dependencies

Follow this order so downstream steps never assume data that was not produced yet:

| Mode | Phases (in order) | Notes |
|------|-------------------|--------|
| `--status` | Coverage query only | Exits immediately; no Yahoo calls for prices in the update path |
| Default (no flags) | Price sync only | Sequential per ticker; safe to re-run (upsert) |
| `--fundamentals` | (1) Price sync → (2) Fundamentals sync | Fundamentals always run **after** all price work finishes in the same invocation |

Do not skip the price-sync phase when using `--fundamentals` unless the user explicitly requests fundamentals-only (not supported by this script — run a full update with `--fundamentals`).

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
3. Calls `yfinance` for each ticker with a 10-day lookback window (or `--days` N)
4. Batch upserts into PostgreSQL using `INSERT ... ON CONFLICT DO UPDATE` on the `uq_ticker_date` constraint
5. Prints the **Price Sync** summary report
6. If `--fundamentals`: after step 5, fetches quarterly financials per ticker and upserts via `financial_data_collector` (see **Execution order** above)

Re-running is always safe — the upsert prevents duplicates and updates existing records.

## Output Format

Console output is structured so you can scan **header → per-ticker detail → summary** quickly. When reporting back to the user, mirror that structure in your reply.

### Price update run

| Section | What appears |
|---------|----------------|
| **Header** | `[UPDATE]` or `[DRY RUN]` line with ticker count and date range |
| **Detail** | One block per ticker: `[i/N] SYMBOL (Name)...` then `→ status: message` |
| **Summary** | `Price Sync:` block with success / no-data counts and total records upserted |

Example:

```
HH:MM:SS [INFO] [UPDATE] 21 tickers, 2026-02-13 ~ 2026-02-23
HH:MM:SS [INFO] [1/21] NVDA (NVIDIA)...
HH:MM:SS [INFO]   → success: Upserted 7 records (2026-02-14 ~ 2026-02-21)
...
==================================================
Price Sync: 21 tickers processed
  Success: 21 | No data: 0
  Total records upserted: 147
==================================================
```

With `--fundamentals`, a second **header** line `[FUNDAMENTALS]` appears, then per-ticker financial lines, then a **`Fundamentals:`** summary block (success / no data / errors).

### `--status` output

| Section | What appears |
|---------|----------------|
| **Header** | Column titles row |
| **Detail** | One row per symbol: counts and first/last dates (or `—` if missing) |

Example:

```
Symbol     Name                      Records        First         Last
----------------------------------------------------------------------
NVDA       NVIDIA                       1250   2021-01-04   2026-02-21
...
```

### Disclaimer (when sharing results)

Yahoo Finance / yfinance data can be delayed, adjusted, or incomplete. Output is for **operational data sync only** — not investment advice or a real-time quote guarantee.

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

### Example 3: Full run — prices, optional preview, fundamentals, verification

User says: "Sync latest prices and fundamentals for everything, but show me a preview first"

This walks **every** phase the script supports: status → dry-run → live update with fundamentals → status.

Actions (from `backend/`):

1. `python scripts/weekly_stock_update.py --status` — baseline coverage
2. `python scripts/weekly_stock_update.py --dry-run --fundamentals` — preview price + fundamentals **without** DB writes (both phases still execute in dry-run mode)
3. `python scripts/weekly_stock_update.py --fundamentals` — **Phase A** price upsert for all tickers, then **Phase B** quarterly financials upsert
4. `python scripts/weekly_stock_update.py --status` — confirm `Last` dates and coverage advanced

Result: Full pipeline executed; user saw a safe preview before writes, then live sync of prices and financial statements, then verification.

## Failure behavior (scripts and external calls)

When running `weekly_stock_update.py`, use this map so failures are handled predictably:

| Situation | Behavior | Agent follow-up |
|-----------|----------|-------------------|
| Unknown `--ticker` value | Process **exits** with code `1`; stderr lists unknown symbols and available tickers | Fix symbols against `TICKER_SLUG_MAP`; do not retry with the same args |
| Yahoo / yfinance empty or bad data for one ticker | That ticker gets `no_data` status; loop **continues** for remaining tickers | Log and optionally retry later or use `stock-csv-downloader` for that symbol (see Troubleshooting) |
| DB connection or commit failure | Exception propagates; process **fails** (non-zero exit) | Check PostgreSQL, migrations, and `DATABASE_URL`; fix infra before re-running |
| `--dry-run` | No DB writes; prints what **would** be upserted | Use before production writes when the user asks for a preview |
| `--fundamentals` + per-ticker financials error | Exception caught per ticker; that ticker counted as error; loop **continues** | Inspect log line `→ Error:`; re-run for failed symbols only if needed |

If the user only asked for `--status` and the DB is unreachable, the command fails fast — treat as environment issue, not a skill logic skip.

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
