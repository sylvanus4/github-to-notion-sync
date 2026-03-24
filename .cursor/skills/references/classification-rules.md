# TDS 변경 분류 규칙

## 변경 유형 판단 매트릭스

커밋의 파일 상태와 커밋 메시지를 조합하여 변경 유형을 결정한다.

### 1차 판단: 파일 상태 (Git status)

| Git Status | 기본 유형 |
|------------|----------|
| `added` | 신규 |
| `modified` | 수정 |
| `removed` | 삭제 |
| `renamed` | 수정 (이동 명시) |

### 2차 판단: 커밋 메시지 키워드 오버라이드

파일 상태가 `modified`인 경우, 커밋 메시지 키워드로 세분화한다:

| 키워드 패턴 | 오버라이드 유형 |
|------------|---------------|
| `refactor`, `리팩토링`, `리팩터`, `restructure` | 리팩토링 |
| `style`, `css`, `스타일`, `color`, `색상`, `font`, `폰트`, `spacing` | 스타일 |
| `a11y`, `accessibility`, `접근성`, `aria`, `sr-only`, `focus` | 접근성 |
| `fix`, `bug`, `수정`, `hotfix`, `패치` | 버그수정 |
| `perf`, `performance`, `최적화`, `optimize` | 성능 |
| `docs`, `문서`, `주석`, `comment`, `storybook` | 문서화 |
| `test`, `테스트`, `spec` | 테스트 |

### 3차 판단: 변경 파일 확장자

| 파일 패턴 | 힌트 |
|----------|------|
| `*.css`, `*.scss`, `*.module.css` | 스타일 변경 가능성 높음 |
| `*.test.*`, `*.spec.*`, `*.stories.*` | 테스트/문서화 |
| `*.md`, `*.mdx` | 문서화 |
| `index.ts`, `index.js` (export만 변경) | 리팩토링 |

## 변경 의도 추론 프롬프트

커밋 메시지와 diff를 기반으로 한국어 1줄 요약을 생성할 때 사용한다:

```
아래 커밋 메시지와 코드 변경 사항을 읽고, 디자이너가 이 변경을 한 이유를
한국어 1줄(30자 이내)로 요약하세요.

- 기술 용어보다 디자인 관점의 표현을 사용하세요
- "~하기 위해", "~을 개선", "~을 추가" 형태로 작성하세요
- 코드 구현 세부사항이 아닌 사용자/디자인 관점의 변경 이유를 작성하세요

커밋 메시지: {commit_message}
변경 파일: {changed_files}
Diff 요약: {diff_summary}
```

## 컴포넌트명 추출 규칙

디렉토리 경로에서 컴포넌트명을 추출하는 규칙:

1. `--path` 직하 1-depth 디렉토리명을 컴포넌트명으로 사용
   - `src/components/Button/Button.tsx` → `Button`
   - `src/components/Modal/hooks/useModal.ts` → `Modal`

2. 파일명이 디렉토리명과 동일한 경우 해당 파일이 메인 컴포넌트
   - `Button/Button.tsx` → 메인 컴포넌트 파일

3. 하위 파일은 모두 부모 컴포넌트에 귀속
   - `Button/ButtonGroup.tsx` → `Button` 컴포넌트의 하위 변경

4. 공용 파일 (여러 컴포넌트에 걸침):
   - `src/components/index.ts` → "공용 Export"로 분류
   - `src/tokens/*` → "디자인 토큰"으로 분류
   - `src/utils/*` → "유틸리티"로 분류
