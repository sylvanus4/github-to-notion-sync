---
name: trading-market-breadth-analyzer
description: >-
  Quantifies market breadth health using TraderMonty's public CSV data.
  Generates a 0-100 composite score across 6 components (100 = healthy). Use
  when the user asks "is the market rally broad-based", "how healthy is market
  breadth", "market participation rate", "advance-decline health", "market
  narrowing", "마켓 브레드스", "시장 참여율", "상승 폭 분석". Do NOT use for daily stock
  signals (use daily-stock-check). Do NOT use for chart-based breadth analysis
  (use trading-breadth-chart-analyst).
---

# Market Breadth Analyzer Skill

## Purpose

Quantify market breadth health using a data-driven 6-component scoring system (0-100). Uses TraderMonty's publicly available CSV data to measure how broadly the market is participating in a rally or decline.

**Score direction:** 100 = Maximum health (broad participation), 0 = Critical weakness.

**No API key required** - uses freely available CSV data from GitHub Pages.

## When to Use This Skill

**English:**
- User asks "Is the market rally broad-based?" or "How healthy is market breadth?"
- User wants to assess market participation rate
- User asks about advance-decline indicators or breadth thrust
- User wants to know if the market is narrowing (fewer stocks participating)
- User asks about equity exposure levels based on breadth conditions

**Japanese:**
- 「マーケットブレッドスはどうですか？」「市場の参加率は？」
- 「上昇は広がっている？」「一部の銘柄だけの上昇？」
- ブレッドス指標に基づくエクスポージャー判断
- 市場の健康度をデータで確認したい

## Difference from Breadth Chart Analyst

| Aspect | Market Breadth Analyzer | Breadth Chart Analyst |
|--------|------------------------|----------------------|
| Data Source | CSV (automated) | Chart images (manual) |
| API Required | None | None |
| Output | Quantitative 0-100 score | Qualitative chart analysis |
| Components | 6 scored dimensions | Visual pattern recognition |
| Repeatability | Fully reproducible | Analyst-dependent |

---

## Execution Workflow

### Phase 1: Execute Python Script

Run the analysis script:

```bash
python3 skills/trading-market-breadth-analyzer/scripts/market_breadth_analyzer.py \
  --detail-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" \
  --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv" \
  --output-dir outputs/reports/trading/
```

The script will:
1. Fetch detail CSV (~2,500 rows, 2016-present) and summary CSV (8 metrics)
2. Validate data freshness (warn if > 5 days old)
3. Calculate all 6 component scores (with automatic weight redistribution if any component lacks data)
4. Generate composite score with zone classification
5. Track score history and compute trend (improving/deteriorating/stable)
6. Output JSON and Markdown reports

### Phase 2: Present Results

Present the generated Markdown report to the user, highlighting:
- Composite score and health zone
- Strongest and weakest components
- Recommended equity exposure level
- Key breadth levels to watch
- Any data freshness warnings

### Phase 2b: Trading Analysis Eval Contract (Mandatory)

Structure every **user-facing** answer (after the script runs, or if the script fails) so it passes five binary gates:

| Gate | Pass condition |
|------|----------------|
| **Structured output** | Include `## Summary`, `## Composite & Components`, `## Equity Guidance`, `## Recommendation`, `## Risks & Data Caveats`. |
| **Specific numbers** | Cite **≥3** values from the generated JSON/Markdown (e.g. composite 0–100, one component score, data `as-of` date or days-since-update). |
| **Actionable conclusion** | Map score → health zone → explicit equity exposure **band** from the zone table (e.g. 75–90%). |
| **Risk awareness** | State **≥1** risk: stale data (>5 days), weight redistribution, or history trend (improving/deteriorating). |
| **No hallucinated data** | Numbers must trace to script output; if fetch failed, say so—do not invent breadth levels. |

**Text-only requests (no run yet):** Run the script first when possible; if blocked, output the same header structure and state the exact CLI from Phase 1.

---

## 6-Component Scoring System

| # | Component | Weight | Key Signal |
|---|-----------|--------|------------|
| 1 | Breadth Level & Trend | **25%** | Current 8MA level + 200MA trend direction + 8MA direction modifier |
| 2 | 8MA vs 200MA Crossover | **20%** | Momentum via MA gap and direction |
| 3 | Peak/Trough Cycle | **20%** | Position in breadth cycle |
| 4 | Bearish Signal | **15%** | Backtested bearish signal flag |
| 5 | Historical Percentile | **10%** | Current vs full history distribution |
| 6 | S&P 500 Divergence | **10%** | Multi-window (20d + 60d) price vs breadth divergence |

**Weight Redistribution:** If any component lacks sufficient data (e.g., no peak/trough markers detected), it is excluded and its weight is proportionally redistributed among the remaining components. The report shows both original and effective weights.

**Score History:** Composite scores are persisted across runs (keyed by data date). The report includes a trend summary (improving/deteriorating/stable) when multiple observations are available.

## Health Zone Mapping (100 = Healthy)

| Score | Zone | Equity Exposure | Action |
|-------|------|-----------------|--------|
| 80-100 | Strong | 90-100% | Full position, growth/momentum favored |
| 60-79 | Healthy | 75-90% | Normal operations |
| 40-59 | Neutral | 60-75% | Selective positioning, tighten stops |
| 20-39 | Weakening | 40-60% | Profit-taking, raise cash |
| 0-19 | Critical | 25-40% | Capital preservation, watch for trough |

---

## Data Sources

**Detail CSV:** `market_breadth_data.csv`
- ~2,500 rows from 2016-02 to present
- Columns: Date, S&P500_Price, Breadth_Index_Raw, Breadth_Index_200MA, Breadth_Index_8MA, Breadth_200MA_Trend, Bearish_Signal, Is_Peak, Is_Trough, Is_Trough_8MA_Below_04

**Summary CSV:** `market_breadth_summary.csv`
- 8 aggregate metrics (average peaks, average troughs, counts, analysis period)

Both are publicly hosted on GitHub Pages - no authentication required.

## Output Files

- JSON: `outputs/reports/trading/market_breadth_YYYY-MM-DD_HHMMSS.json`
- Markdown: `outputs/reports/trading/market_breadth_YYYY-MM-DD_HHMMSS.md`
- History: `outputs/reports/trading/market_breadth_history.json` (persists across runs, max 20 entries)

## Reference Documents

### `references/breadth_analysis_methodology.md`
- Full methodology with component scoring details
- Threshold explanations and zone definitions
- Historical context and interpretation guide

### When to Load References
- **First use:** Load methodology reference for framework understanding
- **Regular execution:** References not needed - script handles scoring

## Examples

### Example 1: Breadth health check
**User:** "Is the market rally broad-based? How healthy is market breadth?"
**Action:** Runs `market_breadth_analyzer.py` to fetch CSV data, compute 6-component scores, and generate composite score (0–100).
**Output:** Markdown report with composite score, zone (Strong/Healthy/Neutral/Weakening/Critical), equity exposure guidance, and strongest/weakest components.

### Example 2: Data freshness concern
**User:** "Run breadth analysis and tell me if the data is stale."
**Action:** Script validates data freshness (warns if >5 days old) and includes freshness note in report.
**Output:** Report with composite score plus explicit data freshness warning when applicable.

### Example 3: Exposure guidance
**User:** "What equity exposure level should I use based on current breadth?"
**Action:** Maps composite score to health zone and recommended exposure (90–100% Strong, 25–40% Critical, etc.).
**Output:** Clear exposure range and key breadth levels to watch for regime change.

## Error Handling

| Error | Action |
|-------|--------|
| CSV fetch fails (404, timeout) | Verify detail-url and summary-url; check TraderMonty GitHub Pages availability |
| Missing component data (e.g., no peak/trough) | Script redistributes weight across remaining components; report shows effective weights |
| Output dir not writable | Ensure `outputs/reports/trading/` exists and is writable; create if missing |
| Very old data | Note data date in report; recommend updating source or manual override if possible |
