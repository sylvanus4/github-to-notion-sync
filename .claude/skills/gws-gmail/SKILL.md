---
name: gws-gmail
description: >-
  Manage Gmail via the gws CLI -- send emails, triage inbox, watch for new
  messages, manage labels and filters. Use when the user asks to send email,
  check inbox, read mail, triage messages, or manage Gmail. Do NOT use for
  Google Chat messages (use gws-chat), calendar invites (use gws-calendar), or
  Drive file operations (use gws-drive), or AI-drafted reply workflows with
  approval gates (use email-auto-reply). Korean triggers: "이메일", "메일 보내기",
  "받은편지함".
disable-model-invocation: true
---

# Gmail

> **Prerequisites**: `gws` CLI installed + `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` env var set. See `gws-workspace` skill for the manual OAuth2 bypass setup.

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

**Note**: `--fields` is NOT a standalone flag. Pass `fields` inside `--params` JSON.

```bash
# List unread messages
gws gmail users messages list \
  --params '{"userId": "me", "q": "is:unread", "maxResults": 10}'

# Get a specific message (full)
gws gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID"}'

# Get message metadata only (lightweight)
gws gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID", "format": "metadata", "metadataHeaders": ["From", "Subject", "Date", "To", "Cc"]}'

# List labels
gws gmail users labels list --params '{"userId": "me"}'

# Search messages by date range
gws gmail users messages list \
  --params '{"userId": "me", "q": "after:2026/03/09 before:2026/03/10", "maxResults": 20}'

# Search messages by sender
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:alice subject:report after:2026/01/01"}'

# Trash a message (reversible)
gws gmail users messages trash \
  --params '{"userId": "me", "id": "MSG_ID"}'

# Modify labels (move to label, remove from inbox)
gws gmail users messages modify \
  --params '{"userId": "me", "id": "MSG_ID"}' \
  --json '{"addLabelIds": ["LABEL_ID"], "removeLabelIds": ["INBOX"]}'

# Create a label
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "Low Priority", "labelListVisibility": "labelShow", "messageListVisibility": "show"}'

# Get attachment data
gws gmail users messages attachments get \
  --params '{"userId": "me", "messageId": "MSG_ID", "id": "ATTACHMENT_ID"}'
```

## Gmail Filters

Manage automatic email rules via the Gmail settings API.

```bash
# List existing filters
gws gmail users settings filters list --params '{"userId": "me"}'

# Create a filter (e.g., label GitHub notifications and skip inbox)
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "notifications@github.com"},
    "action": {"addLabelIds": ["LABEL_ID"], "removeLabelIds": ["INBOX"]}
  }'

# Create a filter to auto-delete spam-like emails
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "noreply@spam-domain.com"},
    "action": {"removeLabelIds": ["INBOX"], "addLabelIds": ["TRASH"]}
  }'

# Delete a filter
gws gmail users settings filters delete \
  --params '{"userId": "me", "id": "FILTER_ID"}'

# Get a specific filter
gws gmail users settings filters get \
  --params '{"userId": "me", "id": "FILTER_ID"}'
```

### Filter Criteria Fields

| Field | Description | Example |
|-------|-------------|---------|
| `from` | Sender address or pattern | `"notifications@github.com"` |
| `to` | Recipient address | `"me@company.com"` |
| `subject` | Subject contains | `"[GitHub]"` |
| `query` | Gmail search query | `"is:unread category:promotions"` |
| `hasAttachment` | Has attachment | `true` |
| `size` | Message size (bytes) | `5000000` |
| `sizeComparison` | `"larger"` or `"smaller"` | `"larger"` |

### Filter Action Fields

| Field | Description |
|-------|-------------|
| `addLabelIds` | Label IDs to add |
| `removeLabelIds` | Label IDs to remove (e.g., `["INBOX"]` to skip inbox) |
| `forward` | Email to forward to |

## Examples

### Example 1: Basic operation

**User says:** "Send email"

**Actions:**
1. Verify `gws` CLI is authenticated (`gws gmail +triage --max 1`)
2. Execute the appropriate `gws` command with required parameters
3. Confirm the result and report back

### Example 2: Troubleshooting

**User says:** "The command failed with an authentication error"

**Actions:**
1. Verify `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` is set: `echo $GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`
2. Re-authenticate: `python3 ~/.config/gws/oauth2_manual.py`
3. Clean stale caches: `rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`
4. Retry the original command

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Authentication error | Run `python3 ~/.config/gws/oauth2_manual.py` and clean caches (`rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`) |
| API rate limit | Wait and retry. For bulk operations, add delays between requests |
| Resource not found | Verify the resource ID/name and check permissions |
