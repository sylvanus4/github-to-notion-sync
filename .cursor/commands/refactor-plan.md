## Refactor Plan

Simulate blast radius of a proposed refactor, then produce a detailed plan with tiny commits and a GitHub issue.

### Usage

```
/refactor-plan "rename UserService to AccountService"  # plan a specific refactor
/refactor-plan src/api/auth/                           # plan refactor for a directory
/refactor-plan --file-issue                            # also create a GitHub issue
```

### Workflow

1. **Interview** — Clarify refactor scope, goals, and constraints
2. **Blast radius** — Analyze call sites, import chains, type dependencies, and test coverage
3. **Risk assessment** — Score impact by number of affected files and test coverage gaps
4. **Plan commits** — Break refactor into atomic, bisect-safe commit steps
5. **Output** — Detailed plan with risk scores and optional GitHub issue

### Execution

Read and follow the `refactor-simulator` skill (`.cursor/skills/review/refactor-simulator/SKILL.md`) for blast radius analysis, risk scoring, and impact report format.

### Examples

Plan a rename refactor:
```
/refactor-plan "rename all usages of OrderDTO to OrderResponse"
```

Plan and file as issue:
```
/refactor-plan --file-issue "extract shared validation logic into a utils module"
```
