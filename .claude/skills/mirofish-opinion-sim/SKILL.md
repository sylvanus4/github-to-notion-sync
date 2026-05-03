---
name: mirofish-opinion-sim
description: >-
  Run public opinion and social media reaction simulations using MiroFish
  multi-agent engine — predict how communities, media, regulators, and
  consumers respond to events, crises, or announcements through swarm
  intelligence on simulated Twitter/Reddit platforms. Use when the user asks
  to "simulate public reaction", "opinion simulation", "crisis simulation",
  "PR impact prediction", "social media prediction", "여론 시뮬레이션", "위기 시뮬레이션",
  "PR 영향 예측", "mirofish-opinion", or any request to simulate public opinion
  dynamics. Do NOT use for financial market simulations (use
  mirofish-financial-sim). Do NOT use for general MiroFish operations (use
  mirofish). Do NOT use for actual Twitter scraping (use
  twitter-timeline-to-slack).
---

# MiroFish Public Opinion Simulation

## Overview

Specialized workflow for simulating public opinion dynamics on dual social media platforms (Twitter + Reddit). Creates digital communities of diverse stakeholders who react to news events, product launches, policy announcements, and crises.

## Prerequisites

Same as the `mirofish` skill. Verify: `curl -s http://localhost:5001/health`

## Quality Contract (aligned with simulation evals)

### EVAL 1 — Opinion / policy seed document

Build a markdown seed before ontology with:

| Element | Requirement |
|--------|-------------|
| Title | H1 describing the controversy or policy (e.g. `# AI Regulation Bill — Public Reaction`) |
| Date | ISO `YYYY-MM-DD` |
| Sections | ≥3 `##` sections: Background, Stakeholders & platforms, Incident or policy text, Hypothesized narrative arcs |
| Entities | ≥5 named actors (regulators, companies, NGOs, media, geographies) |

For *AI 규제법 통과* scenarios, include bill summary bullets, jurisdiction, enforcement body, and which communities (developers, enterprises, general public) are modeled.

### EVAL 2 — Simulation parameters

| Parameter | Default | Override |
|-----------|---------|----------|
| Topic | User scenario → `simulation_requirement` (ontology multipart) | Tighten scope if graph explodes |
| Agents | ~26 after prepare | More diverse stakeholders in seed → richer personas |
| Rounds | 20–25 for viral/PR arcs | Stop with `/api/simulation/stop` when target rounds reached |
| `project_name` | `Opinion-{slug}-{date}` | User label |

Platforms: MiroFish dual Twitter + Reddit is the default for full opinion runs (see **Simulation Platform Options**).

### EVAL 3 — Report output structure

Deliver to the user:

1. **Primary prediction** — e.g. boycott likelihood, trust shift, regulatory probability
2. **Confidence** — qualitative + why (agent coverage, seed strength)
3. **≥3 key factors** — narrative, influencer/regulator actions, platform differences
4. **Consensus / divergence** — which cohorts (media vs public vs policymakers) aligned or split

### EVAL 4 — Canonical API paths

Full pipeline matches `mirofish`:

`POST /api/graph/ontology/generate` → `POST /api/graph/build` → `GET /api/graph/task/<task_id>` → `POST /api/simulation/create` with `{"project_id","graph_id"}` → `prepare` + `prepare/status` → `POST /api/simulation/start` → `GET .../run-status` → `POST /api/report/generate` + status poll → `GET /api/report/<report_id>`.

Do not use undocumented JSON fields on `simulation/create` in place of graph+prepare.

## Workflow

### Step 1: Prepare Opinion Seed Document

Compile background context:

- Company/organization profile and history
- Product/service documentation
- Past public incidents or controversies
- Key stakeholder positions and influence networks
- Relevant social media history and sentiment baselines

Validate against the EVAL 1 table, then save to `/tmp/mirofish-opinion-seed-{date}.md`.

### Step 2: Ontology, graph, simulation (same API order as mirofish)

```bash
curl -X POST http://localhost:5001/api/graph/ontology/generate \
  -F "files=@/tmp/mirofish-opinion-seed-{date}.md" \
  -F "simulation_requirement=<predict multi-day opinion trajectory across Twitter and Reddit for this scenario>" \
  -F "project_name=Opinion-{slug}-{date}"

curl -X POST http://localhost:5001/api/graph/build \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>"}'

# Poll GET /api/graph/task/<task_id> until graph ready → graph_id

curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>", "graph_id": "<graph_id>"}'

curl -X POST http://localhost:5001/api/simulation/prepare \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'

curl -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
```

### Step 3: Opinion-specific God’s Eye injections

| Round | Event Type | Example |
|-------|-----------|---------|
| 5 | Initial incident | Viral video surfaces showing product safety failure |
| 10 | Media amplification | Major news outlet publishes investigative report |
| 12 | Company response | CEO issues public statement and recall notice |
| 18 | Regulatory action | Government agency announces investigation |
| 22 | Resolution attempt | Company offers free replacement and compensation |

### Step 4: Analyze opinion dynamics

1. **Sentiment trajectory** — sentiment shifts per round at injection points (`GET /api/simulation/<id>/timeline` when available)
2. **Influence mapping** — which agent types amplified vs dampened the crisis
3. **Platform comparison** — Twitter (fast, emotional) vs Reddit (slower, analytical)
4. **Narrative evolution** — how the dominant narrative shifted across rounds
5. **Intervention effectiveness** — impact of each God’s Eye injection

### Step 5: ReportAgent chat (optional structured follow-up)

```bash
curl -X POST http://localhost:5001/api/report/chat \
  -H "Content-Type: application/json" \
  -d '{"report_id": "<report_id>", "message": "Based on the simulation results, recommend the optimal crisis response timeline: when to issue a statement, when to announce remediation, and which stakeholder group to address first."}'
```

## Simulation Platform Options

MiroFish supports dual social media platforms. Platform selection is configured in the MiroFish product layer when creating or preparing simulations; document the intent in `simulation_requirement` (e.g. “model both Twitter and Reddit”). Do not assume a `platform_type` JSON field unless your deployed backend version documents it.

| Platform | Best For |
|----------|----------|
| Twitter | Fast-moving opinion dynamics, real-time reactions, short-form takes |
| Reddit | Deep discussion, community deliberation, long-form analysis |
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
| Simulation create fails | Ensure `project_id` and `graph_id` exist — complete Phase 1 graph build first |
| No stakeholder agents generated | Enrich seed with diverse perspectives (EVAL 1) |
| Platform comparison unclear | State in `simulation_requirement` that both Twitter and Reddit must be modeled |
| LLM API quota exceeded | Reduce rounds or use a more cost-effective model |

## Examples

```
/mirofish-opinion -- Simulate public reaction if our CEO makes a controversial political statement
/mirofish-opinion -- Predict 7-day social media trajectory after a product recall announcement
/mirofish-opinion -- How would Chinese social media react to a new data privacy regulation?
/mirofish-opinion -- Simulate university campus response to a controversial policy change
```
