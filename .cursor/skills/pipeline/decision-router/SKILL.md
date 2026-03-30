---
name: decision-router
description: >-
  Detect decision-worthy items from pipeline outputs and route them to the
  appropriate Slack decision channel. Personal decisions (trading, email replies,
  tool adoption) go to #효정-의사결정; team/CTO decisions (infra, strategy,
  partnerships, budget) go to #7층-리더방. Invoked inline by other pipeline
  skills after their main posting is complete. Use when a pipeline skill
  (google-daily, today, bespin-news-digest, twitter-timeline-to-slack,
  x-to-slack) detects content that requires a decision.
  Do NOT use standalone — always invoked as a sub-routine by pipeline skills.
  Do NOT use for general Slack messaging (use kwp-slack-slack-messaging).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---

# Decision Router

Centralized decision detection, scope classification, and Slack routing engine.
Pipeline skills invoke this as an inline sub-routine after completing their
normal posting workflow.

## Channel Registry

| Channel | ID | Scope | Description |
|---|---|---|---|
| `효정-의사결정` | `C0ANBST3KDE` | personal | Solo decisions (trading, email replies, tool adoption) |
| `7층-리더방` | `C0A6Q7007N2` | team | Team/CTO decisions (infra, strategy, partnerships, budget) |

> **Action Required**: Replace `C0ANBST3KDE` and `C0A6Q7007N2` with actual
> channel IDs after creating the channels in Slack. Use `slack_search_channels`
> MCP tool to retrieve IDs.

## Decision Detection Rules

Each source skill has specific criteria for what constitutes a "decision item."

### From `google-daily`

| Signal | Scope | Urgency |
|---|---|---|
| Colleague email requesting approval, budget, or architectural decision | team | HIGH |
| Email with explicit questions requiring a response decision | personal | MEDIUM |
| Calendar conflict needing resolution | personal | HIGH |
| Procurement/vendor request | team | MEDIUM |
| Keywords: 승인, 결정, 예산, 아키텍처, 채용, 제안, 검토 요청 | context-dependent | MEDIUM |

### From `twitter-timeline-to-slack`

| Signal | Scope | Urgency |
|---|---|---|
| Tool/technology with clear adoption-or-not signal (platform-level) | team | MEDIUM |
| Tool/technology with personal adoption signal | personal | LOW |
| Market-moving news requiring portfolio adjustment | personal | HIGH |
| Competitor announcement requiring strategic response | team | MEDIUM |

### From `x-to-slack`

| Signal | Scope | Urgency |
|---|---|---|
| GitHub repo/tool with "should we adopt?" framing (infra) | team | MEDIUM |
| Article proposing architectural pattern applicable to us | team | LOW |
| Content requiring team discussion | team | LOW |
| Personal tool or workflow suggestion | personal | LOW |

### From `bespin-news-digest`

| Signal | Scope | Urgency |
|---|---|---|
| Cloud provider pricing/service change affecting infrastructure | team | HIGH |
| Partnership or vendor opportunity | team | MEDIUM |
| Competitive product launch requiring response | team | MEDIUM |
| Product feature idea derived from industry trend | team | LOW |

### From `today`

| Signal | Scope | Urgency |
|---|---|---|
| STRONG_BUY signal with composite score >= 8 | personal | HIGH |
| STRONG_SELL signal with high confidence | personal | HIGH |
| Multiple correlated signals in same sector | personal | MEDIUM |
| RSI extreme (> 80 or < 20) with ADX > 25 | personal | MEDIUM |
| Screener STRONG BUY stocks not in portfolio | personal | MEDIUM |

## Scope Classification

### Personal (`#효정-의사결정`)

Any of the following criteria:

- Trading/portfolio/stock decisions
- Personal tool adoption (not platform-level)
- Email reply triage (respond/ignore/delegate)
- Calendar scheduling conflicts
- Content follow-up decisions

### Team (`#7층-리더방`)

Any of the following criteria:

- Infrastructure/architecture decisions
- Product strategy, feature, or roadmap decisions
- Cloud service provider or vendor decisions
- Partnership or business development opportunities
- Competitive response strategies
- Budget, procurement, or investment decisions
- Security or compliance decisions
- Hiring or organizational decisions
- Anything impacting the AI Platform team or CTO's domain

## Message Template

```
*[DECISION]* {urgency_badge} | 출처: {source_skill}

*{Decision Title}*

*배경*
{1-3 sentence context from the source content}

*판단 필요 사항*
{Clear statement of what needs to be decided}

*옵션*
A. {option A} — {brief pro/con}
B. {option B} — {brief pro/con}
C. 보류 / 추가 조사 필요

*추천*
{recommended option with 1-sentence rationale}

*긴급도*: {HIGH / MEDIUM / LOW}
*원본*: <{source_url_or_thread}|{source title}>
```

### Urgency Badges

| Urgency | Badge | Meaning |
|---|---|---|
| HIGH | `:rotating_light:` | Decision within 24h |
| MEDIUM | `:large_orange_circle:` | Decision within 1 week |
| LOW | `:white_circle:` | Can wait |

## Invocation Pattern

Pipeline skills invoke the decision router as follows:

1. After the skill's normal posting is complete, review the processed content
2. Apply the source-specific decision detection rules (see tables above)
3. For each detected decision item, classify scope (personal vs team)
4. Format using the DECISION message template
5. Post to the appropriate channel via `slack_send_message`:
   - Personal → `효정-의사결정` (`C0ANBST3KDE`)
   - Team → `7층-리더방` (`C0A6Q7007N2`)
6. If multiple decisions are detected, post each as a separate message (not threaded)

### Threshold Principle

Default to **NOT** posting a decision. Only post when the signal is clear and
actionable. When uncertain, err on the side of skipping — false negatives are
preferable to noisy channels.

### Skip Flag

All pipeline skills support `skip-decisions` to bypass decision extraction.

## MCP Tool Reference

| Tool | Server | Purpose |
|---|---|---|
| `slack_send_message` | `plugin-slack-slack` | Post decision messages |

## Examples

### Example 1: Trading decision from `today`

Signal: AAPL STRONG_BUY with composite score 9.2, RSI 35 (oversold), ADX 32 (strong trend)

```
*[DECISION]* :rotating_light: | 출처: today

*AAPL 매수 포지션 진입 검토*

*배경*
AAPL이 종합 점수 9.2로 STRONG_BUY 시그널 발생. RSI 35로 과매도 구간이며 ADX 32로 강한 추세 확인. 이동평균선 정배열 상태.

*판단 필요 사항*
과매도 반등 구간에서 매수 포지션 진입 여부

*옵션*
A. 현재가 기준 포지션 진입 — RSI 과매도 + 강한 추세 + 정배열 삼박자
B. 추가 하락 대기 — 지지선 테스트 후 진입
C. 보류 / 추가 조사 필요

*추천*
A. 3가지 기술적 시그널이 동시 충족되어 진입 적기로 판단

*긴급도*: HIGH
*원본*: outputs/reports/daily-2026-03-19.docx
```

### Example 2: Team decision from `bespin-news-digest`

Signal: AWS announces 40% GPU instance price reduction

```
*[DECISION]* :rotating_light: | 출처: bespin-news-digest

*AWS GPU 인스턴스 40% 가격 인하 대응*

*배경*
AWS가 P5 인스턴스(H100 기반) 가격을 40% 인하 발표. ThakiCloud의 GPU 클라우드 가격 경쟁력에 직접적 영향.

*판단 필요 사항*
ThakiCloud GPU 인스턴스 가격 정책 조정 및 차별화 전략 수립 여부

*옵션*
A. 가격 매칭 + 관리형 서비스 차별화 — 가격 동등화 후 MLOps/모니터링 부가가치로 차별화
B. 가격 유지 + 성능/지원 강조 — 마진 유지하면서 엔터프라이즈 지원 품질로 차별화
C. 보류 / 추가 조사 필요

*추천*
A. 가격 격차가 40%로 크기 때문에 매칭이 필수적이며, 관리형 서비스 부가가치로 수익 보전

*긴급도*: HIGH
*원본*: <https://press-thread-link|AWS GPU 가격 인하 기사>
```
