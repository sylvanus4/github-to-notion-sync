---
name: hf-repos
description: >-
  Manage repository lifecycle on Hugging Face Hub — create, delete, branch,
  tag, configure settings, move, duplicate, and delete files. Use when the
  user asks to create a new HF repo, manage branches or tags, change repo
  settings (gating, visibility), duplicate or move repos, or delete repo
  files. Do NOT use for model search or download (use hf-models), file upload
  (use hf-models with hf upload), discussions/PRs (use hf-discussions), or
  dataset CRUD (use hf-datasets). Korean triggers: "HF 레포 생성", "레포 관리", "브랜치
  관리", "레포 삭제".
disable-model-invocation: true
---

# Hugging Face Repos

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.

## Quick Commands

### Create Repository

```bash
hf repos create ORG/my-model --type model --private
hf repos create my-dataset --type dataset
hf repos create my-space --type space
```

| Flag | Required | Description |
|------|----------|-------------|
| `REPO_ID` | Yes | Repository ID (e.g., `org/name`) |
| `--type` | No | `model` (default), `dataset`, `space` |
| `--private` | No | Create as private repo |

> **Write command** — confirm with the user before executing.

### Delete Repository

```bash
hf repos delete ORG/my-model
hf repos delete ORG/my-dataset --type dataset
```

> **DESTRUCTIVE** — this action is irreversible. Always confirm with the user.

## Raw CLI Commands

### Branch Management

```bash
hf repos branch create REPO_ID BRANCH_NAME
hf repos branch delete REPO_ID BRANCH_NAME
hf repos branch list REPO_ID
```

### Tag Management

```bash
hf repos tag create REPO_ID TAG_NAME --revision COMMIT_HASH
hf repos tag delete REPO_ID TAG_NAME
hf repos tag list REPO_ID
```

### Repository Settings

```bash
hf repos settings REPO_ID --gated auto       # auto-approve access requests
hf repos settings REPO_ID --gated manual      # manual approval
hf repos settings REPO_ID --gated false        # remove gating
hf repos settings REPO_ID --private            # make private
hf repos settings REPO_ID --no-private         # make public
```

> **Write command** — confirm setting changes with the user.

### Move / Rename

```bash
hf repos move FROM_ID TO_ID
```

> **Write command** — this changes the repo URL permanently.

### Duplicate

```bash
hf repos duplicate SOURCE_ID
hf repos duplicate SOURCE_ID --to TARGET_ID --private
```

### Delete Files

```bash
hf repos delete-files REPO_ID "*.bin" --revision main
hf repos delete-files REPO_ID "path/to/file.safetensors"
```

> **DESTRUCTIVE** — confirm file deletion patterns with the user.

## Common Patterns

```bash
# Create a private model repo and upload
hf repos create my-org/my-finetuned-model --type model --private
hf upload my-org/my-finetuned-model ./output/

# Create a feature branch for model updates
hf repos branch create my-org/my-model experiment-v2
hf upload my-org/my-model ./new_weights/ --revision experiment-v2

# Tag a release
hf repos tag create my-org/my-model v1.0.0 --revision main

# Duplicate a model to your namespace
hf repos duplicate meta-llama/Llama-3.2-1B --to my-org/llama-custom --private

# Clean up old binary files after converting to safetensors
hf repos delete-files my-org/my-model "*.bin" --revision main

# List all branches
hf repos branch list my-org/my-model
```

## Examples

### Example 1: Create and configure a model repo

**User says:** "Create a private gated model repo"

**Actions:**
1. Create: `hf repos create my-org/my-model --type model --private`
2. Gate: `hf repos settings my-org/my-model --gated manual`
3. Upload: `hf upload my-org/my-model ./model_files/`
4. Tag: `hf repos tag create my-org/my-model v1.0.0`

### Example 2: Troubleshooting

**User says:** "Can't create a repo — permission denied"

**Actions:**
1. Check auth: `hf auth whoami`
2. Verify org membership and write access
3. Check token scopes at huggingface.co/settings/tokens
4. Retry with explicit token: `hf repos create REPO_ID --token hf_xxx`

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Permission denied | Verify token has write scope and org membership |
| Repo already exists | Use a different name or `--exist-ok` if supported |
| Branch not found | Check branch name with `hf repos branch list REPO_ID` |
| Delete failed | Confirm repo ID and type are correct |
| Move failed | Ensure target namespace exists and you have write access |
