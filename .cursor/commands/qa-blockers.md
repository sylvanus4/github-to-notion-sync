## QA with Blockers

Run a comprehensive QA pass that discovers edge cases and files dependency-ordered issues with explicit blocking relationships.

### Usage

```
/qa-blockers "user authentication feature"
/qa-blockers --scope "PR #142" --severity-threshold major
/qa-blockers "payment flow" --max-issues 20
```

### Workflow

1. **Scope** — Map changed files, classify surfaces (UI flows, API contracts, data model, integrations)
2. **Discover** — Probe each surface for edge cases across 8 categories (boundary, error, auth, concurrency, etc.)
3. **Graph** — Build a DAG of blocking relationships between discovered issues with Mermaid visualization
4. **File** — Produce structured issue bodies with severity, reproduction steps, blocks/blocked-by, and acceptance criteria
5. **Summarize** — Critical path analysis, topological fix order, and PASS/CONDITIONAL/FAIL ship-readiness verdict

### Execution

Read and follow the `qa-with-blockers` skill (`.cursor/skills/review/qa-with-blockers/SKILL.md`) for the full 5-phase QA workflow.

### Examples

Feature branch QA before merge:
```
/qa-blockers "checkout flow redesign"
```

Scoped to a specific PR:
```
/qa-blockers --scope "PR #287" --severity-threshold critical
```
