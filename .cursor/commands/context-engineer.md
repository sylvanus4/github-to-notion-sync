## Context Engineer

Manage project knowledge architecture — MEMORY.md, domain glossaries, context packages, and agent context optimization.

### Usage

```
/context-engineer                         # Interactive: choose mode
/context-engineer refresh                 # Refresh MEMORY.md with current state
/context-engineer package <domain>        # Create context package for a domain
/context-engineer glossary                # Update domain glossary
/context-engineer optimize               # Optimize agent context loading
/context-engineer audit                   # Audit all context sources for staleness
```

### Workflow

1. **Refresh** — Update MEMORY.md with recent commits, tasks, and decisions
2. **Package** — Build reusable context packages for analysis domains
3. **Glossary** — Maintain domain-specific terminology
4. **Optimize** — Ensure progressive disclosure and right-sized context
5. **Audit** — Check for stale, redundant, or missing context

### Execution

Read and follow the `context-engineer` skill (`.cursor/skills/context-engineer/SKILL.md`) for the knowledge architecture tiers, update protocols, and quality checks.

### Examples

Post-work context refresh:
```
/context-engineer refresh
```

Build technical analysis context:
```
/context-engineer package technical-analysis
```

Optimize slow agent responses:
```
/context-engineer optimize
```
