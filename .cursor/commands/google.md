## Google Daily Automation

Run all Google Workspace daily tasks in one flow: calendar briefing, Gmail inbox triage, and Drive upload.

### Usage

```
/google
```

### Workflow

1. **Calendar Briefing** -- Fetch today's schedule, classify events, alert for meetings/interviews needing preparation
2. **Gmail Triage** -- Fetch yesterday's emails, delete spam, move low-priority notifications (Notion, RunPod, GitHub, calendar accepts) to "Low Priority" label, extract bespin_news links into a news digest .docx, summarize unanswered emails with action items into a reply-needed .docx, create Gmail filters for recurring patterns
3. **Drive Upload** -- Upload generated .docx/.pptx files to a dated Google Drive folder
4. **Summary** -- Present unified Korean daily briefing with all results
5. **Slack Orphan Cleanup** -- Delete orphaned thread replies (deleted parent, remaining replies) in #press, #deep-research, #ai-coding-radar, #idea

### Execution

Read and follow the `google-daily` skill (`.cursor/skills/google-daily/SKILL.md`) for detailed instructions. The skill orchestrates three sub-skills sequentially:

- `calendar-daily-briefing` (`.cursor/skills/calendar-daily-briefing/SKILL.md`)
- `gmail-daily-triage` (`.cursor/skills/gmail-daily-triage/SKILL.md`)
- `gws-drive` (`.cursor/skills/gws-drive/SKILL.md`)
- `slack-orphan-cleaner` (`.cursor/skills/slack-orphan-cleaner/SKILL.md`)

### Prerequisites

- `gws` CLI installed and authenticated: `gws auth login -s drive,gmail,calendar`
- Playwright available for news article extraction
- `SLACK_USER_TOKEN` in `.env` for orphan cleanup (optional — skipped if missing)

### Examples

Run the full daily automation:
```
/google
```
