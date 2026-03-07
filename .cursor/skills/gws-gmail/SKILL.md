---
name: gws-gmail
description: >-
  Manage Gmail via the gws CLI -- send emails, triage inbox, watch for new
  messages, manage labels and filters. Use when the user asks to send email,
  check inbox, read mail, triage messages, or manage Gmail. Do NOT use for
  Google Chat messages (use gws-chat), calendar invites (use gws-calendar),
  or Drive file operations (use gws-drive).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Gmail

> **Prerequisites**: `gws` must be installed and authenticated. See `gws-workspace` skill.

```bash
gws gmail <resource> <method> [flags]
```

## Quick Commands

### Send Email

```bash
gws gmail +send --to <EMAIL> --subject <SUBJECT> --body <TEXT>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--to` | Yes | Recipient email |
| `--subject` | Yes | Email subject |
| `--body` | Yes | Plain text body |

For HTML, attachments, or CC/BCC, use the raw API: `gws gmail users messages send --json '...'`

> **Write command** -- confirm with the user before executing.

### Triage Inbox

```bash
gws gmail +triage
gws gmail +triage --max 5 --query 'from:boss'
gws gmail +triage --labels --format table
```

| Flag | Default | Description |
|------|---------|-------------|
| `--max` | 20 | Maximum messages to show |
| `--query` | is:unread | Gmail search query |
| `--labels` | off | Include label names |

Read-only -- never modifies your mailbox.

### Watch for New Emails

```bash
gws gmail +watch --project <GCP_PROJECT_ID>
gws gmail +watch --project my-project --label-ids INBOX --once
gws gmail +watch --project my-project --cleanup --output-dir ./emails
```

| Flag | Default | Description |
|------|---------|-------------|
| `--project` | -- | GCP project ID for Pub/Sub |
| `--subscription` | -- | Existing Pub/Sub subscription |
| `--label-ids` | -- | Comma-separated label IDs to filter |
| `--max-messages` | 10 | Max messages per pull batch |
| `--poll-interval` | 5 | Seconds between pulls |
| `--once` | off | Pull once and exit |
| `--cleanup` | off | Delete Pub/Sub resources on exit |
| `--output-dir` | -- | Write each message to JSON file |

Gmail watch expires after 7 days -- re-run to renew.

## Raw API Resources

### users

- `getProfile` -- current user's Gmail profile
- `drafts` -- create, delete, get, list, send, update
- `history` -- list history changes
- `labels` -- create, delete, get, list, patch, update
- `messages` -- delete, get, import, insert, list, modify, send, trash, untrash
  - `attachments` -- get attachment data
- `settings` -- getAutoForwarding, getImap, getLanguage, getPop, getVacation, updateAutoForwarding, updateImap, updateLanguage, updatePop, updateVacation
  - `delegates`, `filters`, `forwardingAddresses`, `sendAs` (with `smimeInfo`)
- `threads` -- delete, get, list, modify, trash, untrash
- `stop` / `watch` -- push notification management

## Discovering Commands

```bash
gws gmail --help
gws schema gmail.users.messages.list
gws schema gmail.users.messages.send
```

## Common Patterns

```bash
# List unread messages (use --fields to protect context window)
gws gmail users messages list \
  --params '{"userId": "me", "q": "is:unread", "maxResults": 10}' \
  --fields "messages(id,threadId)"

# Get a specific message
gws gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID"}'

# List labels
gws gmail users labels list --params '{"userId": "me"}'

# Search messages
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:alice subject:report after:2026/01/01"}'
```
