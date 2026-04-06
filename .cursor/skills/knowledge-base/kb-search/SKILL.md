---
name: kb-search
description: >-
  Search across Knowledge Base wiki articles using SQLite FTS5
  full-text search, optional vector embeddings (hybrid mode),
  and ripgrep fallback. Returns ranked results with context
  snippets. Designed as both a user-facing tool and an LLM tool
  for use in larger query pipelines.
  Use when the user asks to "search KB", "find in knowledge base",
  "kb search", "grep wiki", "look up in KB", or wants to locate
  specific information across wiki articles without full Q&A synthesis.
  Do NOT use for synthesized Q&A answers (use kb-query).
  Do NOT use for web search (use WebSearch).
  Do NOT use for codebase search (use Grep).
  Korean triggers: "KB 검색", "위키 검색", "지식베이스 검색",
  "KB에서 찾기", "위키에서 검색".
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "execution"
  tags: ["knowledge-base", "search", "retrieval", "fts5", "vector", "hybrid"]
---

# KB Search — Wiki Search Engine

Fast search across Knowledge Base wiki articles powered by SQLite FTS5 full-text search and optional vector embeddings. Falls back to ripgrep when the index is unavailable.

## Search Modes

| Mode | Engine | Speed | Best For |
|------|--------|-------|----------|
| **auto** | FTS5 (fallback: ripgrep) | Fast | Default — uses best available engine |
| **fts** | SQLite FTS5 | Fast | Exact keywords, titles, porter-stemmed terms |
| **hybrid** | FTS5 + OpenAI vectors | Medium | Conceptual queries, semantic similarity |
| **ripgrep** | ripgrep grep | Fast | Legacy fallback, no DB required |

## Prerequisites

- `brain_index.db` must exist for FTS5/hybrid modes. Build with:

```bash
python scripts/kb_index_db.py --rebuild          # full rebuild
python scripts/kb_index_db.py --rebuild --embed   # with vector embeddings
```

- For hybrid mode: `OPENAI_API_KEY` environment variable and `openai` Python package

## Workflow

### Step 1: Select Search Mode

The `--mode` flag controls engine selection:

- **auto** (default): Uses FTS5 if `brain_index.db` exists, otherwise ripgrep
- **fts**: FTS5 only; errors if DB missing
- **hybrid**: FTS5 (weight 0.4) + vector cosine similarity (weight 0.6)
- **ripgrep**: Legacy file-based grep

### Step 2: Execute Search

#### FTS5 Search (default)

SQLite FTS5 with porter stemming and unicode61 tokenizer. Searches title, compiled_truth, timeline, and body columns:

```bash
python scripts/kb_search.py "knowledge base architecture" --mode fts --top 10
```

#### Hybrid Search (FTS5 + Vector)

Combines FTS5 keyword relevance with OpenAI `text-embedding-3-small` cosine similarity:

```bash
python scripts/kb_search.py "how do agents learn" --mode hybrid --top 10
```

Requires `--embed` flag during index build and `OPENAI_API_KEY` at search time.

#### Ripgrep Fallback

When no SQLite index exists:

```bash
python scripts/kb_search.py "query" --mode ripgrep -C 3
```

### Step 3: Format Output

Results are ranked by relevance score. Use `--json` for pipeline consumption:

```bash
python scripts/kb_search.py "RSI signals" --json --top 5
```

```json
{
  "query": "RSI signals",
  "mode": "fts",
  "total": 3,
  "results": [
    {
      "topic": "trading-daily",
      "article": "rsi-oscillator",
      "title": "RSI Oscillator",
      "path": "knowledge-bases/trading-daily/wiki/concepts/rsi-oscillator.md",
      "fts_rank": -8.2,
      "hits": 8
    }
  ]
}
```

## Standalone CLI

```bash
python scripts/kb_search.py "query"                           # auto mode, all KBs
python scripts/kb_search.py "query" -t ai-knowledge-bases      # specific topic
python scripts/kb_search.py "query" --mode hybrid              # semantic + keyword
python scripts/kb_search.py "query" --mode ripgrep -C 3        # legacy with context
python scripts/kb_search.py "query" --json --top 20            # JSON for pipelines
```

## Index Management

```bash
python scripts/kb_index_db.py --rebuild          # full rebuild (no embeddings)
python scripts/kb_index_db.py --rebuild --embed   # full rebuild with vectors
python scripts/kb_index_db.py --incremental       # delta update (fast)
python scripts/kb_index_db.py --stats             # print index statistics
python scripts/kb_index_db.py --search "query"    # quick FTS5 test
```

## Examples

### Example 1: FTS5 keyword search

**User says:** "Search my trading KB for 'bollinger bands'"

**Actions:**
1. Run: `python scripts/kb_search.py "bollinger bands" -t trading-daily`
2. FTS5 returns ranked results with porter-stemmed matching
3. Present results with topic grouping

### Example 2: Hybrid semantic search

**User says:** "Find articles about market risk assessment methods"

**Actions:**
1. Run: `python scripts/kb_search.py "market risk assessment methods" --mode hybrid`
2. FTS5 finds keyword matches, vector search finds semantically similar articles
3. Weighted merge (40% FTS, 60% vector) produces final ranking

### Example 3: Search as LLM tool

**Used by kb-query internally:**

1. kb-query calls `search_fts()` or `search_hybrid()` from `kb_search.py`
2. Returns top results with file paths and scores
3. kb-query reads those files for full content
4. kb-query synthesizes the final answer

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No matches | Zero results | Suggest alternative queries, check spelling |
| No brain_index.db | DB missing | Run `python scripts/kb_index_db.py --rebuild` |
| No OPENAI_API_KEY | Hybrid mode fails | Falls back to FTS5-only results |
| No wiki | Wiki directory missing | Prompt to run kb-compile |
