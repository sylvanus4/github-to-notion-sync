## Weekly Digest

Weekly summary for planning: this week's calendar, email backlog, important threads, and action items.

### Usage

```
/weekly-digest
```

### Workflow

1. Fetch 7-day calendar via `gwcli calendar events --days 7 --format json`
2. Fetch unread email backlog via `gwcli gmail list --unread --limit 50 --format json`
3. Find important/starred emails via `gwcli gmail search "is:important" --format json`
4. Identify action items via `gwcli gmail search "subject:(action OR deadline OR review) newer_than:7d" --format json`
5. Produce a structured Korean weekly digest with per-day breakdown and priorities

### Execution

Read and follow the `ai-chief-of-staff` skill (`.cursor/skills/ai-chief-of-staff/SKILL.md`), then load the weekly-digest sub-skill at `references/weekly-digest.md`.
