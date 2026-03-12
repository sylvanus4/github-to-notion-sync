---
name: ai-chief-of-staff
description: >-
  Personal AI assistant that combines Gmail, Calendar, and Drive data into
  actionable briefings via gwcli. Three sub-workflows: Morning Sweep (email
  triage + today's calendar + task classification), Meeting Prep (attendee
  context + related docs), and Weekly Digest (weekly calendar + email overview).
  Use when the user asks for "morning sweep", "morning briefing", "daily
  briefing", "meeting prep", "weekly digest", "weekly summary", "start my day",
  "prep my meeting", "what's on my plate", or "아침 브리핑", "미팅 준비", "주간 요약". Do NOT
  use for single-service operations (use gwcli directly).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# AI Chief of Staff -- Personal Assistant

A personal AI assistant inspired by Jim Prosser's Claude Code "Chief of Staff" system. Combines Gmail, Calendar, and Drive data into structured, actionable briefings using `gwcli` (google-workspace-cli).

> **Prerequisites**: `gwcli` must be installed and authenticated with a profile. See [gwcli setup](https://github.com/ianpatrickhines/google-workspace-cli).

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| morning-sweep | "Morning briefing", "start my day", daily triage | [references/morning-sweep.md](references/morning-sweep.md) |
| meeting-prep | "Prep my meeting", "meeting prep", next meeting context | [references/meeting-prep.md](references/meeting-prep.md) |
| weekly-digest | "Weekly summary", "weekly digest", Monday planning | [references/weekly-digest.md](references/weekly-digest.md) |

## gwcli Command Reference

For the full command reference with Gmail, Calendar, Drive, and Profile commands, see [references/gwcli-reference.md](references/gwcli-reference.md). Key pattern: always use `--format json` for structured agent-parseable output.

## Workflow

1. **Route**: Match user intent to one sub-skill from the index.
2. **Read**: Load `references/<sub-skill>.md` and follow its instructions.
3. **Execute**: Run gwcli commands, collect JSON output, synthesize the briefing.

## 4-Category Classification Framework

Used across all sub-skills to classify actionable items:

| Category | Label | Description | Agent Action |
|----------|-------|-------------|--------------|
| Green | Dispatch | Agent can fully handle | Draft reply, file note, schedule |
| Yellow | Prep | 80% ready, human finishes | Prepare draft with options for user |
| Red | Yours | Requires human judgment | Provide context only, flag for user |
| Gray | Skip | Not actionable today | Defer with reason |

## Security Rules

- **Never send emails** without explicit user confirmation. Draft only.
- **Never delete** calendar events or emails without confirmation.
- **Never expose** full email bodies in logs or outputs -- summarize instead.
- Use `--format json` to parse structured data, not raw text.

## Examples

### Example 1: Morning Sweep

User says: "Start my day" or "아침 브리핑"

Actions:
1. Read [references/morning-sweep.md](references/morning-sweep.md)
2. Run `gwcli calendar events --days 1 --format json` and `gwcli gmail list --unread --limit 20 --format json`
3. Classify items into Green/Yellow/Red/Gray categories
4. Present structured Korean briefing with prioritized action items

Result: Markdown briefing with today's calendar, email triage, and recommended actions

### Example 2: Meeting Prep

User says: "Prep me for my next meeting" or "다음 미팅 준비해줘"

Actions:
1. Read [references/meeting-prep.md](references/meeting-prep.md)
2. Find next event, research attendees via email history, search related Drive docs
3. Produce prep document with attendees, context, and talking points

Result: Structured meeting prep with attendee history, related docs, and suggested agenda

### Example 3: Weekly Digest

User says: "What's my week look like?" or "주간 요약"

Actions:
1. Read [references/weekly-digest.md](references/weekly-digest.md)
2. Fetch 7-day calendar + unread email backlog + important/starred emails
3. Produce weekly overview with per-day breakdown and action items

Result: Weekly digest with meeting density, email highlights, and priority recommendations

## Error Handling

| Situation | Action |
|-----------|--------|
| gwcli not installed | Tell user to run: `cd ~/work/tools/google-workspace-cli && npm link` |
| Auth expired / no profile | Tell user to run: `gwcli profiles add work --client <path>` |
| No unread emails | Report "Inbox zero" in briefing |
| No calendar events | Report "No meetings scheduled" |
| API rate limit | Wait 10 seconds and retry once |
