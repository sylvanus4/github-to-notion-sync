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

All download commands below are run from the **`backend/`** directory (the script lives at `backend/scripts/download_stock_csv.py`).

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

## Phased workflow (dependency order)

Execute phases in order. Do not skip a phase whose output later steps depend on.

| Phase | Action | Depends on | Output / gate |
|-------|--------|------------|---------------|
| **1** | Satisfy [Prerequisites](#prerequisites) | — | Playwright + DB ready |
| **2** | `python scripts/download_stock_csv.py --status` (optional but recommended before bulk/gap-fill) | Phase 1 | Coverage report in stdout |
| **3** | Download: choose **one** mode — `--gap-fill`, `--ticker …`, or `--all` (see [CLI](#cli-arguments)) | Phase 1 | CSV files on disk |
| **4** | Import: `--import` on the same command **or** manual import after Phase 3: from `backend/`, `python scripts/import_csv.py ../data/latest --directory`; from repo root, `python backend/scripts/import_csv.py data/latest --directory` | Phase 3 completed | Rows upserted in PostgreSQL |
| **5** | Verify via HTTP API (see [Phase 5](#phase-5-verify-imported-data)) | Phase 4 completed | Confirms rows visible |
| **6** | Re-run `--status` (optional) | Phase 5 | Confirms coverage / gaps closed |

**Branching:** For gap-fill, Phase 3 uses `--gap-fill` (and optional `--ticker`). For a fresh range download, Phase 3 uses `--ticker` with `--start-date` / `--end-date` (or script defaults). Phase 4 must not start until Phase 3 finishes without aborting the script.

### Phase 5: Verify imported data

```bash
# From project root or wherever the API is reachable (default dev port shown)
curl http://localhost:4567/api/v1/stock-prices/tickers
curl http://localhost:4567/api/v1/stock-prices/NVDA?limit=5
```

## Error recovery and halt behavior

| Step / call | On failure | Recovery / fallback |
|-------------|------------|---------------------|
| Playwright browser launch | Script exits with error | **Halt.** Run `playwright install chromium`; confirm Python env matches `backend`. |
| `page.goto` / instrument_id missing | Ticker skipped or script errors | **Halt** for that ticker. Use `--no-headless` to inspect; see [instrument_id not found](#instrument_id-not-found). |
| investing.com API `fetch` (non-OK or JSON error) | Download for that range/ticker fails | **Halt** for that batch. Increase `--delay`; retry smaller `--ticker` set; use `--no-headless` if CAPTCHA suspected. |
| CSV write to disk | Script exits if path invalid | **Halt.** Fix `--output-dir` or permissions; re-run Phase 3. |
| `--import` / DB upsert | Import errors printed; pipeline stops for that file | **Halt.** Fix `DATABASE_URL`, migrations, connectivity; re-run **only** import on existing CSVs (from `backend/`: `python scripts/import_csv.py ../data/latest --directory`, or the directory printed as `Output dir`). |
| Rate limiting / CAPTCHA | Blocks or empty responses | **Fallback:** `--no-headless` + manual solve; increase `--delay`; reduce batch size (fewer tickers per run). |

Do not assume silent skip: if the script prints a failure for a ticker, treat Phase 3 as incomplete for that ticker until re-run succeeds.

## Output files and CSV format

- **Directory:** Default `data/latest/` at the **project root** (override with `--output-dir`, path relative to project root). The script prints `Output dir: …` at startup.
- **Filenames:** One file per ticker: `{csv_name}.csv` where `csv_name` comes from the internal ticker map (see [references/ticker-mapping.md](references/ticker-mapping.md)), not always identical to the ticker symbol.
- **Encoding:** UTF-8 with BOM (`utf-8-sig`).
- **Columns (header row):** `Date`, `Price`, `Open`, `High`, `Low`, `Vol.`, `Change %` — investing.com-style daily rows. `import_csv.py` / `CSVParserService` map these into `StockPrice` columns.

**Verification:** After import, use Phase 5 curls or re-run `--status` to compare date ranges and counts.

## CLI Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--ticker` | One or more ticker symbols | — (required in ticker mode) | `--ticker NVDA AAPL` |
| `--all` | Download all configured tickers | off | `--all` |
| `--list` | List available tickers | off | `--list` |
| `--status` | Show DB coverage for all tickers (optional `--ticker` scopes the list) | off | `--status` |
| `--gap-fill` | Detect and download only missing DB dates | off | `--gap-fill --import` |
| `--gap-fill-from` | Start date for gap analysis | `2021-01-01` | `--gap-fill-from 2023-01-01` |
| `--output-dir` | Output directory relative to **project root** | `data/latest` | `--output-dir data/3` |
| `--start-date` | Start date `YYYY-MM-DD` for historical download | 1 year before run date | `--start-date 2024-01-01` |
| `--end-date` | End date `YYYY-MM-DD` for historical download | today | `--end-date 2026-02-22` |
| `--import` | Run automatic import after download | off | `--import` |
| `--no-headless` | Visible browser (debug / CAPTCHA) | headless on | `--no-headless` |
| `--delay` | Seconds between ticker downloads | `3` | `--delay 5` |

The database uses upsert (`ON CONFLICT DO UPDATE`); re-downloading overlapping ranges is safe.

**Flag coverage in examples:** `--status`, `--gap-fill`, `--gap-fill-from`, `--ticker`, `--import`, `--list`, `--all`, `--delay`, `--start-date`, `--end-date`, `--output-dir`, and `--no-headless` are all used in at least one example below or in [Troubleshooting](#troubleshooting).

## Natural language → command mapping

| User intent (examples) | Suggested command sequence |
|------------------------|----------------------------|
| "NVDA 주식 데이터 다운로드해줘" | `cd backend` → `python scripts/download_stock_csv.py --ticker NVDA --import` (add `--start-date` / `--end-date` if user specifies a range). |
| "모든 종목 갭 채워줘" | `python scripts/download_stock_csv.py --status` → `python scripts/download_stock_csv.py --gap-fill --import` → optional `--status`. |
| "stock-csv-downloader --status" | `python scripts/download_stock_csv.py --status` |
| "investing.com에서 데이터 받아서 DB에 넣어줘" | Phases 2–5: download with `--import` or download then `import_csv.py` on `../data/latest`; verify with API. |
| "2024년 1월부터 AAPL 데이터 다운로드" | `python scripts/download_stock_csv.py --ticker AAPL --start-date 2024-01-01 --import` |

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
4. Verify: `curl http://localhost:4567/api/v1/stock-prices/tickers`

Result: CSV files in `data/latest/`, data in PostgreSQL.

### Example 3: Date range download (single ticker)

User says: "Download AAPL from 2024-01-01 through end of 2025"

Actions:
1. `cd backend`
2. `python scripts/download_stock_csv.py --ticker AAPL --start-date 2024-01-01 --end-date 2025-12-31 --import`
3. Optional: add `--output-dir data/aapl-run` to isolate files; verify with `curl …/stock-prices/AAPL?limit=5`

Uses: `--ticker`, `--start-date`, `--end-date`, `--import`, `--output-dir` (optional).

### Example 4: Full pipeline end-to-end (single ticker)

User says: "Get NVDA history into the DB and prove it worked"

Actions (from `backend/`):
1. `python scripts/download_stock_csv.py --status` — baseline coverage
2. `python scripts/download_stock_csv.py --ticker NVDA --import` — download + import (add `--start-date` / `--end-date` if needed)
3. `curl http://localhost:4567/api/v1/stock-prices/NVDA?limit=5` — verify latest rows
4. `python scripts/download_stock_csv.py --status` — optional confirmation

**Debugging path:** If step 2 fails with anti-bot, re-run with `python scripts/download_stock_csv.py --ticker NVDA --import --no-headless --delay 10`.

This example runs Phase 2 → Phase 3 → Phase 4 → Phase 5 → optional Phase 6.

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
