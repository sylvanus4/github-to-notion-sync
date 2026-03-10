---
description: "Track and visualize ML training experiments with Trackio — log metrics, fire alerts, retrieve results"
---

# HF Trackio — Experiment Tracking

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-trackio/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **tracking operation** from user input:

- **status / list**: List recent training runs and their metrics
- **logs <run>**: Retrieve logged metrics for a specific run
- **alerts <run>**: Check fired alerts for a run
- **dashboard**: Get Trackio dashboard URL
- **compare <run1> <run2>**: Compare metrics between runs
- No arguments: Show dashboard URL and recent runs

### Step 2: Execute

Use the Trackio CLI for retrieving metrics:

```bash
trackio runs list
trackio runs logs <run-id>
trackio alerts list <run-id>
```

Or use the Python API for logging (inside training scripts).

### Step 3: Report

Show metrics summary, dashboard link, and any alerts.

## Constraints

- Trackio is primarily used within training scripts (hf-model-trainer)
- Use CLI for post-training analysis and retrieval
- Dashboard syncs to HF Spaces for real-time monitoring
