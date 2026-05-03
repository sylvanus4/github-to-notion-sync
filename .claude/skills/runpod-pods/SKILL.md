---
name: runpod-pods
description: >-
  Create, list, manage, and SSH into RunPod GPU pods via runpodctl CLI. Use
  when the user asks to "create a pod", "list pods", "start pod", "stop pod",
  "delete pod", "SSH into pod", "RunPod pod", "GPU instance", "runpod-pods",
  "RunPod 팟", "GPU 인스턴스", "RunPod 생성", "RunPod SSH", or any pod lifecycle
  operation on RunPod. Do NOT use for installation or auth (use runpod-setup).
  Do NOT use for network volume CRUD (use runpod-volumes). Do NOT use for file
  send/receive (use runpod-transfer).
---

# RunPod Pod Management

Create, list, start, stop, restart, and delete GPU pods on RunPod. Includes SSH access.

## Prerequisites

- `runpodctl` installed and authenticated (run `runpod-setup` first)
- Verify auth: `runpodctl gpu list --output json`

## Commands Reference

### List Pods

```bash
runpodctl pod list --output json
```

Filter by status:
```bash
runpodctl pod list --status running --output json
runpodctl pod list --status exited --output json
```

### Get Pod Details

```bash
runpodctl pod get <pod-id> --output json
```

### Create Pod

```bash
runpodctl pod create \
  --gpu-id <GPU_TYPE> \
  --image <DOCKER_IMAGE> \
  --volume-size <GB> \
  --ports "<PORT_SPEC>" \
  --enable-ssh \
  --name "<POD_NAME>"
```

**Common creation patterns:**

PyTorch development pod:
```bash
runpodctl pod create \
  --gpu-id A100_SXM \
  --image runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04 \
  --volume-size 50 \
  --ports "8888/http,22/tcp" \
  --enable-ssh \
  --name "dev-pytorch"
```

Inference pod (community tier for cost savings):
```bash
runpodctl pod create \
  --gpu-id RTX_4090 \
  --image runpod/pytorch:latest \
  --volume-size 20 \
  --cloud-tier community \
  --name "inference-4090"
```

Multi-GPU training:
```bash
runpodctl pod create \
  --gpu-id A100_SXM \
  --gpu-count 4 \
  --image runpod/pytorch:latest \
  --volume-size 100 \
  --enable-ssh \
  --name "training-4xa100"
```

With network volume attached:
```bash
runpodctl pod create \
  --gpu-id A100_SXM \
  --image runpod/pytorch:latest \
  --network-volume-id <VOLUME_ID> \
  --enable-ssh \
  --name "pod-with-volume"
```

With environment variables:
```bash
runpodctl pod create \
  --gpu-id RTX_4090 \
  --image runpod/pytorch:latest \
  --env "HF_TOKEN=hf_xxx" \
  --env "WANDB_API_KEY=xxx" \
  --enable-ssh \
  --name "training-env"
```

### Lifecycle Operations

```bash
runpodctl pod start <pod-id>
runpodctl pod stop <pod-id>
runpodctl pod restart <pod-id>
```

### Update Pod

```bash
runpodctl pod update <pod-id> --gpu-count 2
```

### Delete Pod

```bash
runpodctl pod delete <pod-id>
```

### SSH Access

High-level helper (interactive, requires TTY):
```bash
runpodctl ssh <pod-id>
```

Direct endpoint (scripted / non-interactive — validated 2026-05-01 on B200 pod):
```bash
# 1. Wait for ssh.ip + ssh.port to populate
runpodctl pod get <pod-id> -o yaml | grep -E '^(ssh:|  (ip|port|error))'
# Example output:
#   ssh:
#     ip: 38.80.152.146
#     port: 30344
#     ssh_command: ssh -i ~/.runpod/ssh/RunPod-Key-Go root@38.80.152.146 -p 30344

# 2. Connect with the auto-generated key
ssh -o StrictHostKeyChecking=no -i ~/.runpod/ssh/RunPod-Key-Go \
    -p $POD_PORT root@$POD_IP
```

Notes:
- Use the direct endpoint for scp/automation; the helper requires a TTY.
- `~/.runpod/ssh/RunPod-Key-Go` (RSA) is auto-created and registered on first `runpodctl config --apiKey ...`. User-uploaded keys (e.g. `~/.ssh/id_ed25519`) work only if registered to the RunPod account.
- `ssh.error: "pod not ready"` while `ssh.status: RUNNING` means the proxy is up but the container isn't — keep polling `uptimeSeconds`.

### Capacity-Aware Multi-DC Fallback

Newer GPU types (B200 in particular) are often "Low" or "EMPTY" in any single DC. Always:

1. Check current stock first:
   ```bash
   runpodctl dc list -o json | python3 -c '
   import json,sys
   for dc in json.load(sys.stdin):
       for g in dc.get("gpuAvailability") or []:
           if "B200" in (g.get("gpuId") or ""):
               print(f"  {dc[\"id\"]:12s} stock={g.get(\"stockStatus\") or \"EMPTY\"}")'
   ```
2. Pass a comma-separated DC fallback list to `pod create`:
   ```bash
   --data-center-ids EU-RO-1,US-CA-2,US-NC-2
   ```
   RunPod tries left-to-right; first DC with capacity wins.
3. If all DCs are EMPTY, retry every 5–15 min — pool rotates.

### Pricing & Spot Caveats

- The current CLI (`runpodctl 2.1.x`) has **no `--spot` / `--interruptible` flag**. `pod create` provisions ondemand only.
- For B200, that means $5.49/hr (Secure Cloud) regardless of intent.
- Bid-priced spot pods exist via the GraphQL API but are not exposed in the CLI; expect this to change in a future CLI release. Re-verify after upgrading `runpodctl` before assuming spot is still unavailable.

### Bootstrap on Ubuntu 24.04 Pods (PEP 668)

RunPod's `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404` (template `runpod-torch-v280`, the recommended Blackwell B200 image) ships Ubuntu 24.04, which enforces **PEP 668**: bare `pip install` fails with "externally-managed-environment".

In transient pods (you control the entire OS, lifetime measured in hours), pass:
```bash
python3 -m pip install --break-system-packages --no-cache-dir <pkg>
```

**WARNING — never on local dev**: do NOT add `--break-system-packages` to your Mac/Linux dev machine setup; create a venv there. The flag is appropriate only on disposable pod root environments.

## Output Formats

All commands support three output formats:
- `--output json` (default, recommended for agent parsing)
- `--output table` (human-readable)
- `--output yaml`

## GPU Types

For common GPU IDs and their specs, see [references/pod-gpu-types.md](references/pod-gpu-types.md).

Quick reference:
```bash
runpodctl gpu list --output table
```

## Safety and Cost Awareness

- **Always confirm with the user** before creating pods — GPU instances incur hourly charges.
- Use `--cloud-tier community` for development workloads to reduce cost (~2-3x cheaper).
- Recommend `runpodctl pod stop` when work is paused to avoid idle charges.
- Document estimated hourly cost when proposing pod creation.
- **Never delete pods** without explicit user confirmation.

## Output Discipline

- Show only the fields the user asked for. Do not dump full pod JSON unless requested.
- When listing pods, show: name, id, status, GPU type. Omit detailed specs unless asked.
- When creating a pod, report: id, name, GPU, cost/hr, status. Do not add unsolicited usage tips.

## Honest Reporting

- If pod creation fails, report the exact error — never claim success without a confirmed pod ID.
- If GPU is out of stock, say so explicitly and list alternatives.
- Report actual hourly cost from the API response, not estimates.

## Gotchas

- Pod creation may fail if the requested GPU type is out of stock in all data centers. Try a different GPU type or `--cloud-tier community`.
- `--volume-size` creates an **ephemeral** container volume. For persistent storage, use `--network-volume-id` with a pre-created network volume (see `runpod-volumes`).
- SSH requires `--enable-ssh` at pod creation time; it cannot be enabled after creation.
- Port specs use the format `PORT/PROTOCOL` (e.g., `8888/http`, `22/tcp`). Multiple ports are comma-separated.

## Error Handling

| Error | Action |
|-------|--------|
| `No available machines` | Try a different `--gpu-id` or `--cloud-tier community` |
| `Invalid GPU type` | Run `runpodctl gpu list` to see valid IDs |
| `Insufficient funds` | User needs to add credits at runpod.io |
| SSH connection refused | Verify pod status is `running` and SSH was enabled at creation |
| `pod not found` | Pod may have been terminated; run `pod list --status all` |

## Verification Before Completion

- [ ] Pod created/managed successfully (confirmed via `pod get`)
- [ ] User informed of hourly cost implications
- [ ] SSH connectivity verified if SSH was enabled
