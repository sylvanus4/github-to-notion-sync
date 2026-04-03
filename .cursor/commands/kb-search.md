---
description: "Search across Knowledge Base wiki articles with keyword, semantic, or fuzzy matching"
---

# KB Search

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-search/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Search across a Knowledge Base wiki. `$ARGUMENTS` should contain:

1. **Topic name** — the KB topic to search
2. **Search query** — what to find

Optional:
- `--mode keyword|semantic|fuzzy|heading` — search mode (auto-detected by default)
- `--top N` — return top N results (default 10)

Examples:
- `transformer-architectures attention mechanism` — semantic search
- `ml-foundations --mode keyword "dropout rate"` — exact keyword search
- `robotics --mode heading sim-to-real` — search by heading

If topic is missing, list available KBs and ask which to search.
