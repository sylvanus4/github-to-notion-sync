---
name: recall
description: Restore cross-session context from long-term memory — search session transcripts, decisions, patterns, and glossary.
arguments: [query]
---

Search long-term memory for `$query`.

## Search Methods

1. **BM25**: Keyword-based search across extracted session transcripts
2. **Semantic**: Embedding-based similarity search (if embeddings built)
3. **Hybrid**: Combined BM25 + semantic with reciprocal rank fusion

## Sources Searched

- `memory/sessions/*.md` — extracted session transcripts
- `memory/topics/*.md` — topic-specific knowledge
- `MEMORY.md` — index pointers
- `tasks/lessons.md` — learned corrections

## Output

```markdown
## Recall Results: [query]

### Relevant Sessions
[Session date, topic, key decisions]

### Related Topics
[Topic file excerpts]

### Lessons Learned
[Relevant corrections and patterns]
```

## Flags

- `--summarize`: Run LLM-powered structured Korean summary of results
- Default: return raw search results with context snippets

## Rules

- Search before creating new memory entries to avoid duplication
- Prefer recent sessions over old ones
- Include source file paths for traceability
