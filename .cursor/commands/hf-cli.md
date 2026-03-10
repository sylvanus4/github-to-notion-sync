---
description: "Run HuggingFace Hub CLI operations — download models, upload files, manage repos, check auth"
---

# HF CLI — HuggingFace Hub Operations

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-cli/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **operation** from user input:

- **auth / login / whoami**: Check or manage HF authentication
- **download <repo>**: Download model or dataset files from Hub
- **upload <repo> <path>**: Upload files to Hub
- **repo create / delete / info**: Manage Hub repositories
- **jobs / list / logs**: Manage HF Jobs
- **cache**: Manage local model cache
- No arguments: Show available commands and auth status

### Step 2: Verify Authentication

Before any Hub operation, verify auth:

```bash
hf auth whoami
```

If not authenticated, use the `HF_TOKEN` from `.env`:

```bash
export HF_TOKEN=$(grep HF_TOKEN .env | cut -d= -f2)
hf auth login --token $HF_TOKEN
```

### Step 3: Execute Operation

Run the requested `hf` CLI command. Use `--format json` for machine-readable output when piping results.

### Step 4: Report Results

Summarize what was done, any files downloaded/uploaded, and the Hub URL.

## Constraints

- Always verify auth before write operations
- Use `HF_TOKEN` from `.env` (never hardcode tokens)
- For large uploads, prefer `hf upload-large-folder`
- Report Hub URLs for all created/modified resources
