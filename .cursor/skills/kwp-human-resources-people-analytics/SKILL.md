---
name: kwp-human-resources-people-analytics
description: >-
  Analyze workforce data — attrition, engagement, diversity, and productivity.
  Trigger with "attrition rate", "turnover analysis", "diversity metrics",
  "engagement data", "retention risk", or when the user wants to understand
  workforce trends from HR data. Do NOT use for tasks outside the human domain.
  Korean triggers: "분석", "데이터".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# People Analytics

Analyze workforce data to surface trends, risks, and opportunities.

## Key Metrics

### Retention
- Overall attrition rate (voluntary + involuntary)
- Regrettable attrition rate
- Average tenure
- Flight risk indicators

### Diversity
- Representation by level, team, and function
- Pipeline diversity (hiring funnel by demographic)
- Promotion rates by group
- Pay equity analysis

### Engagement
- Survey scores and trends
- eNPS (Employee Net Promoter Score)
- Participation rates
- Open-ended feedback themes

### Productivity
- Revenue per employee
- Span of control efficiency
- Time to productivity for new hires

## Approach

1. Understand what question they're trying to answer
2. Identify the right data (upload, paste, or pull from BambooHR)
3. Analyze with appropriate statistical methods
4. Present findings with context and caveats
5. Recommend specific actions based on data

## Examples

### Example 1: Typical request

**User says:** "I need help with human resources people analytics"

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