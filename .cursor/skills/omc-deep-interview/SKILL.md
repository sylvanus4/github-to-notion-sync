---
name: omc-deep-interview
description: >-
  Socratic deep interview with mathematical ambiguity scoring that replaces vague
  ideas with crystal-clear specifications before execution. Asks one targeted
  question at a time, scores clarity across weighted dimensions, and gates on a
  configurable ambiguity threshold (default 20%). Outputs a structured spec with
  ontology tracking, clarity breakdown, and acceptance criteria. Use when the user
  asks to "interview me", "deep interview", "clarify requirements", "don't assume
  anything", "make sure you understand", "ask me everything", "Socratic interview",
  "requirements interview", "specification interview", "요구사항 인터뷰",
  "딥 인터뷰", "소크라틱 인터뷰", "가정 검증", "모호성 제거", or has a vague idea
  that needs thorough requirements clarification before implementation. Do NOT use
  for detailed requests with file paths, function names, or acceptance criteria
  (execute directly). Do NOT use for brainstorming or option exploration (use
  sp-brainstorming). Do NOT use for plan creation without requirements gathering
  (use sp-writing-plans). Do NOT use when the user says "just do it" or "skip the
  questions".
metadata:
  author: "oh-my-claudecode"
  version: "1.0.0"
  category: "requirements"
---

# Deep Interview: Socratic Requirements Clarification

Adapted from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) deep-interview skill. Implements Ouroboros-inspired Socratic questioning with mathematical ambiguity gating.

## Instructions

### Phase 1: Initialize

1. **Parse the user's idea** from the request.
2. **Detect brownfield vs greenfield**:
   - Use a `Task` subagent (`subagent_type="explore"`) to check if the workspace has existing source code related to the idea.
   - If source files exist AND the idea references modifying/extending something: **brownfield**.
   - Otherwise: **greenfield**.
3. **For brownfield**: Run exploration to map relevant codebase areas; store as `codebase_context`.
4. **Announce the interview**:

> Starting deep interview. I'll ask targeted questions to understand your idea thoroughly before building anything. After each answer, I'll show your clarity score. We'll proceed to execution once ambiguity drops below 20%.
>
> **Your idea:** "{initial_idea}"
> **Project type:** {greenfield|brownfield}
> **Current ambiguity:** 100% (we haven't started yet)

### Phase 2: Interview Loop

Repeat until `ambiguity ≤ threshold` (default 0.2) OR user exits early:

#### Step 2a: Generate Next Question

- Identify the dimension with the **LOWEST** clarity score.
- State in one sentence why this dimension is the bottleneck.
- Generate a question targeting that dimension.
- Questions expose **ASSUMPTIONS**, not gather feature lists.
- If entities keep shifting or the core noun is unstable, use ontology-style questioning ("What IS this, really?").

**Question styles by dimension:**

| Dimension | Question Style | Example |
|-----------|---------------|---------|
| Goal Clarity | "What exactly happens when...?" | "When you say 'manage tasks', what specific action does a user take first?" |
| Constraint Clarity | "What are the boundaries?" | "Should this work offline, or is internet connectivity assumed?" |
| Success Criteria | "How do we know it works?" | "If I showed you the finished product, what would make you say 'yes, that's it'?" |
| Context Clarity (brownfield) | "How does this fit?" | "I found JWT auth in `src/auth/`. Should this extend that path or diverge?" |

#### Step 2b: Ask ONE Question

Use the `AskQuestion` tool. Present with context:

```
Round {n} | Targeting: {weakest_dimension} | Why now: {rationale} | Ambiguity: {score}%

{question}
```

**CRITICAL: Ask ONE question at a time. Never batch multiple questions.**

#### Step 2c: Score Ambiguity

After each answer, score clarity across all dimensions (0.0-1.0):

1. **Goal Clarity** — Is the primary objective unambiguous?
2. **Constraint Clarity** — Are boundaries, limitations, and non-goals clear?
3. **Success Criteria Clarity** — Could you write a test that verifies success?
4. **Context Clarity** (brownfield only) — Do we understand the existing system?

**Calculate ambiguity:**

- Greenfield: `ambiguity = 1 - (goal × 0.40 + constraints × 0.30 + criteria × 0.30)`
- Brownfield: `ambiguity = 1 - (goal × 0.35 + constraints × 0.25 + criteria × 0.25 + context × 0.15)`

**Extract ontology** — identify key entities (nouns), their types, fields, and relationships. Track stability across rounds:

- `stability_ratio = (stable + changed) / total_entities`

#### Step 2d: Report Progress

```
Round {n} complete.

| Dimension | Score | Weight | Weighted | Gap |
|-----------|-------|--------|----------|-----|
| Goal | {s} | {w} | {s*w} | {gap or "Clear"} |
| Constraints | {s} | {w} | {s*w} | {gap or "Clear"} |
| Success Criteria | {s} | {w} | {s*w} | {gap or "Clear"} |
| Context (brownfield) | {s} | {w} | {s*w} | {gap or "Clear"} |
| **Ambiguity** | | | **{score}%** | |

**Ontology:** {entity_count} entities | Stability: {ratio} | New: {n} | Changed: {c} | Stable: {s}

**Next target:** {weakest_dimension} — {rationale}
```

#### Step 2e: Soft Limits

- **Round 3+**: Allow early exit if user says "enough", "let's go", "build it".
- **Round 10**: Show soft warning with current ambiguity.
- **Round 20**: Hard cap — proceed with current clarity.

### Phase 3: Challenge Agents

At specific round thresholds, shift questioning perspective (each used once):

| Mode | Activates | Purpose |
|------|-----------|---------|
| Contrarian | Round 4+ | "What if the opposite were true?" — Challenge core assumptions |
| Simplifier | Round 6+ | "What's the simplest version?" — Remove unnecessary complexity |
| Ontologist | Round 8+ (if ambiguity > 0.3) | "What IS this, really?" — Stabilize the core entity |

### Phase 4: Crystallize Spec

When ambiguity ≤ threshold (or hard cap / early exit):

1. Generate a structured specification from the full interview transcript.
2. Write to `outputs/specs/deep-interview-{slug}.md`.

**Spec structure:**
- Metadata (interview ID, rounds, final ambiguity, type, threshold, status)
- Clarity Breakdown table
- Goal statement
- Constraints and Non-Goals
- Acceptance Criteria (testable checkboxes)
- Assumptions Exposed & Resolved table
- Technical Context
- Ontology (Key Entities) table
- Ontology Convergence table
- Interview Transcript (collapsible)

### Phase 5: Execution Bridge

Present execution options via `AskQuestion`:

1. **Plan and Execute (Recommended)** — Create a plan with sp-writing-plans, then execute.
2. **Execute directly** — For clear-enough specs, implement using appropriate skills.
3. **Deep review the spec** — Get multi-perspective review via deep-review.
4. **Refine further** — Continue interviewing.

**The deep-interview agent is a requirements agent, not an execution agent.** Always hand off to execution skills; never implement directly.

## Error Handling

- **User provides no initial idea**: Ask for a one-sentence description before starting.
- **Brownfield detection subagent fails**: Default to greenfield mode and note the assumption.
- **User becomes frustrated with questions**: Offer early exit with current ambiguity score and warn about potential rework.
- **Ambiguity never drops below threshold**: Hard cap at round 20 — proceed with the best available clarity and document gaps.
- **AskQuestion tool unavailable**: Fall back to inline questions in the response text.

## When to Use

- User has a vague idea and wants thorough requirements gathering before execution
- User says "deep interview", "interview me", "ask me everything", "don't assume"
- User says "Socratic", "I have a vague idea", "not sure exactly what I want"
- User wants to avoid "that's not what I meant" outcomes from autonomous execution
- Task is complex enough that jumping to code would waste cycles on scope discovery
- User wants mathematically-validated clarity before committing to execution

## When NOT to Use

- User has a detailed, specific request with file paths, function names, or acceptance criteria — execute directly
- User wants to explore options or brainstorm — use `sp-brainstorming`
- User wants a quick fix or single change
- User says "just do it" or "skip the questions" — respect their intent
- User already has a PRD or plan file — use the plan directly

## Examples

<example>
User: "I want to build a task management thing"

Round 1 | Targeting: Goal Clarity | Why now: Goal is the most undefined dimension at 0.1 | Ambiguity: 90%

"When you say 'task management', what specific action does a user take first — creating a task, viewing existing tasks, or something else entirely?"

[User answers: "Creating tasks with deadlines"]

Round 1 complete.
| Dimension | Score | Weight | Weighted | Gap |
|-----------|-------|--------|----------|-----|
| Goal | 0.4 | 0.40 | 0.16 | Need clarity on task lifecycle |
| Constraints | 0.1 | 0.30 | 0.03 | No boundaries defined |
| Success Criteria | 0.1 | 0.30 | 0.03 | No verification criteria |
| **Ambiguity** | | | **78%** | |

**Ontology:** 2 entities (Task, User) | Stability: N/A (first round)
**Next target:** Constraints — no boundaries, tech stack, or scope limits defined yet
</example>

<example>
Challenge agent — Contrarian mode (Round 5):

Round 5 | Contrarian Mode | Ambiguity: 35%

"You've said this needs real-time collaboration. What if it didn't — what if changes sync every 30 seconds instead? Would that simplify the architecture significantly while still meeting user needs?"
</example>

<example>
Early exit with warning:

User: "That's enough, just build it"

Current ambiguity is 35% (threshold: 20%). Areas still unclear:
- Success Criteria: 0.5 (How do we verify the search ranking works?)
- Constraints: 0.6 (No performance targets defined)

Proceeding may require rework. Continue anyway?
[Yes, proceed] [Ask 2-3 more questions] [Cancel]
</example>
