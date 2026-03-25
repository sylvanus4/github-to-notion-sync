# Eval Criteria: prd-cascade-sync

## Binary Evals

EVAL 1: Dependency Graph Generated
Question: Does the output include a visual dependency graph (Mermaid or equivalent) showing the affected nodes?
Pass condition: A rendered or renderable dependency diagram showing source change and downstream nodes
Fail condition: No dependency visualization, or only text-based listing without graph structure

EVAL 2: Modification Suggestions Specific
Question: Does each modification suggestion specify the exact section and content to change in the downstream node?
Pass condition: Each suggestion names the target node, section, current text, and proposed change
Fail condition: Vague suggestions like "update the related section" without specifics

EVAL 3: Impact Level Correct
Question: Is each downstream node assigned an impact level (High/Medium/Low) with justification?
Pass condition: Every affected node has an impact label with a one-line rationale
Fail condition: Impact levels missing or assigned without explanation

EVAL 4: Human Review Gate
Question: Does the output clearly indicate which modifications require human approval vs can be auto-applied?
Pass condition: Each suggestion marked as "auto-apply" or "needs review" with the reason
Fail condition: All suggestions treated the same without distinguishing review needs

## Test Scenarios

1. "PRD의 스토리지 요구사항이 변경됐어 — 연쇄 수정을 제안해줘"
2. "The pricing tier section changed — cascade sync to dependent nodes"
3. "API 스펙이 변경됐으니 관련 PRD 노드를 업데이트해줘"
4. "Monitor this PRD pipeline for changes and suggest cascading updates"
