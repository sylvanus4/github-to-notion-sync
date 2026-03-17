---
name: hf-buckets
description: >-
  Manage S3-style object storage (Xet backend) on Hugging Face Hub via the
  hf CLI. Use when the user asks to create a bucket, upload files to a bucket,
  sync directories, list bucket contents, download from a bucket, or manage
  large artifact storage for checkpoints, logs, and datasets.
  Do NOT use for model uploads to repos (use hf-models with hf upload),
  file management in repos (use hf-repos), dataset CRUD (use hf-datasets),
  or compute jobs (use hf-jobs).
  Korean triggers: "HF 버킷", "오브젝트 스토리지", "버킷 동기화", "체크포인트 저장".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "ml"
---
# Hugging Face Buckets

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.
> Buckets use the `hf://buckets/` URI scheme for remote paths.

## Quick Commands

### Create Bucket

```bash
hf buckets create my-checkpoints
hf buckets create my-org/training-logs --private --exist-ok
```

> **Write command** — confirm with the user before creating.

| Flag | Required | Description |
|------|----------|-------------|
| `BUCKET_ID` | Yes | Bucket name (e.g., `user/bucket-name`) |
| `--private` | No | Create as private bucket |
| `--exist-ok` | No | Don't error if bucket already exists |

### List Buckets / Files

```bash
hf buckets list                          # list all your buckets
hf buckets list NAMESPACE                # list buckets in namespace
hf buckets list BUCKET_ID                # list files in bucket
hf buckets list BUCKET_ID -R --tree -h   # recursive tree with human sizes
```

| Flag | Required | Description |
|------|----------|-------------|
| `-R, --recursive` | No | List recursively |
| `--tree` | No | Tree-style display |
| `-h, --human-readable` | No | Human-readable file sizes |

### Copy Files

```bash
# Upload
hf buckets cp ./model.safetensors hf://buckets/user/my-bucket/models/

# Download
hf buckets cp hf://buckets/user/my-bucket/models/model.safetensors ./local/
```

> **Write command** (for uploads) — confirm with the user.

### Sync Directories

```bash
# Upload sync (local → remote)
hf buckets sync ./training_logs hf://buckets/user/my-bucket/logs/

# Download sync (remote → local)
hf buckets sync hf://buckets/user/my-bucket/logs/ ./local_logs/

# Sync with filters
hf buckets sync ./output hf://buckets/user/my-bucket/output/ \
  --include "*.json" --exclude "*.tmp" --delete
```

The top-level alias also works: `hf sync ./dir hf://buckets/user/bucket/`

| Flag | Required | Description |
|------|----------|-------------|
| `SOURCE` | Yes | Source path (local or `hf://buckets/...`) |
| `DEST` | Yes | Destination path |
| `--include` | No | Glob pattern to include |
| `--exclude` | No | Glob pattern to exclude |
| `--delete` | No | Delete remote files not in source |
| `--every N` | No | Re-sync every N seconds (continuous) |

> **Write command** — `--delete` removes remote files. Confirm with the user.

### Remove Files

```bash
hf buckets rm hf://buckets/user/my-bucket/old-file.bin
hf buckets rm hf://buckets/user/my-bucket/old-dir/ --recursive
```

> **DESTRUCTIVE** — confirm with the user before deleting.

### Get Bucket Info

```bash
hf buckets info BUCKET_ID
```

### Move / Rename Bucket

```bash
hf buckets move user/old-name user/new-name
```

> **Write command** — changes the bucket URI permanently.

### Delete Bucket

```bash
hf buckets delete BUCKET_ID
```

> **DESTRUCTIVE** — removes the entire bucket. Always confirm.

## Common Patterns

```bash
# Create a bucket and sync training checkpoints
hf buckets create my-org/experiment-2026-03 --private --exist-ok
hf buckets sync ./checkpoints/ hf://buckets/my-org/experiment-2026-03/checkpoints/

# Continuous sync during training (every 60 seconds)
hf buckets sync ./logs hf://buckets/user/training/logs --every 60

# Archive evaluation artifacts
hf buckets sync ./eval_results hf://buckets/user/evals/ \
  --include "*.json" --include "*.csv" --exclude "*.tmp"

# List bucket contents with sizes
hf buckets list user/my-bucket -R -h

# Download all JSON files from a bucket
hf buckets sync hf://buckets/user/my-bucket/ ./download/ --include "*.json"

# Clean up old files (mirror local state)
hf buckets sync ./current_data hf://buckets/user/data/ --delete
```

## Examples

### Example 1: Archive training artifacts

**User says:** "Save my training checkpoints to HF storage"

**Actions:**
1. Create bucket: `hf buckets create my-org/training-run-001 --private`
2. Sync: `hf buckets sync ./checkpoints/ hf://buckets/my-org/training-run-001/`
3. Verify: `hf buckets list my-org/training-run-001 -R -h`

### Example 2: Troubleshooting sync

**User says:** "Sync seems stuck or slow"

**Actions:**
1. Check bucket exists: `hf buckets info BUCKET_ID`
2. Try smaller batch: `hf buckets cp ./single_file hf://buckets/...`
3. Check auth: `hf auth whoami`
4. Check disk space and network

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Bucket not found | Verify bucket ID with `hf buckets list` |
| Permission denied | Check token has write access; verify bucket ownership |
| Sync interrupted | Re-run `hf buckets sync` — it handles incremental sync |
| File too large | Buckets handle large files natively; check network stability |
| `--delete` removed needed files | Bucket versioning not available — maintain local backups |
