---
description: "Run 6-phase verification loop: build, type check, lint, test, security scan, diff review"
---

# ECC Verify — 6-Phase Verification Loop

## Skill Reference

Read and follow the skill at `.cursor/skills/ecc-verification-loop/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Determine Scope

- **No arguments**: Verify all changed files (git diff)
- **all / full**: Verify the entire project
- **<path>**: Verify specific file or directory

### Step 2: Run 6 Phases

Execute each phase sequentially; stop and report on first failure:

1. **Build** — Run the project build command (if applicable)
2. **Type Check** — Run type checker (mypy, tsc, etc.)
3. **Lint** — Run linters (ruff, eslint, etc.)
4. **Test** — Run the test suite for affected files
5. **Security** — Run security scan (check for secrets, known vulnerabilities)
6. **Diff Review** — Review staged/unstaged changes for quality

### Step 3: Report

Produce a structured report:

```
Phase       | Status | Details
------------|--------|--------
Build       | PASS   | ...
Type Check  | PASS   | ...
Lint        | FAIL   | 2 errors in stock_screener.py
Test        | SKIP   | (blocked by lint failure)
Security    | SKIP   |
Diff Review | SKIP   |
```

## Constraints

- Skip phases that don't apply to the project stack (e.g., no tsc for Python-only changes)
- Always run security scan on files touching .env, credentials, or API keys
- Report coverage stats from test phase when available
