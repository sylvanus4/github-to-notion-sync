---
name: ship
description: >-
  End-to-end pre-merge pipeline: review code with parallel agents, auto-fix findings,
  verify with linting, create bisect-able domain-split commits, and open a PR.
  Enforces the Iron Law of Verification and Review Readiness checks.
disable-model-invocation: true
arguments: [options]
---

# Ship — Pre-Merge Pipeline

One command to go from "code is done" to "PR is ready". Runs parallel code review, auto-fixes, creates domain-split commits, and opens a PR.

## Usage

```
/ship                    # full pipeline: review -> fix -> commit -> PR
/ship --no-pr            # review -> fix -> commit (skip PR)
/ship --dry-run          # review only, show what would happen
/ship --base main        # specify PR base branch (default: dev)
/ship --no-fix           # review -> commit -> PR (skip auto-fix)
```

## Iron Law of Verification

**Never claim completion without fresh evidence.** Before commits or PRs:
1. Run lint/typecheck on all modified files — confirm PASS
2. Run relevant tests — confirm PASS
3. Verify no files in inconsistent state

If any verification fails, STOP and report. Do NOT proceed with known failures.

## Review Readiness Dashboard

Before committing, display:

```
Review Readiness
================
[✓] All lint checks pass
[✓] No Critical findings remaining
[✓] All auto-fixes verified
[?] Tests pass (N/A if no test runner)
[✓] No TODO/FIXME without issue link
[✓] No secrets or credentials detected
[✓] Commit messages follow convention
```

If any `[✗]`, pause and ask user.

## Bisect-able Commit Strategy

1. Each commit leaves codebase compilable and lint-passing
2. Feature code and tests go in the same commit
3. Refactoring separated from behavior changes
4. DB migrations get own commit before dependent code

## Workflow

### Step 1: Identify Changed Files

```bash
git diff --name-only
git diff --cached --name-only
```

If no changes, inform and stop.

### Step 2: Run Parallel Review (same as /simplify)

4 review agents: Reuse, Quality, Tech Debt, Performance.
Apply 8/10 confidence gate.

### Step 3: Auto-Fix

Apply auto-fixable findings. Run lint after each fix.

### Step 4: Verify

Run full lint, typecheck, and test suite on modified files.

### Step 5: Domain-Split Commits

Group changes by domain and create separate commits:
- `feat: Add user authentication handler` (backend)
- `feat: Add login form component` (frontend)
- `test: Add auth handler tests` (tests)
- `chore: Update dependencies` (deps)

Commit format: `<TYPE>: <Summary>` per project conventions.

### Step 6: Push and Create PR

```bash
git push -u origin HEAD
gh pr create --title "#<ISSUE> <type>: <summary>" --body "..."
```

PR body follows project template (Issue, Changes, Why, Test).

## Test Invocation

```
/ship
/ship --dry-run
/ship --base dev --no-fix
```
