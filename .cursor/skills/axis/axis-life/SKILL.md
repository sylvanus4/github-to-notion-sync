---
name: axis-life
description: >-
  Axis 6 of the 6-Axis Personal Assistant. Daily personal productivity —
  calendar briefing, email triage, meeting scheduling, errands, household
  management, and wellness. Wraps `google-daily` and all `gws-*` skills with
  a personal errand tracker. Use when the user asks for "axis life", "life
  assistant", "생활 축", "personal axis", "axis-life", or wants the daily
  personal productivity routine. Do NOT use for google-daily alone (use
  google-daily). Do NOT use for individual gws operations (use the specific
  gws-* skill). Do NOT use for investment intelligence (use axis-investment).
metadata:
  author: thaki
  version: "1.0.0"
  category: axis-orchestrator
  axis: 6
  automation_level: 0
---

# Axis 6: Life Assistant

Orchestrates daily personal productivity: morning briefing, email triage,
calendar management, meeting scheduling, errand tracking, and evening
preparation. Wraps the existing `google-daily` pipeline and `gws-*` skills.

## Principles

- **Single Responsibility**: Only personal life management (non-work)
- **Context Isolation**: Reads/writes to `outputs/axis/life/{date}/`
- **Failure Isolation**: Email triage failure does not block calendar briefing
- **File-First Data Bus**: Summaries written to files for cross-axis consumption

## Phase Guard Protocol

Before running Google Workspace operations, check if `google-daily` was
already invoked today. If its outputs exist, reuse them instead of re-running
calendar and email operations (prevents duplicate triage, double Slack posts,
and unnecessary Google API calls).

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (Calendar) | `outputs/google-daily/{date}/phase-1-calendar.json` | File exists with today's date |
| 2 (Email) | `outputs/google-daily/{date}/phase-2-gmail.json` | File exists with today's date |

When guard fires, read the existing `google-daily` output and transform it
into axis-life's format at `outputs/axis/life/{date}/`.

Pass `--force` to bypass all guards and re-run from scratch.
When a phase is skipped, log `REUSED — {guard_file}` in the dispatch manifest.

## Composed Skills

### Google Workspace
- All `gws-*` skills (14 total): `gws-gmail`, `gws-calendar`, `gws-drive`,
  `gws-sheets`, `gws-docs`, `gws-chat`, and recipes

### Briefing
- `calendar-daily-briefing` — today's schedule with prep alerts
- `ai-chief-of-staff` — morning sweep, meeting prep, weekly digest

### Email
- `gmail-daily-triage` — spam deletion, notification labeling, action summary
- `gws-email-reply` — AI-drafted replies with approval gate
- `email-auto-reply` — knowledge-based reply drafts
- `email-research-dispatcher` — extract research topics from emails

### Meeting
- `smart-meeting-scheduler` — find slots, invite, create agenda
- `proactive-meeting-scheduler` — detect implicit meeting requests in emails

### Retail/Errands
- `daiso-mcp`, `daiso-nearby-stock` — Korean retail inventory lookup

### Documents
- `anthropic-docx`, `anthropic-pdf`, `anthropic-xlsx` — personal doc management

### Personal Notes
- All `obsidian-*` skills (8 total) — personal vault management

## Workflow

### Morning Routine (triggered by `axis-dispatcher` ~07:00, first axis to run)

```
Phase 1: Calendar briefing      → outputs/axis/life/{date}/calendar.json
Phase 2: Email triage           → outputs/axis/life/{date}/email-triage.json
Phase 3: Errand check           → outputs/axis/life/{date}/errands.json
Phase 4: Morning brief compile  → outputs/axis/life/{date}/morning-briefing.md
```

**Phase 1 — Calendar Briefing** *(guarded)*
Check Phase Guard: if `outputs/google-daily/{date}/phase-1-calendar.json` exists,
read it and transform to `calendar.json` — SKIP re-invoking `calendar-daily-briefing`.
Otherwise run `calendar-daily-briefing` to fetch today's events. Identify
interviews, personal appointments, and preparation needs. Write to `calendar.json`.

**Phase 2 — Email Triage** *(guarded)*
Check Phase Guard: if `outputs/google-daily/{date}/phase-2-gmail.json` exists,
read it and transform to `email-triage.json` — SKIP re-invoking `gmail-daily-triage`.
Otherwise run `gmail-daily-triage` for inbox cleanup. Summarize unanswered
emails with action items. Write to `email-triage.json`.

**Phase 3 — Errand Check**
Read `outputs/axis/life/errands-queue.json` (persistent across days).
Surface any errands due today or overdue. Write to `errands.json`.

**Phase 4 — Morning Brief**
Compile calendar, email highlights, and pending errands into a readable
Korean morning briefing. Write to `morning-briefing.md`.

### Evening Routine (triggered by `axis-dispatcher` ~17:00)

```
Phase E1: Tomorrow prep         → outputs/axis/life/{date}/tomorrow-prep.md
Phase E2: Email follow-up       → outputs/axis/life/{date}/email-followup.json
```

**Phase E1 — Tomorrow Prep**
Fetch tomorrow's calendar. Identify prep needs (documents to review,
meeting agendas to create). Write to `tomorrow-prep.md`.

**Phase E2 — Email Follow-up**
Check for emails sent today awaiting replies. Flag items needing
follow-up tomorrow. Write to `email-followup.json`.

### On-Demand Operations

- `/errand add <item>` — Append to `outputs/axis/life/errands-queue.json`
- `/errand done <id>` — Mark complete in errands queue
- `/errand list` — Show pending errands

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/axis/life/{date}/calendar.json` | Today's calendar |
| 2 | `outputs/axis/life/{date}/email-triage.json` | Email triage results |
| 3 | `outputs/axis/life/{date}/errands.json` | Today's errands |
| 4 | `outputs/axis/life/{date}/morning-briefing.md` | Compiled brief |
| E1 | `outputs/axis/life/{date}/tomorrow-prep.md` | Tomorrow preparation |
| E2 | `outputs/axis/life/{date}/email-followup.json` | Email follow-ups |

## Persistent State

| File | Purpose |
|------|---------|
| `outputs/axis/life/errands-queue.json` | Cross-day errand tracker |

The errands queue is a simple JSON array:
```json
[
  {
    "id": "errand-001",
    "task": "Pick up dry cleaning",
    "due": "2026-04-08",
    "status": "pending",
    "added": "2026-04-07"
  }
]
```

## Slack Channel

- `#효정-할일` — morning briefing post, errand reminders

## Automation Level

Tracked centrally in `outputs/axis/automation-levels.json`.
Full protocol: `axis-dispatcher/references/automation-levels.md`.

- **Level 0 (current)**: Report only — briefing and triage summaries
- **Level 1**: Suggest email replies + schedule meetings with confirmation
- **Level 2**: Auto-draft replies, auto-create calendar conflict alerts

Email sending and meeting scheduling NEVER auto-execute (safety constraint).

## Error Recovery

Follow the protocol in `axis-dispatcher/references/failure-alerting.md`.

Each phase runs independently. If email triage fails (e.g., gws auth issue — run `python ~/.config/gws/oauth2_manual.py`),
calendar briefing still runs. Failed phases are marked in the morning brief
with the error context.

Write errors to `outputs/axis/life/{date}/errors.json` using the
standard error record format (severity S1-S4, phase, impact, recovery).

## Gotchas

- `gws` CLI command is `gws`, not `gwcli` — strip keyring prefix
- `gmail +triage` uses `--max`, not `--max-results`
- Google Workspace auth must be verified before running; if auth fails,
  the entire axis reports a pre-flight failure to `#효정-할일`
- Errand queue file must be created on first run if it doesn't exist
