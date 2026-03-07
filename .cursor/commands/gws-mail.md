## Gmail Operations

Send emails, triage inbox, and manage Gmail via the gws CLI.

### Usage

```
/gws-mail [action] [args]
```

Actions:
- `send` -- send an email via `gws gmail +send --to <email> --subject <subject> --body <body>`
- `triage` -- show unread inbox via `gws gmail +triage`
- `search` -- search messages via `gws gmail users messages list --params '{"userId": "me", "q": "<query>"}'`

### Examples

```
/gws-mail send --to alice@company.com --subject "Q1 Report" --body "Please find the Q1 report attached."
/gws-mail triage
/gws-mail search "from:boss subject:urgent"
```

### Execution

Read and follow the `gws-gmail` skill (`.cursor/skills/gws-gmail/SKILL.md`) for full CLI reference, raw API resources, and common patterns.
