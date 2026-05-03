---
name: obsidian-kb-bridge
description: >-
  Bridge Obsidian vault operations with the project's LLM Knowledge Base
  pipeline — sync vault content to KB raw sources, trigger KB compilation from
  vault notes, query KB from Obsidian context, and maintain bidirectional
  cross-references. Orchestrates obsidian-files, obsidian-search,
  obsidian-notes, kb-ingest, kb-compile, kb-query, and kb-orchestrator into
  unified vault-to-KB workflows. Use when the user asks to sync vault to KB,
  build KB from Obsidian, query KB via Obsidian, vault-to-KB pipeline,
  Obsidian KB integration, bridge vault and knowledge base, or automate KB
  from vault content. Do NOT use for standalone vault operations without KB
  intent (use obsidian-* skills), standalone KB operations without Obsidian
  (use kb-* skills), or general web research (use parallel-web-search). Korean
  triggers: "옵시디언 KB 연동", "볼트 KB 동기화", "옵시디언 지식베이스", "볼트에서 KB", "KB 옵시디언 브릿지",
  "옵시디언 위키 빌드".
---

# Obsidian KB Bridge — Vault ↔ Knowledge Base Integration

Orchestrates Obsidian CLI skills and KB pipeline skills into unified
workflows for bidirectional knowledge management.

## Prerequisites

- Obsidian CLI configured and healthy (`obsidian-setup`)
- Knowledge Base environment ready (`kb-orchestrator`)
- Vault `knowledge-bases/` open in Obsidian (see `OBSIDIAN_SETUP.md`)

## Workflow Modes

### 1. Vault → KB Ingest

Export vault notes as KB raw sources for compilation into a wiki.

```
Obsidian Vault ─── obsidian-search ──→ identify notes
                   obsidian-files  ──→ read content
                   kb-ingest       ──→ add to KB raw/
                   kb-compile      ──→ generate wiki articles
```

**Steps:**

1. **Discover source notes** — use `obsidian search` or `obsidian tags` to
   find notes matching the target KB topic
2. **Read content** — use `obsidian read file="note"` to extract markdown
3. **Ingest to KB** — pipe content through `kb-ingest` as text sources
4. **Compile wiki** — run `kb-compile` to generate wiki articles from the
   new raw sources

**Example invocation:**

```bash
# Find all notes tagged "research"
obsidian tags file="*" | grep research

# Read a specific research note
obsidian read file="Research/LLM Agents"

# Then invoke kb-ingest skill to add the content as a raw source
# Then invoke kb-compile to rebuild the wiki
```

### 2. KB → Vault Publish

Push compiled KB wiki articles back into the Obsidian vault for
graph-based exploration.

```
KB wiki/ ──→ copy articles to vault ──→ obsidian-files creates notes
         ──→ wikilinks preserved    ──→ graph view shows connections
```

**Steps:**

1. **Identify KB articles** — check `wiki/` directory for compiled content
2. **Create vault notes** — use `obsidian create` for each article
3. **Preserve links** — wikilinks in KB articles map directly to Obsidian
   `[[links]]`

### 3. KB Query via Vault Context

Use the current Obsidian context to formulate KB queries.

```bash
# Read current note for context
obsidian read

# Use the content to query KB (invoke kb-query skill)
# "What does the KB say about <topic from current note>?"
```

### 4. Full Sync Pipeline

End-to-end vault-to-KB pipeline:

1. `obsidian tags` — discover source material by tag
2. `obsidian search query="<topic>"` — find relevant notes
3. `obsidian read file="<note>"` — extract content per note
4. `kb-ingest` — add each note as a raw source
5. `kb-compile` — rebuild the wiki
6. `kb-lint` — check wiki health
7. `kb-index` — rebuild navigation indexes

This maps to `kb-orchestrator` build mode with Obsidian as the source.

## Integration Points

### Obsidian Skills Used

| Skill | Purpose in Bridge |
|-------|-------------------|
| `obsidian-setup` | Verify CLI readiness before any workflow |
| `obsidian-files` | Read note content, create notes from KB output |
| `obsidian-search` | Discover notes matching KB topic criteria |
| `obsidian-notes` | Query tags, properties, tasks for source filtering |
| `obsidian-daily` | Capture daily learnings for KB ingest |

### KB Skills Used

| Skill | Purpose in Bridge |
|-------|-------------------|
| `kb-ingest` | Add vault notes as raw sources |
| `kb-compile` | Generate wiki from ingested vault content |
| `kb-query` | Answer questions using compiled knowledge |
| `kb-lint` | Validate wiki health after vault sync |
| `kb-index` | Rebuild navigation after compilation |
| `kb-orchestrator` | Full pipeline coordination |

## Common Patterns

### Daily learning capture

```bash
# Append today's finding to daily note
obsidian daily:append content="## TIL\n- Agent memory consolidation..."

# At EOD, ingest daily note into the KB
obsidian daily:read
# → kb-ingest the output
```

### Research note → KB article

```bash
# Tag research notes for KB inclusion
obsidian tag:add file="LLM Survey" tag="kb-source"

# Later, batch-ingest all kb-source tagged notes
obsidian tags | grep kb-source
# → read each → kb-ingest → kb-compile
```

### KB-powered vault enrichment

```bash
# Query KB for connections the vault doesn't show
# → kb-query "What relates to transformer attention?"
# → Create new vault note with discovered connections
obsidian create name="Attention Connections" content="..."
```

## Directory Mapping

| Obsidian Vault Path | KB Path | Direction |
|---------------------|---------|-----------|
| `knowledge-bases/{topic}/raw/` | `raw/` | Bidirectional |
| `knowledge-bases/{topic}/wiki/` | `wiki/` | KB → Vault |
| Daily notes | `raw/daily-*.md` | Vault → KB |
| Tagged research notes | `raw/` | Vault → KB |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Vault not found` | KB vault not open in Obsidian | Open `knowledge-bases/` as vault |
| `No notes match` | Search/tag query too narrow | Broaden search or check tag spelling |
| `Ingest failed` | Content too large or malformed | Split into smaller sections |
| `Compile stale` | New sources not reflected | Re-run `kb-compile` with `--force` |
