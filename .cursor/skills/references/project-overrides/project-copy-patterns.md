# Project Copy Patterns — AI Stock Analytics

> Override for cloud UI copy patterns.
> Source: `docs/policies/03-tone-and-voice.md` (POL-003)

## Navigation Labels

Use noun form, max 4 characters recommended, 7 max:
- 대시보드, 이벤트, 종목, 분석, 리포트, 패턴
- English abbreviations OK: DualMA, GenAI, LLM, SEFO

## Button Labels

| Pattern | Examples |
|---------|----------|
| Verb form | 분석 실행, 백테스트 시작, 데이터 가져오기 |
| In progress | 실행 중..., 동기화 중..., 생성 중... |
| Disabled | `disabled:opacity-50` + tooltip explaining why |

## Empty States

```
[Icon]
Title: "아직 {item}이 없습니다"
Description: "{action}을 {verb}하여 시작하세요"
[CTA Button]
```

Examples:
- "아직 백테스트가 없습니다. 첫 번째 백테스트를 실행해보세요."
- "종목이 없습니다. CSV 데이터를 업로드해 주세요."

## Error Messages

```
Cause: "데이터를 불러오지 못했습니다"
Resolution: "다시 시도해 주세요" / "잠시 후 다시 시도해 주세요"
```

Patterns:
- Network: "데이터를 불러오는데 실패했습니다. 다시 시도해 주세요."
- Validation: "모든 필수 항목을 올바르게 입력해주세요"
- 404: "찾으시는 페이지가 존재하지 않거나 이동되었습니다"

## Help Text (? Button Tooltips)

Educational tone. Supplement technical terms with analogies:
- "TR (True Range)은 가격 변동성을 측정합니다."
- "N 값(ATR)은 TR의 지수이동평균으로 계산됩니다."
- Use code blocks for formulas when needed.

## Slack Notification Patterns

### #h-report (Professional summary)
```
📊 일일 분석 완료 (2026-03-25)
• BUY 시그널: 3건 (NVDA, GOOGL, 005930)
• SELL 시그널: 1건 (MRNA)
• 매매 적합도: 적합 (78/100)
```

### #h-daily-stock-check (Signal-focused)
Concise BUY/SELL stock list with per-stock details in thread.

### #효정-할일 (Action-oriented)
To-do list format, result reports.

## Multilingual Rules

- Default: Korean (ko)
- Supported: ko, en
- i18n location: `frontend/src/locales/{lang}/translation.json`
- Never translate proper nouns (NVDA, Bollinger, Donchian)
- Use English abbreviations in Korean text: RSI, MACD, ATR, CAR
