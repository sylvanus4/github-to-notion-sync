---
name: zoom-out
description: >
  Tell the agent to zoom out and give broader context or a higher-level
  perspective on an unfamiliar section of code. Use when user says "zoom out",
  "big picture", "broader context", "how does this fit", or is lost in unfamiliar code.
---

# Zoom Out

When exploring unfamiliar code, **map before you dig**.

## Process

1. **Identify the module** the user is looking at
2. **Find its callers** — who uses this module? (grep for imports, usages)
3. **Find its dependencies** — what does this module depend on?
4. **Map the neighborhood** — draw the module in context:
   - Upstream (what calls it)
   - Downstream (what it calls)
   - Siblings (modules at the same level)
5. **Explain in domain terms** — use the project's vocabulary, not implementation jargon
6. **Identify the role** — what job does this module do in the larger system?

## Output format

```
[Caller A] --calls--> [THIS MODULE] --calls--> [Dependency X]
[Caller B] -------/                  \-------> [Dependency Y]
```

**Role**: [One sentence describing the module's job in domain terms]

**Key behaviors**: [2-3 most important things this module does]

**Why it exists**: [What would break or be harder without it]

## Rules

- Use domain vocabulary from CONTEXT.md if it exists
- Don't explain implementation details unless asked
- Focus on relationships and responsibilities, not code structure
- If the module's role is unclear, say so -- that's useful information
