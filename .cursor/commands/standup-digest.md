---
description: "Generate a multi-source daily standup digest per team member — GitHub, Notion, Slack activity aggregated into a Korean summary"
---

## Standup Digest

Generate daily standup summaries from multiple sources for each team member.

### Usage

```
/standup-digest                             # generate for all configured team members
/standup-digest --user hyojung              # generate for a specific user
/standup-digest --since yesterday           # custom time range
/standup-digest --skip-slack                # generate without posting to Slack
```

### Execution

Read and follow the skill at `.cursor/skills/standup-digest/SKILL.md`.

User input: $ARGUMENTS

1. Load team member configuration
2. For each member, collect yesterday's activity from GitHub, Notion, and Slack
3. Generate per-member standup summary in Korean (Done / Doing / Blocked)
4. Post aggregated team digest to Slack with individual thread replies
