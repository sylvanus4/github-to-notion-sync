---
name: daily-skill-digest
description: >
  Extract daily coding patterns, skill usage statistics, per-project activity,
  and skill category breakdowns from ALL Cursor project agent transcripts and
  git logs, then synthesize a Korean summary for Slack distribution. Supports
  `--project=NAME` filter for single-project mode. Use when the user asks to
  "daily digest", "daily skill digest", "오늘 코딩 패턴", "일일 스킬 요약",
  "daily coding stats", "daily-skill-digest", "프로젝트별 스킬 사용량",
  "skill category breakdown", or when invoked as Phase 3.75 of eod-ship.
  Do NOT use for general session recall (use recall), weekly status reports
  (use weekly-status-report), or GitHub-only activity digests (use
  github-sprint-digest).
metadata:
  author: thaki
  version: "2.0.0"
  category: pipeline
triggers:
  - daily digest
  - daily skill digest
  - daily coding stats
  - 오늘 코딩 패턴
  - 일일 스킬 요약
  - 일일 코딩 통계
  - daily-skill-digest
  - /daily-digest
  - 프로젝트별 스킬 사용량
  - skill category breakdown
  - 스킬 카테고리 분석
---

# daily-skill-digest

Extract today's coding patterns, skill usage, per-project activity, and skill
category breakdowns from ALL Cursor project agent transcripts and git history,
then produce a compact Korean summary suitable for Slack threading.

## Data Source

`scripts/daily_skill_digest.py` — deterministic Python extractor (Fat Code).
Auto-discovers ALL Cursor project transcript directories under
`~/.cursor/projects/*/agent-transcripts/`.

Run it first and use its JSON output as the single source of truth for all
numbers referenced below.

```bash
python scripts/daily_skill_digest.py --pretty
python scripts/daily_skill_digest.py --pretty --project=ai-platform-strategy
```

## Execution Steps

### 1. Run the Extractor

```bash
python scripts/daily_skill_digest.py --save --pretty
```

`--save` persists to `outputs/daily-digest/{date}-digest.json`.

Optional: `--project=NAME` filters to transcripts from a specific project only
(partial match supported, e.g. `--project=ai-platform`).

Capture the JSON output into a variable for synthesis.

### 2. Synthesize Korean Summary

Read the JSON output and produce a concise Korean narrative covering:

- **Productivity snapshot**: session count, total tool calls, commit count
- **Top 5 skills** used with invocation count
- **Skill categories**: top categories (pipeline, review, automation, etc.)
  with aggregate invocation count — derive the day's focus from the dominant
  category (e.g. pipeline-heavy = 파이프라인 운영 중심, review-heavy = 코드 리뷰 중심)
- **Per-project activity**: sessions and tool calls per project — highlight
  which project received the most attention
- **Top 5 tool chains** (recurring patterns from SPM)
- **File activity** heatmap by FSD layer / directory
- **Coding pattern** observation — one sentence characterizing the day using
  category-aware language:
  - pipeline-dominant: "파이프라인 오케스트레이션과 자동화에 집중한 하루"
  - review-dominant: "코드 리뷰와 품질 개선에 집중한 하루"
  - frontend-dominant: "프론트엔드 FSD 개발에 집중한 하루"
  - research-dominant: "리서치와 논문 분석 중심의 하루"
  - mixed: "다양한 도메인을 넘나드는 멀티태스킹 하루"

### 3. Format Slack mrkdwn

Use this template:

```
:bar_chart: *Daily Coding Digest — {date}*

*Sessions:* {n} | *Tool Calls:* {n} | *Commits:* {n} (+{added}/-{removed})

*Top Skills:*
{ranked list, max 5, format: `1. \`skill-name\` — N invocations`}

*Skill Categories:*
{ranked list, max 5, format: `• \`category\` — N invocations`}

*Per-Project Activity:*
{ranked list, all projects, format: `• \`project-name\` — N sessions, N tool calls`}

*Top Tool Chains:*
{ranked list, max 5, format: `• Tool1 → Tool2 → Tool3 (×N)`}

*File Activity:*
{ranked list, max 5 categories, format: `• \`directory/\` — N files`}

*Pattern:* {one-sentence Korean characterization, category-aware}
```

If a section has zero items, omit that section entirely.

### 4. Output

Return the formatted Slack mrkdwn string and the raw JSON path.

When invoked by eod-ship (Phase 3.75), the caller captures this mrkdwn and posts
it as a thread reply to the main eod-ship Slack message.

When invoked standalone (`/daily-digest`), post directly to `#효정-할일`
(`C0AA8NT4T8T`).

## Examples

**Standalone invocation**:
```
User: "오늘 코딩 패턴 정리해줘"
→ Runs `python scripts/daily_skill_digest.py --save --pretty`
→ Synthesizes Korean summary from JSON
→ Posts formatted mrkdwn to #효정-할일
```

**Single-project filter**:
```
User: "daily digest --project=ai-platform"
→ Runs `python scripts/daily_skill_digest.py --save --pretty --project=ai-platform`
→ Omits Per-Project Activity section (single project)
→ Returns filtered summary
```

**As eod-ship Phase 3.75**:
```
eod-ship invokes daily-skill-digest
→ Returns formatted mrkdwn string
→ eod-ship posts it as a Slack thread reply to the main message
```

## Edge Cases

- **No transcripts today**: Return a minimal message:
  `":bar_chart: *Daily Coding Digest — {date}*\n\n오늘 에이전트 세션이 없습니다."`
- **No git commits**: Omit the `+added/-removed` part and set commits to 0.
- **Script failure**: Report the error and skip the digest gracefully.
- **Single-project mode**: When `--project=NAME` is used, omit the Per-Project
  Activity section (only one project) and adjust the pattern sentence to
  reference that project specifically.
- **Multi-project with zero skills**: Some projects may have sessions but no
  detected skill invocations — show them in Per-Project Activity with 0 skills.

## Skill Detection Heuristics

The extractor identifies skill invocations through 4 heuristics:

1. **Read/Skill tool on SKILL.md paths**: Direct file reads of `.cursor/skills/*/SKILL.md`
2. **Task tool prompt parsing**: Skill references in `Task` tool `input.prompt`
3. **SemanticSearch on skill paths**: `SemanticSearch` calls targeting `.cursor/skills/`
4. **Skill tool invocations**: Calls to the `Skill` tool from hooks/plugins

## File Layout

```
scripts/daily_skill_digest.py        # Deterministic extractor (Fat Code)
outputs/daily-digest/{date}-digest.json  # Persisted daily output
.cursor/skills/pipeline/daily-skill-digest/SKILL.md  # This skill
.cursor/commands/daily-digest.md     # Standalone command
```
