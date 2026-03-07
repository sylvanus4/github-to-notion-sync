---
name: kwp-operations-risk-assessment
description: Identify, assess, and mitigate operational risks. Trigger with "what are the risks", "risk assessment", "risk register", "what could go wrong", or when the user is evaluating risks associated
  with a project, vendor, process, or decision. Do NOT use for this project's security threat modeling or vulnerability assessment — prefer security-expert skill.
metadata:
  author: anthropic-kwp
  version: 1.0.0
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
