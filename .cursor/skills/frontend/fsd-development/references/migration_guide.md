# Legacy Migration Guide

## Checklist

```
[ ] 1. Analyze features-legacy/{domain}/ structure
[ ] 2. Extract Entity: API, types, models
[ ] 3. Extract Feature: business logic
[ ] 4. Extract Widget: composite UI
[ ] 5. Create Page
[ ] 6. Update Route
[ ] 7. Remove legacy imports
[ ] 8. Test
```

## Entity Extraction Mapping

| Legacy Location       | New Location                                |
| --------------------- | ------------------------------------------- |
| `api/*.api.ts`        | `entities/{domain}/infrastructure/api/`    |
| `api/*.models.ts`     | `entities/{domain}/infrastructure/dto/`     |
| Type definitions      | `entities/{domain}/types/`                  |
| Domain logic          | `entities/{domain}/core/domain/`           |

## Feature Extraction Mapping

| Legacy Location       | New Location                      |
| --------------------- | --------------------------------- |
| `api/*.queries.ts`    | `features/{domain}/hooks/`        |
| Business logic        | `features/{domain}/service/`      |
| Utils                 | `features/{domain}/helper/`       |

## Route Update

```typescript
// Before (legacy)
component: lazy(() => import('@/features-legacy/{domain}').then(...))

// After (new)
component: lazy(() => import('@/pages/{domain}').then(...))
```
