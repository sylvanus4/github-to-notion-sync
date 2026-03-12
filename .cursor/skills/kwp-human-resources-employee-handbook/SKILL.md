---
name: kwp-human-resources-employee-handbook
description: >-
  Answer questions about company policies, benefits, and procedures. Trigger
  with "what's our policy on", "how does PTO work", "benefits question",
  "expense policy", "remote work policy", or any question about company rules,
  perks, or procedures. Do NOT use for tasks outside the human domain.
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Employee Handbook

Answer employee questions about policies, benefits, and procedures by searching connected knowledge bases or using provided handbook content.

## Common Topics

- **PTO and Leave**: Vacation, sick leave, parental leave, bereavement, sabbatical
- **Benefits**: Health insurance, dental, vision, 401k, HSA/FSA, wellness
- **Compensation**: Pay schedule, bonus timing, equity vesting, expense reimbursement
- **Remote Work**: WFH policy, remote locations, equipment stipend, coworking
- **Travel**: Booking policy, per diem, expense reporting, approval process
- **Conduct**: Code of conduct, harassment policy, conflicts of interest
- **Growth**: Professional development budget, conference policy, tuition reimbursement

## How to Answer

1. Search Notion for the relevant policy document
2. Provide a clear, plain-language answer
3. Quote the specific policy language
4. Note any exceptions or special cases
5. Point to who to contact for edge cases

## Important

- Always cite the source document and section
- If no policy is found, say so clearly rather than guessing
- For legal or compliance questions, recommend consulting HR or legal directly

## Examples

### Example 1: Typical request

**User says:** "I need help with human resources employee handbook"

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