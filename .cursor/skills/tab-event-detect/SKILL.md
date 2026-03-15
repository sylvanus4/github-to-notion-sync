---
description: "Trigger event detection from RSS feeds via POST /events/detect. Use when detecting events, '이벤트 탐지', 'tab-event-detect', 'RSS event scan'. Do NOT use for manual event creation (use events API) or event study analysis (use tab-analysis-run)."
---

# tab-event-detect

## Purpose

This skill triggers automated event detection from RSS feeds. It calls `POST /events/detect` which runs the event detection task in background — fetches RSS feeds, scores items with keyword matching, and creates new events in the database.

## When to Use

- detect events
- 이벤트 탐지
- tab-event-detect
- RSS event scan

## When NOT to Use

- manual event creation (use events API)
- event study analysis (use tab-analysis-run)

## Workflow

1. Ensure backend server is running on port 4567
2. Call `POST /api/v1/events/detect` to start the background event detection task
3. Task fetches RSS feeds, scores items with keyword matching, and creates new events in the database

## API Endpoints Used

- `POST /api/v1/events/detect` — triggers background event detection from RSS feeds

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with events schema

## Output

New events created in the database from RSS feed items that match event keywords.
