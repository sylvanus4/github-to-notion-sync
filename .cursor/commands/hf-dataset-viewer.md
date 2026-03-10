---
description: "Explore and query HuggingFace datasets via the Dataset Viewer REST API — metadata, rows, search, filter"
---

# HF Dataset Viewer — Dataset Exploration

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-dataset-viewer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **exploration task** from user input:

- **info <dataset>**: Get dataset metadata and splits
- **preview <dataset>**: Show first rows of a dataset
- **search <dataset> <query>**: Search text within dataset
- **filter <dataset> <predicate>**: Filter rows by condition
- **parquet <dataset>**: Get parquet file URLs for download
- **stats <dataset>**: Get dataset size and statistics
- No arguments: Show usage guide

### Step 2: Execute

Use the Dataset Viewer REST API endpoints:

1. Validate: `GET /is-valid?dataset=<id>`
2. Splits: `GET /splits?dataset=<id>`
3. First rows: `GET /first-rows?dataset=<id>&config=<config>&split=<split>`
4. Paginate: `GET /rows?dataset=<id>&config=<config>&split=<split>&offset=0&length=100`
5. Search: `GET /search?dataset=<id>&config=<config>&split=<split>&query=<text>`
6. Filter: `GET /filter?dataset=<id>&config=<config>&split=<split>&where=<condition>`

### Step 3: Report

Show dataset structure, sample rows, and any search/filter results.

## Constraints

- Max 100 rows per request (use pagination for more)
- Default config is usually "default", default split is "train"
- Use `/first-rows` for quick previews before full exploration
- For large datasets, use `/parquet` to download and process locally
