---
name: gws-calendar
description: >-
  Manage Google Calendar via the gws CLI -- view agenda, create events, check
  availability, and manage invitations. Use when the user asks to check
  calendar, schedule meetings, view agenda, create events, or find free time.
  Do NOT use for email (use gws-gmail), Chat messages (use gws-chat), or task
  lists (use gws-workflows).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Google Calendar

> **Prerequisites**: `gws` must be installed and authenticated. See `gws-workspace` skill.

```bash
gws calendar <resource> <method> [flags]
```

## Quick Commands

### View Agenda

```bash
gws calendar +agenda                       # upcoming events
gws calendar +agenda --today
gws calendar +agenda --tomorrow
gws calendar +agenda --week --format table
gws calendar +agenda --days 3 --calendar 'Work'
```

| Flag | Default | Description |
|------|---------|-------------|
| `--today` | off | Show today's events only |
| `--tomorrow` | off | Show tomorrow's events |
| `--week` | off | Show this week's events |
| `--days` | -- | Number of days ahead |
| `--calendar` | all | Filter to specific calendar |

Read-only -- never modifies events.

### Create an Event

```bash
gws calendar +insert --summary <TEXT> --start <TIME> --end <TIME>
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--summary` | Yes | -- | Event title |
| `--start` | Yes | -- | Start time (ISO 8601 / RFC 3339) |
| `--end` | Yes | -- | End time |
| `--calendar` | No | primary | Calendar ID |
| `--location` | No | -- | Event location |
| `--description` | No | -- | Event body |
| `--attendee` | No | -- | Attendee email (repeatable) |

Use RFC 3339 format: `2026-03-10T09:00:00+09:00`

For recurring events or conference links, use the raw API.

> **Write command** -- confirm with the user before executing.

## Raw API Resources

### calendars

- `clear`, `delete`, `get`, `insert`, `patch`, `update`

### calendarList

- `delete`, `get`, `insert`, `list`, `patch`, `update`, `watch`

### events

- `delete`, `get`, `import`, `insert`, `instances`, `list`, `move`, `patch`, `quickAdd`, `update`, `watch`

### freebusy

- `query` -- check availability across calendars

### acl

- `delete`, `get`, `insert`, `list`, `patch`, `update`, `watch`

### colors / settings

- `get` colors, `get`/`list`/`watch` settings

## Discovering Commands

```bash
gws calendar --help
gws schema calendar.events.list
gws schema calendar.events.insert
gws schema calendar.freebusy.query
```

## Common Patterns

```bash
# List upcoming events (use --fields)
gws calendar events list \
  --params '{"calendarId": "primary", "timeMin": "2026-03-01T00:00:00Z", "maxResults": 10, "singleEvents": true, "orderBy": "startTime"}' \
  --fields "items(id,summary,start,end,attendees)"

# Quick add (natural language)
gws calendar events quickAdd \
  --params '{"calendarId": "primary"}' \
  --json '{"text": "Lunch with Alice tomorrow at noon"}'

# Check free/busy
gws calendar freebusy query \
  --json '{"timeMin": "2026-03-10T00:00:00Z", "timeMax": "2026-03-10T23:59:59Z", "items": [{"id": "primary"}]}'

# Delete an event (use --dry-run first)
gws calendar events delete \
  --params '{"calendarId": "primary", "eventId": "EVENT_ID"}' --dry-run
```
