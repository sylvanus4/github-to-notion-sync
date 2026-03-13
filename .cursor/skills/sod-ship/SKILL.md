---
name: sod-ship
description: >-
  Start-of-day git sync pipeline: commit dirty working directories, push
  unpushed commits, and pull remote changes for all 5 managed projects,
  resolving errors along the way. Use when the user runs /sod-ship, asks to
  "sync all projects", "start of day sync", "pull all repos", "컴퓨터 바꿔서
  작업 시작", "아침 싱크", "프로젝트 동기화", "sod-ship", or needs to ensure all
  repos are clean and up-to-date before starting work. Do NOT use for
  end-of-day shipping (use eod-ship), morning briefing with Google/stock
  pipelines (use morning-ship), or syncing .cursor/ assets only (use
  cursor-sync).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# SOD Ship — Start-of-Day Git Sync Pipeline

Bidirectional git sync for all managed projects: commit dirty repos, push unpushed commits, pull remote changes, and verify everything is in sync. Designed for starting work on a new day or switching to a different computer.

## Configuration

- **Managed projects**: See [eod-ship project-registry.md](../eod-ship/references/project-registry.md)
- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Upstream patterns**: `domain-commit` (commit splitting), `release-ship` (push strategy per repo mode)

## Usage

```
/sod-ship                          # full pipeline (commit + push + pull + Slack)
/sod-ship --skip-push              # pull only, skip committing/pushing local changes
/sod-ship --skip-pull              # commit and push only, skip pulling remote
/sod-ship --targets research       # process specific projects only (comma-separated)
/sod-ship --no-slack               # skip Slack notification
/sod-ship --dry-run                # preview only (show status, no git operations)
```

Arguments can be combined freely. Defaults: commit+push+pull all, post to Slack.

## Workflow

### Phase 1: Pre-flight Scan

Scan all managed projects to build a status map before making any changes.

**If `--targets` is set**, only scan the specified projects. Otherwise scan all 5.

Read project paths from [eod-ship project-registry.md](../eod-ship/references/project-registry.md).

For each project in order:

```bash
cd PROJECT_PATH
git status --short
git log @{u}.. --oneline 2>/dev/null
git fetch origin
```

Build a per-project status map (`project`, `mode`, `branch`, `dirty_count`, `unpushed`, `behind`, `diverged`) and display a summary table:

```
SOD Pre-flight Scan
=====================
Project                          Branch    Dirty  Unpushed  Behind  Status
github-to-notion-sync            main      0      0         3       PULL NEEDED
ai-template                      main      0      0         0       UP TO DATE
ai-model-event-stock-analytics   dev       5      2         0       PUSH NEEDED
research                         main      0      0         1       PULL NEEDED
ai-platform-webui                issue/42  12     0         5       COMMIT+PULL
```

If `--dry-run` flag is set, stop here after displaying the scan results.

**Important**: Always `cd` back to the original directory after processing each project in every phase.

### Phase 2: Ship Local Changes (Commit + Push)

**Skip if** `--skip-push` flag is set.

For each project that has `dirty: true` or `unpushed > 0`:

#### Step 2a: Commit dirty repos

If `dirty: true`:

1. `cd PROJECT_PATH`
2. Follow the `domain-commit` pattern:
   - `git status --short | sort` to list all changes
   - Categorize files by directory prefix into domain batches
   - For each batch, `git add <files>` and commit with `[TYPE] Summary` format (HEREDOC)
   - If pre-commit hooks fail: fix lint errors, re-stage, create new commit (never amend)
   - For projects without `.pre-commit-config.yaml`: simple `git add -A && git commit`
3. Verify: `git status --short` must be empty

#### Step 2b: Push unpushed commits

If `unpushed > 0` (including commits just created in Step 2a):

```bash
# ai-platform-webui (tmp-only mode)
git push origin HEAD:tmp

# Other repos (full mode)
git push origin HEAD
```

If push is rejected (diverged history):

1. Mark as `push_deferred: true` — will retry after Phase 3 pull
2. Continue to next project

Record per-project result: `{commits_created: N, pushed: bool, push_deferred: bool}`.

### Phase 3: Pull Remote Changes

**Skip if** `--skip-pull` flag is set.

For each project that has `behind > 0` or needs a fresh check:

```bash
cd PROJECT_PATH
git fetch origin
```

#### Step 3a: Pull

```bash
# ai-platform-webui (tmp-only mode)
git pull origin tmp

# Other repos (full mode)
git pull
```

#### Step 3b: Conflict resolution

If pull succeeds (fast-forward or clean merge): record `{pulled: true, commits_received: N}`.

If merge conflict occurs:

1. `git merge --abort`
2. Attempt rebase: `git pull --rebase`
3. If rebase succeeds: record `{pulled: true, rebased: true, commits_received: N}`
4. If rebase also fails:
   - `git rebase --abort`
   - Record `{pulled: false, conflict_files: [...]}`
   - Report conflicting files to user
   - Skip this project, continue with others

#### Step 3c: Retry deferred push

If `push_deferred: true` from Phase 2 and pull succeeded:

```bash
# ai-platform-webui
git push origin HEAD:tmp

# Other repos
git push origin HEAD
```

If retry push still fails, record the error and continue.

### Phase 4: Verify Sync

For each project:

```bash
cd PROJECT_PATH
git status --short
git log @{u}.. --oneline 2>/dev/null
git log ..@{u} --oneline 2>/dev/null
```

Classify each project:

| Status | Condition |
|--------|-----------|
| SYNCED | Clean working directory, no unpushed, no unpulled |
| PARTIAL | Pushed but pull failed (or vice versa) |
| FAILED | Both push and pull failed, or conflict unresolved |
| SKIPPED | Directory missing or `--targets` excluded it |

Display verification table:

```
SOD Sync Verification
======================
Project                          Status    Details
github-to-notion-sync            SYNCED    3 commits received
ai-template                      SYNCED    already up to date
ai-model-event-stock-analytics   SYNCED    2 commits pushed, 1 received
research                         SYNCED    1 commit received
ai-platform-webui                PARTIAL   12 files committed, push OK, pull conflict in 2 files
```

### Phase 5: Slack + Report

#### Step 5a: Slack Notification

**Skip if** `--no-slack` or `--dry-run` flag is set.

Post to `#효정-할일` using the `slack_send_message` MCP tool.

```json
{
  "channel_id": "C0AA8NT4T8T",
  "message": "<Slack mrkdwn message>"
}
```

**Message template** (Slack mrkdwn):

```
*🔄 SOD Git 동기화 리포트* (YYYY-MM-DD)

*로컬 → 리모트 (커밋 & 푸시)*
- project-a: N개 커밋 생성, 푸시 완료
- project-b: 변경사항 없음

*리모트 → 로컬 (Pull)*
- project-a: N개 커밋 수신
- project-b: 이미 최신

*결과*
- SYNCED: N/5, PARTIAL: N/5, FAILED: N/5
```

Slack mrkdwn rules:
- `*bold*` (single asterisk only, never `**`)
- `<url|text>` for links
- Write all message text in Korean
- Omit sections with no data
- Keep message under 5000 chars

#### Step 5b: Chat Report

Display the same structure as the Slack message in the chat as a formatted Korean report, using the Phase 4 verification table as the base.

## Examples

### Example 1: Full SOD sync (typical start-of-day)

User runs `/sod-ship` on a new morning with changes in 2 projects.

1. Pre-flight: scan reveals ai-model-event-stock-analytics has 5 dirty files, ai-platform-webui has 3 unpushed commits, 3 projects need pull
2. Ship local: 2 domain-split commits in analytics project, push both projects
3. Pull remote: 3 projects receive new commits, 2 already up to date
4. Verify: 5/5 SYNCED
5. Slack + Report posted

### Example 2: Switching computers (dirty repos everywhere)

User runs `/sod-ship` after switching to a different machine.

1. Pre-flight: 3 projects have uncommitted changes, 2 have unpushed commits, 4 need pull
2. Ship local: commit all dirty repos, push all
3. Pull remote: all 5 receive commits
4. Verify: 5/5 SYNCED
5. Slack + Report posted

### Example 3: Partial pipeline (skip-push or skip-pull)

`/sod-ship --skip-push` — pull only (repos already pushed from other machine). `/sod-ship --skip-pull` — commit and push only (about to switch computers).

### Example 4: Conflict during pull

User runs `/sod-ship` and one project has a merge conflict.

1. Pre-flight: research has 2 behind commits
2. Ship local: no dirty repos
3. Pull: research merge conflict on `README.md` — attempt rebase — rebase also fails — abort and report conflict files
4. Verify: 4/5 SYNCED, 1/5 PARTIAL (research: conflict)
5. Report shows: `research: PARTIAL — 충돌 파일: README.md (수동 해결 필요)`

## Error Handling

| Scenario | Action |
|----------|--------|
| Project directory does not exist | Warn and skip; continue with remaining projects |
| Pre-commit hook fails | Fix lint errors, re-stage, create new commit (never amend) |
| Push rejected (diverged history) | Defer push; pull first in Phase 3, then retry push |
| Push retry still fails | Report error with remediation; continue with others |
| Merge conflict on pull | Attempt rebase; if fails, abort and report conflict files |
| Network error (fetch/push/pull) | Retry once; if still fails, skip with error |
| No upstream tracking branch | Use `git push -u origin HEAD` for first push |
| Stash exists in project | Warn user about existing stashes; do not auto-apply |
| `gh` CLI not authenticated | Not needed (git-only operations); ignore |
| No changes in any project | Report "all projects already in sync" |

## Safety Rules

- **Never force push** (`--force`) to any branch in any project
- **Never push directly** to `main` or `dev` in any project
- **Never auto-resolve** merge conflicts that require manual intervention — abort and report
- **Never delete** branches, tags, or reset history
- **Never amend** failed commits; create new ones
- **Never commit** `.env`, credentials, or secret files
- **Never switch branches** automatically — work on the current branch only
- **ai-platform-webui**: Always `git push origin HEAD:tmp`, always `git pull origin tmp`
- **Always return** to original working directory after processing each project
- **Always display** pre-flight scan before making any changes
