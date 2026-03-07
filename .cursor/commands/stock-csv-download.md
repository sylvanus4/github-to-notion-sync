---
description: "Download stock price CSVs from investing.com and import into database"
---

# Stock CSV Download

## Skill Reference

Read and follow the skill at `.cursor/skills/stock-csv-downloader/SKILL.md`.
For detailed ticker mappings and CSV format, see `.cursor/skills/stock-csv-downloader/reference.md`.

## Your Task

The user input can be provided directly or as a command argument — consider it before proceeding.

User input:

$ARGUMENTS

### Step 1: Parse Request

Determine the **mode** from user input:

- **Gap-fill / backfill / missing**: keywords like "gap", "fill", "missing", "backfill", "update" → use `--gap-fill` mode
- **Status / coverage / check**: keywords like "status", "coverage", "check" → use `--status` mode
- **Specific tickers with date range**: → use `--ticker` mode
- **All tickers**: → use `--all` mode
- **No arguments at all**: → run `--status` first, then ask user whether to gap-fill or do a full download

Also determine:
- **Target tickers**: specific symbols (e.g., NVDA, AAPL) or "all"
- **Date range**: start and end dates, if specified (for standard mode)
- **Gap-fill-from**: custom start date for gap analysis (default: 2021-01-01)
- **Import**: whether to auto-import into the database (default: yes)
- **Output directory**: where to save CSVs (default: `data/latest`)

### Step 2: Verify Prerequisites

```bash
# Check Python Playwright is installed
python -c "from playwright.async_api import async_playwright; print('OK')"
```

If not installed:

```bash
pip install playwright
playwright install chromium
```

### Step 3: Check Coverage (for gap-fill or when no arguments)

Run status check to show the user what data exists and what's missing:

```bash
cd backend
python scripts/download_stock_csv.py --status
```

For specific tickers only:

```bash
cd backend
python scripts/download_stock_csv.py --status --ticker NVDA AAPL
```

### Step 4: Run Download

**Gap-fill mode** (only downloads missing data):

```bash
cd backend
# Fill all tickers
python scripts/download_stock_csv.py --gap-fill --import --delay 3

# Fill specific tickers
python scripts/download_stock_csv.py --gap-fill --ticker NVDA AAPL --import

# Fill from a custom start date
python scripts/download_stock_csv.py --gap-fill --gap-fill-from 2023-01-01 --import
```

**Standard download mode**:

```bash
cd backend
python scripts/download_stock_csv.py --ticker <TICKERS> --import

# All tickers
python scripts/download_stock_csv.py --all --import --delay 3
```

### Step 5: Verify Results

After download completes:

1. Check that CSV files exist in the output directory
2. Run `--status` again to confirm gaps have been filled:

```bash
cd backend
python scripts/download_stock_csv.py --status
```

### Step 6: Report

Summarize:
- Number of tickers downloaded successfully vs failed
- Number of records imported
- Coverage improvement (before vs after)
- Any errors or warnings encountered

## Constraints

- Always use `--import` flag unless the user explicitly says not to import
- Use `--delay 3` or higher for batch downloads to avoid rate limiting
- Date format is YYYY-MM-DD (e.g., `--start-date 2025-01-01`)
- If a download fails due to anti-bot detection, suggest `--no-headless` mode
- Do not modify the ticker-to-slug mapping without user confirmation
- Duplicates are safely handled via upsert — re-downloading existing data is harmless
- When no arguments are provided, always show `--status` first before asking what to do
