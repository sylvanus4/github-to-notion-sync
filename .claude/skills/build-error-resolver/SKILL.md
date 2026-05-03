---
name: build-error-resolver
description: >-
  Dedicated skill for resolving build/compile errors across Python, Node.js,
  and Go — runs build, parses errors, classifies, fixes in priority order, and
  re-runs until clean.
---

# Build Error Resolver

Resolve build and compile errors systematically across the project's multi-language stack. Runs the build command, parses structured error output, classifies each error, fixes them in priority order, and re-runs until the build is clean or max cycles are reached.

## Trigger Phrases

- "fix build", "build errors", "compile errors", "resolve build failures"
- "빌드 에러 수정", "컴파일 에러", "빌드 수정"
- `/build-fix` command

## Do NOT Use For

- Runtime errors or exceptions (use `diagnose`)
- Lint-only issues without build failure (use `ci-quality-gate`)
- General code review (use `deep-review` or `simplify`)
- Broad QA cycling across tests, lint, and typecheck (use `omc-ultraqa`)
- Single known bug diagnosis (use `diagnose`)

## Supported Build Stacks

| Stack | Build Command | Error Parser |
|-------|---------------|--------------|
| Python | `ruff check`, `mypy`, `python -m py_compile` | Structured ruff JSON, mypy output |
| Node.js | `tsc --noEmit`, `vite build`, `esbuild` | TypeScript diagnostics, Vite errors |
| Go | `go build ./...`, `go vet ./...` | Go compiler output |

## Error Classification Priority

Errors are fixed in this order (highest priority first):

1. **Syntax errors** — Prevents any further compilation
2. **Missing imports** — Quick fixes, unblocks dependent errors
3. **Type mismatches** — Core logic errors
4. **Undefined references** — Missing functions, variables, types
5. **Configuration errors** — Build config, tsconfig, pyproject.toml issues
6. **Deprecation/compatibility** — API changes, version mismatches

## Workflow

### Step 1: Detect Language
- If `--lang` flag provided, use that
- Otherwise auto-detect from project files: `pyproject.toml`/`setup.py` → Python, `tsconfig.json`/`package.json` → Node.js, `go.mod` → Go
- If multiple stacks present, run all in sequence

### Step 2: Run Build
```bash
# Python
ruff check . --output-format json 2>&1; mypy . 2>&1

# Node.js
npx tsc --noEmit 2>&1

# Go
go build ./... 2>&1
```

### Step 3: Parse & Classify
- Extract file path, line number, error code, and message
- Classify each error into the priority categories above
- Group errors by file for efficient batch fixing

### Step 4: Fix (Priority Order)
- Fix all syntax errors first across all files
- Then missing imports
- Then type mismatches (may require reading surrounding code)
- Continue through the priority list
- After each category, re-run the build to check for cascade fixes

### Step 5: Re-run Build
- After fixing a batch, re-run the build command
- If new errors appear, return to Step 3
- **Max 5 cycles** — if errors persist after 5 iterations, stop and report remaining issues

### Step 6: Report
Output a structured summary:
```
Build Error Resolution Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stack: Python (ruff + mypy)
Cycles: 3/5
Initial errors: 14
Fixed: 12
Remaining: 2

Fixed:
  ✓ backend/app/services/foo.py:23 — Missing import (os)
  ✓ backend/app/models/bar.py:45 — Type mismatch (str vs int)
  ...

Remaining (manual review needed):
  ✗ backend/app/utils/baz.py:67 — Circular import detected
  ✗ scripts/migrate.py:12 — Missing external dependency
```

## Guardrails

- **Max 5 fix cycles** — prevents infinite loops
- **Early exit on repeated failures** — if the same error appears in 2 consecutive cycles, flag it and move on
- **No refactoring** — only fix build errors, do not restructure code
- **Preserve existing tests** — never modify test files to fix build errors (fix the source instead)
- If a fix requires installing a new dependency, ask the user first

## Examples

### Example 1: Auto-detect and Fix
```
User: "Fix the build errors"
Agent: Detects Python + Node.js stacks → Runs ruff/mypy/tsc → Fixes 8 errors in 2 cycles → Reports clean build
```

### Example 2: Specific Stack
```
User: "/build-fix --lang python"
Agent: Runs ruff + mypy only → Fixes Python errors → Reports
```

### Example 3: Custom Command
```
User: "/build-fix --cmd 'make build'"
Agent: Runs `make build` → Parses output → Fixes errors → Re-runs until clean
```

## Error Handling

- If the build command is not found (e.g., `tsc` not installed), report and suggest installation
- If the project has no build configuration, inform the user and suggest creating one
- If all errors are in generated/vendor files, skip them and report
