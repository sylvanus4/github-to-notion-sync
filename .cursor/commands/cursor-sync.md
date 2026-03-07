## Cursor Sync

Synchronize `.cursor/` assets (commands, skills, rules) from this project to multiple target projects. Uses rsync with checksum-based diffing — only new and changed files are copied; target-specific files are preserved.

### Usage

```
# Sync all to all targets
/cursor-sync

# Sync to a specific target (by alias)
/cursor-sync --targets ai-template

# Sync to a specific target (by GitHub repo)
/cursor-sync --repo thakicloud/ai-template

# Preview only (no changes)
/cursor-sync --dry-run

# Sync only specific directories
/cursor-sync --scope commands
/cursor-sync --scope skills,rules

# Combine arguments (--targets and --repo are mutually exclusive)
/cursor-sync --targets ai-template --dry-run --scope commands
/cursor-sync --repo thakicloud/ai-template --dry-run --scope commands
```

### Workflow

1. **Resolve** — Read target paths from sync config, parse arguments
2. **Validate** — Check each target directory exists
3. **Preview** — Dry-run rsync to show new/updated/unchanged files per target
4. **Execute** — Apply sync (skip if `--dry-run`)
5. **Report** — Summary of changes per target

### Execution

Read and follow the `cursor-sync` skill (`.cursor/skills/cursor-sync/SKILL.md`) for target configuration, rsync flags, and error handling.

### Examples

Sync everything after updating skills:
```
/cursor-sync
```

Check what would change before syncing:
```
/cursor-sync --dry-run
```

Sync only commands to one project (by alias):
```
/cursor-sync --targets ai-model-event-stock-analytics --scope commands
```

Sync to a specific GitHub repo:
```
/cursor-sync --repo thakicloud/ai-template
```
