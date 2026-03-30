---
name: trading-uptrend-analyzer
description: >-
  Analyzes market breadth using Monty's Uptrend Ratio Dashboard to diagnose market environment. Generates 0-100 composite score from 5 components.
  Use when the user asks "market breadth healthy", "how broad is the rally", "uptrend ratios", "market participation",
  "exposure guidance based on breadth", "마켓 브레드스", "업트렌드 비율", "시장 참여도".
  Do NOT use for daily stock signals (use daily-stock-check). Do NOT use for market top risk assessment (use trading-market-top-detector).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: analysis
  source: claude-trading-skills
  api_required: none
---

# Uptrend Analyzer Skill

## Purpose

Diagnose market breadth health using Monty's Uptrend Ratio Dashboard, which tracks ~2,800 US stocks across 11 sectors. Generates a 0-100 composite score (higher = healthier) with exposure guidance.

Unlike the Market Top Detector (API-based risk scorer), this skill uses free CSV data to assess "participation breadth" - whether the market's advance is broad or narrow.

## When to Use This Skill

**English:**
- User asks "Is the market breadth healthy?" or "How broad is the rally?"
- User wants to assess uptrend ratios across sectors
- User asks about market participation or breadth conditions
- User needs exposure guidance based on breadth analysis
- User references Monty's Uptrend Dashboard or uptrend ratios

**Japanese:**
- 「市場のブレドスは健全？」「上昇の裾野は広い？」
- セクター別のアップトレンド比率を確認したい
- 相場参加率・ブレドス状況を診断したい
- ブレドス分析に基づくエクスポージャーガイダンスが欲しい
- Montyのアップトレンドダッシュボードについて質問

## Difference from Market Top Detector

| Aspect | Uptrend Analyzer | Market Top Detector |
|--------|-----------------|-------------------|
| Score Direction | Higher = healthier | Higher = riskier |
| Data Source | Free GitHub CSV | FMP API (paid) |
| Focus | Breadth participation | Top formation risk |
| API Key | Not required | Required (FMP) |
| Methodology | Monty Uptrend Ratios | O'Neil/Minervini/Monty |

---

## Execution Workflow

### Phase 1: Execute Python Script

Run the analysis script (no API key needed):

```bash
python3 skills/trading-uptrend-analyzer/scripts/uptrend_analyzer.py --output-dir outputs/reports/trading/
```

The script will:
1. Download CSV data from Monty's GitHub repository
2. Calculate 5 component scores
3. Generate composite score and reports

### Phase 2: Present Results

Present the generated Markdown report to the user, highlighting:
- Composite score and zone classification
- Exposure guidance (Full/Normal/Reduced/Defensive/Preservation)
- Sector heatmap showing strongest and weakest sectors
- Key momentum and rotation signals

### Phase 2b: Trading Analysis Eval Contract (Mandatory)

Every **user-facing** response after `uptrend_analyzer.py` (or when explaining a failure to run) MUST satisfy:

| Gate | Pass condition |
|------|----------------|
| **Structured output** | `## Summary`, `## Composite & Zones`, `## Sector / Participation Highlights`, `## Recommendation`, `## Risks & Data Caveats`. |
| **Specific numbers** | **≥3** figures from the latest report (composite 0–100, one sector uptrend % or spread, data timestamp). |
| **Actionable conclusion** | Tie composite + warnings to an exposure stance using the zone table (e.g. Normal Exposure 80–100%). |
| **Risk awareness** | Include **≥1** of: Late Cycle / High Spread / Divergence penalty, thin history (Low confidence), or CSV fetch age. |
| **No hallucinated data** | All metrics must come from script JSON/Markdown; never invent sector ratios. |

If the user asks in Korean without you having run the script, run Phase 1 first when possible; otherwise use the headers above and give the exact command from Phase 1.

---

## 5-Component Scoring System

| # | Component | Weight | Key Signal |
|---|-----------|--------|------------|
| 1 | Market Breadth (Overall) | **30%** | Ratio level + trend direction |
| 2 | Sector Participation | **25%** | Uptrend sector count + ratio spread |
| 3 | Sector Rotation | **15%** | Cyclical vs Defensive balance |
| 4 | Momentum | **20%** | Slope direction + acceleration |
| 5 | Historical Context | **10%** | Percentile rank in history |

## Scoring Zones

| Score | Zone | Exposure Guidance |
|-------|------|-------------------|
| 80-100 | Strong Bull | Full Exposure (100%) |
| 60-79 | Bull | Normal Exposure (80-100%) |
| 40-59 | Neutral | Reduced Exposure (60-80%) |
| 20-39 | Cautious | Defensive (30-60%) |
| 0-19 | Bear | Capital Preservation (0-30%) |

### 7-Level Zone Detail

Each scoring zone is further divided into sub-zones for finer-grained assessment:

| Score | Zone Detail | Color |
|-------|-------------|-------|
| 80-100 | Strong Bull | Green |
| 70-79 | Bull-Upper | Light Green |
| 60-69 | Bull-Lower | Light Green |
| 40-59 | Neutral | Yellow |
| 30-39 | Cautious-Upper | Orange |
| 20-29 | Cautious-Lower | Orange |
| 0-19 | Bear | Red |

### Warning System

Active warnings trigger exposure penalties that tighten guidance even when the composite score is high:

| Warning | Condition | Penalty |
|---------|-----------|---------|
| **Late Cycle** | Commodity avg > both Cyclical and Defensive | -5 |
| **High Spread** | Max-min sector ratio spread > 40pp | -3 |
| **Divergence** | Intra-group std > 8pp, spread > 20pp, or trend dissenters | -3 |

Penalties stack (max -10) + multi-warning discount (+1 when ≥2 active). Applied after composite scoring.

### Momentum Smoothing

Slope values are smoothed using EMA(3) (Exponential Moving Average, span=3) before scoring. Acceleration is calculated by comparing the recent 10-point average vs prior 10-point average of smoothed slopes (10v10 window), with fallback to 5v5 when fewer than 20 data points are available.

### Historical Confidence Indicator

The Historical Context component includes a confidence assessment based on:
- **Sample size:** Number of historical data points available
- **Regime coverage:** Proportion of distinct market regimes (bull/bear/neutral) observed
- **Recency:** How recent the latest data point is

Confidence levels: High, Medium, Low.

---

## API Requirements

**Required:** None (uses free GitHub CSV data)

## Output Files

- JSON: `outputs/reports/trading/uptrend_analysis_YYYY-MM-DD_HHMMSS.json`
- Markdown: `outputs/reports/trading/uptrend_analysis_YYYY-MM-DD_HHMMSS.md`

## Reference Documents

### `references/uptrend_methodology.md`
- Uptrend Ratio definition and thresholds
- 5-component scoring methodology
- Sector classification (Cyclical/Defensive/Commodity)
- Historical calibration notes

### When to Load References
- **First use:** Load `uptrend_methodology.md` for full framework understanding
- **Regular execution:** References not needed - script handles scoring

## Examples

### Example 1: Breadth health check
**User:** "Is market breadth healthy? How broad is the rally?"
**Action:** Runs `uptrend_analyzer.py` to fetch Monty CSV, compute 5-component scores, and generate composite (0–100).
**Output:** Markdown report with composite score, zone (Strong Bull/Bull/Neutral/Cautious/Bear), exposure guidance, and sector heatmap.

### Example 2: Exposure guidance
**User:** "What equity exposure should I use based on breadth?"
**Action:** Maps composite score to zone and recommended exposure (Full/Normal/Reduced/Defensive/Preservation).
**Output:** Exposure range (e.g., 60–80% for Neutral) and key momentum/rotation signals.

### Example 3: Sector participation
**User:** "Which sectors are participating in the uptrend?"
**Action:** Presents sector heatmap and participation metrics from script output; identifies strongest and weakest sectors.
**Output:** Sector-level breakdown with uptrend ratios and rotation implications.

## Error Handling

| Error | Action |
|-------|--------|
| CSV fetch fails (GitHub) | Verify Monty uptrend CSV URL; check network; script downloads from public repo |
| Output dir not writable | Create `outputs/reports/trading/`; ensure write permissions |
| Warning penalties applied | Report shows active warnings (Late Cycle, High Spread, Divergence) and adjusted exposure |
| Fewer than 20 slope data points | Script uses 5v5 fallback for acceleration; note in report if applicable |
