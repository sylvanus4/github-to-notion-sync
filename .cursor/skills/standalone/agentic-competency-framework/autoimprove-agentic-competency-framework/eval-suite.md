# Eval Suite — agentic-competency-framework

## Test Inputs (5)

| ID | Input | Target Mode |
|----|-------|-------------|
| T1 | "Assess my agentic competencies" | Mode 1: Self-Assessment |
| T2 | "I want to explore competency 3 - task decomposition" | Mode 2: Skill Mapping (specific) |
| T3 | "Generate a 4-week development plan for my agentic skills" | Mode 3: Development Plan |
| T4 | "What are the 7 core agentic engineering competencies? Give me a quick overview" | Mode 2: Overview |
| T5 | "Help me get better at AI stuff" | Vague — should route to assessment or overview |

## Eval Criteria (5 binary checks)

### EVAL 1: Mode Recognition
Question: Does the agent correctly identify which mode (assess/map/plan) to execute based on the test input, without mixing unrelated modes?
Pass: The correct mode is selected and no unrelated mode workflow steps are mixed in.
Fail: Wrong mode selected, or multiple modes are triggered simultaneously when only one is appropriate.

### EVAL 2: Structured Output
Question: Does the output use structured formatting (tables, lists, or charts) rather than unstructured prose for competency data?
Pass: Output includes at least one table or structured list per competency discussed, consistent with the skill's table-based rubric format.
Fail: Output is entirely prose without structural elements, or competency data is presented as narrative paragraphs.

### EVAL 3: Specific Skill References
Question: Does the output recommend at least 3 specific, actually-existing project skills (from .cursor/skills/) with practice context?
Pass: At least 3 different skill names from the Competency-to-Skill Mapping table are mentioned with a brief practice focus description.
Fail: Fewer than 3 skills referenced, or fabricated skill names, or generic advice without naming specific skills.

### EVAL 4: Artifact Creation
Question: Does the output specify or create a concrete artifact with an explicit file path and format?
Pass: Mode 1 → HTML radar chart at output/competency/assessment-{date}.html; Mode 3 → markdown plan at output/competency/dev-plan-{date}.md; Mode 2 → structured presentation of skill chain. At least one artifact path is specified.
Fail: No artifact specification, or generic "output" without format/path.

### EVAL 5: Actionable Next Steps
Question: Does the output end with at least 2 concrete, immediately-executable next steps the user can take?
Pass: At least 2 specific actions like "run /simplify on your codebase to practice Evaluation" or "invoke prompt-architect with a vague request to practice Specification Accuracy."
Fail: Vague next steps like "continue practicing" or "learn more" or no next steps at all.

## Configuration

- Runs per experiment: 5
- Budget cap: 10 experiments
- Max score per run: 5 (one point per eval)
- Max total per experiment: 25 (5 runs × 5 evals)
