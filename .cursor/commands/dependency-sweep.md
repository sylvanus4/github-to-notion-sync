## Dependency Sweep

Orchestrated workflow to audit all dependencies, apply safe updates, verify with CI, and commit changes per domain.

### Usage

```
/dependency-sweep
```

### Workflow

1. Read the mission-control skill at `.cursor/skills/mission-control/SKILL.md`
2. Follow **WF-5: Dependency Sweep** defined there
3. Execute sequentially:

**Step 1: Full Audit**
- **dependency-auditor** (`.cursor/skills/dependency-auditor/SKILL.md`): Scan all dependency files across the stack:
  - Python: `shared/python/pyproject.toml`, `services/*/pyproject.toml`, `pyproject.toml`, `uv.lock`
  - Go: `services/call-manager/go.mod`, `services/call-manager/go.sum`
  - Node.js: `frontend/package.json`, `frontend/package-lock.json`
  - Other: `services/telephony-stack/scripts/requirements.txt`
- Classify vulnerabilities by severity (Critical / High / Medium / Low)
- Identify available patch, minor, and major updates

**Step 2: Safe Patch Updates**
- Apply patch-level updates automatically (e.g., 1.2.3 → 1.2.4)
- For each update, run the relevant test suite to verify compatibility
- Revert any update that causes test failures

**Step 3: CI Verification**
- **ci-quality-gate** (`.cursor/skills/ci-quality-gate/SKILL.md`): Run the full CI pipeline to verify all updates work together
- If CI fails, identify the breaking update and revert it

**Step 4: Domain Commits**
- **domain-commit** (`.cursor/skills/domain-commit/SKILL.md`): Commit dependency changes split by domain:
  - `[chore] Update Python dependencies` — `shared/`, `services/` pyproject.toml changes
  - `[chore] Update Go dependencies` — `services/call-manager/go.mod`, `go.sum`
  - `[chore] Update frontend dependencies` — `frontend/package.json`, `package-lock.json`

**Step 5: Report**
- Update `tasks/dependency-audit.md` with the latest audit results
- Report summary of changes

### Output

```
Dependency Sweep Report
=======================
Date: [YYYY-MM-DD]

Vulnerabilities:
  Before: Critical [N], High [N], Medium [N], Low [N]
  After:  Critical [N], High [N], Medium [N], Low [N]

Updates Applied:
  Python: [N] packages updated
  Go: [N] modules updated
  Node.js: [N] packages updated

CI Status: [PASS / FAIL]

Major Updates Available (manual review needed):
  [list of major updates with impact notes]
```
