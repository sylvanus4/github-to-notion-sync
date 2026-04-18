## Improve Architecture

Explore a codebase for architectural improvement opportunities, focusing on deepening shallow modules and improving testability.

### Usage

```
/improve-architecture                          # scan entire project
/improve-architecture src/api/                 # scan a specific directory
/improve-architecture --top 5                  # show top 5 hotspots only
```

### Workflow

1. **Scan** — Analyze module boundaries, dependency depth, and code complexity
2. **Identify hotspots** — Find shallow modules, god functions, and tight coupling
3. **Propose strategies** — Generate 2-3 refactor strategies with risk/effort/impact
4. **Detail plans** — Break each strategy into actionable steps
5. **Report** — Prioritized improvement list with architecture diagrams

### Execution

Read and follow the `simplify` skill (`.cursor/skills/review/simplify/SKILL.md`) in full mode for codebase-wide analysis. Combine with `deep-review` (`.cursor/skills/review/deep-review/SKILL.md`) for multi-domain perspective.

### Examples

Full architecture scan:
```
/improve-architecture
```

Focus on a specific module:
```
/improve-architecture src/services/
```
