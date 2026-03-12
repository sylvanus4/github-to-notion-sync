---
name: kwp-operations-process-optimization
description: >-
  Analyze and improve business processes. Trigger with "this process is slow",
  "how can we improve", "streamline this workflow", "too many steps",
  "bottleneck", or when the user describes an inefficient process they want to
  fix. Do NOT use for tasks outside the operations domain. Korean triggers:
  "분석", "워크플로우", "수정".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Process Optimization

Analyze existing processes and recommend improvements.

## Analysis Framework

### 1. Map Current State
- Document every step, decision point, and handoff
- Identify who does what and how long each step takes
- Note manual steps, approvals, and waiting times

### 2. Identify Waste
- **Waiting**: Time spent in queues or waiting for approvals
- **Rework**: Steps that fail and need to be redone
- **Handoffs**: Each handoff is a potential point of failure or delay
- **Over-processing**: Steps that add no value
- **Manual work**: Tasks that could be automated

### 3. Design Future State
- Eliminate unnecessary steps
- Automate where possible
- Reduce handoffs
- Parallelize independent steps
- Add checkpoints (not gates)

### 4. Measure Impact
- Time saved per cycle
- Error rate reduction
- Cost savings
- Employee satisfaction improvement

## Output

Produce a before/after process comparison with specific improvement recommendations, estimated impact, and an implementation plan.

## Examples

### Example 1: Typical request

**User says:** "I need help with operations process optimization"

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