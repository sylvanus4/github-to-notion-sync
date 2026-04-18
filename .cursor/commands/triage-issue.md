## Triage Issue

Investigate a bug by exploring the codebase, identify the root cause, and file a GitHub issue with a TDD-based fix plan.

### Usage

```
/triage-issue "TypeError in auth module"       # investigate a specific error
/triage-issue src/api/users.ts                  # investigate a specific file
/triage-issue --no-issue                        # diagnose only, skip issue creation
```

### Workflow

1. **Reproduce** — Gather error context, logs, and minimal reproduction steps
2. **Diagnose** — Run 3 parallel analysis agents to identify root cause
3. **Plan fix** — Design a TDD-based fix: failing test first, then minimal code change
4. **File issue** — Create a GitHub issue with root cause, reproduction steps, and fix plan
5. **Report** — Diagnosis summary with confidence level and next steps

### Execution

Read and follow the `diagnose` skill (`.cursor/skills/review/diagnose/SKILL.md`) for root cause analysis. Use `commit-to-issue` (`.cursor/skills/review/commit-to-issue/SKILL.md`) for GitHub issue creation with project field setup.

### Examples

Triage a runtime error:
```
/triage-issue "Cannot read property 'id' of undefined in UserService"
```

Investigate a file without filing:
```
/triage-issue --no-issue src/api/billing.ts
```
