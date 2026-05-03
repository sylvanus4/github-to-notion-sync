---
name: daily-git-work-report
description: >-
  Summarize yesterday and today's GitHub commits plus agent sessions across
  all 5 managed repositories into a structured Korean report with
  remaining-work status. Posts to Slack and saves to disk. Use when the user
  asks to "daily work report", "yesterday today work summary", "git work
  report", "어제 오늘 작업 정리", "일일 작업 보고", "깃 작업 요약", "작업 내역 정리", "어제 오늘 작업한 내용
  정리", "daily git work report", or wants a consolidated summary of recent
  development activity across projects. Do NOT use for weekly status reports
  (use weekly-status-report), sprint-level GitHub platform events like
  PRs/issues/reviews (use github-sprint-digest), agent skill usage analytics
  (use daily-skill-digest), or engineering health metrics like bus factor and
  test ratio (use engineering-retro).
---

# Daily Git Work Report

Summarize yesterday and today's GitHub commits plus agent sessions across all 5 managed repositories into a structured Korean report with remaining-work status. Posts to Slack and saves to disk.

Use when the user asks to "daily work report", "yesterday today work summary", "git work report", "어제 오늘 작업 정리", "일일 작업 보고", "깃 작업 요약", "작업 내역 정리", "어제 오늘 작업한 내용 정리", "daily git work report", or wants a consolidated summary of recent development activity across projects.

Do NOT use for weekly status reports (use `weekly-status-report`), sprint-level GitHub platform events like PRs/issues/reviews (use `github-sprint-digest`), agent skill usage analytics (use `daily-skill-digest`), or engineering health metrics like bus factor and test ratio (use `engineering-retro`).

---

## Quick Reference

- **In scope**: Multi-repo `git log` (default since yesterday 00:00 local), agent transcript first-user lines, per-repo dirty/unpushed status, Korean markdown report, `outputs/daily-git-work-report/`, Slack `#효정-할일`.
- **Route elsewhere**: weekly cadence → `weekly-status-report`; PR/issue digests → `github-sprint-digest`; skill usage stats → `daily-skill-digest`; engineering health retro → `engineering-retro`.


## Repository Registry

| Repo | Path | Branch |
|---|---|---|
| ai-platform-strategy | `/Users/hanhyojung/thaki/ai-platform-strategy` | `main` |
| github-to-notion-sync | `/Users/hanhyojung/thaki/github-to-notion-sync` | `main` |
| ai-template | `/Users/hanhyojung/thaki/ai-template` | `main` |
| ai-model-event-stock-analytics | `/Users/hanhyojung/thaki/ai-model-event-stock-analytics` | `main` |
| research | `/Users/hanhyojung/thaki/ai-platform-strategy` | `main` |

Submodule status for `ai-platform-strategy` is included when changes are detected in `ai-suite`, `thaki-ui`, or `ai-platform-webui`.

---



> **Subset-repo requests**: If the user names fewer than five repos, still evaluate all five unless they explicitly ask to *exclude* repositories; emphasize named repos in Overview Highlights.

## Workflow

### Phase 0: Environment

Source `.env` so `GITHUB_TOKEN` and `SLACK_USER_TOKEN` are available:

```bash
set -a
source /Users/hanhyojung/thaki/ai-platform-strategy/.env 2>/dev/null || true
set +a
```

### Phase 1: Collect

Run in parallel for each repo:

#### 1a. Git Log

```bash
git -C <REPO_PATH> log --all --oneline \
  --since="<YESTERDAY> 00:00" \
  --format="%h %ad %s" --date=format:"%m-%d %H:%M"
```

Default time window: yesterday 00:00 to now. Configurable via `--since` / `--until` arguments if the user specifies a different range.

#### 1b. Agent Transcript Sessions

Read recent `.jsonl` files from `agent-transcripts/`:

```
/Users/hanhyojung/.cursor/projects/Users-hanhyojung-thaki-ai-platform-strategy/agent-transcripts/
```

For each file modified within the time window:
1. Read the file line by line.
2. Parse each line as JSON.
3. Find the **first** entry with `"role": "user"`.
4. Extract the `content` field (may be a string or a list of objects — if a list, concatenate text parts).
5. Truncate to 120 characters for the summary table.
6. Record the file modification timestamp as the session time.

#### 1c. Remaining Work

Per repo:

```bash
git -C <REPO_PATH> status --porcelain
git -C <REPO_PATH> log @{u}..HEAD --oneline 2>/dev/null
```

- Dirty files → listed as uncommitted changes.
- Unpushed commits → listed with commit messages.

### Phase 2: Analyze

1. **Merge & Sort**: Combine all commits from all repos into a single chronological list, tagging each with its repo name.
2. **Classify**: Group commits by repo. Within each repo section, list commits in reverse-chronological order (newest first).
3. **Extract Sessions**: List agent sessions in reverse-chronological order with their first user message as the description.
4. **Remaining Work**: Aggregate dirty files and unpushed commits per repo.

### Phase 3: Output

#### 3a. Generate Korean Markdown Report

Produce a report following this structure:

```markdown
## 1. 개요 (Overview)
- **기간**: YYYY-MM-DD ~ YYYY-MM-DD
- **레포 수**: N개
- **총 커밋 수**: N건
- **주요 하이라이트**: (1-2 sentence summary of most significant changes)

## 2. 레포별 커밋 내역 (Per-Repo Commits)

### repo-name (N건)
| 시간 | 커밋 | 내용 |
|---|---|---|
| MM-DD HH:MM | abc1234 | commit message |

(Repeat for each repo with commits. Skip repos with 0 commits.)

## 3. 에이전트 세션별 작업 (Agent Sessions)
| 시간 | 세션 | 작업 내용 |
|---|---|---|
| MM-DD HH:MM | <6-word title> | first user message (truncated) |

(If no sessions found, display "기간 내 에이전트 세션 없음")

## 4. 남은 작업 (Remaining Work)
| 레포 | 항목 | 상태 | 설명 |
|---|---|---|---|
| repo-name | uncommitted files | ⚠️ 미커밋 | N개 파일 |
| repo-name | unpushed commits | 📤 미푸시 | N건 |

(If all repos are clean, display "모든 레포 클린 상태 ✅")

## 5. 요약 (Executive Summary)
- (3-5 bullet points of key accomplishments)
- (Any blockers or items requiring attention)
```

#### 3b. Save to Disk

```
outputs/daily-git-work-report/{YYYY-MM-DD}.md
```

Create the directory if it does not exist.

#### 3c. Post to Slack

Post the report to `#효정-할일` via Slack MCP `slack_send_message`.

If the report exceeds 3000 characters, split into:
- **Message 1**: Sections 1 + 2 (overview + commits)
- **Thread reply**: Sections 3 + 4 + 5 (sessions + remaining + summary)

---

## Error Handling

| Scenario | Behavior |
|---|---|
| Repo directory does not exist | Skip repo, note in report as "⚠️ 디렉토리 없음" |
| No commits in time window | Skip repo from commits section, include in overview count as 0 |
| No agent transcripts directory | Skip section 3, display "에이전트 트랜스크립트 디렉토리 없음" |
| Transcript JSONL parse error | Skip file, log warning |
| Slack MCP unavailable | Save report to disk only, warn user |
| Git command fails | Log error, continue with remaining repos |

---

## Examples

**User**: "어제 오늘 작업한 깃헙 내용을 정리해서 요약 보고해줘"

**Agent**:
1. Sources `.env`.
2. Runs `git log --since` across 5 repos in parallel.
3. Scans `agent-transcripts/` for recent sessions.
4. Checks `git status` and unpushed commits per repo.
5. Generates Korean markdown report.
6. Saves to `outputs/daily-git-work-report/2026-04-22.md`.
7. Posts to Slack `#효정-할일`.

**User**: "지난 3일간 작업 정리해줘"

**Agent**: Same workflow with `--since="3 days ago"`.
