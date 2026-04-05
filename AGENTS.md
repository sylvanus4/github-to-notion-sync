# AGENTS.md

Slim redirect — full context lives in topic files. See `learned-memory.mdc` for compacted preferences.

## Where to Find Details

| Topic | Location |
|-------|----------|
| User preferences & doc standards | `memory/topics/preferences.md` |
| Workspace facts, repos, auth | `memory/topics/workspace-facts.md` |
| Pipeline protocols (Google Daily) | `memory/topics/pipeline-ops.md` |
| Session transcripts (search only) | `memory/sessions/` via `scripts/memory/search.py` |

## Memory Architecture

- **Layer 1 (Index)**: `MEMORY.md` — ~150-char pointers, always loaded
- **Layer 2 (Topics)**: `memory/topics/*.md` — on-demand fetch
- **Layer 3 (Transcripts)**: `memory/sessions/*.md` — grep/BM25 only
