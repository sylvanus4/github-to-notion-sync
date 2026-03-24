# TDS Timeline — Eval Criteria

## Binary Evals (pass/fail)

### EVAL 1: Component Extraction
Question: 변경된 파일 경로에서 컴포넌트명이 정확히 추출되었는가?
Pass condition: 모든 변경 파일이 올바른 컴포넌트에 귀속됨
Fail condition: 컴포넌트명 누락, 잘못된 매핑, 또는 경로 파싱 오류

### EVAL 2: Change Classification
Question: 각 커밋의 변경 유형(신규/수정/삭제/리팩토링/스타일/접근성)이 올바르게 분류되었는가?
Pass condition: 80% 이상의 커밋이 올바른 유형으로 분류됨
Fail condition: 일괄 "수정"으로 분류하거나 유형 판단 누락

### EVAL 3: Intent Summary
Question: 변경 의도 요약이 디자인 관점에서 작성되었는가?
Pass condition: 기술 구현 세부사항이 아닌 디자인/UX 관점 1줄 요약
Fail condition: "파일 수정", "코드 변경" 등 무의미한 요약 또는 코드 레벨 설명

### EVAL 4: Timeline Format
Question: 출력이 요청한 group-by 옵션에 맞는 타임라인 마크다운 형식인가?
Pass condition: 테이블 헤더, 날짜/작성자/유형/내용 컬럼, 요약 통계 포함
Fail condition: 비구조화된 텍스트, 테이블 형식 미준수, 요약 통계 누락

### EVAL 5: Delivery
Question: 지정한 출력 채널(markdown/notion/slack)로 올바르게 발행되었는가?
Pass condition: 파일 저장 또는 MCP 호출 완료
Fail condition: 출력 채널 무시, MCP 호출 오류

## Test Inputs

1. `--repo thaki/design-system --since 2026-03-01 --until 2026-03-24 --output markdown`
2. `--repo thaki/design-system --authors designer-a --group-by date`
3. `--repo thaki/design-system --output slack --channel C0123DESIGN`

## Max Score

5 evals x 5 runs = 25
