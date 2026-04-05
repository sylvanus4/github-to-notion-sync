# Long-Term Memory Index

This directory is the project's long-term memory store, enabling cross-session context restoration via the `/recall` skill.

## Architecture: 3-Layer Memory

- **Layer 1 (Index)**: `MEMORY.md` — ~150-char pointer lines, always loaded (~3K tokens max)
- **Layer 2 (Topics)**: `memory/topics/*.md` — full detail, fetched on-demand by keyword match
- **Layer 3 (Transcripts)**: `memory/sessions/*.md` — grep/BM25 only, never loaded directly

## Directory Structure

```
memory/
├── topics/         # Layer 2: structured topic files (on-demand fetch)
│   ├── preferences.md      # User prefs, doc standards, Slack conventions
│   ├── workspace-facts.md  # Repos, tools, credentials, key people
│   └── pipeline-ops.md     # Google Daily pipeline, continual-learning issue
├── sessions/       # Layer 3: auto-extracted session transcripts (BM25 search)
├── archive/        # COLD tier memory (attention decay < 0.3)
├── .cache/         # Embedding cache and processed transcript tracker
│   ├── embeddings.pkl
│   └── processed.txt
└── index.md        # This file
```

## How It Works

1. **Extract**: `scripts/memory/extract-sessions.py` parses agent transcript JSONL files into `sessions/*.md`
2. **Index**: `scripts/memory/build-index.py` builds BM25 and semantic embedding indexes
3. **Search**: `scripts/memory/search.py` provides 4 search modes (bm25, semantic, hybrid, temporal)
4. **Recall**: The `/recall` skill wraps search with query routing and "One Thing" action output

## Maintenance

- Run `python scripts/memory/extract-sessions.py --incremental` after sessions
- Run `python scripts/memory/build-index.py` after extraction to rebuild the search index
- Run `python scripts/memory/attention_decay.py --apply` when MEMORY.md exceeds 50 pointers
- Run `python scripts/memory/memory_classify.py "entry"` to auto-classify and route new memory
