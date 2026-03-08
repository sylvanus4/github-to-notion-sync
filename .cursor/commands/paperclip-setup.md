## Paperclip Setup

Install, configure, and deploy the Paperclip AI agent orchestration platform.

### Usage

```
/paperclip-setup install                # clone and install Paperclip
/paperclip-setup start                  # start dev server
/paperclip-setup stop                   # stop dev server
/paperclip-setup configure <section>    # configure (server|storage|llm|database)
/paperclip-setup doctor                 # run diagnostics
/paperclip-setup context                # show/set context profile
/paperclip-setup docker                 # docker compose setup
```

### Workflow

1. **Parse action** — determine operation from `$ARGUMENTS`
2. **Check prerequisites** — Node.js 20+, pnpm 9.15+
3. **Execute** — run appropriate setup command
4. **Verify** — health check and diagnostics

### Execution

Read and follow the `paperclip-setup` skill (`.cursor/skills/paperclip-setup/SKILL.md`) for installation methods, deployment modes, and troubleshooting.

### Examples

Fresh installation:
```
/paperclip-setup install
```

Start the server:
```
/paperclip-setup start
```

Run diagnostics:
```
/paperclip-setup doctor
```
