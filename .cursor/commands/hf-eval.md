---
description: "Evaluate model quality with lighteval/inspect-ai and manage evaluation results in model cards"
---

# HF Eval — Model Evaluation

## Skill Reference

Read and follow the skill at `.cursor/skills/hf/hf-evaluation/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **evaluation task** from user input:

- **run <model> <task>**: Run evaluation benchmark (lighteval or inspect-ai)
- **inspect <repo>**: Inspect evaluation tables in a model card
- **extract <repo>**: Extract evaluation results from README to model-index
- **import-aa <model>**: Import scores from Artificial Analysis API
- **validate <repo>**: Validate existing model-index metadata
- No arguments: Show usage guide

### Step 2: Pre-Flight Check

1. Verify auth: `hf auth whoami`
2. For `--create-pr` operations, check for existing PRs first:

```bash
cd .cursor/skills/hf-evaluation
uv run scripts/evaluation_manager.py get-prs --repo-id "<repo>"
```

### Step 3: Execute Evaluation

For running benchmarks, prefer cost-efficient hardware:
- `cpu-basic` for small models or simple tasks
- `t4-small` for models <3B params
- `a10g-small` for larger models

### Step 4: Report Results

Show evaluation scores, model-index YAML, and any created PRs.

## Constraints

- Always check for existing PRs before creating new ones
- Use `inspect-tables` first to understand table structure
- Preview YAML output before applying changes
- Prefer cost-efficient hardware (cpu-basic > t4-small > a10g)
