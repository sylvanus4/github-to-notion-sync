# Common Mistakes (자주 하는 실수)

## Query Key Hardcoding

```typescript
// ❌ WRONG
queryKey: ["user", "list"],

// ✅ CORRECT
import { userQueryKeys } from "@/shared/constants/query-key";
queryKey: userQueryKeys.lists(),
```

## Wildcard Export

```typescript
// ❌ WRONG
export * from "./Button";

// ✅ CORRECT
export { Button } from "./Button";
export type { ButtonProps } from "./Button";
```

## Wrong Dependency Direction

```typescript
// ❌ WRONG - entities must not import features
import { useLogin } from "@/features/user";
```

## DTO vs Entity Confusion

```typescript
// ❌ WRONG - Entity with snake_case
export type UserEntity = { created_at: number; };

// ✅ CORRECT - Entity uses camelCase
export type UserEntity = { createdAt: number; };
```

## Model vs DTO Role Confusion

- **Single response** → Define in DTO (`{Domain}ResponseDto`)
- **Nested structure (many sub-types)** → Separate Model, DTO imports Model
- **Mapper** uses DTO (`{Domain}ResponseDto`) → Entity

## Skipping Mapper

```typescript
// ❌ WRONG
const user = await UserAdapter.getUser();
setUser(user);

// ✅ CORRECT
const dto = await UserAdapter.getUser();
const user = UserMapper.toUserEntity(dto);
```

## Legacy References

```typescript
// ❌ WRONG
import { something } from "@/features-legacy/auth";
```
