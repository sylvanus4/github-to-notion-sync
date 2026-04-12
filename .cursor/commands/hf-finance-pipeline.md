---
description: "End-to-end financial model improvement pipeline — prepare data, train, monitor, evaluate on HuggingFace (budget-aware for Pro $9/month)"
---

# HF Finance Pipeline — End-to-End Model Improvement

## Skill References

This composite command chains multiple HF skills:
- `.cursor/skills/hf-datasets/SKILL.md` — Dataset preparation
- `.cursor/skills/hf-model-trainer/SKILL.md` — Model training
- `.cursor/skills/hf-trackio/SKILL.md` — Experiment monitoring
- `.cursor/skills/hf/hf-evaluation/SKILL.md` — Model evaluation
- `.cursor/skills/hf-jobs/SKILL.md` — Compute jobs

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Mode

Determine the **pipeline mode** from user input:

| Mode | Pipeline | Est. Cost |
|------|----------|-----------|
| `train-sentiment` | datasets → trainer (FinBERT SFT) → trackio → evaluation | ~$2-5 |
| `train-embeddings` | datasets → trainer (sentence-transformer) → trackio → evaluation | ~$2-5 |
| `upload-data` | datasets (create/update on Hub) | Free |
| `benchmark` | evaluation → trackio (log results) | ~$0.50-2 |
| `validate` | dataset-viewer (inspect) → datasets (validate format) | Free |
| `status` | trackio (list runs) → jobs (list jobs) | Free |

If no mode specified, show the table above and ask user to choose.

### Step 2: Budget Gate ($9/month Pro Plan)

Before any paid operation:

1. Check remaining budget (user tracks manually)
2. Estimate job cost using `scripts/estimate_cost.py`
3. Recommend cheapest viable hardware:
   - **Free**: `upload-data`, `validate`, `status` modes
   - **~$0.10-0.50**: Dataset validation on `cpu-basic`
   - **~$0.75-1.50**: Small experiments on `t4-small` (1-2 hours)
   - **~$3.50-5.00**: Production training on `a10g-small` (1 hour)

**Cost-saving tips:**
- Validate datasets on CPU before GPU training
- Use small subsets (100-500 rows) for initial experiments
- Use LoRA (r=8-16) to reduce memory and training time
- Skip eval during quick experiments (`eval_strategy="no"`)
- Use `t4-small` unless model requires more VRAM

### Step 3: Execute Pipeline

#### Mode: `train-sentiment`

Fine-tune FinBERT or similar model for financial sentiment analysis.

**Phase 1 — Data Prep** (hf-datasets):
1. Prepare sentiment-labeled dataset from project data
2. Upload to Hub: `{username}/finance-sentiment-{date}`
3. Validate format on CPU

**Phase 2 — Training** (hf-model-trainer):
1. Base model: `ProsusAI/finbert` or `yiyanghkust/finbert-tone`
2. Method: SFT with LoRA (r=16, alpha=32)
3. Hardware: `t4-small` for <1B, `a10g-small` for larger
4. Include Trackio monitoring

**Phase 3 — Monitoring** (hf-trackio):
1. Check Trackio dashboard for training progress
2. Monitor loss convergence and eval metrics

**Phase 4 — Evaluation** (hf-evaluation):
1. Run sentiment benchmarks on test split
2. Compare against base FinBERT accuracy
3. Update model card with results

#### Mode: `train-embeddings`

Fine-tune sentence-transformers for financial text similarity.

**Phase 1 — Data Prep**: Prepare sentence pairs from stock analysis reports
**Phase 2 — Training**: Fine-tune `all-MiniLM-L6-v2` with SFT
**Phase 3 — Monitoring**: Track contrastive loss metrics
**Phase 4 — Evaluation**: Compare embedding quality on financial text benchmarks

#### Mode: `upload-data`

Upload curated financial data to HuggingFace Hub.

1. Read the hf-datasets skill
2. Create/update dataset repository
3. Stream rows or upload files
4. Set proper metadata (source, date range, tickers)

#### Mode: `benchmark`

Run evaluation benchmarks on existing models.

1. Read the hf-evaluation skill
2. Run lighteval or inspect-ai on target model
3. Log results to Trackio
4. Update model card

#### Mode: `validate`

Validate dataset format before training.

1. Use hf-dataset-viewer to inspect structure
2. Run format validation on CPU
3. Report compatibility for SFT/DPO/GRPO

#### Mode: `status`

Check status of all HF resources.

1. List recent Trackio runs
2. List active/completed jobs
3. Show dashboard URLs

### Step 4: Summary

Report:
- Pipeline mode and phases completed
- Total estimated cost
- Hub URLs for all created resources (models, datasets, dashboards)
- Recommendations for next steps

## Constraints

- Always estimate and report costs before paid operations
- Never exceed single-job cost of $5 without user confirmation
- Always validate datasets on CPU before GPU training
- Always include Trackio in training scripts
- Always set `push_to_hub=True` for training jobs
- Use `HF_TOKEN` from `.env` for authentication
- This pipeline is advisory — each phase asks for confirmation before executing
