## Google Calendar Operations

View agenda, create events, and manage calendar via the gws CLI.

### Usage

```
/gws-calendar [action] [args]
```

Actions:
- `agenda` -- view upcoming events via `gws calendar +agenda [--today|--week|--days N]`
- `insert` -- create an event via `gws calendar +insert --summary <text> --start <time> --end <time>`
- `freebusy` -- check availability via `gws calendar freebusy query --json '...'`

### Examples

```
/gws-calendar agenda --today
/gws-calendar agenda --week
/gws-calendar insert --summary "Team Standup" --start "2026-03-10T09:00:00+09:00" --end "2026-03-10T09:30:00+09:00"
```

### Execution

Read and follow the `gws-calendar` skill (`.cursor/skills/gws-calendar/SKILL.md`) for full CLI reference, raw API resources, and common patterns.
