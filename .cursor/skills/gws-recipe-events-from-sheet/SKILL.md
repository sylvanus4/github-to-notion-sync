---
name: gws-recipe-events-from-sheet
description: >-
  Read event data from a Google Sheets spreadsheet and create Google Calendar
  entries for each row. Use when the user asks to bulk-create calendar events
  from a spreadsheet, import events from sheet data, or batch schedule from a
  table. Do NOT use for single event creation (use gws-calendar) or non-calendar
  data (use gws-sheets). Korean triggers: "일정 일괄 생성", "시트에서 일정".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
---
# Recipe: Create Calendar Events from a Sheet

> **Required skills**: `gws-sheets`, `gws-calendar`

Read event data from a Google Sheets spreadsheet and create Google Calendar entries for each row.

## Steps

1. **Read event data** from the spreadsheet:

```bash
gws sheets +read --spreadsheet SHEET_ID --range 'Events!A2:D'
```

Expected columns: Summary, Start Time (ISO 8601), End Time (ISO 8601), Attendees (comma-separated emails).

2. **For each row**, substitute values and create a calendar event:

```bash
# Example: row = ["Team Standup", "2026-03-10T09:00:00+09:00", "2026-03-10T09:30:00+09:00", "alice@co.com,bob@co.com"]
gws calendar +insert \
  --summary 'Team Standup' \
  --start '2026-03-10T09:00:00+09:00' \
  --end '2026-03-10T09:30:00+09:00' \
  --attendee alice@co.com \
  --attendee bob@co.com
```

The agent reads each row, substitutes literal values. For the Attendees column (comma-separated), split by comma and pass each email as a separate `--attendee` flag.

> **Write command** -- confirm the event list with the user before creating.

## Tips

- Create the first event and confirm with the user before the full batch
- Times must be RFC 3339 format (e.g. `2026-03-10T09:00:00+09:00`)
- For recurring events, use the raw Calendar API
- Consider adding a "Created" column to track which events have been created

## Examples

### Example 1: Basic operation

**User says:** "Bulk-create calendar events from a spreadsheet"

**Actions:**
1. Verify `gws` CLI is authenticated (`gws auth status`)
2. Execute the appropriate `gws` command with required parameters
3. Confirm the result and report back

### Example 2: Troubleshooting

**User says:** "The command failed with an authentication error"

**Actions:**
1. Check auth status: `gws auth status`
2. Re-authenticate if expired: `gws auth login`
3. Retry the original command
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Authentication error | Run `gws auth status` and re-authenticate if expired |
| API rate limit | Wait and retry. For bulk operations, add delays between requests |
| Resource not found | Verify the resource ID/name and check permissions |
