---
description: "Generate a daily summary of coding patterns, skill usage, tool chains, and git activity from today's agent sessions"
---

# Daily Skill Digest

## Skill Reference

Read and follow the skill at `.cursor/skills/pipeline/daily-skill-digest/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Run Extractor

```bash
python scripts/daily_skill_digest.py --save --pretty
```

Capture the JSON output. If no sessions exist for today, report that and stop.

### Step 2: Synthesize Korean Summary

Read the JSON output and produce a Korean narrative covering:

- **Productivity snapshot**: session count, total tool calls, git commits
- **Top 5 skills**: most invoked skills with counts
- **Top 5 tool chains**: recurring tool-call sequences
- **File activity**: files touched grouped by FSD layer or directory
- **Coding pattern observation**: one-sentence insight in Korean

### Step 3: Format and Present

Format the summary using the Slack mrkdwn template defined in the skill.

**If `--slack` flag is present**: Post to `#효정-할일` (`C0AA8NT4T8T`) via `slack_send_message`.

**Otherwise**: Display the formatted summary inline.

## Constraints

- Output language is Korean
- If zero sessions found, report cleanly and exit
- Never fabricate data — only report what the extractor produces

## Examples

Run and display inline:
```
/daily-digest
```

Run and post to Slack:
```
/daily-digest --slack
```
