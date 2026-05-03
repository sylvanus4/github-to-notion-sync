---
name: msp-argocd-drift-analyzer
description: >-
  MSP read-only skill that detects and reports configuration drift between
  Git-declared state and live Kubernetes/ArgoCD state across MSP-managed
  clusters. Fan-out compares Helm release values, K8s resource specs, and
  ArgoCD Application sync status, then fan-in produces a tenant-scoped drift
  report with severity classification and remediation guidance. Composes
  argocd-expert and infra-drift-detector. Use when the user asks to detect
  drift, check ArgoCD sync, compare live vs Git, cluster drift report,
  configuration drift analysis, or needs to verify declared-vs-actual state
  for MSP-managed infrastructure. Do NOT use for applying fixes or syncing
  ArgoCD apps (use argocd-expert directly), general IaC review without drift
  context (use iac-review-agent), Terraform state drift (use
  infra-drift-detector directly), or incident investigation (use
  k8s-incident-investigator). Korean triggers: ArgoCD 드리프트, 설정 드리프트, Git 라이브
  비교, 동기화 상태 확인, 클러스터 드리프트.
---

# MSP ArgoCD Drift Analyzer

Read-only MSP skill that compares Git-declared infrastructure state against live Kubernetes/ArgoCD cluster state, classifies drift severity, and produces actionable remediation guidance without modifying any resources.

## Usage

```
/msp-argocd-drift-analyzer --tenant acme-corp --cluster prod-eks-01 --namespace default
/msp-argocd-drift-analyzer --cloud gcp --cluster gke-prod "check all ArgoCD apps for drift"
/msp-argocd-drift-analyzer --app-selector "team=platform" "drift report for platform team apps"
```

## Prerequisites

- **Identity**: `tenant_id`, `cluster_name` or `cluster_context`, optional `namespace` filter.
- **Cloud credentials**: read-only roles for target clusters.
- **ArgoCD access**: API read access to ArgoCD server (Application list, sync status, diff).
- **kubectl access**: read-only kubeconfig for target clusters (`get`, `describe`, `diff` — no `apply`, `delete`, `patch`).
- **Git access**: read-only access to the GitOps source repositories.

## Pipeline Overview

```
Fan-out (parallel, read-only)
  ├─ ArgoCD sync-status agent    → Application health, sync status, conditions, history
  ├─ Helm value diff agent       → Compare rendered Helm values (Git vs live release)
  └─ K8s resource diff agent     → kubectl diff for key resource types (Deployments, ConfigMaps, Services, etc.)

        ↓ Fan-in: merge, dedupe, classify severity, map to applications

  ├─ argocd-expert               → ArgoCD-specific drift interpretation, sync wave context
  └─ infra-drift-detector        → General IaC drift patterns and remediation templates

        ↓ Classify + report

  Output: JSON drift report (canonical) + Markdown human summary
```

## Detailed Workflow

1. **Intake and validate** — Confirm `tenant_id`, cluster context, and optional filters (namespace, app-selector, label-selector). Verify ArgoCD API and kubectl connectivity with read-only test calls.

2. **ArgoCD application inventory** — List all ArgoCD Applications matching the scope. Record sync status (`Synced`, `OutOfSync`, `Unknown`), health status (`Healthy`, `Degraded`, `Progressing`, `Missing`, `Suspended`), and last sync time.

3. **Fan-out** — Run three subagents in parallel:
   - **ArgoCD sync-status agent**: For each OutOfSync or Unknown app, retrieve the managed-resource diff from ArgoCD API. Record sync conditions and retry history.
   - **Helm value diff agent**: For Helm-sourced apps, compare the Git-declared `values.yaml` against the live Helm release values (`helm get values`). Flag overrides, missing keys, and value type changes.
   - **K8s resource diff agent**: Run `kubectl diff` (dry-run, read-only) on key resource types. Capture added/removed/modified fields. Flag manual edits (annotations not matching ArgoCD tracking).

4. **Fan-in** — Merge all drift findings. Deduplicate overlapping detections. Align findings to ArgoCD Application boundaries.

5. **Classify drift severity**:
   - **CRITICAL**: Security-relevant drift (RBAC, NetworkPolicy, Secrets, ServiceAccount), resource deletion drift, replica count drift in production.
   - **HIGH**: Configuration drift affecting service behavior (env vars, resource limits, container images).
   - **MEDIUM**: Metadata drift (labels, annotations), non-production replica changes.
   - **LOW**: Cosmetic drift (formatting, comment-only changes), informational-only differences.

6. **Compose remediation guidance** — Using `argocd-expert` patterns, suggest: manual sync, hard-sync with prune, Git revert, or "investigate manual edit." Never execute these actions.

7. **Emit JSON report** — Fill canonical output schema.

8. **Emit Markdown summary** — Headline stats (total apps, drifted apps, severity distribution), per-application drift details, and recommended next steps (all read-only).

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "argocd-drift-analyzer",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cluster": "string",
  "scope": {
    "namespace": "string|null",
    "app_selector": "string|null"
  },
  "summary": {
    "total_apps": 0,
    "synced": 0,
    "out_of_sync": 0,
    "unknown": 0,
    "drift_count_by_severity": {
      "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0
    }
  },
  "drifts": [
    {
      "application": "string",
      "namespace": "string",
      "source_repo": "string",
      "sync_status": "Synced|OutOfSync|Unknown",
      "health_status": "Healthy|Degraded|Progressing|Missing|Suspended",
      "drift_items": [
        {
          "resource_kind": "string",
          "resource_name": "string",
          "field_path": "string",
          "git_value": "string",
          "live_value": "string",
          "severity": "CRITICAL|HIGH|MEDIUM|LOW",
          "category": "security|config|metadata|cosmetic",
          "detected_by": "argocd_sync|helm_diff|kubectl_diff"
        }
      ],
      "remediation": {
        "recommendation": "string",
        "action_type": "manual_sync|hard_sync|git_revert|investigate",
        "read_only": true
      }
    }
  ],
  "data_completeness": {
    "missing_inputs": ["string"],
    "unreachable_clusters": ["string"],
    "degraded_mode": false
  }
}
```

## Cloud Adapters

### AWS (EKS)

| Concern | Services | Notes |
|---------|----------|-------|
| Cluster access | EKS | `DescribeCluster`, kubeconfig generation (read-only) |
| ArgoCD | ArgoCD on EKS | API server access via port-forward or ingress |
| Change context | CloudFormation, CodePipeline | Stack events for recent IaC deployments |

### GCP (GKE)

| Concern | Services | Notes |
|---------|----------|-------|
| Cluster access | GKE | `container.clusters.get`, kubeconfig generation (read-only) |
| ArgoCD | ArgoCD on GKE | API server access via IAP or ingress |
| Change context | Cloud Build, Cloud Deploy | Build/deployment history for change correlation |

## Error Handling

- **ArgoCD API unreachable** — Degrade to kubectl-only diff mode; record in `data_completeness`.
- **Cluster unreachable** — Skip cluster, record in `unreachable_clusters`, continue with remaining clusters.
- **Large diff output** — Truncate per-resource diff to 500 lines; note truncation in `drift_items`.
- **Manual edits detected** — Flag as "investigate" rather than auto-recommending sync (manual edits may be intentional hotfixes).

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No `argocd app sync`, `kubectl apply`, `kubectl delete`, or any mutation.
- Drift remediation recommendations are advisory only; execution requires human action or escalation to `argocd-expert`.
