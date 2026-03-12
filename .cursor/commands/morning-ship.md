## Morning Ship

Start-of-day multi-project pipeline: git pull all 5 managed repos, run Google Workspace briefing (calendar + Gmail triage), run the daily stock analysis pipeline, then post a consolidated morning briefing to Slack `#효정-할일`.

### Usage

```
# Full pipeline (pull + google + stock + Slack)
/morning-ship

# Skip git pull, run briefing only
/morning-ship --skip-pull

# Skip Google daily (calendar + Gmail)
/morning-ship --skip-google

# Skip daily stock pipeline
/morning-ship --skip-stock

# Pull specific projects only (comma-separated)
/morning-ship --targets ai-platform-webui,research

# Preview only (no git pull, no triage, no pipeline)
/morning-ship --dry-run

# Skip Slack notification
/morning-ship --no-slack
```

### Workflow

1. **Git Sync** — Pull latest changes from all 5 managed repos (ai-platform-webui via `git pull origin tmp`)
2. **Google Daily** — Calendar briefing + Gmail triage
3. **Stock Pipeline** — Run daily stock analysis (`today --skip-slack`)
4. **Slack** — Post consolidated morning briefing to `#효정-할일`
5. **Report** — Display summary in chat

### Execution

Read and follow the `morning-ship` skill (`.cursor/skills/morning-ship/SKILL.md`) for pipeline phases, project registry, and error handling.

### Examples

Full morning pipeline:
```
/morning-ship
```

Pull repos only (skip briefing and stock):
```
/morning-ship --skip-google --skip-stock
```

Run briefing without pulling repos:
```
/morning-ship --skip-pull
```

Pull only specific projects:
```
/morning-ship --targets ai-platform-webui,research
```

Preview what would happen:
```
/morning-ship --dry-run
```
