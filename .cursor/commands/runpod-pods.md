## RunPod Pods

Create, list, manage, and SSH into RunPod GPU pods.

### Usage

```
/runpod-pods list                                   # List all pods
/runpod-pods list --status running                  # List running pods only
/runpod-pods create --gpu A100_SXM --name "dev"     # Create a pod
/runpod-pods get <pod-id>                           # Get pod details
/runpod-pods start <pod-id>                         # Start a stopped pod
/runpod-pods stop <pod-id>                          # Stop a running pod
/runpod-pods delete <pod-id>                        # Delete a pod
/runpod-pods ssh <pod-id>                           # SSH into a pod
```

### Skill Reference

Read and follow the `runpod-pods` skill (`.cursor/skills/infra/runpod-pods/SKILL.md`) for the full command reference, GPU types, and safety guidelines.

### Workflow

1. Verify `runpodctl` is authenticated (`runpodctl gpu list`)
2. Execute the requested pod operation
3. Confirm results with `runpodctl pod get <id>`
4. Report cost implications for create/start operations

### Examples

Create a PyTorch dev pod:
```
/runpod-pods create --gpu RTX_4090 --name "pytorch-dev" --image runpod/pytorch:latest --ssh
```

List and stop idle pods:
```
/runpod-pods list --status running
/runpod-pods stop <pod-id>
```

SSH into a running pod:
```
/runpod-pods ssh abc123
```
