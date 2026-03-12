---
name: ecc-coding-standards
description: >-
  Universal coding standards and best practices for TypeScript, JavaScript,
  React, and Node.js — naming conventions, error handling patterns, testing
  strategies, and code organization. Use when enforcing consistent style,
  reviewing code quality, or onboarding new contributors. Do NOT use for
  Python-specific patterns (use backend-expert). Do NOT use for domain-specific
  review (use frontend-expert or backend-expert). Korean triggers: "코딩 표준", "코드 스타일".
metadata:
  author: "ecc"
  version: "1.0.0"
  category: "engineering"
origin: ECC
---
# Coding Standards & Best Practices

Universal coding standards applicable across all projects.

## When to Activate

- Starting a new project or module
- Reviewing code for quality and maintainability
- Refactoring existing code to follow conventions
- Enforcing naming, formatting, or structural consistency
- Setting up linting, formatting, or type-checking rules
- Onboarding new contributors to coding conventions

## Code Quality Principles

### 1. Readability First
- Code is read more than written
- Clear variable and function names
- Self-documenting code preferred over comments
- Consistent formatting

### 2. KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions
- Create reusable components
- Share utilities across modules
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

## TypeScript/JavaScript Standards

### Variable and Function Naming

- **Variables**: Descriptive (`marketSearchQuery`, `isUserAuthenticated`) not unclear (`q`, `flag`, `x`)
- **Functions**: Verb-noun (`fetchMarketData`, `calculateSimilarity`) not noun-only (`market`, `similarity`)

### Immutability Pattern (CRITICAL)

```typescript
// ✅ ALWAYS use spread
const updatedUser = { ...user, name: 'New Name' }
const updatedArray = [...items, newItem]
// ❌ NEVER: user.name = 'New Name' or items.push(newItem)
```

### Error Handling

```typescript
async function fetchData(url: string) {
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}
```

### Async: Use Promise.all When Independent

```typescript
const [users, markets, stats] = await Promise.all([
  fetchUsers(), fetchMarkets(), fetchStats()
])
```

### React: Typed Props and State Updates

```typescript
interface ButtonProps { children: React.ReactNode; onClick: () => void; disabled?: boolean }
export function Button({ children, onClick, disabled = false }: ButtonProps) { ... }

// State: functional update for prev-based
setCount(prev => prev + 1)
```

### React: Conditional Rendering

```typescript
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}
```

**Full patterns:** `references/typescript-react-patterns.md`

## API Design Standards

- REST: GET/POST/PUT/PATCH/DELETE on `/api/resource`, `/api/resource/:id`
- Response: `{ success, data?, error?, meta? }`
- Validate with Zod: `CreateMarketSchema.parse(body)`

**Full details:** `references/api-file-organization.md`

## File Organization

```
src/app/, components/, hooks/, lib/, types/
Button.tsx (PascalCase), useAuth.ts (camelCase), formatDate.ts
```

## Performance and Testing

- **Memoization**: `useMemo` for expensive computation, `useCallback` for callbacks
- **Lazy load**: `lazy(() => import('./HeavyChart'))` + `Suspense`
- **DB**: `select('id, name, status')` not `select('*')`
- **Tests**: AAA pattern; descriptive names (`test('returns empty when no match', ...)`)
- **Code smells**: Long functions → split; deep nesting → early returns; magic numbers → named constants

**Full details:** `references/performance-testing.md`

**Remember**: Code quality is not negotiable.
