---
name: ai-trader-orchestrator
description: >-
  Top-level orchestrator chaining all AI-Trader sub-skills into a single daily
  pipeline. Runs authentication, market intelligence, signal feed, heartbeat,
  and optional strategy publishing in sequence with file-first output
  persistence. Korean triggers: "AI-Trader 파이프라인", "AI-Trader 전체 실행",
  "ai4trade 파
---

# AI-Trader Orchestrator

Top-level orchestrator chaining all AI-Trader sub-skills into a single daily pipeline. Runs authentication, market intelligence, signal feed, heartbeat, and optional strategy publishing in sequence with file-first output persistence. Korean triggers: "AI-Trader 파이프라인", "AI-Trader 전체 실행", "ai4trade 파이프라인", "AI-Trader 오케스트레이터", "AI-Trader 일일 실행".

## When to Use

Use when the user asks to "run AI-Trader pipeline", "ai-trader full run", "AI-Trader daily sync", "execute AI-Trader workflow", "AI-Trader 파이프라인", "AI-Trader 전체 실행", "ai4trade 파이프라인", "AI-Trader 오케스트레이터", "AI-Trader 일일 실행", "ai-trader-orchestrator", "full AI-Trader check", or wants to execute the complete AI-Trader integration cycle.

Do NOT use for individual AI-Trader operations (invoke the specific ai-trader-* skill). Do NOT use for the native daily stock pipeline (use today). Do NOT use for Toss Securities operations (use toss-ops-orchestrator). Do NOT use for KIS pipeline (use kis-team). Do NOT use for AlphaEar intelligence pipeline (use alphaear-orchestrator).

## Prerequisites

- AI-Trader credentials configured (see ai-trader-setup)
- `AI_TRADER_AGENT_EMAIL` and `AI_TRADER_AGENT_PASSWORD` (or `AI_TRADER_TOKEN`) in `.env`
- Network access to ai4trade.ai

## Architecture

```
ai-trader-orchestrator
├── Phase 1: ai-trader-setup       (auth/connectivity)
├── Phase 2: ai-trader-market-intel (read-only market data)
├── Phase 3: ai-trader-signal-feed  (community signals)
├── Phase 4: ai-trader-heartbeat    (notifications/tasks)
└── Phase 5: ai-trader-strategy-publisher (optional, gated)
```

Phases 1-4 always run. Phase 5 (publishing) only runs when `AI_TRADER_AUTO_PUBLISH=true` and qualifying signals exist from the `today` pipeline.

## Workflow

### 1. Full Pipeline (CLI)

```bash
python scripts/ai_trader_pipeline_runner.py
```

### 2. Skip Specific Phases

```bash
python scripts/ai_trader_pipeline_runner.py --skip auth
python scripts/ai_trader_pipeline_runner.py --skip heartbeat
```

### 3. Dry Run

```bash
python scripts/ai_trader_pipeline_runner.py --dry-run
```

### 4. Integration with Daily Pipeline

The AI-Trader pipeline integrates into the existing `today` pipeline and `daily-am-orchestrator` as an additional phase. When configured:

- **Morning pipeline**: Runs after the native stock analysis phases
- **Today pipeline**: Phase 5.6 (after analysis, before report generation)

```python
# In today_pipeline_runner.py PHASE_REGISTRY:
{
    "id": "5.6-ai-trader",
    "label": "AI-Trader platform sync (optional)",
    "stage": "ai_trader",
    "legacy_copy": None,
}
```

Skippable with `--skip-ai-trader` flag. Automatically skipped when `AI_TRADER_*` credentials are not configured.

### 5. Programmatic Invocation

```python
import asyncio
from scripts.ai_trader_pipeline_runner import run_pipeline

async def run():
    output_dir = await run_pipeline()
    print(f"Output: {output_dir}")

asyncio.run(run())
```

## Output Structure

```
outputs/ai-trader/{YYYY-MM-DD}/
├── manifest.json
├── phase-1-auth.json
├── phase-2-market-intel.json
├── phase-3-signal-feed.json
└── phase-4-heartbeat.json
```

## Error Handling

| Phase | Failure Behavior |
|-------|-----------------|
| 1-auth | Pipeline aborts (auth is required for subsequent phases) |
| 2-market-intel | Logs warning, continues (read-only, non-critical) |
| 3-signal-feed | Logs warning, continues |
| 4-heartbeat | Logs warning, continues |
| 5-publish (optional) | Logs warning, does not block pipeline completion |

## Composability

This orchestrator is designed to be called by higher-level orchestrators:

- `daily-am-orchestrator` (Phase 4.5: AI-Trader sync)
- `today` pipeline (Phase 7.5: external platform sync)
- `axis-investment` (investment axis workflow)

Each invocation produces dated, immutable output files for audit and replay.
