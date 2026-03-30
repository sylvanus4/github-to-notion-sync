# Feature / Widget / Page / Route 템플릿

## Feature (비즈니스 로직)

### 서비스 (`service/{domain}.service.ts`)

```typescript
import type { {Domain}Entity } from '@/entities/{domain}';
import { {Domain}Adapter } from '@/entities/{domain}';
import { {Domain}Mapper } from '@/entities/{domain}/mapper';
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

### Query 훅 (`hooks/use{Domain}s.ts`)

```typescript
import { useQuery } from '@tanstack/react-query';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {Domain}Service } from '../service';

export const use{Domain}s = () => {
  return useQuery({
    queryKey: {domain}QueryKeys.lists(),
    queryFn: () => {Domain}Service.getList(),
  });
};
```

### Mutation 훅 (`hooks/useCreate{Domain}.ts`)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { {domain}QueryKeys } from '@/shared/constants/query-key';
import { {Domain}Adapter } from '@/entities/{domain}';

export const useCreate{Domain} = (options?: { onSuccess?: () => void }) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: {Domain}Adapter.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: {domain}QueryKeys.all() });
      options?.onSuccess?.();
    },
  });
};
```

---

## Widget (복합 UI)

Widget은 **여러 Entity/Feature를 조합한 복합 UI 컴포넌트**입니다. 비즈니스 로직 없이 props로 데이터와 핸들러를 전달받습니다.

### 디렉토리 구조

```
widgets/
├── card/{domain}/              ← 단일 리소스 카드
├── section/{domain}/           ← 리스트 + 필터 + 빈/에러 상태
├── gauge/{domain}/             ← 사용량 표시기
└── progress-bar/{domain}/      ← 프로그레스바
```

### Widget 원칙

- **Entity 타입만 사용** (DTO 직접 사용 금지)
- **비즈니스 로직 없음** (props로 데이터/핸들러 전달)
- **도메인별 하위 폴더로 구분** (`widgets/{type}/{domain}/`)
- i18n 필수 적용
- **Status Overview 카드**: Rule `08-ui-rendering-patterns.mdc` #1 Status Overview 참조

### Card Widget (`widgets/card/{domain}/{Domain}Card.tsx`)

```typescript
import type { {Domain}Entity } from '@/entities/{domain}';

interface {Domain}CardProps {
  {domain}: {Domain}Entity;
  onEdit?: ({domain}: {Domain}Entity) => void;
  onDelete?: ({domain}: {Domain}Entity) => void;
}

export function {Domain}Card({ {domain}, onEdit, onDelete }: {Domain}CardProps) {
  const { t } = useTranslation('{domain}');
  return (
    <Card>
      <h3>{{domain}.name}</h3>
      <Button onClick={() => onEdit?.({domain})}>{t('actions.edit')}</Button>
    </Card>
  );
}
```

### Section Widget (`widgets/section/{domain}/{Domain}Section.tsx`)

리스트 + 필터 + 빈 상태 + 에러 상태를 포함하는 복합 위젯입니다.
상태 카운트 카드가 필요하면 Rule `08-ui-rendering-patterns.mdc` #1 Status Overview 패턴 적용.

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
      <FilterSearchInput ... />
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

### Index (`widgets/{type}/{domain}/index.ts`)

```typescript
export { {Domain}Card } from './{Domain}Card';
```

### 참고 코드

- **Card**: `src/widgets/card/volume/VolumeCard.tsx`
- **Section**: `src/widgets/section/volume/VolumeSection.tsx`
- **Gauge**: `src/widgets/gauge/volume/QuotaGauge.tsx`
- **Progress Bar**: `src/widgets/progress-bar/volume/UsageProgressBar.tsx`

---

## Page

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
    </div>
  );
};
```

---

## Route

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
