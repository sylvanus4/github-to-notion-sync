---
name: gws-chat
description: >-
  Manage Google Chat via the gws CLI -- send messages, list spaces, and manage
  chat conversations. Use when the user asks to send a Google Chat message, list
  Chat spaces, or manage Chat conversations. Do NOT use for Slack messaging (use
  Slack MCP tools), email (use gws-gmail), or SMS/phone. Korean triggers: "구글 챗", "챗 메시지".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
---
# Google Chat

> **Prerequisites**: `gws` must be installed and authenticated. See `gws-workspace` skill.

```bash
gws chat <resource> <method> [flags]
```

## Quick Commands

### Send a Message

```bash
gws chat +send --space <NAME> --text <TEXT>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--space` | Yes | Space name (e.g. `spaces/AAAAxxxx`) |
| `--text` | Yes | Message text (plain text) |

Use `gws chat spaces list` to find space names. For cards or threaded replies, use the raw API.

> **Write command** -- confirm with the user before executing.

## Raw API Resources

### spaces

- `completeImport`, `create`, `delete`, `findDirectMessage`, `get`, `list`, `patch`, `search`, `setup`
- `members` -- create, delete, get, list, patch
- `messages` -- create, delete, get, list, patch, update
  - `reactions` -- create, delete, list
  - `attachments` -- get
- `spaceEvents` -- get, list

### users / customEmojis / media

- `users.spaces` -- getSpaceReadState, updateSpaceReadState
- `customEmojis` -- create, delete, get, list
- `media` -- download, upload

## Discovering Commands

```bash
gws chat --help
gws schema chat.spaces.list
gws schema chat.spaces.messages.create
```

## Common Patterns

```bash
# List all spaces
gws chat spaces list --fields "spaces(name,displayName,type)"

# List messages in a space
gws chat spaces messages list \
  --params '{"parent": "spaces/AAAAxxxx"}' \
  --fields "messages(name,text,sender,createTime)"

# Send a message (raw API)
gws chat spaces messages create \
  --params '{"parent": "spaces/AAAAxxxx"}' \
  --json '{"text": "Deploy complete."}'

# Find a direct message space
gws chat spaces findDirectMessage \
  --params '{"name": "users/USER_ID"}'
```

## Examples

### Example 1: Basic operation

**User says:** "Send a Google Chat message"

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
