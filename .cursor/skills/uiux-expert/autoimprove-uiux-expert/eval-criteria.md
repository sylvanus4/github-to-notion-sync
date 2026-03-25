# Eval Criteria: uiux-expert

## Binary Evals

EVAL 1: Cross-Product Consistency Check
Question: Does the output identify and compare UI/UX patterns across multiple Thaki Cloud products (not just one)?
Pass condition: At least 2 products compared on common dimensions (layout, components, interaction patterns)
Fail condition: Analysis covers only a single product with no cross-product comparison

EVAL 2: Nielsen Heuristic Scoring
Question: Does the quality feedback module score against Nielsen's 10 usability heuristics with numeric ratings?
Pass condition: Each applicable heuristic scored with a 1-10 rating and one-line justification
Fail condition: Heuristics mentioned but not scored, or arbitrary non-heuristic criteria used

EVAL 3: Severity-Ranked Findings
Question: Are all UX issues classified with severity (Critical/Major/Minor) and prioritized?
Pass condition: Every finding has a severity label and issues are ordered by priority
Fail condition: Findings listed as a flat list without severity or priority ordering

EVAL 4: Actionable Sharing Materials
Question: Does the output produce materials suitable for direct use in the weekly design sharing meeting?
Pass condition: Output includes a structured summary with key findings, visual references, and action items
Fail condition: Raw analysis that would need significant reformatting for presentation

## Test Scenarios

1. "Review the settings page across Thaki Compute and Thaki Storage for UI consistency"
2. "Run a Nielsen heuristic evaluation on the dashboard design"
3. "Prepare UX review materials for this week's design sharing meeting"
4. "Check if the new feature design follows our established interaction patterns"
