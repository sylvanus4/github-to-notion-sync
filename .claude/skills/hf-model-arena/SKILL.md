---
name: hf-model-arena
description: >-
  Competitive model evaluation arena that discovers competing models for a
  given task, runs head-to-head evaluations on a standardized dataset,
  generates a multi-dimensional leaderboard, deploys the winner as an
  inference endpoint, and archives all artifacts. Use when the user asks to
  "compare models", "model arena", "model shootout", "find best model for
  task", "head-to-head evaluation", "leaderboard", "모델 비교", "모델 아레나", "모델 대결",
  "최적 모델 선정", "리더보드 생성", or wants a systematic comparison of competing models
  with deployment of the winner. Do NOT use for training models (use
  hf-model-trainer). Do NOT use for daily stock analysis (use today). Do NOT
  use for single model evaluation only (use hf-evaluation). Do NOT use for
  model search without evaluation (use hf-models).
disable-model-invocation: true
---

# Model Arena — Competitive Model Evaluation

End-to-end pipeline: discover competing models → evaluate head-to-head →
generate leaderboard → deploy winner → archive artifacts.

## Prerequisites

- `hf` CLI installed and authenticated (see `hf-hub` skill)
- HF Pro/Team plan for Jobs infrastructure (evaluation) and Inference Endpoints (deployment)
- `jq` for JSON processing

## Required Skills

- `hf-models` — candidate discovery and metadata collection
- `hf-evaluation` — benchmark execution
- `hf-endpoints` — winner deployment
- `hf-buckets` — artifact archival
- `hf-collections` — curated winner collection
- `hf-jobs` — compute infrastructure for evaluation
- `hf-dataset-viewer` — evaluation dataset validation
- `anthropic-docx` — evaluation report generation
- `visual-explainer` — interactive leaderboard HTML

## Reference Files

- `references/evaluation-dimensions.md` — scoring dimensions and benchmark selection
- `references/leaderboard-template.md` — leaderboard report structure
- `references/deployment-guide.md` — hardware selection for winner deployment

## Input

The user provides:
- **Task**: Target task (e.g., "text classification", "code generation")
- **Parameter range** (optional): Model size constraints (e.g., "7B-14B")
- **Candidate count** (optional): Number of models to evaluate (default: 5)
- **Evaluation dataset** (optional): Specific dataset to use; auto-selected if not provided
- **Deploy winner** (optional): Whether to deploy the top model as an endpoint

## Pipeline Phases

### Phase 1 — Candidate Discovery

Find the top N models for the specified task.

```bash
# Search by task with parameter filter
hf models ls --filter TASK_TAG \
  --num-parameters "min:MIN,max:MAX" \
  --sort downloads --limit 20 --format json

# Also check by trending score for newer models
hf models ls --filter TASK_TAG \
  --num-parameters "min:MIN,max:MAX" \
  --sort trending_score --limit 10 --format json
```

**Processing:**
1. Merge results from downloads and trending sorts (deduplicate)
2. Filter by license compatibility
3. Prefer models with safetensors format
4. Select top N candidates

**Output:** List of N candidate model IDs

### Phase 2 — Metadata Collection

Gather detailed information about each candidate.

```bash
# For each candidate
hf models info MODEL_ID --format json --expand downloads,likes,tags,safetensors
```

**Extracted metadata per model:**
- Architecture and parameter count
- License type
- Training data information
- Existing benchmark scores (from model card)
- Safetensors availability
- Download count and community engagement
- Last modified date

**Output:** Metadata table for all candidates

### Phase 3 — Eval Dataset Selection

Select or validate the evaluation dataset.

If user provided a dataset:
```bash
hf datasets info DATASET_ID --format json
```

If auto-selecting:
```bash
hf datasets ls --search "TASK_EVAL_KEYWORD" --sort downloads --limit 10 --format json
```

For the selected dataset, validate quality:
```bash
# Get parquet URLs
hf datasets parquet DATASET_ID --format json

# Check size and distribution
hf datasets sql "SELECT COUNT(*) as rows FROM read_parquet('PARQUET_URL')"

# Check label distribution for classification
hf datasets sql "SELECT label, COUNT(*) as n
FROM read_parquet('PARQUET_URL')
GROUP BY label ORDER BY n DESC"

# Verify no data quality issues
hf datasets sql "SELECT
  COUNT(*) as total,
  SUM(CASE WHEN text IS NULL OR text = '' THEN 1 ELSE 0 END) as empty_text
FROM read_parquet('PARQUET_URL')"
```

**Output:** Selected and validated evaluation dataset with quality report

### Phase 4 — Evaluation

Run standardized benchmarks for all candidates on HF Jobs infrastructure.

```bash
# Invoke hf-evaluation skill for each candidate
# Run in parallel batches (max 4 concurrent)
```

**Evaluation dimensions** (see `references/evaluation-dimensions.md`):

1. **Accuracy / Quality**: Task-specific metric (accuracy, F1, BLEU, ROUGE, etc.)
2. **Latency**: Inference time per sample (p50, p95)
3. **Memory**: Peak GPU memory usage during inference
4. **Throughput**: Tokens/samples per second
5. **Cost Efficiency**: Quality per dollar of inference

**Processing:**
1. Split candidates into batches of 4
2. For each batch, launch parallel evaluation jobs via `hf-jobs`
3. Collect results as each job completes
4. Normalize scores across dimensions

**Output:** Raw evaluation results for all candidates across all dimensions

### Phase 5 — Leaderboard

Generate the multi-dimensional comparison leaderboard.

**Composite scoring:**
```
overall_score = (
  0.40 * accuracy_normalized +
  0.20 * latency_normalized +
  0.15 * memory_normalized +
  0.15 * throughput_normalized +
  0.10 * cost_efficiency_normalized
)
```

**Outputs:**
1. **Comparison table** (markdown): All models ranked by overall score
2. **Interactive HTML leaderboard**: Use `visual-explainer` to create radar charts and bar comparisons
3. **Winner announcement**: Model with highest overall score

Save leaderboard HTML to: `output/hf-arena/YYYY-MM-DD-TASK-leaderboard.html`

### Phase 6 — Winner Deployment (Optional)

If the user requested deployment, deploy the top-ranked model.

```bash
# Select optimal hardware based on model size (see references/deployment-guide.md)
hf endpoints deploy arena-winner-TASK \
  --repo WINNER_MODEL_ID \
  --accelerator gpu \
  --instance-type OPTIMAL_HARDWARE \
  --region us-east-1 \
  --vendor aws
```

Wait for endpoint to be ready:
```bash
hf endpoints describe arena-winner-TASK --format json
```

**Output:** Deployed endpoint URL and status

### Phase 7 — Artifact Archive

Archive all evaluation artifacts to HF Buckets.

```bash
# Create archive bucket
hf buckets create arena-archive-$(date +%Y%m%d) --private --exist-ok

# Sync evaluation results
hf buckets sync ./eval_results/ hf://buckets/user/arena-archive-$(date +%Y%m%d)/

# Include: raw predictions, metrics, configs, logs
```

**Archived artifacts:**
- Evaluation configs and scripts
- Raw predictions per model
- Metric scores (JSON)
- Leaderboard HTML
- Evaluation report

**Output:** Bucket URL with archived artifacts

### Phase 8 — Collection & Report

Update the curated collection and generate the final report.

```bash
# Add winner to a "Best Models" collection
hf collections add-item COLLECTION_SLUG WINNER_MODEL_ID model \
  --note "Arena winner for TASK — Score: X.XX — $(date +%Y-%m-%d)"
```

Generate evaluation report via `anthropic-docx`:
- Cover page with task, date, evaluator
- Methodology section (dimensions, weights, dataset)
- Per-model detailed results
- Comparison charts
- Winner recommendation with rationale
- Deployment details (if deployed)

Save report to: `output/hf-arena/YYYY-MM-DD-TASK-report.docx`

**Output:** Collection updated + evaluation report (.docx)

## Output Summary

The pipeline produces:
- **Leaderboard HTML** — interactive comparison at `output/hf-arena/`
- **Evaluation Report** (.docx) — detailed methodology and results
- **Deployed Endpoint** (optional) — live API for the winning model
- **Archived Artifacts** — raw evaluation data in HF Buckets
- **Updated Collection** — winning model added to curated collection

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | No models found for task | Broaden search; relax parameter constraints |
| 1 | Too few candidates | Lower minimum to 3; include trending models |
| 3 | No eval dataset found | Suggest user-provided dataset; try generic benchmarks |
| 3 | Dataset quality issues | Filter bad rows via SQL; report quality concerns |
| 4 | Evaluation job fails | Retry once; skip failed model; continue with remaining |
| 4 | GPU quota exceeded | Queue jobs sequentially instead of parallel |
| 5 | Tie in scores | Use tiebreaker: downloads > likes > recency |
| 6 | Deployment fails | Report endpoint error; save config for manual deployment |
| 7 | Bucket sync fails | Save artifacts locally; retry in next run |
| 8 | Docx generation fails | Save raw markdown report as fallback |
