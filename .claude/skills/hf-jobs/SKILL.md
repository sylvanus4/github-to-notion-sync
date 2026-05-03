---
name: hf-jobs
description: >-
  Run compute workloads on HuggingFace Jobs infrastructure — UV scripts,
  Docker jobs, batch inference, data processing, and scheduled tasks. Use when
  running GPU workloads for financial model inference, batch processing stock
  data, or scheduling recurring compute jobs on HF infra. Do NOT use for TRL
  model training (use hf-model-trainer). Do NOT use for local script
  execution. Do NOT use for stock analysis (use daily-stock-check). Korean
  triggers: "HF Jobs", "GPU 작업".
---

# Running Workloads on Hugging Face Jobs

## Overview

Run any workload on fully managed Hugging Face infrastructure. No local setup required—jobs run on cloud CPUs, GPUs, or TPUs and can persist results to the Hugging Face Hub.

**Common use cases:**
- **Data Processing** - Transform, filter, or analyze large datasets
- **Batch Inference** - Run inference on thousands of samples
- **Experiments & Benchmarks** - Reproducible ML experiments
- **Model Training** - Fine-tune models (see `model-trainer` skill for TRL-specific training)
- **Synthetic Data Generation** - Generate datasets using LLMs
- **Development & Testing** - Test code without local GPU setup
- **Scheduled Jobs** - Automate recurring tasks

**For model training specifically:** See the `model-trainer` skill for TRL-based training workflows.

## When to Use This Skill

Use this skill when users want to:
- Run Python workloads on cloud infrastructure
- Execute jobs without local GPU/TPU setup
- Process data at scale
- Run batch inference or experiments
- Schedule recurring tasks
- Use GPUs/TPUs for any workload
- Persist results to the Hugging Face Hub

## Key Directives

When assisting with jobs:

1. **ALWAYS use `hf_jobs()` MCP tool** - Submit jobs using `hf_jobs("uv", {...})` or `hf_jobs("run", {...})`. The `script` parameter accepts Python code directly. Do NOT save to local files unless the user explicitly requests it. Pass the script content as a string to `hf_jobs()`.

2. **Always handle authentication** - Jobs that interact with the Hub require `HF_TOKEN` via secrets. See Token Usage section below.

3. **Provide job details after submission** - After submitting, provide job ID, monitoring URL, estimated time, and note that the user can request status checks later.

4. **Set appropriate timeouts** - Default 30min may be insufficient for long-running tasks.

## Prerequisites Checklist

Before starting any job, verify:

### ✅ **Account & Authentication**
- Hugging Face Account with [Pro](https://hf.co/pro), [Team](https://hf.co/enterprise), or [Enterprise](https://hf.co/enterprise) plan (Jobs require paid plan)
- Authenticated login: Check with `hf_whoami()`
- **HF_TOKEN for Hub Access** ⚠️ CRITICAL - Required for any Hub operations (push models/datasets, download private repos, etc.)
- Token must have appropriate permissions (read for downloads, write for uploads)

### ✅ **Token Usage** (See Token Usage section for details)

**When tokens are required:**
- Pushing models/datasets to Hub
- Accessing private repositories
- Using Hub APIs in scripts
- Any authenticated Hub operations

**How to provide tokens:**
```python
{
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # Recommended: automatic token
}
```

**⚠️ CRITICAL:** The `$HF_TOKEN` placeholder is automatically replaced with your logged-in token. Never hardcode tokens in scripts.

## Token Usage Guide

**Essential:** Use `secrets={"HF_TOKEN": "$HF_TOKEN"}` for any job that interacts with the Hub. The `$HF_TOKEN` placeholder is automatically replaced with your logged-in token.

**When required:** Push models/datasets, private repos, Hub APIs.
**When not required:** Public downloads only, jobs with no Hub interaction.

For details (token types, verification, common issues, security), see [references/token_usage.md](references/token_usage.md).

## Quick Start: Two Approaches

### Approach 1: UV Scripts (Recommended)

UV scripts use PEP 723 inline dependencies for clean, self-contained workloads.

**MCP Tool:**
```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers", "torch"]
# ///

from transformers import pipeline
import torch

# Your workload here
classifier = pipeline("sentiment-analysis")
result = classifier("I love Hugging Face!")
print(result)
""",
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI Equivalent:**
```bash
hf jobs uv run my_script.py --flavor cpu-basic --timeout 30m
```

**Python API:**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", flavor="cpu-basic", timeout="30m")
```

**Benefits:** Direct MCP tool usage, clean code, dependencies declared inline, no file saving required

**When to use:** Default choice for all workloads, custom logic, any scenario requiring `hf_jobs()`

#### Custom Docker Images for UV Scripts

By default, UV scripts use `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. For ML workloads with complex dependencies, use pre-built images:

```python
hf_jobs("uv", {
    "script": "inference.py",
    "image": "vllm/vllm-openai:latest",  # Pre-built image with vLLM
    "flavor": "a10g-large"
})
```

**CLI:**
```bash
hf jobs uv run --image vllm/vllm-openai:latest --flavor a10g-large inference.py
```

**Benefits:** Faster startup, pre-installed dependencies, optimized for specific frameworks

#### Python Version

By default, UV scripts use Python 3.12. Specify a different version:

```python
hf_jobs("uv", {
    "script": "my_script.py",
    "python": "3.11",  # Use Python 3.11
    "flavor": "cpu-basic"
})
```

**Python API:**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", python="3.11")
```

#### Working with Scripts

⚠️ **Important:** There are *two* "script path" stories depending on how you run Jobs:

- **Using the `hf_jobs()` MCP tool (recommended in this repo)**: the `script` value must be **inline code** (a string) or a **URL**. A local filesystem path (like `"./scripts/foo.py"`) won't exist inside the remote container.
- **Using the `hf jobs uv run` CLI**: local file paths **do work** (the CLI uploads your script).

**Common mistake with `hf_jobs()` MCP tool:**

```python
# ❌ Will fail (remote container can't see your local path)
hf_jobs("uv", {"script": "./scripts/foo.py"})
```

**Correct patterns with `hf_jobs()` MCP tool:**

```python
# ✅ Inline: read the local script file and pass its *contents*
from pathlib import Path
script = Path("hf-jobs/scripts/foo.py").read_text()
hf_jobs("uv", {"script": script})

# ✅ URL: host the script somewhere reachable
hf_jobs("uv", {"script": "https://huggingface.co/datasets/uv-scripts/.../raw/main/foo.py"})

# ✅ URL from GitHub
hf_jobs("uv", {"script": "https://raw.githubusercontent.com/huggingface/trl/main/trl/scripts/sft.py"})
```

**CLI equivalent (local paths supported):**

```bash
hf jobs uv run ./scripts/foo.py -- --your --args
```

#### Adding Dependencies at Runtime

Add extra dependencies beyond what's in the PEP 723 header:

```python
hf_jobs("uv", {
    "script": "inference.py",
    "dependencies": ["transformers", "torch>=2.0"],  # Extra deps
    "flavor": "a10g-small"
})
```

**Python API:**
```python
from huggingface_hub import run_uv_job
run_uv_job("inference.py", dependencies=["transformers", "torch>=2.0"])
```

### Approach 2: Docker-Based Jobs

Run jobs with custom Docker images and commands.

**MCP Tool:**
```python
hf_jobs("run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Hello from HF Jobs!')"],
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI Equivalent:**
```bash
hf jobs run python:3.12 python -c "print('Hello from HF Jobs!')"
```

**Python API:**
```python
from huggingface_hub import run_job
run_job(image="python:3.12", command=["python", "-c", "print('Hello!')"], flavor="cpu-basic")
```

**Benefits:** Full Docker control, use pre-built images, run any command
**When to use:** Need specific Docker images, non-Python workloads, complex environments

**Example with GPU:**
```python
hf_jobs("run", {
    "image": "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel",
    "command": ["python", "-c", "import torch; print(torch.cuda.get_device_name())"],
    "flavor": "a10g-small",
    "timeout": "1h"
})
```

**Using Hugging Face Spaces as Images:**

You can use Docker images from HF Spaces:
```python
hf_jobs("run", {
    "image": "hf.co/spaces/lhoestq/duckdb",  # Space as Docker image
    "command": ["duckdb", "-c", "SELECT 'Hello from DuckDB!'"],
    "flavor": "cpu-basic"
})
```

**CLI:**
```bash
hf jobs run hf.co/spaces/lhoestq/duckdb duckdb -c "SELECT 'Hello!'"
```

**UV scripts on Hub:** `dataset_search({"author": "uv-scripts", ...})` — popular collections: OCR, classification, synthetic-data, vLLM, dataset-creation.

## Hardware Selection

> **Reference:** [HF Jobs Hardware Docs](https://huggingface.co/docs/hub/en/spaces-config-reference) (updated 07/2025)

| Workload Type | Recommended Hardware | Use Case |
|---------------|---------------------|----------|
| Data processing, testing | `cpu-basic`, `cpu-upgrade` | Lightweight tasks |
| Small models, demos | `t4-small` | <1B models, quick tests |
| Medium models | `t4-medium`, `l4x1` | 1-7B models |
| Large models, production | `a10g-small`, `a10g-large` | 7-13B models |
| Very large models | `a100-large` | 13B+ models |
| Batch inference | `a10g-large`, `a100-large` | High-throughput |
| Multi-GPU workloads | `l4x4`, `a10g-largex2`, `a10g-largex4` | Parallel/large models |
| TPU workloads | `v5e-1x1`, `v5e-2x2`, `v5e-2x4` | JAX/Flax, TPU-optimized |

**All Available Flavors:**
- **CPU:** `cpu-basic`, `cpu-upgrade`
- **GPU:** `t4-small`, `t4-medium`, `l4x1`, `l4x4`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large`
- **TPU:** `v5e-1x1`, `v5e-2x2`, `v5e-2x4`

**Guidelines:** Start small, scale up based on needs. See [references/hardware_guide.md](references/hardware_guide.md) for detailed specifications.

## Critical: Saving Results

**⚠️ EPHEMERAL ENVIRONMENT—MUST PERSIST RESULTS**

The Jobs environment is temporary. All files are deleted when the job ends. If results aren't persisted, **ALL WORK IS LOST**.

**Methods:** Push to Hub (recommended), external storage (S3/GCS), or POST to API. Always use `secrets={"HF_TOKEN": "$HF_TOKEN"}` when using Hub.

For detailed examples, see [references/hub_saving.md](references/hub_saving.md).

### Verification Checklist

Before submitting:
- [ ] Results persistence method chosen
- [ ] `secrets={"HF_TOKEN": "$HF_TOKEN"}` if using Hub
- [ ] Script handles missing token gracefully

## Timeout Management

**⚠️ DEFAULT: 30 MINUTES**

Jobs automatically stop after the timeout. For long-running tasks like training, always set a custom timeout.

### Setting Timeouts

**MCP Tool:**
```python
{
    "timeout": "2h"   # 2 hours
}
```

**Supported formats:**
- Integer/float: seconds (e.g., `300` = 5 minutes)
- String with suffix: `"5m"` (minutes), `"2h"` (hours), `"1d"` (days)
- Examples: `"90m"`, `"2h"`, `"1.5h"`, `300`, `"1d"`

**Python API:**
```python
from huggingface_hub import run_job, run_uv_job

run_job(image="python:3.12", command=[...], timeout="2h")
run_uv_job("script.py", timeout=7200)  # 2 hours in seconds
```

### Timeout Guidelines

| Scenario | Recommended | Notes |
|----------|-------------|-------|
| Quick test | 10-30 min | Verify setup |
| Data processing | 1-2 hours | Depends on data size |
| Batch inference | 2-4 hours | Large batches |
| Experiments | 4-8 hours | Multiple runs |
| Long-running | 8-24 hours | Production workloads |

**Always add 20-30% buffer** for setup, network delays, and cleanup.

**On timeout:** Job killed immediately, all unsaved progress lost

## Cost Estimation

**Formula:** `Total Cost = (Hours of runtime) × (Cost per hour)`. Start small, monitor runtime, use checkpoints. See [references/cost_estimation.md](references/cost_estimation.md) for examples.

## Monitoring and Tracking

**MCP Tool:**
```python
hf_jobs("ps")                                    # List jobs
hf_jobs("inspect", {"job_id": "your-job-id"})   # Inspect
hf_jobs("logs", {"job_id": "your-job-id"})      # View logs
hf_jobs("cancel", {"job_id": "your-job-id"})    # Cancel
```

**CLI:** `hf jobs ps`, `hf jobs logs <job-id>`, `hf jobs cancel <job-id>`

**Job URLs:** `https://huggingface.co/jobs/username/job-id` — view logs, status, details in browser.

**Remember:** Wait for user to request status checks. Avoid polling repeatedly.

## Scheduled Jobs

Run jobs on a schedule using CRON or predefined schedules (`@hourly`, `@daily`, etc.). Use `hf_jobs("scheduled uv", {...})` or `hf_jobs("scheduled run", {...})`. See [references/scheduled_jobs.md](references/scheduled_jobs.md).

## Webhooks

Trigger jobs when Hub repos change. Python API: `create_webhook()`. Job receives `WEBHOOK_PAYLOAD` env var. See [references/webhooks.md](references/webhooks.md).

## Common Workload Patterns

Ready-to-run scripts in `hf-jobs/scripts/`: `generate-responses.py` (vLLM batch), `cot-self-instruct.py` (synthetic data), `finepdfs-stats.py` (Polars streaming). See [references/job_patterns.md](references/job_patterns.md) for usage.

## Common Failure Modes

### Out of Memory (OOM)

**Fix:**
1. Reduce batch size or data chunk size
2. Process data in smaller batches
3. Upgrade hardware: cpu → t4 → a10g → a100

### Job Timeout

**Fix:**
1. Check logs for actual runtime
2. Increase timeout with buffer: `"timeout": "3h"`
3. Optimize code for faster execution
4. Process data in chunks

### Hub Push Failures

**Fix:**
1. Add to job: `secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. Verify token in script: `assert "HF_TOKEN" in os.environ`
3. Check token permissions
4. Verify repo exists or can be created

### Missing Dependencies

**Fix:**
Add to PEP 723 header:
```python
# /// script
# dependencies = ["package1", "package2>=1.0.0"]
# ///
```

### Authentication Errors

**Fix:**
1. Check `hf_whoami()` works locally
2. Verify `secrets={"HF_TOKEN": "$HF_TOKEN"}` in job config
3. Re-login: `hf auth login`
4. Check token has required permissions

## Troubleshooting

**Common issues:**
- Job times out → Increase timeout, optimize code
- Results not saved → Check persistence method, verify HF_TOKEN
- Out of Memory → Reduce batch size, upgrade hardware
- Import errors → Add dependencies to PEP 723 header
- Authentication errors → Check token, verify secrets parameter

**See:** [references/troubleshooting.md](references/troubleshooting.md)

## Resources

### References (In This Skill)
- [references/token_usage.md](references/token_usage.md) - Token guide
- [references/hardware_guide.md](references/hardware_guide.md) - Hardware specs
- [references/hub_saving.md](references/hub_saving.md) - Hub persistence
- [references/job_patterns.md](references/job_patterns.md) - Workload patterns
- [references/scheduled_jobs.md](references/scheduled_jobs.md) - Scheduled jobs
- [references/webhooks.md](references/webhooks.md) - Webhooks
- [references/cost_estimation.md](references/cost_estimation.md) - Cost examples
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues

**Scripts:** `scripts/generate-responses.py`, `scripts/cot-self-instruct.py`, `scripts/finepdfs-stats.py`

### External Links

**Official Documentation:**
- [HF Jobs Guide](https://huggingface.co/docs/huggingface_hub/guides/jobs) - Main documentation
- [HF Jobs CLI Reference](https://huggingface.co/docs/huggingface_hub/guides/cli#hf-jobs) - Command line interface
- [HF Jobs API Reference](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api) - Python API details
- [Hardware Flavors Reference](https://huggingface.co/docs/hub/en/spaces-config-reference) - Available hardware

**Related Tools:**
- [UV Scripts Guide](https://docs.astral.sh/uv/guides/scripts/) - PEP 723 inline dependencies
- [UV Scripts Organization](https://huggingface.co/uv-scripts) - Community UV script collection
- [HF Hub Authentication](https://huggingface.co/docs/huggingface_hub/quick-start#authentication) - Token setup
- [Webhooks Documentation](https://huggingface.co/docs/huggingface_hub/guides/webhooks) - Event triggers

## Key Takeaways

1. **Submit scripts inline** - The `script` parameter accepts Python code directly; no file saving required unless user requests
2. **Jobs are asynchronous** - Don't wait/poll; let user check when ready
3. **Always set timeout** - Default 30 min may be insufficient; set appropriate timeout
4. **Always persist results** - Environment is ephemeral; without persistence, all work is lost
5. **Use tokens securely** - Always use `secrets={"HF_TOKEN": "$HF_TOKEN"}` for Hub operations
6. **Choose appropriate hardware** - Start small, scale up based on needs (see hardware guide)
7. **Use UV scripts** - Default to `hf_jobs("uv", {...})` with inline scripts for Python workloads
8. **Handle authentication** - Verify tokens are available before Hub operations
9. **Monitor jobs** - Provide job URLs and status check commands
10. **Optimize costs** - Choose right hardware, set appropriate timeouts

## Quick Reference: MCP Tool vs CLI vs Python API

| Operation | MCP Tool | CLI | Python API |
|-----------|----------|-----|------------|
| Run UV script | `hf_jobs("uv", {...})` | `hf jobs uv run script.py` | `run_uv_job("script.py")` |
| Run Docker job | `hf_jobs("run", {...})` | `hf jobs run image cmd` | `run_job(image, command)` |
| List jobs | `hf_jobs("ps")` | `hf jobs ps` | `list_jobs()` |
| View logs | `hf_jobs("logs", {...})` | `hf jobs logs <id>` | `fetch_job_logs(job_id)` |
| Cancel job | `hf_jobs("cancel", {...})` | `hf jobs cancel <id>` | `cancel_job(job_id)` |
| Schedule UV | `hf_jobs("scheduled uv", {...})` | - | `create_scheduled_uv_job()` |
| Schedule Docker | `hf_jobs("scheduled run", {...})` | - | `create_scheduled_job()` |
