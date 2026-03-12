---
name: fsd-development
description: >-
  AI Platform Frontend의 FSD 변형 구조로 새 도메인을 생성하거나 레거시 코드를 마이그레이션합니다. entities,
  features, pages, widgets 작업 시, 새 도메인 추가 시, features-legacy에서 마이그레이션 시 사용합니다.
  Do NOT use for backend API development (use backend-expert).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# AI Platform FE - FSD 개발 및 마이그레이션

## 핵심 원칙

**의존성 규칙 (단방향)**:

```
shared → entities → features → widgets → pages → app/routes
```

- 하위 레이어는 상위 레이어 참조 불가
- 같은 레이어 내 형제 import 금지

**Export 규칙** (frontend-coding-conventions.mdc 준수):

```typescript
// ❌ WRONG - export * 금지!
export * from "./Button";

// ✅ CORRECT - 명시적 named export
export { Button } from "./Button";
export type { ButtonProps } from "./Button";
```

---

## 새 도메인 생성 워크플로우

### 체크리스트

```
[ ] 1. shared 레이어 설정 (Query Key & 공통 타입)
    [ ] shared/constants/query-key/{domain}.query-key.ts
    [ ] shared/types/ 에 필요한 공통 타입 확인/추가

[ ] 2. entities/{domain}/ 생성
    [ ] core/domain/{domain}.domain.ts
    [ ] core/schema/{domain}.schema.ts (필요시)
    [ ] infrastructure/api/{domain}.adapter.ts
    [ ] infrastructure/dto/{domain}.dto.ts
    [ ] infrastructure/model/{domain}.model.ts
    [ ] mapper/{domain}.mapper.ts
    [ ] types/{domain}.types.ts
    [ ] index.ts

[ ] 3. features/{domain}/ 생성 (필요시)
    [ ] service/{domain}.service.ts
    [ ] hooks/use{Action}.ts (Query Key는 shared에서 import!)
    [ ] index.ts

[ ] 4. widgets/{type}/{domain}/ 생성 (필요시)
    [ ] 도메인별 복합 UI 컴포넌트
    [ ] index.ts

[ ] 5. pages/{domain}/ 생성
    [ ] {Domain}Page.tsx
    [ ] index.ts

[ ] 6. app/routes/{domain}.route.ts 추가

[ ] 7. 테스트 및 검증
```

### Step 1: Entity 생성

**필요 파일:** domain, DTO, adapter, mapper, types, schema(선택), index.

- **단건 응답**: DTO에서 직접 정의 (`{Domain}ResponseDto`).
- **중첩 구조**: Model로 하위 타입 분리 후 DTO가 import.
- **의존성**: Model ← DTO ← Adapter; Mapper(DTO → Entity).

For detailed templates, see [references/entity_templates.md](references/entity_templates.md).

### Step 2: Feature 생성 (비즈니스 로직)

**Service:** `getProjectContext()`로 org/project 추출 → Adapter 호출 → Mapper로 Entity 변환.

**Query 훅:** `useQuery` + `{domain}QueryKeys.lists()` (shared에서 import).

**Mutation 훅:** `useMutation` + `queryClient.invalidateQueries({ queryKey: {domain}QueryKeys.all() })`.

### Step 3: Widget 생성 (복합 UI)

**원칙:** Entity만 사용, 비즈니스 로직 없음, props로 데이터/핸들러 전달, i18n 필수.

**타입:** `card/{domain}/`, `section/{domain}/`, `gauge/{domain}/`, `progress-bar/{domain}/`.

See [references/widget_templates.md](references/widget_templates.md). **참고:** `widgets/card/volume/`, `widgets/section/volume/`.

### Step 4: Page 생성

```typescript
// pages/{domain}/{Domain}Page.tsx
import { use{Domain}s } from '@/features/{domain}';
import { useTranslation } from 'react-i18next';

export const {Domain}Page = () => {
  const { t } = useTranslation('{domain}');
  const { data, isLoading } = use{Domain}s();

  if (isLoading) return <{Domain}Skeleton />;

  return (
    <div className="flex flex-col gap-6">
      <h1>{t('title')}</h1>
      {/* 컨텐츠 */}
    </div>
  );
};
```

### Step 5: Route 추가

```typescript
// app/routes/{domain}/{domain}.route.ts
import type { RouteConfig } from '@/app/providers/router-provider';
import { lazy } from 'react';

export const {Domain}Routes: RouteConfig[] = [
  {
    path: '/{domains}',
    component: lazy(() =>
      import('@/pages/{domain}').then((m) => ({
        default: m.{Domain}Page,
      })),
    ),
  },
];
```

---

## 레거시 마이그레이션 워크플로우

**체크리스트:** 분석 → Entity 추출 → Feature 추출 → Widget 추출 → Page 생성 → Route 업데이트 → 레거시 import 제거 → 테스트.

See [references/migration_guide.md](references/migration_guide.md) for mapping tables.

---

## 네이밍 규칙 Quick Reference

### 파일명

| 유형        | 패턴                  | 예시              |
| ----------- | --------------------- | ----------------- |
| 도메인 타입 | `{domain}.domain.ts`  | `user.domain.ts`  |
| DTO         | `{domain}.dto.ts`     | `user.dto.ts`     |
| 어댑터      | `{domain}.adapter.ts` | `user.adapter.ts` |
| 매퍼        | `{domain}.mapper.ts`  | `user.mapper.ts`  |
| 스키마      | `{domain}.schema.ts`  | `user.schema.ts`  |
| 서비스      | `{domain}.service.ts` | `user.service.ts` |
| 훅          | `use{Action}.ts`      | `useLogin.ts`     |
| 페이지      | `{Domain}Page.tsx`    | `UserPage.tsx`    |
| 라우트      | `{domain}.route.ts`   | `user.route.ts`   |

### 타입 네이밍

| 접미사        | 용도                                       | 예시                                               |
| ------------- | ------------------------------------------ | -------------------------------------------------- |
| `Entity`      | 프론트엔드 도메인 모델 (camelCase)         | `UserEntity`, `EndpointEntity`                     |
| `ResponseDto` | 단건 API 응답 (snake_case)                 | `UserResponseDto`, `EndpointResponseDto`           |
| `ApiModel`    | 중첩 구조의 하위 타입 (snake_case, 선택적) | `NodeGpuResourceApiModel`, `NodeResourcesApiModel` |
| `Dto`         | API 요청/응답 (Request, List, Query 등)    | `EndpointListResponseDto`, `LoginRequestDto`       |
| `Props`       | 컴포넌트 Props                             | `ButtonProps`                                      |

**Model vs DTO 사용 기준**:

- **단건 응답** → DTO에서 직접 정의 (`{Domain}ResponseDto`)
- **중첩 구조 (하위 타입 여러 개)** → Model로 분리 후 DTO가 import
- Mapper는 DTO(`{Domain}ResponseDto`)를 받아 Entity로 변환합니다.
- `Model(하위 타입, 선택적) ← DTO(단건 + 목록 + 요청) ← Adapter(DTO 사용)` ← `Mapper(DTO → Entity)`

### 컴포넌트 접미사

`Page`, `Tab`, `Modal`, `Drawer`, `Card`, `List`, `Form`, `Button`

---

## 참고 파일 및 References

- **References:** [entity_templates](references/entity_templates.md), [widget_templates](references/widget_templates.md), [migration_guide](references/migration_guide.md), [common_mistakes](references/common_mistakes.md)
- **코딩 컨벤션**: `.cursor/rules/frontend-coding-conventions.mdc` (필수 준수!)
- **i18n 가이드**: `.cursor/rules/i18n.mdc`
- **참고 Entity (단순 구조)**: `src/entities/user/` — 단건 응답은 DTO에서 직접 정의
- **참고 Entity (중첩 구조)**: `src/entities/node/` — 하위 타입이 많아 Model로 분리
- **참고 Entity (다중 소스)**: `src/entities/ai-model/` — 3종류 Model → 단일 Entity 매핑
- **참고 Feature**: `src/features/dashboard/`
- **참고 Page**: `src/pages/dashboard/`

---

## 자주 하는 실수

See [references/common_mistakes.md](references/common_mistakes.md) for details. Summary:

- Query Key: `userQueryKeys.lists()` (shared), not `["user","list"]`
- Export: `export { X }` not `export *`
- Dependencies: entities must not import features
- DTO/Entity: Entity uses camelCase; DTO uses snake_case
- Model vs DTO: Single response in DTO; nested structure in Model
- Always use Mapper for DTO → Entity; no legacy imports
