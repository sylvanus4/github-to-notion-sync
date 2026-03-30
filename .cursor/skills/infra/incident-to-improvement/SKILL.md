---
name: incident-to-improvement
description: >-
  Close the loop from production incident to lasting prevention. Orchestrates 7
  existing skills in a pipeline: incident triage, root cause analysis, code fix
  with regression tests, knowledge base article, monitoring recommendations, and
  blameless post-mortem document. Ensures every incident produces lasting
  improvements. Use when the user reports an "incident", "post-mortem",
  "production issue", "outage", "인시던트", "장애 대응", "장애 복구", "incident to
  improvement", or wants to run the full incident response lifecycle. Do NOT use
  for non-incident debugging (use diagnose), code review (use deep-review), or
  monitoring setup only (use sre-devops-expert).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Incident to Improvement — Closed-Loop Incident Response

Every incident is a gift — if you learn from it. This skill ensures that production incidents don't just get fixed, they produce regression tests, knowledge base articles, monitoring improvements, and blameless post-mortems.

## Usage

```
/incident-to-improvement "500 errors on /api/users since 14:00"
/incident-to-improvement --severity P1 "Database connection pool exhaustion"
/incident-to-improvement --phase triage       # triage only
/incident-to-improvement --phase fix          # skip to fix (triage already done)
/incident-to-improvement --phase post-mortem  # generate post-mortem from resolved incident
/incident-to-improvement --no-fix             # analysis + post-mortem only, no code changes
```

## Pipeline Overview

```
Group A (parallel): Respond
  ├─ kwp-engineering-incident-response → Severity classification, impact assessment
  └─ diagnose                          → Root cause analysis (3 parallel agents)

    ↓ Gate: root cause identified with medium+ confidence

Group B (sequential): Fix and Test
  ├─ generalPurpose agent              → Apply the fix
  └─ test-suite                        → Generate regression tests, run suite

    ↓ Gate: fix applied, tests pass

Group C (parallel): Prevent
  ├─ kwp-customer-support-knowledge-management → KB article for future reference
  ├─ sre-devops-expert                          → Monitoring + alerting recommendations
  └─ technical-writer                           → Blameless post-mortem document
```

## Workflow

### Step 1: Incident Intake

Gather incident context:

1. **User description**: error message, affected endpoint, timeline
2. **Severity**: P1 (critical), P2 (major), P3 (minor), P4 (low) — auto-classify if not provided
3. **Impact scope**: users affected, services impacted, revenue impact
4. **Evidence**: error logs, metrics, user reports

Auto-classification heuristic:
- P1: Service fully down, data loss risk, or >50% users affected
- P2: Major feature broken, workaround exists, or 10-50% users affected
- P3: Minor feature broken, <10% users affected
- P4: Edge case, cosmetic issue, no user reports

### Step 2: Group A — Respond (Parallel)

Launch 2 sub-agents:

**Agent 1: Incident Response (KWP)**
- `subagent_type: generalPurpose`, `model: fast`, `readonly: true`
- Prompt: Read and follow `.cursor/skills/kwp/kwp-engineering-incident-response/SKILL.md`. Triage this incident: classify severity, assess blast radius, identify affected services, recommend immediate mitigation steps. Incident: `{user_description}`.
- Expected output: severity, impact assessment, affected services, mitigation steps

**Agent 2: Diagnose (Root Cause)**
- `subagent_type: generalPurpose`, `model: fast`, `readonly: true`
- Prompt: Read and follow `.cursor/skills/review/diagnose/SKILL.md`. Run with `--no-fix`. Analyze: `{user_description}`. Return root cause hypothesis, confidence level, and evidence chain.
- Expected output: root cause, confidence, evidence, proposed fix

**Gate check**:
- If confidence is Low: ask user for additional context (logs, reproduction steps)
- If agents disagree on root cause: present both hypotheses, ask user to choose
- If P1 severity: present mitigation steps immediately, don't wait for full analysis

### Step 3: Group B — Fix and Test (Sequential)

Skip if `--no-fix` or `--phase triage`.

**Step 3a: Apply Fix**
- Use the diagnose agent's proposed fix
- Read the target file(s)
- Apply fix via StrReplace
- Run ReadLints to verify no regressions

**Step 3b: Generate Regression Tests**
- `subagent_type: generalPurpose`
- Prompt: Read and follow `.cursor/skills/review/test-suite/SKILL.md`. For the fix applied to `{files}`, generate regression tests that:
  1. Reproduce the original bug (test should fail without the fix)
  2. Verify the fix works correctly
  3. Cover edge cases related to the root cause
- Run the test suite to verify all tests pass

**Gate check**:
- If tests fail: attempt auto-fix once, then report to user
- If fix introduces new linter errors: fix them before proceeding

### Step 4: Group C — Prevent (Parallel)

**Agent 3: Knowledge Base Article (KWP)**
- `subagent_type: generalPurpose`, `model: fast`
- Prompt: Read and follow `.cursor/skills/kwp/kwp-customer-support-knowledge-management/SKILL.md`. Create a KB article for this incident:
  - Title: descriptive summary
  - Symptoms: what the user/system experienced
  - Root cause: what went wrong and why
  - Resolution: how it was fixed
  - Prevention: what's being done to prevent recurrence
- Save to context for inclusion in post-mortem

**Agent 4: Monitoring Recommendations**
- `subagent_type: generalPurpose`, `model: fast`, `readonly: true`
- Prompt: Read and follow `.cursor/skills/infra/sre-devops-expert/SKILL.md`. Based on this incident (root cause: `{root_cause}`), recommend:
  - New alerts or monitors that would have caught this earlier
  - SLO/SLI adjustments if applicable
  - Runbook updates for faster future response
- Expected output: monitoring recommendations with implementation guidance

**Agent 5: Post-Mortem Document**
- `subagent_type: generalPurpose`, `model: fast`
- Prompt: Read and follow `.cursor/skills/standalone/technical-writer/SKILL.md`. Generate a blameless post-mortem document using this template:

```markdown
# Post-Mortem: [Incident Title]
Date: [date]
Severity: [P1-P4]
Duration: [start → resolution]
Author: [auto-generated]

## Summary
[2-3 sentence summary]

## Impact
- Users affected: [N]
- Services affected: [list]
- Duration: [time]

## Timeline
- [HH:MM] Incident detected
- [HH:MM] Triage started
- [HH:MM] Root cause identified
- [HH:MM] Fix applied
- [HH:MM] Fix verified

## Root Cause
[Technical explanation of what went wrong]

## Resolution
[What was done to fix it]

## Lessons Learned
### What went well
- [positive]
### What could be improved
- [improvement]

## Action Items
- [ ] [monitoring improvement]
- [ ] [process improvement]
- [ ] [code improvement]

## Regression Tests Added
- [test file]: [what it tests]
```

Create directory if needed: `mkdir -p docs/post-mortems`

Generate slug from incident title: lowercase, replace spaces and special characters with hyphens, strip consecutive hyphens. Example: `"Database Connection Pool Exhaustion"` → `database-connection-pool-exhaustion`

Save to: `docs/post-mortems/{YYYY-MM-DD}-{slug}.md`

### Step 5: Update KNOWN_ISSUES.md

Append an entry following the bugfix-loop format:

```markdown
### [Short title]
- **Symptom**: [what went wrong]
- **Root cause**: [why it happened]
- **Fix pattern**: [what worked and why]
```

### Step 6: Incident Report

```
Incident to Improvement Report
================================
Incident: [description]
Severity: [P1-P4]
Status: RESOLVED

Phase 1 — Respond:
  Root cause: [1-line summary]
  Confidence: [High|Medium|Low]
  Mitigation: [immediate steps taken]

Phase 2 — Fix:
  Files changed: [N]
  Fix: [description]
  Regression tests: [N] added
  Test suite: [PASS|FAIL]

Phase 3 — Prevent:
  KB article: [created|skipped]
  Monitoring: [N] recommendations
  Post-mortem: docs/post-mortems/[filename]
  KNOWN_ISSUES.md: updated

Improvement Loop Closed: YES
```

## Examples

### Example 1: Full incident lifecycle

User: `/incident-to-improvement "500 errors on /api/users endpoint since deployment at 14:00"`

All 3 groups execute. Root cause found (missing null check on new field), fix applied, 2 regression tests added, KB article created, monitoring alert recommended, post-mortem saved.

### Example 2: Post-mortem only

User: `/incident-to-improvement --phase post-mortem "Yesterday's auth outage — we already fixed it, need the post-mortem"`

Skips Groups A and B. Asks the user for structured intake (see below), then generates blameless post-mortem, monitoring recommendations, and KB article.

**Post-mortem intake questions** (ask via AskQuestion when `--phase post-mortem`):
1. Incident title (short descriptive name)
2. Timeline (when detected, when triaged, when resolved)
3. Root cause (what went wrong technically)
4. Resolution (what was done to fix it)
5. Impact (users/services affected, duration)

### Example 3: Triage only (P1 urgency)

User: `/incident-to-improvement --phase triage --severity P1 "Payment processing completely down"`

Runs Group A only. Provides immediate severity assessment, mitigation steps, and root cause hypothesis. User applies fix manually and can resume later.

## Error Handling

| Scenario | Action |
|----------|--------|
| Root cause not identifiable | Report as Low confidence with multiple hypotheses |
| Fix introduces regressions | Revert fix, present as manual fix suggestion |
| No test framework configured | Skip regression test generation, note in report |
| KNOWN_ISSUES.md doesn't exist | Create it with initial structure |
| Post-mortem directory doesn't exist | Create `docs/post-mortems/` |
| User provides insufficient context | Ask for: error message, timeline, affected endpoints |
| Incident is in external dependency | Report as external, recommend workaround and vendor contact |

## Troubleshooting

- **Low confidence root cause**: Provide more context -- error logs, stack traces, or reproduction steps improve diagnosis significantly.
- **Regression tests not generated**: Ensure the project has a test framework configured (pytest, vitest, jest). The skill auto-detects from `package.json` or `pyproject.toml`.
- **Post-mortem slug collision**: If a file with the same date+slug already exists, append `-2`, `-3`, etc.
- **KWP skill not available**: If `kwp-engineering-incident-response` or `kwp-customer-support-knowledge-management` are not installed, the pipeline skips those agents and continues with available skills.
