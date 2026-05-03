---
name: gbrain-ingest
description: >-
  Wrapper around gbrain's ingest capabilities adapted to the project's
  file-first pipeline conventions. Accepts pipeline output files (`outputs/`
  manifests), extracts entity-relevant content, and routes it to gbrain via
  MCP tools. Supports `--ambient` mode for lightweight signal detection.
  Enforces gbrain v0.10 conventions: brain-first lookup, Iron Law of
  Back-Linking, inline citations, and subject-based filing.
---

# gbrain-ingest

Wrapper around gbrain's ingest capabilities adapted to the project's file-first pipeline conventions. Accepts pipeline output files (`outputs/` manifests), extracts entity-relevant content, and routes it to gbrain via MCP tools. Follows the `outputs/{pipeline}/{date}/manifest.json` pattern. Supports `--ambient` mode for lightweight signal detection on any conversation context.

Enforces the gbrain v0.10 conventions: brain-first lookup before external APIs, Iron Law of Back-Linking on every `put_page`, inline `[Source: ...]` citations, and subject-based filing (see `gbrain-conventions/` reference files).

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

## Modes

### Pipeline Mode (default)

Reads `outputs/{pipeline}/{date}/manifest.json`, extracts entities, and routes them to gbrain with full enrichment. Used by `knowledge-daily-aggregator` and `meeting-digest`.

### Ambient / Signal-Detector Mode (`--ambient`)

Lightweight mode inspired by gbrain v0.10's `signal-detector` skill. Runs as a low-cost subagent during any conversation to capture:
- **Original ideas**: novel thoughts worth preserving → `ideas/{slug}`
- **Entity mentions**: people, companies, projects referenced in passing → `people/` or `companies/` (only if notable — see Signal Strength Filter)
- **Decisions**: choices with rationale → timeline entry on relevant page

Ambient mode skips the full pipeline workflow. Instead:
1. Scan conversation context for signals
2. Brain-first lookup each candidate (Step 0 below)
3. If new and notable → `put_page` with `[Source: conversation, {date}]`
4. If exists → `add_timeline_entry` only if the new signal adds information

## Workflow (Pipeline Mode)

### Step 0: Brain-First Lookup (MANDATORY)

Before ANY external API call or entity creation, check if the brain already knows about this entity. This is the full 5-step brain-first protocol from `gbrain-conventions/brain-first.md`:

1. **`gbrain search "{entity name}"`** — keyword search for existing pages
2. **`gbrain query "natural question about {entity name}"`** — hybrid search for related context
3. **`gbrain get <slug>`** — if a page exists, read the full page (especially its Compiled Truth section)
4. **`gbrain get_backlinks <slug>`** — check who references this entity for relationship context
5. **`gbrain get_timeline <slug>`** — check recent events involving this entity

After lookup, apply these rules:
- **Merge, don't overwrite**: New evidence APPENDS to the Evidence Trail; Compiled Truth only updates if new facts contradict or extend existing truth
- **Skip if stale-identical**: If the new information adds nothing to what the brain already has, skip the write

This step prevents duplicate pages and ensures the brain compounds knowledge rather than scattering it.

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

### Step 3: Filing Decision (gbrain v0.10 repo-architecture)

Determine the correct directory path by primary subject. Follow `gbrain-conventions/filing-rules.md`:

| Primary subject | Directory | Example slug |
|---|---|---|
| A person | `people/` | `people/jane-doe` |
| A company or org | `companies/` | `companies/acme-corp` |
| An idea or concept | `ideas/` | `ideas/edge-compute-strategy` |
| A project | `projects/` | `projects/platform-v2` |
| A deal or opportunity | `deals/` | `deals/acme-enterprise-2026` |
| A meeting or event | `meetings/` | `meetings/2026-04-10-design-review` |
| A topic or domain | `topics/` | `topics/kubernetes-scheduling` |

If the content spans multiple subjects, file under the PRIMARY subject and add back-links from secondary subjects.

### Step 4: Deduplication Check

For each extracted entity:
1. Call `resolve_slugs` with entity name variations
2. If slug resolves → existing page, use `add_timeline_entry`
3. If no match → call `put_page` to create new entity page

### Step 5: Entity Page Creation/Update

**New entity**: Call `put_page` with inline citation:
```json
{
  "slug": "people/jane-doe",
  "content": "# Jane Doe\n\n## Compiled Truth\nSoftware Engineer at Acme Corp. [Source: meeting-digest, 2026-04-10]\n\n## Evidence Trail\n- [2026-04-10] First seen in meeting digest: Design Review [Source: meeting-digest, 2026-04-10]",
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
  "entry": "[2026-04-10] Mentioned in design review meeting. Discussed API migration timeline. [Source: meeting-digest, 2026-04-10]",
  "source": "meeting-digest"
}
```

### Step 6: Back-Linking (Iron Law)

**Every `put_page` call MUST create at least one back-link.** This is the Iron Law of Back-Linking from gbrain v0.10:

After entity creation/update:
- `add_link` person → company (employment/affiliation)
- `add_link` person → meeting (attendance)
- `add_link` company → deal (if deal context exists)
- `add_link` meeting → attendee pages (reverse links)
- `add_tag` with source pipeline name (e.g., `pipeline:meeting-digest`)

If no natural link target exists, link to the source pipeline's daily output page (e.g., `meetings/2026-04-10-standup`).

### Step 7: Citation Enforcement

Every Compiled Truth statement and Evidence Trail entry MUST include a `[Source: ...]` citation. Format: `[Source: {pipeline-name}, {date}]` or `[Source: {url}]`.

Before finalizing the batch, scan all generated content for citation compliance. If any statement lacks a source tag, add it from the pipeline metadata.

### Step 8: Post-Import Extraction

After all entity pages are created/updated, run link and timeline extraction to update the brain's graph:

```bash
gbrain extract links --dir ~/brain    # refreshes cross-page link graph
gbrain extract timeline --dir ~/brain  # rebuilds timeline indices
```

These commands are idempotent and fast — safe to run on every ingest cycle.

### Step 9: Output Manifest

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
  "back_links_created": 6,
  "tags_applied": 8,
  "citations_enforced": 11,
  "extract_links_run": true,
  "extract_timeline_run": true,
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

- [ ] Step 0: Brain-first lookup for every entity candidate
- [ ] Step 1: Identify input source and path
- [ ] Step 2: Extract entities with signal strength filtering
- [ ] Step 3: Determine correct filing directory per entity
- [ ] Step 4: Deduplicate against existing gbrain pages
- [ ] Step 5: Create/update entity pages with timeline entries
- [ ] Step 6: Enforce Iron Law — every `put_page` has ≥1 back-link
- [ ] Step 7: Verify every statement has a `[Source: ...]` citation
- [ ] Step 8: Run `gbrain extract links` and `gbrain extract timeline`
- [ ] Step 9: Write output manifest to `outputs/gbrain-ingest/{date}/`
- [ ] Report summary with create/update/skip/citation counts

## References

- `gbrain-conventions/brain-first.md` — 5-step brain-first lookup protocol
- `gbrain-conventions/quality.md` — citation, back-link, and compiled truth standards
- `gbrain-conventions/filing-rules.md` — subject-based directory filing decision tree
