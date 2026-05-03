---
name: hf-auto-finetune-planner
description: >-
  End-to-end autonomous fine-tuning planner that takes a natural language task
  description, discovers the optimal base model + training dataset combination
  on HF Hub, validates dataset quality via SQL, estimates GPU cost, generates
  a training config, and optionally launches the job. Use when the user asks
  to "plan fine-tuning", "find best model for task", "auto fine-tune",
  "training planner", "파인튜닝 계획", "자동 파인튜닝", "모델 + 데이터셋 매칭", "학습 계획",
  "fine-tune planner", or wants to go from a task description to a
  training-ready configuration. Do NOT use for running the existing daily
  pipeline (use today). Do NOT use for direct model training without planning
  (use hf-model-trainer). Do NOT use for dataset exploration only (use
  hf-dataset-viewer). Do NOT use for model search only (use hf-models).
---

# Auto Fine-Tune Planner

End-to-end pipeline that transforms a natural language task description into a
training-ready configuration. Autonomously discovers models, matches datasets,
validates quality, estimates costs, and generates configs.

## Prerequisites

- `hf` CLI installed and authenticated (see `hf-hub` skill)
- HF Pro/Team plan for Jobs cost estimation and execution
- `jq` for JSON processing

## Required Skills

- `hf-models` — model discovery and info
- `hf-datasets` (existing) — dataset CRUD and SQL queries
- `hf-dataset-viewer` — dataset exploration via REST API
- `hf-evaluation` — existing benchmark lookup
- `hf-jobs` — hardware listing and cost estimation
- `hf-model-trainer` — training execution (Phase 6)
- `hf-trackio` — experiment monitoring (Phase 6)
- `hf-collections` — save curated model+dataset pairs

## Agent Response Contract (Binary Eval Gate)

When executing or summarizing this planner for the user, the **user-facing reply** MUST satisfy:

1. **EVAL 1 — Relevance first:** Lead with `## 관련도 선행 평가`: `**점수:** N/10` and `**선행 근거:**` (2–4 Korean sentences) mapping the task to model scout / dataset match / cost / config phases. If the ask is training-only or dataset-only, score < 5 and redirect in Korean.

2. **EVAL 2 — Composed related skills (≥3):** Section `## 위임된 관련 스킬` with **≥3 rows** drawn from **Required Skills** above (`hf-models`, `hf-datasets`, `hf-dataset-viewer`, `hf-evaluation`, `hf-jobs`, `hf-model-trainer`, `hf-trackio`, `hf-collections`, `hf-hub`). Table: 스킬 (backticks), 위임 범위 (Korean), 기대 산출물 (Korean).

3. **EVAL 3 — Korean narrative structure:** Phase outputs and recommendations in **Korean**; use H2/H3, bullets, and **≥1** markdown table (e.g., candidate models, datasets, or cost options).

4. **EVAL 4 — Actionable recommendations:** Close with `## 실행 액션 플랜`: **≥3** numbered items including **담당:** and **기한:** each (Korean).

## Reference Files

Read these as needed during execution:

- `references/task-taxonomy.md` — maps task descriptions to HF model tags and dataset filters
- `references/cost-estimation.md` — hardware FLOPS tables and training time formulas
- `references/config-templates.md` — SFT/DPO/GRPO config templates

## Input

The user provides:
- **Task description**: Natural language (e.g., "Korean financial sentiment analysis")
- **Constraints** (optional): Parameter budget, GPU budget, license requirements, accuracy targets

## Pipeline Phases

### Phase 1 — Model Scout

Discover candidate base models for the given task.

```bash
# Search by task keywords
hf models ls --search "TASK_KEYWORDS" --sort trending_score --limit 20 --format json

# Filter by parameter count if user specified constraints
hf models ls --search "TASK_KEYWORDS" --num-parameters "min:1B,max:14B" \
  --sort downloads --limit 20 --format json

# Filter by specific task tag
hf models ls --filter text-classification --sort trending_score --limit 10 --format json
```

**Processing:**
1. Parse JSON results
2. For each candidate, fetch details: `hf models info MODEL_ID --format json --expand downloads,likes,tags,safetensors`
3. Extract: architecture, parameter count, license, existing benchmarks, safetensors availability
4. Score candidates: `0.3*downloads + 0.25*likes + 0.25*trending + 0.2*recency`
5. Select top 3 candidates

**Output:** Ranked list of 3 candidate models with metadata

### Phase 2 — Dataset Match

Find training datasets compatible with the task and selected models.

```bash
# Search datasets by task keywords
hf datasets ls --search "TASK_KEYWORDS" --sort downloads --limit 20 --format json

# Get detailed info
hf datasets info DATASET_ID --format json
```

For each candidate dataset, validate quality via SQL:

```bash
# Check row count
hf datasets sql "SELECT COUNT(*) as total_rows FROM read_parquet('PARQUET_URL')"

# Check null ratio in key columns
hf datasets sql "SELECT
  COUNT(*) as total,
  SUM(CASE WHEN text IS NULL THEN 1 ELSE 0 END) as null_text,
  SUM(CASE WHEN label IS NULL THEN 1 ELSE 0 END) as null_label
FROM read_parquet('PARQUET_URL')"

# Check class distribution (for classification tasks)
hf datasets sql "SELECT label, COUNT(*) as count
FROM read_parquet('PARQUET_URL')
GROUP BY label ORDER BY count DESC"

# Check text length statistics
hf datasets sql "SELECT
  AVG(LENGTH(text)) as avg_len,
  MIN(LENGTH(text)) as min_len,
  MAX(LENGTH(text)) as max_len
FROM read_parquet('PARQUET_URL')"
```

Get parquet URLs first:
```bash
hf datasets parquet DATASET_ID --format json
```

**Output:** Ranked list of datasets with quality scores (row count, null ratio, class balance)

### Phase 3 — Compatibility Check

Cross-reference selected models with selected datasets.

**Validation checklist:**
1. **Tokenizer compatibility**: Model's tokenizer handles dataset's language/domain
2. **Task head match**: Model architecture supports the task type (e.g., SequenceClassification)
3. **Label format**: Dataset labels match expected format (text labels vs. numeric IDs)
4. **Sequence length**: Dataset text lengths fit within model's max context window
5. **License compatibility**: Model and dataset licenses are compatible for intended use

**Processing:**
1. Download model config: `hf download MODEL_ID --include "config.json" "tokenizer_config.json" --local-dir /tmp/inspect/`
2. Check tokenizer vocab for language coverage
3. Verify model architecture from config.json
4. Cross-check with dataset column names and types

**Output:** Compatibility matrix (model x dataset) with pass/fail per criterion

### Phase 4 — Cost Estimate

Estimate training cost based on model size, dataset size, and hardware.

```bash
# List available hardware and pricing
hf jobs hardware --format json
```

**Estimation formula:**
```
training_time_hours = (dataset_rows * epochs * tokens_per_row) / (hardware_TFLOPS * efficiency)
estimated_cost = training_time_hours * hourly_rate
```

Reference hardware FLOPS (see `references/cost-estimation.md`):
- `a10g-small`: ~125 TFLOPS (FP16), ~$1.05/hr
- `a10g-large`: ~250 TFLOPS (FP16), ~$3.15/hr
- `a100-large`: ~312 TFLOPS (FP16), ~$4.50/hr

**Output:** Cost estimate table with hardware options, estimated time, and cost

### Phase 5 — Config Generation

Generate a training configuration file.

Based on task type, select training method:
- **Classification/NER**: SFT with task-specific head
- **Instruction following**: SFT with chat template
- **Preference alignment**: DPO with preference pairs
- **Reasoning**: GRPO with reward function

Generate `train_config.yaml`:
```yaml
model_id: "selected-model-id"
dataset_id: "selected-dataset-id"
training_method: "sft"  # or dpo, grpo
hardware_flavor: "a10g-large"
hyperparameters:
  learning_rate: 2e-5
  num_epochs: 3
  batch_size: 8
  gradient_accumulation_steps: 4
  warmup_ratio: 0.1
  weight_decay: 0.01
  max_seq_length: 512
  lora_r: 16
  lora_alpha: 32
estimated_cost: "$12.50"
estimated_time: "~4 hours"
```

**Output:** `train_config.yaml` + training script

### Phase 6 — Launch or Report

Present the complete plan to the user for approval.

**If user approves training:**
1. Invoke `hf-model-trainer` with the generated config
2. Start `hf-trackio` monitoring
3. Create a collection: `hf collections add-item` for the model+dataset pair
4. Report job ID and monitoring dashboard URL

**If user declines or wants to review:**
1. Save training plan as `.docx` via `anthropic-docx`
2. Include: model comparison table, dataset quality report, cost estimate, config file
3. Report file path to user

## Output Summary

The pipeline produces:
- **Training Plan Document** (.docx) — model comparison, dataset quality, cost estimate
- **Config Files** — `train_config.yaml`, training script
- **Quality Report** — dataset null ratios, class balance, text length statistics
- **Cost Estimate** — hardware options with time and cost projections
- (Optional) **Running Job** — if user approves immediate training launch

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | No models found | Broaden search terms; try related task tags |
| 2 | No datasets found | Suggest creating a custom dataset; search broader terms |
| 2 | SQL query fails | Fall back to Dataset Viewer REST API for sampling |
| 3 | Incompatible model+data | Remove incompatible pairs; suggest adapter alternatives |
| 4 | Hardware unavailable | Try alternative flavors; estimate with fallback pricing |
| 6 | Job launch fails | Save config for manual retry; check auth and quota |
