---
name: infra-drift-detector
description: >-
  Detect infrastructure drift by comparing live cluster state against declared
  IaC (Helm releases, K8s manifests, Terraform state). Reports drifts with
  severity and remediation suggestions. Use when the user asks to "check for
  drift", "infrastructure drift", "인프라 드리프트", "상태 비교", "infra-drift-detector",
  or wants to verify infrastructure matches its declared state. Do NOT use for
  IaC code review (use iac-review-agent), initial validation (use
  helm-validator/k8s-manifest-validator), or deployment (use
  sre-devops-expert).
---

# Infrastructure Drift Detector

Compare live infrastructure state against declared IaC to detect configuration drift, unauthorized changes, and state inconsistencies.

## When to Use

- Periodic drift checks (daily/weekly schedule)
- Before deployments to establish a clean baseline
- After incidents to detect unauthorized changes
- During compliance audits to verify state consistency

## Prerequisites

Requires cluster access (`kubectl` context) and optionally Terraform state access.

## Workflow

### Step 1: Discover Declared State

Identify all IaC sources:

**Helm Releases**:
```bash
helm list -A -o json
```

**K8s Manifests**: Read from `infra/k8s/`, `deploy/` directories.

**Terraform State** (if available):
```bash
terraform show -json
```

### Step 2: Capture Live State

For each declared resource, fetch the live state:

**Helm drift**:
```bash
helm diff upgrade <release> <chart> --values <values> --no-hooks
```

If `helm-diff` plugin not available:
```bash
helm get manifest <release> -n <namespace> > /tmp/declared.yaml
kubectl get <kind> <name> -n <namespace> -o yaml > /tmp/live.yaml
diff /tmp/declared.yaml /tmp/live.yaml
```

**K8s manifest drift**:
```bash
kubectl diff -f <manifest-file> 2>&1
```

**Terraform drift**:
```bash
terraform plan -detailed-exitcode
```
Exit code 2 = drift detected.

### Step 3: Classify Drifts

| Severity | Criteria | Example |
|----------|----------|---------|
| **Critical** | Security-impacting changes | Security context removed, network policy deleted |
| **High** | Behavioral changes | Replica count changed, resource limits modified |
| **Medium** | Configuration differences | Label changes, annotation updates |
| **Low** | Cosmetic differences | Kubectl-applied metadata, last-applied annotations |
| **Expected** | Known managed fields | Kubernetes system annotations, status fields |

### Step 4: Analyze Root Cause

For each drift, determine likely cause:
- **Manual kubectl edit**: Someone modified resources directly
- **Admission webhook**: Mutating webhook modified the resource
- **Controller-managed**: HPA, VPA, or operator modified fields
- **Upgrade side-effect**: K8s version upgrade changed defaults

### Step 5: Generate Report

```
Infrastructure Drift Report
============================
Scan Date: 2026-03-19 14:00
Cluster: production-cluster
Namespaces Scanned: 5

Drift Summary:
  Critical: 0
  High: 2
  Medium: 4
  Low: 8
  Expected: 12

HIGH SEVERITY:
1. Deployment api-server (namespace: production)
   Field: spec.replicas
   Declared: 3 | Live: 5
   Cause: Likely manual scale-up
   Fix: Update values.yaml replicas to 5, or scale down

2. ConfigMap app-config (namespace: production)
   Field: data.DATABASE_URL
   Declared: postgres://db:5432 | Live: postgres://db-replica:5432
   Cause: Manual kubectl edit
   Fix: Update Helm values or revert with helm upgrade

MEDIUM SEVERITY:
3. Service api-service
   Field: metadata.annotations
   Declared: missing | Live: prometheus.io/scrape: "true"
   Cause: Monitoring team annotation
   Fix: Add annotation to Helm template

Resources in sync: 45/53 (85%)
```

### Step 6: Remediation Suggestions

For each drift, provide actionable fixes:
- **Update IaC**: Modify declared state to match desired live state
- **Revert live**: Re-apply declared state to overwrite live changes
- **Exclude**: Mark as expected drift (e.g., HPA-managed replicas)

## Error Handling

| Error | Action |
|-------|--------|
| kubectl context not configured or invalid | Fail with setup instructions; suggest `kubectl config use-context` or `KUBECONFIG` check |
| kubeconfig file not found | Exit with path used and instructions to set `KUBECONFIG` or create config |
| Namespace not accessible (RBAC denied) | Skip that namespace; list skipped namespaces in report; continue with accessible ones |
| IaC source directory empty (no Helm/Terraform/K8s manifests) | Report "no declared state found"; suggest adding manifests or correcting paths |
| Diff too large to display (>10KB) | Summarize drift count and severity; write full diff to file; reference file path in report |

## Examples

### Example 1: Daily drift check
Automated trigger: Daily schedule
Actions:
1. Scan all Helm releases and K8s manifests
2. Compare against live cluster state
3. Classify and report drifts
Result: Drift report with severity and remediation

### Example 2: Pre-deployment baseline
User says: "Check for drift before deploying"
Actions:
1. Full drift scan of target namespace
2. Flag any unauthorized changes
3. Recommend resolving drifts before deployment
Result: Clean baseline verification
