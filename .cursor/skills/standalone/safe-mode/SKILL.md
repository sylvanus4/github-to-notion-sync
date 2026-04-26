---
name: safe-mode
description: >-
  Four-in-one safety tool: (1) intercept destructive shell commands (rm -rf,
  DROP TABLE, force-push, kubectl delete), (2) lock file edits to specific
  directories, (3) combined guard mode for maximum safety during production
  debugging, (4) install persistent Cursor hooks to block dangerous git commands
  across sessions via beforeShellExecution hooks. Use when the user asks for "safe mode",
  "careful mode", "freeze directory", "lock files", "guard mode", "git
  guardrails", "block git push", "git safety hooks", "install git hooks",
  "safe-mode", "세이프 모드", "안전 모드", "디렉토리 잠금", "파일 잠금",
  "가드 모드", "git 가드레일", "위험한 git 명령 차단", "git push 차단",
  "git 안전 훅", or when working on production systems. Do NOT use for general
  code review (use deep-review), security auditing (use security-expert), CI
  checks (use ci-quality-gate), or pre-commit linting hooks (use
  setup-pre-commit).
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "safety"
---
# Safe Mode — Four-in-One Safety Tool

Four safety mechanisms in one skill to prevent catastrophic mistakes during agent operations.

## Modes

| Mode | Trigger | What it does |
|------|---------|-------------|
| `careful` | `/safe-mode careful` | Intercept destructive shell commands before execution |
| `freeze` | `/safe-mode freeze <dir>` | Lock edits to a specific directory scope |
| `guard` | `/safe-mode guard <dir>` | Combined: careful + freeze together |

## Usage

```
/safe-mode careful                    # activate destructive command interception
/safe-mode freeze src/api/            # lock edits to src/api/ only
/safe-mode freeze src/api/ src/db/    # lock edits to multiple directories
/safe-mode guard src/                 # combined careful + freeze
/safe-mode off                        # deactivate all safety modes
/safe-mode status                     # show current safety mode
```

## Mode 1: Careful — Destructive Command Interception

### Intercepted Patterns

Before executing ANY shell command, scan for these destructive patterns:

| Category | Patterns | Risk |
|----------|----------|------|
| File deletion | `rm -rf`, `rm -r`, `rm *`, `rmdir`, `shutil.rmtree` | Data loss |
| Git destructive | `git push --force`, `git push -f`, `git reset --hard`, `git clean -fd` | History loss |
| Database destructive | `DROP TABLE`, `DROP DATABASE`, `TRUNCATE`, `DELETE FROM` (without WHERE) | Data loss |
| Container destructive | `docker rm -f`, `docker system prune`, `kubectl delete` | Service loss |
| Disk operations | `dd if=`, `mkfs`, `fdisk` | Disk destruction |
| Permission bombs | `chmod -R 777`, `chmod -R 000`, `chown -R` | Security breach |
| Network destructive | `iptables -F`, `ufw reset` | Connectivity loss |

### Safe Exceptions (do NOT intercept)

These destructive-looking commands are safe in development context:
- `rm -rf node_modules` — standard cleanup
- `rm -rf .next` / `rm -rf dist` / `rm -rf build` — build artifact cleanup
- `rm -rf __pycache__` / `rm -rf .pytest_cache` — cache cleanup
- `rm -rf coverage` — test coverage cleanup
- `docker rm` (without `-f`) — graceful container removal
- `git clean -fd` in `.gitignore`-listed directories

### Interception Protocol

When a destructive command is detected:

1. **STOP** — do not execute the command
2. **Paperclip Governance Gate (Optional)**: If Paperclip is available and the command falls in the Git destructive or Database destructive category:
   ```
   Tool: paperclip_dashboard
   Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
   ```
   If available, create an approval request:
   ```
   Tool: paperclip_create_issue
   Input: {
     "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92",
     "title": "Destructive op approval: {command_summary}",
     "body": "Command: {full_command}\nRisk: {category}\nScope: {affected_resources}",
     "priority": "critical",
     "labels": ["destructive-op", "governance-required"]
   }
   ```
   Wait for Paperclip approval before presenting options to the user. If Paperclip is unavailable, fall through to the standard interception flow.
3. **Display warning** with the exact command and risk category
4. **Ask for explicit confirmation** using the AskQuestion tool:
   - Option A: "Execute as-is (I understand the risk)"
   - Option B: "Show me a safer alternative"
   - Option C: "Cancel — do not execute"
5. If Option B: suggest a safer equivalent (e.g., `mv` to trash instead of `rm -rf`)
6. Log the interception event (and via `paperclip_log_cost` if Paperclip is available)

### Safer Alternatives Table

| Destructive | Safer Alternative |
|-------------|-------------------|
| `rm -rf <dir>` | `mv <dir> /tmp/<dir>-$(date +%s)` |
| `git push --force` | `git push --force-with-lease` |
| `git reset --hard` | `git stash` then `git reset --soft` |
| `DROP TABLE x` | `ALTER TABLE x RENAME TO x_deprecated_YYYYMMDD` |
| `DELETE FROM x` | `DELETE FROM x WHERE <condition> LIMIT 100` |
| `docker system prune` | `docker system prune --filter "until=24h"` |
| `kubectl delete pod` | `kubectl delete pod --grace-period=30` |

## Mode 2: Freeze — Directory Scope Locking

### How It Works

When freeze mode is active with one or more directory paths:

1. **Before any file write/edit**: Check if the target file path starts with one of the frozen directories
2. **If the file IS within a frozen directory**: Allow the edit (this is the permitted scope)
3. **If the file is OUTSIDE all frozen directories**: Block the edit and warn

### Scope Rules

- Paths are matched with prefix comparison
- Trailing slash is normalized: `src/api` and `src/api/` are equivalent
- Multiple directories can be frozen simultaneously
- `freeze .` means "allow edits only in current working directory"
- Nested paths work: `freeze src/api/auth/` restricts to that subdirectory

### What Gets Checked

- `Write` tool calls — file path must be within frozen scope
- `StrReplace` tool calls — file path must be within frozen scope
- `Delete` tool calls — file path must be within frozen scope
- `Shell` commands that write files (detected by `>` or `>>` redirect operators) — target path checked

### Freeze Bypass

Some operations are always allowed regardless of freeze scope:
- Reading any file (Read, Grep, Glob, SemanticSearch)
- Git operations (`git status`, `git diff`, `git log`)
- Running tests
- Lint checks

## Mode 3: Guard — Combined Safety

Guard mode activates both careful AND freeze simultaneously:

```
/safe-mode guard src/api/
```

Equivalent to:
```
/safe-mode careful
/safe-mode freeze src/api/
```

This is the recommended mode for production debugging sessions where you need maximum safety.

## Implementation Notes

This skill operates as a **behavioral protocol** rather than a hook-based system. When safe-mode is activated:

1. The agent acknowledges the mode activation
2. Before EVERY subsequent shell command or file edit, the agent checks against the active rules
3. The agent maintains awareness of the active mode throughout the session
4. Mode persists until explicitly deactivated with `/safe-mode off`

### State Tracking

The agent tracks these in-session states:
- `careful_active: bool` — whether destructive command interception is on
- `freeze_dirs: list[str]` — list of allowed edit directories (empty = no freeze)
- `guard_active: bool` — combined mode flag

### Status Display

When `/safe-mode status` is invoked:

```
Safe Mode Status
================
Careful (destructive interception): [ON/OFF]
Freeze (directory lock):            [ON/OFF]
  Allowed directories:              [list or "none"]
Guard (combined):                   [ON/OFF]

Commands intercepted this session:  [N]
Edits blocked this session:         [N]
```

## Examples

### Example 1: Production database debugging

```
User: /safe-mode guard backend/
Agent: Safe Mode GUARD activated.
  - Destructive command interception: ON
  - Directory lock: backend/ (edits outside blocked)

User: Can you check the migration and fix the schema issue?
Agent: [reads files, proposes fix within backend/ — allowed]
Agent: [attempts to edit frontend/config.ts — BLOCKED, warns user]
```

### Example 2: Careful mode during deploy

```
User: /safe-mode careful
Agent: Safe Mode CAREFUL activated. Destructive commands will require confirmation.

User: Clean up old containers
Agent: I would run `docker system prune -a`. This is flagged as destructive.
  [AskQuestion: Execute as-is / Show safer alternative / Cancel]
User: Show safer
Agent: Safer alternative: `docker system prune --filter "until=48h"` (only removes items older than 48h)
```

### Example 3: Freeze for focused work

```
User: /safe-mode freeze src/features/auth/
Agent: Safe Mode FREEZE activated. File edits restricted to: src/features/auth/

[During session, all edits outside src/features/auth/ are blocked with warnings]
```

## Mode 4: Git Guardrails — Persistent Hook-Based Git Safety

Install a **persistent Cursor `beforeShellExecution` hook** that intercepts
dangerous git commands across ALL sessions — not just the current one.

### Trigger

```
/safe-mode git-guardrails            # install project-scoped hooks
/safe-mode git-guardrails --global   # install global hooks
```

### What Gets Blocked

| Command | Risk |
|---------|------|
| `git push` (all variants incl. `--force`) | Unreviewed code reaching remote |
| `git reset --hard` | Uncommitted work loss |
| `git clean -f` / `git clean -fd` | Untracked file deletion |
| `git branch -D` | Branch history loss |
| `git checkout .` / `git restore .` | Working tree changes loss |

Read-only commands (`git status`, `git log`, `git diff`) are NEVER blocked.

### Setup Process

#### 1. Determine scope

Ask: install for **this project only** or **globally**?

- **Project**: `.cursor/hooks/block-dangerous-git.sh`
- **Global**: `~/.cursor/hooks/block-dangerous-git.sh`

#### 2. Create the hook script

Write the blocking script to the chosen location:

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except:
    print('')
" 2>/dev/null || echo "")

BLOCKED_PATTERNS=(
    "git push"
    "git reset --hard"
    "git clean -f"
    "git clean -fd"
    "git branch -D"
    "git checkout \.$"
    "git restore \.$"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern"; then
        echo "BLOCKED: '$COMMAND' matches blocked pattern '$pattern'. You do not have authority to run this command." >&2
        exit 2
    fi
done

exit 0
```

Make it executable with `chmod +x`.

#### 3. Register in hooks.json

Add to `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (global).
Uses the Cursor v1 hooks schema with `beforeShellExecution` event:

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": ".cursor/hooks/block-dangerous-git.sh",
        "matcher": "git push|git reset --hard|git clean|git branch -D|git checkout \\\\.|git restore \\\\."
      }
    ]
  }
}
```

If `hooks.json` already exists, **merge** the `beforeShellExecution` entry
into the existing `hooks` object. Never overwrite — that disables other hooks.

#### 4. Customization

Ask if the user wants to add or remove patterns from the blocked list. Edit
the script accordingly.

#### 5. Verify

Test the hook:

```bash
echo '{"command":"git push origin main"}' | .cursor/hooks/block-dangerous-git.sh
```

Should exit with code 2 and print a BLOCKED message to stderr.

### Git Guardrails vs Careful Mode

| Aspect | Careful (Mode 1) | Git Guardrails (Mode 4) |
|--------|-----------------|------------------------|
| Persistence | Session-only | Persists across sessions via hooks.json |
| Scope | All destructive commands | Git commands only |
| Mechanism | Agent behavioral protocol | Cursor `beforeShellExecution` hook |
| Bypass | `/safe-mode off` | Remove from hooks.json |
| User terminal | Not affected | Not affected (agent-only) |

### Git Guardrails Gotchas

- `git checkout .` regex uses end-anchor (`\.$`) to avoid false positives on
  branch checkouts like `git checkout feature-branch`.
- The `python3` JSON parser may fail if Cursor's input format changes.
  The `|| echo ""` fallback prevents crashes but may cause false negatives.
- If `hooks.json` already has `beforeShellExecution` entries, merge into the
  existing array. Overwriting disables other hooks.
- Matcher uses JavaScript regex syntax (not POSIX). Backslashes need double-escaping in JSON.

## Error Handling

| Scenario | Action |
|----------|--------|
| User tries to edit outside freeze scope | Block edit, display warning with scope reminder |
| Destructive command in a pipeline (&&) | Scan entire pipeline string, intercept if any segment is destructive |
| User deactivates mid-session | Confirm deactivation, log session summary |
| Ambiguous path (no trailing slash) | Normalize and confirm scope with user |
