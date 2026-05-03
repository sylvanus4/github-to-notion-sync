---
name: kb-query
description: >-
  Ask complex questions against an LLM Knowledge Base wiki and get researched,
  citation-backed answers. The agent reads the index to identify relevant
  articles, deep-reads those articles, synthesizes an answer, and optionally
  files the result back into the wiki. Use when the user asks to "query the
  KB", "ask the knowledge base", "kb query", "research in KB", "what does the
  KB say about", "search my wiki", or wants answers derived from their curated
  sources. Do NOT use for web search (use WebSearch or parallel-web-search).
  Do NOT use for simple file reading (use Read tool directly). Do NOT use for
  adding new sources (use kb-ingest). Korean triggers: "KB 질문", "지식베이스 질문",
  "위키 검색", "KB 쿼리", "지식베이스에서 찾아줘".
---

# KB Query — Knowledge Base Q&A

Research complex questions against your LLM-maintained wiki. The agent navigates the KB using index files, reads relevant articles, synthesizes answers with citations, and optionally archives results back into the wiki.

## Core Approach

Two complementary retrieval strategies:

1. **SQLite FTS5 + Vector** (primary): When `brain_index.db` exists, use `kb_search.py` for fast FTS5 or hybrid search to identify relevant articles. Scales to hundreds of articles with sub-second retrieval.
2. **Index-file scan** (fallback): Read lightweight `_index.md` (~2-5K tokens) and match question keywords against summaries. Works without any DB.

At scales up to ~100 articles and ~400K words, both approaches work well. The SQLite path is preferred for precision and speed.

## Prerequisites

- Wiki must exist at `knowledge-bases/{topic}/wiki/`
- For best results: `brain_index.db` built via `python scripts/kb_index_db.py --rebuild`
- Index files should be current (run kb-index if stale)

## Input

The user provides:

1. **Topic name** — which KB to query
2. **Question** — natural language question

Optional:
- `--no-file-back` — skip archiving the answer into the wiki (default: auto file-back is ON)
- `--deep` — read all potentially relevant articles, not just top matches
- `--with-sources` — include raw source excerpts in the answer
- `--with-cognee` — cross-system query: search both Karpathy KB and Cognee knowledge graph, merge results via Reciprocal Rank Fusion (RRF)

## Workflow

### Step 0: Read Schema (MANDATORY)

Before any query, read `_schema.md` from the KB root directory. Extract:

- **Conventions**: language, terminology, answer structure preferences
- **Quality Gates**: citation requirements, confidence thresholds, contradiction handling policy
- **Domain Rules**: topic-specific constraints that affect answer synthesis (e.g., "always distinguish between supervised and unsupervised approaches")
- **File-back Rules**: required frontmatter fields for query articles, naming conventions for `queries/` directory

If `_schema.md` does not exist, warn the user and suggest running `kb-orchestrator init` first. Proceed with defaults if the user chooses to continue.

### Step 1: Identify Relevant Articles

Use the best available retrieval method:

#### Path A — SQLite FTS5/Hybrid (preferred)

If `brain_index.db` exists, run FTS5 or hybrid search:

```bash
python scripts/kb_search.py "{question}" --mode auto --json --top 10
```

This returns ranked results with file paths, scores, and snippets. For conceptual queries, use `--mode hybrid` when vector embeddings are available.

#### Path B — Index File Scan (fallback)

If no SQLite index, read `knowledge-bases/{topic}/wiki/_index.md` to get the article inventory:

1. Match question keywords against article titles and summaries
2. Follow `related` links to find connected articles
3. Check `_glossary.md` for term definitions
4. Rank articles by relevance

Typically 3-8 articles are sufficient for most queries.

### Step 2: Deep Read

Read the identified articles in full. For each article, note:
- Key facts relevant to the question
- Citations and source references
- Connections to other concepts
- Gaps or uncertainties

### Step 3: Synthesize Answer

Compose a comprehensive answer following this structure:

```markdown
## Answer

[Direct, clear answer to the question]

### Details

[Supporting analysis with specific references]

### Evidence

- From [[concept-1]]: "relevant excerpt or finding"
- From [[concept-2]]: "relevant excerpt or finding"

### Connections

[How different KB articles relate to this question]

### Limitations

[What the KB doesn't cover, uncertainties, potential gaps]

### Sources

- [[concept-1]] — primary source for [aspect]
- [[reference-notes-2]] — supporting data for [aspect]
```

### Step 4: File Back into Wiki (Schema-Gated)

By default, every query answer is automatically archived into the wiki. This implements the Karpathy feedback loop where explorations and queries "always add up" in the knowledge base. Use `--no-file-back` to skip this step.

**Quality Gate**: Before filing back, validate the answer against schema quality gates:

1. **Minimum citations** — answer must reference at least N wiki articles (default: 1, configurable via schema)
2. **Confidence threshold** — if confidence is "low" and schema requires "medium" minimum, flag for human review instead of auto-filing
3. **Frontmatter compliance** — the filed article must have all schema-required frontmatter fields
4. **Layer separation** — file-back articles go into `wiki/queries/` (Layer 2), NEVER into `raw/` (Layer 1)

If the quality gate fails, present the answer to the user but log `QUERY-FILE-BACK-BLOCKED` instead of filing.

Save the answer as a new article:

```
knowledge-bases/{topic}/wiki/queries/{question-slug}.md
```

With frontmatter (read template from `_schema.md`, fall back to defaults):

```yaml
---
title: "Q: {question}"
category: "queries"
related: ["concept-1", "concept-2"]
sources_consulted: ["concept-1.md", "reference-2.md"]
confidence: "high"  # high | medium | low
date: "2026-04-03"
---
```

Then run kb-index to update the index with the new article.

### Step 5: Report

Present the answer to the user with:
- The synthesized answer
- List of articles consulted
- Confidence level (high/medium/low based on source coverage)
- Suggestions for follow-up queries

## Multi-Hop Queries

For complex questions requiring multi-step reasoning:

1. Decompose the question into sub-questions
2. Research each sub-question against the KB
3. Synthesize sub-answers into the final answer
4. Highlight where the chain of reasoning crosses concept boundaries

## Query Patterns

| Pattern | Example | Strategy |
|---------|---------|----------|
| Factual lookup | "What is X?" | Read glossary + concept article |
| Comparison | "How does X differ from Y?" | Read both concepts + connection articles |
| Synthesis | "What are the key themes?" | Read `_summary.md` + top concepts |
| Gap analysis | "What's missing in our understanding?" | Read `_summary.md` + lint report |
| Historical | "How has X evolved?" | Read chronological sources |
| Cross-cutting | "How do X, Y, Z interact?" | Read all three + connections |

## Examples

### Example 1: Simple concept query

**User says:** "What does the transformer KB say about positional encoding?"

**Actions:**
1. Read `_index.md` for the transformer KB
2. Find `[[positional-encoding]]` article
3. Read the article
4. Present a summary with citations

### Example 2: Complex synthesis query

**User says:** "Based on my ML KB, what are the 3 most promising research directions?"

**Actions:**
1. Read `_index.md` and `_summary.md`
2. Read top 10 concept articles by interconnectedness
3. Synthesize themes and identify frontier areas
4. Present ranked recommendations with evidence

### Example 3: File-back query (default behavior)

**User says:** "Query the diffusion KB: how do classifier-free and classifier guidance compare?"

**Actions:**
1. Research the question against the KB
2. Present the answer to the user
3. **File-back is ON by default**: Write synthesized answer to `wiki/queries/classifier-free-vs-classifier-guidance.md` with proper frontmatter, citations, and `[[wikilinks]]`
4. Run kb-index to update indexes
5. Append to `_log.md`: `QUERY: "{question}" → filed to wiki/queries/{slug}.md`
6. Report the filed location

To skip file-back, user must explicitly say "don't file back" or pass `--no-file-back`.

### Answer Output Formats

Queries can produce answers in multiple formats depending on the question type:

| Question Type | Default Output | Alternative Outputs |
|---------------|----------------|---------------------|
| Factual | Markdown article | Bullet summary |
| Comparison | Comparison table | Pros/cons list |
| Synthesis | Thematic essay | Mermaid concept map |
| Timeline | Chronological list | Timeline diagram |
| Decision | Decision matrix | Recommendation brief |

The LLM should choose the most natural format for the question. User can override with explicit instructions.

## Operations Log

After every query, append to `_log.md` using the **grep-parseable H2 heading format** (never overwrite or truncate):

```markdown
## [2026-04-03 17:00] QUERY | "How does attention differ from convolution?" | articles_read: 4 | confidence: high | → wiki/queries/attention-vs-convolution.md

## [2026-04-03 17:05] QUERY | "What are the key themes?" | articles_read: 8 | confidence: medium | file-back: blocked (low confidence)
```

Format: `## [YYYY-MM-DD HH:MM] QUERY | question | articles_read | confidence | → destination_or_status`

If schema-related issues are detected (e.g., missing domain terminology, answer structure doesn't match schema conventions), append a co-evolution suggestion:

```markdown
## [2026-04-03 17:10] SCHEMA-SUGGEST | source: kb-query | rule: "Add 'queries' category to required frontmatter fields" | status: pending-review
```

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No schema | `_schema.md` missing | Warn user, suggest `kb-orchestrator init`, proceed with defaults |
| Schema parse error | Malformed `_schema.md` | Report parse error, fall back to defaults |
| No index file | `_index.md` missing | Run kb-index first |
| No relevant articles | Question doesn't match any KB content | Report "not covered" + suggest kb-ingest |
| Stale index | Index date much older than newest article | Run kb-index, then re-query |
| Contradictory sources | Different articles disagree | Present both views with citations |

## Unified Cross-System Query (`--with-cognee`)

When `--with-cognee` is passed, the query spans both the Karpathy KB (FTS5 + vector) and the Cognee knowledge graph, merging results via Reciprocal Rank Fusion (RRF). This is powered by `scripts/kb_unified_query.py`.

### How it works

1. **Karpathy KB** search via `brain_index.db` (FTS5 + optional vector embeddings)
2. **Cognee** search via `cognee.search(SearchType.CHUNKS, ...)`
3. Results from both sources are merged using **RRF (k=60)** — items appearing in multiple ranked lists receive a boosted score
4. Either system can be unavailable — the query degrades gracefully and returns results from whichever source is working

### CLI usage

```bash
python scripts/kb_unified_query.py "query text" --sources all --top 10 --json
python scripts/kb_unified_query.py "query text" --sources kb         # KB only
python scripts/kb_unified_query.py "query text" --sources cognee     # Cognee only
python scripts/kb_unified_query.py "query text" --context-lines 3    # snippet context
```

### Pipeline integration

The unified query layer is consumed by:

- **`today` Phase 4.9** — enriches the daily report with historical patterns from KB
- **`daily-pm-orchestrator` Phase 1.8** — grounds strategic analysis in prior decisions
- **`kb_mcp_server.py`** — exposes `brain_search` and `brain_query` as MCP tools with auto-rebuild resilience

### Graceful degradation

| Scenario | Behavior |
|----------|----------|
| Cognee not installed (`ModuleNotFoundError`) | KB-only results returned, warning logged |
| `brain_index.db` missing | Auto-rebuild attempted; if fails, Cognee-only results |
| Both unavailable | Empty results with warnings |
| Network timeout on Cognee | 30s timeout, fall back to KB results |

## Obsidian CLI Integration

Use `obsidian-kb-bridge` to query the KB from the current vault context —
reads the active note to formulate questions automatically.
