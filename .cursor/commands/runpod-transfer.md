## RunPod Transfer

Send and receive files between the local machine and RunPod pods.

### Usage

```
/runpod-transfer send <file_or_dir>       # Send file/dir, get a receive code
/runpod-transfer receive <code>           # Receive a file using the code
```

### Skill Reference

Read and follow the `runpod-transfer` skill (`.cursor/skills/infra/runpod-transfer/SKILL.md`) for the full workflow and integration patterns.

### Workflow

1. Verify `runpodctl` is available on both local machine and pod
2. Initiate send on one end, receive on the other
3. Verify file integrity after transfer

### Examples

Upload a dataset to a pod:
```
/runpod-transfer send ./datasets/train.tar.gz
# Copy the code, then on the pod: runpodctl receive <code>
```

Download results from a pod:
```
# On the pod: runpodctl send ./results/
# Then locally:
/runpod-transfer receive 9338-galileo-collect-fidel
```
