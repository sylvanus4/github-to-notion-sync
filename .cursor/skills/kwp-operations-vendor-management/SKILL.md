---
name: kwp-operations-vendor-management
description: >-
  Evaluate, compare, and manage vendor relationships. Trigger with "evaluate
  this vendor", "compare vendors", "vendor review", "should we renew", "RFP", or
  when the user is making procurement or vendor decisions. Do NOT use for tasks
  outside the operations domain. Korean triggers: "리뷰", "출시".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Vendor Management

Help evaluate, compare, and manage vendor relationships.

## Evaluation Framework

### Cost Analysis
- Total cost of ownership (not just license fees)
- Implementation and migration costs
- Training and onboarding costs
- Ongoing support and maintenance
- Exit costs (data migration, contract termination)

### Risk Assessment
- Vendor financial stability
- Security and compliance posture
- Concentration risk (single vendor dependency)
- Contract lock-in and exit terms
- Business continuity and disaster recovery

### Performance Metrics
- SLA compliance
- Support response times
- Uptime and reliability
- Feature delivery cadence
- Customer satisfaction

## Comparison Matrix

When comparing vendors, produce a side-by-side matrix covering: pricing, features, integrations, security, support, contract terms, and references.

## Output

Provide a clear recommendation with supporting evidence. Always flag risks and negotiation leverage points.

## Examples

### Example 1: Typical request

**User says:** "I need help with operations vendor management"

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
