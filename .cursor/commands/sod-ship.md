## SOD Ship

Start-of-day git sync pipeline: commit dirty working directories, push unpushed commits, and pull remote changes for all 5 managed projects. Ensures every repo is clean and in sync before starting work.

### Usage

```
# Full pipeline (commit + push + pull + Slack)
/sod-ship

# Pull only, skip committing/pushing local changes
/sod-ship --skip-push

# Commit and push only, skip pulling remote
/sod-ship --skip-pull

# Process specific projects only (comma-separated)
/sod-ship --targets research,ai-template

# Preview only (show status, no git operations)
/sod-ship --dry-run

# Skip Slack notification
/sod-ship --no-slack
```

### Workflow

1. **Pre-flight Scan** — Check dirty files, unpushed commits, and remote status for all 5 repos
2. **Ship Local** — Domain-split commit dirty repos, push unpushed commits (ai-platform-webui via `tmp`)
3. **Pull Remote** — Pull latest from remote, resolve conflicts via rebase fallback
4. **Verify Sync** — Confirm all projects are SYNCED / PARTIAL / FAILED
5. **Slack + Report** — Post summary to `#효정-할일` and display in chat

### Execution

Read and follow the `sod-ship` skill (`.cursor/skills/sod-ship/SKILL.md`) for pipeline phases, project registry, and error handling.

### Examples

Full morning sync:
```
/sod-ship
```

Pull repos only (already pushed from other machine):
```
/sod-ship --skip-push
```

Push only before switching computers:
```
/sod-ship --skip-pull
```

Sync only specific projects:
```
/sod-ship --targets ai-platform-webui,research
```

Preview what would happen:
```
/sod-ship --dry-run
```
