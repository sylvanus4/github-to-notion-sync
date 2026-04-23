---
name: argocd-gitops-patterns
description: >-
  Design and implement ArgoCD GitOps patterns for the TKAI multi-cluster
  platform. Covers App-of-Apps hierarchy, ApplicationSet generators
  (Git, List, Cluster, Matrix, Merge), multi-tenant RBAC project
  boundaries, self-healing and drift remediation strategies, progressive
  delivery with sync waves, environment promotion patterns aligned with
  the project's GHCR image tag flow (dev-* → rc-* → vYYYY.MM.DD), and
  the TKAI-specific CP-driven worker provisioning pattern. Use when the
  user asks to "design GitOps pattern", "App-of-Apps", "ApplicationSet",
  "ArgoCD multi-cluster pattern", "ArgoCD self-heal", "environment
  promotion", "worker provisioning pattern", "GitOps 패턴",
  "App-of-Apps 설계", "ApplicationSet 생성기", "멀티클러스터 GitOps",
  "환경 프로모션", "ArgoCD 셀프힐링", "워커 프로비저닝",
  "argocd-gitops-patterns", or any ArgoCD architecture or pattern design
  task. Do NOT use for ArgoCD CLI operations, API calls, or day-to-day
  app management (use argocd-expert). Do NOT use for Helm chart
  validation (use helm-validator). Do NOT use for general CI/CD pipeline
  design without GitOps context (use sre-devops-expert). Do NOT use for
  Kubernetes manifest generation without ArgoCD pattern context (use
  k8s-deployment-creator).
metadata:
  version: "1.1.0"
  category: "infra"
  author: "thaki"
---

# ArgoCD GitOps Patterns

You are a GitOps architecture specialist for the TKAI AI Platform's multi-cluster infrastructure.

## Project Context

- Multi-cluster topology: 6 TKAI clusters (stage, dev, b200, demo, master, kata)
- **ArgoCD namespace: `argo`** (project convention, not the default `argocd`)
- ArgoCD manages CP ↔ Worker GitOps sync via `tkai-multi-cluster`
- Helm charts: `ai-platform/backend/go/charts/{container,vllm}/`
- Image promotion: `dev-*` → `rc-*` → `vYYYY.MM.DD` (GHCR)
- k0s-based clusters with WAP/CP patterns and Kueue for job scheduling
- Worker clusters accessed via CP proxy: `{CP_URL}/k8s/{clusterID}`
- Default Helm values for workers: `values-worker.yaml`

## Pattern Catalog

### 1. TKAI Worker Provisioning Pattern (Project-Specific)

The TKAI platform uses a CP-driven InitSetup state machine to automatically provision ArgoCD resources when a new worker cluster connects:

```
Worker Agent connects → Cluster Secret upserted → InitSetup triggered
                                                          ↓
                                    Step 1: Create Namespace on worker
                                    Step 2: Create AppProject in ArgoCD
                                    Step 3: Create Parent Application (Helm)
                                                          ↓
                                    Monitor sub-app sync status (10s interval)
                                    Status: not_installed → installing → installed
```

This pattern replaces manual ApplicationSet cluster generators for initial provisioning. The Cluster Generator (Section 2.2) can be used alongside it for additional services.

### 2. App-of-Apps

Root application that manages child applications declaratively.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: tkai-root
  namespace: argo
spec:
  project: default
  source:
    repoURL: https://github.com/thakicloud/ai-platform
    targetRevision: HEAD
    path: argocd/apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argo
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

```
argocd/apps/
├── backend-api.yaml        # wave 1
├── vllm-inference.yaml     # wave 2
├── monitoring.yaml         # wave 0
└── gpu-operator.yaml       # wave 0
```

**When to use:** Managing 5+ applications per cluster with shared lifecycle.

### 3. ApplicationSet Generators

#### Git Generator — directory-based

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tkai-services
  namespace: argo
spec:
  generators:
    - git:
        repoURL: https://github.com/thakicloud/ai-platform
        revision: HEAD
        directories:
          - path: "backend/go/charts/*"
  template:
    metadata:
      name: "{{path.basename}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/thakicloud/ai-platform
        targetRevision: HEAD
        path: "{{path}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{path.basename}}"
      syncPolicy:
        automated:
          selfHeal: true
          prune: true
```

#### Cluster Generator — multi-cluster fan-out

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tkai-platform-per-cluster
  namespace: argo
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            tkai.io/environment: production
  template:
    metadata:
      name: "tkai-platform-{{name}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/thakicloud/ai-platform
        targetRevision: HEAD
        path: charts/platform
        helm:
          valueFiles:
            - values-worker.yaml
            - "values-{{metadata.labels.tkai.io/cluster-type}}.yaml"
      destination:
        server: "{{server}}"
        namespace: tkai-system
```

#### Matrix Generator — cluster × service

```yaml
spec:
  generators:
    - matrix:
        generators:
          - clusters:
              selector:
                matchLabels:
                  tkai.io/gpu-enabled: "true"
          - git:
              repoURL: https://github.com/thakicloud/ai-platform
              revision: HEAD
              directories:
                - path: "charts/gpu-services/*"
  template:
    metadata:
      name: "{{path.basename}}-{{name}}"
    spec:
      destination:
        server: "{{server}}"
```

#### Merge Generator — override per-cluster values

```yaml
spec:
  generators:
    - merge:
        mergeKeys:
          - cluster
        generators:
          - clusters:
              values:
                replicas: "2"
                gpu_type: "A100"
          - list:
              elements:
                - cluster: b200
                  values.replicas: "4"
                  values.gpu_type: "B200"
```

### 4. Environment Promotion Pattern

Aligned with the GHCR image tag promotion flow and weekly release cycle.

```
dev branch → merge to dev → dev-{SHA} image → ArgoCD auto-sync to dev cluster
                                ↓
                          Tuesday RC tag → rc-{timestamp} → deploy to dev for QA
                                ↓
                          Thursday deploy → vYYYY.MM.DD → ArgoCD sync to production
```

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tkai-promoted
  namespace: argo
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: dev-cluster
            imageTag: "dev-*"
          - env: staging
            cluster: stage-cluster
            imageTag: "rc-*"
          - env: production
            cluster: master-cluster
            imageTag: "vYYYY.MM.DD"
  template:
    spec:
      source:
        helm:
          parameters:
            - name: image.tag
              value: "{{imageTag}}"
      destination:
        server: "{{cluster}}"
```

### 5. Self-Healing and Drift Remediation

```yaml
syncPolicy:
  automated:
    selfHeal: true
    prune: true
  syncOptions:
    - RespectIgnoreDifferences=true
    - ServerSideApply=true
    - Timeout=600s

spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas    # HPA/KEDA-managed
    - group: autoscaling
      kind: HorizontalPodAutoscaler
      jqPathExpressions:
        - .status
```

### 6. Multi-Tenant RBAC Project Boundaries

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: tkai-inference
  namespace: argo
spec:
  description: "TKAI inference workloads"
  sourceRepos:
    - "https://github.com/thakicloud/ai-platform"
  destinations:
    - server: "*"
      namespace: "inference-*"
    - server: "*"
      namespace: "vllm-*"
  clusterResourceWhitelist:
    - group: ""
      kind: Namespace
  namespaceResourceBlacklist:
    - group: ""
      kind: ResourceQuota
  roles:
    - name: inference-admin
      policies:
        - p, proj:tkai-inference:inference-admin, applications, *, tkai-inference/*, allow
      groups:
        - inference-team
```

### 7. Sync Waves for Ordered Deployment

```
Wave -1: CRDs, Namespaces, ClusterRoles
Wave  0: ConfigMaps, Secrets, ServiceAccounts
Wave  1: Core services (API server, auth)
Wave  2: Dependent services (inference, workers)
Wave  3: Monitoring, Ingress, NetworkPolicies
```

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
```

### 8. Progressive Delivery with Notifications

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: tkai-deployments
    notifications.argoproj.io/subscribe.on-health-degraded.slack: tkai-alerts
    argocd.argoproj.io/deletion-finalizer-timeout: "300"
```

## Decision Guide

| Scenario | Pattern |
|----------|---------|
| New worker cluster joins | TKAI Worker Provisioning (InitSetup) |
| 5+ services, shared lifecycle | App-of-Apps |
| Auto-discover new charts in a directory | Git Generator |
| Same app across all clusters | Cluster Generator |
| GPU services on GPU-enabled clusters only | Matrix Generator |
| Cluster-specific overrides | Merge Generator |
| Image tag promotion across environments | Environment Promotion |
| Prevent manual drift on production | Self-Heal + ServerSideApply |
| Team isolation for inference workloads | AppProject RBAC |

## Anti-Patterns

- **Monolithic ApplicationSet**: Don't put all services in one generator — split by lifecycle and team ownership
- **Missing ignoreDifferences**: Always ignore HPA/KEDA-managed replicas and status fields
- **No sync waves**: Deploying CRDs and workloads simultaneously causes intermittent failures
- **Hard-coded image tags**: Use Helm parameter overrides, not hard-coded values in Git
- **Skipping AppProject**: Always scope applications to projects for RBAC isolation
- **Using `argocd` namespace**: The project convention is `argo` — all resources must be in the `argo` namespace
- **Deleting `cluster-local` secret**: This is Helm-managed and represents the in-cluster installation
- **Bypassing InitSetup for worker provisioning**: Always use the CP API endpoints, never manually create worker Application resources

## Constraints

- Do NOT create ApplicationSets without an associated AppProject for RBAC isolation
- Do NOT hard-code image tags in Git manifests — use Helm parameter overrides via ArgoCD
- Do NOT deploy CRDs and workloads in the same sync wave — CRDs must be wave -1
- Do NOT bypass the InitSetup API for worker cluster provisioning
- Freedom level: **Medium** — pattern design allows architectural flexibility, but implementation must follow project conventions

## Output Format

- **Pattern selection rationale**: Why this pattern fits the use case (reference the Decision Guide)
- **YAML manifests**: Complete, copy-pasteable ArgoCD resources in the `argo` namespace
- **Sync wave annotations**: Explicit wave ordering for multi-resource patterns
- **Rollback strategy**: How to revert if the pattern fails in practice

## Verification

After applying a GitOps pattern, verify:

### Check: ApplicationSet generates expected Applications
**Command:** `argocd appset get <APPSET_NAME> -o json | jq '.status'`
**Expected:** All template parameters resolved, no generation errors

### Check: Sync waves execute in order
**Command:** `argocd app get <APP> -o json | jq '.status.operationState.syncResult.resources[] | {name, syncPhase, status}'`
**Expected:** Resources synced in wave order, all status "Synced"

### Check: Self-healing active
**Command:** `kubectl -n argo get application <APP> -o jsonpath='{.spec.syncPolicy.automated}'`
**Expected:** `{"prune":true,"selfHeal":true}`
