# Dataset Validation

**Validate dataset format BEFORE launching GPU training** to prevent the #1 cause of training failures: format mismatches.

## Why Validate

- 50%+ of training failures are due to dataset format issues
- DPO especially strict: requires exact column names (`prompt`, `chosen`, `rejected`)
- Failed GPU jobs waste $1-10 and 30-60 minutes
- Validation on CPU costs ~$0.01 and takes <1 minute

## When to Validate

**ALWAYS validate for:**
- Unknown or custom datasets
- DPO training (CRITICAL - 90% of datasets need mapping)
- Any dataset not explicitly TRL-compatible

**Skip for known TRL datasets:**
- `trl-lib/ultrachat_200k`, `trl-lib/Capybara`, `HuggingFaceH4/ultrachat_200k`, etc.

## Usage

```python
hf_jobs("uv", {
    "script": "https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py",
    "script_args": ["--dataset", "username/dataset-name", "--split", "train"]
})
```

Or locally:
```bash
uv run https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py \
  --dataset name --split train
```

## Reading Results

- **✓ READY** - Dataset is compatible, use directly
- **✗ NEEDS MAPPING** - Compatible but needs preprocessing (mapping code provided)
- **✗ INCOMPATIBLE** - Cannot be used for this method

When mapping is needed, the output includes a **"MAPPING CODE"** section with copy-paste ready Python.

## DPO Format Mismatch (Common)

Most DPO datasets use non-standard column names:

```
Dataset has: instruction, chosen_response, rejected_response
DPO expects: prompt, chosen, rejected
```

The validator detects this and provides exact mapping code:

```python
def format_for_dpo(example):
    return {
        'prompt': example['instruction'],
        'chosen': example['chosen_response'],
        'rejected': example['rejected_response'],
    }
dataset = dataset.map(format_for_dpo, remove_columns=dataset.column_names)
```
