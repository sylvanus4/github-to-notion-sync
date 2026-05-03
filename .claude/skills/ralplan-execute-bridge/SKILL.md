---
name: ralplan-execute-bridge
description: >-
  Bridge omc-ralplan consensus plans to sp-executing-plans batch execution.
  Transforms ADR-style output into numbered task format, writes to
  docs/plans/, and invokes execution with optional auto-accept and skip-review
  flags.
---

# Ralplan-Execute Bridge

Orchestrator that chains `omc-ralplan` (3-agent consensus planning) with
`sp-executing-plans` (batch execution with checkpoints) into a seamless
plan-then-execute workflow.

## When to Use

- User has a complex task requiring both structured planning AND execution
- User wants to go from idea to implementation without manual plan handoff
- `omc-ralplan` has already produced a plan and user chose "Auto-Execute via Bridge"

## Workflow

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────────┐
│ omc-ralplan  │────▶│  Bridge Transform │────▶│ sp-executing-plans │
│ (consensus)  │     │  (ADR → tasks)   │     │ (batch execution)  │
└─────────────┘     └──────────────────┘     └────────────────────┘
```

### Phase 1: Planning (delegate to omc-ralplan)

If no existing plan is provided, invoke `omc-ralplan` with the user's task
description. Wait for the 3-agent consensus loop to converge.

**Skip this phase** if the user provides a path to an existing ralplan output.

### Phase 2: Transform (this skill's core logic)

Convert the omc-ralplan ADR-style output into the numbered-task format that
`sp-executing-plans` expects.

#### Input format (omc-ralplan output)

```markdown
# RALPLAN-DR: {Title}
## Principles
## Decision Drivers
## Options
## Implementation Steps
### Step 1: {description}
- Files: ...
- Acceptance: ...
### Step 2: ...
## Architecture Decision Record
```

#### Output format (sp-executing-plans input)

```markdown
# Plan: {Title}
Source: ralplan consensus ({date})
Confidence: {unanimous|majority}

## Tasks

### 1. {Step title}
**Goal**: {what this step achieves}
**Files**: {file list from ralplan}
**Steps**:
1. {concrete action}
2. {concrete action}
**Verify**: {acceptance criteria from ralplan}
**Batch**: {batch number, 3 tasks per batch}

### 2. {Step title}
...
```

#### Transformation rules

1. Each ralplan "Implementation Step" becomes a numbered task
2. Acceptance criteria from ralplan become "Verify" fields
3. File references are preserved in "Files" fields
4. Tasks are grouped into batches of 3 (sp-executing-plans default)
5. ADR metadata is preserved as a header comment for traceability
6. Confidence level from the consensus round maps to execution mode:
   - `unanimous` (all 3 agents agreed) → suggest `--auto-accept`
   - `majority` (2/3 agreed) → suggest `--skip-review` only
   - `no consensus` (required 5 iterations) → standard execution with reviews

### Phase 3: Persist

Write the transformed plan to `docs/plans/{YYYY-MM-DD}-{slug}.md`.

Create the `docs/plans/` directory if it does not exist.

### Phase 4: Execute (delegate to sp-executing-plans)

Invoke `sp-executing-plans` with the persisted plan file path.

**Flag selection** based on consensus confidence:

| Consensus | Flags | Behavior |
|-----------|-------|----------|
| Unanimous | `--auto-accept --skip-review` | Execute all batches without pause |
| Majority | `--skip-review` | Skip per-task review, pause between batches |
| Weak | (none) | Full review at every checkpoint |

The user can override these defaults at invocation time.

## Flags

| Flag | Effect |
|------|--------|
| `--plan-only` | Run Phase 1-3, skip execution. Useful for review before commit. |
| `--skip-planning` | Skip Phase 1, accept a plan path as input. |
| `--auto-accept` | Pass to sp-executing-plans: skip batch-level confirmations. |
| `--skip-review` | Pass to sp-executing-plans: skip per-task architect review. |
| `--deliberate` | Pass `--deliberate` to omc-ralplan for high-risk work (adds pre-mortem). |

## Safety Gates

1. **Blast radius check**: If the plan touches >15 files, warn and require
   explicit user confirmation before `--auto-accept`.
2. **Destructive operation scan**: If any step involves `rm`, `DROP`, `DELETE`,
   `force-push`, or schema migration, downgrade to standard execution
   regardless of consensus level.
3. **Consensus mismatch**: If omc-ralplan required all 5 iterations without
   convergence, refuse `--auto-accept` and recommend `--plan-only` for review.

## Error Recovery

- If sp-executing-plans fails mid-batch, the bridge preserves the plan file
  in `docs/plans/` so execution can resume with `--skip-planning`.
- Failed batch number is reported so the user can resume from that point.

## Example Invocation

**Full pipeline (plan + execute):**
> "ralplan execute: refactor the authentication module to use JWT tokens"

**Execute existing plan:**
> "ralplan bridge --skip-planning docs/plans/2026-04-18-auth-refactor.md"

**Plan only, review before executing:**
> "ralplan execute --plan-only: migrate database schema to v3"

## Integration Points

| Skill | Role |
|-------|------|
| `omc-ralplan` | Phase 1 planning with 3-agent consensus |
| `sp-executing-plans` | Phase 4 batch execution with checkpoints |
| `domain-commit` | Post-execution commit splitting |
| `sp-verification` | Verification between batches |
