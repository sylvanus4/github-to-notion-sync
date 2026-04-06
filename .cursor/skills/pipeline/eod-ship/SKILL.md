---
name: eod-ship
description: >-
  End-of-day shipping pipeline: cursor-sync assets across projects, then
  release-ship the current project and 5 managed projects, posting a
  consolidated summary to Slack. Use when the user runs /eod-ship, asks to "wrap
  up for the day", "end of day ship", "하루 마무리", "퇴근 전 커밋", or "EOD push all
  projects". Do NOT use for syncing .cursor/ assets only (use cursor-sync),
  shipping a single repo (use release-ship), or daily standup/scrum automation
  (use daily-scrum).
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
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
/eod-ship --skip-memory          # skip session memory sync
```

Arguments can be combined freely. Defaults: sync all, ship all, memory sync, post to Slack.

## Workflow

### Phase 1: Cursor Sync

**Skip if** `--skip-sync` flag is set.

Follow the `cursor-sync` skill (`.cursor/skills/automation/cursor-sync/SKILL.md`).

```bash
# Sync .cursor/{commands,skills,rules} to all target projects
```

1. Read target paths from `cursor-sync/references/sync-targets.md`
2. Run rsync dry-run preview for each target
3. Execute sync
4. Capture per-target summary: `{target: {new: N, updated: N}}`

### Phase 1½: Dev Branch Merge (ai-platform-webui only)

Before shipping, merge the latest `origin/dev` into the current `tmp` branch of `ai-platform-webui` to ensure the working branch is up-to-date with the main development branch.

**Skip if** `--targets` is set and does not include `ai-platform-webui`, or if the `ai-platform-webui` directory does not exist.

```bash
cd AI_PLATFORM_WEBUI_PATH
git fetch origin dev
git merge origin/dev --no-edit
```

If merge conflict occurs:

1. For simple conflicts: accept `origin/dev` version with `git checkout --theirs <file> && git add <file>`
2. For modify/delete conflicts where `origin/dev` deleted files: `git rm <file>`
3. For complex conflicts that cannot be auto-resolved: abort with `git merge --abort`, record `{dev_merge: "conflict", conflict_files: [...]}`, and report to user
4. After resolving, commit with `git commit --no-verify -m "chore: merge origin/dev into tmp"`

If merge succeeds (fast-forward or clean merge): record `{dev_merge: "ok", dev_commits_received: N}`.

If no new commits from `origin/dev` (already up to date): record `{dev_merge: "up_to_date"}`.

Return to original directory after this step.

### Phase 1¾: Session Memory Sync

Synchronize agent session memory before shipping. Extracts today's session transcripts into structured markdown and rebuilds the search index. Skip with `--skip-memory`.

```bash
cd /Users/hanhyojung/work/thakicloud/ai-model-event-stock-analytics

# 1. Incremental transcript extraction
python scripts/memory/extract-sessions.py --incremental

# 2. Rebuild search index (skip embeddings for speed)
python scripts/memory/build-index.py --skip-embeddings

# 3. If MEMORY.md pointers exceed 50 lines, run attention decay
POINTER_COUNT=$(grep -c '^\- \[' MEMORY.md 2>/dev/null || echo 0)
if [ "$POINTER_COUNT" -gt 50 ]; then
    python scripts/memory/attention_decay.py --apply
fi
```

Record result: `{memory_sync: "ok", transcripts_extracted: N, index_rebuilt: true, decay_applied: bool}`.

On failure: **Warn and continue** — memory sync is optional; shipping proceeds.

### Phase 1⅞: Intelligence KB Routing (Research Repo)

Route accumulated intelligence artifacts (from x-to-slack, twitter-timeline-to-slack, paper-review) to Karpathy KB topics in the research repo. Skip if the research repo is not found.

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
if [ -d "$RESEARCH_REPO" ] && [ -f "$RESEARCH_REPO/scripts/intelligence/kb_intel_router.py" ]; then
    python3 "$RESEARCH_REPO/scripts/intelligence/kb_intel_router.py"
fi
```

This ensures:
- `outputs/intelligence/` and `outputs/papers/` artifacts are routed to `knowledge-bases/{topic}/raw/`
- KB manifests are updated with new sources
- All routed files are included when research repo is committed in Phase 3

Record result: `{intel_routing: "ok", routed: N, skipped: M}` or `{intel_routing: "skipped", reason: "research repo not found"}`.

On failure: Warn and continue. Intelligence routing is best-effort.

### Phase 2: Release Ship (Current Project)

Run the `release-ship` skill on the current working directory **in pipeline mode**.

**CRITICAL — Pipeline Mode**: When invoking release-ship from eod-ship, issue creation must be auto-confirmed (no user prompt). The user approved the entire pipeline by running `/eod-ship`. Do NOT skip issue creation steps. If release-ship's safety rules mention "user confirmation for issue plan", treat the eod-ship invocation as that confirmation.

```bash
git status --short
```

1. If clean, record `{project: "current", status: "clean"}` and skip to Phase 3
2. If dirty, execute release-ship pipeline (domain-commit → push → **issue** → PR → merge)
3. Issue creation is MANDATORY for shipped commits — do not skip Step 4 of release-ship
4. Capture result: `{commits: [...], issues: [...], pr_url: "...", merged: bool}`

### Phase 3: Release Ship (Managed Projects)

**If `--targets` is set**, only process the specified projects. Otherwise process all 5.

Read project paths from [references/project-registry.md](references/project-registry.md).

**Path resolution**: Each project has two possible paths (`Path (회사)` and `Path (집)`). For each project, try `Path (회사)` first; if that directory does not exist, try `Path (집)`. Use the first path that exists. If neither exists, warn and skip the project.

For each project in order:

```bash
cd PROJECT_PATH    # resolved path from above
git status --short
```

1. If clean, record `{project: ALIAS, status: "clean"}` and move to next
2. If dirty, execute the release-ship pipeline **in pipeline mode**:
   - Follow all release-ship rules (ai-platform-webui uses tmp-only mode)
   - Domain-split commits → push → **issue** → PR → merge
   - Issue creation is MANDATORY — auto-confirm the issue plan (pipeline mode)
3. Capture result per project
4. `cd` back to original directory before processing next project

**Execution order** (from [references/project-registry.md](references/project-registry.md)):

1. `github-to-notion-sync` — full pipeline
2. `ai-template` — full pipeline
3. `ai-model-event-stock-analytics` — full pipeline
4. `research` — full pipeline
5. `ai-platform-webui` — tmp-only mode (commit → push → issue → report, no PR/merge)

If a project directory does not exist, warn and skip it. Continue with remaining projects.

### Phase 3½: Pre-Ship Quality Gate

Before posting to Slack, verify shipping integrity:

- [ ] **No unintended files staged** — Check that no `.env`, credentials, or large binary files were committed across any project
- [ ] **All repos clean** — Every shipped project should have a clean `git status` after release-ship (no leftover unstaged changes including untracked files)
- [ ] **No orphaned untracked content** — Verify no `.md`, `.ts`, `.go`, `.py`, `.yaml`, `.json`, `.sql` files remain untracked in `output/`, `docs/`, `ai-platform/`, `scripts/`, `tasks/`, or any content directory. If any exist, run one more `git add` + commit round to catch them.
- [ ] **Branch consistency** — Current project pushed to correct remote branch (ai-platform-webui uses `tmp`, others use standard)
- [ ] **Issue field completeness** — Every issue created in Phase 2/3 MUST have ALL 5 project fields set (Status, Priority, Size, Sprint, Estimate). If any issue is missing fields, run the `set_all_fields()` script from [commit-to-issue/references/project-config.md](../commit-to-issue/references/project-config.md) to fix it before posting to Slack.
- [ ] **GitHub Project #5 등록 검증** — Phase 2/3에서 생성된 모든 이슈와 PR이 GitHub Project #5에 정상 등록되었는지 확인. `gh project item-list 5 --owner ThakiCloud --format json --limit 100` 으로 조회하여 (1) 이슈/PR이 프로젝트 아이템 목록에 존재하는지 (2) 5개 필드(Status, Priority, Size, Sprint, Estimate)가 모두 non-null인지 검증. 누락된 항목은 `gh project item-add` + `set_all_fields()` 로 재시도 1회. 결과를 `{project5_check: {issues: {verified: N, total: M}, prs: {verified: N, total: M}, missing: [...], fields_incomplete: [...]}}` 형태로 기록.
- [ ] **lat.md drift check** — For repos with a `lat.md/` directory, run `lat check` and warn if broken links or drift are detected. Non-blocking: log warnings but do not halt shipping.

If any criterion fails, log the issue in the Slack message as a warning. Do NOT suppress the notification — post with warnings.

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

*dev 브랜치 머지 (ai-platform-webui)*
- origin/dev 머지: N개 커밋 반영 {완료|이미 최신|충돌}

*세션 메모리 동기화*
- N개 트랜스크립트 추출, 인덱스 리빌드 {완료|건너뜀}

*인텔리전스 KB 라우팅*
- research 레포: N개 아티팩트 라우팅, M개 스킵 {완료|건너뜀}

*프로젝트 배포*
- project-a: N개 커밋, <PR_URL|PR #X> 머지 완료
- project-b: 변경사항 없음
- project-c: N개 커밋 (tmp 전용)

*이슈 생성*
- <ISSUE_URL|#N1>, <ISSUE_URL|#N2> → 프로젝트 #5

*GitHub Project #5 검증*
- 이슈 등록: N/N 확인 ✅ (or ⚠️ M개 누락)
- 필드 완성도: N/N 완전 ✅ (or ⚠️ M개 불완전)
- PR 등록: N/N 확인 ✅ (or ⚠️ M개 누락)

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

dev 브랜치 머지 (ai-platform-webui):
  origin/dev → tmp: N개 커밋 머지 완료

세션 메모리 동기화:
  트랜스크립트 추출: N개, 인덱스 리빌드: 완료

인텔리전스 KB 라우팅:
  research 레포: N개 아티팩트 라우팅, M개 스킵

프로젝트:
  github-to-notion-sync:          3개 커밋, PR #12 머지 완료
  ai-template:                    변경사항 없음
  ai-model-event-stock-analytics: 2개 커밋, PR #8 머지 완료
  research:                       1개 커밋, PR #5 머지 완료
  ai-platform-webui:              2개 커밋 (tmp 전용)

이슈: #101, #102, #103, #104 → 프로젝트 #5

GitHub Project #5 검증:
  이슈 등록: 4/4 확인 ✅
  필드 완성도: 4/4 완전 ✅
  PR 등록: 3/3 확인 ✅

슬랙: #효정-할일 채널에 게시 완료

합계: 4/5 프로젝트 배포, 8개 커밋, 4개 이슈
```

## Examples

### Example 1: Full EOD ship

User runs `/eod-ship` at end of day with changes across 3 projects.

1. cursor-sync: 4 targets synced, 6 files updated
1½. dev merge: ai-platform-webui에 origin/dev 5개 커밋 머지 완료
1¾. memory sync: 3개 트랜스크립트 추출, 인덱스 리빌드 완료
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
| Dev merge conflict (ai-platform-webui) | Attempt auto-resolve (theirs for simple, rm for deleted); if unresolvable, abort merge and report conflict files; continue with shipping |
| Dev branch not found | Skip dev merge step; continue with shipping |

## Automation Rules (Pipeline Mode)

- **No confirmation prompts**: This is an automated pipeline. Do NOT ask the user to confirm issue creation, PR creation, or PR merging. Just execute.
- **Issues**: Create issues automatically for all commits. Set ALL 5 project fields (Status, Priority, Size, Sprint, Estimate) using the GraphQL script from project-config.md.
- **PRs**: Create PRs automatically. Merge via `--squash --delete-branch` by default. If merge fails, try `--admin` flag. If still fails, report and continue.
- **No blocking**: If any step fails, log the warning and continue to the next project/phase. Never block the entire pipeline for a single failure.

## Safety Rules

- **Never force push** (`--force`) to any branch in any project
- **Never push directly** to `main` or `dev` in any project
- **Never amend** failed commits; create new ones
- **Never commit** `.env`, credentials, or secret files
- **ai-platform-webui**: Never create PRs or merge — tmp-only mode
- **Always return** to original working directory after processing each project
- **Always post** Slack message as the authenticated user, never impersonate

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, data, context) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must include why the task matters and how its output is used downstream.
- **Continue vs Spawn decision:**
  - Continue (resume) when worker context overlaps with the next task or fixing a previous failure
  - Spawn fresh when verifying another worker's output or when previous approach was fundamentally wrong
- Use `model: "fast"` for exploration/read-only subagents; default model for generation/analysis

## Honest Reporting

- Report phase outcomes faithfully: if a phase fails, say so with the error output
- Never claim "pipeline complete" when phases were skipped or failed
- Never suppress failing phases to manufacture a green summary
- When a phase succeeds, state it plainly without unnecessary hedging
- The Slack summary must accurately reflect what happened — not what was hoped

## Subagent Contract

Subagent prompts must include:
- Always use absolute file paths (subagent cwd may differ)
- Return `{ status, file, summary }` for orchestrator context efficiency
- Include code snippets only when exact text is load-bearing
- Do not recap files merely read — summarize findings
- Final response: concise report of what was done, key findings, files changed
- Do not use emojis
