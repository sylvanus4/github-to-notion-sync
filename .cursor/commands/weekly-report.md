---
description: "Generate an automated weekly status report aggregating GitHub, Notion, and Slack activity into Korean .docx + Notion + Slack"
---

## Weekly Report

Generate a comprehensive weekly status report from multiple sources.

### Usage

```
/weekly-report                              # generate report for the past week
/weekly-report --since 2026-03-10           # custom start date
/weekly-report --skip-slack                 # generate report but skip Slack posting
/weekly-report --skip-notion                # skip Notion page creation
```

### Execution

Read and follow the skill at `.cursor/skills/weekly-status-report/SKILL.md`.

User input: $ARGUMENTS

1. Collect data from GitHub (commits, PRs, issues), Notion (sprint board), and Slack (key threads)
2. Aggregate metrics: velocity, completion rate, blockers
3. Generate Korean .docx report via anthropic-docx
4. Create Notion sub-page under team wiki
5. Post summary to Slack #효정-할일 with thread details
