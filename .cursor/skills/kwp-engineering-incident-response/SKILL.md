---
name: kwp-engineering-incident-response
description: >-
  Triage and manage production incidents. Trigger with "we have an incident",
  "production is down", "something is broken", "there's an outage", "SEV1", or
  when the user describes a production issue needing immediate response. Do NOT
  use for this project's infrastructure or deployment concerns — prefer
  sre-devops-expert skill. Korean triggers: "인시던트", "장애 대응".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Incident Response

Guide incident response from detection through resolution and postmortem.

## Severity Classification

| Level | Criteria | Response Time |
|-------|----------|---------------|
| SEV1 | Service down, all users affected | Immediate, all-hands |
| SEV2 | Major feature degraded, many users affected | Within 15 min |
| SEV3 | Minor feature issue, some users affected | Within 1 hour |
| SEV4 | Cosmetic or low-impact issue | Next business day |

## Response Framework

1. **Triage**: Classify severity, identify scope, assign incident commander
2. **Communicate**: Status page, internal updates, customer comms if needed
3. **Mitigate**: Stop the bleeding first, root cause later
4. **Resolve**: Implement fix, verify, confirm resolution
5. **Postmortem**: Blameless review, 5 whys, action items

## Communication Templates

Provide clear, factual updates at regular cadence. Include: what's happening, who's affected, what we're doing, when the next update is.

## Postmortem Format

Blameless. Focus on systems and processes. Include timeline, root cause analysis (5 whys), what went well, what went poorly, and action items with owners and due dates.

## Examples

### Example 1: Typical request

**User says:** "I need help with engineering incident response"

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
