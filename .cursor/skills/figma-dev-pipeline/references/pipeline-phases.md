# Figma-Dev Pipeline Phase Details

## Phase 1: Design Extraction — 상세

### Figma MCP 호출 순서

1. 파일 메타데이터 조회 (파일명, 페이지 목록)
2. 대상 페이지/프레임 노드 조회
3. 컴포넌트 세트(Component Set) 식별
4. 각 컴포넌트의 variant 속성 추출
5. 스타일 (색상, 텍스트, 이펙트) 추출
6. Auto Layout 속성 추출
7. 에셋 (아이콘, 이미지) 식별

### 추출 데이터 구조

```json
{
  "file": { "name": "", "url": "" },
  "components": [
    {
      "name": "Button",
      "variants": [
        { "property": "Type", "values": ["Primary", "Secondary"] },
        { "property": "Size", "values": ["S", "M", "L"] }
      ],
      "states": ["Default", "Hover", "Active", "Disabled"],
      "layout": { "type": "horizontal", "padding": "12 24", "gap": 8 },
      "tokens": {
        "background": "primary-500",
        "text": "white",
        "borderRadius": "radius-md",
        "fontSize": "body-md"
      }
    }
  ],
  "tokens": { ... }
}
```

## Phase 2: Spec Generation — 상세

### 토큰 매핑 프로세스

1. Figma 토큰 목록 추출
2. 프로젝트 기존 토큰과 대조 (있으면 기존 것 사용)
3. 신규 토큰은 프로젝트 네이밍 컨벤션에 맞게 변환
4. CSS 변수 / Tailwind config / theme 파일 생성

### 컴포넌트 스펙 문서 형식

| 속성 | 값 | 토큰 | CSS |
|------|-----|------|-----|
| Background | #3B82F6 | primary-500 | var(--color-primary-500) |
| Font Size | 16px | body-md | text-base |
| Padding | 12px 24px | space-3, space-6 | px-6 py-3 |

## Phase 3: Code Scaffolding — 상세

### 파일 구조 (React 예시)

```
src/components/
├── Button/
│   ├── Button.tsx          # 컴포넌트
│   ├── Button.styles.ts    # 스타일 (또는 Tailwind classes)
│   ├── Button.types.ts     # TypeScript 타입
│   ├── Button.stories.tsx  # Storybook (선택)
│   └── index.ts            # barrel export
├── tokens/
│   ├── colors.ts
│   ├── typography.ts
│   └── spacing.ts
```

### 스캐폴드 규칙

- Props는 Figma variant와 1:1 매핑
- 기본값은 Figma의 default variant
- 이벤트 핸들러는 표준 HTML 이벤트 기반
- 스타일은 CSS 방식 설정에 따라 생성

## Phase 4: Implementation Guide — 상세

### 가이드 문서 구조

1. **컴포넌트 개요**: 기능, 사용 맥락
2. **Props 명세**: 타입, 기본값, 설명
3. **상태 동작**: 각 state에서의 UI 변화
4. **인터랙션**: hover, focus, click 동작
5. **접근성**: ARIA 속성, 키보드 네비게이션
6. **Edge Cases**: 텍스트 오버플로, 로딩 상태 등
7. **사용 예시**: 코드 스니펫

## Phase 5: Verification — 상세

### 자동 검증 항목

- [ ] TypeScript 컴파일 에러 없음
- [ ] ESLint/Prettier 통과
- [ ] 모든 Props에 타입 정의
- [ ] 기본 접근성 속성 (role, aria-label)
- [ ] 토큰 참조 유효성 (정의되지 않은 토큰 없음)

### 수동 검증 항목 (체크리스트)

- [ ] Figma 디자인과 시각적 일치
- [ ] 반응형 동작 확인
- [ ] 인터랙션 상태 동작 확인
- [ ] 다크모드 대응 (해당 시)
- [ ] 브라우저 호환성
