---
name: simplify
description: >-
  Run parallel code review agents to analyze code for reuse opportunities, code quality,
  tech debt, and performance issues, then auto-fix findings by priority. Supports 3
  scoping modes: diff (changed files), today (daily work), and full (entire project).
disable-model-invocation: true
arguments: [scope]
---

# Simplify — Parallel Code Review & Auto-Fix

Analyze code through 4 parallel review agents, aggregate findings, and auto-fix issues by priority.

## Usage

```
/simplify                    # diff mode (default)
/simplify today              # files changed today
/simplify full               # entire project
/simplify src/api/           # specific directory
```

## Scoping Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| `diff` (default) | `/simplify` | Git diff (unstaged + staged + HEAD) |
| `today` | `/simplify today` | All files changed today |
| `full` | `/simplify full` | All source files in the project |

## Workflow

### Step 1: Identify Target Files

Resolve files based on scoping mode using git commands. If no changes found, fall back to `git diff HEAD~1 HEAD`. If still empty, inform user and stop.

### Step 2: Fan Out 4 Review Agents

**Agent 1: Reuse & Duplication**
- Duplicated logic across files
- Missed abstraction opportunities
- Inconsistent implementations of same concept

**Agent 2: Code Quality**
- Naming clarity, function length, complexity
- Error handling completeness
- Type safety (any, unknown, assertion abuse)

**Agent 3: Tech Debt**
- TODO/FIXME without issue links
- Deprecated API usage
- Dead code, unused imports/exports

**Agent 4: Performance**
- N+1 queries, missing pagination
- Unnecessary re-renders (React)
- Unoptimized loops, missing caching

### Step 3: Aggregate and Deduplicate

Merge all agent outputs, remove duplicates, classify by severity:
1. **Critical**: Bugs, security, data loss
2. **High**: Performance regression, correctness
3. **Medium**: Code quality, maintainability
4. **Low**: Style, best practices

### Step 4: Apply Auto-Fixes

For each finding (highest severity first):
1. If auto-fixable (single-file, mechanical): apply silently
2. If requires judgment: present options to user
3. If informational: include in report only

After each fix:
- Run lint/typecheck on modified file
- If fails, revert and mark as manual

### Step 5: Verification

Run project lint and typecheck on all modified files. Report results.

### Step 6: Summary Report

```markdown
## Simplify Report

### Summary
- Scope: [diff/today/full]
- Files reviewed: N
- Auto-fixed: X issues
- Manual action needed: Y issues

### Findings
[severity-sorted list with code references]

### Changes Made
[list of auto-fixes applied]
```

## Test Invocation

```
/simplify
/simplify today
/simplify full focus on performance
```
