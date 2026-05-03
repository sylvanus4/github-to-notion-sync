---
name: frontend-expert
description: >-
  Review and improve React component architecture, Vite build performance, Core
  Web Vitals, and testing strategy. Use when asked about frontend code review,
  component refactoring, bundle optimization, or frontend testing gaps.
  Do NOT use for one-page lead-magnet MVP build in the founder pipeline
  (use role-builder for Polish < Proof single-HTML+Tailwind), design system
  work (use design-system), or scaffolding new apps (use
  frontend-ui-engineering).
---

# Frontend Expert

Specialist for a React + TypeScript + Vite + Tailwind CSS frontend.

## Component Architecture Review

### Checklist

- [ ] Components follow single-responsibility principle
- [ ] Presentational vs container separation is clear
- [ ] Props are typed with TypeScript interfaces (not `any`)
- [ ] State stores are scoped (no god-store)
- [ ] React Query for server state, Zustand for client state
- [ ] Custom hooks extract reusable logic
- [ ] Memoization (`React.memo` / `useMemo` / `useCallback`) only where profiling justifies
- [ ] Error boundaries wrap feature-level components
- [ ] Route-level code splitting via `React.lazy` + `Suspense`

### Anti-patterns to Flag

- Prop drilling beyond 2 levels (use store or context)
- Side effects in render (move to `useEffect` or React Query)
- Inline styles or raw CSS instead of Tailwind utilities
- Direct DOM manipulation (use refs sparingly)
- Uncontrolled re-renders from unstable references

## Performance Optimization

### Core Web Vitals Targets

| Metric | Target | How to check |
|--------|--------|-------------|
| LCP | < 2.5s | Lighthouse, `web-vitals` lib |
| INP | < 200ms | Chrome DevTools Performance panel |
| CLS | < 0.1 | Lighthouse |

### Vite Build Checklist

- [ ] Compression plugin for gzip/brotli
- [ ] `rollupOptions.output.manualChunks` for vendor splitting
- [ ] Tree-shaking verified (no barrel re-exports of unused modules)
- [ ] Image assets optimized (WebP conversion)
- [ ] CSS purge enabled via Tailwind `content` config

## Testing Strategy

### Vitest Unit/Integration

- Test hooks and stores in isolation
- Mock API calls with MSW or vi.mock
- Coverage target: >= 80% for hooks/stores, >= 60% for components

### Playwright E2E

- Page Object Model pattern
- Test critical user flows: login, dashboard load, CRUD
- Visual regression with screenshot comparison

## Output Format

```
Frontend Analysis Report
========================
Scope: [components/features reviewed]

1. Architecture
   Rating: [Excellent / Good / Needs Improvement]
   Issues:
   - [Component]: [Issue] -> [Recommendation]

2. Performance
   LCP: [value] | INP: [value] | CLS: [value]
   Bundle size: [total KB] (vendor: [KB], app: [KB])
   Recommendations:
   - [Optimization] -> [Expected impact]

3. Test Coverage
   Unit: [XX%] | E2E scenarios: [N]
   Gaps:
   - [Untested area] -> [Suggested test]

4. Priority Actions
   1. [Action] -- [Effort: Low/Med/High]
   2. [Action] -- [Effort: Low/Med/High]
```

## Test Invocation

```
/frontend-expert
/frontend-expert src/features/dashboard/
/frontend-expert focus on bundle optimization
```
