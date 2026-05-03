# Claude Sync

N-repo bidirectional sync of `.claude/` assets (rules, commands, skills, hooks) across all 5 ThakiCloud repositories. Research acts as the merge hub: pull phase absorbs changes from all 4 target repos using newest-wins (`-u` flag), then push phase distributes the merged result to all targets. Any `.claude/` change in any repo propagates to all others in one run.

Use when the user runs `/claude-sync`, asks to "sync claude assets", "sync claude rules across projects", "push claude skills to other repos", or "claude 스킬 동기화". Do NOT use for syncing `.cursor/` assets (use `cursor-sync`), deploying code, or general file copy operations.

---

## Sync Scope

| Directory | Description |
|-----------|-------------|
| `.claude/rules/` | Claude Code rules (always-applied, agent-requestable) |
| `.claude/commands/` | Claude Code slash commands |
| `.claude/skills/` | Claude Code agent skills |
| `.claude/hooks/` | Claude Code lifecycle hooks |

Root-level `.claude/*.json` and `.claude/*.md` files (e.g., `settings.json`, `settings.local.json`) are **excluded** from sync — they contain machine-specific or project-specific configuration.

## Target Repositories

Hub: `research`

Targets (synced bidirectionally through the hub):

| Alias | Path (relative to `{BASE}`) |
|-------|---------------------------|
| `github-to-notion-sync` | `github-to-notion-sync` |
| `ai-platform-strategy` | `ai-platform-strategy` |
| `ai-model-event-stock-analytics` | `ai-model-event-stock-analytics` |
| `ai-template` | `ai-template` |

`{BASE}` resolves at runtime:
- `$HOME/work/thakicloud` if that directory exists
- `$HOME/thaki` otherwise

## Workflow

### Step 1: Environment Detection

```bash
if [ -d "$HOME/work/thakicloud" ]; then
  BASE="$HOME/work/thakicloud"
else
  BASE="$HOME/thaki"
fi
```

### Step 2: Pull Phase (Target → Research)

For each of the 4 target repos, pull `.claude/` assets into the research hub using `rsync -au` (archive + update, newest-wins by mtime).

```bash
EXCLUDES="--exclude node_modules/ --exclude __pycache__/ --exclude .curator/ --exclude state/ --exclude .archive/"

for TARGET in github-to-notion-sync ai-platform-strategy ai-model-event-stock-analytics ai-template; do
  for DIR in rules commands skills hooks; do
    SRC="$BASE/$TARGET/.claude/$DIR/"
    DST="$BASE/research/.claude/$DIR/"
    if [ -d "$SRC" ]; then
      mkdir -p "$DST"
      rsync -au $EXCLUDES "$SRC" "$DST"
    fi
  done
done
```

**Before each rsync**: use `comm` to detect new or removed files:

```bash
comm -23 <(ls "$SRC" 2>/dev/null | sort) <(ls "$DST" 2>/dev/null | sort)
```

This shows files present in source but not in destination (new files to be pulled).

### Step 3: Push Phase (Research → All Targets)

Push the merged research hub to all 4 targets using `rsync -ac` (archive + checksum, content-identical files skipped).

```bash
EXCLUDES="--exclude node_modules/ --exclude __pycache__/ --exclude .curator/ --exclude state/ --exclude .archive/"

for TARGET in github-to-notion-sync ai-platform-strategy ai-model-event-stock-analytics ai-template; do
  for DIR in rules commands skills hooks; do
    SRC="$BASE/research/.claude/$DIR/"
    DST="$BASE/$TARGET/.claude/$DIR/"
    if [ -d "$SRC" ]; then
      mkdir -p "$DST"
      rsync -ac $EXCLUDES "$SRC" "$DST"
    fi
  done
done
```

### Step 4: Final Verification & Report

Verify all 5 repos have identical file counts for each synced directory:

```bash
for DIR in rules commands skills hooks; do
  echo "=== .claude/$DIR ==="
  for REPO in research github-to-notion-sync ai-platform-strategy ai-model-event-stock-analytics ai-template; do
    COUNT=$(find "$BASE/$REPO/.claude/$DIR" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  $REPO: $COUNT files"
  done
done
```

Report format:

```
Claude Sync Complete
- rules/: 12 files (5 repos aligned)
- commands/: 8 files (5 repos aligned)
- skills/: 45 files (5 repos aligned)
- hooks/: 3 files (5 repos aligned)
- New files pulled: X
- Files pushed: Y
```

## Implementation Rules

### Shell Command Rules

- Use `rsync` for all file sync operations
- Use `comm` for diff comparison (macOS `rsync` lacks per-file output)
- Use `mkdir -p` before rsync to ensure target dirs exist
- Use `find ... -type f | wc -l` for file counting

### rsync Flag Reference

| Phase | Flags | Purpose |
|-------|-------|---------|
| Pull  | `-au` | archive + update (newer wins by mtime) |
| Push  | `-ac` | archive + checksum (content-identical files skipped) |

**Forbidden flags**: `-i` (no useful output on openrsync), `-v` (no file list on openrsync), `--delete` (never remove target-only files)

### Excluded Patterns

Always exclude from sync:
- `node_modules/`
- `__pycache__/`
- `.curator/` (skill curator state, project-specific)
- `state/` (skill runtime state, project-specific)
- `.archive/` (archived skills, project-specific)

### Root-Level File Exclusion

Files directly under `.claude/` (not in subdirectories) are NOT synced:
- `settings.json` — project-specific MCP and feature config
- `settings.local.json` — machine-specific overrides
- `CLAUDE.md` — project-specific instructions (synced via git, not rsync)

### Direction Confirmation

Before bulk sync, confirm direction with user if invoked interactively:
- "Pull: {target} → research" for pull phase
- "Push: research → {target}" for push phase

When invoked by `eod-ship` or `sod-ship`, run without confirmation.

## Relationship with cursor-sync

`cursor-sync` already syncs `.claude/skills/` as part of its workflow. When both `cursor-sync` and `claude-sync` run in the same pipeline (eod-ship, sod-ship), the overlap on `.claude/skills/` is harmless — `rsync -ac` is idempotent and checksum-based, so re-syncing identical files has zero effect.

`claude-sync` additionally syncs `.claude/rules/`, `.claude/commands/`, and `.claude/hooks/` which `cursor-sync` does not cover.
