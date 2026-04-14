---
name: hypothesis-pm
description: >-
  Scientific-method investigation loop adapted for Product Managers: Observe
  product usage data and user behavior → Hypothesize assumptions about user needs
  and feature performance → Experiment with minimal data validations → Conclude
  with evidence-backed product decisions. Persists all reasoning to
  INVESTIGATION.md to prevent context loss. Use when a PM assumption about user
  needs requires validation, when a feature bet isn't meeting adoption targets,
  when user feedback contradicts the product roadmap, when "why aren't users
  adopting feature X?" questions arise, or when the user asks to "validate PM
  assumption", "hypothesis PM", "investigate user behavior", "PM assumption test",
  "product hypothesis", "기획 가설 검증", "가설 기반 기획", "사용자 행동 조사",
  "기능 가설 테스트". Do NOT use for writing PRDs from scratch (use pm-execution).
  Do NOT use for market research without a specific product assumption to test
  (use pm-market-research). Do NOT use for sprint planning (use pm-execution). Do
  NOT use for marketing campaign performance diagnosis (use
  hypothesis-marketing). Do NOT use for competitive analysis without a hypothesis
  (use kwp-product-management-competitive-analysis).
---

# Hypothesis-Driven PM Investigation

Adapted from the core `hypothesis-investigation` methodology for Product Management assumption validation.

## Iron Laws (PM Context)

1. **No feature decisions before assumptions are listed** — write ≥3 competing hypotheses in INVESTIGATION.md
2. **Each validation ≤ 1 metric or 5 user data points** — surgical precision, not boil-the-ocean research
3. **All evidence persists to file** — `outputs/investigation/{date}/INVESTIGATION.md` survives context compaction
4. **Two same-direction failures → forced pivot** — if the assumption fails twice with different data, switch direction
5. **Explicit predictions before validation** — write expected outcomes before looking at the data

## Phase 1: Observe (User/Market Signals)

Gather raw signals without interpretation.

1. **Identify the trigger** — what metric dropped, what feedback contradicts expectations, what behavior surprises?
2. **Collect quantitative data** — usage metrics, funnel conversion, retention curves, feature adoption rates
3. **Collect qualitative data** — user feedback, support tickets, interview snippets, NPS comments
4. **Map the working boundary** — what IS working? Which user segments ARE happy? Which flows DO convert?
5. **Create investigation file** — initialize from `hypothesis-investigation/references/investigation-template.md`

Compose with: `pm-data-analytics` (SQL/cohort), `kwp-data-data-exploration` (profiling), `pm-market-research` (personas/segments)

## Phase 2: Hypothesize (Competing Assumptions)

Generate **minimum 3** competing explanations for the observed behavior.

1. **List PM assumptions** — what are we assuming about user needs, market fit, value proposition?
2. **Generate hypotheses** — each must be falsifiable with available data:
   - "Users don't use feature X because [specific reason]"
   - "Conversion drops at step Y because [specific friction]"
   - "Segment Z churns because [specific unmet need]"
3. **Rank by evidence** — which hypothesis has the most supporting/conflicting data from Phase 1?
4. **Design minimal validations** — each test uses ≤ 1 new metric query or 5 user data points

Compose with: `pm-product-discovery` (OST, assumption mapping), `kwp-product-management-user-research-synthesis`

## Phase 3: Experiment (Minimal Validation)

Test one assumption at a time with the smallest possible data request.

1. **Pick the assumption with strongest signal** — start where odds of confirmation are highest
2. **Run the minimal validation**:
   - Query one specific metric (compose with `pm-data-analytics`)
   - Analyze 5 specific user sessions or feedback items
   - Check one competitor's approach to the same problem
3. **Record prediction** — "If assumption A is correct, metric M should show [X]"
4. **Compare actual vs predicted** — Verdict: CONFIRMED / REJECTED / INCONCLUSIVE
5. **Pivot rule** — two same-direction failures → switch to a different assumption

Compose with: `pm-data-analytics` (SQL, cohort, A/B analysis), `kwp-data-statistical-analysis`

### Experiment Guardrails

- Maximum 7 validation rounds before stepping back to re-observe with fresh data
- If all hypotheses are rejected, return to Phase 1 — the original framing may be wrong
- Always log pivot decisions in INVESTIGATION.md Pivot Log section

## Phase 4: Conclude (Evidence-Backed Decision)

Once an assumption is confirmed or all are rejected:

1. **State the validated finding** — one sentence in INVESTIGATION.md
2. **Map to action**:
   - Feature change? → Feed into `pm-execution` (PRD update, user stories)
   - Roadmap shift? → Update via `kwp-product-management-roadmap-management`
   - Need more research? → Escalate to `pm-product-discovery` or `parallel-deep-research`
3. **Document the decision** — capture in decision-tracker or ADR
4. **Archive** — investigation persists at `outputs/investigation/{date}/`

## Quality Gates

### Observation Quality Gate
Before proceeding to Phase 2, verify:
- [ ] Metric trigger clearly documented (which metric, how much deviation)
- [ ] Quantitative and qualitative data collected
- [ ] Working boundary identified (what IS working)
- [ ] Investigation file created at `outputs/investigation/{date}/`

### Hypothesis Quality Gate
Before proceeding to Phase 3, verify:
- [ ] ≥ 3 hypotheses written in INVESTIGATION.md
- [ ] Each hypothesis has supporting/conflicting evidence from Phase 1
- [ ] Each hypothesis has a designed validation (≤ 1 metric or 5 data points)
- [ ] Predictions written for each validation (expected outcome)

### Conclusion Quality Gate
Before declaring done:
- [ ] Validated finding documented in one sentence
- [ ] Action mapped to specific PM deliverable (PRD update, roadmap change, research)
- [ ] Decision captured in decision-tracker or ADR
- [ ] INVESTIGATION.md fully completed and archived

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| "Users want this feature" (no data) | Confirmation bias drives roadmap | List 3+ hypotheses, validate with data |
| Surveying 100 users to test one assumption | Overkill wastes time | 5 data points per validation round |
| Changing the roadmap after one negative signal | Overcorrection on insufficient evidence | Require 2+ converging signals before pivoting |
| Interpreting ambiguous data as confirmation | Anchoring bias | Write predictions BEFORE looking at data |

## Harness Integration

Integrates into `pm-harness` as an optional investigation mode when product metrics diverge from expectations.
