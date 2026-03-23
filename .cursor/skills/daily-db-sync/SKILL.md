---
name: daily-db-sync
description: >-
  Sync daily pipeline outputs (analysis, screener, discovery, news, reports) from
  the outputs/ directory into the project's PostgreSQL database via
  backend/scripts/sync_daily_outputs.py. Use when the user asks to "sync outputs
  to DB", "persist pipeline results", "daily DB sync", "save today's data to
  database", "DB 싱크", "일일 DB 동기화", "파이프라인 결과 저장", "출력 DB 동기화",
  "오늘 데이터 DB에 넣어줘", or after the today pipeline completes. Do NOT use for
  syncing stock prices from Yahoo Finance (use weekly-stock-update). Do NOT use
  for Cognee knowledge graph ingestion (use knowledge-daily-aggregator). Do NOT
  use for running the analysis pipeline itself (use today). Do NOT use for
  downloading CSVs from investing.com (use stock-csv-downloader). Do NOT use for
  API-based server-side computations like market breadth refresh (use tab-*
  skills directly). Korean triggers: "DB 싱크", "일일 동기화", "데이터베이스 동기화",
  "파이프라인 결과 저장", "outputs DB".
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---

# Daily DB Sync

Sync all daily pipeline outputs from the `outputs/` directory into the project's PostgreSQL database. Bridges the gap between file-based pipeline outputs (produced by the `today` skill) and the backend DB, making all daily data queryable via SQL and the REST API.

## Data Flow

| Source File | Target Table | Upsert Key |
|---|---|---|
| `outputs/analysis-{date}.json` | `technical_analysis_results` | `(ticker_id, date, timeframe)` |
| `outputs/screener-{date}.json` | `screener_snapshots` | `(date, symbol)` |
| `outputs/discovery-{date}.json` | `hot_stocks` | insert (append) |
| `outputs/news-{date}.json` | `news_articles` | dedupe by title+source |
| `outputs/reports/daily-{date}.docx` | `reports` | dedupe by title |

Each sync run is tracked in `daily_sync_runs` with per-source statistics.

## Workflow

1. Determine target date (default: today). Convert Korean date expressions ("3월 18일", "어제", "지난주 금요일") to ISO format `YYYY-MM-DD`
2. Verify the backend DB is reachable and migration 023 is applied
3. Scan `outputs/` for matching files: `*-{date}.json` and `reports/daily-{date}.docx`
4. Run the sync script:

```bash
cd backend && python scripts/sync_daily_outputs.py --date {YYYY-MM-DD}
```

5. Parse output and report results: records synced per table, errors, warnings. The sync is idempotent (upsert-based) — safe to re-run without duplicating data
6. If any source reports `UndefinedTableError`, inform the user that the relevant migration (017-022) needs to be applied

## CLI Reference

```bash
# Sync today's outputs
python scripts/sync_daily_outputs.py

# Sync a specific date
python scripts/sync_daily_outputs.py --date 2026-03-20

# Preview without writing to DB
python scripts/sync_daily_outputs.py --dry-run

# Sync only one source
python scripts/sync_daily_outputs.py --source screener

# View recent sync history
python scripts/sync_daily_outputs.py --status
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/daily-sync/run` | Trigger sync (background) |
| `GET` | `/api/v1/daily-sync/history` | List recent sync runs |
| `GET` | `/api/v1/daily-sync/status/{date}` | Check sync status for a date |
| `GET` | `/api/v1/daily-sync/screener/{date}` | Query screener snapshots |

## Composed Skills

After running the file-based sync, optionally invoke these for server-side computation:

- `tab-market-breadth` — refresh market breadth composite scores
- `tab-market-environment` — refresh regime + breadth + news summary
- `tab-technical-analysis` — recompute TA indicators via backend batch endpoint

## Error Handling

| Situation | Behavior |
|---|---|
| Missing output files for target date | Skipped gracefully with INFO log; not treated as errors |
| Unknown ticker symbol in analysis JSON | Logged as WARNING and skipped; other tickers continue |
| Duplicate news article (same title+source) | Silently skipped; no error raised |
| Table does not exist (missing migration) | Source fails with `UndefinedTableError`; other sources continue via SAVEPOINT isolation |
| Partial failures across sources | Recorded in `daily_sync_runs.errors` JSONB; status set to `partial` |
| All sources fail | Status set to `failed`; script exits with code 1 |
| All sources succeed | Status set to `success`; script exits with code 0 |
| Dry-run with no output files for date | Report "No output files found for {date}. Run the today pipeline first to generate outputs." |
| `--status` returns empty history | Report "No sync history found. Run a sync first with `python scripts/sync_daily_outputs.py`." |
| DB connection refused (any mode) | Report "Cannot connect to PostgreSQL. Verify DATABASE_URL in .env and that the DB is running." |

## Examples

### Example 1: Full Sync After Today Pipeline

```
User: 오늘 파이프라인 결과 DB에 싱크해줘
Agent:
1. Runs: cd backend && python scripts/sync_daily_outputs.py --date 2026-03-20
2. Script output shows:
     screener: 39 records synced
     discovery: 1 records synced
     report: registered 'Daily Stock Report 2026-03-20'
     analysis: ERROR — table does not exist (migration 019 needed)
3. Reports to user:
   - 3/5 sources synced successfully (41 total records)
   - analysis and discovery tables need migrations 017-022 applied
   - Recommendation: run `cd backend && alembic upgrade head` to enable all sources
```

### Example 2: Dry Run Preview

```
User: DB 싱크 미리보기 해줘
Agent:
1. Runs: cd backend && python scripts/sync_daily_outputs.py --dry-run --date 2026-03-20
2. Script output shows:
     [DRY] Would upsert TA for 000660 ... (52 records)
     [DRY] Would upsert screener for NVDA (score=19.5) ... (39 records)
3. Reports: "Would sync ~92 records across 5 sources. No DB changes made."
```

### Example 3: Single Source Sync

```
User: screener 데이터만 DB에 넣어줘
Agent:
1. Runs: cd backend && python scripts/sync_daily_outputs.py --source screener --date 2026-03-20
2. Reports: "screener: 39 records synced (upsert — safe to re-run)"
```

### Example 4: Check Sync History

```
User: 최근 싱크 상태 보여줘
Agent:
1. Runs: cd backend && python scripts/sync_daily_outputs.py --status
2. Shows table:
   Date         Status     Records                            Duration
   2026-03-20   partial    screener:39, discovery:1, report:1  0.1s
   2026-03-20   success    screener:39                         0.1s
```
