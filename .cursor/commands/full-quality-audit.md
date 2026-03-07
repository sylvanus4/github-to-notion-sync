## Full Quality Audit

Orchestrated multi-skill quality audit that runs CI checks, security review, and compliance checks in parallel, then aggregates results and auto-fixes where possible.

### Workflow

1. Read the mission-control skill at `.cursor/skills/mission-control/SKILL.md`
2. Follow **WF-1: Full Quality Audit** defined there
3. Execute in this order:

**Parallel Batch (use Task subagents, up to 3 concurrent):**

- **ci-quality-gate**: Read `.cursor/skills/ci-quality-gate/SKILL.md` and run the full local CI pipeline (secret scan, Python lint/test, Go lint/test, frontend lint/test/build, schema check)
- **security-expert**: Read `.cursor/skills/security-expert/SKILL.md` and perform STRIDE threat model + OWASP Top 10 check + secret scan + PII handling review on recent changes
- **compliance-governance**: Read `.cursor/skills/compliance-governance/SKILL.md` and review data classification, access control, audit logging

**Sequential (after parallel batch):**

4. Aggregate all findings into a unified report sorted by severity (Critical > High > Medium > Low)
5. Auto-fix where possible:
   - `ruff check --fix shared/ services/` for Python lint
   - `black shared/ services/` for Python formatting
   - `cd frontend && npm run lint -- --fix` for frontend lint
6. If fixes were applied, use the domain-commit skill (`.cursor/skills/domain-commit/SKILL.md`) to commit changes

### Output

Deliver a unified **Quality Audit Report** with:
- Overall status (PASS / FAIL / WARN)
- Findings count by severity
- Per-skill detailed results
- Auto-fix actions taken
- Remaining issues requiring manual attention
