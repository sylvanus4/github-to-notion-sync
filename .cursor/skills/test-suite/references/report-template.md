# Test Suite Report Template

Use this template when presenting the final report to the user.

## Full Report

```
Test Suite Report
=================
Date: {YYYY-MM-DD}
Scope: {diff|today|full} — {N} source files, {N} test files
Analysis Time: {N} seconds

Pipeline: review → {generate|skip} → {execute|skip}

Agents Completed: {N}/4
  Test Coverage Agent:  Done ({N} findings)
  Test Quality Agent:   Done ({N} findings)
  Test Generator Agent: Done ({N} tests created, {N} tests modified)
  Test Runner Agent:    Done ({N}/{N} passed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Coverage Analysis
─────────────────
Source files:        {N}
Source files tested: {N} ({N}%)
Untested files:      {N}

| Severity | Coverage Gaps | Quality Issues | Total |
|----------|--------------|----------------|-------|
| Critical | {N}          | {N}            | {N}   |
| High     | {N}          | {N}            | {N}   |
| Medium   | {N}          | {N}            | {N}   |
| Low      | {N}          | {N}            | {N}   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated Tests
───────────────
New test files:     {N}
New test cases:     {N}
Modified tests:     {N}
Skipped:            {N}

Files created:
  1. {path} — {N} test cases ({description})
  2. {path} — {N} test cases ({description})
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Execution Results
─────────────────
Framework: {name}
Command:   {test command}

| Metric   | Count |
|----------|-------|
| Total    | {N}   |
| Passed   | {N}   |
| Failed   | {N}   |
| Skipped  | {N}   |
| Duration | {N}s  |
| Retries  | {N}   |

{if failures remain}
Remaining Failures:
  1. {test name} — {error} [{type}]
  2. {test name} — {error} [{type}]
{end if}

{if bugs found}
Bugs Found by Tests:
  1. {source file} — {description}
  2. {source file} — {description}
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verification
────────────
Lint check: {PASS|FAIL}
Files modified: {N}
  {list of modified files}
```

## Compact Report (for small scopes)

When there are fewer than 5 findings total, use this shorter format:

```
Test Suite: {N} source files, {N} test files

Findings: {N} coverage gaps, {N} quality issues
Generated: {N} new tests in {N} files
Execution: {N}/{N} passed ({N}s)

Lint check: PASS
```

## Review-Only Report (when --no-gen --no-run)

When generation and execution are skipped:

```
Test Suite Review
=================
Scope: {diff|today|full} — {N} source files, {N} test files

Coverage:
  Tested: {N}/{N} source files ({N}%)
  Gaps: {list of untested files with priority}

Quality:
  {N} findings ({breakdown by severity})

Top Recommendations:
  1. [{severity}] {description}
  2. [{severity}] {description}
  ...
```
