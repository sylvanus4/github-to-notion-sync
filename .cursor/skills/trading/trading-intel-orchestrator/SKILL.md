---
name: trading-intel-orchestrator
description: >-
  Orchestrate a full market intelligence analysis by dispatching 4 specialist
  analysts in parallel (macro environment, sector rotation, news impact,
  technical charts) then synthesizing their outputs into a unified report with
  contradiction identification and consensus signals. Optionally runs a
  deep-dive on a specific ticker. Use when the user asks for "full market
  analysis", "market intelligence", "trading intel", "comprehensive market
  view", "시장 종합 분석", "시장 인텔리전스", "트레이딩 인텔", "종합 시장 분석",
  or wants multiple market perspectives combined into one report. Do NOT use
  for single-perspective analysis (use the specific analyst skill directly).
  Do NOT use for daily stock screening pipeline (use today). Do NOT use for
  MiroFish simulation (use mirofish).
triggers:
  - full market analysis
  - market intelligence
  - trading intel
  - comprehensive market view
  - 시장 종합 분석
  - 시장 인텔리전스
  - 트레이딩 인텔
  - 종합 시장 분석
tags: [orchestrator, trading, market-intelligence, harness, fan-out-fan-in]
metadata:
  author: "thaki"
  version: "1.0.0"
  pattern: "fan-out/fan-in"
  composes:
    - trading-market-environment-analysis
    - trading-sector-analyst
    - trading-market-news-analyst
    - trading-technical-analyst
    - trading-us-stock-analysis
---

# Trading Market Intelligence Orchestrator

Dispatch 4 market analyst agents in parallel, synthesize their findings into a unified intelligence report, and optionally deep-dive into a specific ticker.

## Usage

```
/trading-intel                          # Full market intelligence (all 4 analysts)
/trading-intel NVDA                     # Full intel + deep-dive on NVDA
/trading-intel --skip sector,tech       # Skip sector and technical analysts
/trading-intel --dry-run                # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `env` | `trading-market-environment-analysis` | included |
| `sector` | `trading-sector-analyst` | included |
| `news` | `trading-market-news-analyst` | included |
| `tech` | `trading-technical-analyst` | included |

## Agent Team

### Model Tier Standard (AutoHedge P3)

Following AutoHedge's role-specific model tiering pattern: data-gathering agents use cheaper/faster models, while synthesis and judgment agents use more capable models.

| Agent | Skill | subagent_type | model | Tier Rationale | Output |
|-------|-------|---------------|-------|----------------|--------|
| Macro Analyst | `trading-market-environment-analysis` | generalPurpose | fast | Data gathering — structured extraction | `_workspace/trading-intel/01_market-environment.md` |
| Sector Analyst | `trading-sector-analyst` | generalPurpose | fast | Data gathering — pattern matching | `_workspace/trading-intel/01_sector-analyst.md` |
| News Analyst | `trading-market-news-analyst` | generalPurpose | fast | Data gathering — content summarization | `_workspace/trading-intel/01_market-news.md` |
| Technical Analyst | `trading-technical-analyst` | generalPurpose | fast | Data gathering — indicator computation | `_workspace/trading-intel/01_technical.md` |
| Follow-up Analyst | (inline — conflict resolution) | generalPurpose | (default) | Judgment — resolves contradictions | `_workspace/trading-intel/02.5_followup_*.md` |
| Deep-Dive Analyst | `trading-us-stock-analysis` | generalPurpose | (default) | Judgment — multi-factor reasoning | `_workspace/trading-intel/03_deep-dive.md` |
| Synthesizer | (main agent) | — | (default) | Judgment — cross-perspective synthesis | `_workspace/trading-intel/02_synthesis.md` |

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for ticker symbol(s) and flags (`--skip`, `--dry-run`).
2. `Shell: mkdir -p _workspace/trading-intel`
3. If `--dry-run`, print the execution plan and stop.

### Phase 1: Parallel Market Analysis (Fan-out)

Launch up to 4 sub-agents via the Task tool in a single message. Max 4 concurrent.

#### Temporal Context (AutoHedge P1)

Every subagent prompt MUST include a system timestamp suffix so the analyst reasons about current market conditions, not stale training-data snapshots:

```
Current date and time: {ISO 8601 timestamp, e.g. 2026-04-14T09:30:00+09:00}
Use this as "now" for all temporal reasoning. Do NOT rely on training-data knowledge for recent dates.
```

For each non-skipped analyst, use this prompt template:

```
You are a {role} specialist.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/trading/{skill-name}/SKILL.md`.

## Task
Analyze the current market from your perspective. Today's date: {date}.
{If ticker provided: "Pay special attention to implications for {ticker}."}

## Output
Write your full analysis to `_workspace/trading-intel/01_{agent-slug}.md` using the Write tool.
Format: Markdown with sections for Key Findings, Signals (bullish/bearish with confidence 0-100), Data Points, and Risks.

## Constraints
- Focus on actionable insights, not general commentary.
- Include specific data points with sources.
- Flag any unusual or extreme readings.
- Assign a confidence score (0-100) to each signal you identify.

## Completion
Return a one-line summary of your key finding.
```

Wait for all Phase 1 agents to complete.

### Phase 2: Synthesis (Fan-in)

Read all Phase 1 output files from `_workspace/trading-intel/01_*.md`.

Produce `_workspace/trading-intel/02_synthesis.md` containing:

1. **Consensus Signals** — points where 2+ analysts agree (direction, strength). Each consensus signal MUST include:
   - `confidence`: 0-100 score based on the average of contributing analysts' individual signal confidences
   - `agreement_count`: how many analysts agree
   - `dissenter`: which analyst (if any) disagrees and why
2. **Contradictions** — points where analysts disagree, with context from each. Each contradiction MUST include:
   - `severity`: HIGH (opposing signals on a key factor like direction or regime) / MEDIUM (differing magnitude) / LOW (nuance disagreement)
   - `confidence_delta`: difference between the conflicting confidence scores
3. **Key Risk Factors** — top 3-5 risks across all perspectives
4. **Market Regime Assessment** — overall market characterization (trending/range-bound, risk-on/off)
5. **Actionable Summary** — top 3 insights ranked by conviction (weighted average confidence)

### Phase 2.5: Directed Follow-up (Conditional)

If Phase 2 synthesis detects any **HIGH-severity contradiction** (2+ analysts with opposing signals on the same factor), spawn a targeted follow-up subagent to resolve the conflict:

1. For each HIGH-severity contradiction, launch 1 Task (max 2 follow-ups per run):

```
You are a conflict resolution analyst.
Current date and time: {ISO 8601 timestamp}

## Contradiction to Resolve
{Paste the contradiction description, including both analysts' positions and confidence scores}

## Task
Gather additional evidence to determine which position is better supported:
1. Search for the most recent data relevant to this disagreement (within the last 48 hours)
2. Check if one analyst may be using outdated information
3. Look for a third-party source that adjudicates the disagreement

## Output
Write to `_workspace/trading-intel/02.5_followup_{contradiction-index}.md`.
Include: verdict (which side is better supported, or "genuinely ambiguous"), evidence, and adjusted confidence score.

## Completion
Return: { "verdict": "analyst_A|analyst_B|ambiguous", "adjusted_confidence": N, "evidence_summary": "one line" }
```

2. After follow-up completes, update the corresponding contradiction in `02_synthesis.md` with the resolution or "ambiguous — both positions have merit" annotation.
3. If no HIGH-severity contradictions exist, skip Phase 2.5 entirely.

### Phase 3: Deep-Dive (Conditional)

If a ticker was specified in `$ARGUMENTS`:

Launch 1 Task for `trading-us-stock-analysis`:

```
You are a comprehensive stock analyst.

## Skill Reference
Read and follow `.cursor/skills/trading/trading-us-stock-analysis/SKILL.md`.

## Context
Read the market synthesis at `_workspace/trading-intel/02_synthesis.md` for macro context.

## Task
Perform a full fundamental + technical analysis of {ticker}.
Incorporate the macro context from the synthesis.

## Output
Write to `_workspace/trading-intel/03_deep-dive.md`.

## Completion
Return a one-line summary with your recommendation.
```

### Phase 4: Final Report

Read `02_synthesis.md` and (if exists) `03_deep-dive.md`.

Produce the final report at `outputs/trading-intel/intel-report-{date}.md`:

```markdown
# Trading Market Intelligence Report — {date}

## Executive Summary
{3-5 bullet synthesis of key findings}

## Market Consensus
{From Phase 2 consensus signals}

## Contradictions & Debates
{From Phase 2 contradictions — present both sides}

## Risk Dashboard
{Top risks with severity rating}

## Market Regime
{Current assessment}

## Deep-Dive: {ticker} (if applicable)
{From Phase 3}

## Analyst Reports
{Links to individual Phase 1 reports for reference}

---
Generated by trading-intel-orchestrator v1.0.0
Analysts: {list of non-skipped analysts}
```

## Error Handling

| Failure | Action |
|---------|--------|
| 1 analyst fails | Retry once. If still fails, proceed without that perspective. Note in report: "_{agent}_ analysis unavailable." |
| 2+ analysts fail | Produce degraded report with available data. Warn user. |
| Synthesis input empty | Abort with error: "No analyst data available." |
| Deep-dive fails | Proceed with synthesis-only report. Note ticker analysis unavailable. |

## Data Flow

```
User input (ticker?, flags)
    │
    ├─► Agent 1: market-environment ──► 01_market-environment.md ─┐
    ├─► Agent 2: sector-analyst     ──► 01_sector-analyst.md     ─┤
    ├─► Agent 3: market-news        ──► 01_market-news.md        ─┼─► Synthesizer ──► 02_synthesis.md
    └─► Agent 4: technical          ──► 01_technical.md          ─┘        │
                                                                           ▼
                                                              (if ticker) Deep-Dive ──► 03_deep-dive.md
                                                                           │
                                                                           ▼
                                                                    Final Report
                                                          outputs/trading-intel/intel-report-{date}.md
```


## Examples

```
User: "시장 종합 분석해줘"
→ Dispatches 4 analysts in parallel, synthesizes, posts intel-report-2026-04-14.md

User: "NVDA에 대한 full market analysis 해줘"
→ 4-analyst fan-out + NVDA deep-dive, outputs intel-report with ticker section

User: "trading intel --skip-news"
→ Skips news analyst, runs remaining 3 + synthesis
```

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
