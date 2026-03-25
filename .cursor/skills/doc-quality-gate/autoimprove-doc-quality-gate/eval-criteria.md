# Eval Criteria: doc-quality-gate

## Binary Evals

EVAL 1: Seven-Dimension Scoring
Question: Does the report score all 7 weighted dimensions with numeric values (0-100)?
Pass condition: All 7 dimensions present with individual scores, weights, and a weighted total
Fail condition: Dimensions missing, or scores not numeric, or weights not applied

EVAL 2: Grade and Verdict
Question: Does the report assign a letter grade (A-D) and a clear verdict (APPROVED/NEEDS REVISION)?
Pass condition: Grade and verdict present, consistent with the scoring formula
Fail condition: No grade, no verdict, or grade contradicts the calculated score

EVAL 3: Finding Severity
Question: Is every finding classified with severity (Critical/High/Medium/Low)?
Pass condition: Each finding has a severity label and findings are grouped or sorted by severity
Fail condition: Findings listed without severity labels

EVAL 4: Actionable Recommendations
Question: Does every NEEDS REVISION finding include a specific, implementable recommendation?
Pass condition: Each revision finding has a concrete action (add section X, clarify term Y, add state Z)
Fail condition: Findings describe problems without suggesting specific fixes

EVAL 5: Source Document Faithfulness
Question: Does the report cite specific sections/pages from the source document for each finding?
Pass condition: Every finding references the exact location in the reviewed document
Fail condition: Findings make claims without pointing to where in the document the issue was found

## Test Scenarios

1. "이 PRD 문서의 품질을 점검해줘"
2. "Run a quality gate on this feature specification"
3. "이 정책 문서의 완전성과 일관성을 검사해줘"
4. "Check this design spec for missing sections and edge case coverage"
5. "기획서 품질 게이트를 실행하고 A-D 등급을 매겨줘"
