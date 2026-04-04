# hermes-checkpoint-rollback

---
name: hermes-checkpoint-rollback
version: 1.0.0
description: Shadow git checkpoint system for transparent filesystem snapshots and rollback before destructive operations
triggers:
  - "checkpoint"
  - "rollback"
  - "snapshot before editing"
  - "undo file changes"
  - "체크포인트"
  - "롤백"
  - "스냅샷"
  - "파일 복원"
  - "되돌리기"
  - "hermes-checkpoint"
category: standalone
composable_with:
  - safe-mode
  - deep-review
  - simplify
  - ship
  - release-commander
do_not_use_for:
  - Git commit management (use domain-commit)
  - Git branch operations (use standard git)
  - Database backups (use db-expert)
  - Infrastructure state drift (use infra-drift-detector)
---

## Purpose

Provide transparent filesystem snapshots via shadow git repositories — separate
from the user's actual git history — so that any file-mutating agent operation
can be safely rolled back without polluting the project's commit log. Inspired
by the Hermes Agent CheckpointManager pattern (nousresearch/hermes-agent).

## When to Use

- Before large-scale refactoring that touches 5+ files
- Before running code generation that overwrites existing files
- When the user says "make a backup before changing" or "save a restore point"
- Before pipeline operations that produce destructive side effects
- When experimenting with risky code changes that might need reverting

## Architecture

```
Project Directory (working tree)
      │
      ├── .git/           ← user's real git (NEVER touched)
      │
Shadow Repo (separate):
  ~/.hermes-checkpoints/<hash>/
      ├── HEAD
      ├── refs/
      ├── objects/        ← snapshots of working tree files
      └── HERMES_WORKDIR  ← pointer back to project dir
```

The shadow repo uses `GIT_DIR` and `GIT_WORK_TREE` environment variables to
operate on the project files without initializing `.git` inside the project.

## Workflow

### Step 1: Take a Checkpoint

Before any destructive operation, snapshot the current directory state:

```bash
SHADOW_DIR="$HOME/.hermes-checkpoints/$(echo "$PWD" | shasum -a 256 | cut -c1-16)"
mkdir -p "$SHADOW_DIR"

if [ ! -f "$SHADOW_DIR/HEAD" ]; then
  git init --bare "$SHADOW_DIR"
  git --git-dir="$SHADOW_DIR" --work-tree="$PWD" config user.email "checkpoint@local"
  git --git-dir="$SHADOW_DIR" --work-tree="$PWD" config user.name "Checkpoint"
  # Exclude common noise
  mkdir -p "$SHADOW_DIR/info"
  echo -e "node_modules/\n.venv/\n__pycache__/\n*.pyc\n.env\n.DS_Store\n*.log" > "$SHADOW_DIR/info/exclude"
fi

git --git-dir="$SHADOW_DIR" --work-tree="$PWD" add -A
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" commit -m "checkpoint: <REASON>" --allow-empty
```

Where `<REASON>` describes why the snapshot was taken (e.g., "before refactoring auth module").

### Step 2: Perform the Operation

Execute the risky file modifications (refactoring, code generation, pipeline execution).

### Step 3: List Available Checkpoints

```bash
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" log --oneline -20
```

### Step 4: Diff Against a Checkpoint

Compare the current state against a previous checkpoint:

```bash
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" diff <COMMIT_HASH>
```

### Step 5: Rollback (if needed)

Restore the entire working tree to a checkpoint:

```bash
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" checkout <COMMIT_HASH> -- .
```

Or restore specific files:

```bash
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" checkout <COMMIT_HASH> -- path/to/file.py
```

## Safety Rules

1. **Never touch `.git/`** — the shadow repo is completely separate from the user's git
2. **Skip overly broad directories** — refuse to checkpoint `/`, `$HOME`, or any directory with 10,000+ files
3. **Deduplicate per turn** — take at most one snapshot per directory per agent turn to avoid spam
4. **Max 50 snapshots** — prune old checkpoints to prevent unbounded disk growth
5. **Silent failures** — checkpoint errors must never block the user's actual work; log and continue
6. **Exclude noise** — always exclude `node_modules/`, `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `.DS_Store`

## Modes

### Mode A: Manual Checkpoint
User explicitly requests a checkpoint before doing something risky.

### Mode B: Auto-Checkpoint (Recommended)
When running multi-file operations (refactoring, code generation, pipeline execution),
automatically take a checkpoint at the start and inform the user:

> "체크포인트를 생성했습니다. 문제가 생기면 롤백할 수 있습니다."

### Mode C: Diff Review
After an operation completes, diff against the pre-operation checkpoint to
show exactly what changed — useful for review before committing.

## Output Format

```
📸 Checkpoint created: abc1234
   Directory: /Users/user/project
   Reason: before refactoring auth module
   Files tracked: 142
   Available checkpoints: 3 (oldest: 2h ago)
```

```
⏪ Rollback complete: abc1234 → def5678
   Files restored: 7
   Changes reverted: 3 files modified, 2 files deleted (restored), 2 files added (removed)
```

## Verification (Mandatory)

After EVERY checkpoint or rollback, verify the operation succeeded:

### Post-Checkpoint Verification
```bash
# Confirm the commit exists
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" log -1 --oneline
# Confirm file count matches expectations
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" diff --stat HEAD~1 HEAD 2>/dev/null || echo "First checkpoint"
```

Report the verification result: commit hash, file count, and any warnings.
Do NOT proceed with the destructive operation until verification passes.

### Post-Rollback Verification
```bash
# Confirm working tree matches target checkpoint
git --git-dir="$SHADOW_DIR" --work-tree="$PWD" status
```

If `status` shows unexpected changes after rollback, STOP and warn the user
that rollback may be incomplete. Never claim "rollback complete" without
running this check.

## Rationalization Detection

NEVER rationalize skipping a checkpoint:
- "This is a small change" — small changes can cascade. If ≥ 3 files, take the checkpoint.
- "I already have git history" — shadow checkpoints capture uncommitted state that git misses.
- "The user didn't ask for it" — auto-checkpoint is the default for 5+ file operations.
- "It will slow things down" — a checkpoint takes < 2 seconds; a botched rollback takes hours.

## Domain Memory

Maintain a lightweight checkpoint ledger at `~/.hermes-checkpoints/ledger.json`:

```json
{
  "entries": [
    {
      "project": "/path/to/project",
      "commit": "abc1234",
      "reason": "before refactoring auth module",
      "timestamp": "2026-04-04T09:30:00Z",
      "files_tracked": 142
    }
  ]
}
```

This enables cross-session checkpoint awareness — the agent can report
"you have 3 checkpoints from yesterday's session" at the start of a new session.
Prune entries older than 7 days.

## Error Handling

| Scenario | Action |
|---|---|
| `git` not installed | Skip checkpoint, warn user, continue operation |
| Shadow repo corrupted | Delete and reinitialize, warn user |
| Directory too large (10K+ files) | Skip with explanation |
| Disk space low | Skip with warning |
| Permission errors | Log and continue |
| Verification fails post-checkpoint | Retry once, then warn and continue |
| Verification fails post-rollback | STOP, report partial rollback, do NOT continue |

## Examples

### Example 1: Before Refactoring
```
User: "이 모듈 리팩토링 해줘"
Agent: Takes checkpoint → refactors → shows diff → user approves or rolls back
```

### Example 2: Pipeline Safety Net
```
User: "/simplify full"
Agent: Auto-checkpoint before modifications → runs simplify → checkpoint preserved for rollback
```

### Example 3: Selective Restore
```
User: "config.py 변경 전 상태로 되돌려줘"
Agent: Lists checkpoints → restores only config.py from selected checkpoint
```
