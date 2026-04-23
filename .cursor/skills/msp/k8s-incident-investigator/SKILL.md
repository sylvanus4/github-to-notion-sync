---
name: msp-k8s-incident-investigator
description: >-
  Structured Kubernetes incident investigation for MSP engineers on EKS and GKE.
  Fan-out four parallel analysis agents (pod status, node conditions, events,
  HPA/rollout), fan-in correlation, ranked cause hypotheses, and read-only
  investigation reports. Use when the user asks about "k8s incident
  investigation", "kubernetes troubleshoot", "pod crash analysis", "node issue
  investigation", "쿠버네티스 장애", "K8s 인시던트", "파드 장애 조사", "노드 문제
  분석", or MSP Tier-1 K8s triage. Only kubectl get/describe/logs/top and
  read-only cloud APIs. Do NOT use for manifest CI validation only (use
  k8s-manifest-validator), Helm chart validation (use helm-validator), Argo CD
  mutations or sync (use argocd-expert operations outside read-only), or
  infrastructure design review (use sre-devops-expert).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "msp/k8s"
  approval_tier: "tier-1"
  approval_spec: "docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md"
  mutations: []
  clouds:
    - "aws"
    - "gcp"
  composes:
    - "k8s-manifest-validator"
    - "argocd-expert"
---

# MSP — K8s Incident Investigator

Rapid, **read-only** Kubernetes incident investigation for MSP L2/L3 and platform operators. Shortens mean time to understanding (MTTU) by gathering cluster-local evidence, correlating pod/node/control-plane signals, and producing **ranked cause hypotheses**—without mutations. Composes **`k8s-manifest-validator`** (spec/policy knowledge) and **`argocd-expert`** (GitOps rollout context, read-only).

## Summary

| Item | Detail |
|------|--------|
| **Approval** | Tier 1 — read-only |
| **Clouds** | AWS (EKS + Container Insights), GCP (GKE + Cloud Logging / Monitoring) |
| **Pattern** | Fan-out 4 agents → Fan-in correlation → Hypothesis ranking → Structured report |

## Usage Examples

**Example 1 — Cluster + namespace**

```text
Investigate k8s incident: context=arn:aws:eks:...:cluster/prod, namespace=payments, incident="checkout-api 503s"
```

**Example 2 — Pod narrowed**

```text
K8s troubleshoot: cluster=gke_my-project_us-central1_ops, namespace=app, pod=checkout-api-7d4f9c6-xk2mn, window=45m
```

**Example 3 — Workload + deployment**

```text
Kubernetes incident: context=prod-eks, namespace=ingress, deployment=nginx-internal, describe node issues
```

Parameters: **cluster context** (required if multi-cluster), **namespace** (recommended), **pod** / **deployment** (optional), **incident description** (optional), **time window** (optional; default 30–60 minutes).

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **kubeconfig / context** | Valid `kubectl` context; region or project for cloud hooks |
| **RBAC** | Read-only: get, list, watch, describe pods/nodes/events/deployments/hpa/rs; logs read; **no** create/update/delete |
| **Cloud (optional)** | AWS: IAM read for EKS Describe*, CloudWatch Container Insights / logs read. GCP: `container.clusters.get`, Cloud Logging read, Monitoring read |
| **Argo CD (optional)** | Read-only CLI or API: `argocd app get`, `argocd app history` when allowed—**no sync/rollback** |

## Pipeline Overview

```text
Scope (cluster, ns, workload, window)
        │
        ├─ Fan-out (parallel) ─────────────────────────────────────┐
        │   Agent A: Pod status        Agent B: Node conditions     │
        │   Agent C: Events            Agent D: HPA / Rollout / Argo │
        └────────────────────────────────────────────────────────────┘
                                │
                        Fan-in: time-align, dedupe, map pod↔node↔cloud
                                │
                        Compose: k8s-manifest-validator rules (advisory)
                                argocd-expert (read-only rollout context)
                                │
                        Rank 3–7 cause hypotheses (evidence-weighted)
                                │
                        Output: investigation report (schema below)
```

### Subagent Contract

| Agent | Role | Primary signals |
|-------|------|-----------------|
| **A — Pod status analyzer** | CrashLoopBackOff, ImagePullBackOff, ErrImagePull, OOMKilled, Pending, CreateContainerConfigError | Container `state` / `lastState`, exit codes, image ref, probe failures, `kubectl logs` / `--previous` |
| **B — Node condition checker** | NotReady, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable | Node `conditions`, allocatable vs capacity, cordon/schedulability |
| **C — Event correlator** | Scheduling, volumes, evictions, warnings | `kubectl get events` sorted by time; field selectors; involved objects |
| **D — HPA / Rollout analyzer** | Replicas, unavailable, HPA, ReplicaSet generations | `describe deploy`, `describe hpa`, RS history; Argo app sync/revision **read-only** |

Optional parallel task: **cloud metrics** (Container Insights / GCP Monitoring) for the same window—merge at fan-in.

**Allowed verbs only:** `kubectl get`, `kubectl describe`, `kubectl logs` (incl. `--previous`), `kubectl top` (node/pod). No `apply`, `delete`, `patch`, `rollout *`, `scale`, `cordon`/`uncordon`/`drain`, mutating `exec`, or Argo sync/rollback.

## Common Incident Patterns

| Pattern | Typical symptoms | Typical root causes (indicative) |
|---------|------------------|---------------------------------|
| CrashLoopBackOff | High restarts, `CrashLoopBackOff` | App error, bad config, failed migration, liveness too aggressive |
| ImagePullBackOff / ErrImagePull | Pull errors in events | Wrong tag, missing pull secret, registry outage |
| Pending (scheduling) | `Pending`, FailedScheduling | Resources, taints, affinity, no nodes |
| Pending (volumes) | Stuck after partial schedule | PVC, StorageClass, zone mismatch |
| OOMKilled | `OOMKilled` in lastState | Limits too low, leak, load spike |
| CreateContainerConfigError | Start failure | Secret/ConfigMap ref, subPath, permissions |
| Eviction | Eviction events, unexpected termination | Node pressure, priority/preemption |
| Node NotReady | Node NotReady, rescheduling | Kubelet, network, instance health |
| Node pressure | MemoryPressure, DiskPressure, PIDPressure | Saturation, logs, IGC, too many pods |
| HPA thrash | Rapid scale oscillation | Metrics noise, low stabilization |
| Rollout regression | Old RS traffic, maxUnavailable | Readiness, PDB, bad rollout |

## Output Schema

Primary artifact: structured **investigation report** (Markdown and/or JSON). Version field: `reportVersion: "1.0"`.

```yaml
reportVersion: "1.0"
metadata:
  cluster: "<context-name>"
  cloud: "aws|gcp"
  regionOrLocation: "<region or zone>"
  namespace: "<ns|*>"
  generatedAt: "<RFC3339>"
  incidentSummary: "<short description>"
  readOnly: true
  approvalTier: "Tier1"

affectedResources: []   # pod, node, deploy, hpa, pvc, ...
conditionAnalysis:
  pods: []
  nodes: []
  workloads: []
eventTimeline: []       # k8s + cloud lines, time-aligned
causeHypotheses: []     # id, summary, evidence[], confidence, rank
recommendedActions:
  immediate: []         # read-only validation only
  followUp: []          # Tier 2 / customer — not executed here
cloudEvidence:
  aws: {}               # e.g. Container Insights query ref, node group status
  gcp: {}               # e.g. Logging filter, alert refs
rolloutContext:
  application: ""     # Argo CD if found
  revision: ""
  syncStatus: ""
complianceNotes:
  toolsUsed: ["kubectl get", "kubectl describe", "kubectl logs", "kubectl top"]
  mutationsPerformed: []
```

## Cloud Adapters

### AWS (EKS)

| Area | Use |
|------|-----|
| EKS | Describe cluster, **managed node groups** / Fargate (read) for version/skew |
| **Container Insights** | CPU/memory/restarts; correlate with crashes/OOM |
| ASG / node group | Scaling, **InsufficientInstanceCapacity**-class signals |
| **CloudWatch Logs** | Control plane (where permitted), workload log groups if configured |
| Auth | IAM / assumed role; least-privilege read policies |

### GCP (GKE)

| Area | Use |
|------|-----|
| GKE API | Cluster, **node pool**, surge upgrade / maintenance (read) |
| **Cloud Logging** | `resource.type`, `k8s_cluster`, labels; stderr/stdout for failing containers |
| **Cloud Monitoring** | Dashboards, alert policies, saturation vs node conditions |
| Logs Router | Note sink scope in report if logs are centralized |
| Auth | Service account: `container.clusters.get` + logging/monitoring read |

Portable core: pod/node/event/HPA logic is **cloud-agnostic** `kubectl` + K8s semantics; cloud sections **augment** evidence.

## Composed Skills

| Skill | Role |
|-------|------|
| **`k8s-manifest-validator`** | **Advisory:** Cross-check observed live spec fragments (from get/describe) against validator rules for misconfigs that show as CrashLoop or Pending (probes, quotas, security context). Not a CI gate in incident mode. |
| **`argocd-expert`** | **Read-only:** Link workloads to Argo CD Application, sync status, revision, history; align timeline with sync waves. **No** sync, rollback, or write operations from this skill. |

## Escalation

Hypotheses requiring config changes, quota increases, node repair, or customer-visible fixes belong in **`recommendedActions.followUp`** and need **Tier 2** or customer approval.

## Evaluation Targets

| Criterion | Target |
|-----------|--------|
| Hypothesis quality | Top hypothesis aligns with post-incident RCA when reviewed |
| Completeness | Agents A–D each contribute or are marked N/A with reason |
| Safety | `mutationsPerformed: []` always; audit allows only listed read verbs |
| Latency | &lt; 60s typical for single namespace, &lt; 50 pods (when instrumented) |

**Non-functional:** Rate-limit friendly backoff on 429/503; redact secrets in log snippets.

## Error Handling

| Situation | Action |
|-----------|--------|
| Missing kubeconfig | Stop; list prerequisite to obtain context |
| RBAC denied | Note scope gap in report; continue allowed resources |
| Cloud API unavailable | Degrade to in-cluster-only; state in `cloudEvidence` |
| Argo CD unavailable | Omit `rolloutContext` or mark unknown; do not guess sync state |

## Governance

- **Approval Tier:** Tier 1 — fully read-only, no human gate required.
- **Mutations:** None. This skill runs `kubectl get/describe/logs/top` and ArgoCD read APIs only; it never performs `kubectl delete/patch/apply`, `argocd sync`, or any mutation.
- **Prohibited:** Pod deletion, rollout restart, Argo sync/rollback, scaling changes, or any cluster mutation.

## References

- Planning: `docs/msp-skills/plans/k8s-incident-investigator.md`
- MSP model: `docs/msp-skills/MSP_MASTER_PRD.md` (Tier 1 read-only)
- Composed: `.cursor/skills/infra/k8s-manifest-validator/SKILL.md`, `.cursor/skills/infra/argocd-expert/SKILL.md`
