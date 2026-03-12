---
name: frontend-expert
description: >-
  Review and improve React component architecture, Vite build performance, Core
  Web Vitals, and testing strategy. Use when the user asks about frontend code
  review, component refactoring, bundle optimization, or frontend testing gaps.
  Do NOT use for building new UI from scratch (use frontend-design), UX audits
  or accessibility evaluation (use ux-expert), or writing Playwright E2E tests
  (use e2e-testing). Korean triggers: "프론트엔드", "감사", "리뷰", "테스트".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# Frontend Expert

Specialist for the React 18 + TypeScript + Vite 6 + Tailwind CSS frontend at `frontend/`.

## Key Directories

- `frontend/src/components/` — Reusable UI components
- `frontend/src/features/` — Feature modules (admin, auth, call, chatbot, dashboard, knowledge, summary)
- `frontend/src/hooks/` — Custom React hooks
- `frontend/src/stores/` — Zustand state stores (authStore, callStore, chatStore)
- `frontend/src/config/` — API clients, env config
- `frontend/src/lib/` — Utilities (api.ts, cn.ts)
- `frontend/src/i18n/` — Internationalization (react-i18next)
- `frontend/src/test/` — Test setup and helpers

## Component Architecture Review

### Checklist

- [ ] Components follow single-responsibility principle
- [ ] Presentational vs container separation is clear
- [ ] Props are typed with TypeScript interfaces (not `any`)
- [ ] Zustand stores are scoped (no god-store)
- [ ] React Query used for server state, Zustand for client state
- [ ] Custom hooks extract reusable logic from components
- [ ] `React.memo` / `useMemo` / `useCallback` used only where profiling justifies
- [ ] Error boundaries wrap feature-level components
- [ ] Lazy loading via `React.lazy` + `Suspense` for route-level code splitting

### Anti-patterns to Flag

- Prop drilling beyond 2 levels (use Zustand or context)
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

- [ ] `vite-plugin-compression` for gzip/brotli
- [ ] `rollupOptions.output.manualChunks` for vendor splitting
- [ ] Tree-shaking verified (no barrel re-exports of unused modules)
- [ ] Image assets optimized (`vite-plugin-imagemin` or WebP conversion)
- [ ] CSS purge enabled via Tailwind `content` config

## Testing Strategy

### Playwright E2E

- Tests at `frontend/` level, run with `pnpm test:e2e`
- Page Object Model pattern for maintainability
- Test critical user flows: login, dashboard load, CRUD operations
- Visual regression with screenshot comparison

### Vitest Unit/Integration

- Run with `pnpm test` or `vitest`
- Test hooks and stores in isolation
- Mock API calls with MSW or vi.mock
- Coverage target: >= 80% for hooks/stores, >= 60% for components

## Examples

### Example 1: Component architecture review
User says: "Review the dashboard feature components"
Actions:
1. Read `frontend/src/features/dashboard/` component files
2. Check for single-responsibility, prop typing, and state management patterns
3. Identify anti-patterns (prop drilling, inline styles, uncontrolled re-renders)
Result: Architecture review with specific refactoring recommendations

### Example 2: Bundle optimization
User says: "The frontend build is too large"
Actions:
1. Run `npm run build` and analyze chunk sizes
2. Check for missing code splitting, tree-shaking issues, or large dependencies
3. Suggest vendor splitting and lazy loading strategies
Result: Performance report with bundle size breakdown and optimization plan

## Troubleshooting

### Vite build out of memory
Cause: Large dependency tree or missing code splitting
Solution: Add `manualChunks` in rollup options and split vendor bundles

### Zustand store re-renders
Cause: Subscribing to entire store instead of specific selectors
Solution: Use `useStore(state => state.specificField)` instead of `useStore()`

## Output Format

```
Frontend Analysis Report
========================
Scope: [components/features reviewed]

1. Architecture
   Rating: [Excellent / Good / Needs Improvement]
   Issues:
   - [Component]: [Issue] → [Recommendation]

2. Performance
   LCP: [value] | INP: [value] | CLS: [value]
   Bundle size: [total KB] (vendor: [KB], app: [KB])
   Recommendations:
   - [Optimization] → [Expected impact]

3. Test Coverage
   Unit: [XX%] | E2E scenarios: [N]
   Gaps:
   - [Untested area] → [Suggested test]

4. Priority Actions
   1. [Action] — [Effort: Low/Med/High]
   2. [Action] — [Effort: Low/Med/High]
   3. [Action] — [Effort: Low/Med/High]
```
