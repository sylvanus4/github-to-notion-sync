---
description: "Marketing team operations — Elon Algorithm performance audit and meeting action extraction"
argument-hint: "[audit|meeting] [team data or transcript path]"
---

# Marketing Team Ops

Read and follow the skill at `.cursor/skills/marketing/marketing-team-ops/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the requested team operation:

| Command | Script | Purpose |
|---------|--------|---------|
| `audit` | `scripts/team_performance_audit.py` | 5-step Elon Algorithm team audit |
| `meeting` | `scripts/meeting_action_extractor.py` | Extract actions, decisions, commitments |

Requires: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`. Optional: `HUBSPOT_API_KEY` for task creation.
