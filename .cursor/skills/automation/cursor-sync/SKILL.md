---
name: cursor-sync
description: >-
  N-repo bidirectional sync of .cursor/ assets (commands, skills, rules) across
  all 5 ThakiCloud repositories. Research acts as the merge hub: pull phase
  absorbs changes from all 4 target repos using newest-wins (-u flag), then
  push phase distributes the merged result to all targets. Any .cursor/ change
  in any repo propagates to all others in one run. Use when the user runs
  /cursor-sync, asks to "sync skills", "sync commands across projects", or
  "push cursor config to other repos". Do NOT use for syncing non-.cursor
  files, deploying code, or general file copy operations.
metadata:
  author: thaki
  version: 2.0.0
---

# Cursor Sync — N-Repo .cursor/ Asset Synchronization

Research는 5개 레포의 `.cursor/` 에셋 **머지 허브**입니다. 5개 레포 중 어디서 변경이 발생하든, research에서 `/cursor-sync`를 한 번 실행하면 모든 레포에 전파됩니다.

- **Pull Phase**: 4개 타겟 레포 → research (`rsync -au`, 최신 파일 우선)
- **Push Phase**: research → 4개 타겟 레포 (`rsync -ac`, checksum 기반)

## 흐름 다이어그램

```
[github-to-notion-sync]        ─┐
[ai-platform-strategy]            ─┼─ rsync -au ──▶ [research] ─── rsync -ac ──▶ [github-to-notion-sync]
[ai-model-event-stock-analytics]─┤  (Pull Phase)   (허브)    (Push Phase)     [ai-platform-strategy]
[ai-template]                  ─┘                                             [ai-model-event-stock-analytics]
                                                                              [ai-template]
```

## Platform Note: macOS openrsync

macOS에 내장된 `/usr/bin/rsync`는 **openrsync** (protocol v29) 이며, GNU rsync와 다릅니다:

- `-i` (itemize-changes): `>f+++++++` 형태의 per-file 출력을 하지 않음
- `-v` (verbose): 개별 전송 파일 목록을 출력하지 않음
- `--dry-run`: 변경 파일 목록을 보여주지 않음 (바이트 요약만 출력)

따라서 이 스킬은 **`comm` 기반 diff 비교**로 새 파일을 감지하고, rsync는 **전송 전용**으로만 사용합니다.

## Configuration

- **Hub (source of truth after merge)**: `{BASE}/research/.cursor/`
- **Sync directories**: `commands/`, `skills/`, `rules/`
- **Target projects**: See [references/sync-targets.md](references/sync-targets.md)
- **Pull sources**: All 4 targets are `Bidirectional = yes`
- **Environment detection**: See [references/sync-targets.md — Environment Configuration](references/sync-targets.md#environment-configuration)

### Environment Detection

`{BASE}` is resolved at runtime before any other step:

```bash
if [ -d "$HOME/work/thakicloud/research/.cursor" ]; then
  BASE="$HOME/work/thakicloud"
  ENV_LABEL="office"
elif [ -d "$HOME/thaki/research/.cursor" ]; then
  BASE="$HOME/thaki"
  ENV_LABEL="home"
else
  echo "ERROR: research/.cursor not found in either candidate:"
  echo "  - $HOME/work/thakicloud/research/.cursor"
  echo "  - $HOME/thaki/research/.cursor"
  exit 1
fi
echo "Environment: $ENV_LABEL (BASE=$BASE)"
```

All subsequent paths use `$BASE` — never hardcoded absolute paths.

## Usage

```
/cursor-sync                               # pull from all 4 repos, then push to all (N-repo sync)
/cursor-sync --dry-run                     # preview only: show diff counts, no file changes
/cursor-sync --pull-only                   # pull from all 4 repos into research only, no push
/cursor-sync --no-pull                     # skip pull phase; push research to all targets only
/cursor-sync --scope commands              # limit sync to commands/ only
/cursor-sync --scope skills,rules          # limit sync to skills/ and rules/
/cursor-sync --targets ai-template         # push to one specific target only (pull phase skipped)
/cursor-sync --repo thakicloud/ai-template # push to one specific target by repo name (pull phase skipped)
/cursor-sync --skill-groups review,infra   # override: push only these skill subdirectories (applies to all targets)
/cursor-sync --all-skills                  # override: push ALL skill groups to every target (ignore per-repo whitelist)
```

Arguments can be combined freely. `--targets` and `--repo` are mutually exclusive. Defaults: all dirs, all targets, execute (not dry-run).

When `--targets` or `--repo` is specified (single-target mode), the pull phase is **skipped** automatically.

### Skill Group Filtering

Skills are organized into subdirectories under `.cursor/skills/` (e.g., `trading/`, `review/`, `infra/`). Each target repo has a **skill group whitelist** defined in [references/sync-targets.md](references/sync-targets.md). During push, only whitelisted skill groups are synced to each target.

- Default behavior: use per-repo whitelist from sync-targets.md
- `--skill-groups review,infra`: override — push only these groups to all targets in this run
- `--all-skills`: override — push ALL skill groups to every target (full sync, ignores whitelist)
- Root-level items in `.cursor/skills/` (files like `README.md`, `SKILL.md`, and shared companion directories -- any subdirectory containing no `SKILL.md` at any depth, e.g. `docs/`, `references/`, `scripts/`, `templates/`) are always synced to all targets

## Workflow

### Step 0: Pull Phase (N-Repo merge)

> Skip this step if `--targets`, `--repo`, or `--no-pull` is specified.

For each target in the order listed in sync-targets.md:

#### 0a. Detect new files (comm-based diff)

For each sync directory (`commands/`, `skills/`, `rules/`, `.claude/skills/`), find files that exist in the target but NOT in research:

```bash
comm -23 <(ls TARGET/.cursor/DIR/ | sort) <(ls RESEARCH/.cursor/DIR/ | sort)
```

For `skills/`, also check each skill group subdirectory individually:

```bash
for group in $(ls -d TARGET/.cursor/skills/*/ 2>/dev/null | xargs -I{} basename {}); do
  comm -23 <(ls TARGET/.cursor/skills/$group/ 2>/dev/null | sort) <(ls RESEARCH/.cursor/skills/$group/ 2>/dev/null | sort)
done
```

This gives exact new file counts per target per directory.

#### 0b. Execute pull (rsync -au)

```bash
EXCLUDES="--exclude node_modules/ --exclude __pycache__/"
rsync -au $EXCLUDES TARGET/.cursor/commands/ RESEARCH/.cursor/commands/
rsync -au $EXCLUDES TARGET/.cursor/skills/   RESEARCH/.cursor/skills/
rsync -au $EXCLUDES TARGET/.cursor/rules/    RESEARCH/.cursor/rules/
rsync -au $EXCLUDES TARGET/.claude/skills/   RESEARCH/.claude/skills/
```

Pull always syncs ALL skill groups from a target into research (the merge hub absorbs everything). `.claude/skills/` is synced as a flat directory (no group filtering).

Flags:
- `-a` (archive): preserve structure, permissions, timestamps
- `-u` (update): only overwrite if source file is newer (mtime comparison)

The `-u` flag ensures research's own newer edits are NOT overwritten. New files (not in research) are always pulled regardless of mtime.

#### 0c. Report per target

```
Pull Phase (N-Repo merge)
=========================
  github-to-notion-sync:          commands/: +5 new
  ai-platform-strategy:              skills/: +2 new
  ai-model-event-stock-analytics: 0 new files
  ai-template:                    0 new files
  Total new files pulled: 7
```

After this step, research is the authoritative push source containing the union of all repos.

### Step 1: Resolve Configuration

1. Read target project paths from [references/sync-targets.md](references/sync-targets.md)
2. Parse user arguments for `--targets`, `--repo`, `--scope`, `--dry-run`, `--pull-only`, `--no-pull`
3. If both `--targets` and `--repo` are provided, report an error: these flags are mutually exclusive
4. If `--repo` is provided (in `org/repo` format), look up the matching row in the `Repo` column and resolve to the local path. If no match, list all registered repos and abort
5. Determine the hub `.cursor/` directory (workspace root)
6. If `--pull-only` was set, stop after Step 0

### Step 2: Validate Targets

For each target project, verify the directory exists:

```bash
[ -d "TARGET_PATH" ] && echo "OK" || echo "MISSING: TARGET_PATH"
```

If a target is missing, warn and skip it. Ensure `.cursor/` subdirs exist:

```bash
mkdir -p TARGET_PATH/.cursor/{commands,skills,rules}
```

### Step 3: Diff Preview

For each target, use `comm` to show differences.

#### commands/ and rules/ (full diff)

```bash
comm -23 <(ls RESEARCH/.cursor/DIR/ | sort) <(ls TARGET/.cursor/DIR/ | sort)
comm -13 <(ls RESEARCH/.cursor/DIR/ | sort) <(ls TARGET/.cursor/DIR/ | sort)
```

#### skills/ (group-filtered diff)

Determine which skill groups apply to this target (same logic as Step 4b). For each allowed group, compare its contents:

```bash
comm -23 <(ls RESEARCH/.cursor/skills/GROUP/ | sort) <(ls TARGET/.cursor/skills/GROUP/ | sort 2>/dev/null)
```

Present a summary:

```
Push Preview
============
Target: ai-template (groups: workflow, anthropic, ce, ecc, standalone)
  commands/:          5 to push, 0 target-only
  skills/workflow/:   2 to push, 0 target-only
  skills/anthropic/:  0 to push, 0 target-only
  skills/ce/:         1 to push, 0 target-only
  skills/ecc/:        0 to push, 0 target-only
  skills/standalone/: 3 to push, 2 target-only (preserved)
  rules/:             0 to push, 0 target-only
  (skipped groups: trading, alphaear, pipeline, pm, agency, kwp, hf, gws, nlm, infra, review, research, frontend, role, omc, planning, automation, notion)
```

If `--dry-run` flag was set, stop here.

### Step 4: Execute Sync

#### 4-pre. Orphan-skill guard

Before pushing, warn if any root-level directory under `skills/` contains a `SKILL.md` directly but has no sub-skills (indicating it should be nested inside a group):

```bash
for d in RESEARCH/.cursor/skills/*/; do
  dir=$(basename "$d")
  if [ -f "$d/SKILL.md" ]; then
    subskills=$(find "$d" -mindepth 2 -name SKILL.md 2>/dev/null | wc -l)
    if [ "$subskills" -eq 0 ]; then
      echo "WARNING: Orphaned skill at root: $dir -- move to a group"
    fi
  fi
done
```

If warnings appear, the agent should report them but **continue the sync** (non-blocking). Orphaned skills still get synced; the warning is informational for future cleanup.

Push research to each target. For `commands/`, `rules/`, and `.claude/skills/`, sync the entire directory. For `.cursor/skills/`, apply **skill group filtering**.

#### 4a. commands/, rules/, and .claude/skills/ (always full sync)

```bash
EXCLUDES="--exclude node_modules/ --exclude __pycache__/"
rsync -ac $EXCLUDES RESEARCH/.cursor/commands/ TARGET/.cursor/commands/
rsync -ac $EXCLUDES RESEARCH/.cursor/rules/    TARGET/.cursor/rules/
rsync -ac $EXCLUDES RESEARCH/.claude/skills/   TARGET/.claude/skills/
```

#### 4b. skills/ (group-filtered sync)

Determine which skill groups to push for this target:

1. If `--all-skills` flag: push all subdirectories
2. If `--skill-groups G1,G2`: push only G1, G2 (overrides per-repo whitelist)
3. Otherwise: read the target's `Skill Groups` column from sync-targets.md

For each allowed skill group, sync that subdirectory:

```bash
mkdir -p TARGET/.cursor/skills/GROUP/
rsync -ac $EXCLUDES RESEARCH/.cursor/skills/GROUP/ TARGET/.cursor/skills/GROUP/
```

Also sync root-level files in `skills/` (README.md, SKILL.md, etc.) and shared companion directories (any root-level subdirectory that contains no SKILL.md at any depth, e.g. `docs/`, `references/`, `scripts/`, `templates/`, and any future additions):

```bash
rsync -ac $EXCLUDES --exclude='*/' RESEARCH/.cursor/skills/ TARGET/.cursor/skills/
for d in RESEARCH/.cursor/skills/*/; do
  dir=$(basename "$d")
  case "$dir" in node_modules|__pycache__) continue ;; esac
  if [ -z "$(find "$d" -name SKILL.md -print -quit 2>/dev/null)" ]; then
    rsync -ac $EXCLUDES "$d" "TARGET/.cursor/skills/$dir/"
  fi
done
```

Flags:
- `-a` (archive): preserve structure, permissions, timestamps
- `-c` (checksum): compare by content hash — files with identical content are skipped even if mtime differs

**No `--delete` flag** — files that exist only in the target are never removed.

Execute targets **one at a time, sequentially** (not in a for loop). Each target gets its own set of rsync commands. This avoids shell instability issues.

```bash
# $BASE and RESEARCH are set by environment detection (see Configuration section)
RESEARCH="$BASE/research"
EXCLUDES="--exclude node_modules/ --exclude __pycache__/"

# Target 1: github-to-notion-sync (groups: gws, nlm, pipeline, workflow, anthropic, standalone)
rsync -ac $EXCLUDES $RESEARCH/.cursor/commands/ $BASE/github-to-notion-sync/.cursor/commands/
rsync -ac $EXCLUDES $RESEARCH/.cursor/rules/    $BASE/github-to-notion-sync/.cursor/rules/
rsync -ac $EXCLUDES $RESEARCH/.claude/skills/   $BASE/github-to-notion-sync/.claude/skills/
rsync -ac $EXCLUDES --exclude='*/' $RESEARCH/.cursor/skills/ $BASE/github-to-notion-sync/.cursor/skills/
# Shared companion dirs (no SKILL.md = not a skill group)
for d in $RESEARCH/.cursor/skills/*/; do
  dir=$(basename "$d")
  case "$dir" in node_modules|__pycache__) continue ;; esac
  [ -z "$(find "$d" -name SKILL.md -print -quit 2>/dev/null)" ] && rsync -ac $EXCLUDES "$d" "$BASE/github-to-notion-sync/.cursor/skills/$dir/"
done
for g in gws nlm pipeline workflow anthropic standalone; do
  mkdir -p $BASE/github-to-notion-sync/.cursor/skills/$g/
  rsync -ac $EXCLUDES $RESEARCH/.cursor/skills/$g/ $BASE/github-to-notion-sync/.cursor/skills/$g/
done

# Target 2: ai-platform-strategy (groups: all)
rsync -ac $EXCLUDES $RESEARCH/.cursor/commands/ $BASE/ai-platform-strategy/.cursor/commands/
rsync -ac $EXCLUDES $RESEARCH/.cursor/rules/    $BASE/ai-platform-strategy/.cursor/rules/
rsync -ac $EXCLUDES $RESEARCH/.claude/skills/   $BASE/ai-platform-strategy/.claude/skills/
rsync -ac $EXCLUDES $RESEARCH/.cursor/skills/   $BASE/ai-platform-strategy/.cursor/skills/

# Target 3: ai-model-event-stock-analytics (groups: all)
rsync -ac $EXCLUDES $RESEARCH/.cursor/commands/ $BASE/ai-model-event-stock-analytics/.cursor/commands/
rsync -ac $EXCLUDES $RESEARCH/.cursor/rules/    $BASE/ai-model-event-stock-analytics/.cursor/rules/
rsync -ac $EXCLUDES $RESEARCH/.claude/skills/   $BASE/ai-model-event-stock-analytics/.claude/skills/
rsync -ac $EXCLUDES $RESEARCH/.cursor/skills/   $BASE/ai-model-event-stock-analytics/.cursor/skills/

# Target 4: ai-template (groups: workflow, anthropic, ce, ecc, standalone)
rsync -ac $EXCLUDES $RESEARCH/.cursor/commands/ $BASE/ai-template/.cursor/commands/
rsync -ac $EXCLUDES $RESEARCH/.cursor/rules/    $BASE/ai-template/.cursor/rules/
rsync -ac $EXCLUDES $RESEARCH/.claude/skills/   $BASE/ai-template/.claude/skills/
rsync -ac $EXCLUDES --exclude='*/' $RESEARCH/.cursor/skills/ $BASE/ai-template/.cursor/skills/
# Shared companion dirs (no SKILL.md = not a skill group)
for d in $RESEARCH/.cursor/skills/*/; do
  dir=$(basename "$d")
  case "$dir" in node_modules|__pycache__) continue ;; esac
  [ -z "$(find "$d" -name SKILL.md -print -quit 2>/dev/null)" ] && rsync -ac $EXCLUDES "$d" "$BASE/ai-template/.cursor/skills/$dir/"
done
for g in workflow anthropic ce ecc standalone; do
  mkdir -p $BASE/ai-template/.cursor/skills/$g/
  rsync -ac $EXCLUDES $RESEARCH/.cursor/skills/$g/ $BASE/ai-template/.cursor/skills/$g/
done
```

### Step 5: Final Verification & Report

After all syncs complete, verify file counts per repo. Repos with `all` skill groups should match research; others will have fewer skills (filtered).

```bash
for repo in research github-to-notion-sync ai-platform-strategy ai-model-event-stock-analytics ai-template; do
  path="$BASE/$repo"
  cmd_count=$(find "$path/.cursor/commands/" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
  skill_count=$(find "$path/.cursor/skills/" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
  claude_count=$(find "$path/.claude/skills/" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
  rule_count=$(find "$path/.cursor/rules/" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "$repo: commands=$cmd_count skills=$skill_count claude_skills=$claude_count rules=$rule_count"
done
```

Present the final report:

```
Cursor Sync Report (N-Repo)
===========================
Hub: $BASE/research/.cursor/ (ENV_LABEL)

Pull Phase:
  [per-target new file counts from Step 0c]

Push Phase:
  github-to-notion-sync:          OK (groups: gws, nlm, pipeline, workflow, anthropic, standalone)
  ai-platform-strategy:              OK (groups: all)
  ai-model-event-stock-analytics: OK (groups: all)
  ai-template:                    OK (groups: workflow, anthropic, ce, ecc, standalone)

Verification:
  research:                       commands: 461 | skills: 584 | rules: 51
  ai-model-event-stock-analytics: commands: 461 | skills: 584 | rules: 51  (all groups)
  ai-platform-strategy:              commands: 461 | skills: 584 | rules: 51  (all groups)
  github-to-notion-sync:          commands: 461 | skills: ~120 | rules: 51  (6 groups)
  ai-template:                    commands: 461 | skills: ~82  | rules: 51  (5 groups)

Skipped targets: 0
```

## Implementation Rules

### Shell command rules

These rules prevent the issues discovered during testing with macOS openrsync:

1. **Never use `-i` or `-v` flags** with rsync — openrsync doesn't produce parseable per-file output with these flags
2. **Never parse rsync output** for file lists — use `comm` or `diff` for file comparison instead
3. **Execute rsync per-target, not in for-loops** — run each target's 3 rsync commands as a separate Shell tool call to avoid shell instability
4. **Use `&&` to chain** the 3 rsync commands (commands, skills, rules) for one target — if any fails, the chain stops
5. **Verify with file counts** after sync — `ls DIR | wc -l` is the source of truth, not rsync output

### rsync flag reference

| Phase | Flags | Purpose |
|-------|-------|---------|
| Pull  | `-au` | archive + update (newer wins) |
| Push  | `-ac` | archive + checksum (content-identical files skipped) |

**Forbidden flags**: `-i` (no useful output on openrsync), `-v` (no file list on openrsync), `--delete` (never remove target-only files)

## Examples

### Example 1: Full N-Repo sync (default — most common)

User made new skills in `ai-platform-strategy` and new commands in `github-to-notion-sync`. They switch to research and run `/cursor-sync`.

Agent actions:
1. Validate 4 targets exist
2. `comm` diff: detect 5 new commands in gns, 2 new skills in webui
3. Pull: `rsync -au` from each target → research (one target per Shell call)
4. `comm` diff: preview push to each target
5. Push: `rsync -ac` from research → each target (one target per Shell call)
6. Verify: all 5 repos show identical file counts
7. Report

### Example 2: Dry-run preview

User runs `/cursor-sync --dry-run`.

Agent actions:
1. Pull Phase: `comm` diff from each target vs research — show new file counts
2. Push Phase: `comm` diff from research vs each target — show what would be pushed
3. No rsync executed, no files changed
4. Report preview

### Example 3: Pull only

User runs `/cursor-sync --pull-only`.

Agent actions:
1. `comm` diff from each target vs research
2. `rsync -au` from each target → research
3. Report what was pulled
4. Stop — no push

### Example 4: Push only

User runs `/cursor-sync --no-pull`.

Agent actions:
1. Skip pull
2. `comm` diff from research vs each target
3. `rsync -ac` from research → each target
4. Verify file counts
5. Report

### Example 5: Single-target push

User runs `/cursor-sync --targets ai-template`.

Agent actions:
1. Pull skipped (single-target mode)
2. `comm` diff from research vs ai-template
3. `rsync -ac` from research → ai-template
4. Verify
5. Report

## Error Handling

| Scenario | Action |
|----------|--------|
| Target directory does not exist | Warn and skip; continue with other targets |
| Bidirectional source does not exist | Warn and skip pull for that source; continue |
| Permission denied | Report the error, suggest `chmod` |
| No changes detected | Report "all targets up to date" |
| Partial failure (some targets fail) | Sync remaining targets, report failures at the end |
| `--repo` and `--targets` both provided | Report error: flags are mutually exclusive |
| `--repo` value not found in registry | List all registered repos and abort |
| Same file in multiple repos | Pull uses `-u` (newest mtime wins); report which version was kept |
| rsync hangs or takes >60s per target | Likely a large skills/ directory — increase Shell timeout to 120s |

## Troubleshooting

- **rsync seems to do nothing**: macOS openrsync produces no per-file output. Use `comm` diff before/after to verify changes
- **Pull overwrote research with older content**: rsync `-u` compares mtime. If a repo has a stale copy with newer mtime (e.g. re-cloned), it wins. Revert with `git checkout -- .cursor/` then `/cursor-sync --no-pull`
- **Shell command fails with exit code 1 but files are synced**: openrsync sometimes returns non-zero even on success when grep finds no matches in piped output. Check file counts to verify actual state
- **Want to push without pulling**: Use `--no-pull`
- **Want to update only research**: Use `--pull-only`

## N-Repo Sync 워크플로우 가이드

### 핵심 규칙

> **어느 레포에서 `.cursor/`를 변경해도, 항상 research에서 `/cursor-sync`를 실행해 전파한다.**

### 일반 워크플로우

```
1. 어느 레포에서나 스킬/커맨드/룰을 수정
2. cd $BASE/research
3. /cursor-sync
   → 4개 레포에서 변경 사항 pull (newest wins)
   → research 기준으로 4개 레포에 push
   → 5개 레포 모두 동기화 완료
```

### 레포별 작업 시나리오

| 시나리오 | 실행할 명령 |
|----------|-------------|
| research에서 스킬 작성 후 배포 | `/cursor-sync --no-pull` |
| 다른 레포에서 스킬 추가, research로 가져오기만 | `/cursor-sync --pull-only` |
| 5개 레포 전체 완전 동기화 | `/cursor-sync` |
| 변경 사항 미리보기 | `/cursor-sync --dry-run` |
| 특정 레포에만 배포 (긴급) | `/cursor-sync --targets ai-template` |
| commands만 전체 동기화 | `/cursor-sync --scope commands` |

### 충돌 해결 우선순위

Pull phase에서 동일 파일이 여러 레포에 있을 때:
1. **파일 mtime이 최신인 레포가 우선** (rsync `-u` 동작)
2. mtime이 같으면 `sync-targets.md`에서 **나중에 나열된 레포**가 우선
3. 잘못된 버전이 pull됐다면: `git checkout -- .cursor/<file>` 로 복원 후 `/cursor-sync --no-pull`
