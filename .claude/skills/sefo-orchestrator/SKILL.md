---
name: sefo-orchestrator
description: >-
  Orchestrate complex tasks via SEFO's Skill-Aware Dynamic Orchestration
  (SADO) API. Decomposes tasks into optimal skill compositions using
  governance-aware routing, cost-constrained DAG optimization, and automated
  subagent execution. Use when the user asks to "SEFO route", "sefo
  orchestrate", "skill-aware routing", "SADO route", "SEFO 오케스트레이션", "스킬 라우팅",
  "SADO 라우팅", or any task that benefits from automated multi-skill composition
  with trust and cost awareness. Do NOT use for manual skill execution (invoke
  skills directly), federation operations (use sefo-federation), or
  governance/trust operations (use sefo-governance).
disable-model-invocation: true
---

# SEFO Orchestrator

Orchestrate complex tasks using SEFO's Skill-Aware Dynamic Orchestration (SADO) pipeline. This skill extends the agent abstraction from 4-tuple to 5-tuple (Instruction, Context, Tools, Model, Skills) with cost-aware compositional routing.

## Instructions

### Input

- A natural language task description
- Optional budget constraint (default: 100.0 cost units)
- Optional compliance requirements (e.g., ["signed_only", "trust_above_0.7"])

### Orchestration Pipeline

1. **Route via SADO**: Call `POST /api/v1/sefo/sado/route` with:
   ```json
   {
     "task_description": "<task>",
     "budget": 100.0,
     "compliance": ["signed_only"]
   }
   ```
   This returns:
   - `selected_skills`: Skills chosen by the governance-aware router
   - `composition_path`: Optimal execution order (DAG path)
   - `total_cost`: Estimated cost within budget
   - `governance_scores`: Per-skill trust/compliance scores

2. **Validate Composition**: Verify the composition path is a valid DAG by checking `GET /api/v1/sefo/sado/graph`. Ensure no circular dependencies and all required skills are active.

3. **Execute Sequentially**: For each skill in `composition_path`:
   - Launch a subagent with `subagent_type="generalPurpose"` and the skill's instructions
   - Pass the previous step's output as context to the next step
   - Record execution outcome for trust scoring

4. **Record Results**: After execution:
   - POST success/failure to `POST /api/v1/sefo/tsg/trust/update` for each skill used
   - Ingest the execution trace to `POST /api/v1/sefo/traces/ingest` for future grammar induction

### Example

```
User: "SEFO로 이 논문 분석하고 슬랙에 공유해줘"

1. Route task -> [paper-review, md-to-notion, slack-post]
2. Execute paper-review subagent
3. Execute md-to-notion subagent with review output
4. Execute slack-post subagent with Notion link
5. Record trust observations for all 3 skills
```

### Cost Awareness

The router applies Proposition 2's greedy (1 - 1/e) approximation to find the optimal skill composition under budget constraint. If total cost exceeds budget:
- Downgrade to cheaper model tiers
- Reduce skill count to essential-only
- Report budget overage to user

### Governance Context

The tri-encoder architecture considers:
- **Task affinity**: How well each skill matches the task semantically
- **Trust score**: Bayesian trust from past executions (Beta-Binomial)
- **Provenance depth**: How well-established the skill's lineage is
- **Compliance**: Whether the skill meets required compliance flags


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
