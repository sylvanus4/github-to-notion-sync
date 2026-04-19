# kubectl GPU Commands Reference

Quick reference for GPU resource inspection on the `tkai-demo` cluster.

## Cluster-Level

```bash
# Node GPU capacity table
kubectl get nodes --context=tkai-demo \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}capacity={.status.capacity.nvidia\.com/gpu}{"\t"}allocatable={.status.allocatable.nvidia\.com/gpu}{"\n"}{end}'

# Allocation detail per node
kubectl describe nodes --context=tkai-demo | grep -A 5 "Allocated resources" | grep nvidia

# Node labels (GPU type)
kubectl get nodes --context=tkai-demo --show-labels | grep nvidia
```

## Pod-Level

```bash
# All GPU-consuming pods (running + pending)
kubectl get pods -A --context=tkai-demo -o json | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('NAMESPACE\tPOD\tGPU_REQ\tGPU_LIM\tNODE\tPHASE')
for p in d['items']:
  for c in p['spec'].get('containers',[]):
    r=c.get('resources',{}).get('requests',{}).get('nvidia.com/gpu','0')
    l=c.get('resources',{}).get('limits',{}).get('nvidia.com/gpu','0')
    if int(r or 0)>0 or int(l or 0)>0:
      print(f\"{p['metadata']['namespace']}\t{p['metadata']['name']}\t{r}\t{l}\t{p['spec'].get('nodeName','Pending')}\t{p['status']['phase']}\")
"

# Pod owner (deployment/job/replicaset)
kubectl get pod <POD> -n <NS> --context=tkai-demo -o jsonpath='{.metadata.ownerReferences[0].kind}/{.metadata.ownerReferences[0].name}'
```

## GPU Utilization (In-Pod)

```bash
# Full nvidia-smi output
kubectl exec -n <NS> <POD> --context=tkai-demo -- nvidia-smi

# CSV metrics
kubectl exec -n <NS> <POD> --context=tkai-demo -- nvidia-smi \
  --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total \
  --format=csv,noheader,nounits

# Process list
kubectl exec -n <NS> <POD> --context=tkai-demo -- nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv,noheader
```

## Actions

```bash
# Delete a specific pod
kubectl delete pod <POD> -n <NS> --context=tkai-demo

# Patch deployment to remove GPU request
kubectl patch deployment <DEPLOY> -n <NS> --context=tkai-demo --type=json \
  -p='[{"op":"remove","path":"/spec/template/spec/containers/0/resources/requests/nvidia.com~1gpu"},{"op":"remove","path":"/spec/template/spec/containers/0/resources/limits/nvidia.com~1gpu"}]'

# Scale down to release GPU
kubectl scale deployment <DEPLOY> -n <NS> --context=tkai-demo --replicas=0
```

## Pending Pods

```bash
# Pending pods requesting GPUs
kubectl get pods -A --context=tkai-demo --field-selector=status.phase=Pending -o json | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d['items']:
  for c in p['spec'].get('containers',[]):
    r=c.get('resources',{}).get('requests',{}).get('nvidia.com/gpu','0')
    if int(r or 0)>0:
      print(f\"{p['metadata']['namespace']}\t{p['metadata']['name']}\tGPU:{r}\")
"

# Events for a pending pod
kubectl describe pod <POD> -n <NS> --context=tkai-demo | tail -20
```

## Known tkai-demo Cluster Facts

- **GPU Nodes**: 5 nodes, each with 1x NVIDIA H100 NVL (80GB)
- **Total Cluster GPUs**: 5
- **Common waste patterns**: nginx pods with GPU requests, embedding services with idle GPUs, abandoned dev pods
