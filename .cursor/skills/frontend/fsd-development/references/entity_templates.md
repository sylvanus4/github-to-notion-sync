# Entity Creation Templates

Detailed code templates for creating FSD entities. Replace `{Domain}`/`{domain}` with your domain name.

## 1.1 Domain Type (`core/domain/{domain}.domain.ts`)

```typescript
export type {Domain}Entity = {
  id: string;
  name: string;
  createdAt: number;
  updatedAt: number;
};
```

## 1.2 DTO (`infrastructure/dto/{domain}.dto.ts`)

```typescript
// Response DTOs
export type {Domain}ResponseDto = {
  id: string;
  name: string;
  status: string;
  owner_id: string;
  created_at: number;
  updated_at: number;
};

export type {Domain}ListResponseDto = {
  items: {Domain}ResponseDto[];
  total: number;
  page: number;
  page_size: number;
};

export type {Domain}ActionResponseDto = { id?: string; message?: string; status?: string; };

// Request DTOs
export type Create{Domain}RequestDto = { name: string; description?: string; };
export type Get{Domain}ListQueryDto = {
  status?: string; q?: string; page?: number; page_size?: number; sort?: string; order?: 'asc' | 'desc';
};
```

## 1.3 API Model (`infrastructure/model/{domain}.model.ts`) — nested structures only

Use only when you have multiple nested sub-types. For simple single-entity responses, define in DTO directly.

## 1.4 Adapter (`infrastructure/api/{domain}.adapter.ts`)

```typescript
import { httpClient } from '@/shared/libs/api';
import type { {Domain}ResponseDto, {Domain}ListResponseDto, Create{Domain}RequestDto, Get{Domain}ListQueryDto } from '../dto';

export const {Domain}Adapter = {
  getList: async (orgId: string, projectId: string, params?: Get{Domain}ListQueryDto): Promise<{Domain}ListResponseDto> =>
    (await httpClient.get(`/api/v1/orgs/${orgId}/projects/${projectId}/{domains}`, { params })).data,
  getById: async (id: string): Promise<{Domain}ResponseDto> =>
    (await httpClient.get(`/api/v1/{domains}/${id}`)).data,
  create: async (data: Create{Domain}RequestDto): Promise<{Domain}ResponseDto> =>
    (await httpClient.post('/api/v1/{domains}', data)).data,
  delete: async (id: string): Promise<void> => { await httpClient.delete(`/api/v1/{domains}/${id}`); },
};
```

## 1.5 Mapper (`mapper/{domain}.mapper.ts`)

```typescript
import type { {Domain}Entity } from '../core';
import type { {Domain}ResponseDto } from '../infrastructure/dto';

export const {Domain}Mapper = {
  toEntity: (dto: {Domain}ResponseDto): {Domain}Entity => ({
    id: dto.id, name: dto.name, createdAt: dto.created_at, updatedAt: dto.updated_at,
  }),
  toEntityList: (dtos: {Domain}ResponseDto[]): {Domain}Entity[] => dtos.map({Domain}Mapper.toEntity),
};
```

## 1.6 Types (`types/{domain}.types.ts`)

```typescript
export type {Domain}Status = 'ACTIVE' | 'INACTIVE' | 'ERROR';
export type {Domain}Type = 'TYPE_A' | 'TYPE_B';
```

## 1.7 Schema (`core/schema/{domain}.schema.ts`) — when needed

```typescript
import { z } from 'zod';
export const create{Domain}Schema = (t: (key: string) => string) =>
  z.object({ name: z.string().min(1, t('{domain}.validation.name.required')).max(100, t('{domain}.validation.name.maxLength')) });
export type Create{Domain}Credentials = z.infer<ReturnType<typeof create{Domain}Schema>>;
```

## 1.8 Index (`index.ts`)

```typescript
export type { {Domain}Entity } from './core';
export { {Domain}Adapter } from './infrastructure';
export type { {Domain}ResponseDto, {Domain}ListResponseDto, Create{Domain}RequestDto, Get{Domain}ListQueryDto } from './infrastructure';
export { {Domain}Mapper } from './mapper';
export type { {Domain}Status, {Domain}Type } from './types';
```

**Model vs DTO:** Single response → DTO. Nested/complex structure → Model (sub-types) + DTO imports Model.

**Reference:** `entities/template/`, `entities/node/` (nested), `entities/ai-model/` (multi-source).
