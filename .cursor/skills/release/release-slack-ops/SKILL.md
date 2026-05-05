---
name: release-slack-ops
description: >-
  Slack announcement operations for the release cycle. Post structured messages
  to #release-control and #hotfix-alert using predefined templates for Tuesday
  collection, Wednesday QA status, Thursday deployment, and hotfix alerts. Use
  when the user asks to "post release update", "release slack announcement",
  "릴리즈 슬랙 공지", "release-slack-ops", or any release-related Slack
  communication. Do NOT use for general Slack messaging (use
  kwp-slack-slack-messaging), Slack search (use kwp-slack-slack-search), or
  non-release channel operations.
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Release Slack Ops

Slack announcement operations for the weekly release cycle and hotfix queue. Infrastructure skill used by other release skills — rarely invoked directly.

## When to Use

- Called by `release-collector` to post Tuesday collection summaries
- Called by `release-qa-gate` to post Wednesday QA status
- Called by `release-deployer` to post Thursday deploy announcements
- Called by `hotfix-manager` to post hotfix alerts
- Directly when manual release announcements are needed

## Prerequisites

- Slack MCP server connected and authenticated
- Channel IDs configured in `config.json`
- Message templates: `release-ops-orchestrator/references/slack-templates.md`

## Configuration

Create `.cursor/skills/release/release-slack-ops/config.json` if not present:

```json
{
  "release_control_channel": "<CHANNEL_ID>",
  "hotfix_alert_channel": "<CHANNEL_ID>"
}
```

Channel IDs must be obtained by searching Slack for the channel names `#release-control` and `#hotfix-alert`. If channels do not exist yet, report to user for creation.

## Channel Routing

| Channel | Content |
|---|---|
| `#release-control` | Regular release ops: collection, QA status, deploy confirmation, blockers |
| `#hotfix-alert` | Hotfix-only: urgent candidates, business impact, deploy status |

Blocker escalations that require decisions route to `#효정-의사결정` via the `decision-router` skill.

## Workflow

### Message Type 1: Tuesday Collection Summary

Post the weekly release candidate list after Tuesday collection.

**Template structure** (main message):
```
📋 Weekly Release Candidate List v1 — {date}

Total: {count} items | By App: AI-Platform({n}), Agent Studio({n})

Ready: {n} | Missing Info: {n} | Blocked: {n}
```

**Thread replies** (one per category):
- Thread 1: Ready items table (App, PR, Owner, Risk)
- Thread 2: Missing info items with specific gaps
- Thread 3: Action items with deadlines

**Channel**: `#release-control`

**Tools**: `scripts/slack_post_message.py` (main) + thread replies using `--thread-ts`

### Message Type 2: Wednesday QA Status

Post QA progress and results during/after Wednesday QA.

**Template structure** (main message):
```
🧪 QA Status Update — {date}

Passed: {n} | Failed: {n} | In Progress: {n} | Not Started: {n}

Gate: {OPEN|CLOSING|CLOSED}
```

**Thread replies**:
- Thread 1: Passed items (ready for Thursday)
- Thread 2: Failed items with failure details
- Thread 3: Items set to Hold with reasons

**Channel**: `#release-control`

### Message Type 3: Thursday Pre-Deploy Announcement

Announce the locked release list and deployment schedule.

**Template structure**:
```
🚀 Release Deployment — {date}

Items: {count} | Deploy Time: {time}
Risk Profile: High({n}) Medium({n}) Low({n})

⚠️ Release list is LOCKED. No new items except hotfixes.
```

**Thread replies**:
- Thread 1: Full item list with owners and rollback plans
- Thread 2: Deployment sequence and timeline

**Channel**: `#release-control`

### Message Type 4: Thursday Post-Deploy Confirmation

Announce deployment completion and monitoring plan.

**Template structure**:
```
✅ Release Complete — {date}

Deployed: {n} items | Rolled Back: {n} | Deferred: {n}

Monitoring: {duration} active
```

**Thread replies**:
- Thread 1: Deployed items with confirmation status
- Thread 2: 3 improvement points for next week
- Thread 3: Rolled back or deferred items with reasons

**Channel**: `#release-control`

### Message Type 5: Hotfix Alert

Post urgent hotfix notifications.

**Template structure**:
```
🚨 Hotfix Alert — {app}

Urgency: {level}
Impact: {customer_impact}
PR: {pr_link}
Status: {status}

Business Team Notified: {yes|no}
QA Status: {status}
```

**Channel**: `#hotfix-alert`

### Message Type 6: Blocker Escalation

Escalate blocked items that need decisions.

**Template structure**:
```
⛔ Release Blocker — {item_title}

Blocked by: {reason}
Impact: {count} items affected
Decision needed by: {deadline}

Options:
1. {option_a}
2. {option_b}
```

**Channel**: `#release-control` with cross-post to decision channel via `decision-router`

## Message Format Rules

- Use Slack mrkdwn syntax (not markdown)
- Bold with `*text*`, italic with `_text_`
- Links: `<https://url|display text>`
- GitHub PR links: `<https://github.com/org/repo/pull/N|#N title>`
- Mention users with `<@USERID>`
- Use thread replies for details to keep the main channel scannable
- One main message per announcement; supporting data in threads

## Error Recovery

- If Slack MCP is unavailable: save the message to `outputs/release-ops/{date}/pending-slack-{type}.md` for manual posting
- If channel ID is not configured: prompt user with instructions to find the channel ID
- If message fails to post: retry once, then save to pending file

## Gotchas

- Slack mrkdwn is NOT markdown: `*bold*` not `**bold**`, `_italic_` not `*italic*`
- Thread replies require `thread_ts` from the parent message response
- Channel IDs start with `C` (e.g., `C0AA8NT4T8T`), not channel names
- Slack rate limits: max 1 message per second per channel
- Messages over 4000 chars must be split or moved to threads
