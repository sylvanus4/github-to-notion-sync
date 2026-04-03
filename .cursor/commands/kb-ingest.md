---
description: "Ingest source material (URLs, PDFs, text) into a Knowledge Base raw/ directory"
---

# KB Ingest

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-ingest/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Ingest raw source material into a Knowledge Base topic. Parse `$ARGUMENTS` to extract:

1. **Topic name** — the KB topic (e.g., `transformer-architectures`)
2. **Sources** — one or more URLs, file paths, or text content

Examples:
- `transformer-architectures https://example.com/article`
- `ml-foundations ~/papers/paper1.pdf ~/papers/paper2.pdf`
- `robotics https://arxiv.org/abs/2401.12345 https://example.com/blog-post`

If topic is missing, ask which KB to ingest into. If sources are missing, ask what to ingest.
