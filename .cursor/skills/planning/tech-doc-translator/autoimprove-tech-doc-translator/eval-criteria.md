# Eval Criteria: tech-doc-translator

## Binary Evals

EVAL 1: Planning Implications Included
Question: Does the output contain a dedicated "기획 시사점" or planning implications section?
Pass condition: Explicit section connecting technical content to planning decisions, constraints, or opportunities
Fail condition: Only restates technical content without business/planning implications

EVAL 2: Jargon Elimination
Question: Is the output free of unexplained technical jargon (all technical terms either replaced or glossary-defined)?
Pass condition: Every technical term is either simplified in-line or listed in a glossary with plain-language explanation
Fail condition: Technical terms used without explanation or glossary entry

EVAL 3: State and Constraint Extraction
Question: Does the output extract and present key states, constraints, and limitations from the technical document?
Pass condition: States/constraints presented in a structured format (table or bullet list) with user-impact notes
Fail condition: No structured extraction of states or constraints

EVAL 4: Audience Appropriateness
Question: Could a non-technical planner read the output without needing additional clarification from an engineer?
Pass condition: Content is self-contained with all necessary context for understanding
Fail condition: Requires engineering background to understand key sections

## Test Scenarios

1. "이 Kubernetes HPA 설정 문서를 기획자가 이해할 수 있게 설명해줘"
2. "Explain this API rate-limiting technical spec for the planning team"
3. "이 클라우드 네트워크 아키텍처 문서의 기획 시사점을 정리해줘"
4. "Translate this database migration plan into non-technical language for stakeholders"
