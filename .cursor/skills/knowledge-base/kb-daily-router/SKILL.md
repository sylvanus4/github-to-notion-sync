---
name: kb-daily-router
description: >-
  Classify daily pipeline outputs by topic and route them to the correct
  Karpathy-style Markdown Knowledge Base for ingestion. Reads source artifacts,
  applies keyword/pattern-based topic classification, and invokes kb-ingest per
  routed file. Supports configurable topic registry, deduplication via _log.md,
  and dry-run mode. Use when the user asks to "route daily outputs to KB",
  "classify outputs", "KB 라우팅", "일일 산출물 분류", "kb-daily-router",
  "topic routing", "outputs to knowledge base", "산출물 KB 인제스트",
  "파이프라인 결과 KB 라우팅", or when invoked programmatically by
  knowledge-daily-aggregator (Step 5.5) or daily-pm-orchestrator (Phase 1a).
  Do NOT use for KB compilation (use kb-compile). Do NOT use for KB querying
  (use kb-query). Do NOT use for manual single-file ingest without routing
  (use kb-ingest directly). Do NOT use for Cognee knowledge graph operations
  (use cognee).
  Korean triggers: "KB 라우팅", "일일 산출물 분류", "산출물 KB 인제스트",
  "파이프라인 결과 KB 라우팅", "토픽 분류", "KB 자동 분류".
metadata:
  author: "thaki"
  version: "1.0.0"
  tags: ["knowledge-base", "kb-integration", "three-layer", "routing"]
  category: "knowledge-base"
---

# KB Daily Router — Topic Classification & Routing

Automatically classify daily pipeline outputs and route them to the correct
Karpathy-style Markdown Knowledge Base topic for ingestion.

## Architecture

```
Pipeline outputs (outputs/{pipeline}/{date}/)
  ↓
kb-daily-router (classify → route → ingest)
  ↓
knowledge-bases/{topic}/raw/daily-{date}-{source}.md
```

## Topic Registry

The router maintains a configurable topic registry. Each topic maps keywords,
file patterns, and pipeline sources to a KB topic directory.

### Default Topics (9-Topic Taxonomy)

| Topic ID | KB Path | Sources | Keywords |
|---|---|---|---|
| `trading-daily` | `knowledge-bases/trading-daily/` | `outputs/today/`, `outputs/toss/`, `outputs/daily/`, `outputs/reports/` | stock, trading, signal, screener, bollinger, turtle, RSI, MACD, daily-report, market-breadth |
| `trading-strategy` | `knowledge-bases/trading-strategy/` | `outputs/mirofish/` | mirofish, simulation, swarm, scenario, strategy, backtest, position-size, edge-candidate |
| `ai-research` | `knowledge-bases/ai-research/` | `outputs/paper-review/`, `outputs/hf-trending/`, paper archive | paper, model, benchmark, arxiv, huggingface, LLM, transformer, fine-tune, training |
| `intelligence` | `knowledge-bases/intelligence/` | `outputs/intel/`, `outputs/x-to-slack/`, `outputs/twitter/`, `outputs/bespin-news-digest/`, `outputs/google-daily/` | intel, news, tweet, press, bespin, google-daily, email, triage, calendar, decision |
| `tech-trends` | `knowledge-bases/tech-trends/` | `outputs/tech-trends/`, `outputs/hf-trending/`, `outputs/carbonyl-analysis/` | trend, open-source, framework, tool, startup, funding, leaderboard, ranking |
| `ai-knowledge-bases` | `knowledge-bases/ai-knowledge-bases/` | `outputs/axis/`, `outputs/research/` | axis, knowledge-base, kb, learning, curriculum, deep-learn, research-pipeline |
| `product-platform` | `knowledge-bases/product-platform/` | `outputs/role-analysis/`, `outputs/sentinel/` | role, strategy, platform, product, OKR, roadmap, stakeholder, PRD |
| `architecture-ops` | `knowledge-bases/architecture-ops/` | `outputs/daily-pm/`, `outputs/eod/`, `outputs/pipeline-state/`, `outputs/sprint/` | sprint, commit, PR, deploy, CI, release, incident, pipeline, eod, shipping |
| `skill-ecosystem` | `knowledge-bases/skill-ecosystem/` | `outputs/agentos-skill-ecosystem/`, `outputs/autoskill-candidates/`, `outputs/autoskill-decisions/`, `outputs/autoskill-reports/`, `outputs/skill-utilization/`, `outputs/harness-refs/` | skill, autoskill, harness, evolution, trigger, agent, orchestrator, sefo |

### Custom Topics

Add custom topics by creating `knowledge-bases/{topic}/_schema.md` with a
`## Topic Routing` section:

```markdown
## Topic Routing
keywords: ["custom", "domain", "specific"]
sources: ["outputs/custom-pipeline/"]
file_patterns: ["*-custom-*.json", "*-custom-*.md"]
```

## Workflow

### Step 0: Load Topic Registry

1. Scan `knowledge-bases/*/` for directories with `_schema.md`
2. Parse each `_schema.md` for `## Topic Routing` section
3. Merge with default topic registry (schema overrides defaults)
4. Build a unified routing table

### Step 1: Collect Source Artifacts

Scan configured output directories for today's date:

```
outputs/today/{date}/
outputs/knowledge-daily-aggregator/{date}/
outputs/daily-pm/{date}/
outputs/toss/{date}/
outputs/twitter/{date}/
outputs/paper-review/
outputs/meeting-digest/
outputs/role-analysis/
```

Collect all `.json`, `.md`, `.docx` files modified today.

### Step 2: Classify Each Artifact

For each artifact, apply classification in order of specificity:

1. **Source-path match**: If the file's parent directory matches a topic's
   `sources` list, assign that topic (highest confidence)
2. **File-pattern match**: If the filename matches a topic's `file_patterns`,
   assign that topic
3. **Keyword match**: Read the file content (first 2000 chars for large files),
   count keyword hits per topic, assign to topic with highest score
4. **Fallback**: If no topic scores above threshold (3+ keyword hits),
   assign to `intelligence` as catch-all

Output: `{ file, topic, confidence, method }` per artifact.

### Step 3: Deduplicate

For each classified artifact, check the target KB's `_log.md` for existing
ingest entries matching the same source filename or content hash:

```bash
grep "daily-{date}" knowledge-bases/{topic}/_log.md
```

Skip artifacts already ingested (log `status: "skipped-duplicate"`).

### Step 4: Route & Ingest

For each non-duplicate artifact, invoke `kb-ingest` with topic-specific parameters:

1. **Ensure KB exists**: If `knowledge-bases/{topic}/` doesn't exist, initialize
   it using `kb-orchestrator init` with default schema
2. **Read `_schema.md`**: Load the target KB's schema for frontmatter requirements
3. **Invoke `kb-ingest`**: Delegate raw file creation to `kb-ingest` with the
   classified topic path and extracted content. If `kb-ingest` is unavailable
   (e.g., programmatic context), generate the raw source file directly:
   Create
   `knowledge-bases/{topic}/raw/daily-{date}-{source-name}.md` with:
   - YAML frontmatter (per schema: `source_type`, `date`, `pipeline`, `tags`)
   - Content extracted from the artifact (JSON → readable markdown, DOCX → text)
4. **Update `_log.md`**: Append ingest entry with grep-parseable format:
   ```
   ## [YYYY-MM-DD] ingest | daily-{source-name} | routed by kb-daily-router
   ```
5. **Flag for compilation**: Add topic to `compile_flagged` list if new raw
   source count since last compile exceeds threshold (default: 3)

### Step 5: Generate Routing Report

Write `outputs/kb-daily-router/{date}/routing-report.json`:

```json
{
  "date": "2026-04-05",
  "artifacts_scanned": 15,
  "artifacts_classified": 12,
  "artifacts_skipped_duplicate": 2,
  "artifacts_unclassifiable": 1,
  "topics_routed": {
    "trading-daily": 4,
    "ai-research": 3,
    "intelligence": 2,
    "architecture-ops": 1,
    "tech-trends": 1
  },
  "compile_flagged": ["trading-daily", "ai-research"],
  "errors": []
}
```

## Dry-Run Mode

When invoked with `--dry-run`, the router classifies and reports without
writing any files. Useful for validating classification accuracy.

## Integration Points

| Caller | When | Mode |
|---|---|---|
| `knowledge-daily-aggregator` Step 5.5 | During daily pipeline | Full |
| `daily-pm-orchestrator` Phase 1a | Evening pipeline | Full |
| User manual invocation | On demand | Full or dry-run |
| `kb-auto-builder` enhance mode | Continuous enhancement | Full |

## Error Handling

| Error | Recovery |
|---|---|
| `_schema.md` missing for topic | Initialize KB with `kb-orchestrator init`, then proceed |
| File read error | Skip file, log warning, continue with remaining artifacts |
| Classification ambiguity (tie) | Route to first matching topic by registry order, log warning |
| `_log.md` parse error | Treat as no prior ingests (risk duplicate), log warning |
| Output directory missing | Create with `mkdir -p`, then proceed |

## Operations Log

Append to `knowledge-bases/_global_log.md` (project-level):

```markdown
## [YYYY-MM-DD] route | kb-daily-router | N artifacts → N topics (N flagged)
```
