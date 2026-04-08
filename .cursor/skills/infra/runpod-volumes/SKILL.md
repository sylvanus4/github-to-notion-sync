---
name: runpod-volumes
description: >-
  Create, list, update, and delete persistent network volumes on RunPod via
  runpodctl CLI. Use when the user asks to "create a volume", "list volumes",
  "network volume", "persistent storage", "runpod-volumes", "RunPod 볼륨",
  "네트워크 볼륨", "영구 스토리지", or any network volume operation on RunPod.
  Do NOT use for installation or auth (use runpod-setup).
  Do NOT use for pod lifecycle management (use runpod-pods).
  Do NOT use for file transfer (use runpod-transfer).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infra"
  upstream: "runpod/runpodctl"
---

# RunPod Network Volume Management

Create, list, update, and delete persistent network volumes that survive pod restarts and can be shared across pods.

## Prerequisites

- `runpodctl` installed and authenticated (run `runpod-setup` first)

## Commands Reference

### List Volumes

```bash
runpodctl nv list --output json
```

### Get Volume Details

```bash
runpodctl nv get <volume-id> --output json
```

### Create Volume

```bash
runpodctl nv create \
  --name "<VOLUME_NAME>" \
  --size <SIZE_GB> \
  --data-center-id <DATACENTER_ID>
```

**Examples:**

Standard training data volume:
```bash
runpodctl nv create --name "training-data" --size 100 --data-center-id US-TX-3
```

Model checkpoint volume:
```bash
runpodctl nv create --name "checkpoints" --size 50 --data-center-id EU-RO-1
```

### Update Volume

Resize an existing volume:
```bash
runpodctl nv update <volume-id> --size <NEW_SIZE_GB>
```

### Delete Volume

```bash
runpodctl nv delete <volume-id>
```

## Attaching Volumes to Pods

When creating a pod, attach a network volume with `--network-volume-id`:

```bash
runpodctl pod create \
  --gpu-id A100_SXM \
  --image runpod/pytorch:latest \
  --network-volume-id <VOLUME_ID> \
  --enable-ssh \
  --name "pod-with-nv"
```

The volume mounts at `/runpod-volume/` inside the pod by default.

## Data Center IDs

Common data center identifiers (run `runpodctl datacenter list` for the full list):

| ID | Region |
|----|--------|
| `US-TX-3` | Dallas, Texas |
| `US-GA-1` | Atlanta, Georgia |
| `US-OR-1` | Portland, Oregon |
| `EU-RO-1` | Bucharest, Romania |
| `EU-SE-1` | Stockholm, Sweden |
| `CA-MTL-1` | Montreal, Canada |

A volume and a pod must be in the **same data center** to attach.

## Output Discipline

- When listing volumes, show: name, id, size, data center, status. Omit detailed metadata unless asked.
- Do not suggest pod creation after volume operations — the user will invoke `runpod-pods` when ready.

## Honest Reporting

- If volume creation fails (quota, invalid data center), report the exact error.
- Never claim a volume is ready without confirming via `nv get`.
- Report actual storage charges when creating or updating volumes.

## Gotchas

- Network volumes are **region-locked** — a volume in `US-TX-3` can only attach to pods in `US-TX-3`.
- Volumes incur storage charges even when no pod is attached. Delete unused volumes to avoid costs.
- Volume size can only be **increased**, not decreased. Plan initial sizing carefully.
- Deleting a volume is **irreversible** — all data is lost.
- Multiple pods can share the same network volume, but concurrent writes from different pods require filesystem-level coordination.

## Error Handling

| Error | Action |
|-------|--------|
| `data center not found` | Run `runpodctl datacenter list` for valid IDs |
| `volume not found` | Volume may have been deleted; check with `nv list` |
| `cannot attach` | Volume and pod must be in the same data center |
| `insufficient storage quota` | Contact RunPod support or upgrade plan |

## Verification Before Completion

- [ ] Volume created/managed successfully (confirmed via `nv get`)
- [ ] User informed that volumes incur storage charges when idle
- [ ] Data center compatibility with intended pods verified
