# GPU Resource Inspector

Inspect GPU resource allocation, utilization, and waste across Kubernetes clusters. Supports 5 workflow modes that progressively deepen analysis from cluster-level overview to actionable reclamation recommendations.

## Triggers

Use when the user asks to "check GPU usage", "GPU 현황", "GPU 리소스 확인", "GPU waste", "GPU 낭비", "which pods use GPUs", "GPU 어떤 팟이 쓰는지", "reclaim GPU", "GPU 회수", "pending GPU pods", "GPU 대기 팟", "gpu-resource-inspector", or any Kubernetes GPU resource visibility request.

Do NOT use for:
- General Kubernetes troubleshooting without GPU focus (use `kubectl` directly)
- GPU driver installation or node setup (use infrastructure skills)
- Non-Kubernetes GPU monitoring (use `nvidia-smi` directly)
- Cluster context switching (use `kube-cluster-switch` skill)

## Constraints

- Always use `--context=tkai-demo` explicitly in all `kubectl` commands
- Never delete pods in `kube-system` namespace
- Require explicit user confirmation before any destructive action
- Report all output in Korean unless user specifies otherwise
- Read `references/kubectl-gpu-commands.md` before executing any workflow

## Workflow Modes

### Mode 1: Cluster GPU Summary

Quick overview of GPU capacity and allocation across all nodes.

```bash
# Total GPU capacity
kubectl get nodes --context=tkai-demo -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.nvidia\.com/gpu}{"\t"}{.status.allocatable.nvidia\.com/gpu}{"\n"}{end}'

# GPU allocation summary
kubectl describe nodes --context=tkai-demo | grep -A 5 "Allocated resources" | grep nvidia
```

**Output**: Table with Node Name, GPU Capacity, GPU Allocatable, GPU Allocated, GPU Available.

### Mode 2: GPU Pod Detail

List all pods consuming GPU resources with ownership and utilization data.

```bash
# All pods requesting GPUs
kubectl get pods --all-namespaces --context=tkai-demo -o json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for pod in data['items']:
    for c in pod['spec'].get('containers', []):
        req = c.get('resources', {}).get('requests', {}).get('nvidia.com/gpu', '0')
        lim = c.get('resources', {}).get('limits', {}).get('nvidia.com/gpu', '0')
        if int(req or 0) > 0 or int(lim or 0) > 0:
            ns = pod['metadata']['namespace']
            name = pod['metadata']['name']
            node = pod['spec'].get('nodeName', 'Pending')
            phase = pod['status']['phase']
            owners = pod['metadata'].get('ownerReferences', [])
            owner = owners[0]['kind'] + '/' + owners[0]['name'] if owners else 'standalone'
            print(f'{ns}\t{name}\t{owner}\t{node}\t{req}\t{lim}\t{phase}')
"
```

**Output**: Table with Namespace, Pod, Owner, Node, GPU Request, GPU Limit, Phase.

### Mode 3: Waste Detection

Identify pods with GPU allocation but zero or minimal utilization.

**Waste indicators**:
- **Misconfigured**: Pod requests GPU but container has no GPU workload (no nvidia-smi)
- **Idle**: GPU allocated, nvidia-smi shows 0% utilization and 0 MiB memory
- **Underutilized**: GPU compute utilization < 10% for extended period

```bash
# Check GPU utilization inside a pod
kubectl exec -n <namespace> <pod> --context=tkai-demo -- nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total --format=csv,noheader,nounits
```

If `nvidia-smi` is not found, classify the pod as **Misconfigured**.

### Mode 4: Pending Pod Analysis

Find pods waiting for GPU resources that cannot be scheduled.

```bash
kubectl get pods --all-namespaces --context=tkai-demo --field-selector=status.phase=Pending -o json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for pod in data['items']:
    for c in pod['spec'].get('containers', []):
        req = c.get('resources', {}).get('requests', {}).get('nvidia.com/gpu', '0')
        if int(req or 0) > 0:
            ns = pod['metadata']['namespace']
            name = pod['metadata']['name']
            print(f'{ns}\t{name}\tGPU requested: {req}')
"
```

### Mode 5: Action Recommendations

Based on Modes 1-4, generate prioritized recommendations:

1. **Immediate**: Delete misconfigured pods (e.g., nginx with GPU request)
2. **High**: Reclaim idle GPU pods (0% utilization for >24h)
3. **Medium**: Patch deployments to remove unnecessary GPU requests
4. **Low**: Right-size underutilized GPU allocations

Present recommendations as a numbered action list with estimated GPU recovery count.

## Tags

`kubernetes`, `gpu`, `nvidia`, `resource-management`, `waste-detection`, `tkai-demo`
