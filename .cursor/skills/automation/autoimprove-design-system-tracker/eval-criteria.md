# Eval Criteria: design-system-tracker

## Binary Evals

EVAL 1: Change Detection
Question: 디자인 시스템 변경사항을 유형별로 분류하여 리포트하는가?
Pass condition: 신규 추가/수정/삭제/이름 변경 유형으로 분류된 변경 목록
Fail condition: 변경 유형 미분류, 또는 변경사항 미감지

EVAL 2: Impact Rating
Question: 각 변경에 영향도 등급(Critical/High/Medium/Low)을 부여하는가?
Pass condition: 모든 변경 항목에 영향도 등급 + 근거 명시
Fail condition: 영향도 미부여, 또는 근거 없는 등급

EVAL 3: PRD Mismatch Detection
Question: PRD 제공 시 기획-디자인 불일치를 최소 1건 이상 식별하는가?
Pass condition: 구체적 불일치 항목 (컴포넌트/상태/인터랙션 수준)
Fail condition: "모두 일치" (실제 불일치 존재 시), 또는 불일치 항목 없음

EVAL 4: Action Items
Question: 변경에 따른 구체적 액션 아이템을 생성하는가?
Pass condition: 기획 업데이트/개발 반영/확인 필요 카테고리의 액션 리스트
Fail condition: 액션 아이템 없음, 또는 모호한 액션

## Test Scenarios

1. "이번 주 디자인 시스템 변경사항 정리해줘" (Figma URL 제공)
2. "PRD와 디자인 싱크 맞는지 확인해줘" (Figma + Notion URL)
3. "색상 토큰 변경 영향 분석해줘"
4. "버튼 컴포넌트 variant 변경 추적해줘"
