---
name: k8s-manifest-review
description: >-
  Validate Kubernetes manifests using schema validation (kubeconform), policy
  checks (KubeLinter), dry-run validation (kubectl), and LLM-augmented review.
  Produces a structured pass/fail report. Use when validating K8s YAML, checking
  manifest quality, or reviewing workload configurations.
disable-model-invocation: true
arguments: [scope]
---

# K8s Manifest Review

Validate raw Kubernetes manifests through a 4-stage pipeline.

## Usage

```
/k8s-manifest-review infra/k8s/
/k8s-manifest-review charts/container/templates/
/k8s-manifest-review $ARGUMENTS
```

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `kubeconform` | `brew install kubeconform` | OpenAPI schema validation |
| `kube-linter` | `brew install kube-linter` | Security and best-practice linting |
| `kubectl` | `brew install kubectl` | Dry-run server-side validation |

Missing tools are reported as `SKIPPED` in the output.

## Workflow

### Step 1: Discover Manifests

Find K8s manifest files in the target scope. Filter out Helm templates (files containing `{{ }}` Go template syntax).

### Step 2: Schema Validation (kubeconform)

```bash
kubeconform -kubernetes-version 1.28.0 -summary -output json \
  -skip CustomResourceDefinition <manifest-files>
```

Detects deprecated APIs, invalid fields, and type mismatches.

### Step 3: Policy Checks (KubeLinter)

```bash
kube-linter lint <manifest-dir> --format json
```

Key checks:
- **Security**: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`
- **Reliability**: liveness/readiness probes, resource requests/limits, PDB
- **Networking**: NetworkPolicy presence, Service type validation
- **Storage**: PVC access modes, StorageClass specification

### Step 4: Dry-Run Validation (kubectl)

If a cluster context is available:

```bash
kubectl apply --dry-run=server -f <manifest-file> 2>&1
```

Catches admission webhook rejections, quota violations, RBAC conflicts. Skip if no cluster context.

### Step 5: LLM-Augmented Review

- **Security context**: Capabilities, seccomp profiles, AppArmor
- **Resource sizing**: Reasonable requests/limits for workload type
- **Labels/annotations**: Consistent `app.kubernetes.io/*` scheme
- **Anti-patterns**: `latest` tag, hostPath volumes, hostNetwork
- **Multi-tenancy**: Namespace isolation, ResourceQuota, LimitRange

### Step 6: Report

```
K8s Manifest Validation Report
==============================
Scope: [directory]
Target K8s Version: 1.28.0
Files Scanned: N

Stage                  Status    Details
────────────────────── ───────── ──────────────────────
Schema Validation      PASS      N/N valid
KubeLinter             WARN      N passed, N warnings
Dry-Run                SKIPPED   No cluster context
LLM Review             WARN      N recommendations

FINDINGS:
- severity: [High/Medium/Low]
  file: [path]
  check: [check-name]
  issue: [description]
  fix: [recommendation]
```

## Error Handling

| Error | Action |
|-------|--------|
| kubeconform not installed | SKIPPED; suggest `brew install kubeconform` |
| KubeLinter not found | SKIPPED; suggest `brew install kube-linter` |
| No cluster context | Skip dry-run stage |
| Invalid YAML syntax | Fail early with parse error location |
| CRD schema unavailable | Skip with `--skip CustomResourceDefinition` |

## Test Invocation

```
/k8s-manifest-review infra/k8s/
/k8s-manifest-review --kubernetes-version 1.30.0 deploy/
```
