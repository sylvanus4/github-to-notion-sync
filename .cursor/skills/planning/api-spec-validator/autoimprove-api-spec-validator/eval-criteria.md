# Eval Criteria: api-spec-validator

## Binary Evals

EVAL 1: Endpoint Coverage
Question: Does the validation report cover all endpoints defined in the spec (not just a sample)?
Pass condition: Every endpoint in the spec document is represented in the gap report
Fail condition: Endpoints skipped or only a subset analyzed without stating scope limitations

EVAL 2: Gap Classification
Question: Is each gap classified by dimension (endpoint, schema, error code, auth, rate limit)?
Pass condition: Every gap labeled with at least one dimension from the validation taxonomy
Fail condition: Gaps listed without dimension classification

EVAL 3: Code Evidence
Question: Are discrepancies backed by specific code references (file, function, line)?
Pass condition: Each gap cites the code location where the deviation was found
Fail condition: Gaps described without pointing to the actual code

EVAL 4: Backlog-Ready Output
Question: Is the gap report structured so items can be directly added to a task backlog?
Pass condition: Each gap has a title, severity, spec reference, code reference, and suggested fix
Fail condition: Narrative-style report that requires restructuring for task creation

## Test Scenarios

1. "기획서의 API 스펙과 실제 코드를 대조 검증해줘"
2. "Validate the billing API implementation against the Swagger spec"
3. "Check if the user management endpoints match the Notion spec document"
4. "API 스펙 대비 구현 갭 리포트를 생성해줘"
