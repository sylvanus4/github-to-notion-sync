---
name: llm-council
description: >-
  Adversarial 5-advisor decision council with blind peer review and chair
  verdict. 3 rounds: argue, score, synthesize. No yes-men. Use for decision
  questions ("should we X?", "which approach?", "council", "카운슬", "판단해줘").
  Skip for implementation, code review, or factual lookups.
arguments: [question]
---

# LLM Council

5 advisors. Blind peer review. 1 verdict.

## Execution

### Step 1: Frame

Extract from `$question`: **Decision** (what), **Constraints** (timeline/budget/team), **Stakes** (cost of being wrong). If ambiguous, ask ONE clarifying question.

Classify complexity:
- **High**: multi-stakeholder, irreversible, >$10K impact -> full 3 rounds
- **Low**: binary, reversible, contained scope -> skip Round 2, go straight to Chair

### Step 2: Round 1 -- 5 Advisors (parallel, model: "sonnet")

Launch 5 Agent calls simultaneously. Each gets this prompt skeleton:

> You are Advisor {ID} on a decision council. Lens: {LENS}.
> Argue aggressively. No hedging. No "it depends."
>
> QUESTION: {decision} | CONSTRAINTS: {constraints} | STAKES: {stakes}
>
> Return exactly:
> 1. POSITION: One sentence (for/against/alternative)
> 2. ARGUMENT: 3 points (evidence > opinion)
> 3. RISK: What breaks if you're wrong?
> 4. KILL SHOT: Single fact that changes your mind
>
> Under 250 words. Match user's language.

| ID | Lens | Focus |
|----|------|-------|
| A | First Principles | What must be true for this to work? |
| B | Devil's Advocate | Strongest case AGAINST the default choice |
| C | Operator | Hidden costs, timeline risk, team capacity |
| D | Contrarian | Reframe: option nobody is considering? |
| E | End-User | Who gets hurt, who benefits? |

### Step 3: Round 2 -- 3 Peer Reviewers (parallel, model: "haiku")

Launch 3 Agent calls. Each receives all 5 Round 1 outputs anonymized as "Perspective 1-5".

> Score each perspective:
> - Logic (1-10), Evidence (1-10), Blindspots (1-10, where 10 = missed nothing)
> - STRONGEST POINT per perspective (quote)
> - WEAKEST POINT per perspective (specific flaw)
>
> Table format. Under 150 words. Discard your review if you scored all perspectives above 8 -- that means you aren't looking hard enough.

Sycophancy filter: if a reviewer scores all 10s, discard that review.

### Step 4: Round 3 -- Chair Synthesis (main context, no extra agent)

The main Claude acts as Chair. Read all Round 1 analyses + Round 2 peer scores. Synthesize:

1. **VERDICT**: Clear recommendation, 1-2 sentences. No "it depends."
2. **CONFIDENCE**: High (>80%) / Medium (50-80%) / Low (<50%) + reasoning
3. **CONSENSUS MAP**: Who aligned, who dissented, on what
4. **DISSENT WORTH HEARING**: Strongest counter-argument that survived peer review
5. **NEXT STEPS**: 3 concrete actions
6. **KILL CONDITION**: Observable signal that reverses this verdict

### Step 5: Output

```
LLM COUNCIL VERDICT
====================
QUESTION: {question}
VERDICT:  {recommendation}
CONFIDENCE: {level} -- {reason}

ADVISOR POSITIONS:
  A First Principles:  {stance}  [{avg score}]
  B Devil's Advocate:  {stance}  [{avg score}]
  C Operator:          {stance}  [{avg score}]
  D Contrarian:        {stance}  [{avg score}]
  E End-User:          {stance}  [{avg score}]

CONSENSUS: {N}/5 on {X}
DISSENT:   {counter-argument}

NEXT STEPS:
  1. {action}
  2. {action}
  3. {action}

KILL CONDITION: {reversal signal}
```

## Cost Profile

| Round | Agents | Model | Est. Output |
|-------|--------|-------|-------------|
| R1 Advisors | 5 parallel | sonnet | ~6,250 |
| R2 Reviewers | 3 parallel | haiku | ~2,250 |
| R3 Chair | 0 (main ctx) | -- | ~800 |
| **Total** | **8 calls** | | **~9,300 tokens** |

## Error Handling

- Advisor hedges -> re-prompt: "Take a clear stance."
- Peer review all 10s -> discard (sycophancy)
- Agent timeout -> proceed with min 3/5 advisors
- Question vague -> ask ONE clarifier before Round 1
- Low complexity detected -> skip Round 2 entirely
