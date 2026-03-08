# Market News Impact Scoring Framework

Use when assessing and ranking news events by market impact significance.

## Three Dimensions

### 1. Asset Price Impact (Primary Factor)

**Equity Markets:**
- Index-level (S&P 500, Nasdaq): Severe ±2%+, Major ±1-2%, Moderate ±0.5-1%, Minor ±0.2-0.5%, Negligible <0.2%
- Sector-level: Severe ±5%+, Major ±3-5%, Moderate ±1-3%, Minor <1%
- Stock-specific (mega-caps): Severe ±10%+, Major ±5-10%, Moderate ±2-5%

**Commodity Markets:**
- Oil: Severe ±5%+, Major ±3-5%, Moderate ±1-3%
- Gold: Severe ±3%+, Major ±1.5-3%, Moderate ±0.5-1.5%
- Base metals: Severe ±4%+, Major ±2-4%, Moderate ±1-2%

**Bond Markets (10Y Treasury):** Severe ±20bps+, Major ±10-20bps, Moderate ±5-10bps

**Currency (DXY):** Severe ±1.5%+, Major ±0.75-1.5%, Moderate ±0.3-0.75%

### 2. Breadth of Impact (Multiplier)

| Breadth | Multiplier | Examples |
|---------|------------|----------|
| Systemic | 3x | FOMC surprise, banking crisis, major war |
| Cross-Asset | 2x | Inflation surprise, geopolitical supply shock |
| Sector-Wide | 1.5x | Tech earnings cluster, energy policy |
| Stock-Specific | 1x | Single company earnings, M&A |

### 3. Forward-Looking Significance (Modifier)

| Type | Modifier | Examples |
|------|----------|----------|
| Regime Change | +50% | Fed pivot, major geopolitical realignment |
| Trend Confirmation | +25% | Consecutive strong inflation, earnings beats |
| Isolated Event | 0% | Single data point, company-specific |
| Contrary Signal | -25% | Good news ignored, bad news rallied |

## Score Calculation

```
Impact Score = (Price Impact Score × Breadth Multiplier) + Forward-Looking Modifier

Price Impact Score:
- Severe: 10 points
- Major: 7 points
- Moderate: 4 points
- Minor: 2 points
- Negligible: 1 point
```

## Example Calculations

**FOMC 75bps hawkish:** Price 10 × Systemic 3 × Forward +25% = 37.5

**NVIDIA earnings beat:** Price 10 × Sector 1.5x × Forward +25% = 18.75

**Geopolitical flare-up:** Price 10 × Cross-asset 2x × Isolated 0% = 20

**Single stock earnings:** Price 7 × 1x × 0% = 7

**Ranking:** Sort all events by Impact Score descending.
