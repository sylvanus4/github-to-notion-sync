---
name: iac-review-agent
description: >-
  Unified Infrastructure-as-Code review agent that detects IaC file types in
  diffs (Helm, Terraform, K8s manifests) and routes to the appropriate
  validator. Orchestrates helm-validator, terraform-reviewer, and
  k8s-manifest-validator into a single review pass. Use when the user asks to
  "review infrastructure code", "IaC review", "validate infra changes",
  "인프라 코드 리뷰", "IaC 검증", "iac-review-agent", or any unified IaC
  validation. Do NOT use for application code review (use deep-review),
  CI/CD pipeline review (use sre-devops-expert), or single-tool validation
  (use the specific validator skill directly).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# IaC Review Agent

Unified orchestrator for Infrastructure-as-Code review. Detects IaC file types in the change set, routes to specialized validators, aggregates results, and optionally posts as PR review comments.

## When to Use

- As the 5th agent in the `deep-review` pipeline (alongside Frontend, Backend, Security, Test Coverage)
- Before merging any PR that touches infrastructure files
- As a standalone IaC quality gate in CI/CD

## Workflow

### Step 1: Detect IaC Files in Scope

Classify changed files by IaC type:

| Pattern | Type | Router Target |
|---------|------|---------------|
| `Chart.yaml`, `templates/*.yaml`, `values*.yaml` in chart dirs | Helm | `helm-validator` |
| `*.tf`, `*.tfvars`, `*.terraform.lock.hcl` | Terraform | `terraform-reviewer` |
| `*.yaml`/`*.yml` with `kind:` field (non-Helm) | K8s Manifest | `k8s-manifest-validator` |
| `docker-compose*.yml`, `Dockerfile*` | Docker | LLM review only |
| `.github/workflows/*.yml` | CI/CD | LLM review only |

If no IaC files are detected, report "No IaC files in scope" and exit.

### Step 2: Launch Parallel Validators

For each detected IaC type, launch the corresponding validator as a subagent:

```
Subagent 1 (if Helm files):      helm-validator
Subagent 2 (if Terraform files):  terraform-reviewer
Subagent 3 (if K8s manifests):    k8s-manifest-validator
```

Configuration:
- `subagent_type`: `generalPurpose`
- `model`: default (not fast — IaC review benefits from deeper reasoning)
- Max 3 parallel subagents

Each validator returns its own structured report.

### Step 3: Docker/CI LLM Review

For Docker and CI/CD files not covered by specialized validators, perform direct LLM review:

**Dockerfile checks**:
- Multi-stage builds, non-root user, pinned base images, `.dockerignore`
- COPY vs ADD, layer ordering for cache efficiency
- Health check instructions

**CI/CD checks**:
- Secret handling (no hardcoded values)
- Caching configuration, parallel job structure
- Deployment safety (rollback on failure, canary/blue-green)

### Step 4: Aggregate Results

Merge all validator reports into a unified IaC review:

```
IaC Review Report
=================
Scope: git diff (12 files changed)
IaC Types Detected: Helm (3 charts), K8s (5 manifests), Docker (2 files)

Overall Status: FAIL (1 critical finding)

HELM CHARTS
───────────
helm/api-server/     PASS    0 errors, 1 warning
helm/worker/         FAIL    1 schema error (deprecated API)
helm/monitoring/     PASS    Clean

K8s MANIFESTS
─────────────
infra/k8s/           WARN    2 policy warnings (missing probes)

DOCKER
──────
Dockerfile.api       PASS    Multi-stage, non-root
Dockerfile.worker    WARN    Using latest base image

CRITICAL FINDINGS (must fix before merge):
1. [High] helm/worker: CronJob using batch/v1beta1 (removed in K8s 1.25)

WARNINGS (recommended fixes):
1. [Medium] infra/k8s/deployment.yaml: No readOnlyRootFilesystem
2. [Medium] Dockerfile.worker: Pin base image version
```

### Step 5: Post as PR Review (Optional)

If invoked in PR context, post findings as GitHub PR review comments using the GitHub MCP:

- Critical/High findings → "Request Changes" review
- Medium/Low only → "Comment" review
- All pass → "Approve" review

## Integration with deep-review

When called from `deep-review`, this agent runs as Agent 5 alongside the existing 4 agents. The `deep-review` orchestrator should detect IaC files in the diff and spawn this agent in parallel.

## Examples

### Example 1: Full IaC review
User says: "Review infrastructure changes"
Actions:
1. Detect IaC types in git diff
2. Launch parallel validators
3. Perform Docker/CI LLM review
4. Aggregate into unified report
Result: Combined IaC report across all detected types

### Example 2: PR review mode
User says: "Review IaC in PR #42"
Actions:
1. Fetch PR diff
2. Classify and route IaC files
3. Run validators and aggregate
4. Post review comments on PR
Result: PR annotated with IaC findings

## Error Handling

| Error | Action |
|-------|--------|
| no IaC files detected | Report "No IaC files in scope" and exit; suggest user verify diff or scope |
| validator subagent fails | Capture subagent error; report partial results with failed validator noted |
| GitHub MCP auth error | Skip PR comment posting; return report as text output; suggest `gh auth login` |
| PR comment API failure | Retry once; on failure, return report for manual posting |
| mixed IaC types in single directory | Route each file to correct validator by type; aggregate all results |
