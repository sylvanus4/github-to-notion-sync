## Paperclip Agent

Create, configure, and operate Paperclip agents — hire, heartbeat, budget, and lifecycle management.

### Usage

```
/paperclip-agent list                                  # list all agents
/paperclip-agent get <agent-id>                        # agent details
/paperclip-agent create "Agent Name" --role engineer   # hire new agent
/paperclip-agent heartbeat <agent-id>                  # run heartbeat
/paperclip-agent pause <agent-id>                      # pause agent
/paperclip-agent resume <agent-id>                     # resume agent
/paperclip-agent budget <agent-id> --amount 500        # set budget ($5.00)
```

### Workflow

1. **Parse action** — determine operation from `$ARGUMENTS`
2. **Discover config** — for agent creation, fetch adapter docs and icons
3. **Execute** — run CLI command or REST call
4. **Handle governance** — if hire requires approval, track and report

### Execution

Read and follow the `paperclip-agents` skill (`.cursor/skills/paperclip-agents/SKILL.md`) for adapter types, heartbeat flow, and budget rules.

### Examples

Hire a Claude Code agent:
```
/paperclip-agent create "frontend-dev" --role engineer --adapter claude_local
```

Run a heartbeat manually:
```
/paperclip-agent heartbeat <agent-id>
```
