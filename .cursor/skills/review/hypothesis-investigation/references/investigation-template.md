# Investigation Log

> **Issue**: [one-line summary]
> **Started**: [timestamp]
> **Status**: INVESTIGATING | ROOT_CAUSE_FOUND | RESOLVED
> **Artifact path**: `outputs/investigation/{date}/`

---

## Observations

- **Reproduction**: [exact steps to reproduce]
- **Error**: [exact message, stack trace, or unexpected behavior]
- **Environment**: [versions, config, OS, runtime]
- **Working boundary**: [what DOES work — narrows the search space]
- **Frequency**: [always / intermittent / under load]

## Hypotheses

### H1: [description] — ROOT HYPOTHESIS

- **Supports**: [evidence for]
- **Conflicts**: [evidence against]
- **Test**: [minimal experiment, max 5 lines]

### H2: [description]

- **Supports**: [evidence for]
- **Conflicts**: [evidence against]
- **Test**: [minimal experiment, max 5 lines]

### H3: [description]

- **Supports**: [evidence for]
- **Conflicts**: [evidence against]
- **Test**: [minimal experiment, max 5 lines]

_(minimum 3 hypotheses required before any experiment)_

## Experiments

### Exp 1 — testing H[N]

- **Change**: [what was modified, max 5 lines]
- **Expected if confirmed**: [predicted outcome]
- **Expected if rejected**: [predicted outcome]
- **Actual**: [observed result]
- **Verdict**: CONFIRMED / REJECTED / INCONCLUSIVE

### Exp 2 — testing H[N]

- **Change**: [what was modified, max 5 lines]
- **Expected if confirmed**: [predicted outcome]
- **Expected if rejected**: [predicted outcome]
- **Actual**: [observed result]
- **Verdict**: CONFIRMED / REJECTED / INCONCLUSIVE

## Pivot Log

| Exp # | Failed Direction | New Hypothesis | Reason for Pivot |
|-------|-----------------|----------------|------------------|
| | | | |

_(Two consecutive failures in the same direction → mandatory pivot)_

## Root Cause

[One sentence identifying the confirmed root cause]

## Fix

- **Files changed**: [list with line numbers]
- **Regression test**: [file:line or test name]
- **Verification**: [command that proves the fix works]

## Timeline

| Time | Action | Result |
|------|--------|--------|
| | | |
