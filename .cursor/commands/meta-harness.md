---
description: "Run Meta-Harness outer-loop optimization — code-level harness mutations with filesystem-based uncompressed history and Pareto frontier tracking"
---

# Meta-Harness Optimizer

## Skill Reference

Read and follow the skill at `.cursor/skills/automation/meta-harness-optimizer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Modes

- `optimize` (default): Run the full outer-loop optimization cycle
- `dry-run`: Analyze the target skill and propose mutations without executing
- `analyze`: Generate a report from an existing TraceArchive
- `ablate`: Remove components one-by-one and measure impact

### Flags

- `--target <path>`: Target skill SKILL.md path (required for optimize/dry-run)
- `--iterations <N>`: Max optimization iterations (default: 20)
- `--archive-root <path>`: TraceArchive root (default: `_workspace/meta-harness/`)
- `--objectives <a,b>`: Comma-separated optimization objectives (default: `accuracy,cost`)
- `--inner-loop`: Run skill-autoimprove in --trace-aware mode as inner loop
- `--resume <run-id>`: Resume a previous optimization run

### Examples

```
/meta-harness --target .cursor/skills/trading/daily-stock-check/SKILL.md
/meta-harness dry-run --target .cursor/skills/pipeline/today/SKILL.md
/meta-harness analyze --archive-root _workspace/meta-harness/run-abc123
/meta-harness optimize --target .cursor/skills/review/deep-review/SKILL.md --iterations 10 --inner-loop
/meta-harness --resume run-abc123
```
