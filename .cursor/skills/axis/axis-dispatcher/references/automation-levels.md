# Progressive Automation Levels

Central state file: `outputs/axis/automation-levels.json`

## Level Definitions

### Level 0 — Report Only (default)

The axis generates outputs (reports, briefings, analyses) but takes
**no autonomous actions**. All decisions are presented to the user for
manual execution.

**Per-axis examples:**

| Axis | Level 0 behavior |
|------|------------------|
| Recruitment | Scans job boards, generates opportunity reports; user applies manually |
| Investment | Runs `today` pipeline, generates signals; user places trades manually |
| Learning | Scans trending papers, queues for review; user triggers paper-review |
| GM | Aggregates cross-axis data, detects synergies; user decides on actions |
| Side PM | Checks sprint status, lists overdue items; user triages and commits |
| Life | Calendar briefing, email triage summary; user acts on items |

### Level 1 — Suggest + Confirm

The axis proposes specific actions and posts them to `#효정-의사결정`
for approval. Execution is blocked until the user responds with
"approve" or "reject".

**Per-axis examples:**

| Axis | Level 1 behavior |
|------|------------------|
| Recruitment | Proposes applying to a matched job; waits for approval before drafting |
| Investment | Suggests specific trades with sizing; waits for order approval |
| Learning | Suggests starting a paper-review for the top-scored paper; waits |
| GM | Proposes cross-axis actions from synergies; waits for confirmation |
| Side PM | Proposes creating issues or PRs; waits for approval |
| Life | Proposes scheduling meetings or sending email replies; waits |

**Confirmation protocol:**
1. Post proposal to `#효정-의사결정` with structured format:
   ```
   🔔 [Axis {N}] Action Proposal
   Action: {description}
   Rationale: {why}
   Risk: {low/medium/high}
   Reply ✅ to approve, ❌ to reject
   ```
2. Wait for user response (no timeout — remains pending)
3. On approval: execute and report result
4. On rejection: log rejection reason and skip

### Level 2 — Act + Notify

The axis executes pre-approved action categories autonomously and
notifies after completion. Only actions within the approved category
list are auto-executed.

**Per-axis approved action categories:**

| Axis | Auto-approved actions | Blocked actions |
|------|----------------------|-----------------|
| Recruitment | Resume tailoring, interview prep doc generation | Job applications, outreach emails |
| Investment | Signal posting to Slack, report generation | Trade execution (always Level 1 max) |
| Learning | Auto-start paper-review for score > 8.5, KB ingest | KB compilation (expensive) |
| GM | Synergy alerts, cross-axis briefing | Decision routing escalation |
| Side PM | Auto-commit domain-split, CI status posting | PR creation, force push |
| Life | Email auto-reply drafts, calendar conflict alerts | Meeting scheduling, email sending |

**Safety constraints at Level 2:**
- Financial transactions (trades, purchases) NEVER auto-execute
- External communications (emails, messages) NEVER auto-send
- Destructive operations (delete, force push) NEVER auto-execute
- These remain at Level 1 maximum regardless of axis level

## Level Transition Rules

### Upgrade Path

```
Level 0 → Level 1:  Requires 7 consecutive clean runs (no S1/S2 errors)
Level 1 → Level 2:  Requires 14 consecutive clean runs at Level 1
                     + explicit human approval via #효정-의사결정
```

### Downgrade Triggers

```
Any S1 error:       Level → max(level - 1, 0)
Circuit breaker:    Level → -1 (disabled, see failure-alerting.md)
Human override:     Level → any value (via #효정-의사결정 or direct edit)
```

### Level -1 (Disabled)

Set by the circuit breaker when an axis fails S1 for 3 consecutive days.
The axis is completely skipped by the dispatcher. A persistent alert
remains in `#효정-의사결정` until a human resets the level to 0.

## State File Schema

```json
{
  "axis-{name}": {
    "level": 0,
    "last_reviewed": "YYYY-MM-DD",
    "level_history": [
      {
        "date": "YYYY-MM-DD",
        "from": 0,
        "to": 1,
        "reason": "7 consecutive clean runs"
      }
    ],
    "notes": "Free-text context"
  }
}
```

## Reading and Writing

- **Dispatcher** reads `automation-levels.json` at startup to determine
  which axes to run and at what level
- **Each axis** reads its own level to decide behavior (report vs suggest
  vs act)
- **Dispatcher** writes level changes (downgrades on errors, circuit
  breaker triggers)
- **Human** edits directly or via `#효정-의사결정` approval for upgrades
