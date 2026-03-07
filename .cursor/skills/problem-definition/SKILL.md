---
name: problem-definition
description: >-
  Guide users through a structured 5D framework (Describe, Decompose, Diagnose,
  Define, Document) to properly define problems before jumping to solutions.
  Produces a Problem Definition Document (PDD) with root cause hypotheses,
  stakeholder perspectives, and testable success criteria. Use when the user
  runs /define-problem, asks to "define the problem", "what's the real problem",
  "frame this problem", "problem statement", or "before we solve this". Do NOT
  use for code review (use simplify or deep-review), generating solutions (use
  diagnose), or project planning (use pm-execution).
metadata:
  author: thaki
  version: 1.0.0
---

# Problem Definition — 5D Framework

Accurate problem definition is the single highest-leverage activity in any project. The 75/25 rule: spend 75% of effort defining the problem (P-code), 25% on the solution (S-code). Most failures trace back to poorly defined problems, not poor solutions.

This skill applies a structured 5-phase process that challenges surface-level framing, decomposes complexity, and produces a testable problem statement.

## Usage

```
/define-problem                                # deep mode (default)
/define-problem quick                          # single-pass problem statement
/define-problem team                           # collaborative workshop template
/define-problem "API latency exceeds SLO"      # with initial problem description
/define-problem deep src/api/                  # deep mode scoped to a directory
```

## Scoping Modes

| Mode | Trigger | Output |
|------|---------|--------|
| `quick` | `/define-problem quick` | One-page problem statement (Steps 1, 4, 5 only) |
| `deep` (default) | `/define-problem` or `/define-problem deep` | Full 5D analysis with PDD |
| `team` | `/define-problem team` | Facilitation template with prompts for team workshops |

## Workflow

### Step 1: D1 — Describe (Capture Raw Symptoms)

Gather the initial situation from the user. Ask clarifying questions using a Socratic approach:

1. **What is happening?** — Observable symptoms, not interpretations
2. **When did it start?** — Timeline and triggering events
3. **Who is affected?** — Users, teams, systems
4. **What has been tried?** — Previous attempts and their outcomes

If the user provides a codebase context (file path, error message), also gather:
- Recent git changes: `git log --oneline -10` and `git diff --stat HEAD~5`
- Linter output: `ReadLints` on mentioned files
- Related documentation or issue threads

Record all raw observations without judgment.

### Step 2: D2 — Decompose (Break Apart)

Split the problem into independent sub-elements:

1. **Separate symptoms from causes** — Symptoms are what you observe; causes are why they happen
2. **Identify distinct sub-problems** — A "big problem" is often 2-3 smaller problems bundled together
3. **Map dependencies** — Which sub-elements block or influence others?

Apply the **Anti-Pattern Detector** at this stage:

| Anti-Pattern | Signal | Challenge Question |
|-------------|--------|--------------------|
| Symptom-as-Problem | Description only states observable effects | "What is causing this symptom?" |
| Solution-as-Problem | Description contains a proposed fix | "What problem does that solution address?" |
| Scope Bundling | Description covers multiple unrelated concerns | "Can this be split into independent problems?" |
| Vague Framing | No measurable impact or affected party stated | "Who is affected and how would we measure it?" |

### Step 3: D3 — Diagnose (Map Cause and Effect)

Analyze relationships between sub-elements:

1. **5 Whys** — For each symptom, ask "why?" iteratively until reaching a structural cause
2. **Multi-Perspective Analysis** — Examine the problem from at least 3 viewpoints:
   - **User/Customer**: How do they experience this? What do they lose?
   - **Engineering/System**: What technical constraint or failure drives this?
   - **Business/Organization**: What is the impact on goals, metrics, or resources?
3. **Hypothesis Formation** — State each potential root cause as a testable hypothesis:
   - Format: "If [cause], then we would observe [evidence]"
   - Assign confidence: High / Medium / Low

### Step 4: D4 — Define (Formulate the Problem Statement)

Synthesize findings into a precise problem statement:

1. **Write the statement** — One sentence that includes: who is affected, what the problem is, and why it matters
2. **Set boundaries** — Explicitly state what is in scope, out of scope, and what constraints exist
3. **Define success criteria** — Measurable outcomes that prove the problem is solved
4. **Validate against anti-patterns** — Re-check: is this still a symptom? a disguised solution? too broad?

A well-formed problem statement follows this template:
> "[Affected party] experiences [specific problem] when [context/trigger], resulting in [measurable impact]. This is caused by [root cause hypothesis]."

### Step 5: D5 — Document (Produce the PDD)

Generate the Problem Definition Document:

```
Problem Definition Document
============================
Title: [concise problem title]

1. Observed Symptoms
   - [symptom 1]
   - [symptom 2]

2. Decomposition
   - Sub-problem A: [description]
   - Sub-problem B: [description]
   - Dependencies: [A blocks B / independent]

3. Root Cause Analysis
   - Hypothesis 1: [cause] -> [effect] (Confidence: High/Med/Low)
     Evidence: [what supports this]
   - Hypothesis 2: [cause] -> [effect] (Confidence: High/Med/Low)
     Evidence: [what supports this]

4. Stakeholder Perspectives
   - User/Customer: [experience and loss]
   - Engineering: [technical framing]
   - Business: [metric and resource impact]

5. Problem Statement
   "[precise, testable problem statement]"

6. Scope & Boundaries
   - In scope: [...]
   - Out of scope: [...]
   - Constraints: [...]

7. Success Criteria
   - [measurable criterion 1]
   - [measurable criterion 2]

8. Anti-Pattern Checklist
   - [ ] Not treating a symptom as the problem
   - [ ] Not embedding a solution in the problem statement
   - [ ] Not bundling multiple distinct problems
   - [ ] Problem statement is testable and measurable

9. Recommended Next Steps
   - [action 1: e.g., validate hypothesis with data]
   - [action 2: e.g., run /diagnose on identified root cause]
```

## Quick Mode

For `quick` mode, skip Steps 2 and 3. Directly ask the user targeted questions (Step 1), then produce a condensed problem statement (Step 4) and a minimal PDD containing only sections 1, 5, 6, and 7.

## Team Mode

For `team` mode, generate a facilitation template:

1. **Pre-work prompt** — Questions for participants to answer before the session
2. **Workshop agenda** — Timed phases: Describe (10 min), Decompose (15 min), Diagnose (20 min), Define (15 min)
3. **Voting template** — For the team to rank root cause hypotheses
4. **Output template** — Blank PDD for collaborative completion

## Examples

### Example 1: Technical problem

User: `/define-problem "Our API is slow"`

- D1: "Slow" is vague. Ask: Which endpoints? What latency? Since when? Under what load?
- D2: Separate concerns — is it database queries, network, serialization, or client rendering?
- D3: 5 Whys reveals N+1 query pattern in the user listing endpoint. User perspective: page takes 8s to load. Engineering: ORM generates 200+ queries per request. Business: conversion drops 40% when load time exceeds 3s.
- D4: "Users of the /api/users endpoint experience 8-second response times under normal load (>50 concurrent users), resulting in a 40% conversion drop. Root cause: N+1 query pattern in UserRepository.list()."
- D5: Full PDD with measurable criteria: p95 latency < 500ms, query count < 5 per request.

### Example 2: Business/product problem

User: `/define-problem "We need to add a dashboard feature"`

- D1: Challenge: This is a solution, not a problem. Ask: What decision can't users make today? What information is missing?
- D2: Unpack the request — users lack visibility into resource utilization, leading to over-provisioning and wasted spend.
- D3: User perspective: "I don't know if my GPU allocation is being used." Business: 30% of allocated resources sit idle.
- D4: "Platform administrators cannot monitor real-time GPU utilization across teams, resulting in ~30% resource waste ($X/month). No existing view aggregates utilization data at the team level."
- D5: PDD with success criteria: admins can view utilization within 2 clicks, idle resource alerts trigger within 15 minutes.

### Example 3: Quick mode

User: `/define-problem quick "Login page is broken on mobile"`

- D1: Which devices? What breaks? Since when?
- D4: "Mobile users on iOS Safari (v16+) cannot submit the login form because the submit button is obscured by the virtual keyboard, blocking 100% of mobile login attempts since the v2.3 CSS refactor."
- Minimal PDD with sections 1, 5, 6, 7.

## Error Handling

| Scenario | Action |
|----------|--------|
| User provides no problem description | Ask for the situation, symptoms, or context |
| Problem is already well-defined | Validate against anti-patterns, then confirm or refine |
| User insists on jumping to solutions | Acknowledge the solution, then ask "What problem does this solve?" |
| Multiple distinct problems detected | Recommend splitting; produce separate PDDs or ask user to prioritize |
| Insufficient information for root cause | Mark hypotheses as Low confidence; recommend data-gathering as next step |

## Composability

The PDD output integrates with other skills:
- Feed into `/diagnose` for technical root cause verification
- Feed into `/plan` or `pm-execution` for solution planning
- Feed into `backend-expert` or `frontend-expert` for domain-specific analysis
- Attach to GitHub issues for structured problem tracking

## Troubleshooting

- **"I already know the problem"**: Even well-understood problems benefit from the anti-pattern check and stakeholder perspective analysis. Use `quick` mode.
- **"This is too abstract for code"**: The framework works at any level — from a single function bug to a system architecture decision. Provide file paths or error messages for concrete grounding.
- **"The team disagrees on the problem"**: Use `team` mode to structure the discussion and vote on root cause hypotheses.
