# dev-planning-bridge Eval Criteria

## Binary Evals (Yes/No)

### EVAL 1: 파이프라인 순서 준수
Question: Phase 1(code-to-spec) → Phase 2(spec-quality-gate) 순서가 정확히 지켜졌는가?
Pass condition: 역기획서 생성 후 품질 점검이 수행됨 (로그에서 순서 확인)
Fail condition: 품질 점검 없이 바로 발행, 또는 순서 역전

### EVAL 2: Phase 2 Gate 동작
Question: Phase 2에서 Critical 이슈가 있을 때 자동 수정을 시도하는가?
Pass condition: Critical 감지 → 자동 수정 시도 → 재검증 수행
Fail condition: Critical을 무시하고 다음 Phase 진행

### EVAL 3: 선택 Phase 조건부 실행
Question: --skip-text 플래그가 있을 때 Phase 3(policy-text-generator)을 SKIP하는가?
Pass condition: Phase 3이 SKIP 처리되고 로그에 "SKIP" 표기
Fail condition: 플래그를 무시하고 Phase 3 실행

### EVAL 4: 최종 리포트 생성
Question: 파이프라인 완료 후 Pipeline Summary 테이블이 생성되는가?
Pass condition: 6개 Phase의 Status가 모두 표시된 요약 테이블 존재
Fail condition: 요약 없이 종료 또는 불완전한 요약

### EVAL 5: 산출물 경로 명시
Question: 최종 리포트에 생성된 파일의 경로가 명시되어 있는가?
Pass condition: 기획서 파일 경로가 `docs/specs/...` 형태로 표시
Fail condition: 경로 미표시

## Test Inputs

### Input 1: 최소 파이프라인
"src/pages/todos/ 역기획해줘" (Phase 1-2만 실행)

### Input 2: 전체 파이프라인
"오늘 작업한 코드 역기획해서 노션에 올려줘 --notion --slack"

### Input 3: 선택 스킵
"src/api/ 역기획해줘 --skip-text --skip-design"

## Baseline Configuration
- Runs per experiment: 3
- Max score: 15 (5 evals × 3 runs)
- Budget cap: 6 experiments
