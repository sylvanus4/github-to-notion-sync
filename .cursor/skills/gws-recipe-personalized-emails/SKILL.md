---
name: gws-recipe-personalized-emails
description: >-
  Read recipient data from Google Sheets and send personalized Gmail messages
  to each row. Use when the user asks to send bulk personalized emails from a
  spreadsheet, mail merge, or batch email from sheet data. Do NOT use for single
  email sending (use gws-gmail) or non-email notifications (use gws-chat).
  Korean triggers: "일괄 이메일", "메일 머지".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
---
# Recipe: Send Personalized Emails from a Sheet

> **Required skills**: `gws-sheets`, `gws-gmail`

Read recipient data from Google Sheets and send personalized Gmail messages to each row.

## Steps

1. **Read recipient list** from the spreadsheet:

```bash
gws sheets +read --spreadsheet SHEET_ID --range 'Contacts!A2:C'
```

Expected columns: Name, Email, Custom Field (adapt as needed).

2. **For each row**, substitute the row values and send:

```bash
# Example: if row is ["Alice", "alice@co.com", "Q1"]
gws gmail +send \
  --to 'alice@co.com' \
  --subject 'Hello, Alice' \
  --body 'Hi Alice, your Q1 report is ready.'
```

The agent reads each row from the JSON output, substitutes column values into the subject/body, then calls `+send` with literal values. The CLI does not support template variables.

> **Write command** -- confirm the email template and recipient list with the user before executing the batch.

## Tips

- Send one test email first and confirm with the user before the full batch
- Use `--format table` on the sheets read to visually verify data
- For HTML emails or attachments, use the raw Gmail API instead of `+send`
- Consider adding a "Sent" column and updating it after each send to track progress

## Examples

### Example 1: Basic operation

**User says:** "Send bulk personalized emails from a spreadsheet"

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
