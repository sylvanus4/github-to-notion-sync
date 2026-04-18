## PRD to Plan

Turn a PRD into a multi-phase implementation plan using tracer-bullet vertical slices that reduce integration risk.

### Usage

```
/prd-to-plan                           # plan from PRD in current context
/prd-to-plan docs/prd/feature-x.md     # plan from a specific PRD file
/prd-to-plan --phases 3                # limit to 3 implementation phases
```

### Workflow

1. **Read PRD** — Parse goals, non-goals, user stories, constraints, and success metrics
2. **Identify slices** — Decompose into vertical slices that each deliver end-to-end value
3. **Order phases** — Sequence slices to minimize integration risk (tracer bullet first)
4. **Detail tasks** — Break each phase into implementable tasks with dependencies
5. **Output plan** — Produce a numbered task list with phase boundaries and verification criteria

### Execution

Read and follow the `sp-writing-plans` skill (`.cursor/skills/standalone/sp-writing-plans/SKILL.md`) for plan structure, task decomposition, and verification criteria format.

### Examples

Generate a plan from a PRD:
```
/prd-to-plan docs/prd/auth-system.md
```

Plan with limited phases:
```
/prd-to-plan --phases 2 docs/prd/dashboard.md
```
