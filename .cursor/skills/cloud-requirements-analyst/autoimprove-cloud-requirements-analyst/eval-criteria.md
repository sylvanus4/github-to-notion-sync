# Eval Criteria: cloud-requirements-analyst

## Binary Evals

EVAL 1: HARD-GATE Enforcement
Question: 필수 수집 항목(기능 목록, 사용자 규모, 성능, 데이터, 일정) 미확보 시 Phase 2 진행을 차단하는가?
Pass condition: 필수 항목 누락 시 사용자에게 질문 또는 기획안에서 추출 시도
Fail condition: 필수 항목 없이 바로 기술 분석 진행

EVAL 2: Feasibility Scoring
Question: 기능별 현실성 점수(1-5)를 부여하고 근거를 명시하는가?
Pass condition: 각 기능에 5점 척도 점수 + 기술적 근거 + 종합 점수
Fail condition: 점수 없음, 또는 근거 없는 점수

EVAL 3: Risk Matrix
Question: 리스크를 확률×영향도 매트릭스로 분류하는가?
Pass condition: Critical/High/Medium/Low 등급 + 완화 전략
Fail condition: 리스크 분류 없음, 또는 등급만 있고 완화 전략 없음

EVAL 4: Tech Team Confirmation List
Question: 기술팀에 반드시 확인해야 할 항목을 별도 섹션으로 정리하는가?
Pass condition: [기술팀 확인 필요] 항목 목록 + 확인 사유
Fail condition: 기술팀 확인 항목 없음 (AI가 모든 것을 확정적으로 판단)

EVAL 5: Alternative Proposals
Question: 현실성 낮은 요구사항에 대한 실현 가능한 대안을 제시하는가?
Pass condition: 점수 1-2 항목에 대안 기술/축소 버전/단계적 구현 제안
Fail condition: "불가능합니다"만 제시, 대안 없음

## Test Scenarios

1. "실시간 대시보드 기획안 기술 타당성 평가해줘" (기획안 직접 제공)
2. "마켓플레이스 전체 기획안 기술 검토" (Notion URL)
3. "채팅 기능 요구사항 수집해줘" (요구사항 없이 빈 시작)
4. "기존 모놀리스에 API Gateway 추가 기획안 평가" (기존 아키텍처 정보 포함)
5. "AWS 기반 서버리스 백엔드 기획안 비용 검토"
