# Project Tone Matrix — AI Stock Analytics

> Override for cloud-platform tone guides.
> Source: `docs/policies/03-tone-and-voice.md` (POL-003)

## Tone by Context

| Context | Tone | Key Rule |
|---------|------|----------|
| Dashboard metrics | Concise, data-first | Numbers first, minimal prose |
| Trading signals | Cautious, neutral | Information, not advice; include disclaimer |
| Analysis reports | Professional, objective | Statistical terms accurate, cite evidence |
| Onboarding/help | Friendly, educational | Easy explanations, ? button tooltips |
| Error messages | Clear, action-oriented | Cause + resolution pattern |
| Slack notifications | Summary, actionable | Key numbers + detail in thread |
| Empty states | Guiding, motivating | Suggest next action |

## Signal Expression Rules

| Allowed | Forbidden | Reason |
|---------|-----------|--------|
| 매수 경보 / 롱 경보 | 지금 사세요 | No investment advice |
| 시그널이 감지됨 | 반드시 매매하세요 | No coercion |
| 추세 확인됨 | 확실히 오릅니다 | No exaggeration |
| 높은 신뢰도 | 100% 정확 | No guarantees |
| 눌림목 진입을 찾으세요 | 무조건 들어가세요 | Conditional only |

## Mandatory Disclaimer

All trading signal pages must include:

> 이 분석은 정보 제공 목적이며 투자 권유가 아닙니다.
> 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다.

## Number Formatting

| Item | Format | Example |
|------|--------|---------|
| Date | YYYY-MM-DD | 2026-03-25 |
| USD price | $#,##0.00 | $142.56 |
| KRW price | ₩#,##0 | ₩68,400 |
| Percentage | ±#0.00% | +2.34%, -1.23% |
| Volume | Abbreviated | 1.2M, 345K |
| Sharpe | 2 decimals | 1.45 |
| p-value | 4 decimals | 0.0234 |

## P&L Color Rules

- Profit: `+2.34%` (green / text-success-text)
- Loss: `-1.23%` (red / text-error-text)
- Neutral: `0.00%` (gray / text-foreground-muted)
