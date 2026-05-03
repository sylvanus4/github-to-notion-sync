---
name: ci-quality-gate
description: Run the full CI pipeline locally (secret scan, lint, test, build, schema check) and produce a pass/fail report. Use before pushing commits or after large refactors.
disable-model-invocation: true
---

# CI Quality Gate

Reproduces the GitHub Actions CI pipeline locally and aggregates results.

## Execution Steps

Run 8 sequential gates:

1. **Secret Scan**: `gitleaks detect --source .`
2. **Python Lint**: `ruff check .` + `ruff format --check .`
3. **Python Type Check**: `mypy` on critical services
4. **Python Security**: `bandit -r services/ -c pyproject.toml`
5. **Python Tests**: `pytest tests/ -x --tb=short`
6. **Go Build/Test**: `cd services/call-manager && go build ./... && go test ./...`
7. **Frontend Lint/Type/Test/Build**: `cd frontend && pnpm lint && pnpm tsc && pnpm test && pnpm build`
8. **Schema Check**: Verify Alembic heads are linear

## Report Format

```
CI Quality Gate Report
═══════════════════════
Gate 1: Secret Scan      ✅ PASS
Gate 2: Python Lint       ✅ PASS
Gate 3: Python Types      ⚠️ SKIP (mypy not configured)
Gate 4: Python Security   ✅ PASS
Gate 5: Python Tests      ❌ FAIL (3 failures)
Gate 6: Go Build/Test     ✅ PASS
Gate 7: Frontend          ✅ PASS
Gate 8: Schema Check      ✅ PASS
═══════════════════════
Result: FAIL (1 gate failed)
```

## Auto-Fix Mode

When asked to "run CI and fix": execute all gates first, then auto-fix lint/format issues and re-run failed gates.

## Prerequisites

Requires Python 3.11+, ruff, Go 1.22+, Node 20+, gitleaks. Missing tools marked as SKIPPED.

Do NOT use for: dependency audits (use dependency-auditor), test strategy (use qa-test-expert).
