# Financial Domain Tone Guide

Supplements the default cloud-tone-matrix for products in the **financial analytics, trading, and investment** domain.

## Tone principles

| Principle | Cloud default | Financial override |
|---|---|---|
| Formality | Neutral | Neutral-to-formal (financial data demands precision) |
| Urgency | Context-dependent | Higher baseline (market-moving data is time-sensitive) |
| Directness | Moderate | High (traders prefer unambiguous signals over hedging) |
| Emotional tone | Calm, reassuring | Factual, confidence-inspiring (avoid emotional language around gains/losses) |

## Category-specific guidance

### Trading signals & scores

- Use precise numeric labels: "RSI 72.3" not "RSI is high"
- BUY/SELL/NEUTRAL: uppercase, unambiguous, no softening
- Score labels: use the raw number + contextual indicator ("68/100 — Moderate")
- Avoid subjective modifiers like "great", "terrible", "amazing performance"

### Error messages (financial context)

- Always state **what data is affected** and **what the user should do**
- Time-sensitivity matters: "Data delayed by 15 min" vs generic "Data unavailable"
- For trading-critical errors: lead with impact, then cause, then action

```
✅ "실시간 시세 연결 끊김 — 표시된 가격이 지연될 수 있습니다. 새로고침하거나 대체 소스를 확인하세요."
❌ "오류가 발생했습니다. 다시 시도해 주세요."
```

### Dashboard labels

- Prefer domain-standard abbreviations traders already know: P/E, RSI, ADX, MACD, SMA
- Expand on first occurrence in tooltips, not in the label itself
- Use sentence case for descriptions, ALL CAPS only for signal verdicts

### Risk / disclaimer copy

- Regulatory disclaimers must be verbatim — never paraphrase legal text
- Separate AI-generated analysis from factual market data visually and textually
- Standard disclaimer pattern:

```
"이 분석은 AI가 생성한 참고 자료이며, 투자 조언이 아닙니다. 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다."
```

## Glossary additions (financial)

| Term | Use | Avoid |
|---|---|---|
| 매수 신호 | Standard | 사세요, 사야 합니다 |
| 매도 신호 | Standard | 파세요, 팔아야 합니다 |
| 중립 | Neutral signal | 관망 (acceptable in commentary, not in UI labels) |
| 수익률 | Return rate | 이익률 |
| 변동성 | Volatility | 리스크 (different concept) |
| 시가총액 | Market cap | 기업 가치 (different concept) |

## When to apply

Apply this guide when the product or feature context involves:
- Stock/crypto/forex price data
- Trading signals, screeners, or alerts
- Portfolio analysis or P&L reporting
- Financial report generation
- Market environment or breadth analysis

For general cloud/SaaS UI elements (auth, settings, navigation), fall back to the standard cloud-tone-matrix.
