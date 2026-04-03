---
description: "Ask complex questions against a Knowledge Base wiki and get researched, citation-backed answers"
---

# KB Query

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-query/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Research a question against a Knowledge Base. `$ARGUMENTS` should contain:

1. **Topic name** — the KB topic to query
2. **Question** — the natural language question

Optional flags:
- `--file-back` — archive the answer into the wiki
- `--deep` — read all potentially relevant articles
- `--with-sources` — include raw source excerpts

Examples:
- `transformer-architectures What are the key differences between RoPE and sinusoidal positional encoding?`
- `ml-foundations --file-back What are the 3 most promising research directions?`

If topic is missing, list available KBs and ask which to query.
