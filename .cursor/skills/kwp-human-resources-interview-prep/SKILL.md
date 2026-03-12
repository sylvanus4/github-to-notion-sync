---
name: kwp-human-resources-interview-prep
description: >-
  Create structured interview plans with competency-based questions and
  scorecards. Trigger with "interview plan for", "interview questions for", "how
  should we interview", "scorecard for", or when the user is preparing to
  interview candidates. Do NOT use for tasks outside the human domain. Korean
  triggers: "생성", "계획".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Interview Prep

Create structured interview plans to evaluate candidates consistently and fairly.

## Before You Start

Before creating an interview plan, ask the user to clarify (use AskQuestion):

1. **Role** — What position is this for? (title, level, team)
2. **Key competencies** — What 3-5 skills or behaviors matter most for this role?
3. **Interview format** — Phone screen, technical, behavioral, panel, or full loop?
4. **Candidate stage** — First round, final round, or specific competency deep-dive?

DO NOT generate questions until aligned on the role and competencies. Generic interview questions waste everyone's time.

## Interview Design Principles

1. **Structured**: Same questions for all candidates in the role
2. **Competency-based**: Map questions to specific skills and behaviors
3. **Evidence-based**: Use behavioral and situational questions
4. **Diverse panel**: Multiple perspectives reduce bias
5. **Scored**: Use rubrics, not gut feelings

## Interview Plan Components

### Role Competencies
Define 4-6 key competencies for the role (e.g., technical skills, communication, leadership, problem-solving).

### Question Bank
For each competency, provide:
- 2-3 behavioral questions ("Tell me about a time...")
- 1-2 situational questions ("How would you handle...")
- Follow-up probes

### Scorecard
Rate each competency on a consistent scale (1-4) with clear descriptions of what each level looks like.

### Debrief Template
Structured format for interviewers to share findings and make a decision.

## Output

Produce a complete interview kit: panel assignment (who interviews for what), question bank by competency, scoring rubric, and debrief template.

## Examples

### Example 1: Typical request

**User says:** "I need help with human resources interview prep"

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