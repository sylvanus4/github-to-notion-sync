# Daily Stock Check Slack Message Template

## Message Structure

```
:chart_with_upwards_trend: *Daily Stock Check — {date}*
Analyzed {total_stocks} stocks | :green_circle: BUY {buy_count} | :white_circle: NEUTRAL {neutral_count} | :red_circle: SELL {sell_count}

---

:large_green_circle: *BUY / STRONG_BUY*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} — {turtle_rationale}
> Bollinger: {bb_signal} — {bb_rationale}
> Overall: *{overall_signal}*

---

:white_circle: *NEUTRAL*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} | BB: {bb_signal}

---

:red_circle: *SELL / STRONG_SELL*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} — {turtle_rationale}
> Bollinger: {bb_signal} — {bb_rationale}
> Overall: *{overall_signal}*

---

_Turtle: SMA(20,50) + Donchian(20) | Bollinger: BB(20,2σ) + %B + Squeeze_
_Data source: data/latest/ CSVs | This is not financial advice._
```

## Grouping Rules

- Group stocks by overall signal: BUY/STRONG_BUY first, then NEUTRAL, then SELL/STRONG_SELL
- NEUTRAL stocks: compact one-line format (ticker, price, change, signals)
- BUY/SELL stocks: full rationale with multi-line detail

## Emoji Indicators

| Signal | Emoji |
|--------|-------|
| BUY / STRONG_BUY | :green_circle: / :large_green_circle: |
| NEUTRAL | :white_circle: |
| SELL / STRONG_SELL | :red_circle: / :large_red_circle: |

## Size Limit

If the message exceeds 4000 characters, split into multiple messages:
1. Header (summary counts)
2. BUY section
3. NEUTRAL section (if large)
4. SELL section + footer
