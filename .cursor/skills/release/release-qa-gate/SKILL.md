---
name: release-qa-gate
description: >-
  Wednesday QA tracking and gate enforcement for the weekly release cycle. Tracks
  QA results in Notion, enforces the rule that items without QA results cannot
  deploy on Thursday, and posts QA status to Slack. Use when the user asks to
  "update QA status", "run QA gate", "Wednesday QA", "수요일 QA", "QA 게이트",
  "release-qa-gate", or during the Wednesday QA pipeline. Do NOT use for Tuesday
  collection (use release-collector), Thursday deployment (use release-deployer),
  or hotfix QA (use hotfix-manager).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Release QA Gate

Wednesday QA operations: track test results, enforce quality gates, and manage the Pass/Fail/Hold transitions that determine what deploys on Thursday.

## When to Use

- Throughout Wednesday as QA results come in
- Called by `release-ops-orchestrator` on Wednesdays
- When QA managers need to record test results
- At Wednesday EOD to enforce the gate (no result = Hold)

## Prerequisites

- Notion MCP connected (for `release-notion-board`)
- Slack MCP connected (for `release-slack-ops`)
- Weekly release page already created by `release-collector`
- Reference: `release-ops-orchestrator/references/checklists.md` for Wednesday QA Checklist

## Workflow

### Phase 1: Load Current Release Items

Query the weekly release Notion board via `release-notion-board` Operation 4:
- Filter: Status = `Collected` or `Ready for QA`
- Sort by App, then Risk (high first)

Transition all `Collected` items to `Ready for QA` status.

### Phase 2: Record QA Results (Interactive or Batch)

**Interactive mode** (user-driven):
- Present items one at a time
- For each item, ask:
  - QA Result: `Pass`, `Fail`, or `Conditional Pass`
  - Notes: Test details, issues found, conditions for conditional pass
- Update Notion via `release-notion-board` Operation 3:
  - Pass → QA Status = `Pass`, Status = `QA Passed`
  - Fail → QA Status = `Fail`, Status = `Hold`
  - Conditional Pass → QA Status = `Conditional Pass`, Status = `QA Passed` (with note)

**Batch mode** (from structured input):
- Accept a JSON or markdown table of results
- Apply all updates in sequence

### Phase 3: Enforce Gate at EOD

At Wednesday EOD, enforce Rule 2 ("No QA result → No Thursday deployment"):

1. Query all items with QA Status = `Not Started` or `In Progress`
2. Set their Status to `Hold` and QA Status to `Not Started`
3. Set their Release Inclusion to `Excluded`
4. Add `qa:needed` label back on the GitHub PR (remove `qa:done` if present)

Items with QA Status = `Pass` or `Conditional Pass`:
1. Set Status to `Ready for Release`
2. Replace `qa:needed` with `qa:done` label on GitHub PR
3. Set Release Inclusion to `Included`

### Phase 4: Generate QA Status Report

Build the QA summary:

```
🧪 QA Status Update — {date}

Passed: {n} | Conditional Pass: {n} | Failed: {n} | Not Tested: {n}

Gate: {OPEN|CLOSED}
Thursday Deploy Candidates: {n}/{total}
```

Breakdown by app:
- AI-Platform: {n} pass / {n} fail / {n} hold
- Agent Studio: {n} pass / {n} fail / {n} hold

### Phase 5: Post to Slack

Call `release-slack-ops` Message Type 2 (Wednesday QA Status):
- Main message with totals to `#release-control`
- Thread 1: Passed items (Thursday deploy candidates)
- Thread 2: Failed items with failure details and reproduction steps
- Thread 3: Hold items (excluded from Thursday) with reasons

### Phase 6: Persist State

Write QA results to `outputs/release-ops/{date}/qa-results.json`:

```json
{
  "date": "2026-04-08",
  "target_release_date": "2026-04-09",
  "gate_status": "CLOSED",
  "total": 8,
  "passed": 5,
  "conditional_pass": 1,
  "failed": 1,
  "not_tested": 1,
  "deploy_candidates": 6,
  "items": [
    {
      "pr_url": "https://github.com/...",
      "title": "...",
      "app": "ai-platform",
      "qa_status": "Pass",
      "status": "Ready for Release",
      "notes": "..."
    }
  ]
}
```

## Output Artifacts

| Phase | Stage | Output File | Skip Flag |
|---|---|---|---|
| 1 | Load items | In-memory from Notion query | — |
| 2 | Record results | Notion database (live) | — |
| 3 | Enforce gate | Notion database + GitHub labels | `skip-gate` |
| 5 | Slack post | `#release-control` message | `skip-slack` |
| 6 | State file | `outputs/release-ops/{date}/qa-results.json` | — |

## Error Recovery

- If Notion query fails: retry once, then fall back to last `collection.json` from Phase 6 of `release-collector`
- If GitHub label update fails: log the PR URL and manual label instruction
- If Slack posting fails: save to `outputs/release-ops/{date}/pending-slack-qa.md`

## Gotchas

- QA Status `Conditional Pass` still allows deployment but must include documented conditions
- Gate enforcement is irreversible for the current cycle — once an item is set to Hold, it requires manual override to re-include
- The gate closes at Wednesday EOD; any late QA results after gate closure need manual intervention
- GitHub label swap (`qa:needed` → `qa:done`) requires removing the old label first, then adding the new one
