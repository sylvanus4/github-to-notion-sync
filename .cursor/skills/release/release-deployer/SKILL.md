---
name: release-deployer
description: >-
  Thursday deployment operations for the weekly release cycle. Locks the release
  list, announces deployment schedule, tracks deployment status, and posts
  post-deploy confirmation with improvement points. Use when the user asks to
  "run deployment", "Thursday deploy", "release deploy", "목요일 배포",
  "릴리즈 배포", "release-deployer", or during the Thursday deployment pipeline.
  Do NOT use for Tuesday collection (use release-collector), Wednesday QA
  (use release-qa-gate), or hotfix deployment (use hotfix-manager).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Release Deployer

Thursday deployment lifecycle: lock the release list, announce schedule, track deployment progress, post confirmation, and record improvement points.

## When to Use

- Thursday morning as part of the release cycle
- Called by `release-ops-orchestrator` on Thursdays
- Manually when deployment operations need to be tracked

## Prerequisites

- Notion MCP connected (for `release-notion-board`)
- Slack MCP connected (for `release-slack-ops`)
- QA gate completed — `qa-results.json` from `release-qa-gate` exists
- Reference: `release-ops-orchestrator/references/checklists.md` for Thursday Deploy Checklist

## Workflow

### Phase 1: Lock Release List

1. Load QA results from `outputs/release-ops/{date}/qa-results.json` or query Notion for items with Status = `Ready for Release`
2. Enforce Rule 5: No new items on deployment day (log the locked list)
3. Generate the final deploy manifest with item count, risk profile, deployment sequence
4. Persist the locked list to `outputs/release-ops/{date}/deploy-manifest.json`

```json
{
  "date": "2026-04-09",
  "locked_at": "2026-04-09T09:00:00+09:00",
  "deploy_time": "14:00",
  "total": 6,
  "risk_profile": {"high": 1, "medium": 3, "low": 2},
  "items": [
    {
      "pr_url": "...",
      "title": "...",
      "app": "ai-platform",
      "risk": "medium",
      "owner": "...",
      "rollback_method": "...",
      "deploy_order": 1
    }
  ]
}
```

### Phase 2: Pre-Deploy Announcement

Call `release-slack-ops` Message Type 3 (Thursday Pre-Deploy):
- Main message: item count, deploy time, risk profile, LOCKED notice
- Thread 1: Full item list with owners and rollback plans
- Thread 2: Deployment sequence and timeline

Notify business/QA teams per the checklist:
- Update Notion items: `Business Team Share Status` = checked
- Update Notion items: `QA Team Share Status` = checked

### Phase 3: Track Deployment Progress

For each item in the deploy manifest, track deployment status:

**Status transitions**:
- `Ready for Release` → `Released` (successful deployment)
- `Ready for Release` → `Hold` (deployment failed, rolled back)

**For each deployed item**:
1. Update Notion via `release-notion-board` Operation 3:
   - Status = `Released`
   - Release Inclusion = `Included`
2. Record deployment timestamp

**For each rolled-back item**:
1. Update Notion:
   - Status = `Hold`
   - Release Inclusion = `Deferred`
2. Record rollback reason

### Phase 4: Post-Deploy Announcement

Call `release-slack-ops` Message Type 4 (Thursday Post-Deploy Confirmation):
- Main message: deployed count, rolled back count, monitoring plan
- Thread 1: Deployed items with confirmation
- Thread 2: 3 improvement points for next week (collected from the team or auto-generated)
- Thread 3: Rolled back or deferred items with reasons

### Phase 5: Post-Deploy Retrospective

Collect and record 3 improvement points:
1. Review the week's release cycle for process issues
2. Note any missed deadlines, validation gaps, or communication failures
3. Document actionable improvements

Persist to `outputs/release-ops/{date}/retrospective.json`:

```json
{
  "date": "2026-04-09",
  "deployed": 5,
  "rolled_back": 1,
  "deferred": 0,
  "improvements": [
    "Improvement 1: ...",
    "Improvement 2: ...",
    "Improvement 3: ..."
  ],
  "monitoring_end": "2026-04-09T18:00:00+09:00"
}
```

### Phase 6: Persist Final State

Write deployment results to `outputs/release-ops/{date}/deploy-results.json`:

```json
{
  "date": "2026-04-09",
  "total_candidates": 6,
  "deployed": 5,
  "rolled_back": 1,
  "deferred": 0,
  "items": [
    {
      "pr_url": "...",
      "title": "...",
      "app": "ai-platform",
      "status": "Released",
      "deployed_at": "2026-04-09T14:15:00+09:00"
    }
  ]
}
```

## Output Artifacts

| Phase | Stage | Output File | Skip Flag |
|---|---|---|---|
| 1 | Lock | `outputs/release-ops/{date}/deploy-manifest.json` | — |
| 2 | Pre-deploy | `#release-control` message | `skip-slack` |
| 3 | Track | Notion database (live) | — |
| 4 | Post-deploy | `#release-control` message | `skip-slack` |
| 5 | Retrospective | `outputs/release-ops/{date}/retrospective.json` | — |
| 6 | State file | `outputs/release-ops/{date}/deploy-results.json` | — |

## Error Recovery

- If deploy-manifest lock fails: fall back to Notion query for `Ready for Release` items
- If Notion update fails during tracking: persist status locally and retry
- If Slack posting fails: save to `outputs/release-ops/{date}/pending-slack-deploy.md`

## Gotchas

- Deploy time is announced, not enforced — actual deployment is a manual operation by the team
- Rule 5 enforcement: if someone tries to add an item on Thursday, this skill rejects it with explanation
- Rolled-back items should be triaged for next week's release or hotfix path
- Monitoring duration after deployment is typically 2-4 hours; adjust per risk profile
- The 3 improvement points are a mandatory output — if no issues occurred, note what went well
