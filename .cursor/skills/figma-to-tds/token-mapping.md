# TDS Token Mapping Reference

Figma 디자인 속성 → TDS 시맨틱 토큰 매핑 상세 테이블.
소스: `@thakicloud/shared/tailwind.preset.js` (suite `packages/shared/tailwind.preset.js`와 동일)

## 색상 매핑

### 배경색 (Background)

| 용도 | Tailwind 클래스 | 비고 |
|------|----------------|------|
| 카드/패널 배경 | `bg-surface` | 가장 기본적인 배경 |
| 비활성/음소거 배경 | `bg-surface-muted` | — |
| 호버 배경 | `bg-surface-hover` | — |
| 3차 배경 | `bg-surface-tertiary` | — |
| 미묘한 배경 | `bg-surface-subtle` | — |
| 높은 위치 요소 | `bg-surface-elevated` | 모달, 드롭다운 |
| 주요 액션 배경 | `bg-primary` | 버튼 |
| 주요 액션 호버 | `bg-primary-hover` | — |
| 보조 액션 | `bg-secondary` | — |
| 보조 액션 호버 | `bg-secondary-hover` | — |
| 3차 액션 | `bg-tertiary` | — |
| 성공 배경 | `bg-success` | — |
| 연한 성공 배경 | `bg-success-light` | 상태 표시 |
| 강한 성공 배경 | `bg-success-strong-bg` | — |
| 성공 약한 배경 | `bg-success-bg` | — |
| 에러 배경 | `bg-error` | — |
| 연한 에러 배경 | `bg-error-light` | 경고 영역 |
| 위험 배경 | `bg-danger-bg` | — |
| 경고 배경 | `bg-warning` | — |
| 연한 경고 배경 | `bg-warning-light` | — |
| 정보 배경 | `bg-info` | — |
| 연한 정보 배경 | `bg-info-light` | — |
| 약한 정보 배경 | `bg-info-weak-bg` | — |
| 중립/비활성 배경 | `bg-muted` | — |
| 연한 중립 배경 | `bg-muted-light` | — |
| 미묘한 배경 | `bg-subtle` | — |

> **주의**: `bg-primary-light`, `bg-secondary-light`, `bg-background`, `bg-overlay`는 프리셋에 **존재하지 않음**.
> 연한 배경이 필요하면 `success-light`, `error-light`, `warning-light`, `info-light`, `muted-light` 사용.
> 오버레이 효과는 `opacity-overlay` 토큰으로 처리: `bg-surface opacity-overlay`.

### 텍스트색 (Text)

| 용도 | Tailwind 클래스 |
|------|----------------|
| 기본 텍스트 | `text-text` |
| 보조/설명 텍스트 | `text-text-muted` |
| 더 연한 텍스트 | `text-text-subtle` |
| 가장 연한 텍스트 | `text-text-light` |
| 반전 텍스트 (어두운 배경 위) | `text-text-inverse` |
| 주요색 위 텍스트 | `text-on-primary` |
| 보조색 위 텍스트 | `text-on-secondary` |
| 3차색 위 텍스트 | `text-on-tertiary` |
| 성공색 위 텍스트 | `text-on-success` |
| 에러색 위 텍스트 | `text-on-error` |
| 경고색 위 텍스트 | `text-on-warning` |
| 정보색 위 텍스트 | `text-on-info` |
| 중립색 위 텍스트 | `text-on-muted` |
| 주요색 텍스트 (링크 등) | `text-primary` |
| 성공 텍스트 | `text-success` |
| 에러 텍스트 | `text-error` |
| 경고 텍스트 | `text-warning` |
| 위험 텍스트 | `text-danger` |

### 테두리 (Border)

| 용도 | Tailwind 클래스 |
|------|----------------|
| 기본 테두리 | `border-border` |
| 연한 테두리 | `border-border-muted` |
| 미묘한 테두리 | `border-border-subtle` |
| 강조 테두리 | `border-border-strong` |
| 포커스 링 | `ring-focus` |

### 테두리 두께 (Border Width)

| 용도 | Tailwind 클래스 |
|------|----------------|
| 기본 | `border` (DEFAULT) |
| 두꺼운 | `border-thick` |
| 없음 | `border-none` |

## 간격 (Spacing)

### 시맨틱 토큰 (우선 사용)

| Figma px | TDS 토큰 | 클래스 예시 |
|----------|----------|------------|
| 4px | xs | `p-xs`, `gap-xs` |
| 8px | sm | `p-sm`, `gap-sm` |
| 16px | md | `p-md`, `gap-md` |
| 24px | lg | `p-lg`, `gap-lg` |
| 32px | xl | `p-xl`, `gap-xl` |
| 48px | 2xl | `p-2xl`, `gap-2xl` |
| 64px | 3xl | `p-3xl`, `gap-3xl` |

### 용도별 시맨틱 토큰

| 토큰 | 클래스 | 용도 |
|------|--------|------|
| inline | `gap-inline`, `p-inline` | 인라인 요소 간격 |
| stack | `gap-stack`, `p-stack` | 스택 요소 간격 |
| inset | `p-inset` | 내부 여백 |
| section | `gap-section`, `p-section` | 섹션 간격 |
| block | `gap-block`, `p-block` | 블록 간격 |

### 프리미티브 토큰 (시맨틱에 없을 때)

| Figma px | 토큰 | 클래스 예시 |
|----------|------|------------|
| 0 | 0 | `p-0`, `m-0` |
| 2px | 0.5 | `p-0.5`, `gap-0.5` |
| 4px | 1 | `p-1` |
| 6px | 1.5 | `p-1.5`, `gap-1.5` |
| 8px | 2 | `p-2` |
| 10px | 2.5 | `p-2.5` |
| 12px | 3 | `p-3`, `gap-3` |
| 16px | 4 | `p-4` |
| 20px | 5 | `p-5`, `gap-5` |
| 24px | 6 | `p-6` |
| 28px | 7 | `p-7` |
| 32px | 8 | `p-8` |
| 36px | 9 | `p-9` |
| 40px | 10 | `p-10` |
| 48px | 12 | `p-12` |
| 56px | 14 | `p-14` |
| 64px | 16 | `p-16` |
| 80px | 20 | `p-20` |
| 96px | 24 | `p-24` |
| 128px | 32 | `p-32` |

## 타이포그래피

### 폰트 크기 (Font Size)

| Figma px | TDS 숫자 클래스 | TDS 시맨틱 클래스 | 비고 |
|----------|----------------|-------------------|------|
| 11px | `text-11` | `text-Xs` | — |
| 12px | `text-12` | `text-Sm` | — |
| 14px | `text-14` | `text-Md` | — |
| 16px | `text-16` | `text-Lg` | lineHeight 자동 포함 |
| 18px | `text-18` | `text-Xl` | lineHeight 자동 포함 |
| 24px | `text-24` | `text-2xl` | lineHeight 자동 포함 |
| 32px | `text-32` | `text-3xl` | lineHeight 자동 포함 |
| 40px | `text-40` | `text-4xl` | — |

> **주의**: 시맨틱 크기는 **대문자 시작** (`text-Xs`, `text-Sm`, `text-Md`, `text-Lg`, `text-Xl`)

### 폼 컨트롤 전용 폰트 크기

| 크기 | 클래스 | 용도 |
|------|--------|------|
| Small | `text-control-sm` | 작은 Input, Select |
| Medium | `text-control-md` | 기본 Input, Select |
| Large | `text-control-lg` | 큰 Input, Select |

### 폰트 굵기 (Font Weight)

| Figma 값 | Tailwind 클래스 |
|----------|----------------|
| 100 | `font-thin` |
| 200 | `font-extralight` |
| 300 | `font-light` |
| 400 | `font-normal` 또는 `font-regular` |
| 500 | `font-medium` |
| 600 | `font-semibold` |
| 700 | `font-bold` |
| 800 | `font-extrabold` |
| 900 | `font-black` |

### 폰트 패밀리 (Font Family)

| 용도 | 클래스 |
|------|--------|
| 기본 (sans-serif) | `font-sans` |
| 코드 (monospace) | `font-mono` |

### 행간 (Line Height)

| 값 | 클래스 | 비고 |
|----|--------|------|
| tight | `leading-tight` | 촘촘한 행간 |
| normal | `leading-normal` | 기본 행간 |
| relaxed | `leading-relaxed` | 넉넉한 행간 |
| 16px | `leading-16` | — |
| 18px | `leading-18` | — |
| 20px | `leading-20` | — |
| 24px | `leading-24` | — |
| 28px | `leading-28` | — |
| 32px | `leading-32` | — |
| 36px | `leading-36` | — |
| 48px | `leading-48` | — |

## 둥글기 (Border Radius)

| Figma px | TDS 클래스 | 용도 |
|----------|-----------|------|
| 0 | `rounded-none` | — |
| 2px | `rounded-sm` | — |
| 4px | `rounded-base` 또는 `rounded-base4` | 기본 |
| 6px | `rounded-md` 또는 `rounded-base6` | — |
| 8px | `rounded-lg` / `rounded-card` / `rounded-base8` | 카드 |
| 12px | `rounded-xl` | — |
| 16px | `rounded-modal` 또는 `rounded-base16` | 모달 |
| 9999px | `rounded-full` | 원형 |
| 폼 컨트롤 | `rounded-control` | Input, Select |

## 그림자 (Shadow)

| 용도 | TDS 클래스 |
|------|-----------|
| 없음 | `shadow-none` |
| 작은 그림자 | `shadow-sm` |
| 기본 그림자 | `shadow-base` |
| 중간 그림자 | `shadow-md` |
| 큰 그림자 | `shadow-lg` |
| 매우 큰 그림자 | `shadow-xl` |
| 카드 그림자 | `shadow-card` |
| 카드 호버 그림자 | `shadow-card-hover` |
| 드롭다운 그림자 | `shadow-dropdown` |
| 모달 그림자 | `shadow-modal` |
| 포커스 그림자 | `shadow-focus` |

## 투명도 (Opacity)

| 용도 | TDS 클래스 |
|------|-----------|
| 비활성화 상태 | `opacity-disabled` |
| 음소거 상태 | `opacity-muted` |
| 호버 상태 | `opacity-hover` |
| 오버레이 | `opacity-overlay` |

> **주의**: `bg-primary/10` 같은 슬래시 문법 **절대 금지**. CSS 변수 기반 색상에서 작동하지 않음.

## 전환 효과 (Transition)

| 용도 | TDS 클래스 |
|------|-----------|
| 빠른 전환 | `transition-fast` |
| 기본 전환 | `transition-normal` |
| 느린 전환 | `transition-slow` |
| 인터랙티브 요소 | `transition-interactive` |
| 콘텐츠 전환 | `transition-content` |

### Easing

| 용도 | 클래스 |
|------|--------|
| ease-out | `ease-out` |
| ease-in-out | `ease-in-out` |

## z-index

| 용도 | TDS 클래스 |
|------|-----------|
| 기본 | `z-base` |
| 살짝 위 | `z-raised` |
| 드롭다운 | `z-dropdown` |
| 모달 | `z-modal` |
| 툴팁 | `z-tooltip` |

## 컨트롤 (폼 요소)

### 높이

| 크기 | 클래스 |
|------|--------|
| Small | `h-control-sm` |
| Medium | `h-control-md` |
| Large | `h-control-lg` |

### 패딩

| 크기 | X축 | Y축 |
|------|-----|-----|
| Small | `px-control-x-sm` | `py-control-y-sm` |
| Medium | `px-control-x-md` | `py-control-y-md` |
| Large | `px-control-x-lg` | `py-control-y-lg` |
