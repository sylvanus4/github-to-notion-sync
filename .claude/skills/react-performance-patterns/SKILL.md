---
name: react-performance-patterns
description: >-
  70 React performance optimization rules across 8 categories, adapted from
  Vercel's react-best-practices for React + Vite + Tailwind CSS v4 + Radix UI
  stacks. Covers waterfalls, bundle size, data fetching, re-renders,
  rendering, JS micro-optimizations, and advanced patterns. Self-contained —
  no external URL fetching required.
---

# React Performance Patterns

**70 rules · 8 categories · React + Vite stack**

Adapted from Vercel's react-best-practices. Next.js-specific APIs replaced
with generic React/Vite equivalents.

---

## 1. Eliminating Waterfalls — **HIGH**

Sequential data fetches are the #1 performance killer.

### 1.1 Start Fetching Before Rendering — CRITICAL

Initiate data fetches at the route level, not inside components.

```tsx
// ❌ Waterfall: component mounts → then fetches
function Dashboard() {
  const { data } = useSWR('/api/stats', fetcher)
  if (!data) return <Skeleton />
  return <Stats data={data} />
}

// ✅ Fetch at route loader level (React Router)
export async function loader() {
  return fetch('/api/stats').then(r => r.json())
}
function Dashboard() {
  const data = useLoaderData<typeof loader>()
  return <Stats data={data} />
}
```

### 1.2 Parallelize Independent Fetches — CRITICAL

Never chain fetches that don't depend on each other.

```tsx
// ❌ Sequential
const user = await fetchUser(id)
const posts = await fetchPosts(id)

// ✅ Parallel
const [user, posts] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
])
```

### 1.3 Preload Data for Anticipated Navigation — HIGH

Trigger fetches on hover/focus of links before the user clicks.

```tsx
function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const prefetch = () => queryClient.prefetchQuery({ queryKey: [to] })
  return (
    <Link to={to} onMouseEnter={prefetch} onFocus={prefetch}>
      {children}
    </Link>
  )
}
```

### 1.4 Use Suspense Boundaries for Streaming — HIGH

Wrap slow sections in `<Suspense>` with fallbacks so the rest of the page
renders immediately.

```tsx
<Suspense fallback={<TableSkeleton />}>
  <AsyncDataTable />
</Suspense>
```

### 1.5 Deduplicate Identical Requests — MEDIUM

Use SWR or TanStack Query for automatic deduplication; for manual fetch
use a module-level cache Map.

```tsx
const inflightMap = new Map<string, Promise<unknown>>()
export function deduplicatedFetch(url: string) {
  if (!inflightMap.has(url)) {
    inflightMap.set(url, fetch(url).then(r => r.json()).finally(() => inflightMap.delete(url)))
  }
  return inflightMap.get(url)!
}
```

### 1.6 Colocate Data Requirements with Components — MEDIUM

Each component declares the data shape it needs; parent assembles fetches.

### 1.7 Avoid Conditional Fetch Chains — MEDIUM

Don't gate fetches behind `if (previousData)` unless truly dependent.
Use `Promise.allSettled` when partial failure is acceptable.

---

## 2. Bundle Size Optimization — **HIGH**

### 2.1 Route-Based Code Splitting with React.lazy — CRITICAL

```tsx
import { lazy, Suspense } from 'react'

const Settings = lazy(() => import('./pages/Settings'))

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  )
}
```

### 2.2 Lazy-Load Below-Fold Components — HIGH

```tsx
const HeavyChart = lazy(() => import('./HeavyChart'))

function Dashboard() {
  return (
    <>
      <AboveFoldMetrics />
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart />
      </Suspense>
    </>
  )
}
```

### 2.3 Import Only What You Need (Tree-Shake) — HIGH

```tsx
// ❌ Imports entire library
import _ from 'lodash'
_.debounce(fn, 300)

// ✅ Cherry-pick
import debounce from 'lodash/debounce'
debounce(fn, 300)
```

### 2.4 Analyze Bundles Regularly — MEDIUM

Use `npx vite-bundle-visualizer` (Vite) to spot unexpected large deps.

### 2.5 Prefer Native APIs Over Libraries — MEDIUM

`structuredClone()` over lodash `cloneDeep`, `URL` over manual parsing,
`crypto.randomUUID()` over uuid.

### 2.6 Lazy-Load Third-Party Scripts — MEDIUM

```tsx
// ❌ Eager
import 'analytics-sdk'

// ✅ Lazy after interaction
button.addEventListener('click', async () => {
  const { init } = await import('analytics-sdk')
  init()
}, { once: true })
```

### 2.7 Audit and Remove Unused Dependencies — LOW

Run `npx depcheck` periodically.

---

## 3. Server-Side Performance — **MEDIUM**

> These rules apply to SSR setups (Vite SSR, Astro, Remix). Skip if your
> app is a pure SPA.

### 3.1 Cache Expensive Server Computations — HIGH

Use `React.cache()` in server-component contexts to deduplicate within
a single render pass.

```tsx
import { cache } from 'react'
const getUser = cache(async (id: string) => db.user.findUnique({ where: { id } }))
```

### 3.2 Defer Non-Critical Server Work — HIGH

After sending the response, run analytics/logging via
`requestIdleCallback` or a post-response hook.

```tsx
requestIdleCallback(() => {
  trackAnalytics({ event: 'page_view', path: location.pathname })
})
```

### 3.3 Stream Long Responses — MEDIUM

Use `ReadableStream` for large payloads; combine with `<Suspense>` on
the client.

### 3.4 Validate Inputs Early with Zod — MEDIUM

```tsx
import { z } from 'zod'
const schema = z.object({ email: z.string().email(), name: z.string().min(1) })
```

### 3.5 Return Minimal Data from APIs — LOW

Select only the fields the client needs. Avoid passing entire DB rows.

---

## 4. Client-Side Data Fetching — **MEDIUM**

### 4.1 Use SWR or TanStack Query for Client Fetches — HIGH

Built-in deduplication, revalidation, caching, and error/loading states.

```tsx
import useSWR from 'swr'
const { data, error, isLoading } = useSWR('/api/user', fetcher)
```

### 4.2 Implement Optimistic Updates — HIGH

Mutate the local cache before the server responds for instant UI feedback.

```tsx
const { trigger } = useSWRMutation('/api/todo', postTodo, {
  optimisticData: (current) => [...(current ?? []), newTodo],
  rollbackOnError: true,
})
```

### 4.3 Subscribe to Real-Time Data Efficiently — MEDIUM

Use `useSWRSubscription` or a similar pattern to bridge WebSocket/SSE
with the caching layer.

```tsx
useSWRSubscription('/api/price', (key, { next }) => {
  const ws = new WebSocket(key)
  ws.onmessage = (e) => next(null, JSON.parse(e.data))
  return () => ws.close()
})
```

### 4.4 Use Passive Event Listeners for Scroll/Touch — MEDIUM

```tsx
useEffect(() => {
  const handler = () => { /* scroll logic */ }
  window.addEventListener('scroll', handler, { passive: true })
  return () => window.removeEventListener('scroll', handler)
}, [])
```

### 4.5 Paginate or Infinite-Scroll Large Datasets — MEDIUM

Never fetch thousands of rows at once. Use cursor-based pagination.

### 4.6 Debounce Search / Filter Inputs — LOW

```tsx
const debouncedSearch = useDebouncedCallback((q: string) => {
  setSearchQuery(q)
}, 300)
```

---

## 5. Re-Render Optimization — **HIGH**

### 5.1 Derive State Instead of Syncing — CRITICAL

```tsx
// ❌ Synced state
const [items, setItems] = useState(data)
const [filtered, setFiltered] = useState(data)
useEffect(() => setFiltered(items.filter(…)), [items])

// ✅ Derived
const filtered = useMemo(() => items.filter(…), [items, filterKey])
```

### 5.2 Defer Expensive State Reads — HIGH

Wrap state updates that trigger large re-renders with `useTransition`.

```tsx
const [isPending, startTransition] = useTransition()
function handleFilter(value: string) {
  startTransition(() => setFilter(value))
}
```

### 5.3 Don't useMemo for Simple Expressions — HIGH

```tsx
// ❌ Overhead exceeds benefit
const fullName = useMemo(() => `${first} ${last}`, [first, last])

// ✅ Inline
const fullName = `${first} ${last}`
```

### 5.4 Never Define Components Inside Components — CRITICAL

```tsx
// ❌ New component identity every render → full remount
function Parent() {
  function Child() { return <div /> }
  return <Child />
}

// ✅ Separate declaration
function Child() { return <div /> }
function Parent() { return <Child /> }
```

### 5.5 Use Functional setState for Updates — HIGH

```tsx
// ❌ Stale closure risk
setCount(count + 1)

// ✅ Always current
setCount((prev) => prev + 1)
```

### 5.6 Use Lazy State Initialization — MEDIUM

```tsx
// ❌ Runs every render
const [state, setState] = useState(JSON.parse(localStorage.getItem('key')!))

// ✅ Runs once
const [state, setState] = useState(() => JSON.parse(localStorage.getItem('key')!))
```

### 5.7 Use useTransition for Non-Urgent Updates — HIGH

Show stale content while computing updates:

```tsx
const [isPending, startTransition] = useTransition()
startTransition(() => setResults(expensiveFilter(query)))
return isPending ? <Spinner /> : <Results data={results} />
```

### 5.8 Use useDeferredValue for Deferred Rendering — MEDIUM

```tsx
const deferredQuery = useDeferredValue(query)
const results = useMemo(() => search(deferredQuery), [deferredQuery])
```

### 5.9 Use useRef for Values That Don't Need Re-Renders — MEDIUM

```tsx
const renderCount = useRef(0)
renderCount.current += 1
```

### 5.10 Memoize Expensive Computations — MEDIUM

Only when the computation measurably impacts render time:

```tsx
const sorted = useMemo(() => data.sort(compareFn), [data])
```

### 5.11 Avoid Spreading Props Blindly — LOW

Spread can pass unwanted props and cause unnecessary re-renders:

```tsx
// ❌
<Input {...formState} />

// ✅
<Input value={formState.value} onChange={formState.onChange} />
```

---

## 6. Rendering Performance — **MEDIUM**

### 6.1 Use content-visibility for Off-Screen Sections — HIGH

```css
.off-screen-section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
```

### 6.2 Virtualize Large Lists — HIGH

Use `virtua`, `@tanstack/react-virtual`, or CSS `content-visibility: auto`
for 50+ item lists.

```tsx
import { VList } from 'virtua'

function MessageList({ messages }: { messages: Message[] }) {
  return (
    <VList style={{ height: '100vh' }}>
      {messages.map((msg) => (
        <MessageItem key={msg.id} message={msg} />
      ))}
    </VList>
  )
}
```

### 6.3 Hoist Static JSX Elements — LOW

```tsx
// ❌ Re-created every render
function Component() {
  const icon = <Icon size={16} />
  return <Button icon={icon} />
}

// ✅ Module-level constant
const icon = <Icon size={16} />
function Component() {
  return <Button icon={icon} />
}
```

### 6.4 Optimize SVG Precision — LOW

Reduce `d` path precision to 1-2 decimal places. Remove metadata.

### 6.5 Prevent Hydration Mismatch Without Flickering — MEDIUM

Use CSS `display: none` / `display: block` with media queries instead of
`useEffect` + state toggle to avoid flash:

```tsx
<div className="hidden md:block"><DesktopNav /></div>
<div className="md:hidden"><MobileNav /></div>
```

### 6.6 Use suppressHydrationWarning Judiciously — LOW

Only for expected mismatches (timestamps, random IDs):

```tsx
<time suppressHydrationWarning>{new Date().toLocaleString()}</time>
```

### 6.7 Use defer/async on Script Tags — LOW

```html
<script defer src="/analytics.js"></script>
```

### 6.8 Prefer Explicit Conditionals — LOW

```tsx
// ❌ Renders "0" when count is 0
{count && <Badge count={count} />}

// ✅ Explicit boolean
{count > 0 && <Badge count={count} />}
```

### 6.9 Use React DOM Resource Hints — LOW

```tsx
import { prefetchDNS, preconnect, preload, preinit } from 'react-dom'

prefetchDNS('https://cdn.example.com')
preconnect('https://api.example.com')
preload('/fonts/inter.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' })
```

---

## 7. JavaScript Performance — **LOW–MEDIUM**

### 7.1 Avoid Layout Thrashing — HIGH

```tsx
// ❌ Read-write interleave
items.forEach((el) => {
  const h = el.offsetHeight    // read (forces layout)
  el.style.height = h * 2 + 'px' // write (invalidates layout)
})

// ✅ Batch reads, then writes
const heights = items.map((el) => el.offsetHeight)
items.forEach((el, i) => { el.style.height = heights[i] * 2 + 'px' })
```

### 7.2 Build Index Maps for Repeated Lookups — MEDIUM

```tsx
// ❌ O(n) per lookup
users.find((u) => u.id === targetId)

// ✅ O(1) with index map
const userById = new Map(users.map((u) => [u.id, u]))
userById.get(targetId)
```

### 7.3 Cache Property Access in Loops — LOW

```tsx
// ❌ items.length re-evaluated each iteration
for (let i = 0; i < items.length; i++) { … }

// ✅ Cached length
for (let i = 0, len = items.length; i < len; i++) { … }
```

### 7.4 Cache Repeated Function Calls — MEDIUM

```tsx
const cache = new Map<string, Result>()
function expensive(key: string): Result {
  if (cache.has(key)) return cache.get(key)!
  const result = compute(key)
  cache.set(key, result)
  return result
}
```

### 7.5 Cache Storage API Calls — LOW

Read `localStorage`/`sessionStorage` once and cache in a variable.

### 7.6 Combine Multiple Array Iterations — LOW

```tsx
// ❌ Two passes
const names = users.map(u => u.name)
const active = names.filter(n => n.startsWith('A'))

// ✅ Single pass
const active = users.reduce<string[]>((acc, u) => {
  if (u.name.startsWith('A')) acc.push(u.name)
  return acc
}, [])
```

### 7.7 Defer Non-Critical Work with requestIdleCallback — MEDIUM

```tsx
requestIdleCallback(() => {
  reportAnalytics(data)
})
```

### 7.8 Early Return from Functions — LOW

Check error/empty conditions first to avoid deep nesting.

### 7.9 Use Set/Map for O(1) Lookups — MEDIUM

```tsx
const idSet = new Set(ids)
const matches = items.filter((item) => idSet.has(item.id))
```

### 7.10 Use flatMap for Map + Filter in One Pass — LOW

```tsx
const results = items.flatMap((item) =>
  item.isActive ? [transform(item)] : []
)
```

### 7.11 Use toSorted() for Immutable Sort — LOW

```tsx
const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name))
```

### 7.12 Hoist RegExp Creation — LOW

```tsx
// ❌ Created every call
function validate(s: string) { return /^[a-z]+$/i.test(s) }

// ✅ Module-level
const ALPHA_RE = /^[a-z]+$/i
function validate(s: string) { return ALPHA_RE.test(s) }
```

---

## 8. Advanced Patterns — **MEDIUM**

### 8.1 Don't Put Effect Events in Dependency Arrays — HIGH

```tsx
const onMessage = useEffectEvent((msg: Message) => {
  showNotification(msg, theme) // reads `theme` without being a dependency
})

useEffect(() => {
  connection.on('message', onMessage)
  return () => connection.off('message', onMessage)
}, [connection]) // onMessage NOT in deps
```

### 8.2 Initialize App Once, Not Per Mount — MEDIUM

Use a module-level guard to prevent double init in StrictMode:

```tsx
let initialized = false
function App() {
  if (!initialized) {
    initialized = true
    initAnalytics()
    loadFeatureFlags()
  }
  return <Router />
}
```

### 8.3 Store Event Handlers in Refs — MEDIUM

Stable callback identity without recreating closures:

```tsx
const callbackRef = useRef(onComplete)
callbackRef.current = onComplete

useEffect(() => {
  const timer = setTimeout(() => callbackRef.current(), 1000)
  return () => clearTimeout(timer)
}, []) // no deps needed
```

### 8.4 Use React 19 `use()` Hook — MEDIUM

Replace `useContext()` with `use()` for conditional context reads:

```tsx
import { use } from 'react'
const theme = use(ThemeContext)
```

### 8.5 React 19 `ref` as Regular Prop — LOW

No more `forwardRef` wrapper needed:

```tsx
// React 19+
function Input({ ref, ...props }: { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />
}
```

### 8.6 Use useActionState for Form Submissions — MEDIUM

```tsx
import { useActionState } from 'react'

const [state, submitAction, isPending] = useActionState(
  async (_prev: State, formData: FormData) => {
    const result = await createItem(formData)
    return result
  },
  initialState,
)
```

### 8.7 Use useOptimistic for Instant UI Feedback — MEDIUM

```tsx
import { useOptimistic } from 'react'

const [optimisticItems, addOptimistic] = useOptimistic(
  items,
  (state, newItem: Item) => [...state, { ...newItem, pending: true }],
)
```

---

## Quick Reference: Impact Priority

| Impact   | Rules |
|----------|-------|
| CRITICAL | 1.1, 1.2, 2.1, 5.1, 5.4 |
| HIGH     | 1.3, 1.4, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2, 5.2, 5.3, 5.5, 5.7, 6.1, 6.2, 7.1, 8.1 |
| MEDIUM   | 1.5–1.7, 2.4–2.5, 3.3–3.4, 4.3–4.5, 5.6, 5.8–5.10, 6.5, 7.2, 7.4, 7.7, 7.9, 8.2–8.4, 8.6, 8.7 |
| LOW      | 2.6–2.7, 3.5, 4.6, 5.11, 6.3–6.4, 6.6–6.9, 7.3, 7.5–7.6, 7.8, 7.10–7.12, 8.5 |

Start from CRITICAL → HIGH. LOW items are micro-optimizations.
