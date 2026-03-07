## Morning Sweep

Daily morning briefing: email triage + today's calendar + task classification into a single actionable report.

### Usage

```
/morning-sweep
```

### Workflow

1. Fetch today's calendar via `gwcli calendar events --days 1 --format json`
2. Fetch unread emails via `gwcli gmail list --unread --limit 20 --format json`
3. Read important emails in full via `gwcli gmail read MSG_ID --format json`
4. Classify all items into 4 categories (Green/Yellow/Red/Gray)
5. Present a structured Korean briefing with prioritized actions

### Execution

Read and follow the `ai-chief-of-staff` skill (`.cursor/skills/ai-chief-of-staff/SKILL.md`), then load the morning-sweep sub-skill at `references/morning-sweep.md`.
