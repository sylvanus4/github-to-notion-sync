---
name: ci-quality-gate
description: Run the full CI pipeline locally (secret scan, Python lint/test, Go lint/test, frontend lint/test/build, schema check) and produce a pass/fail report. Use when the user asks to run CI locally, check quality before pushing, or validate all checks pass. Do NOT use for individual dependency audits (use dependency-auditor) or test strategy design (use qa-test-expert).
metadata:
  version: "1.0.0"
  category: execution
---

# CI Quality Gate

Reproduces the GitHub Actions CI pipeline (`.github/workflows/ci.yml`) on the local machine and aggregates results into a single pass/fail report.

## When to Use

- Before pushing commits to verify CI will pass
- After large refactors to catch regressions across stacks
- As part of the `/full-quality-audit` workflow (called by mission-control)

## Prerequisites

Requires Python 3.11+, ruff, black, mypy, Go 1.22+, Node 20+, and gitleaks. Missing tools are marked as `SKIPPED` in the report.

## Execution Steps

Run 8 sequential gates: Secret Scan, Python Lint/Type/Security, Python Tests, Go Build/Test, Frontend Lint/Type/Test/Build, and Schema Check. For detailed commands and per-gate instructions, see [references/execution-steps.md](references/execution-steps.md).

### Step 8: Aggregate Report

Combine all results into a structured report.

## Examples

### Example 1: Pre-push validation
User says: "Run CI checks before I push"
Actions:
1. Execute all 8 gates sequentially (secret scan through schema check)
2. Collect pass/fail/skip status for each gate
3. Generate aggregated report
Result: CI Quality Gate Report showing all gates with pass/fail status

### Example 2: Auto-fix mode
User says: "Run CI and fix what you can"
Actions:
1. Run all gates to identify failures
2. Apply auto-fixes (ruff --fix, black, eslint --fix)
3. Re-run affected gates
Result: Updated report showing fixed items and remaining issues

## Troubleshooting

### Tool not found errors
Cause: Required tool (ruff, black, mypy, etc.) not installed
Solution: Gate is marked SKIPPED; install the missing tool or run `make setup`

### Python test import failures
Cause: Service dependencies not installed locally
Solution: Run `pip install -e shared/python && pip install -e services/SERVICE`

## Output Format

```
CI Quality Gate Report
======================
Date: [YYYY-MM-DD HH:MM]
Branch: [current branch]

Gate                    Status    Details
─────────────────────── ───────── ──────────────────────
Secret scan             PASS      0 secrets found
Python lint (ruff)      PASS      0 issues
Python format (black)   PASS      0 files reformatted
Python types (mypy)     PASS      0 errors
Python security         WARN      2 pip-audit advisories
Python tests            PASS      42 passed, 0 failed
Go build                PASS      compiled successfully
Go test                 PASS      15 passed
Go lint                 SKIPPED   golangci-lint not found
Frontend lint           PASS      0 issues
Frontend type-check     PASS      0 errors
Frontend unit tests     PASS      87 passed
Frontend build          PASS      bundle size: 1.2 MB
Schema check            PASS      init.sql matches migrations

Overall: PASS (1 warning, 1 skipped)
```

## Auto-Fix Mode

When invoked with `--fix` intent, attempt automatic repairs:

1. `ruff check --fix shared/ services/` for auto-fixable Python lint
2. `black shared/ services/` for formatting
3. `npm run lint -- --fix` for frontend lint

After fixes, re-run the affected gates and update the report.

## Error Handling

- If a tool is not installed, mark the gate as `SKIPPED` and continue
- If a gate fails, continue running remaining gates (do not short-circuit)
- Collect all failures to present a complete picture
- Suggest `make setup` if multiple tools are missing

## Integration with Other Skills

- **mission-control**: Invokes this skill as part of quality audit workflows
- **domain-commit**: Run this skill before committing to ensure clean state
- **pr-review-captain**: Reference this report in PR descriptions
- **dependency-auditor**: pip-audit / npm audit results feed into dependency analysis
