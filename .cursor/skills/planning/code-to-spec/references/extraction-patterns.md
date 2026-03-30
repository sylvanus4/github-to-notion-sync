# Code extraction patterns (planning-oriented)

Use these patterns when scanning implementations for **code-to-spec** and **code-spec-comparator**. Output language for the final document is Korean per skill rules; this reference is English for maintainability.

## State extraction

### React / Next.js

| Pattern | Extract |
|---------|---------|
| `useState`, `useReducer` | Local state, transitions via setters/dispatch |
| `useEffect` deps | Coupling between state and side effects |
| `Context.Provider` | Shared state scope |
| `useQuery` / `useSWR` | Server state, loading/error/success |
| `useSelector` / `useRecoilState` / `zustand` | Global store state |

### Vue / Nuxt

| Pattern | Extract |
|---------|---------|
| `ref`, `reactive` | Component state |
| `computed` | Derived state |
| `watch` | Reactions to state |
| Pinia / Vuex / `defineStore` | Global state |
| `useAsyncData` (Nuxt) | Server/async state |

### Backend / generic

| Pattern | Extract |
|---------|---------|
| `enum`, string unions | Named states |
| `status` / `state` columns | Entity lifecycle |
| State-machine libs (e.g. XState) | Formal transitions |
| `switch` on status | Transition branches |

## Exception and edge-path extraction

| Pattern | Extract |
|---------|---------|
| `try` / `catch` | Error types, recovery |
| `if (!x) throw` / early return | Preconditions, validation |
| `switch` `default` | Fallback / unhandled enum |
| HTTP 4xx/5xx handling | API error scenarios |
| `.catch` / `onError` | Async failure |
| `ErrorBoundary` | UI failure containment |
| Zod / Yup / Joi / Pydantic | Validation rules |

## Business logic extraction

| Pattern | Planning meaning |
|---------|------------------|
| Pricing/totals functions | Billing rules |
| Role/permission checks | Access policy |
| Feature flags | Rollout / experiment |
| Date/time logic | Validity windows, schedules |
| Limits/quotas | Service constraints |
| Sort/filter | UX rules |

## UI flow extraction (frontend)

| Pattern | Planning meaning |
|---------|------------------|
| Router config | Screen map, navigation |
| Conditional render (loading/error/empty/success) | Screen states |
| Modal/dialog/toast | Interrupt flows |
| Form submit → API → result | User journey |
| Redirect / navigate | Transition rules |

## Policy-oriented extraction

| Pattern | Planning meaning |
|---------|------------------|
| `user.role`, session expiry | Auth/session policy |
| min/max/regex validation | Input policy |
| Middleware (auth, rate limit) | Gateway policy |
| Env-based toggles | Configuration policy |
| Hardcoded literals | Possible business rules (tag `[확인 필요]` if unclear) |

## When to tag `[확인 필요]`

- Magic numbers/strings without domain comment
- Complex branches without comments
- TODO / FIXME / HACK
- Dead or flag-disabled paths
- External API calls where product intent is opaque
