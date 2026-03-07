## Release Prep

Orchestrated workflow to prepare a release — generates release notes, assesses risk, validates CI, and checks deployment readiness.

### Usage

```
/release-prep [optional: target version or branch]
```

### Workflow

1. Read the mission-control skill at `.cursor/skills/mission-control/SKILL.md`
2. Follow **WF-3: Release Prep** defined there
3. Execute in this order:

**Step 1: Diff Analysis**
- Run `git log --oneline main..HEAD` (or `dev..HEAD`) to list all commits in the release
- Run `git diff --stat main..HEAD` to understand the scope of changes

**Step 2: Parallel Batch (Task subagents)**
- **pr-review-captain** (`.cursor/skills/pr-review-captain/SKILL.md`): Analyze all changes, generate risk assessment, create review checklist
- **technical-writer** (`.cursor/skills/technical-writer/SKILL.md`): Generate release notes and changelog from commit history

**Step 3: Deployment Readiness**
- **sre-devops-expert** (`.cursor/skills/sre-devops-expert/SKILL.md`): Review Helm values, Docker configs, check for breaking infrastructure changes, validate rollback strategy

**Step 4: CI Validation**
- **ci-quality-gate** (`.cursor/skills/ci-quality-gate/SKILL.md`): Run full CI pipeline locally to ensure all checks pass

**Step 5: Release Report**
Aggregate all results into a release preparation report.

### Output

```
Release Preparation Report
==========================
Version: [version/branch]
Date: [YYYY-MM-DD]
Commits: [N] commits since last release

Release Notes:
  [Generated changelog]

Risk Assessment:
  Overall Risk: [Low / Medium / High]
  Breaking Changes: [Yes / No]
  Migration Required: [Yes / No]
  Rollback Plan: [Available / Needs attention]

CI Status: [PASS / FAIL]

Deployment Checklist:
  - [ ] All CI checks pass
  - [ ] Release notes reviewed
  - [ ] Helm values updated
  - [ ] DB migrations tested
  - [ ] Rollback procedure documented
  - [ ] Monitoring/alerting configured

Recommendation: [Ready to release / Needs attention on X items]
```
