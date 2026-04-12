# gbrain-ingest

Wrapper around gbrain's ingest capabilities adapted to the project's file-first pipeline conventions. Accepts pipeline output files (`outputs/` manifests), extracts entity-relevant content, and routes it to gbrain via MCP tools. Follows the `outputs/{pipeline}/{date}/manifest.json` pattern.

## Triggers

Use when the user asks to "ingest to gbrain", "push pipeline output to gbrain", "gbrain ingest", "route output to gbrain", "entity ingest", "gbrain에 인제스트", "파이프라인 출력 gbrain", "gbrain-ingest", or when invoked by `knowledge-daily-aggregator` (Phase 5.7) or `meeting-digest` post-hook.

Do NOT use for KB topic ingestion (use kb-ingest).
Do NOT use for bidirectional KB-gbrain sync (use gbrain-bridge).
Do NOT use for federated search (use unified-knowledge-search).
Do NOT use for raw gbrain MCP operations without pipeline context (use gbrain MCP tools directly).

## Input Sources

| Source | Path pattern | Entity types extracted |
|--------|-------------|----------------------|
| Meeting digest | `outputs/meeting-digest/{date}/` | People (attendees), companies, action items |
| Email triage | `outputs/gmail-triage/{date}/` | People (senders), companies |
| Paper review | `outputs/paper-review/{date}/` | People (authors), companies (affiliations) |
| Sprint digest | `outputs/github-sprint-digest/{date}/` | People (contributors) |
| Today pipeline | `outputs/today/{date}/` | Companies (stock tickers → company entities) |
| Bespin news | `outputs/bespin-news/{date}/` | Companies mentioned in news articles |
| Manual | User-provided text or file | Any entity type |

## Workflow

### Step 1: Source Detection

Identify the input source type from the provided path or context:
- If a manifest.json path is given → read manifest, identify phases
- If a directory path is given → scan for manifest.json
- If raw text is given → treat as manual ingest

### Step 2: Entity Extraction

Extract entities from the source using content-appropriate patterns:

**Meeting digest**:
- Attendee names → `people/{first-last}` pages
- Company mentions → `companies/{name}` pages
- Action items with owners → timeline entries on person pages

**Email triage**:
- Sender name + email → `people/{first-last}` pages with email in content
- Company domain from email → `companies/{domain}` pages

**Paper review**:
- Author list → `people/{first-last}` pages with affiliation
- Institution/lab names → `companies/{name}` pages

**Today pipeline (stock analysis)**:
- Stock ticker → company entity enrichment
- Only create company pages for stocks with BUY/STRONG_BUY signals (skip routine data)

### Step 3: Deduplication Check

For each extracted entity:
1. Call `resolve_slugs` with entity name variations
2. If slug resolves → existing page, use `add_timeline_entry`
3. If no match → call `put_page` to create new entity page

### Step 4: Entity Page Creation/Update

**New entity**: Call `put_page` with:
```json
{
  "slug": "people/jane-doe",
  "content": "# Jane Doe\n\n## Compiled Truth\nSoftware Engineer at Acme Corp.\n\n## Evidence Trail\n- [2026-04-10] First seen in meeting digest: Design Review",
  "frontmatter": {
    "type": "person",
    "source_pipeline": "meeting-digest",
    "first_seen": "2026-04-10"
  }
}
```

**Existing entity**: Call `add_timeline_entry` with:
```json
{
  "slug": "people/jane-doe",
  "entry": "[2026-04-10] Mentioned in design review meeting. Discussed API migration timeline.",
  "source": "meeting-digest"
}
```

### Step 5: Relationship Linking

After entity creation/update:
- `add_link` person → company (employment/affiliation)
- `add_link` person → meeting (attendance)
- `add_link` company → deal (if deal context exists)
- `add_tag` with source pipeline name (e.g., `pipeline:meeting-digest`)

### Step 6: Output Manifest

Write results to `outputs/gbrain-ingest/{date}/`:
```json
{
  "phase": "gbrain-ingest",
  "source": "meeting-digest",
  "source_date": "2026-04-10",
  "entities_created": 3,
  "entities_updated": 5,
  "timeline_entries_added": 8,
  "links_created": 4,
  "tags_applied": 8,
  "errors": [],
  "skipped": ["John Smith (already up-to-date)"],
  "duration_ms": 2340
}
```

## MCP Tools Used

| Operation | gbrain MCP tool |
|-----------|----------------|
| Check existing entities | `resolve_slugs` |
| Create entity page | `put_page` |
| Append evidence | `add_timeline_entry` |
| Create relationships | `add_link` |
| Tag with source | `add_tag` |

## Signal Strength Filter

Not every mention warrants a gbrain entity. Apply these thresholds:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Person mentioned once, no context | Skip | Too noisy |
| Person with role/title context | Create | `people/` page |
| Person in meeting attendee list | Create | `people/` page + meeting link |
| Company mentioned in passing | Skip | Unless in stock watchlist |
| Company with analysis/deal context | Create | `companies/` page |
| Stock with BUY signal | Create/Update | `companies/` page with signal timeline |

## Error Handling

- gbrain MCP unavailable: log warning, write failed items to `outputs/gbrain-ingest/{date}/retry-queue.json`
- Entity extraction fails: skip item, continue with next
- `put_page` conflict: fall back to `add_timeline_entry` on existing page
- Rate limiting: batch operations with 100ms delay between MCP calls

## Checklist

- [ ] Identify input source and path
- [ ] Extract entities with signal strength filtering
- [ ] Deduplicate against existing gbrain pages
- [ ] Create/update entity pages with timeline entries
- [ ] Establish relationship links between entities
- [ ] Write output manifest to `outputs/gbrain-ingest/{date}/`
- [ ] Report summary with create/update/skip counts
