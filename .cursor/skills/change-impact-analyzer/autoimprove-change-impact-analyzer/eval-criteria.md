# Eval Criteria: change-impact-analyzer

## Binary Evals

EVAL 1: Dependency Graph Completeness
Question: Does the output include a dependency graph (Mermaid or table) showing all affected downstream nodes?
Pass condition: Visual or tabular graph with named nodes, relationship types, and cascade direction
Fail condition: No graph, or only lists some affected areas without showing dependencies

EVAL 2: Risk Assessment with Criteria
Question: Does each impacted node have a risk level (Low/Med/High) based on the criteria in references/impact-criteria.md?
Pass condition: Risk levels assigned using concrete signals (user count, data integrity, SLA) not just intuition
Fail condition: Risk levels without criteria backing, or criteria not applied consistently

EVAL 3: Communication Checklist
Question: Does the output include a stakeholder communication checklist with named teams/channels?
Pass condition: Specific teams listed with notification channels and timing recommendations
Fail condition: Generic "notify stakeholders" without specifying who, how, or when

EVAL 4: Boundary Respect
Question: Does the analysis stay in prediction mode (pre-change) without attempting to apply changes?
Pass condition: Output is analysis and recommendations only — no attempt to modify documents or code
Fail condition: Skill tries to auto-apply changes (that's prd-cascade-sync's job)

## Test Scenarios

1. "스토리지 할당량 정책 변경 시 영향 분석해줘"
2. "Predict the impact of changing the API authentication method"
3. "이 디자인 컴포넌트 변경의 하위 영향도를 예측해줘"
4. "Analyze downstream impact if we change the pricing tier structure"
