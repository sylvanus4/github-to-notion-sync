---
name: kwp-operations-resource-planning
description: >-
  Plan and optimize resource allocation. Trigger with "resource planning",
  "capacity", "utilization", "staffing plan", "who should work on what", "we're
  stretched thin", or when the user needs help allocating people, budget, or
  time across projects and teams. Do NOT use for tasks outside the operations
  domain. Korean triggers: "최적화", "계획".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Resource Planning

Help plan and optimize resource allocation across projects and teams.

## Planning Dimensions

### People
- Available headcount and skills
- Current allocation and utilization
- Planned hires and timeline
- Contractor and vendor capacity

### Budget
- Operating budget by category
- Project-specific budgets
- Variance tracking
- Forecast vs. actual

### Time
- Project timelines and dependencies
- Critical path analysis
- Buffer and contingency planning
- Deadline management

## Utilization Targets

| Role Type | Target Utilization | Notes |
|-----------|-------------------|-------|
| IC / Specialist | 75-80% | Leave room for reactive work and growth |
| Manager | 60-70% | Management overhead, meetings, 1:1s |
| On-call / Support | 50-60% | Interrupt-driven work is unpredictable |

## Common Pitfalls

- Planning to 100% utilization (no buffer for surprises)
- Ignoring meeting load and context-switching costs
- Not accounting for vacation, holidays, and sick time
- Treating all hours as equal (creative work ≠ admin work)

## Output

Produce allocation plans, utilization dashboards, scenario analyses (what if we hire / don't hire / deprioritize), and staffing recommendations.

## Examples

### Example 1: Typical request

**User says:** "I need help with operations resource planning"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |
