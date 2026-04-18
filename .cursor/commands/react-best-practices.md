## React Best Practices

Enforce React/Next.js best practices: component architecture, hooks patterns, performance, and testing strategy.

### Usage

```
/react-best-practices                         # review all React code
/react-best-practices src/components/          # review specific directory
/react-best-practices --focus performance      # focus on performance patterns
/react-best-practices --focus hooks            # focus on hooks usage
```

### Workflow

1. **Scan** — Identify React components, hooks, and patterns in scope
2. **Audit** — Check against Vercel/Next.js style best practices
3. **Flag issues** — Component architecture, unnecessary re-renders, hook deps, error boundaries
4. **Suggest fixes** — Concrete code changes with rationale
5. **Report** — Prioritized findings with severity levels

### Execution

Read and follow the `frontend-expert` skill (`.cursor/skills/frontend/frontend-expert/SKILL.md`) for React component review, Vite build optimization, Core Web Vitals, and testing strategy.

### Examples

Full React code review:
```
/react-best-practices
```

Performance-focused review:
```
/react-best-practices --focus performance src/features/
```
