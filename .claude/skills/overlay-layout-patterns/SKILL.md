---
name: overlay-layout-patterns
description: >-
  useOverlay 훅 기반 오버레이(모달/드로어) 구현 패턴 가이드. Overlay.Template 사용법, 올바른 Props 정의,
  금지 패턴을 포함합니다. 모달, 드로어, 오버레이, ActionModal, 삭제 확인 구현 시 사용합니다. Do NOT use for
  전체 화면 구현(implement-screen) 또는 Figma 컴포넌트 매칭(figma-to-tds).
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

export interface MyDrawerProps extends Omit<OverlayProps, "onConfirm"> {
  itemName: string;
  onConfirm?: (result: SomeResult) => void;
}

export const MyDrawer = ({
  itemName,
  onConfirm,
  onCancel,
  ...restProps
}: MyDrawerProps) => {
  const handleConfirm = () => {
    onConfirm?.({ success: true });
  };

  return (
    <Overlay.Template
      {...restProps}
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
const { openOverlay } = useOverlay();

const result = await openOverlay({
  component: MyDrawer,
  props: { itemName: "My Item" },
  options: { type: "drawer-horizontal", size: "md" },
});
```

---

## 금지 패턴 (CRITICAL)

```tsx
// ❌ isOpen 상태 직접 관리 - 스토어가 관리하므로 불필요
type BadProps = {
  isOpen: boolean;
  onClose: () => void; // ← onCancel로 대체
};

// ❌ appeared 수동 전달
<Overlay.Template appeared={isOpen} />

// ❌ window.confirm() 사용
if (window.confirm("삭제하시겠습니까?")) { ... }
```

---

## Props 타입 패턴

```tsx
// 결과값 없는 경우
interface InfoDrawerProps extends Omit<OverlayProps, "onConfirm"> {
  data: SomeData;
}

// 결과값 있는 경우
interface FormDrawerProps extends Omit<OverlayProps, "onConfirm"> {
  initialData?: FormData;
  onConfirm?: (result: FormData) => void;
}
```

---

## 확인용 ActionModal

```tsx
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
  props: { /* 컴포넌트 props */ },
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

- [ ] `OverlayProps` extend (`extends Omit<OverlayProps, 'onConfirm'>`)
- [ ] `isOpen` prop 없음 (스토어가 관리)
- [ ] `appeared` prop 직접 전달 안 함 (자동 주입)
- [ ] `...restProps` spread로 자동 주입 props 전달
- [ ] `onCancel` 사용 (`onClose` 대신)
- [ ] 결과값 있으면 `onConfirm` 타입 지정

## Cross-reference

| 상황 | 연결 Skill / Rule |
|------|-------------------|
| 전체 화면 구현 시 | `implement-screen` → Phase 3에서 Overlay 필요 시 이 Skill 참조 |
| Figma에서 모달/드로어 발견 시 | `figma-to-tds` → Step 3 컴포넌트 매칭에서 Overlay 매핑 |
| TDS Overlay Props 확인 | `03-tds-essentials.mdc`(자동) + `04-tds-detail-catalog.mdc` Rule → Overlay 섹션 참조 |

## 추가 레퍼런스

- Overlay 컴포넌트 API: [references/reference.md](references/reference.md)

## Examples

### Example 1: 삭제 확인 모달 구현
User says: "리소스 삭제 확인 모달 만들어줘"
Actions:
1. ActionModal + openOverlay 패턴으로 삭제 확인 로직 작성
2. actionConfig에 title, subtitle, actionButtonVariant: 'error' 설정
3. confirmed 결과로 deleteMutation 호출
Result: TDS ActionModal 기반의 삭제 확인 모달이 구현됨

### Example 2: 커스텀 폼 드로어 구현
User says: "리소스 편집 드로어 만들어줘"
Actions:
1. OverlayProps를 extend한 FormDrawerProps 정의
2. Overlay.Template에 ...restProps spread + onConfirm/onCancel 연결
3. openOverlay에 type: 'drawer-horizontal', size: 'md' 설정
Result: 폼 입력 후 결과를 반환하는 드로어가 구현됨

## Troubleshooting

### 드로어/모달이 열리지 않음
Cause: Overlay.Container가 앱 루트에 마운트되지 않았거나, openOverlay를 잘못 호출
Solution: App 루트에 Overlay.Container가 있는지 확인. component에 JSX가 아닌 컴포넌트 참조를 전달

### 닫기 후에도 상태가 남아 있음
Cause: onConfirm/onCancel 호출 없이 수동으로 상태 변경 시도
Solution: 반드시 onConfirm() 또는 onCancel()을 호출해야 스토어에서 제거됨. isOpen 수동 관리 금지
