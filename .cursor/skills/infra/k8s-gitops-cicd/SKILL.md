---
name: k8s-gitops-cicd
description: >-
  Design and maintain Kubernetes-native CI/CD pipelines with GitOps
  principles for the TKAI AI Platform. Covers GitHub Actions workflows
  for building and tagging GHCR images, the weekly release cycle
  (release-ops skills for Tuesday RC tagging, Wednesday QA gate,
  Thursday deployment), ArgoCD-driven continuous deployment, Helm chart
  versioning, KEDA-based scaling integration in pipelines, and
  environment promotion strategies. Use when the user asks to "design
  CI/CD", "build GHA workflow", "image promotion", "release pipeline",
  "GitOps deployment", "weekly release cycle", "KEDA pipeline
  integration", "CI/CD 설계", "GHA 워크플로우", "이미지 프로모션",
  "릴리즈 파이프라인", "GitOps 배포", "주간 릴리즈",
  "k8s-gitops-cicd", or any CI/CD pipeline design task for Kubernetes
  workloads. Do NOT use for ArgoCD Application management (use
  argocd-expert). Do NOT use for GitOps pattern design (use
  argocd-gitops-patterns). Do NOT use for Kubernetes manifest
  generation (use k8s-deployment-creator). Do NOT use for Helm chart
  validation (use helm-validator).
metadata:
  version: "1.1.0"
  category: "infra"
  author: "thaki"
---

# K8s GitOps CI/CD

You are a CI/CD pipeline specialist for the TKAI AI Platform's Kubernetes-native GitOps infrastructure.

## Project Context

- Registry: GHCR (`ghcr.io/thakicloud/`)
- Image tag convention: `dev-{SHA}` → `rc-{TIMESTAMP}` → `vYYYY.MM.DD`
- CI platform: GitHub Actions
- CD platform: ArgoCD (namespace: `argo`)
- Weekly release cycle managed by **release-ops skills** (not raw GHA):
  - `release-collector`: Tuesday RC tagging
  - `release-qa-gate`: Wednesday QA
  - `release-deployer`: Thursday production deploy
- Hotfixes: `hotfix-manager` skill, any day
- Clusters: 6 TKAI k0s clusters
- Autoscaling: KEDA HTTPScaledObject
- Progressive delivery: Argo Rollouts

## Pipeline Architecture

```
Developer PR → GHA Build & Test → Merge to dev
                                      ↓
                               GHA: Build → Push ghcr.io/thakicloud/{service}:dev-{SHA}
                                      ↓
                               ArgoCD auto-sync → dev cluster (automated selfHeal)
                                      ↓
                          Tuesday: release-collector → re-tag HEAD as rc-{TIMESTAMP}
                                      ↓
                          Wednesday: release-qa-gate → QA on dev with rc image
                                      ↓
                          Thursday: release-deployer → promote rc → v{YYYY.MM.DD} → prod
```

## GitHub Actions Workflows

### Build and Push (on merge to dev)

```yaml
name: Build and Push
on:
  push:
    branches: [dev]
    paths:
      - "backend/go/**"
      - "!**.md"

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: thakicloud

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ github.event.repository.name }}
          tags: |
            type=raw,value=dev-${{ github.sha }}
            type=raw,value=dev-latest

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./backend/go/Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=dev-${{ github.sha }}
```

### Weekly Release Cycle

The weekly release cycle is **NOT a GHA workflow** — it's managed by the release-ops Cursor skills:

| Day | Skill | Action |
|-----|-------|--------|
| Tuesday AM | `release-collector` | Scan merged PRs on dev since last release, enforce 3-label gate (`release:approved` / `release:hold` / `release:blocked`), re-tag dev HEAD image as `rc-{TIMESTAMP}`, create Notion weekly release page |
| Wednesday | `release-qa-gate` | Track QA results in Notion, exclude items without QA results, rebuild rc if needed |
| Thursday | `release-deployer` | Promote rc → `vYYYY.MM.DD` production tag, deploy via ArgoCD, restore dev to latest HEAD |

```bash
# Tuesday RC tagging (done by release-collector skill)
# Re-tags existing dev image — no new build
crane tag ghcr.io/thakicloud/{service}:dev-{HEAD_SHA} rc-$(date +%s)

# Thursday production promotion (done by release-deployer skill)
crane tag ghcr.io/thakicloud/{service}:rc-{TIMESTAMP} v$(date +%Y.%m.%d)
```

### Hotfix Pipeline

```bash
# Hotfix (any day, managed by hotfix-manager skill)
# 1. PR merged to hotfix branch → GHA builds with hotfix-{SHA} tag
# 2. hotfix-manager validates impact statement + notification status
# 3. Manual approval → promote to vYYYY.MM.DD-hotfix.N
```

## Helm Chart Versioning

```yaml
# Chart.yaml
apiVersion: v2
name: vllm
version: 0.1.0          # Chart version — bump on chart structure changes
appVersion: "dev-latest" # Overridden by CI with image tag
```

```yaml
# values.yaml — image tag is the only thing that changes per environment
image:
  repository: ghcr.io/thakicloud/vllm-openai
  tag: "dev-latest"      # Overridden by ArgoCD Helm parameters
  pullPolicy: IfNotPresent
```

ArgoCD sets the image tag via Helm parameter override:
```yaml
# ArgoCD Application spec
source:
  helm:
    parameters:
      - name: image.tag
        value: "vYYYY.MM.DD"   # Set by release-deployer
```

## KEDA Integration in Pipelines

When deploying services with KEDA autoscaling:

```yaml
# values-production.yaml
keda:
  enabled: true
  host: "api.tkai.example.com"
  minReplicas: 2
  maxReplicas: 20
  targetRequestRate: 200

# IMPORTANT: When keda.enabled is true, the Deployment template
# must NOT set spec.replicas — KEDA manages it.
```

Pipeline consideration: after deploying a new version, KEDA scaling decisions are based on incoming HTTP request rate, so canary or blue-green strategies with Argo Rollouts should configure separate KEDA targets per service variant.

## Environment-Specific Overrides

```
charts/vllm/
├── Chart.yaml
├── values.yaml              # Base values
├── values-worker.yaml       # Worker cluster defaults
├── values-dev.yaml          # Dev environment
├── values-stage.yaml        # Staging
└── values-production.yaml   # Production
```

ArgoCD selects the values file via `spec.source.helm.valueFiles`:
```yaml
source:
  helm:
    valueFiles:
      - values-worker.yaml
      - values-{{ .Values.environment }}.yaml
```

## Secret Management in Pipelines

```yaml
# External Secrets Operator for production
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: vllm-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: vllm-secrets
  data:
    - secretKey: HF_TOKEN
      remoteRef:
        key: tkai/vllm
        property: hf_token
```

## Quality Gates

### Pre-merge (GHA)
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: golangci/golangci-lint-action@v6
  test:
    runs-on: ubuntu-latest
    steps:
      - run: go test ./... -race -coverprofile=coverage.out
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
```

### Post-deploy (ArgoCD health)
```bash
# Verify deployment health after ArgoCD sync
argocd app wait {APP_NAME} --health --timeout 600
argocd app get {APP_NAME} -o json | jq '.status.health.status'
```

## Troubleshooting

### Image not found after promotion
```bash
# Verify image exists in GHCR
crane manifest ghcr.io/thakicloud/{service}:{tag}
# Check if promotion tag was created
crane ls ghcr.io/thakicloud/{service} | grep "rc-\|^v"
```

### ArgoCD sync fails after image tag change
```bash
# Hard refresh to clear cached manifests
argocd app get {APP} --hard-refresh
# Check Helm parameter override
argocd app get {APP} -o json | jq '.spec.source.helm.parameters'
```

### KEDA not scaling after deployment
```bash
# Check HTTPScaledObject status
kubectl get httpscaledobject {NAME} -o yaml
# Verify KEDA operator is running
kubectl -n keda get pods
# Check KEDA metrics
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1"
```

### Release-collector skipped a PR
```bash
# Check PR labels — must have release:approved
gh pr list --label "release:approved" --state merged --base dev
# Unlabeled PRs are auto-held by release-collector
```

## Common Pitfalls

1. **Don't build new images for RC tagging** — RC tagging re-tags existing `dev-{SHA}` images. Building new images introduces untested code.
2. **Don't use GHA for the release cycle** — The weekly release cycle (Tuesday/Wednesday/Thursday) is managed by release-ops Cursor skills, not GHA workflows.
3. **KEDA + Deployment replicas conflict** — When `keda.enabled` is true, don't set `spec.replicas` in the Deployment. KEDA manages replica count.
4. **Missing `values-worker.yaml`** — Worker cluster deployments require the worker-specific values file. Without it, ArgoCD uses base values which lack cluster-specific overrides.
5. **Image tag format matters** — `dev-{SHA}` (lowercase hex), `rc-{TIMESTAMP}` (Unix epoch), `vYYYY.MM.DD` (with leading `v`). Wrong format breaks ArgoCD parameter matching.
6. **ArgoCD namespace is `argo`** — All ArgoCD operations must target the `argo` namespace, not the default `argocd`.

## Constraints

- Do NOT build new images during RC tagging — re-tag existing `dev-{SHA}` images only
- Do NOT implement the weekly release cycle in GitHub Actions — it's managed by release-ops Cursor skills
- Do NOT set `spec.replicas` in Deployments when KEDA is enabled
- Do NOT skip the 3-label gate (`release:approved` / `release:hold` / `release:blocked`)
- Freedom level: **Low** — CI/CD pipeline changes affect all deployment environments

## Output Format

- **GHA workflow YAML**: Complete `.github/workflows/*.yaml` files
- **Pipeline diagram**: ASCII or Mermaid diagram showing PR-to-production flow
- **Environment matrix**: Which image tags deploy to which clusters
- **Secret requirements**: List of required GitHub and Kubernetes secrets

## Verification

After creating or modifying a pipeline:

### Check: GHA workflow syntax
**Command:** `gh workflow list` and `gh run list --workflow=<NAME>`
**Expected:** Workflow listed, no syntax errors in recent runs

### Check: Image exists in GHCR
**Command:** `crane manifest ghcr.io/thakicloud/<SERVICE>:<TAG>`
**Expected:** Valid manifest (not 404)

### Check: ArgoCD picks up new image
**Command:** `argocd app get <APP> -o json | jq '.spec.source.helm.parameters[] | select(.name=="image.tag")'`
**Expected:** Tag matches the promoted image version
