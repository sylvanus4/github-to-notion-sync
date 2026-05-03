---
name: hf-models
description: >-
  Search, discover, inspect, download, and upload models on Hugging Face Hub
  via the hf CLI. Use when the user asks to find models, search by task or
  author, check model info, download model weights, upload a trained model, or
  discover trending models. Do NOT use for model training (use
  hf-model-trainer), model evaluation (use hf-evaluation), dataset operations
  (use hf-datasets), or repo lifecycle management (use hf-repos). Korean
  triggers: "모델 검색", "모델 다운로드", "모델 업로드", "HF 모델".
---

# Hugging Face Models

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.

## Quick Commands

### Search Models

```bash
hf models ls --search "sentiment" --sort trending_score --limit 10
```

| Flag | Required | Description |
|------|----------|-------------|
| `--search TEXT` | No | Search query |
| `--author TEXT` | No | Filter by author/org (e.g., `meta-llama`) |
| `--filter TEXT` | No | Tag filter, repeatable (e.g., `text-classification`) |
| `--num-parameters TEXT` | No | Parameter range (e.g., `min:7B,max:70B`) |
| `--sort` | No | `created_at`, `downloads`, `last_modified`, `likes`, `trending_score` |
| `--limit INTEGER` | No | Number of results (default: 10) |
| `--format [table\|json]` | No | Output format |
| `-q, --quiet` | No | Print model IDs only |
| `--expand TEXT` | No | Extra metadata (e.g., `downloads,likes,tags`) |

### Get Model Info

```bash
hf models info MODEL_ID
hf models info MODEL_ID --format json --expand downloads,likes,tags,safetensors
```

### Download Model

```bash
hf download MODEL_ID
hf download MODEL_ID --include "*.safetensors" --local-dir ./models/
hf download MODEL_ID --include "config.json" "tokenizer*"
```

| Flag | Required | Description |
|------|----------|-------------|
| `MODEL_ID` | Yes | Repository ID (e.g., `meta-llama/Llama-3.2-1B`) |
| `--include` | No | Glob patterns to include |
| `--exclude` | No | Glob patterns to exclude |
| `--local-dir` | No | Target directory |
| `--revision` | No | Branch/tag/commit to download |
| `--repo-type` | No | `model` (default), `dataset`, `space` |

### Upload Model

```bash
hf upload MODEL_ID ./local_path
hf upload MODEL_ID ./model.safetensors --repo-type model
```

> **Write command** — confirm with the user before executing.

| Flag | Required | Description |
|------|----------|-------------|
| `MODEL_ID` | Yes | Target repo ID |
| `LOCAL_PATH` | Yes | File or folder to upload |
| `--repo-type` | No | `model` (default) |
| `--revision` | No | Target branch |

For large uploads (>5GB or many files), use `hf upload-large-folder`:

```bash
hf upload-large-folder MODEL_ID ./local_folder --repo-type model
```

## Common Patterns

```bash
# Find trending LLMs with 7B-70B parameters
hf models ls --search "llama" --author meta-llama \
  --num-parameters "min:7B,max:70B" --sort trending_score --format json

# Find text-classification models sorted by downloads
hf models ls --filter text-classification --sort downloads --limit 20

# Get top model ID for piping
TOP_MODEL=$(hf models ls --search "sentiment" --sort downloads -q | head -1)
hf download "$TOP_MODEL" --local-dir ./models/

# Check model size and format before downloading
hf models info meta-llama/Llama-3.2-1B --format json | jq '.safetensors'

# Download only config files (lightweight inspection)
hf download MODEL_ID --include "config.json" "tokenizer*" --local-dir /tmp/inspect/

# Search by multiple tags
hf models ls --filter text-generation --filter pytorch --sort likes

# List models by a specific organization
hf models ls --author nvidia --sort trending_score --limit 10
```

## Examples

### Example 1: Find and download a model

**User says:** "Find the most popular Korean NLP model and download it"

**Actions:**
1. Search: `hf models ls --search "korean" --filter text-generation --sort downloads --limit 5`
2. Inspect top result: `hf models info MODEL_ID --format json`
3. Download: `hf download MODEL_ID --local-dir ./models/korean-nlp/`

### Example 2: Troubleshooting download

**User says:** "Download is very slow or failing"

**Actions:**
1. Check network: `hf env` (verify endpoint URL)
2. Try specific files: `hf download MODEL_ID --include "*.safetensors"`
3. For large models, use resumable upload: `hf upload-large-folder`
4. Check disk space: `df -h`

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Authentication error | Run `hf auth login` or set `HF_TOKEN` env var |
| Model not found | Verify repo ID — check if private and token has access |
| Gated model (403) | Accept license at model page, then retry with valid token |
| Download incomplete | Re-run `hf download` — it resumes automatically |
| Disk space full | Use `--include` to download specific files, or `hf cache prune` |
