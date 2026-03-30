---
name: system-thinker
description: >-
  Design end-to-end automated trading analysis systems by mapping data flows,
  identifying bottlenecks, creating feedback loops (prediction vs actual), and
  designing trigger-based automation. Converts manual task-by-task processes into
  interconnected systems with clear inputs, outputs, and feedback mechanisms.
  Use when the user asks to "design a system", "map data flow", "find
  bottlenecks", "create feedback loop", "automate this process end-to-end",
  "system design", "시스템 설계", "데이터 흐름", "병목 분석", "피드백 루프",
  "convert manual to automated", or wants to think about processes as systems
  rather than individual tasks.
  Do NOT use for AI workflow composition (use ai-workflow-integrator).
  Do NOT use for building specific pipelines (use pipeline-builder).
  Do NOT use for microservice architecture review (use backend-expert).
  Do NOT use for infrastructure design (use sre-devops-expert).
metadata:
  author: thaki
  version: 1.0.0
  category: generation
---

# System Thinker

Transform task-by-task thinking into systems thinking for the stock analytics domain. Instead of asking "what do I need to do next?", ask "how much of this could run without me?"

## Meta-Orchestration

### Prompt router (representative user phrases)

| # | Example prompt | This skill? | Delegation order (numbered) | Output merge strategy | User overrides |
|---|----------------|-------------|------------------------------|------------------------|----------------|
| 1 | AI 리포트 품질을 자동 평가해줘 | No | 1) `ai-quality-evaluator` | Evaluation markdown | `DATE`, paths |
| 2 | 데일리 파이프라인을 설계해줘 | Partial | 1) Map current `today` flow (this skill) → 2) `ai-workflow-integrator` to redesign | Map + delta design doc | Scope: whole vs subsystem |
| 3 | 이 프로세스를 자동화할지 결정해줘 | No | 1) `automation-strategist` | — | — |
| 4 | 시스템 데이터 흐름을 분석해줘 | Yes | 1) Boundaries → 2) Data flow trace → 3) Components table → 4) Bottlenecks → 5) Optional `visual-explainer` | **Single** system map + bottleneck appendix (text or HTML link) | `DEPTH=shallow|full`; include feedback loops Y/N |
| 5 | 프로젝트 컨텍스트를 업데이트해줘 | No | 1) `context-engineer` | MEMORY / packages | — |

### Error recovery

| Failure mode | Retry | Fallback | Abort |
|--------------|-------|----------|-------|
| Incomplete logs/metrics | — | Annotate unknown durations; suggest instrumentation | — |
| `visual-explainer` unavailable | — | Text/ASCII diagram per troubleshooting table | — |
| Scope creep | — | Split into subsystems; prioritize one tracer bullet | — |

### Output aggregation

Combine **map + component table + bottleneck ranked list + recommended fixes** into one deliverable. If HTML diagram produced, link it from the top summary.

## Core Framework: DFTS (Data-Flow-Trigger-State)

Every system in this project can be decomposed into four elements:

| Element | Question | Example |
|---------|----------|---------|
| **Data** | What information flows through? | Stock prices, signals, reports |
| **Flow** | How does it move between components? | DB → Script → JSON → Slack |
| **Triggers** | What starts each step? | Cron schedule, price threshold, manual command |
| **State** | What persists between runs? | DB records, signal history, MEMORY.md |

## Workflow

### Mode 1: System Mapping

Create a visual map of an existing or proposed system.

**Step 1 — Identify system boundaries:**

Ask or determine:
- What is the system's purpose? (daily analysis, event response, data collection)
- What are the inputs? (market data, news, user commands)
- What are the outputs? (reports, Slack messages, DB records)
- What are the external dependencies? (Yahoo Finance, Slack API, PostgreSQL)

**Step 2 — Map the data flow:**

Trace data from source to destination:

```
[External Source] → [Ingestion] → [Storage] → [Processing] → [Analysis] → [Output]
```

For this project's daily pipeline:

```
Yahoo Finance ──→ weekly_stock_update.py ──→ PostgreSQL
                                                │
Wikipedia/KRX ──→ discover_hot_stocks.py ───────┤
                                                │
                                                ▼
                                    daily_stock_check.py
                                                │
                    ┌───────────────────────────┤
                    ▼                           ▼
            alphaear-news              analysis JSON
                    │                           │
                    ▼                           ▼
          alphaear-sentiment        generate-report.js
                    │                           │
                    └──────────┬────────────────┘
                               ▼
                        daily-{date}.docx
                               │
                               ▼
                        Slack #h-report
```

**Step 3 — Identify components:**

For each component, document:
- Input format and source
- Processing logic (brief)
- Output format and destination
- Error behavior (retry, skip, abort)
- Current trigger (manual, cron, dependency)

**Step 4 — Produce the system map:**

Use the `visual-explainer` skill to generate an interactive HTML diagram, or produce a text-based diagram. Include:
- All data sources and sinks
- Processing nodes with their scripts/skills
- Data format annotations (JSON, CSV, .docx)
- Trigger annotations (cron, manual, event)

### Mode 2: Bottleneck Analysis

Identify performance and reliability bottlenecks in an existing system.

**Step 1 — Profile each stage:**

For each component in the system map, assess:

| Metric | How to Measure |
|--------|----------------|
| Duration | Run the script/skill and time it |
| Reliability | Check logs for failure frequency |
| Data freshness | Compare output timestamp to real-time |
| Resource usage | Check DB connections, API rate limits |

**Step 2 — Classify bottlenecks:**

| Type | Symptom | Example |
|------|---------|---------|
| **Throughput** | Stage takes too long | Yahoo Finance fetch for 50+ tickers |
| **Reliability** | Stage fails intermittently | API rate limiting, network timeouts |
| **Freshness** | Data is stale by the time it's used | Weekday-only data on Monday morning |
| **Coupling** | One failure cascades to everything | DB down blocks all analysis |
| **Manual** | Requires human intervention | Manually triggering discovery |

**Step 3 — Prioritize fixes:**

Rank bottlenecks by impact (how much they slow or block) and effort (how hard to fix):

```
High Impact + Low Effort  → Fix immediately
High Impact + High Effort → Plan for next sprint
Low Impact + Low Effort   → Fix when convenient
Low Impact + High Effort  → Ignore
```

**Step 4 — Propose solutions:**

For each high-priority bottleneck, suggest:
1. The specific change needed
2. Which file(s) to modify
3. Expected improvement
4. Risk of the change

### Mode 3: Feedback Loop Design

Create closed-loop systems where outputs inform future inputs.

**Step 1 — Identify the prediction:**

What does the system predict or recommend?
- Buy/sell signals
- Price direction
- Market sentiment

**Step 2 — Define the ground truth:**

What actually happened?
- Actual price movement (next day, next week)
- Whether the recommendation was profitable
- Whether the sentiment was accurate

**Step 3 — Design the feedback mechanism:**

```
[Prediction] ──→ [Action/Record] ──→ [Wait Period] ──→ [Measure Outcome]
                                                              │
                                                              ▼
                                                    [Compare to Prediction]
                                                              │
                                                              ▼
                                                    [Update Model/Params]
```

Concrete example for signal accuracy tracking:

```
daily_stock_check signals ──→ Store signal + date + price
                                        │
                              (wait 5 trading days)
                                        │
                                        ▼
                              Fetch actual price change
                                        │
                                        ▼
                              Compare: did BUY stocks go up?
                                        │
                                        ▼
                              Update signal confidence weights
```

**Step 4 — Define metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| Signal accuracy | Correct signals / Total signals | > 60% |
| BUY precision | Profitable BUYs / Total BUYs | > 55% |
| SELL precision | Profitable SELLs / Total SELLs | > 55% |
| Coverage | Signals generated / Total tickers | > 80% |

### Mode 4: Manual-to-System Conversion

Transform a manual process into an automated system.

**Step 1 — Document the manual process:**

List every step the user currently does manually:
1. What they do
2. When they do it
3. What data they use
4. What decision they make
5. What output they produce

**Step 2 — Classify each step:**

| Category | Can Automate? | How |
|----------|---------------|-----|
| Data collection | Yes | Script + cron |
| Data transformation | Yes | Script |
| Rule-based decision | Yes | Script with thresholds |
| Judgment call | Partially | AI + human review |
| Creative output | Partially | AI draft + human edit |
| Relationship/trust | No | Keep manual |

**Step 3 — Design the automated system:**

For each automatable step:
1. Identify the existing script or skill
2. Define the trigger (cron, event, threshold)
3. Define the input/output contract
4. Set the error policy
5. Identify human checkpoints (for "partially" items)

**Step 4 — Build incrementally:**

Follow the tracer bullet strategy:
1. Automate one critical path end-to-end
2. Verify it works reliably for 1 week
3. Add the next path
4. Repeat until the full system is automated

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| System map too complex | Too many components | Group related components into subsystems |
| Bottleneck analysis returns no data | Scripts not instrumented | Time each script manually with `time` command |
| Feedback loop has no ground truth | Outcome data not captured | Design a storage mechanism first (DB table or JSON file) |
| Manual-to-system conversion stalls | Process has too many judgment calls | Focus on automating data collection first, keep judgment manual |
| Diagram generation fails | visual-explainer skill unavailable | Fall back to text-based ASCII diagrams |

## Examples

### Example 1: Map the current daily pipeline

User says: "Show me the system map for our daily analysis"

Actions:
1. Trace data flow from Yahoo Finance through all scripts to Slack
2. Annotate each stage with duration, trigger, and data format
3. Generate an interactive diagram using visual-explainer
4. Identify bottlenecks (Yahoo fetch time, report generation)

### Example 2: Design a signal accuracy feedback loop

User says: "I want to track whether our buy signals are actually profitable"

Actions:
1. Define prediction: daily BUY signals from daily_stock_check
2. Define ground truth: actual price 5 days later from DB
3. Design storage: signal_history table with signal, price, date
4. Design comparison: weekly script to compute accuracy
5. Design feedback: adjust signal weights based on accuracy

### Example 3: Convert manual weekly review to automated

User says: "I manually check 5 stocks every Monday -- automate this"

Actions:
1. Document: which 5 stocks, what do you check, what decisions
2. Map to existing scripts: weekly_stock_update + daily_stock_check
3. Create: Monday cron trigger, filtered analysis, Slack summary
4. Keep: human review of the summary before acting

## Integration

- **Visualization**: `visual-explainer` skill (interactive HTML diagrams)
- **Logic flow**: `alphaear-logic-visualizer` (Draw.io XML for finance logic)
- **Pipeline building**: `pipeline-builder` (build what this skill designs)
- **Workflow composition**: `ai-workflow-integrator` (AI-specific workflows)
- **Scripts**: `backend/scripts/` directory
- **DB models**: `backend/app/models/`
