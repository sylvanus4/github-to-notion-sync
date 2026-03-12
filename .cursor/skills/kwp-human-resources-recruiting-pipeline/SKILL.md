---
name: kwp-human-resources-recruiting-pipeline
description: >-
  Track and manage recruiting pipeline stages. Trigger with "recruiting
  update", "candidate pipeline", "how many candidates", "hiring status", or when
  the user discusses sourcing, screening, interviewing, or extending offers. Do
  NOT use for tasks outside the human domain. Korean triggers: "채용", "인사 파이프라인", "후보자".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Recruiting Pipeline

Help manage the recruiting pipeline from sourcing through offer acceptance.

## Pipeline Stages

| Stage | Description | Key Actions |
|-------|-------------|-------------|
| Sourced | Identified and reached out | Personalized outreach |
| Screen | Phone/video screen | Evaluate basic fit |
| Interview | On-site or panel interviews | Structured evaluation |
| Debrief | Team decision | Calibrate feedback |
| Offer | Extending offer | Comp package, negotiation |
| Accepted | Offer accepted | Transition to onboarding |

## Metrics to Track

- **Pipeline velocity**: Days per stage
- **Conversion rates**: Stage-to-stage drop-off
- **Source effectiveness**: Which channels produce hires
- **Offer acceptance rate**: Offers extended vs. accepted
- **Time to fill**: Days from req open to offer accepted

## If ATS Connected

Pull candidate data automatically, update statuses, and track pipeline metrics in real time.

## Examples

### Example 1: Typical request

**User says:** "I need help with human resources recruiting pipeline"

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