# Paperclip CLI Reference

Run from `~/work/thakicloud/paperclip/` with `pnpm paperclipai`.

## Global Flags

| Flag | Description |
|------|-------------|
| `--data-dir <path>` | Isolate local state away from `~/.paperclip` |
| `--api-base <url>` | Override API base URL |
| `--api-key <token>` | Override API key |
| `--company-id <id>` | Override company ID |
| `--context <name>` | Use named context profile |
| `--profile <name>` | Alias for `--context` |
| `--json` | JSON output |

## Instance Commands

```bash
pnpm paperclipai onboard [--yes]                    # First-run setup wizard
pnpm paperclipai run [--instance <id>]               # Start server
pnpm paperclipai doctor [--repair]                   # Diagnostics
pnpm paperclipai configure --section <section>       # Configure (server|storage|llm|database|logging|secrets)
pnpm paperclipai env                                 # Print env vars
pnpm paperclipai allowed-hostname <hostname>         # Allow hostname (authenticated mode)
pnpm paperclipai db:backup                           # Manual database backup
pnpm paperclipai auth bootstrap-ceo                  # Bootstrap first admin
```

## Context Commands

```bash
pnpm paperclipai context set --api-base <url> --company-id <id>
pnpm paperclipai context set --api-key-env-var-name PAPERCLIP_API_KEY
pnpm paperclipai context show
pnpm paperclipai context list
pnpm paperclipai context use <profile-name>
```

## Company Commands

```bash
pnpm paperclipai company list
pnpm paperclipai company get <company-id>
pnpm paperclipai company delete <id-or-prefix> --yes --confirm <same-id-or-prefix>
```

## Issue Commands

```bash
pnpm paperclipai issue list --company-id <id> [--status todo,in_progress] [--assignee-agent-id <agent-id>] [--match text]
pnpm paperclipai issue get <issue-id-or-identifier>
pnpm paperclipai issue create --company-id <id> --title "..." [--description "..."] [--status todo] [--priority high]
pnpm paperclipai issue update <issue-id> [--status in_progress] [--comment "..."]
pnpm paperclipai issue comment <issue-id> --body "..." [--reopen]
pnpm paperclipai issue checkout <issue-id> --agent-id <agent-id> [--expected-statuses todo,backlog,blocked]
pnpm paperclipai issue release <issue-id>
```

## Agent Commands

```bash
pnpm paperclipai agent list --company-id <id>
pnpm paperclipai agent get <agent-id>
```

## Approval Commands

```bash
pnpm paperclipai approval list --company-id <id> [--status pending]
pnpm paperclipai approval get <approval-id>
pnpm paperclipai approval create --company-id <id> --type hire_agent --payload '{"name":"..."}' [--issue-ids <id1,id2>]
pnpm paperclipai approval approve <approval-id> [--decision-note "..."]
pnpm paperclipai approval reject <approval-id> [--decision-note "..."]
pnpm paperclipai approval request-revision <approval-id> [--decision-note "..."]
pnpm paperclipai approval resubmit <approval-id> [--payload '{"...":"..."}']
pnpm paperclipai approval comment <approval-id> --body "..."
```

## Activity Commands

```bash
pnpm paperclipai activity list --company-id <id> [--agent-id <id>] [--entity-type issue] [--entity-id <id>]
```

## Dashboard Commands

```bash
pnpm paperclipai dashboard get --company-id <id>
```

## Heartbeat Commands

```bash
pnpm paperclipai heartbeat run --agent-id <agent-id> [--api-base <url>] [--api-key <token>]
```
