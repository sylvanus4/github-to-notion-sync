## Meeting Prep (gwcli)

Prepare comprehensive context for the next upcoming meeting: attendees, recent email threads, related Drive documents, and suggested talking points.

### Usage

```
/meeting-prep-gwcli
```

### Workflow

1. Find next meeting via `gwcli calendar events --days 1 --format json`
2. Research each attendee via `gwcli gmail search "from:ATTENDEE" --format json`
3. Search related Drive docs via `gwcli drive search "KEYWORD" --format json`
4. Produce a structured Korean prep document with attendees, context, and talking points

### Execution

Read and follow the `ai-chief-of-staff` skill (`.cursor/skills/ai-chief-of-staff/SKILL.md`), then load the meeting-prep sub-skill at `references/meeting-prep.md`.
