---
name: knowledge-daily-aggregator
description: >-
  End-of-day pipeline that collects all daily outputs (email summaries, sprint
  digests, news analyses, meeting notes, code reviews, strategy briefings),
  ingests them into the Cognee knowledge graph, extracts new entities and
  relationships, and updates MEMORY.md. Use when the user asks to "aggregate
  today's knowledge", "daily knowledge sync", "지식 그래프 갱신",
  "일일 지식 종합", "knowledge-daily-aggregator", or wants to consolidate
  the day's learning into persistent memory. Do NOT use for Cognee operations
  directly (use cognee), context recall (use recall), or MEMORY.md manual
  updates (update directly).
metadata:
  version: "1.1.0"
  category: "execution"
  author: "thaki"
---
# Knowledge Daily Aggregator

End-of-day pipeline that consolidates all daily outputs into the Cognee knowledge graph, building persistent organizational memory.

## Implementation

This skill is fully implemented as a Python script:

```bash
python scripts/knowledge_daily_aggregator.py --date YYYY-MM-DD
```

The script handles all 7 phases (collect → extract → cognee ingest → entity resolution → MEMORY.md update → KB wiki routing → report) and produces structured JSON output in `outputs/knowledge-daily-aggregator/{date}/`.

**Prerequisites**: `pip install cognee fastembed`, `.env` with `ANTHROPIC_API_KEY`, Cognee configured for Claude API (`LLM_PROVIDER=anthropic`, `LLM_MODEL=claude-sonnet-4-6`) + FastEmbed embeddings (see `.env.example`).

## When to Use

- As Phase 1 of `daily-pm-orchestrator` (evening pipeline)
- As part of the Execute → Learn → Evolve flywheel (Learn phase)
- When the user wants to consolidate a day's worth of work into searchable knowledge

## Data Sources

| Source | Skill That Generates It | Content Type |
|--------|------------------------|--------------|
| Email summaries | `gmail-daily-triage` | People, decisions, action items |
| Sprint digests | `github-sprint-digest` | Issues, PRs, contributors, progress |
| News analyses | `unified-intel-intake` | Companies, technologies, trends |
| Meeting notes | `meeting-digest` | Decisions, attendees, action items |
| Code reviews | `deep-review`, `ship` | Architecture patterns, tech debt |
| Strategy briefings | `daily-strategy-post` | Strategic insights, market signals |
| Paper reviews | `paper-review` | Research concepts, methods, findings |
| Trading analysis | `daily-stock-check` | Market signals, positions, theses |

## Configuration

No separate config file is required beyond: MCP access as needed (Slack, Notion), Cognee runtime per the `cognee` skill, and repository write access for `outputs/` and `MEMORY.md`. Run output layout follows **Pipeline Output Protocol (File-First)** below.

## Pipeline Output Protocol (File-First)

All multi-phase work uses a **date-partitioned run directory**. Subagents and main agent stages MUST persist structured results to disk; downstream phases read **only** those files (and `manifest.json`), not conversational memory.

### Output directory

```
outputs/knowledge-daily-aggregator/{date}/
```

Use `{date}` in `YYYY-MM-DD` (authoritative calendar date for the aggregation run).

### Phase files

Each pipeline phase writes exactly one JSON artifact:

```
outputs/knowledge-daily-aggregator/{date}/phase-{N}-{label}.json
```

| Phase | N | label | Example filename |
| ----- | - | ----- | ---------------- |
| Collect daily outputs | 1 | `collect` | `phase-1-collect.json` |
| Extract structured data | 2 | `extract` | `phase-2-extract.json` |
| Ingest into Cognee | 3 | `cognee` | `phase-3-cognee.json` |
| Entity resolution | 4 | `entity-resolution` | `phase-4-entity-resolution.json` |
| Update MEMORY.md | 5 | `memory` | `phase-5-memory.json` |
| Knowledge report | 6 | `report` | `phase-6-report.json` |

### Manifest

`manifest.json` lives beside the phase files and is the **single index** of completed phases and artifact paths.

### Subagent return contract

When a subagent performs part of a phase, it returns **only** this object (no full payloads in chat):

```json
{
  "status": "completed | failed | skipped",
  "file": "outputs/knowledge-daily-aggregator/{date}/phase-{N}-{label}.json",
  "summary": "One short sentence: row counts, paths, or error code."
}
```

The orchestrator merges subagent work into the phase JSON file using the Write tool; the subagent does not rely on the parent retaining large text in context.

### Final summary and reporting

Phases that produce the **daily knowledge report** (Step 6) MUST load inputs **exclusively** from:

- `manifest.json`
- `phase-1-collect.json` through `phase-5-memory.json` (and any prior phase files referenced in the manifest)

Do **not** reconstruct the report from uncached chat history or unstored model output.

### `manifest.json` schema

Top-level object:

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `skill` | string | yes | Always `"knowledge-daily-aggregator"`. |
| `date` | string | yes | Run date `YYYY-MM-DD`. |
| `runId` | string | no | Optional UUID or idempotency key for reruns. |
| `createdAt` | string | yes | ISO 8601 timestamp when the run directory was initialized. |
| `updatedAt` | string | yes | ISO 8601 timestamp of last manifest write. |
| `phases` | array | yes | Ordered list of phase records (see below). |

Each element of `phases`:

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `phase` | number | yes | Phase number (1–6). |
| `label` | string | yes | Short slug matching the filename segment (e.g. `collect`). |
| `file` | string | yes | Relative path from repo root: `outputs/knowledge-daily-aggregator/{date}/phase-{N}-{label}.json`. |
| `status` | string | yes | One of: `pending`, `running`, `completed`, `failed`, `skipped`. |
| `summary` | string | no | Brief outcome; mirrors or extends the phase file’s own summary field if present. |
| `completedAt` | string | no | ISO 8601 when status became terminal (`completed`, `failed`, or `skipped`). |

Example:

```json
{
  "skill": "knowledge-daily-aggregator",
  "date": "2026-04-01",
  "runId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "createdAt": "2026-04-01T18:00:00Z",
  "updatedAt": "2026-04-01T18:22:00Z",
  "phases": [
    {
      "phase": 1,
      "label": "collect",
      "file": "outputs/knowledge-daily-aggregator/2026-04-01/phase-1-collect.json",
      "status": "completed",
      "summary": "18 artifact paths collected",
      "completedAt": "2026-04-01T18:05:00Z"
    }
  ]
}
```

## Output Artifacts

| Phase | Stage | Output file | Notes |
| ----- | ----- | ----------- | ----- |
| 1 | Collect | `outputs/knowledge-daily-aggregator/{date}/phase-1-collect.json` | File list, Slack/Notion/git refs |
| 2 | Extract | `outputs/knowledge-daily-aggregator/{date}/phase-2-extract.json` | Entities, relationships, decisions, learnings, actions |
| 3 | Cognee | `outputs/knowledge-daily-aggregator/{date}/phase-3-cognee.json` | Ingest job ids, dataset name, errors |
| 4 | Entity resolution | `outputs/knowledge-daily-aggregator/{date}/phase-4-entity-resolution.json` | Merge map, dedupe stats |
| 5 | MEMORY.md | `outputs/knowledge-daily-aggregator/{date}/phase-5-memory.json` | Paths/lines appended or diff summary |
| 5.5 | KB Router | `outputs/knowledge-daily-aggregator/{date}/phase-5.5-kb-router.json` | topics_routed map, artifacts_classified, duplicates skipped |
| 6 | Report | `outputs/knowledge-daily-aggregator/{date}/phase-6-report.json` | Structured report + optional plain text path |

Index file: `outputs/knowledge-daily-aggregator/{date}/manifest.json`.

## Workflow

### Initialization (run once per `{date}`)

1. Create the run directory: `outputs/knowledge-daily-aggregator/{date}/`.
2. Write an initial `manifest.json` with `skill`, `date`, `createdAt` = `updatedAt` = now (ISO 8601), and `phases` containing six entries (phase 1–6) each with `status`: `"pending"` and the correct `file` paths.
3. Proceed to Step 1; after each phase completes, update `manifest.json` (`updatedAt`, phase `status`, `summary`, `completedAt`).

### Step 1: Collect Daily Outputs

Scan for today's generated artifacts (project convention: under `outputs/`):

```bash
find outputs/ -name "*.md" -newer .knowledge-aggregator-last-run -type f
find outputs/ -name "*.docx" -newer .knowledge-aggregator-last-run -type f
```

Also collect from:
- Slack messages posted today (via Slack MCP search)
- Notion pages updated today (via Notion MCP)
- Git commit messages from today

**Persist & manifest:** Write `outputs/knowledge-daily-aggregator/{date}/phase-1-collect.json` with structured fields (e.g. `artifactPaths`, `slackRefs`, `notionRefs`, `gitCommitSummary`, `scanNotes`, `collectedAt`). Update `manifest.json`: set phase 1 `status` to `completed` (or `skipped` if nothing to process), `summary`, and `completedAt`.

### Step 2: Extract Structured Data

For each artifact, extract:
- **Entities**: People, companies, technologies, products, papers
- **Relationships**: "works at", "competes with", "depends on", "cited by"
- **Decisions**: Key decisions made today with rationale
- **Learnings**: New insights, patterns discovered, corrections received
- **Action items**: Outstanding tasks with owners and deadlines

**Persist & manifest:** Write `phase-2-extract.json` with `entities`, `relationships`, `decisions`, `learnings`, `actionItems`, and any per-artifact extraction metadata. Inputs for extraction MUST be driven from paths and content references recorded in `phase-1-collect.json`. Update `manifest.json` for phase 2.

### Step 3: Ingest into Cognee

Use the `cognee` skill to add extracted content. **Python SDK approach** (shown below); CLI alternative: `cognee add <path>` and `cognee cognify`.

```python
cognee.add(text_content, dataset_name="daily-{date}")
cognee.cognify()
```

The knowledge graph grows incrementally — new entities connect to existing ones, relationships strengthen with repeated mentions.

**Persist & manifest:** Write `phase-3-cognee.json` with `datasetName`, `ingestAttempts`, `errors`, `cognifyStatus`, and references to source chunks or paths. Base ingestion on structured content from `phase-2-extract.json`, not on uncached chat. Update `manifest.json` for phase 3.

### Step 4: Entity Resolution

Deduplicate and merge entities:
- "NVIDIA" / "Nvidia" / "nvidia" → single entity
- "@user1" / "John Doe" / "john@company.com" → single person entity
- Merge new information into existing entity profiles

**Persist & manifest:** Write `phase-4-entity-resolution.json` with `canonicalEntities`, `mergeMap`, `dedupeStats`, and `warnings`. Source inputs MUST be read from `phase-2-extract.json` (and `phase-3-cognee.json` if needed for graph ids). Update `manifest.json` for phase 4.

### Step 5: Update MEMORY.md

Append significant learnings to MEMORY.md:

```markdown
## [2026-03-19]

### [decision] Adopted vLLM over TGI for inference serving
- Context: Paper review of vLLM benchmark results
- Rationale: 2x throughput on H100, better batching

### [task] Migrate K8s manifests from v1beta1 to v1
- Source: IaC review finding
- Owner: @infra-team
- Deadline: Sprint 14

### [issue] Helm chart values not schema-validated
- Source: helm-validator finding
- Fix: Add values.schema.json to all charts
```

**Persist & manifest:** Write `phase-5-memory.json` with `memoryPath` (e.g. `MEMORY.md`), `entriesAppended`, `sectionAnchors` or diff summary, and `warnings`. Update `manifest.json` for phase 5.

### Step 5.5: Route to LLM Wiki (KB Daily Router)

Route today's collected artifacts to the 9-topic LLM Knowledge Base for long-term compound growth. Invoke the `kb-daily-router` skill (or `python scripts/kb_daily_router.py --date {date}`) to classify and ingest outputs into `knowledge-bases/{topic}/raw/`.

1. Read `phase-1-collect.json` for the artifact list
2. Classify each artifact by topic using keyword matching against the 9-topic taxonomy (trading-daily, trading-strategy, ai-research, intelligence, tech-trends, ai-knowledge-bases, product-platform, architecture-ops, skill-ecosystem)
3. Deduplicate against existing raw files in each topic's `raw/` directory via `_log.md`
4. Ingest new artifacts with YAML frontmatter (date_published, ingested, staleness_flag, kb_topic)
5. Log routing results

**Persist & manifest:** Write `phase-5.5-kb-router.json` with `topics_routed` (map of topic to count), `artifacts_classified`, `artifacts_skipped_duplicate`, and `errors`. Update `manifest.json` for phase 5.5.

### Step 6: Generate Knowledge Report

**Input rule:** Build this step **only** from on-disk artifacts:

- Read `outputs/knowledge-daily-aggregator/{date}/manifest.json`
- Read `phase-1-collect.json` through `phase-5.5-kb-router.json` in the same directory

Do **not** restate counts, learnings, or graph metrics from prior chat turns unless they are reproduced by parsing these files. If a field is missing in a phase file, record `null` or `"unknown"` in `phase-6-report.json` and note the gap in `summary`.

Produce a human-readable report body (example shape below) whose numbers and bullets are **derived from** the JSON phase files:

```
Daily Knowledge Aggregation
============================
Date: 2026-03-19

Sources Processed: 15
  Emails: 3 summaries
  Sprint: 1 digest (12 issues, 5 PRs)
  News: 8 articles
  Meetings: 2 digests
  Reviews: 1 deep-review

Knowledge Graph Updates:
  New entities: 12
  New relationships: 28
  Updated entities: 45
  Total graph size: 2,847 entities, 8,432 relationships

Key Learnings:
1. vLLM shows 2x throughput advantage over TGI on H100
2. Kubernetes 1.30 removes batch/v1beta1 — migration needed
3. Samsung exploring on-prem inference deployment

MEMORY.md entries added: 3
KB articles routed: 12 (trading-daily: 4, ai-research: 3, intelligence: 2, architecture-ops: 1, tech-trends: 1, skill-ecosystem: 1)
```

Optional: if posting to Slack or another channel, compose the message **only** from `phase-6-report.json` (or a path recorded there), not from undocumented context.

**Persist & manifest:** Write `phase-6-report.json` with `reportMarkdown` or `reportText`, `sourcePhaseFiles` (list of inputs used), `metrics` (copied or aggregated from prior phases), and `slackPosted` / `channel` if applicable. Update `manifest.json` for phase 6 (terminal phase).

## Error Handling

| Error | Action |
|-------|--------|
| No outputs generated today | Set phase 1 `status` to `skipped` in `manifest.json`, write `phase-1-collect.json` with empty lists; log "no sources to process" and exit cleanly (downstream phases skip or no-op per policy) |
| Cognee service unavailable | Retry with exponential backoff (3 attempts); if still failing, persist extracted data to `outputs/knowledge-pending/{date}/` **and** record failure in `phase-3-cognee.json`; set manifest phase 3 `failed` |
| File too large for ingestion | Chunk the document into smaller segments (≤50KB each) and ingest sequentially; record chunk ids in `phase-3-cognee.json` |
| Duplicate document detected | Skip ingestion; update entity metadata with new mention count; log deduplication in `phase-3-cognee.json` or `phase-4-entity-resolution.json` |
| Knowledge graph build timeout | Persist partial state in `phase-3-cognee.json`; resume from last successful batch on next run using `manifest.json` + phase files |
| Mid-pipeline failure | Do not rely on chat context: last good checkpoint is the most recent `completed` phase in `manifest.json`; re-run from the failed phase after fixing the cause |

## Examples

### Example 1: End-of-day aggregation
Automated trigger: EOD pipeline
Actions:
1. Initialize `outputs/knowledge-daily-aggregator/{date}/` and `manifest.json`
2. Collect all daily outputs → `phase-1-collect.json`; update manifest
3. Extract entities and relationships → `phase-2-extract.json`; update manifest
4. Ingest into Cognee KG → `phase-3-cognee.json`; update manifest
5. Entity resolution → `phase-4-entity-resolution.json`; update manifest
6. Update MEMORY.md → `phase-5-memory.json`; update manifest
7. Route artifacts to LLM Wiki via kb-daily-router → `phase-5.5-kb-router.json`; update manifest
8. Generate report from phase JSON files only → `phase-6-report.json`; update manifest
Result: Day's knowledge consolidated into persistent graph + LLM Wiki with a full file trail under `outputs/knowledge-daily-aggregator/{date}/`

### Example 2: Retroactive aggregation
User says: "Aggregate knowledge from last 3 days"
Actions:
1. For each calendar date in range, use a separate `outputs/knowledge-daily-aggregator/{date}/` directory (or one run with `date` = range end and embed per-day slices in phase files — document the chosen convention in `phase-1-collect.json`)
2. Scan artifacts from past 72 hours; persist paths to `phase-1-collect.json`
3. Process in chronological order; advance manifest phases per day or per batch as defined
4. Build temporal knowledge chain; final report in `phase-6-report.json` must aggregate **only** from phase files on disk
Result: Multi-day knowledge consolidation with trend detection and auditable manifests


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
