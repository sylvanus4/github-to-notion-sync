# HF Jobs CLI Guide (hf-model-trainer)

When the `hf_jobs()` MCP tool is unavailable, use the `hf jobs` CLI directly.

## Critical Syntax Rules

```bash
# ✅ CORRECT - flags BEFORE script URL
hf jobs uv run --flavor a10g-large --timeout 2h --secrets HF_TOKEN "https://example.com/train.py"

# ❌ WRONG - "run uv" instead of "uv run"
hf jobs run uv "https://example.com/train.py" --flavor a10g-large

# ❌ WRONG - flags AFTER script URL (will be ignored!)
hf jobs uv run "https://example.com/train.py" --flavor a10g-large

# ❌ WRONG - "--secret" instead of "--secrets" (plural)
hf jobs uv run --secret HF_TOKEN "https://example.com/train.py"
```

## Key Rules

1. Command order: `hf jobs uv run` (NOT `hf jobs run uv`)
2. All flags (`--flavor`, `--timeout`, `--secrets`) must come BEFORE the script URL
3. Use `--secrets` (plural), not `--secret`
4. Script URL must be the last positional argument

## Complete CLI Example

```bash
hf jobs uv run \
  --flavor a10g-large \
  --timeout 2h \
  --secrets HF_TOKEN \
  "https://huggingface.co/user/repo/resolve/main/train.py"
```

## Job Status Commands

```bash
hf jobs ps                        # List all jobs
hf jobs logs <job-id>             # View logs
hf jobs inspect <job-id>          # Job details
hf jobs cancel <job-id>           # Cancel a job
```
