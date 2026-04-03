---
description: "Diagnose per-turn token consumption and recommend cost-saving optimizations"
---

# Token Diet

## Skill Reference

Read and follow the skill at `.cursor/skills/standalone/token-diet/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for the mode:

- If empty or contains "diagnose" → run **diagnose** mode
- If contains "apply" → run **apply** mode (diagnose + safe fixes with backup)
- If contains "report" → run **report** mode (diagnose + save to file)

### Execution

Follow the skill workflow steps 1-5 exactly as specified for the selected mode.
