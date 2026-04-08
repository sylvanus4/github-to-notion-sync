## RunPod Volumes

Create, list, update, and delete persistent network volumes on RunPod.

### Usage

```
/runpod-volumes list                                    # List all network volumes
/runpod-volumes create --name "data" --size 100 --dc US-TX-3  # Create volume
/runpod-volumes get <volume-id>                         # Get volume details
/runpod-volumes update <volume-id> --size 200           # Resize volume (increase only)
/runpod-volumes delete <volume-id>                      # Delete volume (irreversible)
```

### Skill Reference

Read and follow the `runpod-volumes` skill (`.cursor/skills/infra/runpod-volumes/SKILL.md`) for the full command reference and data center IDs.

### Workflow

1. Verify `runpodctl` is authenticated
2. Execute the requested volume operation
3. Confirm results with `runpodctl nv get <id>`
4. Report storage cost implications

### Examples

Create a training data volume:
```
/runpod-volumes create --name "training-data" --size 100 --dc US-TX-3
```

List existing volumes:
```
/runpod-volumes list
```

Resize a volume:
```
/runpod-volumes update vol_abc123 --size 200
```
