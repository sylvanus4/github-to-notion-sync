# PRD Template

Standard template for auto-generated PRDs.

## Document Header

```markdown
# [Feature Name] — PRD

## 문서 정보
| 항목 | 내용 |
|------|------|
| 작성자 | |
| 생성일 | YYYY-MM-DD |
| 소스 | [meeting transcript / slack thread / existing doc / manual] |
| 상태 | Draft / In Review / Approved |
| 버전 | 1.0 |
| 관련 PRD | [links to related PRDs] |
```

## Required Sections

### 1. 배경 및 목적

- 왜 이 기능이 필요한가?
- 어떤 사용자 문제를 해결하는가?
- 비즈니스 임팩트는?

### 2. 목표 및 성공 지표

| 목표 | 지표 | 현재 값 | 목표 값 | 측정 방법 |
|------|------|--------|--------|----------|
| | | | | |

### 3. 사용자 스토리

```
As a [user type],
I want to [action],
So that [benefit].

Acceptance Criteria:
- [ ] Given [context], when [action], then [result]
```

### 4. 기능 요구사항

Per requirement:
- 설명
- 상태 커버리지 매트릭스 (from state-edge-case-checklist)
- 관련 API (from code-to-spec / code-spec-comparator, if available)
- 디자인 컴포넌트 (from design system, if available)
- 우선순위 (Must / Should / Could / Won't)

### 5. 비기능 요구사항

| 카테고리 | 요구사항 | 기준 |
|----------|---------|------|
| 성능 | | |
| 보안 | | |
| 접근성 | | |
| 호환성 | | |

### 6. 제약사항 및 가정

- 기술적 제약
- 비즈니스 제약
- 전제 조건 (assumptions)

### 7. 정책 준수 사항

| 정책 ID | 정책명 | 반영 여부 | 반영 위치 |
|---------|-------|----------|----------|
| | | | |

### 8. 미결 사항

| # | 질문/이슈 | 담당자 | 기한 |
|---|----------|--------|------|
| | | | |

### 9. 참고 자료

- 소스 문서 링크
- 관련 API 문서
- 디자인 파일 링크
