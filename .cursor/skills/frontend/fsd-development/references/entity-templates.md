# Entity 생성 템플릿

## 1.1 도메인 타입 (`core/domain/{domain}.domain.ts`)

```typescript
// 프론트엔드용 타입 (camelCase)
export type {Domain}Entity = {
  id: string;
  name: string;
  createdAt: number;  // camelCase
  updatedAt: number;
};
```

## 1.2 DTO (`infrastructure/dto/{domain}.dto.ts`)

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

## 1.3 API 모델 (`infrastructure/model/{domain}.model.ts`) — 중첩 구조일 때만

**하위 타입이 여러 개로 중첩된 복합 구조**일 때만 Model로 분리합니다.

```typescript
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
  gpus: NodeGpuResourceApiModel[];
};

export type NodeConditionsApiModel = {
  NetworkUnavailable: string;
  MemoryPressure: string;
  DiskPressure: string;
  Ready: string;
};

export type NodeResourceInfoApiModel = {
  name: string;
  labels: Record<string, string>;
  conditions: NodeConditionsApiModel;
  allocatable: NodeResourcesApiModel;
  requests: NodeResourcesApiModel;
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

### Model vs DTO 사용 기준

| 상황 | Model | DTO |
| --- | --- | --- |
| 단순 단건 응답 | ❌ | ✅ `{Domain}ResponseDto` |
| 목록 래퍼 | ❌ | ✅ `{Domain}ListResponseDto` |
| Request params | ❌ | ✅ `Create{Domain}RequestDto` |
| 중첩/복합 구조 (하위 타입 여러 개) | ✅ 하위 타입 분리 | DTO가 Model import |

**의존성 방향**: `Model(독립, 하위 타입) ← DTO(Model import 또는 직접 정의) ← Adapter(DTO 사용)`

## 1.4 어댑터 (`infrastructure/api/{domain}.adapter.ts`)

```typescript
import { httpClient } from '@/shared/libs/api';
import type {
  {Domain}ResponseDto,
  {Domain}ListResponseDto,
  Create{Domain}RequestDto,
  Get{Domain}ListQueryDto,
} from '../dto';

export const {Domain}Adapter = {
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

  getById: async (id: string): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.get<{Domain}ResponseDto>(
      `/api/v1/{domains}/${id}`,
    );
    return response.data;
  },

  create: async (data: Create{Domain}RequestDto): Promise<{Domain}ResponseDto> => {
    const response = await httpClient.post<{Domain}ResponseDto>(
      '/api/v1/{domains}',
      data,
    );
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await httpClient.delete(`/api/v1/{domains}/${id}`);
  },
};
```

## 1.5 매퍼 (`mapper/{domain}.mapper.ts`)

```typescript
import type { {Domain}Entity } from '../core';
import type { {Domain}ResponseDto } from '../infrastructure/dto';

export const {Domain}Mapper = {
  toEntity: (dto: {Domain}ResponseDto): {Domain}Entity => ({
    id: dto.id,
    name: dto.name,
    createdAt: dto.created_at,
    updatedAt: dto.updated_at,
  }),

  toEntityList: (dtos: {Domain}ResponseDto[]): {Domain}Entity[] =>
    dtos.map({Domain}Mapper.toEntity),
};
```

## 1.6 타입 (`types/{domain}.types.ts`)

```typescript
export type {Domain}Status = 'ACTIVE' | 'INACTIVE' | 'ERROR';
export type {Domain}Type = 'TYPE_A' | 'TYPE_B';
```

## 1.7 스키마 (`core/schema/{domain}.schema.ts`)

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

## 1.8 Form Hook (`features/{domain}/hooks/use{Domain}Form.ts`)

Entity 스키마를 기반으로 Feature layer에서 폼 훅을 생성합니다.
상세 패턴은 Rule `05-form-and-mutation.mdc` #2 참조.

**CRITICAL**: `react-hook-form`의 `useForm`을 직접 사용하지 않고, 반드시 `useFormWithI18n` from `@/shared/libs/form`을 사용합니다.
이 훅은 언어 전환 시 Zod 스키마 기반 에러 메시지를 자동 재검증합니다.

```typescript
import { zodResolver } from '@hookform/resolvers/zod';
import { useMemo } from 'react';
import { useTranslation } from 'react-i18next';

import { useFormWithI18n } from '@/shared/libs/form';
import {
  create{Domain}FormSchema,
  type {Domain}FormValues,
} from '@/entities/{domain}';

const DEFAULT_VALUES: {Domain}FormValues = {
  name: '',
  description: '',
};

export function use{Domain}Form() {
  const { t } = useTranslation('{domain}');

  const schema = useMemo(() => create{Domain}FormSchema(t), [t]);

  const form = useFormWithI18n<{Domain}FormValues>({
    resolver: zodResolver(schema),
    mode: 'onBlur',
    reValidateMode: 'onChange',
    defaultValues: DEFAULT_VALUES,
  });

  const resetForm = (): void => {
    form.reset(DEFAULT_VALUES);
  };

  return { form, resetForm };
}
```

**참고 코드**: `features/volume/hooks/useVolumeForm.ts`, `features/volume/hooks/useVolumeShareForm.ts`

## 1.9 Index (`index.ts`)

```typescript
// Public API - 명시적 named export (export * 금지!)

export type { {Domain}Entity } from './core';

export { {Domain}Adapter } from './infrastructure';
export type {
  {Domain}ResponseDto,
  {Domain}ListResponseDto,
  Create{Domain}RequestDto,
  Get{Domain}ListQueryDto,
} from './infrastructure';

export { {Domain}Mapper } from './mapper';
export type { {Domain}Status, {Domain}Type } from './types';
```
