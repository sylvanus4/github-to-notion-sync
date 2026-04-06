# GitHub Label Taxonomy

## Existing Labels (already on repo)

These labels are actively used in the repository. Release operations integrate with them directly.

### Change Type Labels

| Label | Color | Description | Release Ops Usage |
|---|---|---|---|
| `bug` | `#D73A4A` (red) | Something isn't working | Classify as fix; default `risk:medium` |
| `enhancement` | `#A2EEEF` (teal) | New feature or request | Classify as improvement; default `risk:medium` |
| `feature` | `#EDEDED` (gray) | Feature work | Classify as new functionality; default `risk:medium` |
| `refactoring` | `#B59476` (brown) | Code refactoring | No behavior change; default `risk:low` |
| `performance` | `#EDEDED` (gray) | Performance improvement | Behavior change possible; default `risk:medium` |
| `chore` | `#FBCA04` (yellow) | Build process, infrastructure, maintenance | Non-user-facing; default `risk:low` |
| `security` | `#D73A4A` (red) | Security-related change | Broad impact; default `risk:high` |

### Area Labels

| Label | Color | Description |
|---|---|---|
| `backend` | `#EDEDED` (gray) | Backend service changes |
| `pods-service` | `#EDEDED` (gray) | Pods service area |
| `workloads-eda` | `#5319E7` (purple) | Workloads EDA Migration |

### Severity Labels

| Label | Color | Description |
|---|---|---|
| `severity:critical` | `#B60205` (dark red) | Critical severity — maps to `risk:high` |

### Process Labels

| Label | Color | Description |
|---|---|---|
| `deployment` | `#0E8A16` (green) | Deployment and infrastructure tasks |
| `testing` | `#1D76DB` (blue) | Testing and verification tasks |

### Automation Labels

| Label | Color | Description |
|---|---|---|
| `automated` | `#EDEDED` (gray) | Auto-generated changes |
| `dependencies` | `#0366D6` (blue) | Dependency updates (Dependabot) |
| `github_actions` | `#000000` (black) | GitHub Actions code changes |

### Other Labels (not directly used in release ops)

| Label | Color | Description |
|---|---|---|
| `documentation` | `#0075CA` | Docs improvements |
| `duplicate` | `#CFD3D7` | Duplicate issue/PR |
| `good first issue` | `#7057FF` | Good for newcomers |
| `help wanted` | `#008672` | Extra attention needed |
| `invalid` | `#E4E669` | Not valid |
| `question` | `#D876E3` | Information request |
| `wontfix` | `#FFFFFF` | Will not be worked on |
| `epic` | `#FF82FF` | Epic tracking |
| `weekly-scan-test` | `#C5DEF5` | Weekly scan test |

---

## New Labels (to be created for release ops)

### Release Cycle Labels

| Label | Color | Description | Usage |
|---|---|---|---|
| `release:thu` | `#0E8A16` (green) | Weekly Thursday release candidate | Applied to PRs targeting the regular weekly release |
| `hotfix` | `#D93F0B` (red) | Urgent fix outside the regular cycle | Applied to PRs requiring immediate deployment |

**Mutual exclusion**: `release:thu` and `hotfix` MUST NOT coexist on the same PR.

### QA Status Labels

| Label | Color | Description |
|---|---|---|
| `qa:needed` | `#FBCA04` (yellow) | QA testing required |
| `qa:done` | `#0E8A16` (green) | QA testing completed and passed |

Transition: `qa:needed` is applied at collection; replaced with `qa:done` after QA pass.

### Risk Classification Labels

| Label | Color | Description |
|---|---|---|
| `risk:low` | `#C2E0C6` (light green) | Low risk — minor changes, well-tested path |
| `risk:medium` | `#FEF2C0` (light yellow) | Medium risk — moderate scope, some new paths |
| `risk:high` | `#F9D0C4` (light red) | High risk — large scope, new infra, or data migration |

---

## Label Setup Commands

Run once per repository to create the release-specific labels:

```bash
# Release cycle
gh label create "release:thu" --color "0E8A16" --description "Weekly Thursday release candidate"
gh label create "hotfix" --color "D93F0B" --description "Urgent fix outside regular cycle"

# QA status
gh label create "qa:needed" --color "FBCA04" --description "QA testing required"
gh label create "qa:done" --color "0E8A16" --description "QA testing completed"

# Risk classification
gh label create "risk:low" --color "C2E0C6" --description "Low risk change"
gh label create "risk:medium" --color "FEF2C0" --description "Medium risk change"
gh label create "risk:high" --color "F9D0C4" --description "High risk change"
```

---

## Risk Auto-Mapping from Existing Labels

When a PR already has existing labels, the release collector can suggest a default risk level:

| Existing label(s) | Suggested risk | Rationale |
|---|---|---|
| `dependencies` or `automated` | `risk:low` | Auto-generated, scoped changes |
| `refactoring` or `chore` or `testing` | `risk:low` | No user-facing behavior change |
| `bug` or `performance` | `risk:medium` | Behavior change, but targeted fix |
| `security` or `severity:critical` | `risk:high` | Broad impact, requires careful rollback plan |
| `deployment` or `feature` or `enhancement` | `risk:medium` | New functionality or infra change — assess per case |

The suggested risk is a **default**; the PR author or release owner can override it.

---

## Validation Rules

1. Every PR with `release:thu` or `hotfix` MUST also have at least one area label (`backend`, `pods-service`, `workloads-eda`) or change type label (`bug`, `enhancement`, `feature`, etc.)
2. Every PR with `release:thu` MUST have exactly one `risk:*` label
3. `qa:needed` is applied during Tuesday collection on all `release:thu` PRs
4. `qa:done` replaces `qa:needed` — they should not coexist
5. `release:thu` + `hotfix` on the same PR is a configuration error
6. PRs with `severity:critical` that also carry `release:thu` MUST be `risk:high`
