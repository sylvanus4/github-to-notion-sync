---
description: "Fine-tune a language model with TRL on HuggingFace Jobs — SFT, DPO, GRPO with Trackio monitoring"
---

# HF Train — Model Fine-Tuning Pipeline

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-model-trainer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **training task** from user input:

- **sft <model> <dataset>**: Supervised Fine-Tuning
- **dpo <model> <dataset>**: Direct Preference Optimization
- **grpo <model> <dataset>**: Group Relative Policy Optimization
- **estimate <model> <dataset>**: Estimate cost and time only (no training)
- **gguf <model>**: Convert a trained model to GGUF format
- No arguments: Show usage guide with cost-efficient recommendations

### Step 2: Budget Check (HF Pro $9/month)

Before launching any job, estimate cost:

```bash
cd .cursor/skills/hf-model-trainer
uv run scripts/estimate_cost.py \
  --model <model> \
  --dataset <dataset> \
  --hardware <flavor> \
  --epochs <n>
```

**Budget guidelines (Pro $9/month):**
- Prefer `t4-small` (~$0.75/hr) for demos and small experiments
- Use `cpu-basic` for dataset validation (free or minimal cost)
- Reserve `a10g-small` for production runs only
- Always validate dataset format on CPU first before GPU training

### Step 3: Dataset Validation

For unknown datasets, validate format before GPU training:

```python
hf_jobs("uv", {
    "script": "https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py",
    "script_args": ["--dataset", "<dataset>", "--split", "train"],
    "flavor": "cpu-basic"
})
```

### Step 4: Launch Training

Use `hf_jobs("uv", {...})` MCP tool with inline script. Always include:
- `push_to_hub=True` and `hub_model_id`
- `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- `report_to="trackio"` for monitoring
- Appropriate timeout (minimum 1-2 hours)

### Step 5: Report

Provide: job ID, monitoring URL, estimated time, estimated cost, Trackio dashboard URL.

## Constraints

- Always estimate cost before launching (Pro plan = $9/month budget)
- Always validate unknown datasets on CPU first
- Always include Trackio monitoring
- Always set `push_to_hub=True` (ephemeral environment)
- Default to `t4-small` for experiments, `a10g-small` for production
- Use LoRA/PEFT for models >7B
