# Financial Report Output Structure

Standard output template for AlphaEar Reporter. The final assembled report must follow this section order.

## Required Sections

```
## Executive Summary
  - Quick Scan table (Ticker | Direction | Confidence | Key Theme)
  - 3-5 sentence overview of major findings

## [Theme 1 Title]
  ### Background
    Macro/industry context for the theme
  ### Transmission Mechanism
    How the signal chain propagates to specific sectors/stocks
  ### Stock Impact
    Per-ticker analysis with ISQ scores (Confidence, Intensity)
    json-chart blocks for forecasts
  ### Predictions
    T+3/T+5 direction forecasts per ticker

## [Theme 2 Title]
  (same structure as Theme 1)

## [Theme N Title]
  (same structure)

## Risk Factors
  - Systematic risks identified across themes
  - Signal contradictions or low-confidence areas
  - Data quality warnings

## References
  - [@CITE_KEY] format, auto-collected from sections
  - Source URLs with access dates
```

## Chart Configuration Templates

### Forecast Chart

```json-chart
{
  "type": "forecast",
  "ticker": "TICKER_SYMBOL",
  "title": "Price Forecast",
  "pred_len": 5
}
```

### Comparison Chart

```json-chart
{
  "type": "comparison",
  "tickers": ["TICKER_1", "TICKER_2"],
  "title": "Relative Performance",
  "period": "3M"
}
```

### Signal Strength Chart

```json-chart
{
  "type": "signal_strength",
  "signals": ["signal_id_1", "signal_id_2"],
  "title": "ISQ Score Comparison"
}
```

## Section Quality Criteria

| Section | Min Length | Required Elements |
|---------|-----------|-------------------|
| Executive Summary | 200 words | Quick Scan table, overview paragraph |
| Theme Section | 500 words | Background, transmission, impact, predictions, 1+ chart |
| Risk Factors | 150 words | At least 3 identified risks |
| References | N/A | All `[@CITE_KEY]` resolved to full citations |
