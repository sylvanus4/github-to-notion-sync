---
description: "Run compute workloads on HuggingFace Jobs — UV scripts, Docker jobs, batch inference, scheduled tasks"
---

# HF Jobs — Compute Workloads

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-jobs/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **job operation** from user input:

- **run <script>**: Submit a UV script or Docker job to HF Jobs
- **list / ps**: List running and completed jobs
- **logs <job-id>**: View job logs
- **cancel <job-id>**: Cancel a running job
- **hardware**: List available hardware options and pricing
- **schedule <script> <cron>**: Create a scheduled job
- No arguments: Show running jobs and available hardware

### Step 2: Budget Check

Before submitting jobs, consider the Pro $9/month budget:

| Hardware | Cost/hr | Budget allows |
|----------|---------|--------------|
| cpu-basic | ~$0.10 | ~90 hours |
| t4-small | ~$0.75 | ~12 hours |
| a10g-small | ~$3.50 | ~2.5 hours |

Always start with the cheapest hardware that meets requirements.

### Step 3: Submit Job

```bash
hf jobs uv run \
  --flavor <hardware> \
  --timeout <duration> \
  --secrets HF_TOKEN \
  "<script-url-or-inline>"
```

### Step 4: Report

Provide job ID, status, monitoring URL, and estimated cost.

## Constraints

- Always estimate cost before submitting
- Use `cpu-basic` for non-GPU workloads
- Set appropriate timeouts (default 30min is too short for training)
- Always include `--secrets HF_TOKEN` for Hub access
- For TRL training, prefer the `/hf-train` command instead
