## Incident to Improvement

Closed-loop incident response: triage, root cause analysis, fix with regression tests, knowledge base article, monitoring recommendations, and blameless post-mortem — orchestrating 7 skills.

### Usage

```
/incident-to-improvement "500 errors on /api/users since 14:00"
/incident-to-improvement --severity P1 "Database connection pool exhaustion"
/incident-to-improvement --phase triage       # triage only
/incident-to-improvement --phase fix          # skip to fix
/incident-to-improvement --phase post-mortem  # generate post-mortem only
/incident-to-improvement --no-fix             # analysis + post-mortem, no code changes
```

### Workflow

1. **Intake** — Gather incident description, auto-classify severity (P1-P4)
2. **Respond** (parallel) — Incident triage + root cause analysis (3 agents)
3. **Fix and test** — Apply fix, generate regression tests, run suite
4. **Prevent** (parallel) — KB article + monitoring recommendations + post-mortem
5. **Update** — Append to KNOWN_ISSUES.md
6. **Report** — Full incident lifecycle summary

### Execution

Read and follow the `incident-to-improvement` skill (`.cursor/skills/incident-to-improvement/SKILL.md`) for pipeline groups, post-mortem template, and severity classification.

### Examples

Full incident lifecycle:
```
/incident-to-improvement "500 errors on /api/users endpoint since deployment at 14:00"
```

Post-mortem for a resolved incident:
```
/incident-to-improvement --phase post-mortem "Yesterday's auth outage"
```

Triage only (P1 urgency):
```
/incident-to-improvement --phase triage --severity P1 "Payment processing down"
```
