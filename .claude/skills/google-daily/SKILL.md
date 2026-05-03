---
name: google-daily
description: Google Workspace daily automation — calendar briefing, Gmail triage, Drive upload, Slack notification.
disable-model-invocation: true
---

Run the daily Google Workspace automation pipeline.

## Pipeline (Sequential)

1. **Pre-flight Auth**: Verify Slack, Notion, and gws CLI authentication
2. **Calendar Briefing**: Fetch today's events, highlight meetings requiring prep
3. **Gmail Triage**: Delete spam, label low-priority notifications, summarize unanswered emails
4. **Drive Upload**: Upload any pending pipeline outputs to Google Drive
5. **Slack Notification**: Post consolidated briefing to #효정-할일 as threaded replies
6. **Memory Sync**: Update MEMORY.md with new information

## Dependencies

- `gws` CLI installed and authenticated (`gws auth status`)
- Slack MCP available
- Notion MCP available

## Output

- Calendar agenda summary (Korean)
- Email triage report with action items
- Drive upload links (webViewLink URLs)
- Slack thread with briefing
