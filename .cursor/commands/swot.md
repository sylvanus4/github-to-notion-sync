---
description: "Run a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) on any product, strategy, or decision"
argument-hint: "<product, company, strategy, or decision to analyze>"
---

# SWOT Analysis

Generate a structured Strengths, Weaknesses, Opportunities, Threats matrix for any subject.

## Usage

```
/swot ThakiCloud AI Platform vs competitors
/swot Launching a freemium tier for our SaaS
/swot 한국 시장에서의 GPU 클라우드 사업 진출
/swot --with-actions Our Q3 product roadmap
/swot --competitive Migrating from monolith to microservices
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Standard 2x2 SWOT matrix (default)
- `--with-actions` — Add strategic actions derived from each quadrant (SO/WO/ST/WT strategies)
- `--competitive` — Add a competitor comparison column alongside the SWOT
- `--weighted` — Add impact scores (1-5) and urgency ratings to each item
- `--with-research` — Perform web research to ground claims with market data

### Workflow

1. **Define subject** — Clearly state what is being analyzed
2. **Research context** (if `--with-research`) — Gather market data, competitor info, and industry trends
3. **Identify Strengths** — Internal advantages, unique capabilities, existing assets (3-5 items)
4. **Identify Weaknesses** — Internal limitations, resource gaps, known pain points (3-5 items)
5. **Identify Opportunities** — External favorable conditions, market trends, unmet needs (3-5 items)
6. **Identify Threats** — External risks, competitive pressures, regulatory changes (3-5 items)
7. **Cross-reference** (if `--with-actions`) — Derive SO/WO/ST/WT strategic actions
8. **Score** (if `--weighted`) — Rate each item on impact (1-5) and urgency (1-5)

### Output Format

```
## SWOT Analysis: [Subject]

| Strengths 💪 | Weaknesses ⚠️ |
|---|---|
| [S1] | [W1] |
| [S2] | [W2] |
| [S3] | [W3] |

| Opportunities 🚀 | Threats 🛡️ |
|---|---|
| [O1] | [T1] |
| [O2] | [T2] |
| [O3] | [T3] |

### Strategic Implications
[2-3 sentences on the most critical insight from the analysis]
```

### Constraints

- Each quadrant must have 3-5 concrete items, not generic platitudes
- Strengths/Weaknesses must be internal (within control)
- Opportunities/Threats must be external (market, regulation, competition)
- Every item should be specific enough to act on — not "good team" but "3 senior ML engineers with production deployment experience"

### Execution

Reference `pm-product-strategy` (`.cursor/skills/pm/pm-product-strategy/SKILL.md`) for SWOT sub-skill methodology. If `--with-research` is set, use `parallel-web-search` (`.cursor/skills/research/parallel-deep-research/SKILL.md`) for market data.
