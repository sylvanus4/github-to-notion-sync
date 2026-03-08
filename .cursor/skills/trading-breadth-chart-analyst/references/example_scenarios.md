# Breadth Chart Analysis Example Scenarios

Reference examples for conducting breadth chart analysis. Use when demonstrating workflow or validating analysis approach.

## Example 1: Strategic Breadth Analysis (Chart 1 Only)

**User:** "Please analyze this S&P 500 breadth chart and tell me where we are in the market cycle."
[Provides Chart 1 image: 200MA Breadth Index]

**Workflow:**
1. Confirm receipt of Chart 1
2. Read breadth_chart_methodology.md for Chart 1 guidance
3. View sample chart for format reference
4. Extract: 8MA, 200MA, slopes, distance from 73%/23%
5. Identify signals: 8MA trough, 200MA peak
6. Assess regime (e.g. Overheated Bull approaching Distribution)
7. Determine strategy: Long preparing to exit; watch for 200MA peak
8. Develop scenarios with probabilities
9. Generate: breadth_200ma_analysis_[DATE].md in outputs/reports/trading/

## Example 2: Tactical Uptrend Ratio Analysis (Chart 2 Only)

**User:** "Should I be buying or selling here? Analyze this uptrend ratio chart."
[Provides Chart 2 image: Uptrend Stock Ratio]

**Workflow:**
1. Confirm Chart 2 receipt
2. Read methodology for Chart 2
3. Extract: Current ratio, color, slope, distances from 10%/40%
4. Identify transitions: red-to-green, green-to-red
5. Assess condition (e.g. Early in new uptrend from extreme oversold)
6. Determine: ENTER LONG if signal active
7. Develop scenarios
8. Generate: uptrend_ratio_analysis_[DATE].md

## Example 3: Combined Strategic + Tactical (Both Charts)

**User:** "Analyze both breadth charts and give me your overall market view."
[Provides both charts]

**Workflow:**
1. Confirm both charts
2. Read full methodology
3. Analyze Chart 1: Regime, strategy position
4. Analyze Chart 2: Condition, trading position
5. Combined assessment: Scenario 1-4 alignment
6. Unified recommendation for long-term, swing, active traders
7. Generate: breadth_combined_analysis_[DATE].md

## Scenario Classification (Combined Analysis)

| Scenario | Chart 1 | Chart 2 | Implication |
|----------|---------|---------|-------------|
| 1. Both Bullish | 8MA rising, 200MA not peaked | Green, ratio rising from oversold | Maximum bullish |
| 2. Strategic Bull, Tactical Bear | 8MA rising | Red, ratio falling/elevated | Hold core, wait for tactical entry |
| 3. Strategic Bear, Tactical Bull | 200MA peaked/declining | Green, ratio rising | Short-term trades only, tight stops |
| 4. Both Bearish | Both MAs declining | Red | Defensive, cash or shorts |
