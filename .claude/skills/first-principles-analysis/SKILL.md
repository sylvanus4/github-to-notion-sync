---
name: first-principles-analysis
description: >-
  Decompose any topic into fundamental truths by systematically stripping
  inherited assumptions layer-by-layer. Identifies what is provably true,
  discards conventional wisdom that lacks foundation, and rebuilds
  understanding from bedrock truths only. Use when the user asks to "first
  principles", "strip assumptions", "rebuild from scratch", "bedrock truth",
  "decompose to fundamentals", "기본 원리 분석", "가정 제거", "근본 분석", "본질 분석", "제1원리",
  or any request to analyze a topic by removing inherited thinking. Do NOT use
  for code review (use deep-review), problem definition with root cause
  analysis (use problem-definition), prompt optimization (use
  prompt-architect), or financial fundamental analysis like P/E ratios (use
  trading-us-stock-analysis).
---

# First Principles Analysis

Strip a topic down to what is fundamentally, provably true — then rebuild understanding from only what remains.

## When to Use

- Challenging conventional wisdom on a topic
- Evaluating a strategy, technology, or decision that "everyone assumes" works a certain way
- Breaking through analysis paralysis by finding the irreducible core
- Exploring whether an established approach is built on solid foundations or inherited assumptions
- Reframing a domain when existing mental models feel inadequate

## Workflow

### Phase 1: Assumption Inventory

Identify every assumption people commonly make about the topic. Be exhaustive — surface both obvious and hidden assumptions.

Categorize each assumption:

| Category | Description | Example |
|----------|-------------|---------|
| **Structural** | How the system/concept is organized | "Microservices are better than monoliths" |
| **Causal** | Believed cause-effect relationships | "More data always improves model accuracy" |
| **Boundary** | Perceived limits or constraints | "You need a GPU cluster to train LLMs" |
| **Value** | What is considered important or optimal | "User growth is the key metric for startups" |
| **Historical** | "We've always done it this way" | "Stocks always recover in the long run" |

Aim for 8-15 assumptions. Fewer means you haven't dug deep enough.

### Phase 2: Assumption Stripping

For each assumption, apply this test:

```
1. Is this provably true from first principles (physics, math, logic)?
2. Or is this an inherited belief (convention, tradition, analogy, authority)?
3. What evidence would DISPROVE this assumption?
4. What happens if this assumption is simply wrong?
```

Classify each assumption into one of three buckets:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **Bedrock** | Provably true, survives all challenges | Keep as foundation |
| **Conditional** | True only under specific circumstances | Note the conditions |
| **Inherited** | Accepted without proof, based on convention | Strip away |

### Phase 3: Bedrock Truth Extraction

List only what survived Phase 2 — the irreducible truths that remain after all inherited thinking is removed.

For each bedrock truth:
- State it as a simple, declarative sentence
- Explain WHY it is fundamentally true (not just conventionally accepted)
- Note what constraints or laws make it true (physics, economics, information theory, etc.)

### Phase 4: Rebuild from Fundamentals

Starting from ONLY the bedrock truths, reconstruct understanding of the topic:

1. **Fresh architecture** — What system/approach would you design if you only knew the bedrock truths and had zero knowledge of how it's "usually done"?
2. **Delta analysis** — Compare the rebuilt understanding against conventional wisdom. What changed? What was the conventional approach getting right by accident? What was it getting wrong?
3. **Novel insights** — What non-obvious conclusions emerge from the rebuilt perspective that are invisible from the conventional viewpoint?
4. **Actionable implications** — What should change in practice based on this analysis?

## Output Template

```markdown
# First Principles Analysis: [Topic]

## 1. Assumption Inventory

| # | Assumption | Category | Source |
|---|-----------|----------|--------|
| 1 | [assumption] | Structural/Causal/Boundary/Value/Historical | [where this belief comes from] |
| ... | ... | ... | ... |

## 2. Assumption Verdicts

| # | Assumption | Verdict | Reasoning |
|---|-----------|---------|-----------|
| 1 | [assumption] | Bedrock / Conditional / Inherited | [why this verdict] |
| ... | ... | ... | ... |

### Stripped Assumptions (Inherited thinking removed)
- [assumption that was discarded and why]

## 3. Bedrock Truths

1. **[Truth 1]** — [why this is fundamentally true]
2. **[Truth 2]** — [why this is fundamentally true]
3. ...

## 4. Rebuilt Understanding

### Fresh Architecture
[What you would build/think/do knowing only the bedrock truths]

### Delta vs Conventional Wisdom
| Aspect | Conventional View | First Principles View | Why Different |
|--------|------------------|----------------------|---------------|
| [aspect] | [what people assume] | [what fundamentals say] | [root cause of divergence] |

### Novel Insights
- [insight 1]
- [insight 2]

### Actionable Implications
1. [what to change based on this analysis]
2. [what to change based on this analysis]
```

## Domain Hints

The methodology is universal, but these prompts sharpen analysis per domain:

| Domain | Extra question to ask during Phase 2 |
|--------|--------------------------------------|
| **Technology** | "Is this a fundamental constraint of computation, or a constraint of current tooling?" |
| **Business** | "Is this driven by actual customer behavior, or by what the industry assumes customers want?" |
| **Investment** | "Is this priced in because of real fundamentals, or because of narrative/momentum?" |
| **Product** | "Does the user actually need this, or do we assume they do because competitors offer it?" |
| **Science** | "Is this derived from experimental evidence, or from theoretical models that haven't been falsified?" |

## Examples

### Example 1: Technology topic

User: "First principles analysis of why companies adopt Kubernetes"

**Phase 1 — Assumptions**: "Container orchestration requires K8s", "K8s is the industry standard so it must be right", "You need K8s to scale", "K8s enables microservices which are inherently better"

**Phase 2 — Stripping**: "You need K8s to scale" → **Inherited**. Linux can scale processes without K8s. Many of the world's largest systems (e.g., early Google, Facebook) scaled without K8s. The real need is: a way to distribute workloads across machines and recover from failures.

**Phase 3 — Bedrock**: (1) Distributed systems need a way to schedule work across nodes. (2) Failed processes must be restarted. (3) Network routing must adapt to topology changes.

**Phase 4 — Rebuild**: Any system satisfying these 3 needs works. K8s is one implementation, not a necessity. Simpler alternatives (Nomad, systemd + load balancer, serverless) may satisfy the bedrock needs with less complexity for many workloads.

### Example 2: Business topic

User: "기본 원리 분석: SaaS 가격 정책은 왜 구독 모델이어야 하나?"

**Phase 1 — Assumptions**: "구독이 최적의 수익 모델", "고객은 구독을 선호", "MRR/ARR이 투자자가 보는 핵심 지표"

**Phase 2 — Stripping**: "고객은 구독을 선호" → **Inherited**. 실제 데이터: 구독 피로(subscription fatigue)가 증가 추세. 고객이 원하는 것은 "지속적 가치", not "월 과금".

**Phase 3 — Bedrock**: (1) 소프트웨어 제공에는 지속적 비용(서버, 유지보수)이 발생. (2) 고객은 받는 가치에 비례한 비용을 선호. (3) 예측 가능한 현금 흐름은 사업 운영에 유리.

**Phase 4 — Rebuild**: 구독은 bedrock truth #3을 만족시키는 하나의 방법일 뿐. Usage-based, credit-based, or hybrid 모델이 #1과 #2를 더 잘 만족시킬 수 있음.

## Error Handling

| Scenario | Action |
|----------|--------|
| User provides no specific topic | Ask: "What topic or decision do you want to analyze from first principles?" |
| Topic is too broad ("analyze everything") | Ask the user to narrow to one specific claim, decision, or system |
| User wants code review, not conceptual analysis | Redirect to `deep-review` or `simplify` |
| All assumptions turn out to be bedrock truths | Report honestly — sometimes conventional wisdom IS well-founded. Note which assumptions were closest to being stripped. |
| User disagrees with a verdict | Present the evidence chain and invite counter-evidence. Verdicts are hypotheses, not dogma. |

## Composability

First Principles output feeds into other skills:
- **problem-definition** — Use stripped assumptions to reframe a problem statement
- **pm-product-strategy** — Feed rebuilt understanding into Lean Canvas or SWOT
- **trading-scenario-analyzer** — Use novel insights as scenario inputs
- **presentation-strategist** — Structure a "challenge conventional wisdom" pitch
- **role-dispatcher** — Run multi-role analysis on the rebuilt understanding
