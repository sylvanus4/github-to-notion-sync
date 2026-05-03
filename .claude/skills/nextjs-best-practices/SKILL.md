---
name: nextjs-best-practices
description: >-
  Enforce Next.js App Router and Vercel deployment best practices — Server
  Components by default, client boundary minimization, streaming with
  Suspense, route handler patterns, metadata API, ISR/PPR strategies, and
  Vercel-specific optimizations (Edge Runtime, Image Optimization, Analytics).
  Distinct from frontend-expert (general React/Vite review) and
  fsd-development (FSD architecture scaffolding) — this skill targets Next.js
  App Router idioms and Vercel platform patterns specifically. Use when the
  user asks to "review Next.js code", "Next.js best practices", "App Router
  patterns", "migrate to App Router", "Vercel deployment review", "Server
  Component optimization", "Next.js 코드 리뷰", "App Router 패턴", "서버 컴포넌트 최적화",
  "Vercel 배포 패턴", "Next.js 마이그레이션", "RSC 패턴", "streaming 패턴", or is
  building/reviewing a Next.js 14+ application deployed to Vercel. Do NOT use
  for general React component review without Next.js context (use
  frontend-expert). Do NOT use for FSD architecture scaffolding (use
  fsd-development). Do NOT use for design system or Tailwind configuration
  (use tailwind-design-system). Do NOT use for general Vite/SPA React apps
  (use frontend-expert).
---

# Next.js Best Practices

Enforce idiomatic Next.js App Router patterns and Vercel deployment optimizations for production-grade applications.

## When to Use

- Building or reviewing Next.js 14+ applications with App Router
- Migrating from Pages Router to App Router
- Optimizing for Vercel deployment (Edge, ISR, PPR, Image Optimization)
- Reviewing Server Component vs Client Component boundaries
- Setting up data fetching, caching, and revalidation strategies

## When NOT to Use

- General React review without Next.js (use `frontend-expert`)
- FSD architecture scaffolding for the AI Platform frontend (use `fsd-development`)
- Design system token or Tailwind setup (use `tailwind-design-system`)
- Vite-based SPA React applications (use `frontend-expert`)

## Workflow

### Phase 1: Architecture Audit

1. **Router model**: Confirm App Router (`app/` directory) is used, not Pages Router
2. **Component classification**: Identify every `'use client'` directive
   - Goal: Minimize client boundaries — push them as deep as possible
   - Flag components with `'use client'` that don't use hooks or browser APIs
3. **Layout hierarchy**: Verify `layout.tsx` / `template.tsx` / `loading.tsx` / `error.tsx` / `not-found.tsx` usage
4. **Route organization**: Check for colocation (components next to their route), route groups `(group)`, parallel routes `@slot`, and intercepting routes `(.)path`

### Phase 2: Data Fetching Review

1. **Server-side data**:
   - Prefer `async` Server Components with direct `fetch()` or DB calls
   - Use `cache()` for request deduplication across components
   - Set appropriate `revalidate` values or use `revalidateTag()` / `revalidatePath()`
2. **Client-side data**:
   - Use Server Actions (`'use server'`) for mutations, not API routes
   - Reserve Route Handlers (`route.ts`) for external webhooks and third-party integrations
   - Use `useOptimistic()` for optimistic UI updates
3. **Streaming**:
   - Wrap slow data fetches in `<Suspense>` with meaningful fallbacks
   - Use `loading.tsx` for route-level streaming
   - Implement `generateStaticParams()` for static generation with dynamic routes

### Phase 3: Performance Patterns

1. **Rendering strategies**:
   - Static (default) → Dynamic (`force-dynamic`, `cookies()`, `headers()`)
   - ISR with `revalidate: N` for content that changes periodically
   - PPR (Partial Pre-Rendering) for pages mixing static shell + dynamic content
2. **Bundle optimization**:
   - Dynamic imports with `next/dynamic` for heavy client components
   - Tree-shake barrel exports — avoid `export * from` patterns
   - Use `next/image` with `sizes` and `priority` attributes correctly
   - Lazy-load below-the-fold content
3. **Metadata**:
   - Use `generateMetadata()` for dynamic SEO metadata
   - Set `viewport`, `robots`, OpenGraph, and Twitter card metadata
   - Implement `sitemap.ts` and `robots.ts` for crawlers

### Phase 4: Vercel Platform Optimization

1. **Edge Runtime**:
   - Use `runtime: 'edge'` for latency-sensitive Route Handlers
   - Verify Edge-compatible APIs (no Node.js `fs`, `child_process`, etc.)
2. **Caching**:
   - Understand the 4-layer cache: Request Memoization → Data Cache → Full Route Cache → Router Cache
   - Set `fetchCache` and `revalidate` correctly per route segment
3. **Image Optimization**:
   - Use `next/image` for all images (automatic WebP/AVIF, responsive sizing)
   - Configure `remotePatterns` in `next.config.js` for external images
4. **Analytics & Monitoring**:
   - Integrate `@vercel/analytics` for Web Vitals
   - Use `@vercel/speed-insights` for performance monitoring
5. **Environment variables**:
   - `NEXT_PUBLIC_*` for client-accessible values only
   - Server-only secrets without the `NEXT_PUBLIC_` prefix

### Phase 5: Common Anti-Patterns

Flag and fix these patterns:

| Anti-Pattern | Fix |
|---|---|
| `'use client'` at the top of every component | Push client boundaries to leaf components |
| `useEffect` for data fetching | Use async Server Components |
| API routes for internal mutations | Use Server Actions |
| `getServerSideProps` / `getStaticProps` | Migrate to App Router data fetching |
| Client-side `fetch` in Server Components | Call DB/service directly |
| Missing `<Suspense>` around async children | Wrap with fallback UI |
| `next/image` without `sizes` prop | Add responsive `sizes` |
| Barrel exports (`index.ts` re-exporting everything) | Direct imports |

## Gotchas

1. **Adding `'use client'` to fix a build error without understanding why.** The build error often means you're using a client API in a Server Component. Move just the interactive part to a Client Component and keep the rest on the server.
2. **Forgetting that `cookies()` and `headers()` opt the entire route into dynamic rendering.** If you call `cookies()` in a layout, every page under that layout becomes dynamic. Scope these calls as narrowly as possible.
3. **Over-caching with ISR when data is user-specific.** ISR caches at the CDN level for all users. User-specific data must be fetched dynamically or via client-side queries.
4. **Ignoring the Router Cache.** Client-side navigation caches route segments for 30 seconds (dynamic) or 5 minutes (static). Users may see stale data after mutations unless you call `router.refresh()` or `revalidatePath()`.

## Verification

After completing the review:
1. Run `next build` — zero warnings about unoptimized images or missing metadata
2. Verify `'use client'` directives are only in components that genuinely need browser APIs or hooks
3. Confirm every dynamic route has either `generateStaticParams()` or an explicit rendering strategy
4. Check Lighthouse score ≥ 90 for Performance, Accessibility, Best Practices, SEO
5. Validate that no API route is used for internal mutations (Server Actions should handle these)

## Anti-Example

```typescript
// BAD: Entire page is client-side for no reason
'use client'
export default function DashboardPage() {
  const data = await fetch('/api/dashboard') // Can't await in client component!
  return <Dashboard data={data} />
}
// → Remove 'use client', make it a Server Component, fetch directly

// BAD: API route for internal mutation
// app/api/update-profile/route.ts
export async function POST(req) { ... }
// app/components/ProfileForm.tsx
fetch('/api/update-profile', { method: 'POST', body: ... })
// → Use a Server Action instead

// BAD: useEffect for initial data loading
'use client'
export default function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => { fetch('/api/users').then(...) }, [])
  // → Make this a Server Component and fetch directly
}
```

## Constraints

- Every `'use client'` directive must be justified by a browser API or React hook usage
- Server Actions (`'use server'`) must validate inputs before any mutation
- All images must use `next/image` with appropriate `sizes` and `priority`
- Dynamic routes must have an explicit rendering strategy (static, ISR, or dynamic)
- Do NOT use API routes for internal data mutations — use Server Actions
- Freedom level: **Structured** — follow the 5-phase audit; adapt recommendations to the project's existing patterns

## Output

1. Architecture audit summary (router model, component classification, layout hierarchy)
2. Data fetching review (server vs client, streaming opportunities)
3. Performance recommendations (rendering strategy, bundle optimization, metadata)
4. Vercel optimization checklist (Edge Runtime, caching, image optimization)
5. Anti-pattern report with specific file locations and fix suggestions
