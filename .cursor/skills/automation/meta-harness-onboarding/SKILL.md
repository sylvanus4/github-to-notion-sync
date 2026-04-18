# Meta-Harness Onboarding

Structured pre-implementation gate for harness optimization. Runs a Socratic conversation loop that produces a `domain_spec.md` before any code-level optimization begins. Adapted from Stanford IRIS Lab's ONBOARDING.md methodology (arXiv:2603.28052).

## When to Use

Use when the user asks to "onboard for meta-harness", "meta-harness onboarding", "harness domain spec", "create domain spec", "meta harness 온보딩", "하네스 도메인 스펙", "도메인 스펙 생성", "harness fitness screening", "is this a good harness target", "메타 하네스 온보딩", or wants to prepare a skill/harness for outer-loop optimization via `meta-harness-optimizer`.

## When NOT to Use

- For running the optimization loop itself — use `meta-harness-optimizer`
- For prompt-only optimization — use `skill-autoimprove`
- For creating new skills from scratch — use `create-skill` or `harness`
- For general product discovery interviews — use `omc-deep-interview`
- For evaluating skill quality without optimization intent — use `skill-optimizer`

## Prerequisites

- Target skill or harness must exist (at least a draft SKILL.md or script)
- User must understand what they want to improve (even vaguely)
- No implementation happens during onboarding — output is `domain_spec.md` only

## Core Principle

**No `domain_spec.md` → no optimization.** This skill is the mandatory first step before `meta-harness-optimizer`. Every required field must be filled or explicitly marked `unknown` with a stated default before the spec is emitted.

## Conversation Loop Protocol

### Phase 1: Domain Fitness Screening

Before starting the full onboarding loop, screen the target against the Promising Domain Properties checklist. Ask the user to confirm or deny each property.

**Promising when (GREEN flags):**

- Long-horizon / multi-step task (harness choices compound over steps)
- Repeated episodes (not a one-off bespoke task)
- Fixed base model; gains from retrieval/memory/context/tools/planning scaffolding
- Measurable eval loop with a real success metric
- Evidence that harness changes move the needle (past experiments or intuition)
- Search space large enough to expose failure modes yet small enough to iterate
- Recurring error patterns that are addressable by harness code changes
- Offline traces or domain docs exist that could warm-start the proposer
- Meaningful held-out test exists or can be plausibly constructed

**Poor fit when (RED flags):**

- Most gains require changing the base model itself (not the code around it)
- No stable evaluation loop (open-ended subjective quality only)
- Single-shot task with no episode structure
- Evaluation takes >30 minutes per candidate (budget infeasible)

**Decision gate:** If 3+ RED flags and <3 GREEN flags, recommend against harness optimization and suggest alternatives (`skill-autoimprove` for prompt tuning, `hermes-skill-evolver` for population-based prompt evolution).

### Phase 2: Structured Requirements Gathering

Run a Socratic interview with these rules:

1. Ask **1-2 focused questions** at a time (never dump a questionnaire)
2. Maintain a **running summary** visible to the user, updated after each answer
3. Identify the **largest missing piece** and ask about that next
4. Prefer **numbers over prose** (budget in dollars, candidate count, eval runtime in seconds)
5. Mark unanswered fields as `unknown` with a stated default assumption
6. Watch for **evaluation leakage** risks (search data contaminating validation)
7. **No implementation** during this conversation — only specification

### Required Fields

Gather all fields across these 6 categories:

#### 1. Problem Framing

- What is the user trying to improve?
- What is the unit of evaluation (one input, one episode, one task, one conversation)?
- What is fixed and what is allowed to change?
- What is the frozen base model or set of models?
- What is the total budget for harness optimization (tokens, dollars, wall-clock time, or candidate count)?

#### 2. Harness Definition

- What interface must every candidate harness satisfy?
- What is the cleanest base Python class or API shape for that harness?
- How would we test interface compliance?
- What changes are explicitly out of scope?

#### 3. Evaluation

- What is the search-set evaluation?
- What is the held-out test evaluation, if any?
- What metric or metrics matter (primary)?
- What secondary metrics matter (latency, context cost, API spend, timeout success)?
- How noisy is evaluation?
- How long does one candidate evaluation take?
- Is there memorization or contamination risk? If so, how will we mitigate it?

#### 4. Baselines

- What are the obvious hand-written baselines?
- What is the strongest current harness in this domain?
- What reusable helper functions should exist from the start?

#### 5. Offline Experience

- Is there an offline trace set we can use to warm-start search?
- Are there papers, reports, or notes worth encoding into the proposer context?

#### 6. Online Experience

- What raw traces should be stored per candidate?
- Which files are likely the highest-signal debugging artifacts?
- What metadata should be preserved?
- What directory structure should hold prior candidates and their results?
- Would a small CLI for querying run history be worth building?

### Phase 3: Verification and Emission

1. Display the complete running summary with all 6 categories
2. Verify every required field is present or marked `unknown` with default
3. Check for evaluation leakage risks one final time
4. Emit `domain_spec.md` using the template below

## Output: `domain_spec.md` Template

Write the spec to `_workspace/meta-harness/domain-specs/{target-name}-domain-spec.md`:

```markdown
# Domain Spec: {target-name}

Generated by meta-harness-onboarding on {date}
Fitness screening: {PASS/CONDITIONAL/FAIL} ({N} green, {M} red flags)

## 1. Problem Framing

- **Improvement goal:** {description}
- **Unit of evaluation:** {unit}
- **Fixed components:** {list}
- **Mutable components:** {list}
- **Frozen base model(s):** {model names}
- **Optimization budget:** {budget with units}

## 2. Harness Definition

- **Interface contract:** {description or code reference}
- **Base class/API shape:** {reference}
- **Compliance test:** {how to verify}
- **Out of scope:** {explicit exclusions}

## 3. Evaluation

- **Search-set eval:** {description}
- **Held-out test eval:** {description or "none — construct from {source}"}
- **Primary metrics:** {list with target values}
- **Secondary metrics:** {list}
- **Noise level:** {low/medium/high with evidence}
- **Eval runtime per candidate:** {time estimate}
- **Contamination mitigation:** {strategy}

## 4. Baselines

- **Hand-written baselines:** {list}
- **Strongest current harness:** {name and score}
- **Reusable helpers:** {list}

## 5. Offline Experience

- **Trace corpus:** {path or "none"}
- **Reference documents:** {list of papers/notes}

## 6. Online Experience

- **Per-candidate traces:** {what to store}
- **High-signal artifacts:** {list}
- **Metadata fields:** {list}
- **Directory layout:** {structure}
- **Query CLI:** {yes/no, commands if yes}

## Recommended Configuration

- `--iterations`: {N}
- `--candidates-per-iter`: {k}
- `--objectives`: {comma-separated}
- `--search-split`: {fraction}
```

## Integration Points

- **Output feeds into:** `meta-harness-optimizer --target {skill} --domain-spec {path}`
- **Fitness screening reuses:** domain properties from Stanford ONBOARDING.md
- **Running summary format:** compatible with `problem-definition` PDD structure
- **Leakage checks:** aligned with `search-split-discipline` contamination prevention

## Anti-Patterns

- Do NOT skip fitness screening — poor-fit domains waste optimization budget
- Do NOT accept vague answers without pressing for numbers
- Do NOT allow "we'll figure out evaluation later" — eval is the foundation
- Do NOT start implementation code during onboarding
- Do NOT emit a domain_spec.md with blank required fields (mark `unknown` explicitly)

## Examples

### Example 1: Good candidate (daily-stock-check)

```
User: I want to optimize daily-stock-check with meta-harness
Agent:
  [Fitness screening]
  ✅ Multi-step (data sync → screen → analyze → report)
  ✅ Repeated daily episodes
  ✅ Fixed base model (Claude Sonnet)
  ✅ Measurable eval (signal accuracy vs next-day price movement)
  ✅ Recurring errors (false signals on low-volume stocks)
  ✅ Offline traces exist (outputs/screener-*.json)
  ✅ Held-out possible (use different date ranges)
  Result: 7 GREEN / 0 RED → PASS

  [Onboarding loop — 6-8 questions across categories]
  ...
  [Emit domain_spec.md]
```

### Example 2: Poor candidate (design-architect)

```
User: Can we meta-harness optimize design-architect?
Agent:
  [Fitness screening]
  ❌ Subjective quality (no stable numeric eval)
  ❌ Open-ended output (14 dimensions, human judgment)
  ⚠️ Single-shot per screen (limited episode structure)
  ✅ Multi-step analysis
  ✅ Recurring patterns
  Result: 2 GREEN / 3 RED → FAIL

  Recommendation: design-architect is better suited for
  skill-autoimprove (prompt tuning) or hermes-skill-evolver
  (population-based prompt evolution). Meta-harness optimization
  requires measurable eval loops that this skill lacks.
```

## References

- Stanford ONBOARDING.md: https://github.com/stanford-iris-lab/meta-harness/blob/main/ONBOARDING.md
- Meta-Harness paper: arXiv:2603.28052, Section 3
- Internal: `meta-harness-optimizer` SKILL.md, `harness` SKILL.md
