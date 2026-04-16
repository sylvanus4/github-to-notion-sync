---
name: daily-skill-digest
description: >
  Extract daily coding patterns and skill usage statistics from agent transcripts
  and git logs, then synthesize a Korean summary for Slack distribution. Use when
  the user asks to "daily digest", "daily skill digest", "오늘 코딩 패턴", "일일
  스킬 요약", "daily coding stats", "daily-skill-digest", or when invoked as
  Phase 3.75 of eod-ship. Do NOT use for general session recall (use recall),
  weekly status reports (use weekly-status-report), or GitHub-only activity
  digests (use github-sprint-digest).
triggers:
  - daily digest
  - daily skill digest
  - daily coding stats
  - 오늘 코딩 패턴
  - 일일 스킬 요약
  - 일일 코딩 통계
  - daily-skill-digest
  - /daily-digest
---

# daily-skill-digest

Extract today's coding patterns and skill usage from agent transcripts and git
history, then produce a compact Korean summary suitable for Slack threading.

## Data Source

`scripts/daily_skill_digest.py` — deterministic Python extractor (Fat Code).

Run it first and use its JSON output as the single source of truth for all
numbers referenced below.

```bash
python scripts/daily_skill_digest.py --pretty
```

## Execution Steps

### 1. Run the Extractor

```bash
python scripts/daily_skill_digest.py --save --pretty
```

`--save` persists to `outputs/daily-digest/{date}-digest.json`.

Capture the JSON output into a variable for synthesis.

### 2. Synthesize Korean Summary

Read the JSON output and produce a concise Korean narrative covering:

- **Productivity snapshot**: session count, total tool calls, commit count
- **Top 5 skills** used with invocation count
- **Top 5 tool chains** (recurring patterns from SPM)
- **File activity** heatmap by FSD layer / directory
- **Coding pattern** observation — one sentence characterizing the day
  (e.g. "프론트엔드 FSD 개발에 집중한 하루", "리뷰와 리팩토링 중심의 하루")

### 3. Format Slack mrkdwn

Use this template:

```
:bar_chart: *Daily Coding Digest — {date}*

*Sessions:* {n} | *Tool Calls:* {n} | *Commits:* {n} (+{added}/-{removed})

*Top Skills:*
{ranked list, max 5, format: `1. \`skill-name\` — N invocations`}

*Top Tool Chains:*
{ranked list, max 5, format: `• Tool1 → Tool2 → Tool3 (×N)`}

*File Activity:*
{ranked list, max 5 categories, format: `• \`directory/\` — N files`}

*Pattern:* {one-sentence Korean characterization}
```

If a section has zero items, omit that section entirely.

### 4. Output

Return the formatted Slack mrkdwn string and the raw JSON path.

When invoked by eod-ship (Phase 3.75), the caller captures this mrkdwn and posts
it as a thread reply to the main eod-ship Slack message.

When invoked standalone (`/daily-digest`), post directly to `#효정-할일`
(`C0AA8NT4T8T`).

## Edge Cases

- **No transcripts today**: Return a minimal message:
  `":bar_chart: *Daily Coding Digest — {date}*\n\n오늘 에이전트 세션이 없습니다."`
- **No git commits**: Omit the `+added/-removed` part and set commits to 0.
- **Script failure**: Report the error and skip the digest gracefully.

## File Layout

```
scripts/daily_skill_digest.py        # Deterministic extractor (Fat Code)
outputs/daily-digest/{date}-digest.json  # Persisted daily output
.cursor/skills/pipeline/daily-skill-digest/SKILL.md  # This skill
.cursor/commands/daily-digest.md     # Standalone command
```
