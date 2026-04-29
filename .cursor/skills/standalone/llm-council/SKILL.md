# The LLM Council

---
name: llm-council
description: >-
  Multi-agent deliberation council for high-stakes decisions. 5 advisors attack
  a decision question from diverse angles (Devil's Advocate, Optimist Strategist,
  Risk Analyst, First-Principles Thinker, Contrarian Outsider), then anonymously
  peer-review each other's work, and a Chairperson synthesizes one verdict with
  concrete next steps. Produces deeper, less biased analysis than a single LLM
  by forcing adversarial diversity and blind evaluation.
  Use when the user asks to "convene the council", "LLM council", "council decision",
  "5 advisors", "multi-agent decision", "council vote", "deliberation council",
  "LLM 카운슬", "카운슬 소집", "의회 소집", "5인 자문단", "다관점 의사결정",
  "의사결정 카운슬", "카운슬 판결", "llm-council", "/llm-council",
  or wants a structured multi-perspective analysis of a decision question
  with adversarial peer review and synthesis.
  Do NOT use for single-perspective analysis (use role-* skills).
  Do NOT use for code review (use deep-review or simplify).
  Do NOT use for 3-way tournament text refinement (use autoreason).
  Do NOT use for evaluator-optimizer loops (use workflow-eval-opt).
  Do NOT use for brainstorming without decision framing (use sp-brainstorming).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "decision-making"
  tags: ["multi-agent", "deliberation", "peer-review", "decision-support"]
---

## Purpose

One LLM tells you you're right. Five LLMs show you where you're wrong.

The LLM Council forces genuine intellectual diversity on your decision by:
1. Assigning 5 **distinct cognitive roles** so no two advisors think alike
2. Requiring **anonymous peer review** so advisors critique ideas, not identities
3. Having a **Chairperson** synthesize consensus, dissent, and actionable next steps

## When to Use

- You face a real decision with trade-offs (not a factual lookup)
- You want adversarial stress-testing, not validation
- You need to surface blind spots before committing

## The 5 Advisor Roles

| # | Role | Lens | Core Question |
|---|------|------|---------------|
| 1 | **Devil's Advocate** | Find fatal flaws | "Why will this fail?" |
| 2 | **Optimist Strategist** | Find upside leverage | "How could this succeed beyond expectations?" |
| 3 | **Risk Analyst** | Quantify uncertainty | "What are the probabilities and second-order effects?" |
| 4 | **First-Principles Thinker** | Strip assumptions | "What is actually true here vs. inherited belief?" |
| 5 | **Contrarian Outsider** | Challenge framing | "Is this even the right question to ask?" |

## Procedure

### Phase 0: Question Intake

1. Accept the user's decision question
2. If the question is vague, ask ONE clarifying question (max 1 round)
3. Frame the decision as: **"Should we [ACTION] given [CONTEXT], where the stakes are [STAKES]?"**
4. Persist the framed question to `outputs/llm-council/{date}/question.md`

### Phase 1: Advisor Deliberation (Fan-Out — 5 Parallel Subagents)

Launch 5 parallel subagents, each receiving ONLY the framed question (no other advisor's output). Each subagent MUST:

1. State their role and lens in one sentence
2. Deliver their analysis in 150-300 words covering:
   - Their core position (for/against/conditional)
   - 2-3 strongest arguments with evidence or reasoning
   - 1 specific scenario where their position breaks down (intellectual honesty)
3. Assign a **confidence score** (1-10) for their position
4. End with a one-sentence verdict: `VERDICT: [PROCEED / REJECT / CONDITIONAL: <condition>]`

Persist each advisor's output to `outputs/llm-council/{date}/advisor-{N}-{role}.md`.

**Subagent prompt template:**

```
You are Advisor {N}: {ROLE_NAME}.

Your cognitive lens: {LENS_DESCRIPTION}
Your core question: {CORE_QUESTION}

DECISION QUESTION:
{framed_question}

RULES:
- Argue from YOUR lens only. Do not try to be balanced.
- Be specific. Name scenarios, numbers, timelines where possible.
- Acknowledge ONE scenario where your position breaks down.
- End with: VERDICT: [PROCEED / REJECT / CONDITIONAL: <condition>]
- Confidence: [1-10]
- Keep to 150-300 words.
```

### Phase 2: Anonymous Peer Review (Fan-Out — 5 Parallel Subagents)

Each advisor reviews ALL OTHER advisors' outputs (not their own). Labels are randomized (Advisor A-E instead of role names) to prevent identity bias.

Each reviewer MUST produce for each of the 4 other advisors:
- **Strength** (1 sentence): strongest point
- **Weakness** (1 sentence): biggest gap or logical flaw
- **Score** (1-5): quality of reasoning

Persist to `outputs/llm-council/{date}/review-by-{N}.md`.

**Reviewer prompt template:**

```
You previously served as an advisor on a decision question. Now review
4 other advisors' analyses. Their identities are hidden.

ORIGINAL QUESTION:
{framed_question}

YOUR OWN ANALYSIS (for reference — do NOT review yourself):
{own_analysis}

ADVISOR A:
{advisor_analysis_shuffled_A}

ADVISOR B:
{advisor_analysis_shuffled_B}

ADVISOR C:
{advisor_analysis_shuffled_C}

ADVISOR D:
{advisor_analysis_shuffled_D}

For each advisor (A, B, C, D), provide:
- Strength: (1 sentence)
- Weakness: (1 sentence)
- Score: (1-5)

Be harsh but fair. Judge reasoning quality, not whether you agree.
```

### Phase 3: Chairperson Synthesis (Sequential — 1 Subagent)

The Chairperson receives ALL advisor analyses AND ALL peer reviews. The Chairperson MUST produce:

1. **Vote Tally**: count of PROCEED / REJECT / CONDITIONAL verdicts
2. **Consensus Points**: what 3+ advisors agree on
3. **Key Dissent**: the strongest minority argument that cannot be dismissed
4. **Peer Review Signal**: which advisor(s) scored highest/lowest by peers, and why
5. **Blind Spots Identified**: gaps NO advisor covered
6. **THE VERDICT**: one of:
   - **STRONG PROCEED** — 4-5 advisors agree, peer reviews confirm quality
   - **LEAN PROCEED** — majority favors, but significant conditional risks
   - **DEADLOCKED** — no clear majority; list the 2 strongest competing positions
   - **LEAN REJECT** — majority opposes, or peer reviews exposed critical flaws
   - **STRONG REJECT** — 4-5 advisors oppose, reasoning is robust
7. **Next Steps**: 3-5 specific, actionable items regardless of verdict

Persist to `outputs/llm-council/{date}/verdict.md`.

**Chairperson prompt template:**

```
You are the Chairperson of a 5-advisor deliberation council.

DECISION QUESTION:
{framed_question}

ADVISOR ANALYSES:
{all_5_advisor_analyses_with_role_labels}

PEER REVIEW RESULTS:
{all_5_review_sets}

YOUR TASK:
Synthesize a final verdict. You are NOT another advisor — you are the
integrator. Do not add your own opinion. Weigh the evidence and reviews.

Produce:
1. Vote Tally
2. Consensus Points
3. Key Dissent (strongest minority view)
4. Peer Review Signal (highest/lowest scored advisors + why)
5. Blind Spots (gaps no advisor covered)
6. THE VERDICT: [STRONG PROCEED / LEAN PROCEED / DEADLOCKED / LEAN REJECT / STRONG REJECT]
7. Next Steps (3-5 actionable items)

Be decisive. Explain your reasoning for the verdict in 2-3 sentences.
```

### Phase 4: Present to User

Display the full verdict to the user in structured Korean, including:
- The framed question
- Summary table of advisor verdicts and confidence scores
- The Chairperson's synthesis
- Actionable next steps

## Output Structure

```
outputs/llm-council/{date}/
  question.md              # Framed decision question
  advisor-1-devils-advocate.md
  advisor-2-optimist-strategist.md
  advisor-3-risk-analyst.md
  advisor-4-first-principles.md
  advisor-5-contrarian-outsider.md
  review-by-1.md           # Peer reviews from advisor 1
  review-by-2.md
  review-by-3.md
  review-by-4.md
  review-by-5.md
  verdict.md               # Chairperson synthesis
```

## Constraints

- Each advisor subagent gets ONLY the question — never other advisors' outputs
- Peer review uses randomized labels (A-E) — never role names
- The Chairperson does NOT add personal opinion — synthesizes only
- All phases persist to files before the next phase begins
- Total runtime: 3 phases of subagent calls (advisors → reviews → synthesis)
- Language: analysis in Korean, technical terms in English as-is

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `advisor_count` | 5 | Number of advisors (min 3, max 7) |
| `word_limit` | 300 | Max words per advisor analysis |
| `date_dir` | today | Output directory date stamp |

## Anti-Patterns

- **Sycophancy**: if all 5 advisors agree, the Chairperson MUST flag this as suspicious and identify what assumption they all share
- **Vague verdicts**: "it depends" is not a verdict — force a directional lean
- **Gold-plating**: do not add extra analysis rounds beyond the 3 phases
- **Echo chamber**: if peer reviews are uniformly positive, flag potential groupthink
