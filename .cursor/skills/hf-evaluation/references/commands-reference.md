# HF Evaluation Commands Reference

## Top-level Help

```bash
uv run scripts/evaluation_manager.py --help
uv run scripts/evaluation_manager.py --version
```

## Inspect Tables (start here)

```bash
uv run scripts/evaluation_manager.py inspect-tables --repo-id "username/model-name"
```

## Extract from README

```bash
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model-name" \
  --table N \
  [--model-column-index N] \
  [--model-name-override "Exact Column Header or Model Name"] \
  [--task-type "text-generation"] \
  [--dataset-name "Custom Benchmarks"] \
  [--apply | --create-pr]
```

## Import from Artificial Analysis

```bash
AA_API_KEY=... uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "creator-name" \
  --model-name "model-slug" \
  --repo-id "username/model-name" \
  [--create-pr]
```

## View / Validate

```bash
uv run scripts/evaluation_manager.py show --repo-id "username/model-name"
uv run scripts/evaluation_manager.py validate --repo-id "username/model-name"
```

## Check Open PRs (ALWAYS run before --create-pr)

```bash
uv run scripts/evaluation_manager.py get-prs --repo-id "username/model-name"
```

Lists all open pull requests for the model repository.

## Run Evaluation Job (Inference Providers)

```bash
hf jobs uv run scripts/inspect_eval_uv.py \
  --flavor "cpu-basic|t4-small|..." \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --task "task-name"
```

Or use the Python helper:

```bash
uv run scripts/run_eval_job.py \
  --model "model-id" \
  --task "task-name" \
  --hardware "cpu-basic|t4-small|..."
```

## Run vLLM Evaluation (Custom Models)

```bash
# lighteval with vLLM
hf jobs uv run scripts/lighteval_vllm_uv.py \
  --flavor "a10g-small" \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --tasks "leaderboard|mmlu|5"

# inspect-ai with vLLM
hf jobs uv run scripts/inspect_vllm_uv.py \
  --flavor "a10g-small" \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --task "mmlu"

# Helper script (auto hardware selection)
uv run scripts/run_vllm_eval_job.py \
  --model "model-id" \
  --task "leaderboard|mmlu|5" \
  --framework lighteval
```
