---
name: planning-daily-briefing
description: >-
  Planning team daily briefing: aggregate Notion project databases, Slack
  channel signal, and Google Calendar into a structured Korean brief with
  priorities, blockers, meetings, and deadlines; publish to Slack and Notion.
  Default Slack context: team planning-automation channel (e.g. Korean-named
  channel used by the planning automation team). Korean triggers: "데일리 브리핑",
  "오늘 할 일", "기획팀 브리핑", "아침 브리핑". English triggers: "planning daily briefing",
  "daily briefing", "morning brief", "today priorities planning team". Do NOT
  use for company-wide executive briefings (use executive-briefing),
  GitHub-only digests (use github-sprint-digest), or personal inbox triage
  without planning context.
---

# Planning Daily Briefing

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Produce a **single morning-ready** planning brief by combining **Notion** (projects/tasks), **Slack** (default: team planning-automation channel unless user specifies another), and **Google Calendar** via **`gws`**.

## Prerequisites

- **Notion MCP**: query access to agreed project / task databases (names or IDs from user).
- **Slack MCP**: post permission to target channel; thread for details.
- **gws** CLI: authenticated for Calendar read.

## Procedure

1. **Confirm scope** — Date (“today” in org timezone), Notion DBs to include, Slack channel, optional filters (project tags, owners).

2. **Notion pull** — Use **Notion MCP** `database-query` / search:
   - Due today / overdue
   - Status = blocked or at-risk (if properties exist)
   - Top 5 **priority** items (by priority field or manual rank)

3. **Slack scan** — Use **Slack MCP** to fetch overnight messages in the channel (or user-provided window). Extract: decisions, links, asks, incidents. Summarize; do not paste raw walls of text.

4. **Calendar** — Run **`gws` calendar** (agenda for today). List meetings with time, title, attendees if available, and **prep** one-liner per critical meeting.

5. **Synthesize** — Build sections (use **Korean headings** in the delivered brief):
   - Today’s priorities (max 5)
   - Blockers / risks
   - Meetings and prep
   - Deadlines
   - Actions surfaced from Slack
   - Data gaps (what could not be fetched)

6. **Publish** — Post main message to **Slack**; detailed bullets in **thread**. Create or append **Notion** page under agreed parent (title pattern example: `[Briefing] Planning daily — YYYY-MM-DD` localized to Korean per team convention) via **Notion MCP**.

7. **Quality bar** — Every bullet should be **actionable** or **explicitly informational**; unknowns marked with a clear “needs verification” label **in Korean** in the output.

8. **Timebox** — If data pulls exceed a reasonable budget, ship a **partial brief** with explicit gaps rather than blocking the user.

## Notion MCP: suggested queries

- **Overdue**: filter where due date `< today` and status not in (Done, Cancelled) — property names vary; ask user to confirm schema.
- **Due today**: due date `== today` OR due within 48h if the team uses a rolling window.
- **Risk flags**: custom select properties such as `Risk`, `Blocked`, `Needs PM` when present.

## Slack MCP: reading strategy

- Prefer **thread summaries** over quoting every message.
- Capture **decisions** as bullet points with who/when only if visible; otherwise mark speaker as unknown **in Korean** in the output.
- Link important **Notion/GitHub** URLs verbatim when they appear in messages.

## Google Workspace CLI (`gws`)

- Pull **today’s agenda** and highlight meetings that likely need pre-reads (user-marked or keyword-based: review, approval, decision — express matches **in Korean** when writing the brief).
- Do not create calendar events unless the user explicitly requests scheduling.

## Output structure (sections must be written in Korean)

Mirror section **Procedure step 5**, plus footer metadata: source timestamps, channels, query scope.

## Examples

- **Typical day**: 4 Notion tasks due, 2 Slack threads with decisions, 3 meetings → one Slack post + Notion archive page.

- **Lightweight mode**: User has only Slack + Calendar → omit Notion section and state Notion was not connected **in Korean**.

## Quality checklist

- Priorities are **ranked**; no more than 5 unless user overrides.
- Blockers name **owner** or mark unassigned **in Korean** in the output.
- Meetings list includes **time zone** if known.
- Slack and Notion copies are **consistent** (no contradictory deadlines).

## Error handling

- **Notion query empty**: State no rows returned **in Korean** and verify DB id/properties with user.
- **Slack rate limits / no access**: Fall back to user-pasted highlights; note limitation.
- **gws auth failure**: Omit calendar section; list exact CLI error class; suggest `python ~/.config/gws/oauth2_manual.py && rm ~/.config/gws/token_cache.json credentials.enc 2>/dev/null`.
- **Partial data**: Ship brief with a **data gaps** section (Korean heading); never fabricate tasks or meetings.
