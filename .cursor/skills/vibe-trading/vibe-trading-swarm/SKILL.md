---
name: vibe-trading-swarm
description: >-
  Orchestrate multi-agent swarm teams via Vibe-Trading MCP: browse 29 presets,
  launch DAG-based agent teams, poll progress, and extract final reports.
  Use when the user asks to "run vibe swarm", "investment committee analysis",
  "multi-agent finance team", "vibe-trading swarm", "바이브 스웜",
  "멀티에이전트 분석", "투자위원회 분석", or wants collaborative AI agent
  research through Vibe-Trading's swarm system.
  Do NOT use for MiroFish simulations (use mirofish or mirofish-financial-sim).
  Do NOT use for project's role-dispatcher (use role-dispatcher).
  Do NOT use for setup (use vibe-trading-setup).
tags: [vibe-trading, swarm, multi-agent, team, orchestration]
version: 1.0.0
---

# Vibe-Trading Swarm Teams

## Overview

Vibe-Trading's swarm system runs multi-agent teams through DAG-based workflows.
Each preset defines specialized agents (bull/bear analysts, risk officers,
portfolio managers, quant researchers) that collaborate in topologically-ordered
layers. 29 pre-configured presets cover investment committees, quant desks,
cross-market analysis, risk committees, and more.

## Workflow

### Step 1: Discover Presets

```
CallMcpTool server=user-vibe-trading toolName=list_swarm_presets arguments={}
```

Returns an array with preset names, descriptions, agent counts, and required
variables. Key presets include:

| Preset | Agents | Purpose | Required Variables |
|--------|--------|---------|--------------------|
| `investment_committee` | 4 | Bull/bear/risk/PM analysis | `target`, `market` |
| `quant_strategy_desk` | 3-5 | Quant strategy design + validation | `target`, `market`, `strategy_type` |
| `risk_committee` | 3-4 | Portfolio risk assessment | `portfolio`, `market` |
| `cross_market_desk` | 4-6 | Cross-market correlation analysis | `targets`, `markets` |
| `crypto_trading_desk` | 3-4 | Crypto-specific trading analysis | `target`, `exchange` |

### Step 2: Launch a Swarm

```
CallMcpTool server=user-vibe-trading toolName=run_swarm
arguments={
  "preset_name": "investment_committee",
  "variables": {
    "target": "AAPL.US",
    "market": "US"
  }
}
```

`run_swarm` is **blocking** -- it polls internally and returns the final result
once all agents complete. If the run exceeds 30 minutes, it may time out and
return a partial status. In that case, use `get_swarm_status(run_id)` to check
whether the run completed after the timeout, then `get_run_result(run_id)` to
retrieve the final report.

### Step 3: Read Results

The response contains:

```json
{
  "status": "completed",
  "preset": "investment_committee",
  "run_id": "abc-123",
  "final_report": "## Investment Committee Report\n...",
  "tasks": [
    {"id": "t1", "agent_id": "bull_analyst", "status": "completed", "summary": "..."},
    {"id": "t2", "agent_id": "bear_analyst", "status": "completed", "summary": "..."},
    {"id": "t3", "agent_id": "risk_officer", "status": "completed", "summary": "..."},
    {"id": "t4", "agent_id": "portfolio_manager", "status": "completed", "summary": "..."}
  ],
  "total_input_tokens": 45000,
  "total_output_tokens": 12000
}
```

Key fields:
- `final_report`: The synthesized report from the last agent in the DAG
- `tasks[].summary`: Individual agent outputs accessible for detailed review
- Token counts for cost tracking

### Step 4: Historical Runs

```
CallMcpTool server=user-vibe-trading toolName=list_runs arguments={"limit": 10}
```

Retrieve details for a specific past run:

```
CallMcpTool server=user-vibe-trading toolName=get_run_result arguments={"run_id": "abc-123"}
```

## DAG Execution Model

Swarm teams execute as directed acyclic graphs:

```
Layer 0 (parallel):  bull_analyst, bear_analyst
                          |              |
Layer 1:              risk_officer (receives both outputs)
                          |
Layer 2:           portfolio_manager (final synthesis)
```

- Agents in the same layer run in parallel
- Each agent receives outputs from all upstream agents
- The final layer's output becomes `final_report`

## Integration with Project Skills

| Scenario | Vibe-Trading Swarm | Project Equivalent |
|----------|-------------------|--------------------|
| Multi-perspective analysis | `run_swarm("investment_committee")` | `role-dispatcher` (12 roles) |
| Market simulation | Not simulating; research-only | `mirofish` (simulation engine) |
| Strategy validation | `run_swarm("quant_strategy_desk")` | `daily-strategy-engine` (7 strategies) |

**Complementary use**: Run a vibe-trading swarm for deep research on a specific
stock, then feed findings into the project's `today` pipeline for operational
signals.

## Cost Awareness

Each swarm run consumes LLM tokens based on agent count and task complexity.
The response includes `total_input_tokens` and `total_output_tokens` for
cost tracking. Typical costs:

| Preset | Approximate Tokens | Cost (GPT-4o) |
|--------|-------------------|---------------|
| 3-agent team | 30-50K | ~$0.15-0.25 |
| 5-agent team | 50-100K | ~$0.25-0.50 |
| 6-agent team | 80-150K | ~$0.40-0.75 |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `DAG validation failed` | Circular dependency or missing agent | Check preset YAML |
| `Swarm timed out` | Agents took > 30 min | Simplify variables or reduce agent count |
| `Run record lost` | Store corruption | Retry the run |
| `preset not found` | Typo in preset name | Call `list_swarm_presets` first |
