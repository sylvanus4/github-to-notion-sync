---
name: tab-patterns
description: >-
  Query event-study pattern groups via GET /patterns, search with GET
  /patterns/search, get statistics with GET /patterns/stats, and export with
  GET /patterns/export. Use when querying patterns, '패턴 조회', 'tab-patterns',
  'pattern analysis'. Do NOT use for event detection (use tab-event-detect),
  event study CAR analysis (use tab-analysis-run), or stock price sync (use
  tab-stock-sync).
---

# tab-patterns

## Purpose

Query, search, and analyze reusable event-study patterns discovered from past analyses. Patterns represent recurring relationships between event types and stock price reactions.

## When to Use

- query patterns
- 패턴 조회
- tab-patterns
- pattern search
- pattern statistics

## When NOT to Use

- Event detection from RSS — use tab-event-detect
- Event study CAR analysis — use tab-analysis-run
- Stock price sync — use tab-stock-sync

## Workflow

1. List all patterns with `GET /api/v1/patterns` (params: min_frequency, min_significance)
2. Search patterns by keyword with `GET /api/v1/patterns/search?q=earnings`
3. Get aggregate statistics with `GET /api/v1/patterns/stats` (top by frequency, strongest by CAR, most consistent)
4. Export all patterns with `GET /api/v1/patterns/export` (param: download=true for file headers)
5. Get detail for a specific pattern group with `GET /api/v1/patterns/{pattern_group}`

## Endpoints Used

- `GET /api/v1/patterns` — list all patterns with filters
- `GET /api/v1/patterns/search` — search by keyword (q param, optional min_frequency, min_significance)
- `GET /api/v1/patterns/stats` — aggregate statistics (total, top by frequency, strongest, most consistent)
- `GET /api/v1/patterns/export` — export all patterns as JSON (optional download=true)
- `GET /api/v1/patterns/{pattern_group}` — single pattern detail with all tickers and events

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with event analysis results

## Output

Pattern data with frequency, average CAR, significance, and associated tickers/events.
