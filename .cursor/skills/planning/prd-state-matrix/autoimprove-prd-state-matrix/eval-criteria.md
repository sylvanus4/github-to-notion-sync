# Eval Criteria: prd-state-matrix

## Binary Evals

EVAL 1: Required Matrix Columns
Question: Does the state matrix contain all required columns from the template (Feature, State, Trigger, Display, Transition, Edge)?
Pass condition: Matrix table includes all column headers matching the reference template
Fail condition: Missing columns or using non-standard column names

EVAL 2: Edge Case Spec Traceability
Question: Is every edge case linked to a specific section or requirement in the source PRD?
Pass condition: Each edge case row cites a PRD section number, page reference, or requirement ID
Fail condition: Edge cases listed without any traceability to the source spec

EVAL 3: Priority Ratings
Question: Does every recommendation include a priority rating (High/Medium/Low)?
Pass condition: Each gap or recommendation has an explicit priority label with brief justification
Fail condition: Recommendations listed without priority or severity indication

EVAL 4: No Hallucinated States
Question: Are all states in the matrix either explicitly mentioned in the PRD or clearly marked as "[INFERRED]"?
Pass condition: Every state is tagged as [FROM_SPEC] or [INFERRED] with reasoning
Fail condition: States presented as fact that don't appear in the source PRD and aren't marked as inferred

## Test Scenarios

1. "이 PRD에서 상태값 매트릭스를 추출해줘"
2. "Extract the state matrix from this cloud storage management spec"
3. "이 기획서의 엣지 케이스를 보완해줘"
4. "Analyze this API spec PRD for missing state transitions"
