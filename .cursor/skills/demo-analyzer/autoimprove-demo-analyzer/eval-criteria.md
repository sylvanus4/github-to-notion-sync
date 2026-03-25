# Eval Criteria: demo-analyzer

## Binary Evals

EVAL 1: Screen Inventory Completeness
Question: Does the output include a numbered screen inventory with all navigable pages/states discovered?
Pass condition: Numbered list of screens with descriptive names and navigation paths
Fail condition: Screens mentioned ad-hoc in text without a consolidated inventory

EVAL 2: State Matrix Coverage
Question: Does the output include a structured state matrix covering normal, loading, error, and empty states per screen?
Pass condition: Matrix or table with at least 3 state types per major screen (normal, error, one edge state)
Fail condition: States described only in prose, or matrix covers only happy-path states

EVAL 3: Edge Case Identification
Question: Does the output identify at least 3 edge cases or boundary conditions per major feature?
Pass condition: Specific edge cases listed with trigger conditions and observed behavior
Fail condition: No edge cases mentioned, or only generic "error handling" without specifics

EVAL 4: Screenshot Evidence
Question: Does the analysis reference specific visual evidence (screenshot descriptions or URL states)?
Pass condition: Key findings backed by visual state descriptions or captured URL states
Fail condition: Assertions about UI without any visual reference or state documentation

EVAL 5: Open Questions Specificity
Question: Are open questions specific and actionable (not generic "needs clarification")?
Pass condition: Each open question references a specific screen/state and asks about a concrete behavior
Fail condition: Vague questions like "need to check more" or "verify with team"

## Test Scenarios

1. "Analyze the demo at localhost:3000 for the cloud VM management feature"
2. "Walk through the staging URL and extract all states for the billing flow"
3. "Analyze this running demo and produce a planning-ready specification"
4. "Extract all user flows and edge cases from the authentication demo"
