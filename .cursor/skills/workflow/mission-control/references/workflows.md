# Predefined Workflows

> **Note**: Many workflows reference planned skills that are not yet implemented.
> When a referenced skill does not exist, handle the step inline (use general
> subagent capabilities) or skip it with a note in the report.

## WF-1: Full Quality Audit (`/full-quality-audit`)

**Parallel batch 1** (read-only analysis):
1. ci-quality-gate → lint, test, build results
2. security-expert → STRIDE, OWASP, secrets
3. compliance-governance → data governance, access control

**Sequential** (after batch 1):
4. Aggregate findings → generate unified report
5. Auto-fix if applicable (ruff --fix, black, eslint --fix)
6. domain-commit → commit fixes

## WF-2: Feature Pipeline (`/feature-pipeline`)

**Sequential**:
1. Analyze spec/requirements
2. **Parallel**: backend-expert (API design) + frontend-expert (component design)
3. Implement code changes
4. **Parallel**: qa-test-expert (test plan) + e2e-testing (write tests)
5. pr-review-captain → review changes
6. domain-commit → split commits
7. Create PR

## WF-3: Release Prep (`/release-prep`)

**Parallel batch 1**:
1. pr-review-captain → diff analysis, risk assessment
2. technical-writer → release notes, changelog

**Sequential**:
3. sre-devops-expert → deployment readiness check
4. ci-quality-gate → full CI validation
5. Generate release preparation report

## WF-4: Incident Response (`/incident-response`)

**Sequential** (time-critical):
1. service-health-doctor → status check, identify down services
2. Diagnose root cause (logs, metrics)
3. **Parallel**: backend-expert + db-expert → root cause analysis
4. Apply fix
5. service-health-doctor → verify recovery
6. technical-writer → postmortem document

## WF-5: Dependency Sweep (`/dependency-sweep`)

**Sequential**:
1. dependency-auditor → full scan across Python/Go/Node
2. Apply safe patch updates
3. ci-quality-gate → verify updates don't break anything
4. domain-commit → commit per domain (Python/Go/Frontend)

## WF-6: i18n Check (`/i18n-check`)

**Sequential**:
1. i18n-sync → detect missing keys, generate drafts
2. User review of translations
3. Apply confirmed translations
4. domain-commit → commit translation changes
