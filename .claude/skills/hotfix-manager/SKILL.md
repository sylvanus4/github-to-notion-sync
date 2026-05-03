---
name: hotfix-manager
description: >-
  Hotfix queue management outside the regular weekly release cycle. Validates
  hotfix PRs, manages the Notion Hotfix Queue, posts alerts to #hotfix-alert,
  and enforces hotfix-specific rules (impact statement, notification status,
  mutual exclusivity with release:approved). Use when the user asks to "submit
  hotfix", "hotfix alert", "manage hotfix", "핫픽스 관리", "핫픽스 등록",
  "hotfix-manager", or any hotfix-related operation. Do NOT use for regular
  release items (use release-collector), QA on regular items (use
  release-qa-gate), or Thursday regular deployment (use release-deployer).
disable-model-invocation: true
---

# Hotfix Manager

Hotfix lifecycle management: validate hotfix PRs, populate the Hotfix Queue in Notion, post alerts to Slack, and track hotfix deployment independently of the weekly cycle.

## When to Use

- Any day when a hotfix is needed (not bound to the weekly cycle)
- Called by `release-ops-orchestrator` when hotfix triggers are detected
- Manually when an urgent fix needs to bypass the regular release process

## Prerequisites

- GitHub CLI (`gh`) authenticated
- Notion MCP connected (for `release-notion-board` hotfix operations)
- Slack MCP connected (for `release-slack-ops` hotfix alerts)
- Reference: `release-ops-orchestrator/references/github-labels.md` for hotfix label rules

## Workflow

### Phase 1: Validate Hotfix PR

For the submitted PR, run hotfix-specific validation:

**1a. Label validation**:
- Must have `hotfix` label
- Must NOT have `release:approved` label (Rule 7: mutually exclusive)
- Must have exactly one app label (`app:ai-platform` or `app:agent-studio`)

**1b. PR body validation** — same 5-section template as regular releases:
1. `## Changes` — non-empty
2. `## User Impact` — non-empty, must describe customer/business impact
3. `## QA Method` — non-empty
4. `## Rollback Method` — non-empty
5. `## Related Issue/Ticket` — non-empty

**1c. Hotfix-specific requirements** (Rule 3):
- Customer/business impact description present in PR body
- Business team notification status must be stated
- QA completion status must be declared

If validation fails, report the specific missing items and block submission.

### Phase 2: Create Hotfix Queue Entry

Call `release-notion-board` Operation 5 to create a hotfix entry:
- App: from `app:*` label
- Urgency: derived from PR labels or user input (`Critical`, `High`, `Medium`)
- Customer/Business Impact: extracted from PR body `## User Impact` section
- Request Background: from PR body `## Changes` section
- Today's Deployment Status: `Pending`
- Business Team Notification: checkbox (from PR body or user confirmation)
- QA Completion Status: `Not Started`

### Phase 3: Post Hotfix Alert

Call `release-slack-ops` Message Type 5 (Hotfix Alert) to `#hotfix-alert`:

```
🚨 Hotfix Alert — {app}

Urgency: {level}
Impact: {customer_impact}
PR: {pr_link}
Status: Pending

Business Team Notified: {yes|no}
QA Status: Not Started
```

### Phase 4: Track Hotfix QA

Update the hotfix entry as QA progresses:
- `Not Started` → `In Progress` → `Done`
- Via `release-notion-board` Operation 6

### Phase 5: Track Hotfix Deployment

Update deployment status:
- `Pending` → `In Progress` → `Deployed` or `Rolled Back`
- Via `release-notion-board` Operation 6

Post deployment confirmation to `#hotfix-alert`:

```
✅ Hotfix Deployed — {app}

PR: {pr_link}
Deployed at: {timestamp}
Monitoring: Active for {duration}
```

Or rollback notice:

```
⚠️ Hotfix Rolled Back — {app}

PR: {pr_link}
Reason: {rollback_reason}
Next steps: {action_plan}
```

### Phase 6: Persist State

Write hotfix record to `outputs/release-ops/{date}/hotfix-{pr_number}.json`:

```json
{
  "date": "2026-04-07",
  "pr_url": "https://github.com/...",
  "pr_number": 456,
  "app": "ai-platform",
  "urgency": "Critical",
  "impact": "...",
  "business_notified": true,
  "qa_status": "Done",
  "deploy_status": "Deployed",
  "deployed_at": "2026-04-07T16:30:00+09:00"
}
```

## Output Artifacts

| Phase | Stage | Output File | Skip Flag |
|---|---|---|---|
| 1 | Validation | In-memory validation result | — |
| 2 | Notion entry | Hotfix Queue database (live) | `skip-notion` |
| 3 | Slack alert | `#hotfix-alert` message | `skip-slack` |
| 5 | Deploy tracking | `#hotfix-alert` update | `skip-slack` |
| 6 | State file | `outputs/release-ops/{date}/hotfix-{pr_number}.json` | — |

## Error Recovery

- If GitHub PR not found: prompt user for the PR URL or number
- If Notion creation fails: persist hotfix data locally and report
- If Slack posting fails: save to `outputs/release-ops/{date}/pending-slack-hotfix.md`

## Gotchas

- Hotfixes are independent of the weekly cycle — they can happen any day
- A hotfix PR must NOT also be labeled `release:approved`; if it is, remove `release:approved` and explain Rule 7
- Hotfixes still require QA, but the QA cycle is compressed (same-day)
- Business team notification is a hard requirement (Rule 3), not optional
- If a hotfix is submitted on Thursday, it does NOT get added to the regular release list
