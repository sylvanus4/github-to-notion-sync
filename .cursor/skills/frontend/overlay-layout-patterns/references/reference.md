# Overlay 컴포넌트 API 레퍼런스

## Overlay 컴포넌트

```typescript
import { Overlay } from "@thakicloud/shared";
```

### Overlay.Template

기본 오버레이 템플릿 (모달/드로어).

```tsx
<Overlay.Template
  type="modal | drawer-horizontal | drawer-vertical" // 필수
  appeared={boolean} // 필수 (useOverlay 시 자동 주입)
  title="Title"
  size="sm | md | lg | xl | full" // 기본값: 'md'
  // 액션 버튼
  onConfirm={handleConfirm}
  onCancel={handleCancel}
  confirmUI="Save" // 기본값: 'Confirm'
  cancelUI="Cancel" // 기본값: 'Cancel'
  // 상태
  isLoading={false}
  confirmDisabled={false}
>
  {children}
</Overlay.Template>
```

### Size 옵션

| Size   | Modal 너비 | Drawer 너비 |
| ------ | ---------- | ----------- |
| `sm`   | 400px      | 320px       |
| `md`   | 500px      | 400px       |
| `lg`   | 600px      | 500px       |
| `xl`   | 800px      | 640px       |
| `full` | 100vw      | 100vw       |

### 저수준 API (Overlay.Container)

세밀한 제어가 필요한 경우:

```tsx
<Overlay.Template
  type="modal"
  appeared={isOpen}
  onCancel={() => setIsOpen(false)}
>
  <Overlay.Container>
    <Overlay.Header>
      <h2>Custom Header</h2>
    </Overlay.Header>
    <Overlay.Body>
      <p>Custom body</p>
    </Overlay.Body>
    <Overlay.Footer>
      <Button onClick={handleAction}>Custom Action</Button>
    </Overlay.Footer>
  </Overlay.Container>
</Overlay.Template>
```

### 커스텀 푸터

```tsx
<Overlay.Template
  type="modal"
  title="Wizard"
  appeared={isOpen}
  onCancel={onCancel}
>
  <p>Content</p>
  <Layout.HStack gap="sm" justify="end" className="mt-4">
    <Button variant="muted" appearance="ghost" onClick={handleSkip}>
      Skip
    </Button>
    <Button variant="secondary" appearance="outline" onClick={handleBack}>
      Back
    </Button>
    <Button variant="primary" onClick={handleNext}>
      Next
    </Button>
  </Layout.HStack>
</Overlay.Template>
```

---

## useOverlay Provider 설정

App.tsx에 다음 설정이 필요합니다:

```tsx
import "@thakicloud/shared/core.css";
import {
  createOverlayStore,
  Overlay,
  OverlayProvider,
} from "@thakicloud/shared";

const overlayStore = createOverlayStore();

const App = () => (
  <OverlayProvider overlayStore={overlayStore}>
    <YourApp />
    <Overlay.Container overlayStore={overlayStore} />
  </OverlayProvider>
);
```

---

## 타입 Import

```tsx
import type {
  OverlayProps,
  OverlayOptions,
  ActionConfig,
  ActionModalProps,
  ResourceActionModalProps,
} from "@thakicloud/shared";
```
