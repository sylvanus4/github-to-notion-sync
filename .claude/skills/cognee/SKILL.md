---
name: cognee
description: Build persistent AI memory and knowledge graphs — ingest documents, extract entities/relationships, search with graph-enhanced RAG.
disable-model-invocation: true
arguments: [operation, source]
---

Operate the Cognee knowledge engine: `$operation` on `$source`.

## Operations

| Operation | Description |
|-----------|-------------|
| add | Ingest text, PDF, DOCX, CSV, images, or audio |
| cognify | Process ingested data — extract entities, build knowledge graph |
| search | Graph-enhanced RAG search |
| status | Show ingestion and graph statistics |
| reset | Clear all data (requires confirmation) |

## Usage Patterns

```bash
# Ingest a document
cognee add path/to/document.pdf

# Process and build graph
cognee cognify

# Search with graph context
cognee search "How does tenant isolation work?"
```

## Integration Points

- Used by `knowledge-daily-aggregator` for daily output ingestion
- Used by `kb-ingest` as optional graph backend
- Used by `ai-context-router` for graph-enhanced queries

## Rules

- Always `cognify` after adding new documents
- Use graph search for relationship-heavy queries
- Use keyword search for specific fact retrieval
