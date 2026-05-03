---
name: morning-ship
description: Start-of-day pipeline — git pull all repos, Google Workspace briefing, and daily stock analysis.
disable-model-invocation: true
---

Run the complete morning startup pipeline.

## Pipeline (Sequential)

1. **Git Sync**: Pull latest from all 5 managed repos (sod-ship logic)
2. **Google Daily**: Calendar briefing + Gmail triage (google-daily)
3. **Stock Pipeline**: Full daily stock analysis (today)
4. **Consolidated Briefing**: Post morning summary to Slack #효정-할일

## Managed Repositories

- ai-platform-strategy (dev branch, full mode)
- ai-model-event-stock-analytics
- research
- ai-template
- github-to-notion-sync

## Output

- Git sync status per repo
- Calendar agenda for today
- Email triage summary
- Stock analysis report + Slack posts
- Consolidated morning briefing on Slack
