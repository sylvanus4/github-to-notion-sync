---
name: mirofish-opinion-sim
description: Run public opinion and social media reaction simulations using MiroFish multi-agent engine — predict how communities, media, regulators, and consumers respond to events, crises, or announcements through swarm intelligence on simulated Twitter/Reddit platforms. Use when the user asks to "simulate public reaction", "opinion simulation", "crisis simulation", "PR impact prediction", "social media prediction", "여론 시뮬레이션", "위기 시뮬레이션", "PR 영향 예측", "mirofish-opinion", or any request to simulate public opinion dynamics. Do NOT use for financial market simulations (use mirofish-financial-sim). Do NOT use for general MiroFish operations (use mirofish). Do NOT use for actual Twitter scraping (use twitter-timeline-to-slack).
---

# MiroFish Public Opinion Simulation

## Overview

Specialized workflow for simulating public opinion dynamics on dual social media platforms (Twitter + Reddit). Creates digital communities of diverse stakeholders who react to news events, product launches, policy announcements, and crises.

## Prerequisites

Same as the `mirofish` skill. Verify: `curl -s http://localhost:5001/health`

## Workflow

### Step 1: Prepare Opinion Seed Document

Compile background context:
- Company/organization profile and history
- Product/service documentation
- Past public incidents or controversies
- Key stakeholder positions and influence networks
- Relevant social media history and sentiment baselines

### Step 2: Configure Opinion Simulation

```bash
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "<graph_id>",
    "prediction_requirement": "Simulate public reaction across Twitter and Reddit if a safety incident with our autonomous vehicle goes viral. Track sentiment trajectory over 7 days. Include consumer advocates, regulators, industry analysts, competing brands, general public, and media. Predict boycott probability and regulatory response likelihood.",
    "num_rounds": 25
  }'
```

### Step 3: Opinion-Specific God's Eye Injections

| Round | Event Type | Example |
|-------|-----------|---------|
| 5 | Initial incident | "Viral video surfaces showing product safety failure" |
| 10 | Media amplification | "Major news outlet publishes investigative report" |
| 12 | Company response | "CEO issues public statement and recall notice" |
| 18 | Regulatory action | "Government agency announces investigation" |
| 22 | Resolution attempt | "Company offers free replacement and compensation" |

### Step 4: Analyze Opinion Dynamics

Key analyses after simulation:

1. **Sentiment trajectory:** Plot sentiment scores per round to identify tipping points
2. **Influence mapping:** Identify which agent types amplified vs dampened the crisis
3. **Platform comparison:** Compare Twitter (fast, emotional) vs Reddit (slower, analytical) reactions
4. **Narrative evolution:** Track how the dominant narrative shifted across rounds
5. **Intervention effectiveness:** Measure the impact of each God's Eye injection (company response, regulatory action)

### Step 5: Generate Crisis Response Plan

Use ReportAgent chat to generate actionable recommendations:

```bash
curl -X POST http://localhost:5001/api/report/chat \
  -d '{
    "report_id": "<report_id>",
    "message": "Based on the simulation results, recommend the optimal crisis response timeline: when to issue a statement, when to announce remediation, and which stakeholder group to address first."
  }'
```

## Simulation Platform Options

MiroFish supports dual social media platforms, selected via the `platform_type` parameter at simulation creation (not invoked directly):

| Platform | Best For |
|----------|----------|
| `twitter` | Fast-moving opinion dynamics, real-time reactions, short-form takes |
| `reddit` | Deep discussion, community deliberation, long-form analysis |
| Both (parallel) | Cross-platform dynamics (recommended for comprehensive analysis) |

## Agent Archetypes for Opinion Simulation

- **Consumer advocate** — vocal, community-oriented, boycott-prone
- **Industry journalist** — narrative-shaping, investigation-oriented
- **Government regulator** — cautious, precedent-following, policy-driven
- **Competing brand** — opportunistic, indirect commentary
- **Influencer/KOL** — high-reach, opinion-amplifying
- **General public** — varied, herd-following, emotionally reactive
- **Company employee** — defensive, insider perspective, leaked information potential

## Error Handling

| Error | Action |
|-------|--------|
| MiroFish backend unreachable | Start with `cd ~/thaki/MiroFish && npm run dev`. Verify: `curl -s http://localhost:5001/health` |
| Simulation create fails | Ensure `graph_id` exists — build graph first using `mirofish` skill Phase 1 |
| No stakeholder agents generated | Seed document may lack diverse perspectives. Add explicit stakeholder descriptions. |
| Platform comparison unclear | Use parallel mode (`both`) to see how the same event plays out differently on Twitter vs Reddit |
| LLM API quota exceeded | Reduce `num_rounds` or use a more cost-effective model |

## Examples

```
/mirofish-opinion -- Simulate public reaction if our CEO makes a controversial political statement
/mirofish-opinion -- Predict 7-day social media trajectory after a product recall announcement
/mirofish-opinion -- How would Chinese social media react to a new data privacy regulation?
/mirofish-opinion -- Simulate university campus response to a controversial policy change
```
