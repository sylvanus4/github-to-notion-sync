---
name: trading-theme-detector
description: >-
  Detects and ranks trending market themes across sectors using cross-sector momentum, volume, and breadth signals.
  Use when the user asks "current market themes", "trending sectors", "sector rotation", "thematic investing",
  "hot or cold themes", "bullish bearish narratives", "theme lifecycle", "시장 테마", "섹터 로테이션", "테마 투자".
  Do NOT use for daily stock signals (use daily-stock-check). Do NOT use for sector rotation analysis without theme detection (use trading-sector-analyst).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: analysis
  source: claude-trading-skills
  api_required: optional
---

# Theme Detector

## Overview

This skill detects and ranks trending market themes by analyzing cross-sector momentum, volume, and breadth signals. It identifies both bullish (upward momentum) and bearish (downward pressure) themes, assesses lifecycle maturity (early/mid/late/exhaustion), and provides a confidence score combining quantitative data with narrative analysis.

**3-Dimensional Scoring Model:**
1. **Theme Heat** (0-100): Direction-neutral strength of the theme (momentum, volume, uptrend ratio, breadth)
2. **Lifecycle Maturity**: Stage classification (Early / Mid / Late / Exhaustion) based on duration, extremity clustering, valuation, and ETF proliferation
3. **Confidence** (Low / Medium / High): Reliability of the detection, combining quantitative breadth with narrative confirmation

**Key Features:**
- Cross-sector theme detection using FINVIZ industry data
- Direction-aware scoring (bullish and bearish themes)
- Lifecycle maturity assessment to identify crowded vs. emerging trades
- ETF proliferation scoring (more ETFs = more mature/crowded theme)
- Integration with uptrend-dashboard for 3-point evaluation
- Dual-mode operation: FINVIZ Elite (fast) or public scraping (slower, limited)
- WebSearch-based narrative confirmation for top themes

---

## When to Use This Skill

**Explicit Triggers:**
- "What market themes are trending right now?"
- "Which sectors are hot/cold?"
- "Detect current market themes"
- "What are the strongest bullish/bearish narratives?"
- "Is AI/clean energy/defense still a strong theme?"
- "Where is sector rotation heading?"
- "Show me thematic investing opportunities"

**Implicit Triggers:**
- User wants to understand broad market narrative shifts
- User is looking for thematic ETF or sector allocation ideas
- User asks about crowded trades or late-cycle themes
- User wants to know which themes are emerging vs. exhausted

**When NOT to Use:**
- Individual stock analysis (use us-stock-analysis instead)
- Specific sector deep-dive with chart reading (use trading-sector-analyst instead)
- Portfolio rebalancing (use portfolio-manager instead)
- Dividend/income investing (use value-dividend-screener instead)

---

## Workflow

### Step 1: Verify Requirements

Check for required API keys and dependencies:

```bash
# Check for FINVIZ Elite API key (optional but recommended)
echo $FINVIZ_API_KEY

# Check for FMP API key (optional, used for valuation metrics)
echo $FMP_API_KEY
```

**Requirements:**
- **Python 3.7+** with `requests`, `beautifulsoup4`, `lxml`
- **FINVIZ Elite API key** (recommended for full industry coverage and speed)
- **FMP API key** (optional, for P/E ratio valuation data)
- Without FINVIZ Elite, the skill uses public FINVIZ scraping (limited to ~20 stocks per industry, slower rate limits)

**Installation:**
```bash
pip install requests beautifulsoup4 lxml
```

### Step 2: Execute Theme Detection Script

Run the main detection script:

```bash
python3 skills/trading-theme-detector/scripts/theme_detector.py \
  --output-dir outputs/reports/trading/
```

**Script Options:**
```bash
# Full run (public FINVIZ mode, no API key required)
python3 skills/trading-theme-detector/scripts/theme_detector.py \
  --output-dir outputs/reports/trading/

# With FINVIZ Elite API key
python3 skills/trading-theme-detector/scripts/theme_detector.py \
  --finviz-api-key $FINVIZ_API_KEY \
  --output-dir outputs/reports/trading/

# With FMP API key for enhanced stock data
python3 skills/trading-theme-detector/scripts/theme_detector.py \
  --fmp-api-key $FMP_API_KEY \
  --output-dir outputs/reports/trading/

# Custom limits
python3 skills/trading-theme-detector/scripts/theme_detector.py \
  --max-themes 5 \
  --max-stocks-per-theme 5 \
  --output-dir outputs/reports/trading/

# Explicit FINVIZ mode
python3 skills/trading-theme-detector/scripts/theme_detector.py \
  --finviz-mode public \
  --output-dir outputs/reports/trading/
```

**Expected Execution Time:**
- FINVIZ Elite mode: ~2-3 minutes (14+ themes)
- Public FINVIZ mode: ~5-8 minutes (rate-limited scraping)

### Step 3: Read and Parse Detection Results

The script generates two output files in `outputs/reports/trading/`:
- `theme_detector_YYYY-MM-DD_HHMMSS.json` - Structured data for programmatic use
- `theme_detector_YYYY-MM-DD_HHMMSS.md` - Human-readable report

Read the JSON output to understand quantitative results:

```bash
# Find the latest report
ls -lt outputs/reports/trading/theme_detector_*.json | head -1

# Read the JSON output
cat outputs/reports/trading/theme_detector_YYYY-MM-DD_HHMMSS.json
```

### Step 4: Perform Narrative Confirmation via WebSearch

For the top 5 themes (by Theme Heat score), execute WebSearch queries to confirm narrative strength:

**Search Pattern:**
```
"[theme name] stocks market [current month] [current year]"
"[theme name] sector momentum [current month] [current year]"
```

**Evaluate narrative signals:**
- **Strong narrative**: Multiple major outlets covering the theme, analyst upgrades, policy catalysts
- **Moderate narrative**: Some coverage, mixed sentiment, no clear catalyst
- **Weak narrative**: Little coverage, or predominantly contrarian/skeptical tone

Update Confidence levels based on findings:
- Quantitative High + Narrative Strong = **High** confidence
- Quantitative High + Narrative Weak = **Medium** confidence (possible momentum divergence)
- Quantitative Low + Narrative Strong = **Medium** confidence (narrative may lead price)
- Quantitative Low + Narrative Weak = **Low** confidence

### Step 5: Analyze Results and Provide Recommendations

Cross-reference detection results with knowledge bases:

**Reference Documents to Consult:**
1. `references/cross_sector_themes.md` - Theme definitions and constituent industries
2. `references/thematic_etf_catalog.md` - ETF exposure options by theme
3. `references/theme_detection_methodology.md` - Scoring model details
4. `references/finviz_industry_codes.md` - Industry classification reference

**Analysis Framework:**

For **Hot Bullish Themes** (Heat >= 70, Direction = Bullish):
- Identify lifecycle stage (Early = opportunity, Late/Exhaustion = caution)
- List top-performing industries within the theme
- Recommend proxy ETFs for exposure
- Flag if ETF proliferation is high (crowded trade warning)

For **Hot Bearish Themes** (Heat >= 70, Direction = Bearish):
- Identify industries under pressure
- Assess if bearish momentum is accelerating or decelerating
- Recommend hedging strategies or sectors to avoid
- Note potential mean-reversion opportunities if lifecycle is Late/Exhaustion

For **Emerging Themes** (Heat 40-69, Lifecycle = Early):
- These may represent early rotation signals
- Recommend monitoring with watchlist
- Identify catalyst events that could accelerate the theme

For **Exhausted Themes** (Heat >= 60, Lifecycle = Exhaustion):
- Warn about crowded trade risk
- High ETF count confirms excessive retail participation
- Consider contrarian positioning or reducing exposure

### Step 6: Generate Final Report

Present the final report to the user using the report template structure:

```markdown
# Theme Detection Report
**Date:** YYYY-MM-DD
**Mode:** FINVIZ Elite / Public
**Themes Analyzed:** N
**Data Quality:** [note any limitations]

## Theme Dashboard
[Top themes table with Heat, Direction, Lifecycle, Confidence]

## Bullish Themes Detail
[Detailed analysis of bullish themes sorted by Heat]

## Bearish Themes Detail
[Detailed analysis of bearish themes sorted by Heat]

## All Themes Summary
[Complete theme ranking table]

## Industry Rankings
[Top performing and worst performing industries]

## Sector Uptrend Ratios
[Sector-level aggregation if uptrend data available]

## Methodology Notes
[Brief explanation of scoring model]
```

Save the report to `outputs/reports/trading/` directory.

### Step 6b: Trading Analysis Eval Contract (Mandatory)

Whether in chat or saved Markdown, the final user-visible analysis MUST satisfy:

| Gate | Pass condition |
|------|----------------|
| **Structured output** | `## Summary`, `## Theme Dashboard (Top N)`, `## Bullish / Bearish Highlights`, `## Recommendation`, `## Risks, Data & Narrative Caveats`. |
| **Specific numbers** | **≥3** quantitative fields from JSON/MD output (e.g. Theme Heat scores, industry avg change%, uptrend % if present, ETF counts). |
| **Actionable conclusion** | State how to express or avoid themes (proxy ETFs, watchlist only, reduce crowded Late/Exhaustion). |
| **Risk awareness** | **≥1** limitation from Known Limitations (scraping lag, survivorship, narrative subjectivity) or invalidation if WebSearch disagrees with quant. |
| **No hallucinated data** | All performance and heat values must trace to `theme_detector_*.json`/`.md`; label WebSearch as narrative only. |

If the script cannot run, keep the same headers and document the blocker—do not fabricate theme ranks.

---

## Resources

### Scripts Directory (`scripts/`)

**Main Scripts:**
- `theme_detector.py` - Main orchestrator script
  - Coordinates industry data collection, theme classification, and scoring
  - Generates JSON + Markdown output
  - Usage: `python3 theme_detector.py [options]`

- `theme_classifier.py` - Maps industries to cross-sector themes
  - Reads theme definitions from `cross_sector_themes.md`
  - Calculates theme-level aggregated scores
  - Determines direction (bullish/bearish) from constituent industries

- `finviz_industry_scanner.py` - FINVIZ industry data collection
  - Elite mode: CSV export with full stock data per industry
  - Public mode: Web scraping with rate limiting
  - Extracts: performance, volume, change%, avg volume, market cap

- `lifecycle_analyzer.py` - Lifecycle maturity assessment
  - Duration scoring, extremity clustering, valuation analysis
  - ETF proliferation scoring from thematic_etf_catalog.md
  - Stage classification: Early / Mid / Late / Exhaustion

- `report_generator.py` - Report output generation
  - Markdown report from template
  - JSON structured output
  - Theme dashboard formatting

### References Directory (`references/`)

**Knowledge Bases:**
- `cross_sector_themes.md` - Theme definitions with industries, ETFs, stocks, and matching criteria
- `thematic_etf_catalog.md` - Comprehensive thematic ETF catalog with counts per theme
- `finviz_industry_codes.md` - Complete FINVIZ industry-to-filter-code mapping
- `theme_detection_methodology.md` - Technical documentation of the 3D scoring model

### Assets Directory (`assets/`)

- `report_template.md` - Markdown template for report generation with placeholder format

---

## Important Notes

### FINVIZ Mode Differences

| Feature | Elite Mode | Public Mode |
|---------|-----------|-------------|
| Industry coverage | All ~145 industries | All ~145 industries |
| Stocks per industry | Full universe | ~20 stocks (page 1) |
| Rate limiting | 0.5s between requests | 2.0s between requests |
| Data freshness | Real-time | 15-min delayed |
| API key required | Yes ($39.99/mo) | No |
| Execution time | ~2-3 minutes | ~5-8 minutes |

### Direction Detection Logic

Theme direction (bullish vs. bearish) is determined by:
1. **Weighted industry performance**: Average change% across constituent industries, weighted by market cap
2. **Uptrend ratio**: Percentage of stocks in each industry that are in technical uptrends (if uptrend data available)
3. **Volume confirmation**: Whether volume supports the price direction (accumulation vs. distribution)

A theme is classified as:
- **Bullish**: Weighted performance > 0 AND (uptrend ratio > 50% OR volume accumulation confirmed)
- **Bearish**: Weighted performance < 0 AND (uptrend ratio < 50% OR volume distribution confirmed)
- **Neutral**: Mixed signals or insufficient data

### Known Limitations

1. **Survivorship bias**: Only analyzes currently listed stocks and ETFs
2. **Lag**: FINVIZ data may lag intraday moves by 15 minutes (public mode)
3. **Theme boundaries**: Some stocks fit multiple themes; classification uses primary industry
4. **ETF proliferation**: Catalog is static and may not capture very new ETFs
5. **Narrative scoring**: WebSearch-based and inherently subjective
6. **Public mode limitation**: ~20 stocks per industry may miss small-cap signals

### Disclaimer

**This analysis is for educational and informational purposes only.**
- Not investment advice
- Past thematic trends do not guarantee future performance
- Theme detection identifies momentum, not fundamental value
- Conduct your own research before making investment decisions

---

**Version:** 1.0
**Last Updated:** 2026-02-16
**API Requirements:** FINVIZ Elite (recommended) or public mode (free); FMP API optional
**Execution Time:** ~2-8 minutes depending on mode
**Output Formats:** JSON + Markdown
**Themes Covered:** 14+ cross-sector themes
**Output Location:** `outputs/reports/trading/`

## Examples

### Example 1: Current themes
**User:** "What market themes are trending right now?"
**Action:** Runs `theme_detector.py`, parses JSON/MD output, performs WebSearch narrative confirmation for top 5 themes.
**Output:** Report with theme dashboard (Heat, Direction, Lifecycle, Confidence), bullish/bearish detail, and recommendations.

### Example 2: Theme lifecycle check
**User:** "Is AI still a strong theme or is it exhausted?"
**Action:** Runs detector, identifies AI theme in output, assesses Heat, Lifecycle (Early/Mid/Late/Exhaustion), and ETF proliferation.
**Output:** Theme-specific analysis with lifecycle stage, crowded-trade warning if Late/Exhaustion, and positioning guidance.

### Example 3: Thematic investing ideas
**User:** "Show me thematic investing opportunities."
**Action:** Runs full detection, cross-references thematic_etf_catalog.md, identifies hot themes with ETF proxies.
**Output:** Ranked themes with constituent industries, proxy ETFs, and suitability notes.

## Error Handling

| Error | Action |
|-------|--------|
| FINVIZ scraping rate limit (public mode) | Wait and retry; or use FINVIZ Elite API key for faster runs |
| Theme script timeout | Reduce `--max-themes` or `--max-stocks-per-theme`; public mode can take 5–8 min |
| JSON/MD output missing | Check `outputs/reports/trading/`; ensure script completed; verify output-dir writable |
| WebSearch narrative returns little | Proceed with quantitative confidence only; note narrative gap in report |
