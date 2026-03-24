# spec-quality-gate Eval Criteria

## Binary Evals (Yes/No)

### EVAL 1: Critical 이슈 정확 감지
Question: 필수 섹션(화면 개요, 기능 목록, 상태별 화면)이 없는 기획서에서 Critical 이슈를 정확히 감지하는가?
Pass condition: 누락된 필수 섹션마다 Critical 심각도로 보고
Fail condition: 필수 섹션 누락을 감지하지 못하거나 Medium/Low로 분류

### EVAL 2: False Positive 제어
Question: 완전한 기획서(모든 섹션 존재, 상태 정의 완료)에서 Critical/High를 오탐하지 않는가?
Pass condition: 완전한 기획서에 Critical 0건, High 0건
Fail condition: 완전한 기획서에 Critical 또는 High가 1건 이상

### EVAL 3: 리포트 형식 일관
Question: 품질 리포트가 Summary + Critical Issues + Passed Checks 구조를 따르는가?
Pass condition: 3개 섹션이 모두 존재하며, Summary에 판정(PASS/FAIL)이 명시
Fail condition: 구조가 다르거나 PASS/FAIL 판정 없음

### EVAL 4: 상태 커버리지 정확 판정
Question: 상태별 화면에서 loading만 있고 error/empty/success가 없을 때 정확히 누락을 보고하는가?
Pass condition: 누락된 상태(error, empty, success)를 구체적으로 명시
Fail condition: "상태 정의 불완전" 같은 모호한 보고

### EVAL 5: PASS/FAIL 판정 정확
Question: Critical 0건이면 PASS, Critical 1건 이상이면 FAIL로 정확히 판정하는가?
Pass condition: 판정 기준이 정확히 적용됨
Fail condition: Critical이 있는데 PASS, 또는 Critical이 없는데 FAIL

## Test Inputs

### Input 1: 완전한 기획서 (PASS 기대)
모든 섹션 포함, 상태 4/4 정의, 예외 5건, 사용자 플로우 2개

### Input 2: 불완전한 기획서 (FAIL 기대)
화면 개요만 있고 나머지 섹션 없음

### Input 3: 부분 완성 기획서 (경계 케이스)
필수 섹션 있지만 상태 2/4만 정의, 예외 1건

## Baseline Configuration
- Runs per experiment: 5
- Max score: 25 (5 evals × 5 runs)
- Budget cap: 8 experiments
