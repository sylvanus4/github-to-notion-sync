# Performance and Testing Standards

## Memoization

```typescript
import { useMemo, useCallback } from 'react'

const sortedMarkets = useMemo(() => markets.sort((a, b) => b.volume - a.volume), [markets])
const handleSearch = useCallback((query: string) => setSearchQuery(query), [])
```

## Lazy Loading

```typescript
const HeavyChart = lazy(() => import('./HeavyChart'))
<Suspense fallback={<Spinner />}><HeavyChart /></Suspense>
```

## Database Queries

```typescript
// ✅ GOOD: Select only needed columns
const { data } = await supabase.from('markets').select('id, name, status').limit(10)

// ❌ BAD: Select everything
const { data } = await supabase.from('markets').select('*')
```

## Test Structure (AAA Pattern)

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]
  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)
  // Assert
  expect(similarity).toBe(0)
})
```

## Test Naming

```typescript
// ✅ GOOD: Descriptive
test('returns empty array when no markets match query', () => { })
test('throws error when OpenAI API key is missing', () => { })

// ❌ BAD: Vague
test('works', () => { })
test('test search', () => { })
```

## Code Smell: Long Functions and Deep Nesting

```typescript
// ✅ GOOD: Split into smaller functions
function processMarketData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}

// ✅ GOOD: Early returns
if (!user) return
if (!user.isAdmin) return
if (!market) return
// Do something
```

## Code Smell: Magic Numbers

```typescript
// ✅ GOOD: Named constants
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500
```
