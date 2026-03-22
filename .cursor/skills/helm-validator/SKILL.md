---
name: helm-validator
description: >-
  Validate Helm charts using helm lint, helm template rendering, kubeconform
  schema validation, and kube-score/Polaris policy checks. Produces a structured
  pass/fail report with fix suggestions. Use when the user asks to "validate
  Helm chart", "lint Helm", "check Helm chart", "Helm 검증", "Helm 차트 린트",
  "helm-validator", or any Helm chart quality/security validation request.
  Do NOT use for general K8s manifest validation without Helm (use
  k8s-manifest-validator), Terraform review (use terraform-reviewer), or
  CI/CD pipeline review (use sre-devops-expert).
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# Helm Validator

Validate Helm charts through a 4-stage pipeline: lint, template render, schema validation, and policy checks.

## When to Use

- Before merging PRs that modify `Chart.yaml`, `values.yaml`, or templates
- As part of the `iac-review-agent` unified IaC review pipeline
- When onboarding new Helm charts or upgrading chart versions
- Pre-deployment validation in CI/CD

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `helm` | `brew install helm` | Lint and template rendering |
| `kubeconform` | `brew install kubeconform` | Schema validation against K8s OpenAPI |
| `kube-score` | `brew install kube-score` | Best-practice policy checks |

Missing tools are reported as `SKIPPED` in the output.

## Workflow

### Step 1: Discover Charts

Detect Helm charts in the target scope:

```bash
find <scope> -name "Chart.yaml" -type f
```

For each discovered chart directory, run Steps 2-5.

### Step 2: Helm Lint

Run `helm lint` with strict mode to catch template errors and best-practice violations:

```bash
helm lint <chart-dir> --strict --values <chart-dir>/values.yaml
```

Capture exit code and parse warning/error output.

### Step 3: Template Render

Render templates to catch runtime errors that lint misses:

```bash
helm template test-release <chart-dir> --values <chart-dir>/values.yaml --debug 2>&1
```

If the chart has multiple values files (e.g., `values-production.yaml`), render with each.

### Step 4: Schema Validation (kubeconform)

Pipe rendered templates through kubeconform to validate against the target K8s version schema:

```bash
helm template test-release <chart-dir> --values <chart-dir>/values.yaml | \
  kubeconform -kubernetes-version <target-version> -summary -output json
```

Default target version: `1.28.0`. Override with user-specified version.

Parse JSON output for resource-level pass/fail results.

### Step 5: Policy Checks (kube-score)

Run kube-score on rendered templates for best-practice scoring:

```bash
helm template test-release <chart-dir> --values <chart-dir>/values.yaml | \
  kube-score score -
```

Key checks: resource limits, probes, security context, network policies, pod disruption budgets.

### Step 6: LLM-Augmented Review

After automated checks, perform an LLM review of:
- `values.yaml` for sensitive defaults (debug mode, weak passwords, open ports)
- Template logic for complex conditionals that may produce invalid YAML
- Chart dependencies for version pinning
- NOTES.txt for helpful post-install instructions

### Step 7: Aggregate Report

Produce a structured report:

```
Helm Validation Report
======================
Chart: <chart-name> (<chart-version>)
App Version: <app-version>
Target K8s: <version>

Stage                  Status    Details
────────────────────── ───────── ──────────────────────
Helm Lint              PASS      0 errors, 2 warnings
Template Render        PASS      12 resources rendered
Schema Validation      FAIL      1 invalid resource (CronJob v1beta1 deprecated)
Policy Checks          WARN      3 resources missing probes

FINDINGS:
- severity: High
  file: templates/deployment.yaml
  issue: No resource limits defined for container "app"
  fix: Add resources.limits.cpu and resources.limits.memory

- severity: Medium
  file: templates/cronjob.yaml
  issue: Using deprecated API version batch/v1beta1
  fix: Update to batch/v1
```

## Examples

### Example 1: Validate project Helm charts
User says: "Validate our Helm charts"
Actions:
1. Discover charts in `helm/` directory
2. Run 4-stage pipeline on each chart
3. Aggregate results into single report
Result: Pass/fail report with findings and fix suggestions

### Example 2: PR-scoped validation
User says: "Check Helm changes in this PR"
Actions:
1. Identify changed Helm files from git diff
2. Determine affected chart directories
3. Run full validation on affected charts only
Result: Focused report on changed charts

## Error Handling

| Error | Action |
|-------|--------|
| helm binary not found | Report SKIPPED for Helm stages; suggest `brew install helm` |
| chart lint fails | Capture lint output, include in report as FAIL with fix suggestions |
| kubeconform schema fetch fails | Retry with `--schema-location`; if persistent, skip schema stage and note in report |
| kube-score not installed | Report SKIPPED for policy checks; suggest `brew install kube-score` |
| values file missing | Run `helm template` with `--set` defaults or skip values-specific validation; note in report |

## Troubleshooting

### kubeconform fails with CRD resources
Cause: Custom Resource Definitions not in default schema registry
Solution: Skip CRD validation with `--skip CustomResourceDefinition` or provide CRD schemas via `--schema-location`

### helm template fails with missing dependencies
Cause: Chart has subcharts not yet downloaded
Solution: Run `helm dependency update <chart-dir>` before validation
