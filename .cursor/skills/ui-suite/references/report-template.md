# UI Suite Report Template

Use this template when presenting the final report to the user after all fixes have been applied.

## Full Report

```
UI Suite Report
===============
Date: {YYYY-MM-DD}
Scope: {diff|today|full} — {N} UI files reviewed
Analysis Time: {N} seconds

Agents Completed: {N}/4
  Design Audit Agent:      Done ({N} findings)
  Web Standards Agent:     Done ({N} findings)
  UX/Design System Agent:  Done ({N} findings)
  UI Builder Agent:        Done ({N} fixes applied)

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

By Domain:
  Design Audit:      {N} findings ({N} fixed)
  Web Standards:     {N} findings ({N} fixed)
  UX/Design System:  {N} findings ({N} fixed)

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
UI Suite: {N} files reviewed, {N} findings, {N} fixed

Fixes applied:
  1. {file} — {description}
  2. {file} — {description}

Lint check: PASS
```
