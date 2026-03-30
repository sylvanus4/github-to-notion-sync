---
name: hf-endpoints
description: >-
  Deploy, manage, and monitor Hugging Face Inference Endpoints via the hf CLI.
  Use when the user asks to deploy a model as an API endpoint, list endpoints,
  browse the endpoint catalog, pause or resume an endpoint, scale to zero, or
  delete an endpoint. Do NOT use for cloud compute jobs (use hf-jobs), model
  download (use hf-models), Spaces (use hf-spaces), or model training
  (use hf-model-trainer).
  Korean triggers: "추론 엔드포인트", "모델 배포", "엔드포인트 관리", "HF 엔드포인트".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "ml"
---
# Hugging Face Inference Endpoints

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.
> Inference Endpoints require a Pro, Team, or Enterprise plan.

## Quick Commands

### List Endpoints

```bash
hf endpoints ls
hf endpoints ls --namespace my-org --format json
```

### Describe Endpoint

```bash
hf endpoints describe my-endpoint
hf endpoints describe my-endpoint --format json
```

### Deploy from Repository

```bash
hf endpoints deploy my-endpoint \
  --repo meta-llama/Llama-3.2-1B-Instruct \
  --framework pytorch \
  --accelerator gpu \
  --instance-size x1 \
  --instance-type nvidia-a10g \
  --region us-east-1 \
  --vendor aws
```

> **Write command** — deploying creates a billable resource. Confirm with the user.

| Flag | Required | Description |
|------|----------|-------------|
| `NAME` | Yes | Endpoint name |
| `--repo` | Yes | Model repository ID |
| `--framework` | Yes | `pytorch`, `tensorflow`, etc. |
| `--accelerator` | Yes | `cpu`, `gpu` |
| `--instance-size` | Yes | Size tier (e.g., `x1`, `x2`, `x4`) |
| `--instance-type` | Yes | Hardware type (e.g., `nvidia-a10g`, `nvidia-a100`) |
| `--region` | Yes | Cloud region |
| `--vendor` | Yes | Cloud provider (`aws`, `gcp`, `azure`) |
| `--min-replica` | No | Minimum replicas (default: 1) |
| `--max-replica` | No | Maximum replicas for autoscaling |
| `--namespace` | No | Organization namespace |

### Deploy from Catalog

```bash
hf endpoints catalog list --task text-generation --format json
hf endpoints catalog deploy --repo meta-llama/Llama-3.2-1B-Instruct
```

The catalog provides pre-configured deployment options for popular models.

### Manage Endpoint State

```bash
hf endpoints pause my-endpoint          # stop billing, preserve config
hf endpoints resume my-endpoint         # restart a paused endpoint
hf endpoints scale-to-zero my-endpoint  # scale down, auto-wake on request
hf endpoints delete my-endpoint         # permanently remove
```

> **Write commands** — `pause`, `resume`, `scale-to-zero` affect billing. `delete` is irreversible.

### Update Endpoint

```bash
hf endpoints update my-endpoint --min-replica 2 --max-replica 4
```

## Common Patterns

```bash
# Quick deploy from catalog (simplest path)
hf endpoints catalog deploy --repo meta-llama/Llama-3.2-1B-Instruct

# List all endpoints with status
hf endpoints ls --format json | jq '.[] | {name, status, model}'

# Deploy, test, then scale to zero for cost savings
hf endpoints deploy my-llm --repo MODEL_ID --accelerator gpu --instance-type nvidia-a10g ...
# ... test the endpoint ...
hf endpoints scale-to-zero my-llm

# Browse catalog for available models
hf endpoints catalog list --task text-generation --format json

# Check endpoint status
hf endpoints describe my-endpoint --format json | jq '.status'

# Clean up unused endpoints
hf endpoints ls -q | while read name; do
  echo "Checking $name..."
  hf endpoints describe "$name" --format json | jq '{name: .name, status: .status.state}'
done
```

## Examples

### Example 1: Deploy a model

**User says:** "Deploy Llama 3.2 as an inference endpoint"

**Actions:**
1. Check catalog: `hf endpoints catalog list --task text-generation --format json`
2. Deploy: `hf endpoints catalog deploy --repo meta-llama/Llama-3.2-1B-Instruct`
3. Monitor: `hf endpoints describe my-endpoint`
4. When ready, report the endpoint URL

### Example 2: Cost optimization

**User says:** "My endpoint is too expensive when idle"

**Actions:**
1. Scale to zero: `hf endpoints scale-to-zero my-endpoint`
2. Explain: endpoint auto-wakes on first request (cold start ~30-60s)
3. Alternative: `hf endpoints pause my-endpoint` (no cold start billing)

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Permission denied | Requires Pro/Team/Enterprise plan and write scope token |
| Model not compatible | Check supported frameworks at HF Inference Endpoints docs |
| Deployment failed | Check `hf endpoints describe NAME` for error details |
| Quota exceeded | Check account limits or contact HF support |
| Endpoint not responding | Wait for status `running`, check logs via HF dashboard |
