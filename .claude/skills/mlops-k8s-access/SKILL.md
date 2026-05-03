---
name: mlops-k8s-access
description: >-
  Manage MLOps Kubernetes cluster access, context switching, GPU/MIG pod
  deployment, NFS storage provisioning, GHCR image build/push, and resource
  availability checks across 6 TKAI clusters (stage, dev, b200, demo, master,
  kata). Use when the user asks to "switch cluster", "deploy GPU pod", "deploy
  MIG pod", "check GPU availability", "check resources", "create PVC", "push
  to GHCR", "create ghcr-secret", "generate pod YAML", "MLOps 배포", "클러스터 전환",
  "GPU 파드 배포", "MIG 파드", "NFS 볼륨 생성", "PVC 생성", "GHCR 이미지 빌드", "GHCR 푸시", "이미지
  시크릿", "GPU 리소스 확인", "노드 확인", "mlops-k8s-access", or any MLOps K8s deployment
  task. Do NOT use for Helm chart validation (use helm-validator). Do NOT use
  for IaC review (use iac-review-agent). Do NOT use for local dev environment
  setup (use local-dev-setup).
disable-model-invocation: true
---

# MLOps Kubernetes Access and Deployment

Manage multi-cluster TKAI Kubernetes access, GPU/MIG workload deployment, NFS storage provisioning, and GHCR container image workflows.

## When to Use

- Switching between TKAI cluster contexts (stage, dev, b200, demo, master, kata)
- Deploying pods that require GPU or MIG GPU resources
- Creating PersistentVolumeClaims with NFS StorageClasses
- Building and pushing container images to GHCR (`ghcr.io/thakicloud/`)
- Creating `ghcr-secret` for private image pulls
- Checking GPU/MIG resource availability before deployment
- Generating complete pod YAML specs with all required fields

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `kubectl` | `brew install kubectl` | Cluster access and pod management |
| `docker` | Docker Desktop or `brew install --cask docker` | Image build and push |
| GitHub PAT | https://github.com/settings/tokens | GHCR authentication (`read:packages`, `write:packages`) |
| kubeconfig files | Pre-downloaded to `~/.kube/` | Cluster credentials |

## Anti-Gold-Plating

- Generate ONLY the YAML the user asked for; do not add Deployment/Service/Ingress unless requested.
- Do NOT create namespaces, RBAC roles, or network policies unless the user explicitly asks.
- Do NOT apply (`kubectl apply`) generated YAML without user confirmation — output it for review first.
- Stick to the exact nodeSelector and resource limits that match the user's stated node type.

## Cluster Registry

| Cluster | Config File | Path | Description |
|---------|-------------|------|-------------|
| Staging | `tkai-stage.config` | `~/.kube/tkai-stage.config` | Staging environment |
| Development | `tkai-dev.config` | `~/.kube/tkai-dev.config` | Development environment |
| B200 | `tkai-b200.config` | `~/.kube/tkai-b200.config` | B200 GPU cluster |
| Demo | `tkai-demo.config` | `~/.kube/tkai-demo.config` | Demo environment |
| Master | `tkai-master.config` | `~/.kube/tkai-master.config` | Master/production cluster |
| Kata | `tkai-kata.config` | `~/.kube/tkai-kata.config` | Kata container cluster |

## Step 0: Determine Intent (AskQuestion)

If the user's intent is ambiguous, use AskQuestion to clarify:

| id | prompt | options |
|----|--------|---------|
| `cluster` | Which TKAI cluster? | `stage`, `dev`, `b200`, `demo`, `master`, `kata` |
| `node_type` | What node type for deployment? | `gpu` (Full GPU), `mig` (MIG GPU), `cpu` (CPU only) |
| `storage` | Need persistent storage? | `shared` (tkai-nfs-agent), `individual` (tkai-nfs-agent-individual), `none` |
| `ghcr` | Need GHCR image pull secret? | `yes`, `no` |

Skip questions when the user already provided enough context.

## Workflow

Route to the appropriate mode based on user intent.

### Mode 1: Switch Cluster

Set the `KUBECONFIG` environment variable and verify connectivity.

```bash
export KUBECONFIG="$HOME/.kube/tkai-<cluster>.config"
kubectl cluster-info
kubectl get nodes
```

**Verification**: `kubectl cluster-info` must return a reachable API server URL. If it times out, the cluster may require VPN access.

### Mode 2: Deploy GPU Pod

Generate a pod spec targeting GPU nodes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <pod-name>
spec:
  nodeSelector:
    node-role.kubernetes.io/gpu: ""
  containers:
    - name: <container-name>
      image: <image>
      resources:
        limits:
          nvidia.com/gpu: <count>
```

Constraints:
- nodeSelector MUST be `node-role.kubernetes.io/gpu: ""`
- Only one nodeSelector role at a time (gpu, mig, or cpu)
- Run Mode 5 first to confirm available GPU count on the target cluster

### Mode 3: Deploy MIG Pod

Generate a pod spec targeting MIG GPU nodes. MIG slices the GPU into smaller isolated instances.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <pod-name>
spec:
  nodeSelector:
    node-role.kubernetes.io/mig: ""
  containers:
    - name: <container-name>
      image: <image>
      resources:
        limits:
          nvidia.com/mig-4g.47gb: 1
```

Constraints:
- nodeSelector MUST be `node-role.kubernetes.io/mig: ""` (not gpu)
- Use MIG resource keys (e.g. `nvidia.com/mig-4g.47gb`) instead of `nvidia.com/gpu`
- MIG must be enabled on the cluster (`nvidia.com/mig.config` != `all-disabled`); run Mode 5 to verify MIG slice availability before deploying

### Mode 4: Create PVC

Prompt for StorageClass and generate PVC YAML.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <pvc-name>
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: <storage-class>
  resources:
    requests:
      storage: <size>Gi
```

StorageClass options:

| StorageClass | Sharing | NFS Server | Use Case |
|--------------|---------|------------|----------|
| `tkai-nfs-agent` | Shared (ReadWriteMany) | 10.7.12.240 | Multi-pod shared data |
| `tkai-nfs-agent-individual` | Individual | 10.7.12.240 | Single-pod private data |

**Verification**: After `kubectl apply`, run `kubectl get pvc <name>` and confirm status is `Bound`.

### Mode 5: Check Resources

Run these commands to assess resource availability before deployment:

```bash
# Node overview with roles and GPU info
kubectl get nodes -o custom-columns='NAME:.metadata.name,ROLES:.metadata.labels.node-role\.kubernetes\.io/gpu,CPU:.status.allocatable.cpu,MEM:.status.allocatable.memory'

# GPU allocatable vs allocated on GPU nodes
kubectl describe nodes -l node-role.kubernetes.io/gpu= | grep -A 10 "Allocated resources"

# MIG availability — check if MIG is enabled and which slices exist
kubectl get nodes -l node-role.kubernetes.io/gpu= -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.nvidia\.com/mig\.config}{"\t"}{.status.allocatable.nvidia\.com/gpu}{"\n"}{end}'

# Available StorageClasses
kubectl get sc

# Pending pods (scheduling failures)
kubectl get pods --all-namespaces --field-selector=status.phase=Pending
```

Grafana dashboards for real-time monitoring:
- **Prod/Stage**: https://grafana.tkai.thakicloud.site
- **Dev**: https://grafana.tkai.dev.thakicloud.site

### Mode 6: GHCR Build & Push

Build a container image and push to GitHub Container Registry.

```bash
# Login (requires GitHub PAT with read:packages + write:packages)
echo <github_pat> | docker login ghcr.io -u <github_username> --password-stdin

# Build
docker build -t ghcr.io/thakicloud/<image_name>:<tag> .

# Push
docker push ghcr.io/thakicloud/<image_name>:<tag>
```

GitHub PAT creation:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Enable scopes: `read:packages`, `write:packages`
4. Copy the token immediately (shown only once)
5. The account must have access to the `thakicloud` organization

**Verification**: `docker login` must print `Login Succeeded`. After push, verify with `docker pull ghcr.io/thakicloud/<image_name>:<tag>`.

### Mode 7: Create ghcr-secret

Create an imagePullSecret for pulling private GHCR images. Must be created in every namespace where private images are used.

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<github_username> \
  --docker-password=<github_pat> \
  --docker-email=<email> \
  --namespace=<namespace>
```

**Verification**:
```bash
kubectl get secret ghcr-secret -n <namespace>
```

### Mode 8: Generate Full Pod YAML

Composite template combining all elements: nodeSelector, GPU/MIG resources, PVC mount, and imagePullSecrets.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <pod-name>
spec:
  nodeSelector:
    node-role.kubernetes.io/gpu: ""
  containers:
    - name: <container-name>
      image: ghcr.io/thakicloud/<image>:<tag>
      resources:
        limits:
          nvidia.com/gpu: 1
      volumeMounts:
        - name: data
          mountPath: /mnt/data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: <pvc-name>
  imagePullSecrets:
    - name: ghcr-secret
```

Adapt the template based on user requirements:
- Replace `gpu` nodeSelector with `mig` or `cpu` as needed
- Replace `nvidia.com/gpu` with `nvidia.com/mig-4g.47gb` for MIG
- Remove `volumes`/`volumeMounts` if no storage needed
- Remove `imagePullSecrets` if using public images
- This template also applies to Deployment, Job, and StatefulSet (add under `spec.template.spec`)

## Output Format

- YAML templates: print to stdout in a fenced code block; do NOT write files unless the user says "save" or "apply"
- Mode 5 (Check Resources): summarize as a markdown table with node name, role, GPU count, and availability
- Verification results: single-line pass/fail with the command used

## Verification Checklist

After every mode, run the corresponding verification step:

| Mode | Verification Command | Success Criteria |
|------|---------------------|-----------------|
| 1 (Switch) | `kubectl cluster-info` | API server URL returned without timeout |
| 2/3 (Deploy) | `kubectl get pod <name> -w` | Pod reaches `Running` state |
| 4 (PVC) | `kubectl get pvc <name>` | Status is `Bound` |
| 5 (Check) | N/A | Resource table displayed |
| 6 (GHCR) | `docker pull ghcr.io/thakicloud/<image>:<tag>` | Pull succeeds |
| 7 (Secret) | `kubectl get secret ghcr-secret -n <ns>` | Secret exists |
| 8 (Full YAML) | `kubectl apply --dry-run=client -f <file>` | No validation errors |

## Node Selector Reference

| Role | nodeSelector Label | Description |
|------|--------------------|-------------|
| GPU | `node-role.kubernetes.io/gpu: ""` | Full GPU nodes (H100 NVL, B200) |
| Multi-GPU | `node-role.kubernetes.io/multi-gpu: ""` | Multi-GPU capable nodes |
| Multi-GPU-4 | `node-role.kubernetes.io/multi-gpu-4: ""` | 4-GPU nodes |
| MIG | `node-role.kubernetes.io/mig: ""` | MIG-partitioned GPU nodes (when MIG enabled) |
| CPU | `node-role.kubernetes.io/cpu: ""` | CPU-only nodes |
| NFS | `node-role.kubernetes.io/nfs: ""` | NFS server nodes |

Only specify ONE primary role per pod (`gpu`, `mig`, or `cpu`). Multiple nodeSelector roles cause scheduling failures unless the target node carries all specified labels.

## GPU/MIG Resource Reference

| Type | Resource Key | Hardware | Notes |
|------|-------------|----------|-------|
| Full GPU | `nvidia.com/gpu` | H100 NVL (95GB), B200 (192GB) | Use with `gpu` nodeSelector |
| MIG 4g.47gb | `nvidia.com/mig-4g.47gb` | H100 MIG slice | Use with `mig` nodeSelector; requires MIG enabled |
| MIG 1g.12gb | `nvidia.com/mig-1g.12gb` | H100 MIG slice | Smallest MIG partition |

## Gotchas

1. **MIG availability varies by cluster**: MIG mode is configured per-cluster. Check `nvidia.com/mig.config` label — if `all-disabled`, no MIG slices are schedulable. Run Mode 5 before deploying MIG pods.
2. **nodeSelector mismatch**: GPU nodes may carry multiple role labels (`gpu`, `multi-gpu`, `multi-gpu-4`), but MIG nodes require the `mig` label. Never mix `nvidia.com/gpu` with `nvidia.com/mig-*` resources.
3. **ghcr-secret is namespace-scoped**: The secret must exist in the SAME namespace as the pod. Creating it in `default` does not make it available in other namespaces.
4. **VPN requirement**: Some clusters (e.g., dev) may require VPN connectivity. If `kubectl cluster-info` times out, connect to VPN first.
5. **PAT expiration**: GitHub PATs expire. If `docker login` or `imagePullSecrets` suddenly fail, regenerate the PAT and update the secret.

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `kubeconfig not found` | Config file path incorrect or missing | Verify file exists at `~/.kube/tkai-*.config`; re-download if needed |
| `Unable to connect to the server` | Cluster unreachable or VPN not connected | Check VPN; try `ping` to cluster API; verify kubeconfig server URL |
| `SchedulingFailed` | No nodes match nodeSelector or insufficient GPU/MIG resources | Run Mode 5 to check availability; verify nodeSelector matches node labels |
| `ImagePullBackOff` | Missing `ghcr-secret` or invalid PAT | Run Mode 7 to create secret; verify PAT has `read:packages` scope |
| `MIG resource not found` | Using `nvidia.com/gpu` on MIG nodes or MIG disabled | Check `nvidia.com/mig.config` label; match resource key to nodeSelector |
| `PVC Pending` | StorageClass not available or NFS server unreachable | Verify StorageClass exists with `kubectl get sc`; check NFS server 10.7.12.240 connectivity |
| `Forbidden` | RBAC insufficient for the namespace | Contact cluster admin for namespace access |

## Troubleshooting

### Pod stuck in Pending
1. Check events: `kubectl describe pod <name>`
2. Look for `FailedScheduling` events
3. Run Mode 5 to verify resource availability
4. Confirm nodeSelector matches actual node labels: `kubectl get nodes --show-labels`

### Cannot pull GHCR image
1. Verify secret exists in the pod's namespace: `kubectl get secret ghcr-secret -n <namespace>`
2. Verify PAT is valid: `echo <pat> | docker login ghcr.io -u <user> --password-stdin`
3. Verify `imagePullSecrets` is set in the pod spec
4. Verify the PAT account has access to the `thakicloud` organization

### MIG scheduling mismatch
1. Confirm MIG is enabled on the cluster: `kubectl get nodes -l node-role.kubernetes.io/gpu= -o jsonpath='{.items[*].metadata.labels.nvidia\.com/mig\.config}'` — must NOT be `all-disabled`
2. Use `nvidia.com/mig-*` resource keys (not `nvidia.com/gpu`) on MIG nodes
3. Verify available MIG slices: `kubectl describe nodes -l node-role.kubernetes.io/gpu= | grep nvidia.com/mig`
