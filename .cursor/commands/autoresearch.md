---
description: "Run AutoResearchClaw 23-stage pipeline and distribute results to Notion, Slack, PPTX, NLM, and archive"
---

# AutoResearch — AutoResearch E2E Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/research/autoresearch-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- Topic description as primary input (e.g., `"LLM-based trading agents"`)
- `--run-id {id}`: skip research, distribute an existing run
- `--skip research,distribute`: skip specific stages (comma-separated)
- `--dry-run`: show execution plan without running

### Examples

```
/autoresearch "Autonomous AI agents for financial market analysis"
/autoresearch --run-id abc123-def456
/autoresearch "topic" --skip distribute
/autoresearch "topic" --dry-run
```
