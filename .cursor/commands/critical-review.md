## Critical Review

End-to-end CTO/CEO critical review and remediation pipeline: dual-perspective technical and strategic critique, PM documentation (PRD, OKRs, Lean Canvas, SWOT), 3-sprint remediation, and executive summary .docx generation.

### Usage

```
# Execution modes
/critical-review                      # full pipeline — all 4 phases
/critical-review review-only          # Phase 1 only — CTO + CEO reviews
/critical-review with-implementation  # Phases 1-3 — reviews + PM docs + sprints
/critical-review docs-only            # Phase 4 only — generate docs from existing reviews
```

### Workflow

1. **Phase 1: Critical Reviews** — Parallel CTO + CEO reviews (4 sections x 4 issues each)
2. **Phase 2: PM Documents** — PRD, OKRs, Lean Canvas, SWOT from review findings
3. **Phase 3: Sprint Execution** — 3 sprints: Foundation, Test Quality, UX/Performance
4. **Phase 4: Documentation** — Remediation summary .md + executive summary .docx

### Execution

Read and follow the `critical-review` skill (`.cursor/skills/critical-review/SKILL.md`) for phase details, agent prompts, output templates, and error handling.

### Examples

Full CTO/CEO review with remediation:
```
/critical-review
```

Assess the project without making changes:
```
/critical-review review-only
```

Generate docs from previous review findings:
```
/critical-review docs-only
```
