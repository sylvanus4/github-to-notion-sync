---
name: cursor-sync
description: >-
  Synchronize .cursor/ assets (commands, skills, rules) from the current
  project to multiple target projects using rsync with checksum-based diffing.
  Only new and changed files are copied; target-specific files are preserved.
  Use when the user runs /cursor-sync, asks to "sync skills", "sync commands
  across projects", or "push cursor config to other repos". Do NOT use for
  syncing non-.cursor files, deploying code, or general file copy operations.
  Korean triggers: "커서 동기화", "스킬 동기화".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Cursor Sync — Multi-Project .cursor/ Asset Synchronization

Sync `.cursor/{commands,skills,rules}` from this project (source of truth) to target projects. Uses `rsync --checksum` so only new and modified files are transferred; target-specific files remain untouched.

## Configuration

- **Source**: The current project's `.cursor/` directory (+ extra directories)
- **Sync directories**: `commands/`, `skills/`, `rules/`
- **Extra sync directories**: `docs/skill-guides/` (bidirectional, with per-target path mapping)
- **Target projects**: See [references/sync-targets.md](references/sync-targets.md)

## Usage

```
/cursor-sync                              # sync all dirs to all targets
/cursor-sync --targets ai-template        # sync to one specific target (by alias)
/cursor-sync --repo thakicloud/ai-template # sync to one specific target (by GitHub repo)
/cursor-sync --dry-run                    # preview only, no file changes
/cursor-sync --scope commands             # sync only commands/
/cursor-sync --scope skills,rules         # sync multiple specific dirs
/cursor-sync --scope skill-guides             # sync only docs/skill-guides/ (bidirectional)
/cursor-sync --targets ai-template --dry-run --scope commands
/cursor-sync --repo thakicloud/ai-template --dry-run --scope commands
```

Arguments can be combined freely. `--targets` and `--repo` are mutually exclusive — use one or the other, not both. Defaults: all dirs (including skill-guides), all targets, execute (not dry-run).

## Workflow

### Step 1: Resolve Configuration

1. Read target project paths from [references/sync-targets.md](references/sync-targets.md)
2. Parse user arguments for `--targets`, `--repo`, `--scope`, `--dry-run`
3. If both `--targets` and `--repo` are provided, report an error: these flags are mutually exclusive
4. If `--repo` is provided (in `org/repo` format), look up the matching row in the `Repo` column of sync-targets.md and resolve to the corresponding local path. If no match is found, list all registered repos and abort
5. Determine the source `.cursor/` directory (workspace root)

### Step 2: Validate Targets (multi-path fallback)

Each target has two candidate paths (회사/집). For each target, try both paths in order and use the first one that exists:

```bash
for CANDIDATE in "PATH_WORK" "PATH_HOME"; do
  [ -d "$CANDIDATE" ] && TARGET="$CANDIDATE" && break
done
[ -z "$TARGET" ] && echo "SKIP: neither path exists for <alias>"
```

If neither path exists, warn the user and skip the target. Continue with remaining targets.

Ensure `.cursor/` exists in each resolved target (create if missing):

```bash
mkdir -p TARGET_PATH/.cursor/{commands,skills,rules}
```

### Step 3: Dry-Run Preview

Always run a dry-run first to show what will change:

```bash
rsync -acvi --dry-run SOURCE/.cursor/commands/ TARGET/.cursor/commands/
rsync -acvi --dry-run SOURCE/.cursor/skills/  TARGET/.cursor/skills/
rsync -acvi --dry-run SOURCE/.cursor/rules/   TARGET/.cursor/rules/
```

Parse the output to categorize changes:
- Lines starting with `>f+++++++` — new files
- Lines starting with `>f.s` or `>fc.` — changed files
- No output — everything up to date

Present a summary per target:

```
Target: ai-template
  commands/: 3 new, 2 updated, 45 unchanged
  skills/:   1 new, 0 updated, 22 unchanged
  rules/:    0 new, 1 updated, 14 unchanged
```

If `--dry-run` flag was set, stop here.

### Step 4: Execute Sync

After showing the preview, execute the actual sync:

```bash
rsync -acvi SOURCE/.cursor/commands/ TARGET/.cursor/commands/
rsync -acvi SOURCE/.cursor/skills/  TARGET/.cursor/skills/
rsync -acvi SOURCE/.cursor/rules/   TARGET/.cursor/rules/
```

Flags:
- `-a` (archive): preserve structure, permissions, timestamps
- `-c` (checksum): compare by content hash, not timestamp
- `-v` (verbose): list transferred files
- `-i` (itemize-changes): show per-file change details

**No `--delete` flag** — files that exist only in the target are never removed.

### Step 4b: Sync Extra Directories (bidirectional)

For directories listed in the "Extra Sync Directories" table in sync-targets.md:

1. Look up the source path and per-target path mapping
2. **Push** (source → target): `rsync -acvi SOURCE_PATH/ TARGET_PATH/`
3. **Pull** (target → source): `rsync -acvi TARGET_PATH/ SOURCE_PATH/`

Path mapping example for `skill-guides`:
- Source: `docs/skill-guides/` (relative to workspace root)
- Target `ai-template`: `skill-guides/` (relative to target root — different path!)
- Target `ai-platform-webui`: `docs/skill-guides/` (same path)

```bash
# Push: source → ai-template
rsync -acvi SOURCE_ROOT/docs/skill-guides/ TARGET_ROOT/skill-guides/

# Pull: ai-template → source
rsync -acvi TARGET_ROOT/skill-guides/ SOURCE_ROOT/docs/skill-guides/
```

Only targets that have a mapping row in the extra directories table are synced. Targets without a mapping are skipped for that scope.

### Step 5: Report

Present a final summary:

```
Cursor Sync Report
==================
Source: /path/to/X-to-Slack/.cursor/
Targets synced: 4/4

Per-target results:
  github-to-notion-sync:          5 new, 2 updated
  ai-platform-webui:              3 new, 1 updated
  ai-model-event-stock-analytics: 5 new, 2 updated
  ai-template:                    0 new, 1 updated

Total: 13 new files, 6 updated files
Skipped targets: 0
```

## Examples

### Example 1: Full sync to all targets

User runs `/cursor-sync` after updating several skills and commands.

Actions:
1. Read sync-targets.md, resolve 4 target paths
2. Validate all 4 targets exist
3. Dry-run preview shows 8 new files, 3 updated across targets
4. Execute rsync for each target
5. Report: 4/4 targets synced, 11 total changes

### Example 2: Preview-only sync to one target

User runs `/cursor-sync --targets ai-template --dry-run` to check what would change.

Actions:
1. Resolve ai-template path only
2. Validate target exists
3. Dry-run shows 2 new commands, 1 updated skill
4. Stop (dry-run mode) — no files written
5. Report: preview complete, user can re-run without --dry-run to apply

### Example 3: Sync by GitHub repo identifier

User runs `/cursor-sync --repo thakicloud/ai-template --dry-run` to preview changes for a specific repo.

Actions:
1. Look up `thakicloud/ai-template` in the `Repo` column of sync-targets.md
2. Resolve to local path `/Users/hanhyojung/work/thakicloud/ai-template`
3. Validate target exists
4. Dry-run shows 2 new skills, 1 updated command
5. Stop (dry-run mode) — no files written

### Example 4: Scoped sync

User runs `/cursor-sync --scope commands --targets ai-model-event-stock-analytics`.

Actions:
1. Only sync `commands/` directory
2. Dry-run: 3 new commands, 1 updated
3. Execute: rsync commands/ only
4. Report: 4 changes applied to 1 target

## Error Handling

| Scenario | Action |
|----------|--------|
| Target directory does not exist | Warn and skip; continue with other targets |
| rsync not installed | Inform user to install rsync (pre-installed on macOS/Linux) |
| Permission denied on target | Report the error, suggest `chmod` or running with elevated permissions |
| No changes detected | Report "all targets up to date" |
| Partial failure (some targets fail) | Sync remaining targets, report failures at the end |
| `--repo` and `--targets` both provided | Report error: flags are mutually exclusive; use one or the other |
| `--repo` value not found in registry | List all registered repos from sync-targets.md and abort |

## Troubleshooting

- **"Target not found"**: Verify the path in `references/sync-targets.md`; the project may have moved
- **"Permission denied"**: Check file ownership on the target `.cursor/` directory
- **Unexpected overwrites**: Use `--dry-run` first to preview; rsync uses checksums, not timestamps
- **Missing target-specific files**: This skill never deletes target-only files; if files are missing, check git history in the target project
