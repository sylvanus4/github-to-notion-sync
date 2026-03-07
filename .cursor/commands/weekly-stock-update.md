---
description: "Fetch recent stock prices from Yahoo Finance and upsert into PostgreSQL"
---

# Weekly Stock Update

## Skill Reference

Read and follow the skill at `.cursor/skills/weekly-stock-update/SKILL.md`.

## Your Task

The user input can be provided directly or as a command argument — consider it before proceeding.

User input:

$ARGUMENTS

### Step 1: Parse Request

Determine the **mode** from user input:

- **Status / check / coverage**: keywords like "status", "check", "coverage" → use `--status`
- **Dry run / preview**: keywords like "dry-run", "preview", "test" → use `--dry-run`
- **Specific tickers**: ticker symbols mentioned → use `--ticker`
- **Custom days**: number of days mentioned → use `--days`
- **No arguments**: run update for all tickers with default 10-day lookback

Also determine:
- **Target tickers**: specific symbols (e.g., NVDA, AAPL, 005930) or all
- **Lookback days**: custom number of days (default: 10)

### Step 2: Check DB Status

Always start by showing current coverage:

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

### Step 3: Run Update

Based on parsed mode:

**All tickers (default):**

```bash
cd backend
python scripts/weekly_stock_update.py
```

**Specific tickers:**

```bash
cd backend
python scripts/weekly_stock_update.py --ticker <TICKERS>
```

**Custom lookback:**

```bash
cd backend
python scripts/weekly_stock_update.py --days <N>
```

**Dry run:**

```bash
cd backend
python scripts/weekly_stock_update.py --dry-run
```

### Step 4: Verify Results

After the update completes, re-run status to confirm:

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

### Step 5: Report

Summarize:
- Number of tickers updated successfully vs failed
- Total records upserted
- Date range of updated data
- Any errors or warnings encountered

## Constraints

- Always show `--status` before and after the update
- Use `--delay 1` or higher if rate limiting is observed
- If no arguments are provided, update all tickers with a 10-day lookback
- Re-running is safe — upsert prevents duplicates
- For historical backfill (months/years of data), suggest using `/stock-csv-download` instead
