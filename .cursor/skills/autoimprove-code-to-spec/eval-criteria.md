# Eval Criteria: code-to-spec

## Binary Evals

EVAL 1: State Extraction
Question: 코드에서 상태값(State)을 정확히 추출하여 상태 다이어그램을 생성하는가?
Pass condition: 상태 변수, 전이 로직이 식별되고 mermaid stateDiagram 포함
Fail condition: 상태값 미추출, 또는 상태 다이어그램 없음

EVAL 2: Edge Case Identification
Question: 예외 처리 코드에서 Edge Case를 3개 이상 식별하는가?
Pass condition: try-catch, validation, error boundary에서 최소 3개 Edge Case 추출
Fail condition: Edge Case 3개 미만 또는 예외 처리 코드 무시

EVAL 3: Confirmation Tags
Question: 코드에서 의도가 불명확한 항목에 [확인 필요] 태그를 부여하는가?
Pass condition: 매직 넘버, TODO 주석, 불명확한 조건에 [확인 필요] 태그 존재
Fail condition: [확인 필요] 태그 없음 (추측으로 의도 채움)

EVAL 4: Structured Output
Question: 출력이 역기획서 템플릿 구조(7개 섹션)를 따르는가?
Pass condition: 개요, 기능 명세, 상태 정의, 예외 케이스, 비즈니스 규칙, 데이터 모델, 확인 필요 항목 섹션 존재
Fail condition: 비정형 텍스트, 또는 주요 섹션 3개 이상 누락

EVAL 5: No Hallucination
Question: 코드에 없는 기능이나 동작을 추측하여 추가하지 않았는가?
Pass condition: 모든 기술된 기능/동작이 코드에서 직접 추출 가능
Fail condition: 코드에 근거 없는 기능 설명 포함

## Test Scenarios

1. React Checkout 컴포넌트 디렉토리 분석 (상태+예외+비즈니스 로직)
2. REST API 컨트롤러 파일 분석 (엔드포인트+인증+에러 코드)
3. Vue.js 대시보드 페이지 분석 (조건부 렌더링+라우팅)
4. GitHub PR URL의 변경 파일 분석
5. 비즈니스 로직만 있는 서비스 레이어 분석 (UI 없음)
