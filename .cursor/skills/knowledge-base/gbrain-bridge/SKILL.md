# gbrain-bridge

Bidirectional sync between gbrain entity pages (Postgres + pgvector) and the Karpathy Markdown Knowledge Base (`knowledge-bases/*/wiki/`). Extracts entities from KB wiki articles into gbrain, and syncs gbrain compiled-truth pages back as KB raw sources.

## Triggers

Use when the user asks to "sync gbrain with KB", "bridge gbrain", "push entities to gbrain", "pull gbrain to KB", "gbrain KB sync", "entity extraction to gbrain", "gbrain-bridge", "KB 엔티티 gbrain 동기화", "gbrain KB 브릿지", "gbrain에서 KB로", "KB에서 gbrain으로", or any request to move knowledge between gbrain and the Karpathy KB.

Do NOT use for standalone gbrain operations without KB context (use gbrain MCP tools directly).
Do NOT use for KB compilation or indexing (use kb-compile, kb-index).
Do NOT use for general knowledge search (use unified-knowledge-search).
Do NOT use for meeting entity extraction (use meeting-digest + Phase 4a hook).

## Domain Split Rules

gbrain owns **entity-centric** pages only:

| Slug prefix | Entity type | Example |
|-------------|-------------|---------|
| `people/` | People, contacts | `people/garry-tan` |
| `companies/` | Companies, orgs | `companies/y-combinator` |
| `deals/` | Deals, opportunities | `deals/series-a-acme` |
| `meetings/` | Meeting summaries | `meetings/2026-04-10-design-review` |
| `ideas/` | Project ideas | `ideas/agent-memory-federation` |

Karpathy KB owns **domain-topic** knowledge (trading-daily, engineering-standards, ai-research, etc.).

## Modes

### 1. `kb-to-gbrain` (Extract entities from KB → gbrain)

**When**: New wiki articles contain references to people, companies, or organizations.

**Steps**:
1. Scan target KB topic's `wiki/` directory for markdown files
2. Extract entity mentions using NER patterns:
   - People: proper nouns near role indicators (CEO, CTO, researcher, author, founder)
   - Companies: proper nouns near org indicators (Inc, Corp, LLC, Labs, AI, Technologies)
   - Papers: author names from `paper-review` outputs
3. For each extracted entity:
   - Check if gbrain page exists: `resolve_slugs` with the entity name
   - If exists: `add_timeline_entry` with source reference
   - If new: `put_page` with frontmatter and initial content from KB context
4. Create `add_link` between related entities (e.g., person → company)
5. `add_tag` with the source KB topic name (e.g., `kb:ai-research`)
6. Log sync to `outputs/gbrain-bridge/{date}/kb-to-gbrain.json`

**Entity page template** (for `put_page`):
```markdown
---
type: {person|company|organization}
source: kb:{topic-name}
extracted_from: {wiki-article-path}
extracted_at: {ISO-date}
---

# {Entity Name}

## Compiled Truth
{Initial context extracted from KB article}

## Evidence Trail
- [{date}] Extracted from KB topic `{topic}`, article `{article-title}`
```

### 2. `gbrain-to-kb` (Sync gbrain compiled truth → KB raw/)

**When**: gbrain entity pages accumulate enough evidence to be useful as KB source material.

**Steps**:
1. Query gbrain for pages updated since last sync: `list_pages` with date filter
2. Filter for pages with `>= 3 timeline entries` (threshold for KB-worthy content)
3. For each qualifying page:
   - `get_page` to retrieve full compiled truth + timeline
   - Determine target KB topic from tags (e.g., `kb:competitive-intel` → `competitive-intel`)
   - Write to `knowledge-bases/{topic}/raw/gbrain-{slug}.md` with YAML frontmatter
   - Include source attribution: `source: gbrain, slug: {slug}, synced_at: {date}`
4. Log sync to `outputs/gbrain-bridge/{date}/gbrain-to-kb.json`

### 3. `link-sync` (Maintain cross-references)

**Steps**:
1. Scan gbrain entity pages for `[[wiki:topic/article]]` references
2. Scan KB wiki articles for `[[gbrain:slug]]` references
3. Ensure bidirectional links exist in gbrain via `add_link`
4. Generate a cross-reference report

### 4. `status` (Sync health check)

**Steps**:
1. `get_stats` from gbrain for page/link/tag counts
2. Count KB wiki articles across all topics
3. Compare entity coverage: how many KB-mentioned entities exist in gbrain
4. Report last sync timestamps from `outputs/gbrain-bridge/` logs
5. Flag stale entities (no timeline entry in 30+ days)

## Slug Convention

Entity slugs follow gbrain's convention with domain prefix:

```
people/{first-last}           → people/garry-tan
companies/{name-normalized}   → companies/y-combinator
deals/{identifier}            → deals/series-a-acme
meetings/{date-title}         → meetings/2026-04-10-standup
ideas/{kebab-title}           → ideas/federated-skill-sync
```

## Configuration

Sync settings in `outputs/gbrain-bridge/config.json`:
```json
{
  "kb_topics_for_entity_scan": ["ai-research", "competitive-intel", "meeting-summaries"],
  "gbrain_to_kb_threshold": 3,
  "sync_interval_hours": 24,
  "entity_patterns": {
    "people": ["CEO", "CTO", "founder", "researcher", "author", "engineer", "professor"],
    "companies": ["Inc", "Corp", "LLC", "Labs", "AI", "Technologies", "Cloud", "Platform"]
  }
}
```

## MCP Tools Used

| Operation | gbrain MCP tool |
|-----------|----------------|
| Check entity exists | `resolve_slugs` |
| Create/update entity page | `put_page` |
| Add evidence to timeline | `add_timeline_entry` |
| Create entity relationships | `add_link` |
| Tag with KB source | `add_tag` |
| List updated pages | `list_pages` |
| Read entity content | `get_page` |
| Check brain health | `get_stats` |

## Output Format

All sync operations produce manifest files following the project's file-first convention:

```
outputs/gbrain-bridge/{date}/
├── kb-to-gbrain.json      # Entities extracted and pushed
├── gbrain-to-kb.json      # Pages synced back to KB raw/
├── link-sync.json          # Cross-references maintained
└── manifest.json           # Phase summary
```

## Error Handling

- gbrain MCP unavailable: skip sync, log warning, continue pipeline
- Entity already exists: merge via `add_timeline_entry` (append-only)
- KB topic not found: skip with warning, do not create new topics
- Embedding failures: `put_page` still succeeds; embeddings run later via `gbrain embed --stale`

## Checklist

- [ ] Determine sync mode (kb-to-gbrain / gbrain-to-kb / link-sync / status)
- [ ] Verify gbrain MCP server is reachable
- [ ] Run the selected sync operation
- [ ] Verify output manifest in `outputs/gbrain-bridge/{date}/`
- [ ] Report sync summary with counts and any warnings
