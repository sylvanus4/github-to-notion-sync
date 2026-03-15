---
description: Generate a comprehensive multi-phase implementation plan that maps a high-level goal to all available skills with phase decomposition, skill assignments, mermaid diagrams, and concurrency strategies.
---

## Full-Stack Plan

Generate an enterprise-grade implementation plan that decomposes your goal into 5 standard phases (Survey, Analysis, Research, Implementation, Testing), assigns skills to each sub-step, and produces a structured plan via the CreatePlan tool.

### Usage

```bash
/full-stack-plan <goal description>
/full-stack-plan --phases 1,2,3 <goal>
/full-stack-plan --scope survey-only <goal>
/full-stack-plan --scope plan-only <goal>
/full-stack-plan --execute <goal>
```

### Options

| Option | Description |
|--------|-------------|
| (none) | Full 5-phase plan generation |
| `--phases <list>` | Include only specified phases (comma-separated: 1,2,3,4,5) |
| `--scope survey-only` | Phase 1 only (project survey and gap analysis) |
| `--scope plan-only` | Phases 1-3 (survey + analysis + research/planning, no implementation) |
| `--execute` | After plan approval, delegate execution to mission-control |

### What It Does

1. **Surveys** project context (README, MEMORY.md, PRDs, roadmap)
2. **Decomposes** the goal into up to 5 standard phases
3. **Assigns** the most relevant skills from a registry of 100+ skills to each sub-step
4. **Batches** skills into parallel groups (max 4 concurrent per batch)
5. **Generates** a structured plan via CreatePlan with mermaid diagrams, skill counts, and concurrency strategy

### Examples

```bash
# Full feature development pipeline (~40-50 skills)
/full-stack-plan Add a backtesting engine for trading strategies

# Scoped security audit (phases 1 and 5 only)
/full-stack-plan --phases 1,5 Security and quality audit of the backend

# Research and planning only (no implementation)
/full-stack-plan --scope plan-only Evaluate adding real-time streaming to the platform

# Full pipeline with auto-execution after approval
/full-stack-plan --execute Migrate the legacy API to FastAPI with full test coverage

# Code-only task (skip research phases)
/full-stack-plan --phases 1,4,5 Refactor the stock analysis module for better testability
```

### Output

A plan file in `.cursor/plans/` with:
- YAML frontmatter with todos for each phase sub-step
- Detailed phase sections with skills, inputs, and outputs
- Mermaid execution flow diagram
- Skill count summary table
- Concurrency strategy
- Key files touched

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/plans` | Optimize prompt + match 3-8 tasks to skills | When you need prompt optimization, not a full pipeline |
| `/plan` | General implementation planning | When you have a clear prompt and need a simple plan |
| `/simplify` | Code review + auto-fix | When you only need code quality review |
| `/full-quality-audit` | Fixed multi-skill audit | When you want the standard audit, not a custom pipeline |

### Skill Reference

This command uses the **full-stack-planner** skill at `.cursor/skills/full-stack-planner/SKILL.md`.
Read and follow the skill instructions before proceeding.

User input:

$ARGUMENTS
