# FSD 개발 템플릿 모음

복사해서 사용할 수 있는 템플릿 파일들입니다.

---

## Shared 템플릿 (Query Key & 공통 타입)

### shared/types/filter.type.ts (공통 필터 타입)

```typescript
/**
 * 공통 목록 조회 필터
 * - 다른 레이어에서 Pick, Omit으로 확장하여 사용
 */
export type BaseListFilters = {
  page?: number;
  pageSize?: number;
  search?: string;
  sortBy?: string;
  sortOrder?: "asc" | "desc";
};

export type StatusFilter = {
  status?: string;
};

export type DateRangeFilter = {
  startDate?: string;
  endDate?: string;
};
```

### shared/types/index.ts

```typescript
// ⚠️ 명시적 named export 필수 (export * 금지!)
export type {
  BaseListFilters,
  StatusFilter,
  DateRangeFilter,
} from "./filter.type";
```

### shared/constants/query-key/{domain}.query-key.ts

```typescript
import type { BaseListFilters, StatusFilter } from '@/shared/types';

/**
 * {Domain} Query Key 필터 타입
 * - 공통 타입 조합으로 정의
 */
type {Domain}ListFilters = BaseListFilters & StatusFilter;

/**
 * {Domain} Query Key Factory
 * - 모든 Query Key는 여기서 중앙 관리
 * - features 훅에서 import해서 사용
 */
export const {domain}QueryKeys = {
  all: () => ['{domain}'] as const,
  lists: () => [...{domain}QueryKeys.all(), 'list'] as const,
  list: (filters: {Domain}ListFilters) => [...{domain}QueryKeys.lists(), filters] as const,
  details: () => [...{domain}QueryKeys.all(), 'detail'] as const,
  detail: (id: string) => [...{domain}QueryKeys.details(), id] as const,
};
```

### shared/constants/query-key/index.ts

```typescript
// ⚠️ 명시적 named export 필수 (export * 금지!)
export { userQueryKeys } from './user.query-key';
export { workloadQueryKeys } from './workload.query-key';
export { {domain}QueryKeys } from './{domain}.query-key';
```

---

## Entity 템플릿

### index.ts (Entity Root)

```typescript
// entities/{domain}/index.ts
// ⚠️ 명시적 named export 필수 (export * 금지!)

// Core
export { {Domain}Entity } from './core';
export type { Create{Domain}Input } from './core';

// Infrastructure
export { {Domain}Adapter } from './infrastructure';
export type {
  Create{Domain}RequestDto,
  Update{Domain}RequestDto,
  {Domain}ResponseDto,
  {Domain}ListResponseDto,
  {Domain}ApiModel,
} from './infrastructure';

// Mapper
export { {Domain}Mapper } from './mapper';

// Types
export type { {Domain}Status, {Domain}Type, {Domain}FilterOptions } from './types';
```

### core/index.ts

```typescript
// ⚠️ 명시적 named export 필수 (export * 금지!)
export { {Domain}Entity } from './domain';
export { create{Domain}Schema, type Create{Domain}Input } from './schema';
```

### core/domain/{domain}.domain.ts

```typescript
import type { {Domain}Status, {Domain}Type } from '../../types';

/**
 * {Domain} Entity - 프론트엔드 도메인 모델
 * - camelCase 네이밍
 * - 비즈니스 로직에서 사용
 */
export type {Domain}Entity = {
  id: string;
  name: string;
  description?: string;
  status: {Domain}Status;
  type: {Domain}Type;
  createdAt: number;
  updatedAt: number;
};
```

### core/schema/{domain}.schema.ts

```typescript
import { z } from 'zod';

type TFunction = (key: string) => string;

/**
 * {Domain} 생성 스키마 (i18n 지원)
 */
export const create{Domain}Schema = (t: TFunction) =>
  z.object({
    name: z
      .string()
      .min(1, t('{domain}.validation.name.required'))
      .max(100, t('{domain}.validation.name.maxLength')),
    description: z
      .string()
      .max(500, t('{domain}.validation.description.maxLength'))
      .optional(),
    type: z.enum(['TYPE_A', 'TYPE_B'], {
      errorMap: () => ({ message: t('{domain}.validation.type.required') }),
    }),
  });

export type Create{Domain}Input = z.infer<ReturnType<typeof create{Domain}Schema>>;
```

### infrastructure/index.ts

```typescript
// ⚠️ 명시적 named export 필수 (export * 금지!)
export { {Domain}Adapter } from './api';
export type {
  Create{Domain}RequestDto,
  Update{Domain}RequestDto,
  {Domain}ResponseDto,
  {Domain}ListResponseDto,
} from './dto';
export type { {Domain}ApiModel } from './model';
```

### infrastructure/api/{domain}.adapter.ts

```typescript
import { httpClient } from '@/shared/libs/api';
import type {
  {Domain}ListResponseDto,
  {Domain}ResponseDto,
  Create{Domain}RequestDto,
  Update{Domain}RequestDto,
} from '../dto';

const BASE_URL = '/api/v1';

/**
 * {Domain} API Adapter
 * - HTTP 호출 담당
 * - DTO 타입 사용
 */
export const {Domain}Adapter = {
  /**
   * 목록 조회
   */
  getList: async (
    organizationId: string,
    projectId: string,
  ): Promise<{Domain}ListResponseDto> => {
    const response = await httpClient.get<{Domain}ListResponseDto>(
      `${BASE_URL}/orgs/${organizationId}/projects/${projectId}/{domains}`,
    );
    return response.data;
  },

  /**
   * 단건 조회
   */
  getById: async (id: string): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.get<{Domain}ResponseDto>(
      `${BASE_URL}/{domains}/${id}`,
    );
    return response.data;
  },

  /**
   * 생성
   */
  create: async (
    organizationId: string,
    projectId: string,
    data: Create{Domain}RequestDto,
  ): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.post<{Domain}ResponseDto>(
      `${BASE_URL}/orgs/${organizationId}/projects/${projectId}/{domains}`,
      data,
    );
    return response.data;
  },

  /**
   * 수정
   */
  update: async (
    id: string,
    data: Update{Domain}RequestDto,
  ): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.put<{Domain}ResponseDto>(
      `${BASE_URL}/{domains}/${id}`,
      data,
    );
    return response.data;
  },

  /**
   * 삭제
   */
  delete: async (id: string): Promise<void> => {
    await httpClient.delete(`${BASE_URL}/{domains}/${id}`);
  },

  /**
   * 카운트 조회
   */
  getCount: async (
    organizationId: string,
    projectId: string,
  ): Promise<number> => {
    const response = await httpClient.get<{ count: number }>(
      `${BASE_URL}/orgs/${organizationId}/projects/${projectId}/{domains}/count`,
    );
    return response.data.count;
  },
};
```

### infrastructure/dto/{domain}.dto.ts

```typescript
import type { {Domain}ApiModel } from '../model';

/**
 * Request DTOs - 서버로 보내는 데이터
 * - snake_case 사용
 */
export type Create{Domain}RequestDto = {
  name: string;
  description?: string;
  type: string;
};

export type Update{Domain}RequestDto = Partial<Create{Domain}RequestDto>;

/**
 * Response DTOs - 서버에서 받는 데이터
 * - snake_case 유지
 */
export type {Domain}ResponseDto = {Domain}ApiModel;

export type {Domain}ListResponseDto = {Domain}ApiModel[];
```

### infrastructure/model/{domain}.model.ts

```typescript
/**
 * {Domain} API Model - 서버 응답 형태
 * - snake_case 유지 (서버 응답 그대로)
 */
export type {Domain}ApiModel = {
  id: string;
  name: string;
  description?: string;
  status: string;
  type: string;
  created_at: number;
  updated_at: number;
};
```

### mapper/{domain}.mapper.ts

```typescript
import { toUpperCaseEnum } from '@/shared/utils';
import type { {Domain}Entity } from '../core';
import type { {Domain}ApiModel } from '../infrastructure/model';
import type { {Domain}Status, {Domain}Type } from '../types';

/**
 * {Domain} Mapper
 * - API Model → Entity 변환
 * - snake_case → camelCase 변환
 * - Enum 변환
 */
export const {Domain}Mapper = {
  /**
   * 단건 변환
   */
  toEntity: (model: {Domain}ApiModel): {Domain}Entity => ({
    id: model.id,
    name: model.name,
    description: model.description,
    status: toUpperCaseEnum<{Domain}Status>(model.status),
    type: toUpperCaseEnum<{Domain}Type>(model.type),
    createdAt: model.created_at,
    updatedAt: model.updated_at,
  }),

  /**
   * 목록 변환
   */
  toEntityList: (models: {Domain}ApiModel[]): {Domain}Entity[] =>
    models.map({Domain}Mapper.toEntity),
};
```

### types/{domain}.types.ts

```typescript
import type { BaseListFilters } from '@/shared/types';

/**
 * {Domain} 상태 Enum
 */
export type {Domain}Status = 'ACTIVE' | 'INACTIVE' | 'ERROR' | 'PENDING';

/**
 * {Domain} 타입 Enum
 */
export type {Domain}Type = 'TYPE_A' | 'TYPE_B' | 'TYPE_C';

/**
 * {Domain} 필터 옵션
 * - shared의 공통 타입을 Pick/Omit으로 확장
 */
export type {Domain}FilterOptions = Pick<BaseListFilters, 'search' | 'page' | 'pageSize'> & {
  status?: {Domain}Status;
  type?: {Domain}Type;
};
```

---

## Feature 템플릿

### index.ts (Feature Root)

```typescript
// features/{domain}/index.ts
// ⚠️ 명시적 named export 필수 (export * 금지!)

export { use{Domain}s, use{Domain} } from './hooks';
export { useCreate{Domain} } from './hooks';
export { useDelete{Domain} } from './hooks';
export { {Domain}Service } from './service';
```

### service/{domain}.service.ts

```typescript
import {
  {Domain}Adapter,
  {Domain}Mapper,
  type {Domain}Entity,
} from '@/entities/{domain}';
import { getProjectContext, isValidContext } from '@/shared/utils';

/**
 * {Domain} Service
 * - 비즈니스 로직 처리
 * - 여러 Entity 조합
 */
export const {Domain}Service = {
  /**
   * 목록 조회
   */
  async getList(): Promise<{Domain}Entity[]> {
    const ctx = getProjectContext();
    if (!isValidContext(ctx)) return [];

    const { organizationId, projectId } = ctx;
    const data = await {Domain}Adapter.getList(organizationId, projectId);
    return {Domain}Mapper.toEntityList(data);
  },

  /**
   * 단건 조회
   */
  async getById(id: string): Promise<{Domain}Entity | null> {
    try {
      const data = await {Domain}Adapter.getById(id);
      return {Domain}Mapper.toEntity(data);
    } catch {
      return null;
    }
  },
};
```

### hooks/use{Domain}s.ts (Query Hook)

```typescript
import { useQuery } from '@tanstack/react-query';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {Domain}Service } from '../service';

/**
 * {Domain} 목록 조회 훅
 * ⚠️ Query Key는 shared에서 import해서 사용!
 */
export const use{Domain}s = () => {
  return useQuery({
    queryKey: {domain}QueryKeys.lists(),  // ✅ shared에서 관리하는 Query Key
    queryFn: () => {Domain}Service.getList(),
    staleTime: 1000 * 60 * 5, // 5분
  });
};

/**
 * {Domain} 단건 조회 훅
 */
export const use{Domain} = (id: string | undefined) => {
  return useQuery({
    queryKey: {domain}QueryKeys.detail(id!),  // ✅ shared에서 관리하는 Query Key
    queryFn: () => {Domain}Service.getById(id!),
    enabled: Boolean(id),
  });
};
```

### hooks/useCreate{Domain}.ts (Mutation Hook)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {Domain}Adapter } from '@/entities/{domain}';
import type { Create{Domain}RequestDto } from '@/entities/{domain}';

type UseCreate{Domain}Options = {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
};

/**
 * {Domain} 생성 훅
 * ⚠️ Query Key는 shared에서 import해서 사용!
 */
export const useCreate{Domain} = (options?: UseCreate{Domain}Options) => {
  const { t } = useTranslation('{domain}');
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: Create{Domain}RequestDto) => {
      const ctx = getProjectContext();
      if (!isValidContext(ctx)) throw new Error('Invalid context');

      return {Domain}Adapter.create(ctx.organizationId, ctx.projectId, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: {domain}QueryKeys.all() });  // ✅ Query Key 팩토리 사용
      options?.onSuccess?.();
    },
    onError: (error: Error) => {
      console.error('{Domain} creation failed:', error);
      options?.onError?.(error);
    },
  });
};
```

### hooks/useDelete{Domain}.ts (Delete Mutation)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {Domain}Adapter } from '@/entities/{domain}';

type UseDelete{Domain}Options = {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
};

/**
 * {Domain} 삭제 훅
 * ⚠️ Query Key는 shared에서 import해서 사용!
 */
export const useDelete{Domain} = (options?: UseDelete{Domain}Options) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: {Domain}Adapter.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: {domain}QueryKeys.all() });  // ✅ Query Key 팩토리 사용
      options?.onSuccess?.();
    },
    onError: (error: Error) => {
      console.error('{Domain} deletion failed:', error);
      options?.onError?.(error);
    },
  });
};
```

### hooks/index.ts

```typescript
// ⚠️ 명시적 named export 필수 (export * 금지!)
export { use{Domain}s, use{Domain} } from './use{Domain}s';
export { useCreate{Domain} } from './useCreate{Domain}';
export { useDelete{Domain} } from './useDelete{Domain}';
```

---

## Page 템플릿

### {Domain}Page.tsx

```typescript
import { use{Domain}s } from '@/features/{domain}';
import { Button, Skeleton } from '@thakicloud/shared';
import React from 'react';
import { useTranslation } from 'react-i18next';

// ============================================================================
// Skeleton
// ============================================================================

const {Domain}Skeleton = () => (
  <div className="flex flex-col gap-6">
    <div className="flex items-center justify-between">
      <Skeleton className="h-6 w-32" />
      <Skeleton className="h-9 w-24" />
    </div>
    <Skeleton className="h-[400px] rounded-lg" />
  </div>
);

// ============================================================================
// Page Component
// ============================================================================

export const {Domain}Page = () => {
  const { t } = useTranslation('{domain}');
  const { data, isLoading, refetch } = use{Domain}s();

  if (isLoading) {
    return <{Domain}Skeleton />;
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold text-text-default">
          {t('title')}
        </h1>
        <div className="flex gap-2">
          <Button
            onClick={() => refetch()}
            variant="secondary"
            appearance="outline"
            size="md"
          >
            {t('actions.refresh')}
          </Button>
          <Button variant="primary" size="md">
            {t('actions.create')}
          </Button>
        </div>
      </div>

      {/* Content */}
      <div className="rounded-lg border border-border-default bg-surface-default p-6">
        {data?.length === 0 ? (
          <div className="text-center text-text-muted">
            {t('empty.message')}
          </div>
        ) : (
          <div>
            {/* 리스트 렌더링 */}
            {data?.map((item) => (
              <div key={item.id}>{item.name}</div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
```

### index.ts (Page Export)

```typescript
export { {Domain}Page } from './{Domain}Page';
```

---

## Route 템플릿

### {domain}.route.ts

```typescript
import type { RouteConfig } from '@/app/providers/router-provider';
import { lazy } from 'react';

export const {Domain}Routes: RouteConfig[] = [
  // 목록 페이지
  {
    path: '/{domains}',
    component: lazy(() =>
      import('@/pages/{domain}').then((m) => ({
        default: m.{Domain}Page,
      })),
    ),
  },

  // 상세 페이지
  {
    path: '/{domains}/$id',
    component: lazy(() =>
      import('@/pages/{domain}').then((m) => ({
        default: m.{Domain}DetailPage,
      })),
    ),
  },

  // 생성 페이지
  {
    path: '/{domains}/create',
    component: lazy(() =>
      import('@/pages/{domain}').then((m) => ({
        default: m.{Domain}CreatePage,
      })),
    ),
  },
];
```

---

## 사용법

1. `{Domain}` → 도메인명 (PascalCase, 예: `User`, `Workload`)
2. `{domain}` → 도메인명 (camelCase, 예: `user`, `workload`)
3. `{domains}` → 복수형 (URL용, 예: `users`, `workloads`)

### 예시: User 도메인

| 플레이스홀더      | 변환 결과     |
| ----------------- | ------------- |
| `{Domain}`        | `User`        |
| `{domain}`        | `user`        |
| `{domains}`       | `users`       |
| `{Domain}Entity`  | `UserEntity`  |
| `{Domain}Adapter` | `UserAdapter` |
| `use{Domain}s`    | `useUsers`    |
