---
description: "Run end-of-day knowledge aggregation — collect all daily outputs and ingest into the Cognee knowledge graph"
---

## Knowledge Aggregate

Collect all outputs generated today and ingest them into the Cognee knowledge graph for long-term retrieval.

### Usage

```
/knowledge-aggregate                        # aggregate today's outputs
/knowledge-aggregate --date 2026-03-18      # aggregate a specific day
/knowledge-aggregate --dry-run              # list files to ingest without ingesting
/knowledge-aggregate --skip-cognify         # add documents but skip graph building
```

### Execution

Read and follow the skill at `.cursor/skills/knowledge-daily-aggregator/SKILL.md`.

User input: $ARGUMENTS

1. Scan output directories for today's artifacts (reports, reviews, analyses, meeting digests)
2. Deduplicate against previous ingestion records
3. Ingest new documents into Cognee via Python SDK or CLI
4. Run cognify to build/update the knowledge graph
5. Report ingestion summary (files added, entities extracted, relationships built)
