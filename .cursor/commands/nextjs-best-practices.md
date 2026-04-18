## Next.js Best Practices

Enforce idiomatic Next.js App Router patterns and Vercel deployment optimizations.

### Usage

```
/nextjs-best-practices "app/dashboard"
/nextjs-best-practices --scope "app/(auth)" --focus data-fetching
/nextjs-best-practices "app/products/[id]" --check vercel-deploy
```

### Workflow

1. **Architecture** — Audit router model, `'use client'` directives, layout hierarchy, and route organization
2. **Data Fetching** — Review Server Components, Server Actions, streaming with Suspense, and caching strategies
3. **Performance** — Check rendering strategies (static/ISR/PPR/dynamic), bundle optimization, metadata API
4. **Vercel** — Validate Edge Runtime usage, 4-layer cache config, Image Optimization, and analytics
5. **Anti-Patterns** — Flag and fix common mistakes (unnecessary `'use client'`, API routes for mutations, missing Suspense)

### Execution

Read and follow the `nextjs-best-practices` skill (`.cursor/skills/frontend/nextjs-best-practices/SKILL.md`) for the full 5-phase audit workflow.

### Examples

Full App Router audit:
```
/nextjs-best-practices "app/"
```

Focus on data fetching patterns:
```
/nextjs-best-practices "app/dashboard" --focus data-fetching
```
