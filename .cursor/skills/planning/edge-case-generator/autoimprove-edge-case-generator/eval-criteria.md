# Eval Criteria: edge-case-generator

## Binary Evals

EVAL 1: Multi-Dimension Coverage
Question: Does the matrix cover at least 5 of the 8 edge-case dimensions (states, boundaries, concurrency, errors, permissions, validation, network, cross-feature)?
Pass condition: At least 5 distinct dimensions represented with specific edge cases per dimension
Fail condition: Fewer than 5 dimensions covered, or dimensions listed without concrete edge cases

EVAL 2: Severity Accuracy
Question: Is each edge case assigned a severity level (P0-P3) that matches its actual impact?
Pass condition: P0 for data loss/security, P1 for core flow broken, P2 for degraded UX, P3 for cosmetic — correctly applied
Fail condition: Severity misclassified (e.g., cosmetic issue marked P0, data loss marked P3)

EVAL 3: Spec Section Traceability
Question: Is every edge case traceable to a specific section of the source document?
Pass condition: Each edge case cites the spec section, requirement, or flow it derives from
Fail condition: Edge cases presented without source traceability

EVAL 4: No Fabrication
Question: Are all edge cases plausible given the system described in the spec (no invented features or impossible states)?
Pass condition: Every edge case describes a scenario that could actually occur in the specified system
Fail condition: Edge cases reference features not in the spec or describe physically impossible scenarios

## Test Scenarios

1. "이 결제 플로우 PRD에서 엣지 케이스 매트릭스를 생성해줘"
2. "Generate edge cases from this cloud VM lifecycle management spec"
3. "Find missing boundary conditions in this API quota management PRD"
4. "이 사용자 인증 기획서에서 예외 상황을 도출해줘"
