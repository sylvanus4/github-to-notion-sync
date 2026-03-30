---
name: decision-tracker
description: >-
  Automatically extract decisions from meetings (meeting-digest output), Slack threads,
  and Notion discussions; log them to a Notion Decision Log database with context,
  rationale, alternatives, participants, and follow-ups; track status
  (proposed/approved/implemented/revised); notify Slack for new decisions and deadlines.
  Korean triggers: "의사결정 추적", "결정 이력", "의사결정 로그", "결정 기록".
  English triggers: "decision tracker", "decision log", "decision-tracker".
  Do NOT use for generic meeting summaries without decision extraction (use meeting-digest),
  or task-only tracking without decision context (use meeting-action-tracker).
metadata:
  version: "1.0.1"
  category: tracking
  author: thaki
---

# Decision Tracker

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Turn scattered **decision signals** (meeting outputs, Slack threads, Notion comments) into **durable, queryable records** in a **Notion Decision Log** database, with **status lifecycle** and **Slack** alerts for new entries and implementation due dates.

## Prerequisites

- **Notion MCP**: Decision Log database ID (or name resolvable via search); property schema agreed with the team.
- **Slack MCP**: channel for decision announcements; optional thread for detail.
- Source material: **meeting-digest** markdown/Notion pages, Slack permalink or export, or Notion discussion URLs.

## Recommended Notion schema (adapt to your workspace)

| Property | Type | Notes |
|----------|------|--------|
| Title | Title | Short decision statement |
| Status | Select | proposed, approved, implemented, revised |
| Context | Rich text | Background |
| Rationale | Rich text | Why this option |
| Alternatives | Rich text | Options considered |
| Participants | Multi-select or People | Who was involved |
| Source | URL | Meeting page, Slack thread, Notion link |
| Decision date | Date | When decided or proposed |
| Implementation due | Date | Optional; drives Slack reminders |
| Follow-up actions | Rich text | Linked tasks if applicable |

## Procedure

1. **Intake** — Collect inputs: pasted meeting-digest sections labeled “decisions,” Slack thread URLs, or Notion page IDs. If ambiguous, ask for the **single source of truth** link.

2. **Extract** — For each candidate decision, capture: **what** was decided (one sentence), **why**, **alternatives** mentioned, **who** participated (names or roles), **dependencies**, and **open risks**.

3. **Normalize** — Map to the Decision Log properties. Default **Status** to `proposed` unless the source explicitly states approval or shipped implementation.

4. **Deduplicate** — Use **Notion MCP** `search` / `database-query` on title keywords and date window. Merge or update existing rows instead of creating duplicates.

5. **Write** — Create or update rows via **Notion MCP** (`create-database-row` or equivalent). Store **Source** URLs on every record.

6. **Notify Slack** — Post a concise summary: decision title, status, owner if known, implementation due date, link to Notion row. Use a **thread** for rationale bullets.

7. **Deadline watch** — For decisions with **Implementation due**, schedule or note the next Slack nudge (manual or automation outside this skill). In the delivered run, list upcoming due dates (Korean copy per output rule).

8. **Report** — Return a summary table in Korean: decisions logged, status, Notion links, Slack post confirmation.

## Notion MCP usage

- **Search** existing decisions before insert.
- **Query** Decision Log filtered by `Status`, `Decision date`, or `Implementation due`.
- **Create** one database row per distinct decision; link related pages in body or relation fields if your schema supports it.

## Slack MCP usage

- Main message: headline + status + Notion link.
- Thread: rationale (2–4 bullets), alternatives (1–2 bullets), follow-ups.

## Output structure

Deliver in Korean: run summary (counts, new vs updated); decision list table (title, status, source, Notion link); upcoming due dates for reminders; gaps where extraction failed.

## Error handling

- If schema mismatch: list **missing properties** and propose a minimal compatible row (title + status + source only).
- If source lacks decisions: state clearly that no extractable decisions were found (Korean message); do not fabricate.

## Examples

- **Input**: meeting-digest bullet “We will ship feature X behind flag Y by March 30.” → Log with `approved`, implementation due, Slack post with due date.
- **Input**: Slack debate without closure → Log as `proposed`, Slack post asks for explicit approver.

## Guardrails

- Never invent participants or approval without evidence in the source.
- Prefer **update** over **duplicate** when the same decision appears in multiple channels.
