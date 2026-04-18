---
name: gbrain-bridge
description: Bidirectional sync between gbrain entity pages and the Karpathy Markdown Knowledge Base with v0.10 convention enforcement
conventions:
  - skills/knowledge-base/gbrain-conventions/brain-first.md
  - skills/knowledge-base/gbrain-conventions/quality.md
  - skills/knowledge-base/gbrain-conventions/filing-rules.md
---

# gbrain-bridge

Bidirectional sync between gbrain entity pages (Postgres + pgvector) and the Karpathy Markdown Knowledge Base (`knowledge-bases/*/wiki/`). Extracts entities from KB wiki articles into gbrain, and syncs gbrain compiled-truth pages back as KB raw sources.

All write operations follow the gbrain v0.10 conventions:
- **Brain-First Lookup** (`gbrain-conventions/brain-first.md`): 5-step protocol before any write
- **Quality Convention** (`gbrain-conventions/quality.md`): citations, back-linking, notability gate
- **Filing Rules** (`gbrain-conventions/filing-rules.md`): subject-determined directory placement

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
3. **Brain-First Lookup (MANDATORY)** — for each extracted entity, run the full 5-step protocol before creating or updating:
   1. `gbrain search "{entity name}"` — keyword search for existing pages
   2. `gbrain query "what do we know about {entity name}"` — hybrid search for related context
   3. `gbrain get <slug>` — if a page exists, read the full content (especially Compiled Truth)
   4. `get_backlinks <slug>` — check who references this entity for relationship context
   5. `get_timeline <slug>` — check recent events involving this entity
4. **Apply Notability Gate** — only create new pages for entities that meet at least one criterion:
   - ≥ 2 independent KB source mentions
   - Role significance (C-suite, lead author, founding team)
   - Active deal or meeting participant
   - Sub-notable entities go into the parent entity's Evidence Trail instead
5. Based on lookup results:
   - **Entity exists + new info**: `add_timeline_entry` with `[Source: KB/{topic}/{article}]` citation
   - **Entity exists + stale-identical**: skip (no write needed)
   - **New notable entity**: `put_page` with template below, mandatory `[Source: ...]` citation
6. Create `add_link` between related entities (e.g., person → company) — **Iron Law of Back-Linking**: every link must be bidirectional
7. `add_tag` with the source KB topic name (e.g., `kb:ai-research`)
8. **Filing Rules**: slug prefix determined by primary subject (`people/`, `companies/`, etc.) per `gbrain-conventions/filing-rules.md`
9. Log sync to `outputs/gbrain-bridge/{date}/kb-to-gbrain.json`

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
{Initial context extracted from KB article} [Source: KB/{topic}/{article-title}]

## Evidence Trail
- [{date}] Extracted from KB topic `{topic}`, article `{article-title}` [Source: KB/{topic}/{article-title}]
```

### 2. `gbrain-to-kb` (Sync gbrain compiled truth → KB raw/)

**When**: gbrain entity pages accumulate enough evidence to be useful as KB source material.

**Steps**:
1. Query gbrain for pages updated since last sync: `list_pages` with date filter
2. Filter for pages with `>= 3 timeline entries` (threshold for KB-worthy content)
3. For each qualifying page:
   - `get_page` to retrieve full compiled truth + timeline
   - Determine target KB topic from tags (e.g., `kb:competitive-intel` → `competitive-intel`)
   - Convert to KB raw source format — **preserve all inline `[Source: ...]` citations** from the original gbrain page
   - Write to `knowledge-bases/{topic}/raw/gbrain-{slug}.md` with YAML frontmatter
   - Include source attribution: `source: gbrain, slug: {slug}, synced_at: {date}`
4. **Back-Linking**: add a `[[gbrain:{slug}]]` wikilink in the KB raw file, and ensure the gbrain page has a tag referencing the KB topic
5. Log sync to `outputs/gbrain-bridge/{date}/gbrain-to-kb.json`

### 3. `link-sync` (Maintain cross-references)

**Steps**:
1. Scan gbrain entity pages for `[[wiki:topic/article]]` references
2. Scan KB wiki articles for `[[gbrain:slug]]` references
3. Use `get_backlinks` to verify existing gbrain-side back-links are complete
4. Ensure bidirectional links exist in gbrain via `add_link` — **Iron Law of Back-Linking**: every link must be paired
5. Generate a cross-reference report with gap count and newly created links

### 4. `status` (Sync health check)

**Steps**:
1. `get_stats` from gbrain for page/link/tag counts
2. `gbrain health --json` for composite Brain Health Score (0-100)
3. Count KB wiki articles across all topics
4. Compare entity coverage: how many KB-mentioned entities exist in gbrain
5. Report last sync timestamps from `outputs/gbrain-bridge/` logs
6. Flag stale entities (no timeline entry in 30+ days) using `get_timeline`

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
| Keyword search | `gbrain search` (CLI) |
| Hybrid search | `gbrain query` (CLI) |
| Create/update entity page | `put_page` |
| Add evidence to timeline | `add_timeline_entry` |
| Create entity relationships | `add_link` |
| Check back-links | `get_backlinks` |
| Check entity timeline | `get_timeline` |
| Tag with KB source | `add_tag` |
| List updated pages | `list_pages` |
| Read entity content | `get_page` |
| Check brain health | `get_stats` |
| Brain health score | `gbrain health --json` (CLI) |

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
- [ ] Run Brain-First 5-step lookup before any entity write (kb-to-gbrain mode)
- [ ] Apply Notability Gate for new entities (kb-to-gbrain mode)
- [ ] Ensure all writes include `[Source: ...]` citations
- [ ] Verify Iron Law of Back-Linking: every `add_link` is bidirectional
- [ ] Run the selected sync operation
- [ ] Verify output manifest in `outputs/gbrain-bridge/{date}/`
- [ ] Report sync summary with counts and any warnings
