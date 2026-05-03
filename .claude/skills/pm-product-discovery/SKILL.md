---
name: pm-product-discovery
description: Product discovery workflows — ideation, assumption testing, Opportunity Solution Trees, interview synthesis, feature prioritization, and experiment design.
arguments: [workflow, topic]
---

Run product discovery workflow `$workflow` on `$topic`.

## Workflows

| Workflow | Description |
|----------|-------------|
| brainstorm | Divergent ideation with categorization |
| assumptions | Identify and prioritize risky assumptions |
| ost | Build Opportunity Solution Tree |
| interview-script | Generate customer interview script |
| interview-synthesis | Synthesize interview notes into insights |
| prioritize | RICE/ICE/MoSCoW feature prioritization |
| feature-requests | Analyze and cluster feature requests |
| experiment | Design validation experiments |

## Output

Structured Korean document with:
1. Workflow-specific deliverable
2. Confidence levels per insight
3. Next steps and validation plan
4. Stakeholder discussion points

## Based On

Teresa Torres (Continuous Discovery Habits) and Marty Cagan (Inspired) frameworks.

## Rules

- Separate user problems from proposed solutions
- Test assumptions before building features
- Minimum 3 alternatives before selecting an approach
