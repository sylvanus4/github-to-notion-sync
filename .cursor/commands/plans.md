---
description: Optimize a raw prompt using prompt-architect frameworks, then decompose it into a skill-based execution plan with task delegation and dependency ordering.
---

## Plans

Two-phase pipeline: optimize your prompt with a research-backed framework, then generate a structured execution plan that maps sub-tasks to the best available skills.

### Usage

```bash
/plans <your raw prompt>
/plans --framework <name> <your raw prompt>
/plans --execute <your raw prompt>
/plans --framework risen --execute <your raw prompt>
```

### Options

| Option | Description |
|--------|-------------|
| (none) | Auto-detect best framework, produce plan only |
| `--framework <name>` | Force a specific framework: `co-star`, `risen`, `rise-ie`, `rise-ix`, `tidd-ec`, `rtf`, `cot`, `cod` |
| `--execute` | After plan approval, auto-execute via mission-control |

### What It Does

**Phase 1 — Prompt Optimization** (via prompt-architect):
1. Score your raw prompt across 5 dimensions (Clarity, Specificity, Context, Completeness, Structure)
2. Recommend and apply the best framework (CO-STAR, RISEN, TIDD-EC, etc.)
3. Present before/after comparison with quality scores
4. Wait for your approval before proceeding

**Phase 2 — Execution Planning** (skill matching):
1. Decompose the optimized prompt into 3-8 concrete sub-tasks
2. Match each sub-task to the best available skill from the registry
3. Determine parallel vs sequential execution order
4. Produce a structured plan with verification criteria

### Examples

```bash
# Feature development — auto-selects RISEN framework
/plans Build a user authentication system with OAuth and JWT

# Force CO-STAR for a content task
/plans --framework co-star Write a technical blog post about our platform architecture

# Code quality audit with auto-execution
/plans --execute Review the frontend codebase for performance issues and fix them

# Complex multi-domain task
/plans Migrate the legacy API to FastAPI, add tests, update docs, and create a PR

# Security-focused task
/plans --framework risen Perform a security audit on our authentication endpoints

# Simple task (Phase 2 may be skipped if too few sub-tasks)
/plans Refactor the user model to use Pydantic v2
```

### Output

The command produces a Plans Report with two sections:

1. **Phase 1 — Prompt Optimization**: Framework used, score improvement, structured prompt
2. **Phase 2 — Execution Plan**: Task table with skill assignments, dependency groups, complexity estimates, and verification criteria

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/plan` | General implementation planning | When you already have a clear prompt and don't need optimization |
| `/prompt-transform` | Polish prompt structure | When you only need prompt quality improvement, no execution plan |
| `/simplify` | Code review + auto-fix | When you only need code quality review on existing code |
| `/full-quality-audit` | Fixed multi-skill audit | When you want the standard audit workflow, not a custom plan |

### Skill Reference

This command uses the **plans** skill at `.cursor/skills/plans/SKILL.md`.
Read and follow the skill instructions before proceeding.

User input:

$ARGUMENTS
