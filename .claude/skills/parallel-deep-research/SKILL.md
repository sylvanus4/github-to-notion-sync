---
name: parallel-deep-research
description: Exhaustive multi-source parallel web research with citation-backed reports. ONLY use when user explicitly says 'deep research' or 'comprehensive report'.
disable-model-invocation: true
arguments: [topic]
---

Run exhaustive parallel web research on `$topic`.

## When to Use

ONLY when user explicitly requests:
- "deep research", "exhaustive", "comprehensive report", "thorough investigation"

For normal research/lookup, use WebSearch directly — it's faster and cheaper.

## Process

1. **Query Decomposition**: Break topic into 5-8 sub-questions
2. **Parallel Search**: Fan out searches across multiple engines
3. **Source Evaluation**: Score credibility (domain authority, recency, citation count)
4. **Synthesis**: Merge findings with deduplication
5. **Citation**: Include source URLs for every claim

## Output Format

```markdown
## Research Report: [topic]
Date: [YYYY-MM-DD]

### Executive Summary
### Key Findings
### Detailed Analysis
### Sources & Citations
### Confidence Assessment
### Open Questions
```

## Rules

- Minimum 10 distinct sources
- Recency preference (< 6 months)
- Explicit confidence levels per finding
- Clearly separate facts from interpretation
