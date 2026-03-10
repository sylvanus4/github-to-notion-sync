---
description: "Suggest strategic context compaction points based on workflow phase transitions"
---

# ECC Compact — Strategic Context Compaction

## Skill Reference

Read and follow the skill at `.cursor/skills/ecc-strategic-compact/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Analyze Session State

Evaluate the current session:
1. Estimate context window usage (tool calls, file reads, conversation length)
2. Identify the current workflow phase (research, planning, implementation, testing, review)
3. Check if a natural transition boundary is approaching

### Step 2: Recommend Action

Based on the analysis:

- **Low usage (< 40%)**: No compaction needed — continue working
- **Medium usage (40-70%)**: Suggest compacting at the next phase transition
- **High usage (> 70%)**: Recommend immediate compaction with preservation list

### Step 3: Generate Compaction Summary

If compaction is recommended, generate a summary of what should survive:

1. **Active task context** — current todo items, in-progress work
2. **Key decisions** — architectural choices, rejected alternatives
3. **File change log** — which files were modified and why
4. **Blocking issues** — unresolved problems, open questions
5. **Next steps** — what to do after compaction

Present this as a ready-to-use context block the user can paste after `/compact`.

## Constraints

- Never auto-compact — always suggest and let the user decide
- Preserve all unfinished todo items in the survival summary
- Include file paths for all recently modified files
