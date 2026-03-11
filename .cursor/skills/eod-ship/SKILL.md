---
name: eod-ship
description: >-
  End-of-day shipping pipeline: cursor-sync assets across projects, then
  release-ship the current project and 5 managed projects, posting a
  consolidated summary to Slack. Use when the user runs /eod-ship, asks to
  "wrap up for the day", "end of day ship", "하루 마무리", "퇴근 전 커밋",
  or "EOD push all projects". Do NOT use for syncing .cursor/ assets only
  (use cursor-sync), shipping a single repo (use release-ship), or daily
  standup/scrum automation (use daily-scrum).
metadata:
  author: thaki
  version: 1.0.0
---

# EOD Ship — End-of-Day Multi-Project Shipping Pipeline

Chain cursor-sync and release-ship across all managed projects in a single flow. Syncs `.cursor/` assets first, ships uncommitted changes in the current project and 5 managed repos, then posts a consolidated report to Slack.

## Configuration

- **Managed projects**: See [references/project-registry.md](references/project-registry.md)
- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Upstream skills**: `cursor-sync`, `release-ship`

## Usage

```
/eod-ship                        # full pipeline (sync + ship all + Slack)
/eod-ship --skip-sync            # skip cursor-sync, ship only
/eod-ship --targets research     # ship specific project only (comma-separated)
/eod-ship --dry-run              # preview what would be shipped (no commits/push)
/eod-ship --no-slack             # skip Slack notification
```

Arguments can be combined freely. Defaults: sync all, ship all projects, post to Slack.

## Workflow

### Phase 1: Cursor Sync

**Skip if** `--skip-sync` flag is set.

Follow the `cursor-sync` skill (`.cursor/skills/cursor-sync/SKILL.md`).

```bash
# Sync .cursor/{commands,skills,rules} to all target projects
```

1. Read target paths from `cursor-sync/references/sync-targets.md`
2. Run rsync dry-run preview for each target
3. Execute sync
4. Capture per-target summary: `{target: {new: N, updated: N}}`

### Phase 2: Release Ship (Current Project)

Run the `release-ship` skill on the current working directory.

```bash
git status --short
```

1. If clean, record `{project: "current", status: "clean"}` and skip to Phase 3
2. If dirty, execute release-ship pipeline (domain-commit → push → issue → PR → merge)
3. Capture result: `{commits: [...], issues: [...], pr_url: "...", merged: bool}`

### Phase 3: Release Ship (Managed Projects)

**If `--targets` is set**, only process the specified projects. Otherwise process all 5.

Read project paths from [references/project-registry.md](references/project-registry.md).

For each project in order:

```bash
cd PROJECT_PATH
git status --short
```

1. If clean, record `{project: ALIAS, status: "clean"}` and move to next
2. If dirty, execute the release-ship pipeline:
   - Follow all release-ship rules (ai-platform-webui uses tmp-only mode)
   - Domain-split commits → push → issue → PR → merge
3. Capture result per project
4. `cd` back to original directory before processing next project

**Execution order** (from [references/project-registry.md](references/project-registry.md)):

1. `github-to-notion-sync` — full pipeline
2. `ai-template` — full pipeline
3. `ai-model-event-stock-analytics` — full pipeline
4. `research` — full pipeline
5. `ai-platform-webui` — tmp-only mode (commit → push → issue → report, no PR/merge)

If a project directory does not exist, warn and skip it. Continue with remaining projects.

### Phase 4: Slack Notification

**Skip if** `--no-slack` or `--dry-run` flag is set.

Post a consolidated summary to `#효정-할일` using the `slack_send_message` MCP tool.

```json
{
  "channel_id": "C0AA8NT4T8T",
  "message": "<Slack mrkdwn message>"
}
```

**Message template** (Slack mrkdwn — use `*bold*`, `_italic_`, `<url|text>`):

```
*📦 EOD 배포 리포트* (YYYY-MM-DD)

*커서 동기화*
- N개 타겟 동기화 완료, M개 파일 신규/업데이트

*프로젝트 배포*
- project-a: N개 커밋, <PR_URL|PR #X> 머지 완료
- project-b: 변경사항 없음
- project-c: N개 커밋 (tmp 전용)

*이슈 생성*
- <ISSUE_URL|#N1>, <ISSUE_URL|#N2> → 프로젝트 #5

*합계*
- N개 프로젝트 배포, M개 커밋, K개 이슈 생성
```

Rules:
- Use `*bold*` (single asterisk, never `**`)
- Use `<url|text>` for links
- Write all message text in Korean (한국어)
- Omit sections with no data (e.g., no Issues if `--no-issue` was used)
- Keep message under 5000 chars

### Phase 5: Report

Display the same consolidated summary in the chat as a formatted report (in Korean).

```
EOD 배포 리포트
================
날짜: YYYY-MM-DD

커서 동기화:
  동기화 타겟: N/N
  파일: M개 신규, K개 업데이트

프로젝트:
  github-to-notion-sync:          3개 커밋, PR #12 머지 완료
  ai-template:                    변경사항 없음
  ai-model-event-stock-analytics: 2개 커밋, PR #8 머지 완료
  research:                       1개 커밋, PR #5 머지 완료
  ai-platform-webui:              2개 커밋 (tmp 전용)

이슈: #101, #102, #103, #104 → 프로젝트 #5
슬랙: #효정-할일 채널에 게시 완료

합계: 4/5 프로젝트 배포, 8개 커밋, 4개 이슈
```

## Examples

### Example 1: Full EOD ship

User runs `/eod-ship` at end of day with changes across 3 projects.

1. cursor-sync: 4 targets synced, 6 files updated
2. Current project (github-to-notion-sync): 2 domain-split commits, PR #15 merged
3. ai-template: clean, skipped
4. ai-model-event-stock-analytics: 3 commits, PR #22 merged
5. research: 1 commit, PR #9 merged
6. ai-platform-webui: 2 commits pushed to tmp
7. Slack: summary posted to #효정-할일
8. Report displayed in chat

### Example 2: Ship without sync

User runs `/eod-ship --skip-sync` to skip cursor-sync.

1. cursor-sync: skipped
2. release-ship on current + 5 projects
3. Slack + Report

### Example 3: Ship specific project

User runs `/eod-ship --targets research,ai-template`.

1. cursor-sync: all targets synced
2. Current project: shipped
3. Only `research` and `ai-template` processed (others skipped)
4. Slack + Report

### Example 4: Dry run

User runs `/eod-ship --dry-run` to preview.

1. cursor-sync: dry-run preview (no file changes)
2. For each project: show `git status` and what would be committed
3. No commits, no push, no issues, no PRs
4. Slack: skipped (dry-run)
5. Report: preview summary only

## Error Handling

| Scenario | Action |
|----------|--------|
| Project directory does not exist | Warn and skip; continue with remaining projects |
| Project has merge conflicts | Report error for that project; continue with others |
| release-ship fails on one project | Report error; continue with remaining projects |
| cursor-sync fails | Report error; continue with Phase 2 (ship) |
| Slack message fails | Report error; still display report in chat |
| No changes in any project | Report "all projects clean" |
| `gh` CLI not authenticated | Report error; suggest `gh auth login` |
| Push rejected on a project | Report error with remediation; continue with others |

## Safety Rules

- **Never force push** (`--force`) to any branch in any project
- **Never push directly** to `main` or `dev` in any project
- **Never amend** failed commits; create new ones
- **Never commit** `.env`, credentials, or secret files
- **ai-platform-webui**: Never create PRs or merge — tmp-only mode
- **Always return** to original working directory after processing each project
- **Always post** Slack message as the authenticated user, never impersonate
