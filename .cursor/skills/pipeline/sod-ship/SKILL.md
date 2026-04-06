---
name: sod-ship
description: >-
  Start-of-day git sync pipeline: commit dirty working directories, push
  unpushed commits, pull remote changes for all 5 managed projects, then
  run cursor-sync to propagate .cursor/ assets across all repos. Use when
  the user runs /sod-ship, asks to "sync all projects", "start of day sync",
  "pull all repos", "컴퓨터 바꿔서 작업 시작", "아침 싱크", "프로젝트 동기화",
  "sod-ship", or needs to ensure all repos are clean and up-to-date before
  starting work. Do NOT use for end-of-day shipping (use eod-ship), morning
  briefing with Google/stock pipelines (use morning-ship), or syncing
  .cursor/ assets only (use cursor-sync).
metadata:
  author: "thaki"
  version: "1.1.0"
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
/sod-ship --skip-doctor            # skip Phase 0 environment pre-flight diagnostics
/sod-ship --skip-push              # pull only, skip committing/pushing local changes
/sod-ship --skip-pull              # commit and push only, skip pulling remote
/sod-ship --targets research       # process specific projects only (comma-separated)
/sod-ship --no-slack               # skip Slack notification
/sod-ship --no-canvas              # skip Slack Canvas update (Phase 7b)
/sod-ship --dry-run                # preview only (show status, no git operations)
```

Arguments can be combined freely. Defaults: commit+push+pull all, run pre-flight, post to Slack, update canvas.

## Workflow

### Phase 0: Environment Pre-flight

**Skip if** `--skip-doctor` flag is set.

Run lightweight environment diagnostics and live MCP connectivity probes before starting git operations. Results are stored in a `preflight` map and surfaced in the Slack notification (Phase 5) and Chat Report (Phase 6).

#### Step 0a: CLI & Environment Checks

Verify critical CLI tools exist on `$PATH`:

```bash
which git && git --version
which rsync
which node
which python3
```

Check essential environment variables:

```bash
test -n "$GITHUB_TOKEN" && echo "GITHUB_TOKEN set" || echo "GITHUB_TOKEN missing"
test -n "$SLACK_USER_TOKEN" && echo "SLACK_USER_TOKEN set" || echo "SLACK_USER_TOKEN missing"
```

Record results: `{cli: {git: "2.44.0", rsync: true, node: true, python3: true}, env: {GITHUB_TOKEN: true, SLACK_USER_TOKEN: false}}`.

#### Step 0b: Live MCP Connectivity Probes

Probe all 13 registered MCP servers by calling a lightweight read-only tool on each. Run probes **in parallel batches** (max 4 concurrent) using the Task tool with `model: "fast"`.

Each probe calls `CallMcpTool` with the parameters below. If the call returns a successful response, classify as `CONNECTED`. If it throws an error or times out, classify as `DISCONNECTED`.

| # | MCP Server | Probe Tool | Arguments | Priority |
|---|------------|-----------|-----------|----------|
| 1 | `plugin-slack-slack` | `slack_search_channels` | `{"query": "general", "limit": 1}` | Critical |
| 2 | `plugin-notion-workspace-notion` | `mcp_auth` | `{}` | Critical |
| 3 | `user-Notion` | `mcp_auth` | `{}` | Critical |
| 4 | `user-GitHub` | `get_me` | `{}` | Critical |
| 5 | `user-notebooklm-mcp` | `notebook_list` | `{"max_results": 1}` | Normal |
| 6 | `user-Context7` | `resolve-library-id` | `{"query": "test", "libraryName": "react"}` | Normal |
| 7 | `plugin-context7-plugin-context7` | `resolve-library-id` | `{"query": "test", "libraryName": "react"}` | Normal |
| 8 | `user-Figma` | `whoami` | `{}` | Normal |
| 9 | `plugin-figma-figma` | `whoami` | `{}` | Normal |
| 10 | `cursor-ide-browser` | `browser_tabs` | `{"action": "list"}` | Normal |
| 11 | `user-daiso-mcp` | `daiso_search_products` | `{"query": "test"}` | Normal |
| 12 | `user-public-apis` | `get_category_list` | `{}` | Normal |
| 13 | `plugin-huggingface-skills-huggingface-skills` | `mcp_auth` | `{}` | Normal |

**Classification logic**: Any response (even an empty list or auth prompt) counts as `CONNECTED`. Only errors (connection refused, timeout, server not found) count as `DISCONNECTED`.

#### Step 0b-2: ATG Gateway Probe

Check if the Agent Tool Gateway Docker container is running and healthy:

```bash
curl -sf --max-time 3 http://localhost:4000/api/v1/health >/dev/null 2>&1 \
  && echo "CONNECTED" || echo "DISCONNECTED"
```

ATG is an **optional accelerator** — classify as `CONNECTED` or `DISCONNECTED` but never block the pipeline. When healthy, Notion/Slack/GitHub tool calls benefit from caching, deduplication, and compression via the `atg-routing` rule.

Add ATG status to the preflight map under `atg: {status: "CONNECTED"|"DISCONNECTED"}`.

If `DISCONNECTED` and Docker is available, optionally attempt to start ATG:

```bash
cd ai-platform/agent-tool-gateway
docker compose -f docker-compose.monitoring.yml up -d agent-tool-gateway 2>/dev/null
sleep 3
curl -sf --max-time 3 http://localhost:4000/api/v1/health >/dev/null 2>&1 \
  && echo "ATG started successfully" || echo "ATG start failed (non-blocking)"
cd -
```

#### Step 0c: Build Pre-flight Report

Aggregate results into a `preflight` map:

```
preflight:
  cli:
    git: "2.44.0"
    rsync: true
    node: true
    python3: true
  env:
    GITHUB_TOKEN: true
    SLACK_USER_TOKEN: false
  mcp:
    connected: ["plugin-slack-slack", "user-GitHub", ...]
    disconnected: ["user-notebooklm-mcp", "user-Notion"]
    connected_count: 11
    disconnected_count: 2
  atg:
    status: "CONNECTED"  # or "DISCONNECTED"
  work_items:
    - "⚠️ SLACK_USER_TOKEN 환경 변수 미설정 — orphan cleaner, file upload 불가"
    - "❌ user-notebooklm-mcp 연결 끊김 — NLM 스킬 사용 불가, MCP 서버 재시작 필요"
    - "❌ user-Notion 연결 끊김 — Notion 스킬 사용 불가, MCP 서버 재시작 필요"
```

**Work item generation rules**:
- Missing CLI tool → `"❌ {tool} 미설치 — {impact}"`
- Missing env var → `"⚠️ {var} 환경 변수 미설정 — {impact}"`
- Disconnected Critical MCP → `"❌ {server} 연결 끊김 — {impact}, MCP 서버 재시작 필요"`
- Disconnected Normal MCP → `"⚠️ {server} 연결 끊김 — {feature} 사용 불가"`

Display a summary table in the chat:

```
SOD 환경 Pre-flight
=====================
CLI: git=2.44.0  rsync=✅  node=✅  python3=✅
ENV: GITHUB_TOKEN=✅  SLACK_USER_TOKEN=❌

MCP 연결 상태 (11/13 연결됨):
  ✅ plugin-slack-slack, user-GitHub, plugin-notion-workspace-notion, ...
  ❌ user-notebooklm-mcp, user-Notion

ATG Gateway: ✅ HEALTHY (Notion/Slack/GitHub 캐싱 활성)

작업 필요 항목:
  1. ⚠️ SLACK_USER_TOKEN 환경 변수 미설정
  2. ❌ user-notebooklm-mcp 연결 끊김
  3. ❌ user-Notion 연결 끊김
```

**Phase 0 does NOT block** the pipeline. Even if all MCPs are disconnected, proceed to Phase 1. Diagnostic results are advisory and surfaced in Phase 5/6 reports.

### Phase 1: Pre-flight Scan

Scan all managed projects to build a status map before making any changes.

**If `--targets` is set**, only scan the specified projects. Otherwise scan all 5.

Read project paths from [eod-ship project-registry.md](../eod-ship/references/project-registry.md).

**Path resolution**: Each project has two possible paths (`Path (회사)` and `Path (집)`). For each project, try `Path (회사)` first; if that directory does not exist, try `Path (집)`. Use the first path that exists. If neither exists, mark the project as SKIPPED and continue with others.

For each project in order:

```bash
cd PROJECT_PATH    # resolved path from above
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
   - `git status --short | sort` to list all changes (both modified `M` AND untracked `??` files)
   - Categorize files by directory prefix into domain batches using the mapping in [domain-commit references](../domain-commit/references/hooks-and-domains.md)
   - **Critical**: Include ALL untracked content files (`??` entries) — especially `output/`, `docs/`, `ai-platform/`, `scripts/`, `tasks/` directories. Files not matching any domain go to `[chore]` catch-all batch. Never silently skip untracked files.
   - For each batch, `git add <files>` and commit with `[TYPE] Summary` format (HEREDOC)
   - If pre-commit hooks fail: fix lint errors, re-stage, create new commit (never amend)
   - For projects without `.pre-commit-config.yaml`: simple `git add -A && git commit`
3. Verify: `git status --short` must be empty. If any files remain, stage and commit them as `[chore] Add remaining files`

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

#### Step 3c: Merge dev into tmp (ai-platform-webui only)

After pulling from `tmp`, merge the latest `origin/dev` into the current branch to keep it up-to-date with the main development branch. This step only applies to `ai-platform-webui`.

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

If `ai-platform-webui` was not processed (SKIPPED or `--targets` excluded it), skip this step.

#### Step 3d: Retry deferred push

If `push_deferred: true` from Phase 2 and pull succeeded:

```bash
# ai-platform-webui
git push origin HEAD:tmp

# Other repos
git push origin HEAD
```

If retry push still fails, record the error and continue.

#### Step 3e: Push dev-merge result (ai-platform-webui only)

If Step 3c produced new merge commits, push them to `tmp`:

```bash
git push origin HEAD:tmp
```

### Phase 3f: Intelligence KB Routing (Research Repo)

After pulling the research repo, route any new intelligence artifacts (received from other machines via git pull) to Karpathy KB topics. Skip if the research repo was not pulled or does not exist.

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
if [ -d "$RESEARCH_REPO" ] && [ -f "$RESEARCH_REPO/scripts/intelligence/kb_intel_router.py" ]; then
    python3 "$RESEARCH_REPO/scripts/intelligence/kb_intel_router.py"
fi
```

If new artifacts were routed, commit the KB changes and push:

```bash
cd "$RESEARCH_REPO"
git add knowledge-bases/
git diff --cached --quiet || git commit -m "chore: route intelligence artifacts to KB"
git push origin HEAD
cd -
```

Record result: `{intel_routing: "ok", routed: N}` or `{intel_routing: "skipped"}`.

On failure: Warn and continue. Does not block the SOD pipeline.

### Phase 3g: lat.md Drift Check

For each project that has a `lat.md/` directory:

```bash
cd PROJECT_PATH
[ -d "lat.md" ] && lat check || true
```

Record per-project result: `{lat_check: "pass"|"warnings"|"errors"|"no_lat_dir"}`.

Non-blocking: log warnings in the Slack and chat reports but do not halt the pipeline.

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

### Phase 4½: GitHub Project #5 Verification

After sync verification, check that any recently created issues and PRs (within the last 24 hours) across the 5 managed repos are properly registered on GitHub Project #5 with complete fields.

```bash
# 1. List recent issues/PRs for the main repo
gh issue list --repo ThakiCloud/ai-model-event-stock-analytics --state all --json number,url,createdAt --limit 20
gh pr list --repo ThakiCloud/ai-model-event-stock-analytics --state all --json number,url,createdAt --limit 10

# 2. Filter to items created in the last 24 hours

# 3. Check Project #5 registration
gh project item-list 5 --owner ThakiCloud --format json --limit 100
```

For each recent issue/PR:
1. Verify it appears in the Project #5 item list
2. Verify all 5 fields (Status, Priority, Size, Sprint, Estimate) have non-null values

If any item is missing from Project #5, add it with `gh project item-add 5 --owner ThakiCloud --url $ITEM_URL` and run `set_all_fields()` from [commit-to-issue/references/project-config.md](../../review/commit-to-issue/references/project-config.md). Retry once if the first attempt fails.

Record verification result:

```json
{
  "project5_check": {
    "issues": { "verified": N, "total": M, "missing": [] },
    "prs": { "verified": N, "total": M, "missing": [] },
    "fields_incomplete": []
  }
}
```

Non-blocking: if `gh project` commands fail (auth issues, API limits), log the error and continue to Phase 5. Include the failure in the Slack notification.

### Phase 5: Slack Notification

**Skip if** `--no-slack` or `--dry-run` flag is set.

Post a consolidated summary to `#효정-할일` using the `plugin-slack-slack` MCP server's `slack_send_message` tool. Use **threaded replies** — main summary first, then per-project details in thread.

#### Step 5a: Main Message

Call `CallMcpTool` with:

```json
{
  "server": "plugin-slack-slack",
  "toolName": "slack_send_message",
  "arguments": {
    "channel_id": "C0AA8NT4T8T",
    "message": "<main summary message>"
  }
}
```

**Main message template** (standard markdown):

```
**🔄 SOD Git 동기화 리포트** (YYYY-MM-DD)

{if Phase 0 ran:
**🩺 환경 Pre-flight**
- MCP 연결: ✅ N/13 연결 {if disconnected_count > 0: | ❌ M/13 끊김}
- ATG Gateway: {✅ HEALTHY | ⚠️ UNREACHABLE} (선택적 가속기)
{if work_items non-empty: - ⚠️ 작업 필요 항목 N건 (쓰레드 참조)}
}

**로컬 → 리모트 (커밋 & 푸시)**
- project-a: N개 커밋 생성, 푸시 완료
- project-b: 변경사항 없음

**리모트 → 로컬 (Pull)**
- project-a: N개 커밋 수신
- project-b: 이미 최신

**dev 브랜치 머지 (ai-platform-webui)**
- origin/dev 머지: N개 커밋 반영 {완료|충돌|스킵}

**인텔리전스 KB 라우팅**
- research 레포: N개 아티팩트 라우팅 {완료|건너뜀}

**커서 동기화**
- N개 파일 Pull → research 허브, M개 파일 Push → 4개 타겟
- 검증: commands=X  skills=Y  rules=Z (5개 레포 동일)

**GitHub Project #5 검증**
- 이슈 등록: N/N 확인 ✅ (or ⚠️ M개 누락)
- 필드 완성도: N/N 완전 ✅ (or ⚠️ M개 불완전)
- PR 등록: N/N 확인 ✅ (or ⚠️ M개 누락)

**결과**
- ✅ SYNCED: N/5 | ⚠️ PARTIAL: N/5 | ❌ FAILED: N/5
- 총 커밋: 생성 N개, 수신 M개
```

**Save** the returned `message.ts` timestamp from the response — it is needed for threaded replies.

#### Step 5b: Pre-flight Work Items Thread

**Skip if** Phase 0 was skipped (`--skip-doctor`) or `work_items` list is empty.

Post a threaded reply with the full pre-flight diagnostics:

```json
{
  "server": "plugin-slack-slack",
  "toolName": "slack_send_message",
  "arguments": {
    "channel_id": "C0AA8NT4T8T",
    "thread_ts": "<ts from Step 5a>",
    "message": "<pre-flight details>"
  }
}
```

**Pre-flight thread template**:

```
**🩺 SOD 환경 Pre-flight 상세**

**CLI 도구**: git={version}  rsync={✅|❌}  node={✅|❌}  python3={✅|❌}
**환경 변수**: GITHUB_TOKEN={✅|❌}  SLACK_USER_TOKEN={✅|❌}

**MCP 연결 상태** ({connected_count}/{total} 연결됨)
✅ 연결됨: server1, server2, ...
{if disconnected: ❌ 끊김: server-a, server-b, ...}

**작업 필요 항목**
{for each work_item:
{number}. {work_item}
}
```

#### Step 5c: Per-Project Threaded Details

For each project that had activity (not "변경사항 없음" / "이미 최신"), post a threaded reply with details:

```json
{
  "server": "plugin-slack-slack",
  "toolName": "slack_send_message",
  "arguments": {
    "channel_id": "C0AA8NT4T8T",
    "thread_ts": "<ts from Step 5a>",
    "message": "<per-project detail>"
  }
}
```

**Thread message template** per project:

```
**📂 {project-name}** — {SYNCED|PARTIAL|FAILED}

Push: N개 커밋 생성 → 푸시 {완료|실패|스킵}
Pull: M개 커밋 수신 → {fast-forward|rebase|충돌}
브랜치: {branch-name}
{충돌 파일이 있으면: 충돌 파일: file1.md, file2.py (수동 해결 필요)}
```

Omit thread replies for projects with no activity on either direction (push or pull).

#### Slack Message Rules

- Use `**bold**` (standard markdown, the MCP tool converts automatically)
- Use standard markdown links `[text](url)` for any links
- Write all message text in Korean (한국어)
- Omit sections with no data (e.g., no Push section if `--skip-push`)
- Keep each message under 5000 chars
- If all projects are already in sync, post a single message: `**🔄 SOD Git 동기화 리포트** (YYYY-MM-DD)\n\n모든 프로젝트 동기화 완료 — 변경사항 없음 ✅`

### Phase 6: Chat Report

Display the consolidated summary in the chat as a formatted Korean report, using the Phase 4 verification table as the base. If Phase 0 ran, prepend the environment diagnostics section.

```
SOD 동기화 리포트
==================
날짜: YYYY-MM-DD

{if Phase 0 ran:
환경 Pre-flight:
  CLI:  git={version}  rsync=✅  node=✅  python3=✅
  ENV:  GITHUB_TOKEN=✅  SLACK_USER_TOKEN=❌
  MCP:  11/13 연결됨
    ✅ plugin-slack-slack, user-GitHub, plugin-notion-workspace-notion, ...
    ❌ user-notebooklm-mcp, user-Notion
  작업 필요 항목:
    1. ⚠️ SLACK_USER_TOKEN 환경 변수 미설정
    2. ❌ user-notebooklm-mcp 연결 끊김
    3. ❌ user-Notion 연결 끊김
}

로컬 → 리모트:
  github-to-notion-sync:          변경사항 없음
  ai-template:                    2개 커밋 생성, 푸시 완료
  ai-model-event-stock-analytics: 3개 커밋 생성, 푸시 완료
  research:                       변경사항 없음
  ai-platform-webui:              5개 커밋 생성, 푸시 완료 (tmp)

리모트 → 로컬:
  github-to-notion-sync:          3개 커밋 수신
  ai-template:                    이미 최신
  ai-model-event-stock-analytics: 1개 커밋 수신
  research:                       2개 커밋 수신
  ai-platform-webui:              4개 커밋 수신

dev 브랜치 머지 (ai-platform-webui):
  origin/dev → tmp: N개 커밋 머지 완료

인텔리전스 KB 라우팅:
  research 레포: N개 아티팩트 라우팅, M개 스킵

커서 동기화:
  Pull: N개 파일 → research 허브
  Push: M개 파일 → 4개 타겟
  검증: commands=426  skills=498  rules=34 (5개 레포 동일)

GitHub Project #5 검증:
  이슈 등록: N/N 확인 ✅
  필드 완성도: N/N 완전 ✅
  PR 등록: N/N 확인 ✅

결과: SYNCED 5/5, PARTIAL 0/5, FAILED 0/5
슬랙: #효정-할일 채널에 게시 완료

합계: 10개 커밋 생성, 10개 커밋 수신
```

### Phase 7: Post-Sync Actions

**Skip if** `--dry-run` is set, or if both `--skip-push` AND `--skip-pull` are set.

#### Step 7a: Skill Guide Sync

Run the `skill-guide-generator` skill in `--readme-only` mode to quickly update
counts and tables in `docs/skill-guides/README.md` without generating full guide
sections.

1. Inventory installed skills (glob `.cursor/skills/*/SKILL.md`)
2. Cross-reference against documented skills in `docs/skill-guides/*.md`
3. Update README.md counts and tables
4. Record whether any new undocumented skills were found (`new_skills_found: bool`,
   `new_skill_names: [...]`)

If no changes were made to README.md and no new skills found, log
"Skill guides up to date — no changes" and proceed.

#### Step 7b: Publish to Slack Canvas

**Skip if** `--no-canvas` flag is set, or if there are no changes to report
(all projects were already in sync AND no new skills were found in Step 7a).

Append a dated SOD sync digest to the fixed canvas `F0AN2C7UKCY`:

```json
{
  "server": "plugin-slack-slack",
  "toolName": "slack_update_canvas",
  "arguments": {
    "canvas_id": "F0AN2C7UKCY",
    "action": "append",
    "content": "<dated-digest>"
  }
}
```

**Digest content template** (Canvas markdown):

```
## YYYY-MM-DD SOD Sync

**Git 동기화**
- SYNCED: N/5 프로젝트
- 커밋: 생성 N개, 수신 M개
{if PARTIAL or FAILED: - ⚠️ PARTIAL/FAILED: project-name (details)}

{if new skills found:
**스킬 가이드 업데이트**
- 신규 문서화 스킬: skill-a, skill-b
}
```

Keep each digest entry concise (under 500 chars). The canvas accumulates entries
over time as a running log of daily SOD activities.

### Phase 8: Cursor Sync

**Skip if** `--dry-run` is set, or if `--skip-pull` is set (no new remote content to propagate).

After git pull brings each repo's `.cursor/` assets up to date with its remote,
run `cursor-sync` to propagate any new or updated skills/commands/rules across
all 5 repos via the research merge hub.

Follow the `cursor-sync` skill (`.cursor/skills/automation/cursor-sync/SKILL.md`):

1. **Pull Phase**: `rsync -au` from each of the 4 target repos → research (newest wins)
2. **Push Phase**: `rsync -ac` from research → all 4 target repos (checksum-based)
3. **Verify**: all 5 repos have identical file counts for `commands/`, `skills/`, `rules/`

Record `{cursor_sync: {pulled: N, pushed: M}}` where N = total new files pulled
into research, M = total new files pushed per target.

If cursor-sync encounters errors (missing directories, rsync failures), warn and
continue — it does not block the SOD pipeline.

Include cursor-sync results in the Phase 5 Slack message and Phase 6 Chat Report
under a new **커서 동기화** section:

```
**커서 동기화**
- N개 파일 Pull (research 허브로), M개 파일 Push (4개 타겟으로)
- 검증: commands=X  skills=Y  rules=Z (5개 레포 동일)
```

## Examples

### Example 1: Full SOD sync (typical start-of-day)

User runs `/sod-ship` on a new morning with changes in 2 projects.

1. Pre-flight: scan reveals ai-model-event-stock-analytics has 5 dirty files, ai-platform-webui has 3 unpushed commits, 3 projects need pull
2. Ship local: 2 domain-split commits in analytics project, push both projects
3. Pull remote: 3 projects receive new commits, 2 already up to date
3½. Dev merge: ai-platform-webui에 origin/dev 4개 커밋 머지 → tmp에 푸시
4. Verify: 5/5 SYNCED
5. Slack: main summary posted to #효정-할일, 2 threaded replies for projects with activity
6. Chat report displayed
7. Post-Sync: skill guide sync, canvas update
8. Cursor Sync: pull에서 받은 .cursor/ 에셋 → research 허브 → 4개 타겟 전파

### Example 2: Switching computers (dirty repos everywhere)

User runs `/sod-ship` after switching to a different machine.

1. Pre-flight: 3 projects have uncommitted changes, 2 have unpushed commits, 4 need pull
2. Ship local: commit all dirty repos, push all
3. Pull remote: all 5 receive commits
4. Verify: 5/5 SYNCED
5. Slack: main summary + 5 threaded replies
6. Chat report displayed
7. Post-Sync: skill guide sync, canvas update
8. Cursor Sync: 5개 레포의 .cursor/ 에셋 N-Repo 동기화

### Example 3: Partial pipeline (skip-push or skip-pull)

`/sod-ship --skip-push` — pull only (repos already pushed from other machine). `/sod-ship --skip-pull` — commit and push only (about to switch computers).

### Example 4: Conflict during pull

User runs `/sod-ship` and one project has a merge conflict.

1. Pre-flight: research has 2 behind commits
2. Ship local: no dirty repos
3. Pull: research merge conflict on `README.md` — attempt rebase — rebase also fails — abort and report conflict files
4. Verify: 4/5 SYNCED, 1/5 PARTIAL (research: conflict)
5. Slack: main summary + 1 threaded reply for research (PARTIAL — 충돌 파일 포함)
6. Chat report displayed

### Example 5: All projects in sync (no activity)

User runs `/sod-ship` and every project is already up to date.

1. Pre-flight: all 5 projects clean, no behind commits
2. Ship local: nothing to commit or push
3. Pull remote: all up to date
4. Verify: 5/5 SYNCED
5. Slack: single message "모든 프로젝트 동기화 완료 — 변경사항 없음 ✅" (no threaded replies)
6. Chat report displayed

## Error Handling

| Scenario | Action |
|----------|--------|
| MCP probe times out (>5s) | Classify as `DISCONNECTED`; add to work items; continue probing other servers |
| All MCP probes fail | Report all as disconnected; add blanket reconnection work item; do NOT block git sync |
| setup-doctor prerequisites missing | Add each missing item to work items list; continue with git sync phases |
| Phase 0 itself errors unexpectedly | Log error; skip pre-flight section in Slack/chat report; continue with Phase 1 |
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
| Slack message fails | Report error; still display chat report (Phase 6) |
| Slack thread_ts not returned | Post details as separate channel message instead of thread |
| Dev merge conflict (ai-platform-webui) | Attempt auto-resolve (theirs for simple, rm for deleted); if unresolvable, abort merge and report conflict files; still push tmp changes from Phase 3a |
| Dev branch not found | Skip dev merge step; continue with remaining phases |
| Canvas update fails | Warn and continue; does not affect sync results |
| skill-guide-generator not available | Skip Phase 7a; still attempt Phase 7b with git-only digest |
| cursor-sync fails (Phase 8) | Warn and continue; git sync results are unaffected |
| cursor-sync target directory missing | Skip that target; sync remaining targets |

## Automation Rules (Pipeline Mode)

- **No confirmation prompts**: This is an automated pipeline. Do NOT ask the user to confirm commit creation, push operations, or issue creation. Just execute.
- **Dirty repos**: If a repo has uncommitted changes, auto-commit using domain-commit conventions. Do NOT ask "shall I commit these?".
- **Unpushed commits**: If a repo has unpushed commits, push automatically. Do NOT ask "shall I push?".
- **Issues**: If issues are created (e.g., via commit-to-issue), set ALL 5 project fields automatically using the GraphQL script from project-config.md.
- **No blocking**: If any step fails, log the warning and continue to the next project/phase.

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
