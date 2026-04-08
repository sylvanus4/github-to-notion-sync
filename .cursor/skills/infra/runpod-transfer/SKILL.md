---
name: runpod-transfer
description: >-
  Send and receive files between the local machine and RunPod pods via
  runpodctl's peer-to-peer transfer. Use when the user asks to "send files
  to RunPod", "download from RunPod", "transfer files", "upload dataset",
  "download checkpoint", "runpod send", "runpod receive", "runpod-transfer",
  "RunPod 파일 전송", "파일 보내기", "파일 받기", or any file transfer
  operation with RunPod.
  Do NOT use for installation or auth (use runpod-setup).
  Do NOT use for pod lifecycle management (use runpod-pods).
  Do NOT use for network volume CRUD (use runpod-volumes).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infra"
  upstream: "runpod/runpodctl"
---

# RunPod File Transfer

Send and receive files between local machine and RunPod pods using runpodctl's peer-to-peer transfer protocol.

## Prerequisites

- `runpodctl` installed and authenticated (run `runpod-setup` first)
- A running RunPod pod with `runpodctl` available inside it (pre-installed in most RunPod images)

## Commands Reference

### Send Files (Local to Pod)

On the **local machine**, initiate the send:

```bash
runpodctl send <file_or_directory>
```

This prints a **receive code** (e.g., `9338-galileo-collect-fidel`). On the **pod**, run:

```bash
runpodctl receive <code>
```

### Receive Files (Pod to Local)

On the **pod**, initiate the send:

```bash
runpodctl send <file_or_directory>
```

Copy the receive code, then on the **local machine**:

```bash
runpodctl receive <code>
```

## Common Use Cases

### Upload Training Dataset

```bash
# Local machine
runpodctl send ./datasets/training-data.tar.gz
# → Code: 9338-galileo-collect-fidel

# On the pod (via SSH or web terminal)
runpodctl receive 9338-galileo-collect-fidel
```

### Download Model Checkpoint

```bash
# On the pod
runpodctl send /workspace/checkpoints/model-final.pt
# → Code: 4521-alpha-bravo-charlie

# Local machine
runpodctl receive 4521-alpha-bravo-charlie
```

### Transfer Experiment Results

```bash
# On the pod
tar -czf results.tar.gz ./outputs/
runpodctl send results.tar.gz
# → Code: 7712-delta-echo-foxtrot

# Local machine
runpodctl receive 7712-delta-echo-foxtrot
tar -xzf results.tar.gz
```

## Workflow Integration

Combine with other RunPod skills:

1. Create a pod (`runpod-pods`)
2. Upload data (`runpod-transfer send`)
3. SSH in and run experiments (`runpod-pods ssh`)
4. Download results (`runpod-transfer receive`)
5. Stop or delete the pod (`runpod-pods`)

## Output Discipline

- Report only: file name, transfer direction, code (for send), and completion status.
- Do not suggest pod creation or volume management after transfer — those are separate skills.

## Honest Reporting

- If transfer fails or stalls, report the failure explicitly — never claim completion without confirmed file presence.
- Report file sizes before and after transfer to help the user verify integrity.

## Gotchas

- The transfer uses a **peer-to-peer relay** — both sender and receiver must be online simultaneously.
- The receive code is **one-time use** — if the transfer fails or is cancelled, re-run `send` to get a new code.
- For **large files** (>10 GB), consider compressing first with `tar -czf` to reduce transfer time.
- The transfer works across networks (no need for direct pod SSH). It routes through RunPod's relay infrastructure.
- `runpodctl` must be available on both ends. Most RunPod images have it pre-installed; if not, install inside the pod.

## Error Handling

| Error | Action |
|-------|--------|
| `code expired or invalid` | Re-run `send` to generate a fresh code |
| Transfer stalls | Check network connectivity on both ends; re-initiate |
| `runpodctl not found` on pod | Install via `wget -qO- cli.runpod.net \| bash` inside the pod |
| Large file timeout | Compress the file first; use a stable network connection |

## Verification Before Completion

- [ ] File transfer completed (confirmed via file presence on receiving end)
- [ ] File integrity verified (size or checksum comparison)
- [ ] Transfer code consumed and no longer valid
