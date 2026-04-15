---
name: wiki-company
description: >-
  Company wiki CRUD orchestrator for organization-wide official knowledge.
  Ingests verified content, compiles to interlinked wiki, lints for policy
  compliance, and manages the company tier of the LLM Wiki. Wraps kb-ingest,
  kb-compile, kb-lint with company-tier validation gates that enforce review
  requirements and trust-level standards defined in _wiki-registry.json.
  Use when the user asks to "add to company wiki", "compile company wiki",
  "lint company wiki", "company knowledge base", "official wiki update",
  "회사 위키", "공식 위키", "회사 지식 추가", "회사 위키 빌드",
  "company wiki status", "wiki-company", or any CRUD operation targeting
  organization-wide official knowledge topics.
  Do NOT use for team/domain-specific wiki operations (use wiki-team).
  Do NOT use for promoting team content to company (use wiki-promote).
  Do NOT use for personal memory operations (use memkraft skills).
  Do NOT use for individual kb-* operations without company-tier context
  (invoke kb-ingest, kb-compile, kb-lint directly).
  Korean triggers: "회사 위키", "공식 지식", "회사 위키 빌드",
  "회사 위키 린트", "공식 문서 추가".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "knowledge-base"
  tags: ["wiki", "company", "official", "knowledge-management", "llm-wiki"]
---

# Company Wiki Orchestrator

Manages the **company tier** of the LLM Wiki — organization-wide official
knowledge including policies, standards, architecture docs, brand guidelines,
legal templates, compliance records, and verified facts.

## Architecture Context

```
_wiki-registry.json  ←  source of truth for topic classification
       │
       ▼
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│  wiki-company   │────▶│  kb-ingest   │────▶│  kb-compile  │
│  (this skill)   │     │  + validate  │     │  + quality    │
└────────┬────────┘     └──────────────┘     └──────┬───────┘
         │                                          │
         │              ┌──────────────┐            │
         └─────────────▶│   kb-lint    │◀───────────┘
                        │  + policy    │
                        └──────────────┘
```

## Modes

### 1. `ingest` — Add verified content to a company topic

```
wiki-company ingest <topic> --source <url|path> [--reviewer <name>]
```

**Validation gates before ingestion:**
1. Confirm `<topic>` is listed in `_wiki-registry.json` under `company.topics`
2. If topic is NOT a company topic, reject with guidance to use `wiki-team`
3. Require `--reviewer` flag or prompt for reviewer name (audit trail)
4. Run source through standard `kb-ingest` pipeline
5. Tag raw file frontmatter with `tier: company` and `reviewed_by: <name>`

### 2. `compile` — Build/rebuild company wiki articles

```
wiki-company compile [<topic>] [--force]
```

1. If `<topic>` specified, compile only that topic; otherwise compile all company topics
2. Load company topic list from `_wiki-registry.json`
3. For each topic, invoke `kb-compile` with company-tier quality constraints:
   - Evidence diversity score must be ≥ 3 (multiple independent sources)
   - Articles must include "Compiled Truth" section with clear factual assertions
   - Cross-references to related company topics are required where applicable
4. After compilation, auto-run `kb-lint` on compiled topics

### 3. `lint` — Policy compliance check

```
wiki-company lint [<topic>] [--fix]
```

1. Run `kb-lint` on company topics with elevated thresholds:
   - Freshness: articles older than 30 days flagged as WARNING
   - Freshness: articles older than 90 days flagged as CRITICAL
   - Broken wikilinks: zero tolerance (CRITICAL)
   - Evidence timeline gaps > 60 days: WARNING
2. Check company-specific policies:
   - All articles must have `tier: company` in source frontmatter
   - Sensitive topics (legal, compliance, finance) must have `reviewed_by` metadata
   - No unverified or "WIP" content in company topics
3. Generate a compliance report with pass/fail per topic

### 4. `status` — Company wiki health overview

```
wiki-company status
```

1. List all company topics from `_wiki-registry.json`
2. For each: article count, last compile date, freshness score, lint status
3. Highlight topics with zero articles or stale content
4. Show pending promotion candidates from team wikis (if any)

### 5. `list` — List company topics

```
wiki-company list
```

Display all topics classified as company tier with brief descriptions.

## Implementation Steps

For each mode, follow this sequence:

1. **Read** `knowledge-bases/_wiki-registry.json` to get the current company topic list
2. **Validate** the target topic is in the company tier
3. **Delegate** to the appropriate `kb-*` skill with company-tier parameters
4. **Tag** all artifacts with provenance: `[OFFICIAL]` tier marker
5. **Report** results with company-tier compliance summary

## Company Topic List Reference

The canonical list of company topics is maintained in
`knowledge-bases/_wiki-registry.json` under `company.topics`.
Never hardcode topic lists — always read from the registry.

## Provenance Rules

- All company wiki content carries `[OFFICIAL]` provenance tag
- Content ingested without review is quarantined until reviewed
- Promotion from team tier requires passing `wiki-promote` gates
- Company wiki articles are the authoritative source when conflicts arise
  with team or personal memory content

## Error Handling

| Error | Action |
|-------|--------|
| Topic not in company tier | Reject, suggest `wiki-team` |
| Missing reviewer for sensitive topic | Block until reviewer provided |
| Lint critical failures after compile | Warn, do not mark as "clean" |
| Source already exists in raw/ | Skip with dedup warning |

## Integration Points

- **wiki-promote**: Receives validated team content for company ingestion
- **wiki-team**: Sibling skill for team-tier operations
- **ai-context-router**: Queries company wiki as the official facts layer
- **kb-daily-build-orchestrator**: Can trigger company wiki compilation
