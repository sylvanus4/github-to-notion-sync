---
name: overlay-layout-patterns
description: useOverlay 훅 기반 오버레이(모달/드로어) 구현 패턴 가이드. Overlay.Template 사용법, 올바른 Props 정의, 금지 패턴을 포함합니다. 모달, 드로어, 오버레이 컴포넌트 구현 시 사용합니다.
---

# Overlay 패턴 가이드

## useOverlay 훅 패턴 (권장)

### 동작 원리

```
openOverlay() → Zustand 스토어에 추가 → Overlay.Container가 자동 렌더링
→ onConfirm/onCancel 호출 → 스토어에서 제거 (자동 닫힘)
```

**자동 주입되는 props**: `appeared`, `onConfirm`, `onCancel`

### 올바른 컴포넌트 정의

```tsx
import { Overlay, type OverlayProps } from "@thakicloud/shared";

// ✅ OverlayProps를 extend, 고유 props만 정의
export interface MyDrawerProps extends Omit<OverlayProps, "onConfirm"> {
  itemName: string;
  onConfirm?: (result: SomeResult) => void;
}

export const MyDrawer = ({
  itemName,
  onConfirm,
  onCancel,
  ...restProps // appeared, type 등 자동 주입
}: MyDrawerProps) => {
  const handleConfirm = () => {
    onConfirm?.({ success: true });
  };

  return (
    <Overlay.Template
      {...restProps} // ← 자동 주입된 props spread (필수!)
      title="My Drawer"
      onConfirm={handleConfirm}
      onCancel={onCancel}
    >
      {/* 콘텐츠 */}
    </Overlay.Template>
  );
};
```

### 호출 방법

```tsx
// 방법 1: 직접 호출
const { openOverlay } = useOverlay();

const result = await openOverlay({
  component: MyDrawer,
  props: { itemName: "My Item" },
  options: { type: "drawer-horizontal", size: "md" },
});

// 방법 2: 커스텀 훅으로 래핑
export const useMyDrawer = ({
  type,
}: {
  type: "modal" | "drawer-horizontal";
}) => {
  const { openOverlay } = useOverlay();

  return {
    openMyDrawer: async (itemName: string) => {
      return await openOverlay({
        component: MyDrawer,
        props: { itemName },
        options: { type },
      });
    },
  };
};
```

---

## 금지 패턴 (CRITICAL)

```tsx
// ❌ isOpen 상태 직접 관리 - 스토어가 관리하므로 불필요
type BadProps = {
  isOpen: boolean; // ← 금지
  onClose: () => void; // ← onCancel로 대체
};

// ❌ appeared 수동 전달 - Overlay.Container가 자동 주입
<Overlay.Template appeared={isOpen} />

// ❌ openOverlay에 isOpen 전달
await openOverlay({ props: { isOpen: true } })

// ❌ window.confirm() 사용
if (window.confirm("삭제하시겠습니까?")) { ... }

// ❌ 커스텀 삭제 모달 직접 구현
```

---

## Props 타입 패턴

```tsx
// 결과값 없는 경우 (정보 표시용)
interface InfoDrawerProps extends Omit<OverlayProps, "onConfirm"> {
  data: SomeData;
}

// 결과값 있는 경우 (폼, 선택 등)
interface FormDrawerProps extends Omit<OverlayProps, "onConfirm"> {
  initialData?: FormData;
  onConfirm?: (result: FormData) => void;
}

// Drawer/Modal 둘 다 지원
interface MyOverlayProps extends Omit<OverlayProps, "onConfirm"> {
  variant?: "drawer" | "modal";
}
```

---

## 확인용 ActionModal

```tsx
import { useOverlay, ActionModal } from "@thakicloud/shared";

const { openOverlay } = useOverlay();

const confirmed = await openOverlay({
  component: ActionModal,
  props: {
    actionConfig: {
      title: "Delete Item",
      subtitle: "This action cannot be undone.",
      actionButtonText: "Delete",
      actionButtonVariant: "error",
      cancelButtonText: "Cancel",
    },
  },
});

if (confirmed) await deleteItem();
```

---

## openOverlay 옵션

```tsx
openOverlay({
  component: MyComponent,
  props: {
    /* 컴포넌트 props */
  },
  options: {
    type: "modal" | "drawer-horizontal" | "drawer-vertical",
    size: "sm" | "md", // drawer-horizontal만
    title: "Title",
    description: "Description",
    rejectOnCancel: false,
    duration: 300,
  },
});
```

---

## 체크리스트

새로운 Overlay 컴포넌트 작성 시:

- [ ] `OverlayProps` extend (`extends Omit<OverlayProps, 'onConfirm'>`)
- [ ] `isOpen` prop 없음 (스토어가 관리)
- [ ] `appeared` prop 직접 전달 안 함 (자동 주입)
- [ ] `...restProps` spread로 자동 주입 props 전달
- [ ] `onCancel` 사용 (`onClose` 대신)
- [ ] 결과값 있으면 `onConfirm` 타입 지정

## 추가 레퍼런스

- Overlay 컴포넌트 API: [reference.md](reference.md)
