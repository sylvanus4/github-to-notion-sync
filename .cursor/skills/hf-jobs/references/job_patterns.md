# Common Workload Patterns

This repository ships ready-to-run UV scripts in `hf-jobs/scripts/`. Prefer using them instead of inventing new templates.

## Pattern 1: Dataset → Model Responses (vLLM)

**Script:** `scripts/generate-responses.py`

**What it does:** Loads a Hub dataset (chat `messages` or a `prompt` column), applies a model chat template, generates responses with vLLM, and **pushes** the output dataset + dataset card back to the Hub.

**Requires:** GPU + **write** token (it pushes a dataset).

```python
from pathlib import Path

script = Path("hf-jobs/scripts/generate-responses.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "username/input-dataset",
        "username/output-dataset",
        "--messages-column", "messages",
        "--model-id", "Qwen/Qwen3-30B-A3B-Instruct-2507",
        "--temperature", "0.7",
        "--top-p", "0.8",
        "--max-tokens", "2048",
    ],
    "flavor": "a10g-large",
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

## Pattern 2: CoT Self-Instruct Synthetic Data

**Script:** `scripts/cot-self-instruct.py`

**What it does:** Generates synthetic prompts/answers via CoT Self-Instruct, optionally filters outputs (answer-consistency / RIP), then **pushes** the generated dataset + dataset card to the Hub.

**Requires:** GPU + **write** token (it pushes a dataset).

```python
from pathlib import Path

script = Path("hf-jobs/scripts/cot-self-instruct.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "--seed-dataset", "davanstrien/s1k-reasoning",
        "--output-dataset", "username/synthetic-math",
        "--task-type", "reasoning",
        "--num-samples", "5000",
        "--filter-method", "answer-consistency",
    ],
    "flavor": "l4x4",
    "timeout": "8h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

## Pattern 3: Streaming Dataset Stats (Polars + HF Hub)

**Script:** `scripts/finepdfs-stats.py`

**What it does:** Scans parquet directly from Hub (no 300GB download), computes temporal stats, and (optionally) uploads results to a Hub dataset repo.

**Requires:** CPU is often enough; token needed **only** if you pass `--output-repo` (upload).

```python
from pathlib import Path

script = Path("hf-jobs/scripts/finepdfs-stats.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "--limit", "10000",
        "--show-plan",
        "--output-repo", "username/finepdfs-temporal-stats",
    ],
    "flavor": "cpu-upgrade",
    "timeout": "2h",
    "env": {"HF_XET_HIGH_PERFORMANCE": "1"},
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```
