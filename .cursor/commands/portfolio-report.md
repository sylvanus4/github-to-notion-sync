---
description: "Generate a cross-project portfolio report aggregating status from all managed projects into an executive summary"
---

## Portfolio Report

Generate an executive portfolio report spanning all managed ThakiCloud projects.

### Usage

```
/portfolio-report                           # generate for all managed projects
/portfolio-report --period weekly           # weekly rollup (default)
/portfolio-report --period monthly          # monthly rollup
/portfolio-report --skip-notion             # skip Notion upload
/portfolio-report --skip-slack              # skip Slack posting
```

### Execution

Read and follow the skill at `.cursor/skills/portfolio-report-generator/SKILL.md`.

User input: $ARGUMENTS

1. Iterate through all 5 managed projects (from project registry)
2. Collect GitHub activity, sprint progress, and release status per project
3. Calculate health scores (velocity, bug rate, PR cycle time)
4. Generate executive summary with cross-project risk matrix
5. Output Korean .docx, Notion page, and Slack summary
