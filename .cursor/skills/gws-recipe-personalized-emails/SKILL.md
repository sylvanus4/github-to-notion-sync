---
name: gws-recipe-personalized-emails
description: >-
  Read recipient data from Google Sheets and send personalized Gmail messages
  to each row. Use when the user asks to send bulk personalized emails from
  a spreadsheet, mail merge, or batch email from sheet data. Do NOT use for
  single email sending (use gws-gmail) or non-email notifications (use
  gws-chat).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
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
