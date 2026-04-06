---
description: "Unified router for ops skills: evaluate, scan, inbox, archive, preflight"
---

# /ops Command Router

Route operational commands to the appropriate ops skill.

## Sub-commands

| Sub-command | Skill | Description |
|-------------|-------|-------------|
| `eval <entity> [--rubric DOMAIN]` | evaluation-engine | Evaluate entity against rubric |
| `eval compare <entity> --rubric DOMAIN` | evaluation-engine | Compare multiple entities |
| `scan <portal>` | portal-scanner | Run a portal scan |
| `scan list` | portal-scanner | List configured portals |
| `scan status` | portal-scanner | Show scan history summary |
| `scan new <name> <url>` | portal-scanner | Create new portal config |
| `inbox add <item>` | pipeline-inbox | Add item to processing queue |
| `inbox list` | pipeline-inbox | Show pending items |
| `inbox process [--skill SKILL]` | pipeline-inbox | Process pending items |
| `inbox drain` | pipeline-inbox | Clear processed items |
| `archive search [--entity X]` | report-archiver | Search evaluation history |
| `archive compare <entity>` | report-archiver | Compare evaluations over time |
| `archive stats` | report-archiver | Show report statistics |
| `archive prune --before DATE` | report-archiver | Archive old reports |
| `preflight` | session-preflight | Run environment health check |
| `status` | (built-in) | Show ops dashboard summary |

## Usage

```
/ops eval AAPL --rubric stock-evaluation
/ops eval compare AAPL MSFT --rubric stock-evaluation
/ops scan github-trending
/ops scan list
/ops inbox add https://arxiv.org/abs/2401.12345 --skill paper-review
/ops inbox list
/ops inbox process
/ops archive search --domain stock-evaluation --grade A
/ops archive compare AAPL --last 5
/ops preflight
/ops status
```

## Routing Logic

1. Parse the first argument as the sub-command
2. Load the corresponding ops skill from `.cursor/skills/ops/`
3. Pass remaining arguments to the skill
4. If no sub-command given, show this help

## Status Dashboard (`/ops status`)

When invoked with `status` or no arguments, display:

```
=== Ops Dashboard ===
Inbox:     3 pending, 12 processed today
Scans:     2 portals scanned today (github-trending, arxiv-new)
Evals:     5 evaluations this week (avg B+)
Archive:   847 total reports
Preflight: Last run 2h ago — READY
```
