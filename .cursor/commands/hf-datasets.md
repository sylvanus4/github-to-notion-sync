---
description: "Create and manage datasets on HuggingFace Hub — init repos, stream rows, run SQL queries"
---

# HF Datasets — Dataset Management

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-datasets/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **dataset operation** from user input:

- **create <name>**: Initialize a new dataset repository on Hub
- **add-rows <dataset> <data>**: Stream rows to an existing dataset
- **sql <query>**: Run SQL query against a dataset
- **config <dataset>**: Set dataset configuration and system prompts
- **upload <dataset> <file>**: Upload local data files to Hub dataset
- No arguments: Show usage guide

### Step 2: Verify Authentication

```bash
export HF_TOKEN=$(grep HF_TOKEN .env | cut -d= -f2)
```

### Step 3: Execute Operation

Use the dataset management scripts from the skill:

```bash
cd .cursor/skills/hf-datasets
uv run scripts/<script>.py [args]
```

### Step 4: Report Results

Show dataset URL, row counts, and any configuration applied.

## Constraints

- Always verify auth before write operations
- Use streaming for large datasets (avoid loading full dataset into memory)
- For financial datasets, include proper metadata (source, date range, ticker list)
- Use SQL queries for data exploration before downloading
