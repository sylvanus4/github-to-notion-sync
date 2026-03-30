---
description: "Manage financial glossary terms via CRUD at /glossary, batch import with POST /glossary/batch, search with GET /glossary/search, and export with GET /glossary/export. Use when managing glossary, '용어 관리', 'tab-glossary', 'glossary import export'. Do NOT use for general documentation (use technical-writer), news analysis (use tab-news-fetch), or stock data (use tab-stock-sync)."
---

# tab-glossary

## Purpose

Manage financial domain glossary terms — create, read, update, delete, search, batch import, and export. Supports Korean/English terms with categories and example contexts.

## When to Use

- glossary management
- 용어 관리
- tab-glossary
- glossary import/export
- add financial term
- batch import terms

## When NOT to Use

- General documentation — use technical-writer
- News analysis — use tab-news-fetch
- Stock data management — use tab-stock-sync

## Workflow

1. List all terms with `GET /api/v1/glossary` (params: skip, limit)
2. Search terms with `GET /api/v1/glossary/search?q=...` (optional category filter)
3. Create a term with `POST /api/v1/glossary` (body: term, definition, category, korean_term, example_context)
4. Batch import with `POST /api/v1/glossary/batch` (body: array of term objects; skips duplicates)
5. Export all terms with `GET /api/v1/glossary/export` (param: download=true for file headers)
6. Update a term with `PUT /api/v1/glossary/{term_id}`
7. Delete a term with `DELETE /api/v1/glossary/{term_id}`

## Endpoints Used

- `GET /api/v1/glossary` — list all terms (paginated)
- `GET /api/v1/glossary/search` — search by keyword + optional category
- `POST /api/v1/glossary` — create single term
- `POST /api/v1/glossary/batch` — batch import (skips duplicates, reports created/skipped/errors)
- `GET /api/v1/glossary/export` — export all as JSON (optional download=true)
- `GET /api/v1/glossary/{term_id}` — get single term
- `PUT /api/v1/glossary/{term_id}` — update term
- `DELETE /api/v1/glossary/{term_id}` — delete term

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL

## Output

Glossary term CRUD operations with batch import/export support.
