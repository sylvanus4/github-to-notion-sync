---
name: trading-us-market-bubble-detector
description: >-
  Evaluates market bubble risk through quantitative data-driven analysis using the Minsky/Kindleberger
  framework v2.1. Prioritizes objective metrics (Put/Call, VIX, margin debt, breadth, IPO data) over
  subjective impressions. Features strict qualitative adjustment criteria with confirmation bias prevention.
  Use for "bubble risk", "market bubble", "バブル検出", "시장 버블", "과열 판단", "profit-taking timing".
  Do NOT use for daily stock signals (use daily-stock-check).
  Do NOT use for AlphaEar analysis (use alphaear-deepear-lite).
  Do NOT use for weekly price updates (use weekly-stock-update).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: analysis
  source: claude-trading-skills
  api_required: none
---

# US Market Bubble Detection Skill (Revised v2.1)

## Key Revisions in v2.1

**Critical Changes from v2.0:**
1. ✅ **Mandatory Quantitative Data Collection** - Use measured values, not impressions or speculation
2. ✅ **Clear Threshold Settings** - Specific numerical criteria for each indicator
3. ✅ **Two-Phase Evaluation Process** - Quantitative evaluation → Qualitative adjustment (strict order)
4. ✅ **Stricter Qualitative Criteria** - Max +3 points (reduced from +5), requires measurable evidence
5. ✅ **Confirmation Bias Prevention** - Explicit checklist to avoid over-scoring
6. ✅ **Granular Risk Phases** - Added "Elevated Risk" phase (8-9 points) for nuanced risk management

---

## When to Use This Skill

Use this skill when:

**English:**
- User asks "Is the market in a bubble?" or "Are we in a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User reports social phenomena (non-investors entering, media frenzy, IPO flood)
- User mentions narratives like "this time is different" or "revolutionary technology" becoming mainstream
- User consults about risk management for existing positions

**Japanese:**
- ユーザーが「今の相場はバブルか?」と尋ねる
- 投資の利確・新規参入・空売りのタイミング判断を求める
- 社会現象(非投資家の参入、メディア過熱、IPO氾濫)を観察し懸念を表明
- 「今回は違う」「革命的技術」などの物語が主流化している状況を報告
- 保有ポジションのリスク管理方法を相談

---

## Evaluation Process (Strict Order)

### Phase 1: Mandatory Quantitative Data Collection

**CRITICAL: Always collect the following data before starting evaluation**

#### 1.1 Market Structure Data (Highest Priority)
```
□ Put/Call Ratio (CBOE Equity P/C)
  - Source: CBOE DataShop or web_search "CBOE put call ratio"
  - Collect: 5-day moving average

□ VIX (Fear Index)
  - Source: Yahoo Finance ^VIX or web_search "VIX current"
  - Collect: Current value + percentile over past 3 months

□ Volatility Indicators
  - 21-day realized volatility
  - Historical position of VIX (determine if in bottom 10th percentile)
```

#### 1.2 Leverage & Positioning Data
```
□ FINRA Margin Debt Balance
  - Source: web_search "FINRA margin debt latest"
  - Collect: Latest month + Year-over-Year % change

□ Breadth (Market Participation)
  - % of S&P 500 stocks above 50-day MA
  - Source: web_search "S&P 500 breadth 50 day moving average"
```

#### 1.3 IPO & New Issuance Data
```
□ IPO Count & First-Day Performance
  - Source: Renaissance Capital IPO or web_search "IPO market 2025"
  - Collect: Quarterly count + median first-day return
```

**⚠️ CRITICAL: Do NOT proceed with evaluation without Phase 1 data collection**

---

### Phase 2: Quantitative Evaluation (Quantitative Scoring)

Score mechanically based on collected data. For detailed scoring criteria for all 6 indicators (Put/Call, Volatility, Leverage, IPO, Breadth, Price Acceleration), see [references/scoring_criteria.md](references/scoring_criteria.md).

---

### Phase 3: Qualitative Adjustment (REVISED v2.1)

**Limit: +3 points maximum (REDUCED from +5 in v2.0)**

Run the confirmation bias prevention checklist before adding any points. For detailed criteria for Adjustments A (Social Penetration), B (Media/Search Trends), and C (Valuation Disconnect), see [references/scoring_criteria.md](references/scoring_criteria.md).

**Phase 3 Total: Maximum +3 points**

---

### Phase 4: Final Judgment (REVISED v2.1)

```
Final Score = Phase 2 Total (0-12 points) + Phase 3 Adjustment (0 to +3 points)
Range: 0 to 15 points

Judgment Criteria (with Risk Budget):
- 0-4 points: Normal (Risk Budget: 100%)
- 5-7 points: Caution (Risk Budget: 70-80%)
- 8-9 points: Elevated Risk (Risk Budget: 50-70%) ⚠️ NEW in v2.1
- 10-12 points: Euphoria (Risk Budget: 40-50%)
- 13-15 points: Critical (Risk Budget: 20-30%)
```

**Key Change in v2.1:**
- Added "Elevated Risk" phase (8-9 points) for more nuanced positioning
- 9 points is no longer extreme defensive zone (was 40% risk budget)
- Now allows 50-70% risk budget at 8-9 point level
- More gradual transition from Caution to Euphoria phases

---

## Data Sources (Required)

### US Market
- **Put/Call**: https://www.cboe.com/tradable_products/vix/
- **VIX**: Yahoo Finance (^VIX) or https://www.cboe.com/
- **Margin Debt**: https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics
- **Breadth**: https://www.barchart.com/stocks/indices/sp/sp500?viewName=advanced
- **IPO**: https://www.renaissancecapital.com/IPO-Center/Stats

### Japanese Market
- **Nikkei Futures P/C**: https://www.barchart.com/futures/quotes/NO*0/options
- **JNIVE**: https://www.investing.com/indices/nikkei-volatility-historical-data
- **Margin Debt**: JSF (Japan Securities Finance) Monthly Report
- **Breadth**: https://en.macromicro.me/series/31841/japan-topix-index-200ma-breadth
- **IPO**: https://www.pwc.co.uk/services/audit/insights/global-ipo-watch.html

---

## Implementation Checklist

Verify the following when using:

```
□ Have you collected all Phase 1 data?
□ Did you apply each indicator's threshold mechanically?
□ Did you keep qualitative evaluation within +3 point limit (v2.1)?
□ Are you NOT assigning points based on news article impressions?
□ Does your final score align with other quantitative frameworks?
```

---

## Important Principles (Revised)

### 1. Data > Impressions
Ignore "many news reports" or "experts are cautious" without quantitative data.

### 2. Strict Order: Quantitative → Qualitative
Always evaluate in this order: Phase 1 (Data Collection) → Phase 2 (Quantitative) → Phase 3 (Qualitative Adjustment).

### 3. Upper Limit on Subjective Indicators
Qualitative adjustment has a total limit of **+3 points** (v2.1). It cannot override quantitative evaluation.

### 4. "Taxi Driver" is Symbolic
Do not readily acknowledge mass penetration without direct recommendations from non-investors.

---

## Common Failures and Solutions (Revised)

### Failure 1: Evaluating Based on News Articles
❌ "Many reports on Takaichi Trade" → Media saturation 2 points
✅ Verify Google Trends numbers → Evaluate with measured values

### Failure 2: Overreaction to Expert Comments
❌ "Warning of overheating" → Euphoria zone
✅ Judge with measured values of Put/Call, VIX, margin debt

### Failure 3: Emotional Reaction to Price Rise
❌ 4.5% rise in 1 day → Price acceleration 2 points
✅ Verify position in 10-year distribution → Objective evaluation

### Failure 4: Judgment Based on Valuation Alone
❌ P/E 17 → Valuation disconnect 2 points
✅ P/E + narrative dependence + other quantitative indicators for comprehensive judgment

---

## Recommended Actions by Bubble Stage (REVISED v2.1)

For detailed risk budgets, ATR levels, and short-selling rules per phase (Normal/Caution/Elevated Risk/Euphoria/Critical), see [references/action_playbook.md](references/action_playbook.md).

---

## Output Format

Reports may be saved to `outputs/reports/trading/` when generating structured evaluation reports.

### Trading Analysis Eval Contract (Mandatory)

User-facing answers MUST satisfy five gates:

| Gate | Pass condition |
|------|----------------|
| **Structured output** | `## Summary`, `## Phase 1 Data Table`, `## Quantitative Score (Phase 2)`, `## Qualitative Adjustment (Phase 3, max +3)`, `## Final Judgment & Risk Budget`, `## Risks & What Would Change the Score`. |
| **Specific numbers** | **≥3** measured fields from Phase 1 **and** the final 0–15 score with phase label (e.g. Caution 5–7). Show Put/Call 5d avg, VIX, margin debt YoY %, breadth %, IPO stats as collected—not placeholders. |
| **Actionable conclusion** | End with risk budget % band + concrete actions (profit-taking stairs, new entry throttle) per phase. |
| **Risk awareness** | List **≥1** invalidation (e.g. data revision, breadth improvement, qualitative evidence failing checklist). |
| **No hallucinated data** | If a Phase 1 box is empty, write **not collected**—never invent CBOE/Yahoo values. |

**Phase 1 Data Table (minimum columns):** Indicator | Value | As-of date | Source — one row per collected item.

---

## Reference Documents

### `references/implementation_guide.md` (English) - **RECOMMENDED FOR FIRST USE**
- Step-by-step evaluation process with mandatory data collection
- NG examples vs OK examples
- Self-check quality criteria (4 levels)
- Red flags during review
- Best practices for objective evaluation

### `references/bubble_framework.md` (Japanese)
- Detailed theoretical framework
- Explanation of Minsky/Kindleberger model
- Behavioral psychology elements

### `references/historical_cases.md` (Japanese)
- Analysis of past bubble cases
- Dotcom, Crypto, Pandemic bubbles
- Common pattern extraction

### `references/quick_reference.md` (Japanese)
### `references/quick_reference_en.md` (English)
- Daily checklist
- Emergency 3-question assessment
- Quick scoring guide
- Key data sources

### When to Load References
- **First use or need detailed guidance:** Load `implementation_guide.md`
- **Need theoretical background:** Load `bubble_framework.md`
- **Need historical context:** Load `historical_cases.md`
- **Daily operations:** Load `quick_reference.md` (Japanese) or `quick_reference_en.md` (English)

---

## Summary: Essence of v2.1 Revision

**v2.0 Problem (Identified Nov 2025):**
- Qualitative adjustment too loose (+5 max)
- "AI narrative elevated" → +1 point (no data)
- "P/E 30.8" → +1 point (double-counting with quantitative)
- **Result: 11/16 points - overly bearish without evidence**

**v2.1 Solution:**
- Qualitative adjustment stricter (+3 max)
- "AI narrative elevated" → 0 points (unmeasured)
- "P/E 30.8 but AI has fundamental backing" → 0 points (fundamentals support)
- **Result: 9/15 points - balanced, data-driven assessment**

**Key Improvements:**
1. **Confirmation Bias Prevention**: Explicit checklist before adding qualitative points
2. **Measurable Evidence Required**: No points without concrete data (Google Trends, media coverage)
3. **Double-Counting Prevention**: Valuation must not duplicate Phase 2 quantitative
4. **Granular Risk Phases**: Added "Elevated Risk" (8-9 points) for nuanced positioning
5. **Balanced Risk Budgets**: 9 points = 50-70% (not 40% extreme defensive)

**Core Principle:**
> "In God we trust; all others must bring data." - W. Edwards Deming

**2025 Lesson:**
Even data-driven frameworks can be undermined by subjective qualitative adjustments.
v2.1 requires MEASURABLE evidence for ALL qualitative points.
Independent observers must be able to verify each adjustment.

---

**Version History:**
- **v2.0** (Oct 27, 2025): Mandatory quantitative data collection
- **v2.1** (Nov 3, 2025): Stricter qualitative criteria, confirmation bias prevention, granular risk phases

**Reason for v2.1 Revision:**
Prevent over-scoring through unmeasured "narrative" assessments and double-counting.
Ensure all bubble risk evaluations are independently verifiable and free from confirmation bias.

## Examples

### Example 1: Quantitative bubble check
**User:** "Is the market in a bubble right now?"
**Action:** Collects Phase 1 data (Put/Call, VIX, margin debt, breadth, IPO); applies Phase 2 quantitative scoring; applies Phase 3 qualitative adjustment (max +3) with measurable evidence only.
**Output:** Final score (0–15), risk phase (Normal/Caution/Elevated/Euphoria/Critical), risk budget, and recommended actions.

### Example 2: Profit-taking timing
**User:** "When should I take profits? The market has run up a lot."
**Action:** Runs full evaluation; maps score to risk budget and stair-step profit-taking rules (e.g., +20% take 25%); considers short-selling composite conditions.
**Output:** Risk budget, ATR tightening level, profit-taking percentage, and short-selling eligibility (if 3+ of 7 conditions met).

### Example 3: Social penetration check
**User:** "My barber and dentist are both recommending stocks. Does that add to bubble risk?"
**Action:** Applies Adjustment A (Social Penetration) with strict criteria: direct report, specific examples, 3+ independent sources. Without all three, scores +0.
**Output:** Explanation of whether criteria are met and impact on qualitative adjustment (0 or +1).

## Error Handling

| Error | Action |
|-------|--------|
| Phase 1 data missing | Do NOT proceed; collect Put/Call, VIX, margin debt, breadth, IPO before evaluating |
| Qualitative points without measurable evidence | Score 0; require Google Trends, specific media cites, or documented sources |
| Double-counting (P/E in Phase 2 and Phase 3) | Phase 3 Valuation Disconnect +1 only if P/E not already in quantitative score |
| Confirmation bias risk | Run checklist before adding qualitative points; document evidence for each |
