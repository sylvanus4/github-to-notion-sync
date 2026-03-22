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
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Knowledge Daily Aggregator

End-of-day pipeline that consolidates all daily outputs into the Cognee knowledge graph, building persistent organizational memory.

## When to Use

- As the final step in the EOD pipeline (after `eod-ship`, before daily-strategy-post)
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

## Workflow

### Step 1: Collect Daily Outputs

Scan for today's generated artifacts:

```bash
find output/ -name "*.md" -newer .knowledge-aggregator-last-run -type f
find output/ -name "*.docx" -newer .knowledge-aggregator-last-run -type f
```

Also collect from:
- Slack messages posted today (via Slack MCP search)
- Notion pages updated today (via Notion MCP)
- Git commit messages from today

### Step 2: Extract Structured Data

For each artifact, extract:
- **Entities**: People, companies, technologies, products, papers
- **Relationships**: "works at", "competes with", "depends on", "cited by"
- **Decisions**: Key decisions made today with rationale
- **Learnings**: New insights, patterns discovered, corrections received
- **Action items**: Outstanding tasks with owners and deadlines

### Step 3: Ingest into Cognee

Use the `cognee` skill to add extracted content. **Python SDK approach** (shown below); CLI alternative: `cognee add <path>` and `cognee cognify`.

```python
cognee.add(text_content, dataset_name="daily-{date}")
cognee.cognify()
```

The knowledge graph grows incrementally — new entities connect to existing ones, relationships strengthen with repeated mentions.

### Step 4: Entity Resolution

Deduplicate and merge entities:
- "NVIDIA" / "Nvidia" / "nvidia" → single entity
- "@user1" / "John Doe" / "john@company.com" → single person entity
- Merge new information into existing entity profiles

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

### Step 6: Generate Knowledge Report

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
```

## Error Handling

| Error | Action |
|-------|--------|
| No outputs generated today | Skip aggregation; log "no sources to process" and exit cleanly |
| Cognee service unavailable | Retry with exponential backoff (3 attempts); if still failing, save extracted data to `output/knowledge-pending/` for manual ingestion later |
| File too large for ingestion | Chunk the document into smaller segments (≤50KB each) and ingest sequentially |
| Duplicate document detected | Skip ingestion; update entity metadata with new mention count; log deduplication |
| Knowledge graph build timeout | Persist partial state; resume from last successful entity batch on next run |

## Examples

### Example 1: End-of-day aggregation
Automated trigger: EOD pipeline
Actions:
1. Collect all daily outputs
2. Extract entities and relationships
3. Ingest into Cognee KG
4. Update MEMORY.md
5. Generate report
Result: Day's knowledge consolidated into persistent graph

### Example 2: Retroactive aggregation
User says: "Aggregate knowledge from last 3 days"
Actions:
1. Scan artifacts from past 72 hours
2. Process in chronological order
3. Build temporal knowledge chain
Result: Multi-day knowledge consolidation with trend detection
