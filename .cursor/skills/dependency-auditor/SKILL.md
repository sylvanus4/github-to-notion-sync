---
name: dependency-auditor
description: Audit and update Python, Go, and Node.js dependencies — scan for CVEs, classify severity, apply safe patch updates, and generate impact reports for major updates. Use when the user asks to audit dependencies, update packages, check for vulnerabilities, or run a dependency sweep. Do NOT use for general security reviews or threat modeling (use security-expert) or running the full CI pipeline (use ci-quality-gate).
metadata:
  version: "1.0.0"
  category: execution
---

# Dependency Auditor

Manages dependencies across the entire polyglot stack (19 Python services, 1 Go service, 1 Node.js frontend).

## When to Use

- Periodic dependency health checks
- After Dependabot PRs to verify compatibility
- Before releases to ensure no known CVEs
- As part of the `/dependency-sweep` workflow (called by mission-control)

## Dependency Map

### Python (20 packages)

| Scope | File | Package Manager |
|-------|------|----------------|
| Shared library | `shared/python/pyproject.toml` | pip / uv |
| 19 services | `services/*/pyproject.toml` | pip / uv |
| Root workspace | `pyproject.toml` | pip / uv |
| Lock file | `uv.lock` | uv |

### Go (1 service)

| Scope | File |
|-------|------|
| call-manager | `services/call-manager/go.mod` |
| Lock file | `services/call-manager/go.sum` |

### Node.js (1 app)

| Scope | File |
|-------|------|
| Frontend | `frontend/package.json` |
| Lock file | `frontend/package-lock.json` |

### Other

| Scope | File |
|-------|------|
| Telephony scripts | `services/telephony-stack/scripts/requirements.txt` |

## Execution Steps

### Step 1: Vulnerability Scan

Run all scanners in parallel (use Task tool subagents):

**Python:**
```bash
pip-audit --strict --desc on 2>&1
```

**Go:**
```bash
cd services/call-manager && go list -m -json all | go run golang.org/x/vuln/cmd/govulncheck@latest ./... 2>&1 || true
```

**Node.js:**
```bash
cd frontend && npm audit --audit-level=low 2>&1
```

### Step 2: Classify Findings

Categorize each finding:

| Severity | Action | Automation |
|----------|--------|-----------|
| Critical | Immediate patch | Auto-apply if patch available |
| High | Patch within 24h | Auto-apply if patch available |
| Medium | Patch within 1 week | Report only |
| Low | Track in backlog | Report only |

### Step 3: Identify Available Updates

**Python:**
```bash
pip list --outdated --format=json
```

Or with uv:
```bash
uv pip list --outdated 2>/dev/null || pip list --outdated --format=json
```

**Go:**
```bash
cd services/call-manager && go list -m -u all 2>&1
```

**Node.js:**
```bash
cd frontend && npm outdated --json 2>&1
```

### Step 4: Apply Safe Updates

Only apply **patch-level** updates automatically (e.g., 1.2.3 → 1.2.4). For each update:

1. Record current version
2. Apply update
3. Run relevant tests:
   - Python: `pytest services/SERVICE/tests/ -x --tb=short`
   - Go: `cd services/call-manager && go test ./...`
   - Frontend: `cd frontend && npm test`
4. If tests fail, revert and flag as manual review needed

**Python patch update:**
```bash
pip install --upgrade PACKAGE==NEW_VERSION
```

**Go patch update:**
```bash
cd services/call-manager && go get PACKAGE@vNEW_VERSION && go mod tidy
```

**Node.js patch update:**
```bash
cd frontend && npm update PACKAGE
```

### Step 5: Major Update Impact Analysis

For minor/major updates, do NOT auto-apply. Instead, generate an impact report:

1. Read the package changelog/release notes
2. Check breaking changes
3. List affected files via `grep -r "import PACKAGE" services/ shared/`
4. Estimate migration effort (Low / Medium / High)

### Step 6: Update Audit Report

Append or update the audit report in `tasks/dependency-audit.md`.

## Examples

### Example 1: Vulnerability scan
User says: "Check our dependencies for security issues"
Actions:
1. Run pip-audit, govulncheck, and npm audit in parallel
2. Classify findings by severity
3. Auto-apply critical/high patch updates with test verification
Result: Dependency Audit Report with CVE list and patch status

### Example 2: Dependency sweep
User says: "Update all safe dependencies"
Actions:
1. Scan all outdated packages across Python/Go/Node
2. Apply patch-level updates automatically
3. Run tests after each update; revert if tests fail
Result: Updated packages with test verification results

## Troubleshooting

### pip-audit fails with resolver errors
Cause: Conflicting dependency versions in pyproject.toml
Solution: Run `uv pip compile` to check for conflicts, then resolve manually

### npm audit false positives
Cause: Vulnerability in dev dependency not used in production
Solution: Add to `.npmrc` audit exceptions or document as accepted risk

## Output Format

```
Dependency Audit Report
=======================
Date: [YYYY-MM-DD]
Scanned: [N] Python packages, [M] Go modules, [K] npm packages

Vulnerabilities Found:
  Critical: [N] | High: [N] | Medium: [N] | Low: [N]

  [SEVERITY] [CVE-ID] [Package] [Current] → [Fixed]
    Description: [brief]
    Affected: [service(s)]

Updates Applied (patch-level):
  ✓ [Package] [Old] → [New] — tests passed
  ✗ [Package] [Old] → [New] — tests failed, reverted

Major Updates Available (manual review):
  [Package] [Current] → [Available] — breaking changes: [Yes/No]
  Impact: [Low/Medium/High] — [N] files affected

Outdated Summary:
  Python: [N] outdated / [M] total
  Go: [N] outdated / [M] total
  Node.js: [N] outdated / [M] total
```

## Integration with Other Skills

- **mission-control**: Called during `/dependency-sweep` workflow
- **ci-quality-gate**: Shares pip-audit and npm audit results
- **security-expert**: CVE findings feed into security review
- **domain-commit**: After updates, commit changes split by domain (Python/Go/Frontend)
