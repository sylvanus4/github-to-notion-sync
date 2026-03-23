---
description: "Sync daily pipeline outputs (analysis, screener, discovery, news, reports) from outputs/ into the project's PostgreSQL database"
---

## Daily DB Sync

Sync all daily pipeline outputs from `outputs/` into the PostgreSQL database, bridging file-based pipeline results and the backend DB.

### Usage

```
/daily-db-sync                              # sync today's outputs
/daily-db-sync --date 2026-03-20            # sync a specific date
/daily-db-sync --dry-run                    # preview without DB writes
/daily-db-sync --source screener            # sync only screener data
/daily-db-sync --status                     # show recent sync history
/daily-db-sync --with-api                   # also trigger tab-* API refreshes
```

### Execution

Read and follow the skill at `.cursor/skills/daily-db-sync/SKILL.md`.

User input: $ARGUMENTS

1. Determine target date from arguments (default: today)
2. Run `cd backend && python scripts/sync_daily_outputs.py` with appropriate flags
3. Report per-source record counts, errors, and sync run status
4. If `--with-api` flag is set, also call tab-market-breadth, tab-market-environment, and tab-technical-analysis API refreshes
5. Output summary: total records synced, sync run ID, any warnings
