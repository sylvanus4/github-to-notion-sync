---
name: weekly-status-report
description: >-
  Generate automated weekly status reports by aggregating GitHub sprint data,
  Notion project updates, Slack channel summaries, and completed tasks.
  Produces a structured Korean report as .docx + Notion page + Slack post.
  Use when the user asks to "generate weekly report", "weekly status",
  "주간 리포트", "주간 보고서", "weekly-status-report", or wants automated
  weekly reporting. Do NOT use for daily stock reports (use today), GitHub
  activity digests only (use github-sprint-digest), or cross-project portfolio
  reports (use portfolio-report-generator).
metadata:
  version: "1.0.1"
  category: "execution"
  author: "thaki"
---
# Weekly Status Report Generator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Aggregate data from multiple sources into a structured weekly status report, replacing the manual 4-hour weekly reporting process.

## When to Use

- End of each sprint week (typically Friday afternoon)
- When management requests a status update
- As part of the EOD pipeline on reporting days

## Workflow

### Step 1: Gather Data Sources

Collect data from the past 7 days across all sources:

**GitHub** (via `github-sprint-digest` data):
```bash
gh issue list --state all --json number,title,state,labels,closedAt,assignees --search "updated:>=$(date -v-7d +%Y-%m-%d)"
gh pr list --state all --json number,title,state,mergedAt,author --search "updated:>=$(date -v-7d +%Y-%m-%d)"
```

**Notion** (via `planning-weekly-pulse` data):
- Project status changes
- Completed milestones
- Updated roadmap items

**Slack** (via Slack MCP):
- Key decisions from team channels
- Blockers raised and resolved
- Customer feedback highlights

### Step 2: Classify and Organize

Group gathered data into standard sections:

1. **Accomplishments**: Merged PRs, closed issues, completed milestones
2. **In Progress**: Open PRs, active issues, ongoing work
3. **Blockers**: Blocked items, unresolved dependencies, stale reviews
4. **Risks**: Overdue items, scope changes, resource constraints
5. **Next Week Plan**: Upcoming milestones, planned work, meetings

### Step 3: Generate Metrics

Calculate key metrics:
- **Velocity**: Story points completed vs planned
- **PR Cycle Time**: Average time from PR open to merge
- **Issue Resolution**: Issues opened vs closed
- **Sprint Burndown**: Remaining work vs sprint timeline
- **Review Coverage**: PRs reviewed within 24h

### Step 4: Write Report

Generate a structured Korean report following the 3P format (Progress, Plans, Problems). Include: title with date range; executive summary (3 sentences); accomplishments with checkmarks and owners; metrics table (week vs prior week); next-week plan; risks/blockers with severity. Use Korean section headings and bullets per output rule.

### Step 5: Generate .docx

Use `anthropic-docx` to create a formatted Word document with:
- Company header/footer
- Table of contents
- Formatted metrics tables
- Color-coded status indicators

### Step 6: Publish to Notion

Use `md-to-notion` to create a Notion page under the weekly reports parent.

### Step 7: Post to Slack

Post a condensed summary to the team Slack channel with:
- Key metrics as inline stats
- Top 3 accomplishments
- Critical blockers
- Link to full report (Notion page)

## Output

```
Weekly Report Generated
=======================
Period: 2026-03-13 ~ 2026-03-19
Report ID: weekly-2026-W12

Outputs:
- DOCX: output/reports/weekly-2026-W12.docx
- Notion: <page-url>
- Slack: Posted to #team-updates

Metrics Summary:
- Story Points: 21/25 (84%)
- PRs Merged: 8
- Issues Closed: 12
- Blockers: 2 active
```

## Error Handling

| Error | Action |
|-------|--------|
| GitHub API rate limit | Retry with exponential backoff; if exhausted, generate report with partial GitHub data and note "GitHub data incomplete" |
| Notion MCP not connected | Skip Notion publish; save DOCX and post to Slack with local file path; prompt user to connect Notion |
| No activity in time range | Generate minimal report with "No activity this period" in each section; still produce DOCX and post to Slack |
| DOCX generation fails | Retry with `anthropic-docx`; if still fails, output markdown-only report and post raw markdown to Slack |
| Slack posting fails | Save report locally; retry Slack post once; report failure to user with file path |

## Examples

### Example 1: End-of-week report
User says: "Generate weekly report"
Actions:
1. Aggregate 7 days of GitHub, Notion, Slack data
2. Calculate metrics and classify items
3. Write Korean report
4. Generate .docx, publish to Notion, post to Slack
Result: Complete weekly report across all channels

### Example 2: Custom period
User says: "Weekly report for last two weeks"
Actions:
1. Extend data collection to 14-day window
2. Generate comparative metrics (week-over-week)
3. Produce consolidated report
Result: Two-week report with trend comparison
