## RTK Token Analytics

View RTK token savings analytics and discover optimization opportunities.

### Usage

```
/rtk [gain|discover|status]
```

### Subcommands

| Subcommand | Description |
|-----------|-------------|
| `gain` | Show token savings summary with ASCII graph (default) |
| `discover` | Find commands that could benefit from RTK but aren't using it |
| `status` | Check RTK version, configuration, and installation health |

### Workflow

1. **Default (`/rtk` or `/rtk gain`)**: Run `rtk gain --graph` and `rtk gain --daily` to show visual token savings summary
2. **Discover (`/rtk discover`)**: Run `rtk discover --all --since 7` to find missed optimization opportunities across all projects in the last 7 days
3. **Status (`/rtk status`)**: Run `rtk --version`, check config at `~/Library/Application Support/rtk/config.toml`, and verify PATH

### Execution

Read and follow the `rtk` skill (`.cursor/skills/rtk/SKILL.md`) for detailed instructions, configuration options, and troubleshooting.

### Examples

Check overall savings:
```
/rtk
```

Find optimization opportunities:
```
/rtk discover
```

Verify RTK installation:
```
/rtk status
```
