---
description: "Build knowledge graphs and AI memory from documents using cognee"
---

## Cognee

Build persistent AI memory and knowledge graphs from documents using the cognee knowledge engine.

### Usage

```
/cognee <action> [arguments]
```

### Actions

| Action | Arguments | Description |
|--------|-----------|-------------|
| `add` | `<data> [--dataset name]` | Ingest text, files, or directories |
| `cognify` | `[--datasets name1 name2]` | Build knowledge graph from ingested data |
| `search` | `<query> [--type TYPE] [--top-k N]` | Search the knowledge graph |
| `delete` | `[--dataset name] [--all]` | Delete datasets |
| `setup` | | Check prerequisites and configure env vars |
| `demo` | `[topic]` | Run a full add → cognify → search demo |
| `ui` | | Start web UI and API server |

### Execution

Read and follow the `cognee` skill (`.cursor/skills/cognee/SKILL.md`) for the full workflow, API details, configuration, and error handling.

### Examples

```bash
# Index project documentation
/cognee add docs/ --dataset project_docs

# Build knowledge graph
/cognee cognify --datasets project_docs

# Search with graph-enhanced RAG
/cognee search "What is the caching strategy?"

# Search specific chunks
/cognee search "authentication" --type CHUNKS --top-k 5

# Full demo pipeline
/cognee demo "AI agent memory systems"

# Check prerequisites
/cognee setup

# Start web UI
/cognee ui

# Delete and re-index
/cognee delete --all
```
