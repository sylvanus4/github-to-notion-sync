---
name: meeting-action-tracker
description: >-
  Track meeting action items end-to-end: ingest from meeting-digest outputs, create/update
  Notion task DB rows with owners, send Slack DM reminders at 24h/48h/72h intervals
  (configurable), track completion, escalate overdue items, and produce completion reports.
  Korean triggers: "액션 아이템 추적", "회의 후속 관리", "액션 추적", "회의 액션".
  English triggers: "meeting action tracker", "action item tracking", "meeting-action-tracker".
  Do NOT use for logging strategic decisions without tasks (use decision-tracker) or generic daily standup (use standup-digest).
metadata:
  version: "1.0.1"
  category: tracking
  author: thaki
---

# Meeting Action Tracker

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Turn **meeting-digest action items** into **tracked Notion tasks**, keep owners accountable with **Slack DM reminders**, escalate **overdue** work, and report **completion** status in Korean.

## Prerequisites

- **Notion MCP**: Tasks database with properties for owner, due date, status, source meeting link.
- **Slack MCP**: permission to DM assignees (Slack user IDs or emails mappable to users—confirm with user).
- **meeting-digest** output or equivalent structured list: action text, owner, due date.

## Recommended Notion task schema

| Property | Type |
|----------|------|
| Title | Title |
| Owner | People |
| Due | Date |
| Status | Select (Open, In progress, Done, Blocked) |
| Source meeting | URL or Relation |
| Reminder stage | Select (none, 24h, 48h, 72h, escalated) |
| Notes | Rich text |

## Procedure

1. **Ingest** — Parse action items from meeting-digest markdown or Notion child page. Normalize: one row per actionable item; merge duplicates by title similarity.

2. **Assign** — Map owners to **Notion People** fields when emails or names are provided. If owner missing, create row with **Owner TBD** tag in title prefix and flag in report.

3. **Create/Update** — Use **Notion MCP** to upsert rows. Store **Source meeting** link on every task.

4. **Reminders** — For each open item with due date, compute hours until due. If user enabled reminders, draft **Slack DM** texts in Korean for thresholds: **24h**, **48h**, **72h** before due (or after creation if no due date—use user policy). Send via **Slack MCP** only when user confirms automation for this run; otherwise output **ready-to-send** messages.

5. **Escalation** — Items past due and not **Done**: set **Reminder stage** to `escalated` in Notion; notify **manager channel** on Slack if user supplies channel; include item links.

6. **Completion sweep** — Query **Done** items closed in the reporting window; summarize velocity and recurring blockers.

7. **Report** — Korean summary: new tasks, open, overdue, completed, escalations, next reminder schedule.

## Notion MCP usage

- Query open tasks by **Due** ascending.
- Batch-create tasks from a meeting; link back to meeting page ID.

## Slack MCP usage

- DM template (Korean copy): meeting name, one-line action, due date, Notion link, quick acknowledgment request.
- Escalation template: overdue prefix in subject line (localized); mention assignees only when the user supplies Slack handles.

## Google Workspace CLI (`gws`)

- Optional: if tasks should mirror **Gmail** follow-ups, link thread URLs in Notion notes using user-provided message IDs (do not fabricate).

## Reminder configuration

- Default offsets: **72h**, **48h**, **24h** before due (all optional).
- User may set **business days only**; honor timezone stated by user.

## Output structure

Deliver in Korean: round summary; new/updated tasks with Notion links; scheduled reminders (time, recipient); overdue/escalations; completion trend vs prior period.

## Error handling

- Slack user not resolvable → keep task in Notion and list DM failure with needed identifier (Korean message in deliverable).
- Ambiguous action text → create task with **clarification needed** sub-status in notes.

## Examples

- Action: “Legal to confirm wording by Friday” → Due Friday, reminders Wed/Thu, escalate Monday if still open.

## Guardrails

- Never send DMs without user confirmation on **first-time** automation for a workspace.
- Redact sensitive meeting content in Slack; link to Notion for detail.
