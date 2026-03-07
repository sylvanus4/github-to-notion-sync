# Simplify Report Template

Use this template when presenting the final report to the user after all fixes have been applied.

## Full Report

```
Simplify Review Report
======================
Date: {YYYY-MM-DD}
Changed Files: {N}
Analysis Time: {N} seconds

Agents Completed: {N}/4
  Refactor Agent:          Done ({N} tool uses, {N}k tokens)
  Quality Agent:           Done ({N} tool uses, {N}k tokens)
  Tech Debt + Analyzer:    Done ({N} tool uses, {N}k tokens)
  Performance Agent:       Done ({N} tool uses, {N}k tokens)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Findings Summary
────────────────
Total: {N} findings

| Severity | Count | Fixed | Skipped |
|----------|-------|-------|---------|
| Critical | {N}   | {N}   | {N}     |
| High     | {N}   | {N}   | {N}     |
| Medium   | {N}   | {N}   | {N}     |
| Low      | {N}   | {N}   | {N}     |

By Category:
  Refactor:     {N} findings ({N} fixed)
  Quality:      {N} findings ({N} fixed)
  Tech Debt:    {N} findings ({N} fixed)
  Performance:  {N} findings ({N} fixed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Applied Fixes ({N}/{N})
───────────────────────
1. [{severity}] {file}:{line} — {description}
2. [{severity}] {file}:{line} — {description}
...

Skipped ({N})
─────────────
1. [{severity}] {file}:{line} — {reason for skipping}
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verification
────────────
Lint check: {PASS|FAIL}
  {lint details if any errors}

Files modified: {N}
  {list of modified files}
```

## Compact Report (for small diffs)

When there are fewer than 5 findings total, use this shorter format:

```
Simplify: {N} files reviewed, {N} findings, {N} fixed

Fixes applied:
  1. {file} — {description}
  2. {file} — {description}

Lint check: PASS
```
