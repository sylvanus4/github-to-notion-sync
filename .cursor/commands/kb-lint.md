---
description: "Run health checks on a Knowledge Base wiki — find inconsistencies, gaps, and improvement opportunities"
---

# KB Lint

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-lint/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run health checks on a Knowledge Base. `$ARGUMENTS` should contain:

1. **Topic name** — the KB topic to lint

Optional flags:
- `--fix` — auto-fix trivial issues (missing frontmatter, broken links)
- `--impute` — use web search to find data for gap filling
- `--deep` — run all checks including expensive cross-article consistency

Examples:
- `transformer-architectures` — basic lint
- `ml-foundations --fix` — lint and auto-fix
- `robotics --impute --fix` — full lint with web enrichment and auto-fix

If topic is missing, list available KBs and ask which to lint.
