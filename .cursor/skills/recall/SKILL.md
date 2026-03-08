---
name: recall
description: >-
  Restore cross-session context from the project's long-term memory store.
  Searches extracted session transcripts, decisions, patterns, and glossary
  using BM25, semantic, or hybrid search. Use when the user says "recall",
  "what did we work on", "load context about", "remember when we",
  "prime context", "yesterday's session", "restore context", "이전 작업",
  "맥락 복원", "recall topic", "recall yesterday", "what was the decision about",
  "이전에 뭐 했지", "컨텍스트 복원", "지난 세션", or needs to resume prior work.
  Do NOT use for general web search (use WebSearch), code search in the current
  codebase (use Grep/SemanticSearch), or creating new memory entries (update
  MEMORY.md directly).
metadata:
  author: thaki
  version: 1.0.0
---

# Recall: Long-Term Memory Search

Restore context from prior sessions, decisions, and patterns stored in the project's `memory/` directory.

## Prerequisite

Before first use, ensure sessions have been extracted:

```bash
python scripts/memory/extract-sessions.py --verbose
python scripts/memory/build-index.py --skip-embeddings
```

## Query Routing

Classify the user's request into one of three modes:

### 1. Temporal Mode

**Triggers**: date references — "yesterday", "last week", "March 5", "오늘", "어제", "지난주"

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

## Memory Store Structure

The search indexes these sources:

| Source | Path | Content |
|--------|------|---------|
| Sessions | `memory/sessions/*.md` | Auto-extracted user messages from agent transcripts |
| Decisions | `memory/decisions.md` | Consolidated architectural decisions from MEMORY.md |
| Patterns | `memory/patterns.md` | Recurring failure/success patterns |
| Glossary | `memory/glossary.md` | Project-specific terms and acronyms |

## Incremental Update

If the user starts a new session and wants fresh context, run extraction first:

```bash
python scripts/memory/extract-sessions.py --incremental --verbose
python scripts/memory/build-index.py --skip-embeddings
```

The `--incremental` flag only processes transcripts not yet in `memory/.cache/processed.txt`.

## Integration with Session Lifecycle

- **Session start**: Use `/recall` with a relevant topic to prime context before work begins
- **Session end**: The done-checklist rule triggers extraction automatically
- **Context handoff**: When splitting a long conversation, use `/recall` in the new session to restore state
