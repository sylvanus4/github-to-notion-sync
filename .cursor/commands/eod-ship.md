## EOD Ship

End-of-day multi-project shipping pipeline: cursor-sync assets, release-ship the current project and 5 managed projects, then post a consolidated summary to Slack `#효정-할일`.

### Usage

```
# Full pipeline (sync + ship all + Slack notify)
/eod-ship

# Skip cursor-sync, ship only
/eod-ship --skip-sync

# Ship specific projects only (comma-separated)
/eod-ship --targets research,ai-template

# Preview only (no commits, no push, no Slack)
/eod-ship --dry-run

# Skip Slack notification
/eod-ship --no-slack
```

### Workflow

1. **Cursor Sync** — Sync `.cursor/` assets to all target projects
2. **Ship Current** — Release-ship the current working directory
3. **Ship 5 Projects** — Release-ship each managed project sequentially
4. **Slack** — Post consolidated report to `#효정-할일`
5. **Report** — Display summary in chat

### Execution

Read and follow the `eod-ship` skill (`.cursor/skills/eod-ship/SKILL.md`) for pipeline phases, project registry, and error handling.

### Examples

Wrap up everything at end of day:
```
/eod-ship
```

Ship without syncing cursor assets:
```
/eod-ship --skip-sync
```

Ship only specific projects:
```
/eod-ship --targets research
```

Preview what would be shipped:
```
/eod-ship --dry-run
```
