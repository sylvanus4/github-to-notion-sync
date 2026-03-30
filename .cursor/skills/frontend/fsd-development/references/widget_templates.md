# Widget Templates

Widgets are composite UI that combine multiple entities. Props receive data and handlers—no business logic.

## Directory Layout

```
widgets/card/{domain}/       ← single resource card
widgets/section/{domain}/   ← list + filter + empty/error
widgets/gauge/{domain}/     ← usage display
widgets/progress-bar/{domain}/
```

## Card Widget (`widgets/card/{domain}/{Domain}Card.tsx`)

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
      <h3>{entity.name}</h3>
      <Button onClick={() => onEdit?.({domain})}>{t('actions.edit')}</Button>
    </Card>
  );
}
```

## Section Widget (`widgets/section/{domain}/{Domain}Section.tsx`)

List + filter + empty + error states.

```typescript
interface {Domain}SectionProps {
  items: {Domain}Entity[];
  isLoading: boolean;
  error: Error | null;
  onRefresh: () => void;
  onCreate: () => void;
  onEdit: (item: {Domain}Entity) => void;
  onDelete: (item: {Domain}Entity) => void;
}

export function {Domain}Section({ items, isLoading, error, onRefresh, onCreate, onEdit, onDelete }: {Domain}SectionProps) {
  if (isLoading && items.length === 0) return <LoadingSpinner />;
  if (error) return <ErrorState message={error.message} onRetry={onRefresh} />;
  return (
    <div>
      <FilterSearchInput ... />
      {filteredItems.length === 0 ? <EmptyState onCreate={onCreate} /> : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredItems.map((item) => <{Domain}Card key={item.id} {domain}={item} onEdit={onEdit} onDelete={onDelete} />)}
        </div>
      )}
    </div>
  );
}
```

## Index

```typescript
export { {Domain}Card } from './{Domain}Card';
```

**Reference:** `widgets/card/volume/`, `widgets/section/volume/`, `widgets/gauge/volume/`, `widgets/progress-bar/volume/`.
