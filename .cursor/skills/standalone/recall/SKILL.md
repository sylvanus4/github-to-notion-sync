---
name: recall
description: >-
  Restore cross-session context from the project's long-term memory store.
  Searches extracted session transcripts, decisions, patterns, and glossary
  using BM25, semantic, or hybrid search. Supports --summarize flag for
  LLM-powered structured Korean summaries of search results via Haiku.
  Use when the user says "recall", "what did we work on", "load context about",
  "remember when we", "prime context", "yesterday's session", "restore context",
  "이전 작업", "맥락 복원", "recall topic", "recall yesterday", "what was the decision
  about", "이전에 뭐 했지", "컨텍스트 복원", "지난 세션", "recall summarize", "요약해서
  recall", or needs to resume prior work. Do NOT use for general web search (use
  WebSearch), code search in the current codebase (use Grep/SemanticSearch), or
  creating new memory entries (update MEMORY.md directly).
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Recall: Long-Term Memory Search

Restore context from prior sessions, decisions, and patterns stored in the project's `memory/` directory.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Prerequisite

Before first use, ensure sessions have been extracted:

```bash
python scripts/memory/extract-sessions.py --verbose
python scripts/memory/build-index.py --skip-embeddings
```

## Query Routing

Classify the user's request into one of three modes:

### 1. Temporal Mode

**Triggers**: date references — e.g. "yesterday", "last week", "March 5" (Korean date phrases are listed in YAML `description` triggers)

```bash
python scripts/memory/search.py --mode temporal --date "yesterday" --top 10 --verbose
python scripts/memory/search.py --mode temporal --date "2026-03-05" --days 3 --top 10 --verbose
```

### 2. Topic Mode

**Triggers**: conceptual queries — "trading agent design", "CI/CD setup", "stock analysis", any topic name

Use BM25 first (fast). If results are insufficient (<3 results or low relevance), escalate to hybrid.

**Query expansion**: Before searching, generate 2-3 synonyms or related terms for the user's query. Run parallel BM25 searches for each variant and merge results.

```bash
# Fast BM25 search
python scripts/memory/search.py --mode bm25 "trading agent guard pipeline" --top 5 --verbose

# If BM25 results are weak, escalate to hybrid
python scripts/memory/search.py --mode hybrid "trading agent guard pipeline" --top 5 --verbose
```

### 3. Graph Mode

**Triggers**: file-session relationship queries — "which sessions touched X", "what files were modified when we worked on Y"

Read the session markdown files and filter by `files_touched` in frontmatter:

```bash
# Search sessions mentioning specific files
python scripts/memory/search.py --mode bm25 "daily_stock_check" --top 10 --json
```

Then cross-reference `files_touched` fields in the results.

## LLM-Powered Summarization (`--summarize`)

When the user requests a condensed, actionable summary instead of raw search results,
append `--summarize` to any search command. This sends results to Claude Haiku for
structured Korean summarization.

```bash
# Summarize BM25 results for a topic
python scripts/memory/search.py --mode bm25 "trading agent pipeline" --top 10 --summarize

# Summarize hybrid results
python scripts/memory/search.py --mode hybrid "release workflow" --top 5 --summarize

# Combine with temporal mode
python scripts/memory/search.py --mode temporal --date "yesterday" --top 10 --summarize
```

**Requirements**: `ANTHROPIC_API_KEY` environment variable must be set. Install `anthropic` package (`pip install anthropic`).

**Output format**: The LLM returns a structured Korean summary with:
1. 핵심 요약 (Core Summary) — cross-session synthesis
2. 세션별 주요 포인트 (Per-Session Key Points) — with session references
3. One Thing — the single most actionable next step

**When to use `--summarize`**:
- Many results (5+) that need synthesis rather than individual reading
- Context handoff between sessions where a quick overview is needed
- When the user says "요약해서 recall", "recall summarize", or "간단히 정리해줘"

**When NOT to use `--summarize`**:
- When the user needs exact file paths or raw content from specific sessions
- When debugging requires precise session timestamps
- Use `--json` for machine-readable output instead

## Output Contract

Every recall MUST end with **"One Thing"**:

After presenting search results, synthesize them into a single, concrete, actionable next step:

> **One Thing**: Based on the recalled context, the highest-leverage next action is: [specific action with file/function references]

This is not a generic summary. It must be a specific, executable next step that leverages the recalled context.

## Search Result Presentation

Format results as:

```
## Recalled Context (N results, mode: hybrid)

### [1] Session Title (2026-03-07)
- **Path**: memory/sessions/2026-03-07-1430-abc12345.md
- **Relevance**: 0.8542
- **Key content**: [2-3 sentence summary of relevant content]

### [2] ...

---

**One Thing**: [Specific next action]
```

## Memory Store Structure (3-Layer Architecture)

The recall skill searches Layer 2 and Layer 3 of the memory architecture.
Layer 1 (`MEMORY.md` pointer index) is always loaded and provides entry points.

### Layer 2 — Topic Files (read on demand for full detail)

| Source | Path | Content |
|--------|------|---------|
| Preferences | `memory/topics/preferences.md` | User prefs, doc standards, commit conventions |
| Workspace facts | `memory/topics/workspace-facts.md` | Repos, tools, infra, doc paths |
| Pipeline ops | `memory/topics/pipeline-ops.md` | Pipeline protocols, today/google-daily/git-sync |
| Trading stack | `memory/topics/trading-stack.md` | Agent desk, MiroFish, Toss/KIS/Kiwoom |
| Slack routing | `memory/topics/slack-routing.md` | Channel IDs, routing rules |
| Skill ecosystem | `memory/topics/skill-ecosystem.md` | Skill registry, reorganization, harness |
| Runbooks | `memory/topics/runbooks.md` | Operational procedures |
| Tech debt | `memory/topics/tech-debt.md` | Known debt, structural issues |
| Decisions | `memory/decisions.md` | Architecture/tool/pattern choices |
| Patterns | `memory/patterns.md` | Recurring failure/success patterns |
| Glossary | `memory/glossary.md` | Project-specific terms and acronyms |

### Layer 3 — Transcripts & Archive (grep/BM25 only, never loaded directly)

| Source | Path | Content |
|--------|------|---------|
| Sessions | `memory/sessions/*.md` | Auto-extracted user messages from agent transcripts |
| Archive | `memory/archive/*.md` | COLD-tier entries (attention decay < 0.3) |

## Incremental Update

If the user starts a new session and wants fresh context, run extraction first:

```bash
python scripts/memory/extract-sessions.py --incremental --verbose
python scripts/memory/build-index.py --skip-embeddings
```

The `--incremental` flag only processes transcripts not yet in `memory/.cache/processed.txt`.
Hash deduplication automatically skips sessions with identical content.

### Memory Maintenance

After extraction, optionally run maintenance to keep the pointer index lean:

```bash
python scripts/memory/attention_decay.py --apply
```

This prunes COLD entries (attention < 0.3) from `MEMORY.md` to `memory/archive/`.

## Integration with Session Lifecycle

- **Session start**: Use `/recall` with a relevant topic to prime context before work begins
- **Session end**: The done-checklist rule triggers extraction automatically
- **Context handoff**: When splitting a long conversation, use `/recall` in the new session to restore state

## Examples

### Example 1: Standard usage
**User says:** "recall" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
