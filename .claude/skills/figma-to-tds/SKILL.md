---
name: figma-to-tds
description: >-
  Figma 디자인을 TDS(@thakicloud/shared) 토큰과 컴포넌트로 변환하여 React TSX 코드를 생성합니다. Figma
  URL 제공 시, 피그마, Figma 구현, 디자인 변환, 레이아웃 구현, 단일 컴포넌트/섹션 구현 시 사용합니다. Do NOT use
  for 전체 화면 구현 오케스트레이션(implement-screen), 디자인 리뷰(design-review), 또는 기획서
  작성(screen-description).
---

# Figma → TDS Code Generator

## Prerequisites

- Figma MCP server 연결 필수
- Figma URL 형식: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

## Workflow

### Step 0 – 화면 기획서 확인 (선택)

`docs/screens/{domain}/{screen}.md` 경로에서 기획서를 검색. 있으면 인터랙션 정의, 상태별 화면, 컴포넌트 구성 정보를 참고. 없으면 건너뜀.

### Step 1 – Figma URL 파싱 및 디자인 데이터 수집

1. URL에서 `fileKey`와 `nodeId` 추출
2. **반드시 두 MCP 도구를 병렬 호출**: `get_design_context` + `get_screenshot`
3. 응답이 truncated된 경우: `get_metadata`로 구조 파악 → 하위 노드별 개별 호출

### Step 2 – TDS 토큰 매핑

Figma 색상/간격/타이포그래피를 **TDS 시맨틱 토큰**으로 매핑. 상세 테이블은 [token-mapping.md](token-mapping.md) 참조.

**핵심 원칙**:
- Figma hex → 가장 가까운 시맨틱 색상 클래스
- `bg-blue-500` 같은 Tailwind 기본 색상 **절대 금지**
- `bg-primary/10` 같은 opacity modifier **절대 금지**
- 연한 배경 → `bg-success-light`, `bg-error-light`, `bg-warning-light`, `bg-info-light`, `bg-muted-light`
- `bg-primary-light`는 **존재하지 않음**

### Step 3 – TDS 컴포넌트 우선 매칭

| Figma 요소 | TDS 컴포넌트 |
|-----------|-------------|
| 버튼 | `Button` (variant, size, appearance) |
| 입력 필드 | `Input`, `Textarea`, `FormField` |
| 테이블 | `Table`, `SelectableTable` |
| 드롭다운 | `ContextMenu`, `Dropdown` |
| 모달/드로어 | `Overlay` (useOverlay 패턴) |
| 페이지네이션 | `Pagination` |
| 레이아웃 | `Layout.VStack`, `Layout.HStack`, `Layout.Block` |
| 텍스트 | `Typography.Heading`, `Typography.Text` |

TDS에 없는 요소만 시맨틱 토큰 + Tailwind로 직접 구현.

### Step 4 – 코드 생성

**전체 화면 구현** 시에는 `implement-screen` Skill의 Phase 3 사용 권장. 이 Step은 **단일 컴포넌트/섹션** 구현 시에 사용.

**코드 생성 규칙**:
- Arrow function 컴포넌트
- Props는 `interface` 사용
- 모든 텍스트 `t()` i18n 처리
- 시맨틱 컬러만 사용 (Tailwind 기본 색상 금지)
- TDS 컴포넌트 Props는 `04-tds-detail-catalog.mdc` 참조 (필수 규칙은 `03-tds-essentials.mdc` 자동 적용)

### Step 5 – 검증

- [ ] 레이아웃(간격, 정렬, 크기) 일치
- [ ] 타이포그래피(폰트 크기, 굵기) 일치
- [ ] 색상 → 시맨틱 토큰 정확 매핑
- [ ] TDS 컴포넌트 우선 사용됨
- [ ] i18n 처리 완료

## Figma MCP 실패 시

1. **즉시 중단** — 추측으로 구현 금지
2. 사용자에게 에러 알림
3. 대안 제시: 재시도 / 스크린샷 제공 / 텍스트 설명

## 간격 토큰 빠른 참조

| Figma px | TDS 토큰 | Tailwind 클래스 |
|----------|----------|----------------|
| 4px | xs | `p-xs`, `gap-xs` |
| 8px | sm | `p-sm`, `gap-sm` |
| 16px | md | `p-md`, `gap-md` |
| 24px | lg | `p-lg`, `gap-lg` |
| 32px | xl | `p-xl`, `gap-xl` |

## 폰트 크기 빠른 참조

| Figma px | TDS 클래스 |
|----------|-----------|
| 11px | `text-11` / `text-Xs` |
| 12px | `text-12` / `text-Sm` |
| 14px | `text-14` / `text-Md` |
| 16px | `text-16` / `text-Lg` |
| 24px | `text-24` / `text-2xl` |

## Cross-reference

| 상황 | 연결 Skill / Rule |
|------|-------------------|
| 화면 기획서 존재 시 | `screen-description` → Step 0에서 기획서 참조 |
| 전체 화면 구현 시 | `implement-screen` → Phase 3 FSD 코드 생성 |
| TDS 컴포넌트 Props 확인 | `03-tds-essentials.mdc`(자동) + `04-tds-detail-catalog.mdc` Rule |
| 모달/드로어 구현 시 | `overlay-layout-patterns` Skill |

## Examples

### Example 1: 단일 섹션 Figma 구현
User says: "이 Figma 카드 컴포넌트 구현해줘. https://figma.com/design/abc/File?node-id=42-15"
Actions:
1. Figma MCP로 design context + screenshot 수집
2. 색상/간격을 TDS 시맨틱 토큰으로 매핑
3. Figma 요소를 TDS 컴포넌트(Layout.Block, Typography.Text, Badge)에 매칭
4. Arrow function 컴포넌트로 코드 생성
Result: Figma 디자인과 일치하는 TDS 기반 카드 컴포넌트 생성

### Example 2: 전체 페이지 Figma 분석만 수행
User says: "이 Figma 페이지의 TDS 컴포넌트 매핑 분석해줘"
Actions:
1. Figma MCP로 디자인 데이터 수집
2. 컴포넌트 맵(Figma 요소 → TDS 컴포넌트) 작성
3. 토큰 맵(색상/간격/폰트 → TDS 토큰) 작성
4. 코드 생성 없이 분석 결과만 반환
Result: Component Map + Token Map이 생성되어 implement-screen Phase 3에서 활용 가능

## Troubleshooting

### Figma MCP 호출 실패 (timeout/auth error)
Cause: Figma MCP 서버 미연결, 인증 만료, 또는 노드 ID 오류
Solution: 즉시 중단 후 사용자에게 에러 알림. Figma 데스크톱 앱 연결 상태와 URL 정확성 확인 요청

### 시맨틱 토큰 매핑 불확실
Cause: Figma 디자인에서 비표준 색상(커스텀 hex)이 사용됨
Solution: token-mapping.md의 색상 테이블에서 가장 가까운 시맨틱 토큰 선택. 확신 없으면 사용자에게 확인 요청
