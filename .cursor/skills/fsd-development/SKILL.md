---
name: fsd-development
description: AI Platform Frontend의 FSD 변형 구조로 새 도메인을 생성하거나 레거시 코드를 마이그레이션합니다. entities, features, pages, widgets 작업 시, 새 도메인 추가 시, features-legacy에서 마이그레이션 시 사용합니다.
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

**1.1 도메인 타입** (`core/domain/{domain}.domain.ts`):

```typescript
// 프론트엔드용 타입 (camelCase)
export type {Domain}Entity = {
  id: string;
  name: string;
  createdAt: number;  // camelCase
  updatedAt: number;
};
```

**1.2 DTO** (`infrastructure/dto/{domain}.dto.ts`):

API 응답/요청 타입을 정의합니다. **단건 응답은 DTO에서 직접 정의**합니다.

```typescript
// ============================================================================
// Response DTOs
// ============================================================================

/** 단건 응답 - API 엔티티 1건의 형태 (snake_case) */
export type {Domain}ResponseDto = {
  id: string;
  name: string;
  status: string;
  owner_id: string;
  created_at: number;  // snake_case (API 원본)
  updated_at: number;
};

/** 목록 응답 - 단건 ResponseDto를 페이지네이션으로 래핑 */
export type {Domain}ListResponseDto = {
  items: {Domain}ResponseDto[];
  total: number;
  page: number;
  page_size: number;
};

/** 액션 응답 - 단건과 다른 구조 */
export type {Domain}ActionResponseDto = {
  id?: string;
  message?: string;
  status?: string;
};

// ============================================================================
// Request DTOs (요청 파라미터)
// ============================================================================

/** 생성 요청 */
export type Create{Domain}RequestDto = {
  name: string;
  description?: string;
};

/** 목록 조회 쿼리 */
export type Get{Domain}ListQueryDto = {
  status?: string;
  q?: string;
  page?: number;
  page_size?: number;
  sort?: string;
  order?: 'asc' | 'desc';
};
```

**참고 코드**: `entities/template/infrastructure/dto/template.dto.ts`

**1.3 API 모델** (`infrastructure/model/{domain}.model.ts`) — **중첩 구조일 때만 사용**:

**하위 타입이 여러 개로 중첩된 복합 구조**일 때만 Model로 분리합니다. 단순 단건 응답은 DTO에서 직접 정의하고, Model은 사용하지 않습니다.

```typescript
// 예: node처럼 하위 타입이 여러 개인 경우 Model로 분리
export type NodeGpuResourceApiModel = {
  key: string;
  total: number;
  requests: number;
  available: number;
};

export type NodeResourcesApiModel = {
  cpu_m: number;
  memory_mi: number;
  disk_mi: number;
  gpus: NodeGpuResourceApiModel[]; // 하위 모델 참조
};

export type NodeConditionsApiModel = {
  NetworkUnavailable: string;
  MemoryPressure: string;
  DiskPressure: string;
  Ready: string;
};

// 최상위 모델 (하위 모델들을 조합)
export type NodeResourceInfoApiModel = {
  name: string;
  labels: Record<string, string>;
  conditions: NodeConditionsApiModel;
  allocatable: NodeResourcesApiModel;
  requests: NodeResourcesApiModel;
  // ...
};
```

그 후 DTO에서 Model을 import해서 래퍼 구성:

```typescript
// infrastructure/dto/{domain}.dto.ts
import type { NodeResourceInfoApiModel } from "../model";

export type NodeResourcesListResponseDto = {
  nodes?: NodeResourceInfoApiModel[];
};
```

**참고 코드**: `entities/node/infrastructure/model/node.model.ts`

**언제 Model을 사용하나?**
| 상황 | Model | DTO |
| --- | --- | --- |
| 단순 단건 응답 | ❌ | ✅ `{Domain}ResponseDto` |
| 목록 래퍼 | ❌ | ✅ `{Domain}ListResponseDto` |
| Request params | ❌ | ✅ `Create{Domain}RequestDto` |
| 중첩/복합 구조 (하위 타입 여러 개) | ✅ 하위 타입 분리 | DTO가 Model import |

**의존성 방향**: `Model(독립, 하위 타입) ← DTO(Model import 또는 직접 정의) ← Adapter(DTO 사용)`

**1.4 어댑터** (`infrastructure/api/{domain}.adapter.ts`):

HTTP 통신 레이어입니다. DTO 타입을 사용합니다.

```typescript
import { httpClient } from '@/shared/libs/api';
import type {
  {Domain}ResponseDto,
  {Domain}ListResponseDto,
  Create{Domain}RequestDto,
  Get{Domain}ListQueryDto,
} from '../dto';

export const {Domain}Adapter = {
  /** 목록 조회 */
  getList: async (
    orgId: string,
    projectId: string,
    params?: Get{Domain}ListQueryDto,
  ): Promise<{Domain}ListResponseDto> => {
    const response = await httpClient.get<{Domain}ListResponseDto>(
      `/api/v1/orgs/${orgId}/projects/${projectId}/{domains}`,
      { params },
    );
    return response.data;
  },

  /** 단건 조회 */
  getById: async (id: string): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.get<{Domain}ResponseDto>(
      `/api/v1/{domains}/${id}`,
    );
    return response.data;
  },

  /** 생성 */
  create: async (data: Create{Domain}RequestDto): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.post<{Domain}ResponseDto>(
      '/api/v1/{domains}',
      data,
    );
    return response.data;
  },

  /** 삭제 */
  delete: async (id: string): Promise<void> => {
    await httpClient.delete(`/api/v1/{domains}/${id}`);
  },
};
```

**1.5 매퍼** (`mapper/{domain}.mapper.ts`):

DTO를 직접 import해서 Entity로 변환합니다.

```typescript
import type { {Domain}Entity } from '../core';
import type { {Domain}ResponseDto } from '../infrastructure/dto';

export const {Domain}Mapper = {
  toEntity: (dto: {Domain}ResponseDto): {Domain}Entity => ({
    id: dto.id,
    name: dto.name,
    createdAt: dto.created_at,  // snake → camel
    updatedAt: dto.updated_at,
  }),

  toEntityList: (dtos: {Domain}ResponseDto[]): {Domain}Entity[] =>
    dtos.map({Domain}Mapper.toEntity),
};
```

**1.6 타입** (`types/{domain}.types.ts`):

```typescript
export type {Domain}Status = 'ACTIVE' | 'INACTIVE' | 'ERROR';

export type {Domain}Type = 'TYPE_A' | 'TYPE_B';
```

**1.7 스키마** (`core/schema/{domain}.schema.ts`) - 필요시:

```typescript
import { z } from 'zod';

export const create{Domain}Schema = (t: (key: string) => string) =>
  z.object({
    name: z
      .string()
      .min(1, t('{domain}.validation.name.required'))
      .max(100, t('{domain}.validation.name.maxLength')),
  });

export type Create{Domain}Credentials = z.infer<ReturnType<typeof create{Domain}Schema>>;
```

**1.8 Index** (`index.ts`):

```typescript
// Public API - 명시적 named export (export * 금지!)

// Domain Entity (camelCase - 프론트엔드 사용)
export type { {Domain}Entity } from './core';

// Infrastructure
export { {Domain}Adapter } from './infrastructure';
export type {
  {Domain}ResponseDto,                                              // DTO (단건 응답)
  {Domain}ListResponseDto,                                          // DTO (목록 래퍼)
  Create{Domain}RequestDto,                                         // DTO (요청)
  Get{Domain}ListQueryDto,                                          // DTO (쿼리 파라미터)
} from './infrastructure';

// Mapper & Types
export { {Domain}Mapper } from './mapper';
export type { {Domain}Status, {Domain}Type } from './types';
```

### Step 2: Feature 생성 (비즈니스 로직)

**2.1 서비스** (`service/{domain}.service.ts`):

```typescript
import { {Domain}Adapter } from '@/entities/{domain}';
import { getProjectContext, isValidContext } from '@/features/dashboard/helper';

export const {Domain}Service = {
  async getList(): Promise<{Domain}Entity[]> {
    const ctx = getProjectContext();
    if (!isValidContext(ctx)) return [];

    const { organizationId, projectId } = ctx;
    const data = await {Domain}Adapter.getList(organizationId, projectId);
    return {Domain}Mapper.toEntityList(data);
  },
};
```

**2.2 훅** (`hooks/use{Domain}s.ts`):

```typescript
import { useQuery } from '@tanstack/react-query';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {domain}Service } from '../service';

export const use{Domain}s = () => {
  return useQuery({
    queryKey: {domain}QueryKeys.lists(),  // ✅ shared에서 관리하는 Query Key 사용
    queryFn: () => {domain}Service.getList(),
  });
};
```

**2.3 뮤테이션 훅** (`hooks/useCreate{Domain}.ts`):

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {Domain}Adapter } from '@/entities/{domain}';

export const useCreate{Domain} = (options?: { onSuccess?: () => void }) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: {Domain}Adapter.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: {domain}QueryKeys.all() });  // ✅ Query Key 팩토리 사용
      options?.onSuccess?.();
    },
  });
};
```

### Step 3: Widget 생성 (복합 UI)

Widget은 **여러 Entity/Feature를 조합한 복합 UI 컴포넌트**입니다. 비즈니스 로직 없이 props로 데이터와 핸들러를 전달받습니다.

**디렉토리 구조**:

```
widgets/
├── card/{domain}/              ← 단일 리소스 카드
├── section/{domain}/           ← 리스트 + 필터 + 빈/에러 상태
├── gauge/{domain}/             ← 사용량 표시기
└── progress-bar/{domain}/      ← 프로그레스바
```

**Widget 원칙**:

- **Entity 타입만 사용** (DTO 직접 사용 금지)
- **비즈니스 로직 없음** (props로 데이터/핸들러 전달)
- **도메인별 하위 폴더로 구분** (`widgets/{type}/{domain}/`)
- i18n 필수 적용

**3.1 Card Widget** (`widgets/card/{domain}/{Domain}Card.tsx`):

```typescript
import type { {Domain}Entity } from '@/entities/{domain}';

interface {Domain}CardProps {
  {domain}: {Domain}Entity;              // ✅ Entity 타입 사용
  onEdit?: ({domain}: {Domain}Entity) => void;    // 핸들러는 props로 전달
  onDelete?: ({domain}: {Domain}Entity) => void;
}

export function {Domain}Card({ {domain}, onEdit, onDelete }: {Domain}CardProps) {
  const { t } = useTranslation('{domain}');
  return (
    <Card>
      <h3>{entity.name}</h3>
      {/* UI 렌더링만, 비즈니스 로직 없음 */}
      <Button onClick={() => onEdit?.({domain})}>{t('actions.edit')}</Button>
    </Card>
  );
}
```

**3.2 Section Widget** (`widgets/section/{domain}/{Domain}Section.tsx`):

리스트 + 필터 + 빈 상태 + 에러 상태를 포함하는 복합 위젯입니다.

```typescript
import type { {Domain}Entity } from '@/entities/{domain}';
import { {Domain}Card } from '@/widgets/card/{domain}';

interface {Domain}SectionProps {
  items: {Domain}Entity[];
  isLoading: boolean;
  error: Error | null;
  onRefresh: () => void;
  onCreate: () => void;
  onEdit: (item: {Domain}Entity) => void;
  onDelete: (item: {Domain}Entity) => void;
}

export function {Domain}Section({
  items, isLoading, error, onRefresh, onCreate, onEdit, onDelete,
}: {Domain}SectionProps) {
  const { t } = useTranslation('{domain}');

  if (isLoading && items.length === 0) return <LoadingSpinner />;
  if (error) return <ErrorState message={error.message} onRetry={onRefresh} />;

  return (
    <div>
      {/* 필터/검색 영역 */}
      <FilterSearchInput ... />

      {/* 카드 그리드 또는 빈 상태 */}
      {filteredItems.length === 0 ? (
        <EmptyState onCreate={onCreate} />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredItems.map((item) => (
            <{Domain}Card key={item.id} {domain}={item} onEdit={onEdit} onDelete={onDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
```

**3.3 Index** (`widgets/{type}/{domain}/index.ts`):

```typescript
export { {Domain}Card } from './{Domain}Card';
```

**참고 코드**:

- **Card**: `src/widgets/card/volume/VolumeCard.tsx`
- **Section**: `src/widgets/section/volume/VolumeSection.tsx`
- **Gauge**: `src/widgets/gauge/volume/QuotaGauge.tsx`
- **Progress Bar**: `src/widgets/progress-bar/volume/UsageProgressBar.tsx`

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

### 마이그레이션 체크리스트

```
[ ] 1. 분석: features-legacy/{domain}/ 구조 파악
[ ] 2. Entity 추출: API, 타입, 모델 분리
[ ] 3. Feature 추출: 비즈니스 로직 분리
[ ] 4. Widget 추출: 복합 UI 분리
[ ] 5. Page 생성: 페이지 컴포넌트 분리
[ ] 6. Route 업데이트: 새 경로로 변경
[ ] 7. 레거시 import 제거 확인
[ ] 8. 테스트
```

### Step 1: 레거시 코드 분석

```bash
# 구조 확인
ls -la src/features-legacy/{domain}/

# API 파일 확인
cat src/features-legacy/{domain}/api/*.ts

# 컴포넌트 확인
cat src/features-legacy/{domain}/components/*.tsx
```

**확인 사항**:

- API 호출 패턴 (axios/httpClient)
- 타입 정의 위치
- 비즈니스 로직 위치
- UI 컴포넌트 구조

### Step 2: Entity 추출

레거시에서 다음을 분리:

| 레거시 위치       | 새 위치                                 |
| ----------------- | --------------------------------------- |
| `api/*.api.ts`    | `entities/{domain}/infrastructure/api/` |
| `api/*.models.ts` | `entities/{domain}/infrastructure/dto/` |
| 타입 정의         | `entities/{domain}/types/`              |
| 도메인 로직       | `entities/{domain}/core/domain/`        |

### Step 3: Feature 추출

| 레거시 위치        | 새 위치                      |
| ------------------ | ---------------------------- |
| `api/*.queries.ts` | `features/{domain}/hooks/`   |
| 비즈니스 로직      | `features/{domain}/service/` |
| 유틸 함수          | `features/{domain}/helper/`  |

### Step 4: Widget 추출

복합 UI 컴포넌트를 widgets/로 이동:

- 여러 컴포넌트 조합
- 레이아웃 관련 복합체
- 재사용 가능한 UI 블록

### Step 5: Route 업데이트

```typescript
// 변경 전 (레거시 참조)
component: lazy(() => import('@/features-legacy/{domain}').then(...))

// 변경 후 (새 구조 참조)
component: lazy(() => import('@/pages/{domain}').then(...))
```

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

## 참고 파일

- **코딩 컨벤션**: `.cursor/rules/frontend-coding-conventions.mdc` (필수 준수!)
- **i18n 가이드**: `.cursor/rules/i18n.mdc`
- **참고 Entity (단순 구조)**: `src/entities/user/` — 단건 응답은 DTO에서 직접 정의
- **참고 Entity (중첩 구조)**: `src/entities/node/` — 하위 타입이 많아 Model로 분리
- **참고 Entity (다중 소스)**: `src/entities/ai-model/` — 3종류 Model → 단일 Entity 매핑
- **참고 Feature**: `src/features/dashboard/`
- **참고 Page**: `src/pages/dashboard/`

---

## 자주 하는 실수

### ❌ Query Key 하드코딩

```typescript
// features 훅에서 Query Key 하드코딩 - 금지!
export const useUsers = () => {
  return useQuery({
    queryKey: ["user", "list"], // ❌ 하드코딩 금지!
    queryFn: () => UserService.getList(),
  });
};

// 올바른 방법 - shared에서 Query Key import
import { userQueryKeys } from "@/shared/constants/query-key";

export const useUsers = () => {
  return useQuery({
    queryKey: userQueryKeys.lists(), // ✅ 팩토리 함수 사용
    queryFn: () => UserService.getList(),
  });
};
```

### ❌ Wildcard Export 사용

```typescript
// index.ts에서 export * 사용 - 금지!
export * from "./Button"; // ❌

// 올바른 방법
export { Button } from "./Button"; // ✅
export type { ButtonProps } from "./Button"; // ✅
```

### ❌ 잘못된 의존성

```typescript
// entities에서 features 참조 - 금지!
import { useLogin } from "@/features/user";
```

### ❌ DTO와 Entity 혼용

```typescript
// Entity에서 snake_case 사용 - 금지!
export type UserEntity = {
  created_at: number; // ❌ camelCase 사용해야 함
};
```

### ❌ Model과 DTO 역할 혼동

```typescript
// ❌ WRONG - 단순 단건 응답을 Model로 분리 (불필요한 분리)
// infrastructure/model/{domain}.model.ts
export type {Domain}ApiModel = {
  id: string;
  name: string;
  created_at: number;
};

// ✅ CORRECT - 단건 응답은 DTO에서 직접 정의
// infrastructure/dto/{domain}.dto.ts
export type {Domain}ResponseDto = {
  id: string;
  name: string;
  created_at: number;
};
export type {Domain}ListResponseDto = {
  items: {Domain}ResponseDto[];  // ✅ DTO가 DTO를 조합 (단순 구조)
};

// ✅ CORRECT - 중첩 구조일 때만 Model 분리
// infrastructure/model/node.model.ts (복합 구조 예시)
export type NodeGpuResourceApiModel = { ... };
export type NodeResourcesApiModel = { gpus: NodeGpuResourceApiModel[]; ... };
export type NodeConditionsApiModel = { ... };
export type NodeResourceInfoApiModel = {
  conditions: NodeConditionsApiModel;
  allocatable: NodeResourcesApiModel;  // ✅ 하위 타입 조합
};

// infrastructure/dto/node.dto.ts
import type { NodeResourceInfoApiModel } from '../model';
export type NodeResourcesListResponseDto = {
  nodes?: NodeResourceInfoApiModel[];  // ✅ 복합 Model을 래핑
};
```

### ❌ 매퍼 없이 직접 사용

```typescript
// API 응답을 직접 사용 - 금지!
const user = await UserAdapter.getUser();
setUser(user); // ❌ 매퍼로 변환 필요

// 올바른 방법
const dto = await UserAdapter.getUser();
const user = UserMapper.toUserEntity(dto); // ✅
```

### ❌ 레거시 참조

```typescript
// 새 코드에서 레거시 참조 - 금지!
import { something } from "@/features-legacy/auth"; // ❌
```
