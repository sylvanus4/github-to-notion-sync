---
name: release-qa-gate
description: >-
  Wednesday QA tracking and gate enforcement for the weekly release cycle. QA
  runs against the RC image deployed on the dev environment. Tracks QA results
  in Notion, enforces the rule that items without QA results are excluded from
  the release (RC image is rebuilt if needed), and posts QA status to Slack.
  Use when the user asks to "update QA status", "run QA gate", "Wednesday QA",
  "수요일 QA", "QA 게이트", "release-qa-gate", or during the Wednesday QA pipeline.
  Do NOT use for Tuesday collection (use release-collector), Thursday
  deployment (use release-deployer), or hotfix QA (use hotfix-manager).
---

# Release QA Gate (Image Tagging Model)

Wednesday QA operations: verify the RC image running on the dev environment, track test results, and enforce the gate that determines what deploys on Thursday. Failed or untested items are excluded and — if necessary — the RC image is rebuilt from a clean dev state.

## When to Use

- Throughout Wednesday as QA results come in
- Called by `release-ops-orchestrator` on Wednesdays
- When QA members need to record test results
- At Wednesday EOD to enforce the gate

## Prerequisites

- RC image tagged and deployed to dev by `release-collector` on Tuesday
- Notion weekly release page populated by `release-collector`
- `collection.json` available at `outputs/release-ops/{date}/`
- Slack MCP connected (for `release-slack-ops`)
- Reference: `release-ops-rules.mdc` for QA gate rules

## Context: QA Environment

This team has **no staging environment**. QA is performed against the **dev environment running the RC image**. The RC image is an immutable container built from the `dev` branch at collection time; it contains changes from all `release:approved` PRs up to that point.

## Workflow

### Phase 1: Verify RC Image Deployment

Before QA begins, confirm the RC image is running on dev:

```bash
kubectl get deployment <app> -n dev -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Expected: image tag matching the RC tag from `collection.json` (e.g., `rc-20260408103000`).

If the RC image is NOT deployed, alert the Release Owner and block QA start.

### Phase 2: Load RC Items from Notion

Query the weekly release Notion board:
- Filter: items with `rc_status = included`
- Sort by Risk (high first), then by app area

Transition all `Collected` items to `Ready for QA` status.

### Phase 3: Record QA Results

**Interactive mode** (user-driven):
- Present items one at a time, ordered by risk
- For each item, record:
  - QA Result: `Pass`, `Fail`, or `Conditional Pass`
  - Notes: test details, issues found, conditions for conditional pass
- Update Notion:
  - Pass → QA Status = `Pass`
  - Fail → QA Status = `Fail`
  - Conditional Pass → QA Status = `Conditional Pass` (with note)

**Batch mode** (from structured input):
- Accept a JSON or markdown table of results
- Apply all updates in sequence

### Phase 4: Enforce Gate at EOD

At Wednesday EOD, enforce Rule 2 from `release-ops-rules.mdc`:

**Items without QA result (Not Started / In Progress):**
1. Mark as excluded from release
2. Update Notion: Status = `Excluded`, QA Status = `Not Tested`
3. Update GitHub PR: remove `qa:needed`, add `release:blocked` with comment explaining exclusion

**Items with QA Fail:**
1. Mark as excluded from release
2. Update Notion: Status = `Excluded`, QA Status = `Fail`
3. Update GitHub PR: remove `qa:needed`, add `release:blocked` with comment including failure details

**Items with Pass / Conditional Pass:**
1. Update Notion: Status = `Ready for Release`
2. Update GitHub PR: remove `qa:needed`, add `qa:done`

**If any items were excluded**, evaluate whether the RC image must be rebuilt:

- **RC image still valid**: If the excluded PRs' changes do NOT affect other approved items' functionality (isolated features, independent services), the existing RC image can still be deployed. The excluded changes exist in the image but are unused or feature-flagged.
- **RC image must be rebuilt**: If excluded PRs introduce regressions or interfere with approved changes, rebuild the RC:
  1. Revert the problematic PR(s) from `dev`
  2. Wait for CI to build a new `dev-{TIMESTAMP}` image
  3. Re-tag the new dev image as `rc-{NEW_TIMESTAMP}`
  4. Redeploy to dev for a final sanity check
  5. Update `collection.json` with the new RC image tag

The decision to rebuild is made by the Release Owner based on the nature of the exclusion.

### Phase 5: Generate QA Status Report

```
🧪 QA Gate Result — {date}

RC Image: ghcr.io/thakicloud/ai-platform-strategy:rc-{timestamp}
Environment: dev (RC image)

Passed: {n} | Conditional Pass: {n} | Failed: {n} | Not Tested: {n}
Post-Gate Exclusions: {n}
RC Rebuild Required: {yes/no}

Gate: {OPEN — deploy Thursday | CLOSED — no deploy candidates}
Thursday Deploy Candidates: {n}/{total}
```

Risk breakdown:
- High risk: {n} pass / {n} fail
- Medium risk: {n} pass / {n} fail
- Low risk: {n} pass / {n} fail

### Phase 6: Post to Slack

Call `release-slack-ops` to `#release-control`:
- Main message: QA gate result with pass/fail counts and RC image tag
- Thread 1: Passed items (Thursday deploy candidates) with risk levels
- Thread 2: Failed items with failure details
- Thread 3: Excluded items (failed or untested) with reasons
- Thread 4: If all items passed — green light message for Thursday

### Phase 7: Persist State

Write to `outputs/release-ops/{date}/qa-results.json`:

```json
{
  "date": "2026-04-09",
  "target_release_date": "2026-04-10",
  "rc_image_tag": "rc-20260408103000",
  "rc_image_url": "ghcr.io/thakicloud/ai-platform-strategy:rc-20260408103000",
  "rc_image_verified": true,
  "rc_rebuilt": false,
  "gate_status": "OPEN",
  "total_rc_items": 15,
  "passed": 12,
  "conditional_pass": 1,
  "failed": 1,
  "not_tested": 1,
  "post_gate_exclusions": 2,
  "deploy_candidates": 13,
  "items": [
    {
      "pr_number": 123,
      "pr_url": "https://github.com/...",
      "title": "...",
      "risk": "medium",
      "qa_status": "Pass",
      "status": "Ready for Release",
      "notes": "..."
    }
  ]
}
```

## Output Artifacts

| Phase | Output | Skip Flag |
|---|---|---|
| 1 | RC image verification | `skip-verify` |
| 3 | Notion QA updates | — |
| 4 | GitHub label updates + optional RC rebuild | `skip-gate` |
| 6 | Slack `#release-control` message | `skip-slack` |
| 7 | `outputs/release-ops/{date}/qa-results.json` | — |

## Error Recovery

- RC image not deployed: alert Release Owner, block QA, retry after deploy
- Notion query fails: retry once, fall back to `collection.json`
- RC rebuild CI failure: report status, suggest manual re-trigger via `release-webui.yaml`
- Slack failure: save to `outputs/release-ops/{date}/pending-slack-qa.md`

## Gotchas

- QA runs on dev with the RC image — dev environment is temporarily frozen for the RC during Wednesday
- `Conditional Pass` allows deployment but conditions must be documented and accepted by the Release Owner
- No direct git reverts on an "RC branch" — the image tagging model means exclusions are handled by rebuilding a clean image if necessary
- The gate closes at Wednesday EOD; late QA results need manual intervention by Release Owner
- After Thursday deployment, dev is restored to the latest `dev` HEAD image (handled by `release-deployer`)
- If all excluded items are isolated, the RC image can still be used as-is — rebuilding is a last resort
