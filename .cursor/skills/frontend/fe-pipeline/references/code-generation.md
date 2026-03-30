# Phase 5 – Code Generation 상세

Phase 4(Entity)까지 완료된 상태에서, 기획서 + Figma 분석 + 유사 컴포넌트 참조를 바탕으로 Feature → Widget → Page → Route를 생성하는 규칙.

기반 템플릿: `fsd-development/references/feature-widget-page-templates.md`

---

## 1. 입력 컨텍스트 전달

Phase 5는 이전 Phase 산출물을 **명시적으로 참조**하여 코드에 반영해야 한다.

| 소스 Phase | 산출물 | Phase 5에서의 용도 |
|-----------|--------|-------------------|
| Phase 2 (Screen Spec) | `docs/screens/{domain}/*.md` | 인터랙션 정의 → 이벤트 핸들러, 상태별 화면 → 조건부 렌더링 |
| Phase 3 (Figma) | Component Map + Token Map (메모리) | TDS 컴포넌트 선택, 간격/색상 토큰 적용 |
| Phase 3.5 (유사 스캔) | 유사 컴포넌트 목록 | 코드 구조/패턴 참조 (복사가 아닌 패턴 참조) |
| Phase 4 (Entity) | `src/entities/{domain}/` | 타입 import, Adapter/Mapper 사용 |
| CP 1 (Plan) | 생성 파일 목록 | 생성할 파일 경로 확정 |

### 참조 방법

```
Phase 5 시작 전 확인:
1. 기획서 읽기: docs/screens/{domain}/*.md
2. Entity 타입 확인: src/entities/{domain}/core/domain/{domain}.domain.ts
3. Adapter 메서드 확인: src/entities/{domain}/infrastructure/api/{domain}.adapter.ts
4. 유사 컴포넌트 코드 읽기: Phase 3.5에서 식별된 파일 (최대 3개)
5. Figma Component Map 참조 (메모리): 각 UI 영역 → TDS 컴포넌트 매핑
```

---

## 2. Sub-phase 구조

### 의존성 순서 (필수)

```
5.1 Feature ──→ 5.2 Widget ──→ 5.3 Page ──→ 5.4 Route
                                    ↓
                              5.5 Overlay (필요 시)
```

각 Sub-phase는 이전 단계가 완료되어야 import 가능.

---

### 5.1 Feature 레이어

**생성 파일**:

```
features/{domain}/
├── service/{domain}.service.ts
├── hooks/
│   ├── use{Domain}s.ts            (목록 Query)
│   ├── use{Domain}.ts             (상세 Query, Detail 화면 시)
│   ├── useCreate{Domain}.ts       (생성 Mutation)
│   └── useDelete{Domain}.ts       (삭제 Mutation)
└── index.ts
```

**기획서 → Feature 매핑**:

| 기획서 인터랙션 | 생성할 훅 |
|---------------|----------|
| 목록 조회 | `use{Domain}s` (useQuery) |
| 상세 조회 | `use{Domain}` (useQuery) |
| 생성 버튼 → 폼 제출 | `useCreate{Domain}` (useMutation) |
| 삭제 버튼 → 확인 → 삭제 | `useDelete{Domain}` (useMutation) |
| 시작/중지 등 커스텀 액션 | `use{Action}{Domain}` (useMutation) |

**규칙**:
- Query Key는 반드시 `shared/constants/query-key/`에서 import
- Mutation `onSuccess`에서 관련 쿼리 invalidate
- Toast는 `sonner` + `Toast` 컴포넌트 패턴 (Rule: `13-frontend-patterns.mdc` #4)
- Service에서 Mapper.toEntity/toEntityList 변환 필수

**템플릿 참조**: `fsd-development/references/feature-widget-page-templates.md` Feature 섹션

---

### 5.2 Widget 레이어

**화면 유형별 생성 전략**:

| 화면 유형 | 생성할 Widget | 디렉토리 |
|----------|-------------|---------|
| **List** | Table 또는 Card + Section | `widgets/table/{domain}/` 또는 `widgets/card/{domain}/` + `widgets/section/{domain}/` |
| **Detail** | DetailCard + Tabs 내 섹션 | `widgets/section/{domain}/` |
| **Create/Edit** | FormDrawer 또는 CreatePage 내 Form | `widgets/form/{domain}/` |
| **Dashboard** | StatCard + Chart Section | `widgets/card/{domain}/` |

**Figma Component Map 활용**:

```
Component Map에서 "테이블" → SelectableTable 사용 결정
Component Map에서 "카드 그리드" → Card + Grid 레이아웃 결정
Component Map에서 "폼 드로어" → Overlay.Template + FormField 결정
```

**Table Widget 생성 시** (기획서에 테이블 정의가 있을 때):
1. COLUMN_KEYS 상수 정의 (Rule: `08-table-component-patterns.mdc`)
2. columns + columnMap 패턴 적용
3. Status 매핑 상수 (기획서 상태 목록 참조)
4. 액션 셀에 `preventClickPropagation` 필수
5. emptyUI는 `EmptyUI` 직접 사용 (테이블이 컨테이너 제공)

**Card Widget 생성 시** (기획서에 카드 레이아웃 정의가 있을 때):
1. Entity 타입만 props로 받기 (DTO 금지)
2. 액션 핸들러는 props callback으로 전달
3. Skeleton 컴포넌트도 함께 생성 (Rule: `15-loading-skeleton-patterns.mdc`)

**Form Widget 생성 시** (기획서에 생성/편집 폼 정의가 있을 때):
1. Zod 스키마는 Phase 4에서 `core/schema/`에 이미 생성됨
2. `useFormWithI18n` from `@/shared/libs/form` + `zodResolver` 패턴 (Rule: `05-form-and-mutation.mdc` #2). `useForm` 직접 사용 금지.
3. Controller 바인딩 필수 (비네이티브 입력)
4. Drawer 패턴은 Rule: `05-form-and-mutation.mdc` #3

**템플릿 참조**: `fsd-development/references/feature-widget-page-templates.md` Widget 섹션

---

### 5.3 Page 레이어

**화면 유형별 Page 구조**:

#### List Page

```
{Domain}Page
├── ActionBar (생성 버튼, 새로고침, 벌크 액션)
├── FilterSearchInput (필터 키 + 검색)
├── [Status Overview] (기획서에 상태 카운트 정의 시)
├── Table 또는 Card Grid (Widget 참조)
├── Pagination
└── [CreateDrawer / DeleteModal] (Overlay)
```

**기획서 → Page 매핑**:

| 기획서 섹션 | Page 코드 영역 |
|-----------|--------------|
| 상단 액션 바 | ActionBar + Button |
| 필터/검색 | useFilterSearch 훅 + FilterSearchInput |
| 목록 영역 | Widget (Table/Card) |
| 페이지네이션 | Pagination 컴포넌트 |
| 빈 상태 | EmptyStatePanel (섹션) 또는 EmptyUI (테이블) |
| 로딩 상태 | isLoading → Skeleton 또는 Table isLoading |
| 생성 드로어 | useOverlay + CreateDrawer Widget |
| 삭제 확인 | useOverlay + DeleteResourceModal |

#### Detail Page

```
{Domain}DetailPage
├── DetailPageHeader (뒤로가기 + 제목 + 상태 + 액션)
├── Tabs (useTabSearchParam 훅으로 URL 동기화)
│   ├── Tab: Details (DetailCard + infoFields)
│   ├── Tab: Logs (기획서에 로그 정의 시)
│   └── Tab: Settings (기획서에 설정 정의 시)
└── [EditDrawer / DeleteModal] (Overlay)
```

#### Create Page (풀 페이지 폼)

```
{Domain}CreatePage
├── CreateLayout
│   ├── Fieldset (논리적 그룹)
│   │   ├── FormField + Input/Dropdown/Toggle
│   │   └── FormField + Input/Dropdown/Toggle
│   └── Fieldset
└── Footer (취소 + 생성 버튼)
```

**규칙**:
- Page는 Feature 훅을 호출하여 데이터/핸들러를 Widget에 전달
- Page 자체에 비즈니스 로직 최소화 (Widget/Feature에 위임)
- 탭이 있으면 `useTabSearchParam` 필수 (Rule: `13-frontend-patterns.mdc` #1)

---

### 5.4 Route 등록

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
  // Detail 화면이 있을 때
  {
    path: '/{domains}/:id',
    component: lazy(() =>
      import('@/pages/{domain}').then((m) => ({
        default: m.{Domain}DetailPage,
      })),
    ),
  },
];
```

기존 라우트 파일에 등록:
1. `app/routes/` 에서 기존 라우트 구조 확인
2. 동일 패턴으로 새 도메인 라우트 추가
3. 라우트 등록 파일(routeConfig 등)에 import 추가

---

### 5.5 Overlay/Drawer (기획서에 정의 시)

기획서에 다음이 정의된 경우에만 실행:
- 생성/편집 드로어
- 삭제 확인 모달
- 상세 정보 모달
- 공유/내보내기 드로어

**패턴 참조**: `overlay-layout-patterns` Skill

**생성 파일 위치**:

| Overlay 유형 | 파일 위치 |
|-------------|---------|
| 생성/편집 Drawer (Form 포함) | `widgets/form/{domain}/Create{Domain}Drawer.tsx` |
| 삭제 확인 Modal | `DeleteResourceModal` 재사용 (TDS 제공) |
| 커스텀 액션 Modal | `widgets/modal/{domain}/{Action}Modal.tsx` |
| 다중 뷰 Drawer | `features/{domain}/ui/{Domain}ListDrawer.tsx` |

---

## 3. 생성 순서 체크리스트

```
[ ] 5.1 Feature
    [ ] service/{domain}.service.ts
    [ ] hooks/use{Domain}s.ts (목록)
    [ ] hooks/use{Domain}.ts (상세, 필요 시)
    [ ] hooks/useCreate{Domain}.ts (생성, 필요 시)
    [ ] hooks/useDelete{Domain}.ts (삭제, 필요 시)
    [ ] hooks/use{Action}{Domain}.ts (커스텀 액션, 필요 시)
    [ ] index.ts

[ ] 5.2 Widget
    [ ] 화면 유형에 맞는 Widget 생성
    [ ] Skeleton 컴포넌트 (카드 리스트 시)
    [ ] index.ts

[ ] 5.3 Page
    [ ] {Domain}Page.tsx (목록)
    [ ] {Domain}DetailPage.tsx (상세, 필요 시)
    [ ] index.ts

[ ] 5.4 Route
    [ ] {domain}.route.ts
    [ ] 라우트 등록 파일에 import 추가

[ ] 5.5 Overlay (필요 시)
    [ ] Create/Edit Drawer
    [ ] Delete Modal (TDS 재사용 또는 커스텀)
```

---

## 4. Figma 없을 때의 코드 생성

Figma Component Map이 없을 때는 **유사 컴포넌트 + 화면 유형 기본 구성**으로 대체:

| 화면 유형 | 기본 TDS 구성 (auto-discovery.md §3.3) |
|----------|--------------------------------------|
| List | ActionBar + FilterSearchInput + SelectableTable + Pagination |
| Detail | DetailPageHeader + DetailCard + Tabs |
| Create | CreateLayout + Fieldset + FormField |
| Dashboard | Layout.Grid + FloatingCard |

유사 컴포넌트의 JSX 구조를 읽어서 레이아웃 패턴만 참조 (코드 복사 금지).

---

## 5. 참조 구현 (실제 프로젝트 코드)

| 패턴 | 파일 |
|------|------|
| Service | `features/devspace/service/devspace.service.ts` |
| Query 훅 | `features/volume/hooks/useMyVolumesTab.ts` |
| Mutation 훅 | `features/volume/hooks/queries/useCreateSnapshotMutation.ts` |
| Table Widget | `widgets/table/devspace/DevSpaceTable.tsx` |
| Card Widget | `widgets/card/volume/VolumeCard.tsx` |
| Section Widget | `widgets/section/volume/VolumeSection.tsx` |
| Form Drawer | `widgets/form/devspace/CreateDevSpaceDrawer.tsx` |
| Skeleton | `features/volume/ui/VolumeCardSkeleton.tsx` |
| Page (목록) | `pages/devspace/DevSpacePage.tsx` |
| Delete Modal | `DeleteResourceModal` (TDS 제공) |
