---
name: k8s-manifest-validator
description: >-
  Validate Kubernetes manifests using kubeconform schema validation,
  KubeLinter policy checks, and kubectl dry-run server-side validation.
  Produces a structured pass/fail report. Use when the user asks to "validate
  K8s manifests", "check Kubernetes YAML", "K8s 매니페스트 검증", "쿠버네티스 검증",
  "k8s-manifest-validator", or any Kubernetes manifest quality/security
  validation. Do NOT use for Helm chart validation (use helm-validator),
  Terraform review (use terraform-reviewer), or infrastructure design review
  (use sre-devops-expert).
disable-model-invocation: true
---

# K8s Manifest Validator

Validate raw Kubernetes manifests (non-Helm YAML files) through a 4-stage pipeline: schema validation, policy checks, dry-run validation, and LLM-augmented review.

## When to Use

- Before merging PRs that modify files in `infra/k8s/`, `deploy/`, or any directory containing K8s manifests
- As part of the `iac-review-agent` unified IaC review pipeline
- When migrating between Kubernetes versions (API deprecation checks)
- Security review of workload configurations

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `kubeconform` | `brew install kubeconform` | OpenAPI schema validation |
| `kube-linter` | `brew install kube-linter` | Security and best-practice linting |
| `kubectl` | `brew install kubectl` | Dry-run server-side validation |

Missing tools are reported as `SKIPPED` in the output.

## Workflow

### Step 1: Discover Manifests

Find Kubernetes manifest files in the target scope:

```bash
find <scope> -name "*.yaml" -o -name "*.yml" | \
  xargs grep -l "^kind:" 2>/dev/null
```

Filter out Helm templates (files containing `{{ }}` Go template syntax) — those go to `helm-validator`.

### Step 2: Schema Validation (kubeconform)

Validate each manifest against the target K8s version OpenAPI schema:

```bash
kubeconform -kubernetes-version <target-version> -summary -output json \
  -skip CustomResourceDefinition <manifest-files>
```

Default target version: `1.28.0`. Detects deprecated APIs, invalid field names, and type mismatches.

### Step 3: Policy Checks (KubeLinter)

Run KubeLinter for security and operational best-practice checks:

```bash
kube-linter lint <manifest-dir> --format json
```

Key checks:
- **Security**: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`
- **Reliability**: liveness/readiness probes, resource requests/limits, PodDisruptionBudget
- **Networking**: NetworkPolicy presence, Service type validation
- **Storage**: PVC access modes, StorageClass specification

### Step 4: Dry-Run Validation (kubectl)

If a cluster context is available, validate against the live API server:

```bash
kubectl apply --dry-run=server -f <manifest-file> 2>&1
```

Catches: admission webhook rejections, quota violations, RBAC conflicts. Skip if no cluster context.

### Step 5: LLM-Augmented Review

After automated checks, perform an LLM review of:
- **Security context**: Capabilities, seccomp profiles, AppArmor annotations
- **Resource sizing**: Whether requests/limits are reasonable for the workload type
- **Labels/annotations**: Consistent labeling scheme (`app.kubernetes.io/*`)
- **Anti-patterns**: Using `latest` tag, hostPath volumes, hostNetwork
- **Multi-tenancy**: Namespace isolation, ResourceQuota, LimitRange

### Step 6: Aggregate Report

```
K8s Manifest Validation Report
==============================
Scope: infra/k8s/
Target K8s Version: 1.28.0
Files Scanned: 15

Stage                  Status    Details
────────────────────── ───────── ──────────────────────
Schema Validation      PASS      15/15 valid
KubeLinter             WARN      12 passed, 3 warnings
Dry-Run                SKIPPED   No cluster context
LLM Review             WARN      2 recommendations

FINDINGS:
- severity: High
  file: infra/k8s/deployment.yaml
  check: no-read-only-root-fs
  issue: Container "api" does not set readOnlyRootFilesystem
  fix: Add securityContext.readOnlyRootFilesystem: true

- severity: Medium
  file: infra/k8s/service.yaml
  check: dangling-service
  issue: Service selector does not match any Deployment labels
  fix: Verify label selectors match between Service and Deployment
```

## Examples

### Example 1: Validate project manifests
User says: "Validate our K8s manifests"
Actions:
1. Discover manifests in `infra/k8s/`
2. Run 4-stage pipeline
3. Generate report with findings
Result: Pass/fail report with security and best-practice findings

### Example 2: API version migration check
User says: "Check if our manifests work with K8s 1.30"
Actions:
1. Run kubeconform with `--kubernetes-version 1.30.0`
2. Flag deprecated/removed APIs
3. Suggest migration paths
Result: Migration readiness report

## Error Handling

| Error | Action |
|-------|--------|
| kubeconform not installed | Report SKIPPED for schema validation; suggest `brew install kubeconform` |
| KubeLinter not found | Report SKIPPED for policy checks; suggest `brew install kube-linter` |
| kubectl not configured | Skip dry-run stage; note "No cluster context" in report |
| invalid YAML syntax | Fail early with parse error location; suggest YAML linter |
| CRD schema not available | Skip CRD resources with `--skip CustomResourceDefinition` or provide `--schema-location` |

## Troubleshooting

### kubeconform fails on CRDs
Cause: Custom resources not in default schema registry
Solution: Provide CRD schemas via `--schema-location` or skip with `--skip <Kind>`

### KubeLinter noisy on Kustomize
Cause: KubeLinter processes raw overlays before kustomize build
Solution: Run `kustomize build <dir> | kube-linter lint -` on built output
