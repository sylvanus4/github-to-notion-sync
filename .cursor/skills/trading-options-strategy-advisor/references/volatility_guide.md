# Volatility Guide

## Historical vs Implied Volatility

**Historical Volatility (HV):** What happened
- Calculated from past price movements
- Objective, based on data
- Available for free (FMP API)
- Method: 90-day log returns, annualize with √252

**Implied Volatility (IV):** What market expects
- Derived from option prices
- Subjective, based on supply/demand
- Requires live options data (user provides from broker)

## Comparison

| Condition | Implication |
|-----------|-------------|
| IV > HV | Options expensive — consider selling premium |
| IV < HV | Options cheap — consider buying options |
| IV = HV | Fairly priced |

## IV Percentile

When user provides current IV, calculate percentile vs 1-year HV series:

```python
historical_hvs = calculate_hv_series(prices_1yr, window=30)
iv_percentile = percentileofscore(historical_hvs, current_iv)
```

**Guidance:**
- **IV percentile > 75:** High IV — consider selling premium (credit spreads, iron condors)
- **IV percentile < 25:** Low IV — consider buying options (long calls/puts, debit spreads)
- **IV percentile 25-75:** Normal IV — any strategy appropriate

## HV Calculation Method

```python
# Fetch 90 days of price data
prices = get_historical_prices(ticker, days=90)
returns = np.log(prices / prices.shift(1))
HV = returns.std() * np.sqrt(252)  # Annualized
```

Note to user: "HV = X%, consider using current market IV from broker for more accuracy."
