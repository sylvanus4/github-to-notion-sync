---
name: kwp-operations-risk-assessment
description: >-
  Identify, assess, and mitigate operational risks. Trigger with "what are the
  risks", "risk assessment", "risk register", "what could go wrong", or when the
  user is evaluating risks associated with a project, vendor, process, or
  decision. Do NOT use for this project's security threat modeling or
  vulnerability assessment — prefer security-expert skill. Korean triggers:
  "보안", "스킬", "모델".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Risk Assessment

Systematically identify, assess, and plan mitigations for operational risks.

## Before You Start

Before assessing risks, ask the user to clarify (use AskQuestion):

1. **Scope** — What are we assessing? (project, vendor, process, decision, or system change)
2. **Risk domain** — Operational, financial, technical, regulatory, reputational, or all?
3. **Context** — Timeline, stakeholders, and any known concerns or prior incidents?

DO NOT produce a generic risk register. Tailor the assessment to the specific scope and domain.

## Risk Assessment Matrix

| | Low Impact | Medium Impact | High Impact |
|---|-----------|---------------|-------------|
| **High Likelihood** | Medium | High | Critical |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Low | Low | Medium |

## Risk Categories

- **Operational**: Process failures, staffing gaps, system outages
- **Financial**: Budget overruns, vendor cost increases, revenue impact
- **Compliance**: Regulatory violations, audit findings, policy breaches
- **Strategic**: Market changes, competitive threats, technology shifts
- **Reputational**: Customer impact, public perception, partner relationships
- **Security**: Data breaches, access control failures, third-party vulnerabilities

## Risk Register Format

For each risk, document:
- **Description**: What could happen
- **Likelihood**: High / Medium / Low
- **Impact**: High / Medium / Low
- **Risk Level**: Critical / High / Medium / Low
- **Mitigation**: What we're doing to reduce likelihood or impact
- **Owner**: Who is responsible for managing this risk
- **Status**: Open / Mitigated / Accepted / Closed

## Output

Produce a prioritized risk register with specific, actionable mitigations. Focus on risks that are controllable and material.

## Examples

### Example 1: Typical request

**User says:** "I need help with operations risk assessment"

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
