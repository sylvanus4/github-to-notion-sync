---
description: "KIS account status — balance, holdings, and KOSPI/KOSDAQ index"
---

# KIS My Status

## Skill Reference

Read and follow the skill at `.cursor/skills/trading/kis-cs/SKILL.md` for customer-service tone guidance.

## Your Task

User input: $ARGUMENTS

Query KIS account information. Parse `$ARGUMENTS` to determine scope:

| Input | Subcommand | Description |
|---|---|---|
| (no args) | `balance` + `holdings` | Balance and holdings |
| `잔고`, `예수금`, `balance` | `balance` | Cash balance only |
| `보유종목`, `종목`, `holdings` | `holdings` | Holdings only |
| `코스피`, `지수`, `index` | `index` | KOSPI/KOSDAQ index |
| `전체`, `all` | `all` | Balance + holdings + index |

## Execution Steps

### 1. Check authentication

Run `uv run scripts/kis/auth.py`. If `authenticated` is `false`, tell the user: "먼저 `/kis-auth vps`로 인증하세요" and stop.

### 2. Query API

Run `uv run scripts/kis/api_client.py <subcommand>`.

### 3. Format results

Present JSON results as user-friendly Korean tables:

**Balance format:**

| 항목 | 값 |
|---|---|
| 계좌 | XXXX**** (모의투자) |
| 예수금 | 78,903,041원 |
| 총평가 | 102,242,541원 |
| 평가손익 | +2,330,500원 |

**Holdings format:**

| 종목 | 수량 | 평균단가 | 현재가 | 수익률 |
|---|---|---|---|---|
| SK하이닉스 | 15 | 808,466 | 894,000 | +10.58% |

**Index format:**

| 지수 | 현재 | 등락 | 등락률 |
|---|---|---|---|
| 코스피 | 2,650.12 | +15.3 | +0.58% |

## Constraints

- Format amounts with thousand-separator commas for readability
- Use `+`/`-` signs for profit/loss values
- Use the `account` field from JSON as-is (already masked)
- NEVER output tokens, appkey, appsecret, or any credentials
- Only reference script JSON output — never read config files directly
- Present final summary in Korean
