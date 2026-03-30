---
name: trading-breadth-chart-analyst
description: >-
  Analyzes market breadth charts: S&P 500 Breadth Index (200-Day MA) and US Stock Market Uptrend Stock Ratio.
  Use when the user asks for "market breadth assessment", "breadth chart analysis", "positioning strategy",
  "strategic tactical market outlook", "마켓 브레드스", "차트 분석", "포지셔닝 전략".
  Do NOT use for daily stock signals (use daily-stock-check). Do NOT use for AlphaEar news aggregation (use alphaear-news).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: analysis
  source: claude-trading-skills
  api_required: none
---

# Breadth Chart Analyst

## Overview

This skill enables specialized analysis of two complementary market breadth charts that provide strategic (medium to long-term) and tactical (short-term) market perspectives. Analyze breadth chart images to assess market health, identify trading signals based on backtested strategies, and develop positioning recommendations. All thinking and output are conducted exclusively in English.

## When to Use

Use this skill when:
- User provides S&P 500 Breadth Index (200-Day MA based) chart images for analysis
- User provides US Stock Market Uptrend Stock Ratio chart images for analysis
- User requests market breadth assessment or market health evaluation
- User asks about medium-term strategic positioning based on breadth indicators
- User needs short-term tactical timing signals for swing trading
- User wants combined strategic and tactical market outlook

Do NOT use this skill when:
- User asks about individual stock analysis (use `us-stock-analysis` skill instead)
- User needs sector rotation analysis without breadth charts (use `trading-sector-analyst` skill instead)
- User wants news-based market analysis (use `alphaear-news` skill instead)

## Prerequisites

- **Chart Images Required**: User must provide one or both breadth chart images:
  - Chart 1: S&P 500 Breadth Index (200-Day MA based)
  - Chart 2: US Stock Market Uptrend Stock Ratio
- **No API Keys Required**: This skill analyzes user-provided images; no external data sources needed
- **Language**: All analysis and output conducted in English

## Output

This skill generates markdown analysis reports saved to the `outputs/reports/trading/` directory:
- Chart 1 only: `breadth_200ma_analysis_[YYYY-MM-DD].md`
- Chart 2 only: `uptrend_ratio_analysis_[YYYY-MM-DD].md`
- Both charts: `breadth_combined_analysis_[YYYY-MM-DD].md`

Reports include executive summaries, current readings, signal identification, scenario analysis with probabilities, and actionable positioning recommendations for different trader types.

## Trading Analysis Eval Contract (Mandatory)

Every user-facing reply (Slack, chat, or saved file) MUST satisfy five binary quality gates aligned with structured output, numeric specificity, actionable conclusion, risk awareness, and anti-hallucination.

### Required `##` headers (minimum)

Use in order: `## Summary`, `## Data & Levels`, `## Regime / Scenarios`, `## Recommendation`, `## Risks & Invalidation`. Saved reports must still follow the template in `assets/breadth_analysis_template.md`; these headers map to that structure for chat-style answers.

### Numeric evidence (≥3 distinct numbers)

- **Chart image(s) provided:** Quote **≥3** readings taken only from the image(s) (e.g. 8MA %, 200MA %, uptrend ratio %, threshold distances, dates visible on the axis).
- **No chart (text-only request):** Do **not** fabricate live market %. State that analysis requires Chart 1 and/or Chart 2 **or** delegate to `trading-market-breadth-analyzer` / `trading-uptrend-analyzer` for CSV-based breadth. You **may** cite **≥3** methodology constants (73%, 23%, ~10%, ~40%) **only** when each is labeled **reference threshold (not a live reading)**.

### Actionable conclusion

`## Recommendation` must end with an explicit stance: signal status (CONFIRMED BUY / DEVELOPING / FAILED / SELL / WAIT), or **obtain charts / run alternate skill** before trading.

### Risk / invalidation

`## Risks & Invalidation` must list **≥1** concrete failure mode (stale chart date, failed reversal per Step 4.1.5, strategic vs tactical conflict, ambiguous right-edge slope).

### Anti-hallucination

Never assert index prices, live breadth %, or chart dates not visible in the user upload. Use **not visible / not provided** when uncertain.

## Core Principles

1. **Dual-Timeframe Analysis**: Combine strategic (Chart 1: 200MA Breadth) and tactical (Chart 2: Uptrend Ratio) perspectives
2. **Backtested Strategy Focus**: Apply proven systematic strategies based on historical patterns
3. **Objective Signal Identification**: Focus on clearly defined thresholds, transitions, and markers
4. **English Communication**: Conduct all analysis and generate all reports in English
5. **Actionable Recommendations**: Provide specific positioning guidance for different investor types

## Chart Types and Purposes

**Chart 1 (200MA Breadth):** Strategic positioning. 8MA (orange) = entry signals; 200MA (green) = exit signals. 73% = overheated; 23% = extreme oversold. Purple ▼ = 8MA troughs (buy); Red ▲ = 200MA peaks (sell). See [references/breadth_chart_methodology.md](references/breadth_chart_methodology.md).

**Chart 2 (Uptrend Ratio):** Tactical swing trading. Green = uptrend, Red = downtrend. ~10% = oversold; ~40% = overbought. ENTER when red→green (<15%); EXIT when green→red (>35%). See methodology.

## Analysis Workflow

### Step 1: Receive Chart Images and Prepare Analysis

When the user provides breadth chart images for analysis:

1. Confirm receipt of chart image(s)
2. Identify which chart(s) are provided:
   - Chart 1 only (200MA Breadth)
   - Chart 2 only (Uptrend Ratio)
   - Both charts
3. Note any specific focus areas or questions from the user
4. Proceed with systematic analysis

**Language Note**: All subsequent thinking, analysis, and output will be in English.

### Step 2: Load Breadth Chart Methodology

Before beginning analysis, read the comprehensive breadth chart methodology:

```
Read: references/breadth_chart_methodology.md
```

This reference contains detailed guidance on:
- Chart 1: 200MA-based breadth index interpretation and strategy
- Chart 2: Uptrend stock ratio interpretation and strategy
- Signal identification and threshold significance
- Strategy rules and risk management
- Combining both charts for optimal decision-making
- Common pitfalls to avoid

### Step 3: Examine Sample Charts (First Time or for Reference)

To understand the chart format and visual elements, review the sample charts included in this skill:

```
View: skills/trading-breadth-chart-analyst/assets/SP500_Breadth_Index_200MA_8MA.jpeg
View: skills/trading-breadth-chart-analyst/assets/US_Stock_Market_Uptrend_Ratio.jpeg
```

These samples demonstrate:
- Visual appearance and structure of each chart type
- How signals and thresholds are displayed
- Color coding and marker systems
- Historical patterns and cycles

### Step 4: Analyze Chart 1 (200MA-Based Breadth Index)

If Chart 1 is provided, conduct systematic analysis:

#### 4.1 Extract Current Readings

From the chart image, identify:
- **Current 8MA level** (orange line): Specific percentage
- **Current 200MA level** (green line): Specific percentage
- **8MA slope**: Rising, falling, or flat
- **200MA slope**: Rising, falling, or flat
- **Distance from 73% threshold**: How close to overheating
- **Distance from 23% threshold**: How close to extreme oversold
- **Most recent date** visible on the chart

#### 4.1.5 CRITICAL: Latest Data Point Trend Analysis

**MANDATORY** — avoids misreading recent trend changes. Before stating 8MA slope or BUY status, analyze the rightmost 3-5 data points. See [references/latest_data_checklist.md](references/latest_data_checklist.md) for full checklist and failed-reversal detection.

#### 4.2 Identify Signal Markers

Look for and document:
- **Most recent 8MA trough (purple ▼)**: Date and level
- **Most recent 200MA trough (blue ▼)**: Date and level (if visible in timeframe)
- **Most recent 200MA peak (red ▲)**: Date and level
- **Days/weeks since most recent signals**
- **Any pink background shading** (downtrend periods)

#### 4.3 Assess Market Regime

Classify: Healthy Bull, Overheated Bull, Market Top/Distribution, Bear/Correction, Capitulation/Extreme Oversold, Early Recovery. See methodology for regime criteria.

#### 4.4 Determine Strategy Position

Apply backtested rules. BUY: Trough (purple ▼) + reversal + 2-3 consecutive rises + 8MA currently rising (see 4.1.5). SELL: 200MA peak (red ▲) near/above 73%. Status: CONFIRMED / DEVELOPING / FAILED / NO SIGNAL. See [references/breadth_chart_methodology.md](references/breadth_chart_methodology.md) for full criteria.

#### 4.5 Develop Scenarios

Create 2-3 scenarios with probability estimates:
- Base case scenario (highest probability)
- Alternative scenario(s)
- Each scenario includes: description, supporting factors, strategy implications, key levels

### Step 5: Analyze Chart 2 (Uptrend Stock Ratio)

If Chart 2 is provided, conduct systematic analysis:

#### 5.1 Extract Current Readings

From the chart image, identify:
- **Current uptrend stock ratio**: Specific percentage
- **Current color**: Green (uptrend) or Red (downtrend)
- **Ratio slope**: Rising, falling, or flat
- **Distance from 10% threshold**: How close to extreme oversold
- **Distance from 40% threshold**: How close to overbought
- **Most recent date** visible on the chart

#### 5.2 Identify Trend Transitions

Look for and document:
- **Most recent red-to-green transition**: Date and ratio level at transition
- **Most recent green-to-red transition**: Date and ratio level at transition
- **Duration of current color phase**: How long in current trend
- **Days/weeks since most recent transition**

#### 5.3 Assess Market Condition

Classify: Extreme Oversold (<10%), Moderate Bearish (10-20%), Neutral (20-30%), Moderate Bullish (30-37%), Extreme Overbought (>37%).

#### 5.4 Determine Trading Position

Apply the swing trading strategy rules:

**Check for ENTER LONG signal**:
- Has color changed from red to green?
- Was the transition from an oversold level (<15%)?
- Is the transition confirmed (2-3 days of green)?

**Check for EXIT LONG signal**:
- Has color changed from green to red?
- Was the transition from an overbought level (>35%)?
- Is momentum weakening?

**Current position**: Long, Flat, Preparing to Enter, or Preparing to Exit

#### 5.5 Develop Scenarios

Create 2-3 scenarios with probability estimates:
- Base case scenario (highest probability)
- Alternative scenario(s)
- Each scenario includes: description, supporting factors, trading implications, key levels

### Step 6: Combined Analysis (When Both Charts Provided)

If both charts are provided, integrate the strategic and tactical perspectives:

#### 6.1 Alignment Assessment

Create a positioning matrix:
- **Chart 1 (Strategic)**: Bullish / Bearish / Neutral + signal status
- **Chart 2 (Tactical)**: Bullish / Bearish / Neutral + signal status
- **Combined Implication**: How do they align or conflict?

#### 6.2 Scenario Classification

Determine which scenario applies. See [references/example_scenarios.md](references/example_scenarios.md) for the 4-scenario matrix (Both Bullish, Strategic Bull/Tactical Bear, Strategic Bear/Tactical Bull, Both Bearish).

#### 6.3 Unified Recommendation

Provide integrated positioning guidance for:
- **Long-term investors** (based primarily on Chart 1)
- **Swing traders** (based primarily on Chart 2)
- **Active tactical traders** (based on combination)

Address any conflicts between charts and explain resolution.

### Step 7: Generate Analysis Report in English

Create a comprehensive markdown report using the template structure:

```
Read and use as template: skills/trading-breadth-chart-analyst/assets/breadth_analysis_template.md
```

**IMPORTANT**: All analysis and output must be in English.

The report structure varies based on which chart(s) are analyzed:

**If Chart 1 only**:
- Executive Summary
- Chart 1 full analysis sections
- Summary and Conclusion
- Omit Chart 2 and Combined Analysis sections

**If Chart 2 only**:
- Executive Summary
- Chart 2 full analysis sections
- Summary and Conclusion
- Omit Chart 1 and Combined Analysis sections

**If Both Charts**:
- Executive Summary
- Chart 1 full analysis sections
- Chart 2 full analysis sections
- Combined Analysis section (mandatory)
- Summary and Conclusion

**File Naming Convention**: Save each analysis to `outputs/reports/trading/`:
- Chart 1 only: `breadth_200ma_analysis_[YYYY-MM-DD].md`
- Chart 2 only: `uptrend_ratio_analysis_[YYYY-MM-DD].md`
- Both charts: `breadth_combined_analysis_[YYYY-MM-DD].md`

### Step 8: Quality Assurance

Before finalizing the report, verify:

1. ✓ **Language**: All content is in English (thinking and output)
2. ✓ **Latest Data Trend Analysis**: Step 4.1.5 was thoroughly completed - the most recent 3-5 data points were analyzed to determine CURRENT trend direction
3. ✓ **Trend Direction Accuracy**: The stated 8MA slope (Rising/Falling/Flat) accurately reflects the RIGHTMOST data points, not historical movement
4. ✓ **Failed Reversal Check**: If a trough was identified, explicitly verified whether the reversal sustained or failed by analyzing latest trajectory
5. ✓ **Specific Values**: All readings include specific percentages/levels, not vague descriptions
6. ✓ **Signal Status**: Clear identification of active signals (CONFIRMED BUY / DEVELOPING / FAILED / SELL / WAIT)
7. ✓ **Strategy Alignment**: Recommendations align with backtested strategies and confirmation requirements
8. ✓ **Probabilities**: Scenario probabilities sum to 100%
9. ✓ **Actionable**: Clear positioning recommendations for different trader types
10. ✓ **Context**: Historical comparison and reference to similar past situations
11. ✓ **Risk Management**: Invalidation levels and risk factors clearly stated

## Quality Standards

**Objectivity:** Observable chart data only; precise terminology; separate facts from forecasts. **Completeness:** All template sections; specific values; invalidation levels. **Clarity:** Professional English; actionable recommendations. **Strategy:** Apply backtested rules; clear position status; risk management.

## Example Usage Scenarios

For step-by-step workflow examples (Chart 1 only, Chart 2 only, both charts), see [references/example_scenarios.md](references/example_scenarios.md). Includes scenario classification matrix for combined analysis.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/breadth_chart_methodology.md](references/breadth_chart_methodology.md) | Chart 1/2 components, regimes, backtested strategy, common pitfalls. Read before analysis. |
| [references/latest_data_checklist.md](references/latest_data_checklist.md) | Latest data point trend analysis, failed-reversal detection |
| [references/example_scenarios.md](references/example_scenarios.md) | Example workflows, 4-scenario combined matrix |
| assets/breadth_analysis_template.md | Report template structure. Use for every analysis. |
| assets/SP500_Breadth_Index_200MA_8MA.jpeg | Sample Chart 1 format reference |
| assets/US_Stock_Market_Uptrend_Ratio.jpeg | Sample Chart 2 format reference |

## Special Notes

**Language:** All analysis and output in English. **Strategy:** Backtested, systematic rules; specific entry/exit; risk management. **Goal:** Actionable — strategic stance, tactical timing, invalidation levels.

## Examples

### Example 1: Strategic breadth assessment
**User:** "Please analyze this S&P 500 breadth chart and tell me where we are in the market cycle."
**Action:** Loads breadth methodology, examines 8MA/200MA levels and signal markers, determines regime (e.g., Overheated Bull approaching Distribution), and applies backtested BUY/SELL rules.
**Output:** Markdown report `breadth_200ma_analysis_YYYY-MM-DD.md` with current readings, signal status, scenarios with probabilities, and positioning recommendation.

### Example 2: Tactical swing timing
**User:** "Should I be buying or selling here? Analyze this uptrend ratio chart."
**Action:** Extracts uptrend ratio and color (green/red), identifies recent red-to-green or green-to-red transitions, and applies swing trading entry/exit rules.
**Output:** Report `uptrend_ratio_analysis_YYYY-MM-DD.md` with ENTER LONG / EXIT LONG / HOLD status and key levels.

### Example 3: Combined strategic + tactical
**User:** "Analyze both breadth charts and give me your overall market view."
**Action:** Analyzes both charts, assesses alignment (Scenario 1–4), and produces unified recommendations for long-term investors, swing traders, and tactical traders.
**Output:** Report `breadth_combined_analysis_YYYY-MM-DD.md` with integrated positioning matrix and conflict resolution.

## Error Handling

| Error | Action |
|-------|--------|
| User provides no chart image | Request one or both breadth chart images (200MA Breadth Index and/or Uptrend Ratio) |
| Chart date appears stale | Note data age in report; recommend updating with current chart before trading |
| 8MA slope ambiguous at rightmost edge | Perform Step 4.1.5 detailed trend analysis; avoid stating slope without tracing 3–5 latest points |
| Failed reversal suspected (8MA rose then fell) | Classify as FAILED REVERSAL; do NOT issue BUY signal; recommend WAIT |
