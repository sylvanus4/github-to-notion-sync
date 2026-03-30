---
name: role-trading-expert
description: >
  Analyze a given topic from the Trading Expert perspective — market environment impact, technical
  analysis, strategy validation, risk management, and sentiment assessment. Scores topic relevance
  (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes daily-stock-check, trading-technical-analyst, trading-market-environment-analysis,
  trading-backtest-expert, trading-position-sizer, trading-scenario-analyzer, alphaear-deepear-lite,
  trading-us-stock-analysis, alphaear-sentiment, alphaear-news, workflow-miner, semantic-guard,
  and intent-alignment-tracker.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "trading expert perspective", "트레이딩 전문가 관점", "매매 전문가 분석", "trading impact analysis".
  Do NOT use for running daily stock checks directly (use daily-stock-check),
  backtesting execution (use trading-backtest-expert), or weekly price updates (use weekly-stock-update).
  Korean triggers: "트레이딩 전문가 관점", "매매 전문가 분석", "트레이딩 영향 분석".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "role-analysis"
---

# Trading Expert Perspective Analyzer

Analyzes any business topic from the Trading Expert's viewpoint, covering market environment impact,
technical analysis, fundamental valuation, strategy validation, risk management, scenario planning,
sentiment analysis, and news-driven signal assessment.

## Relevance Criteria

Score the topic 1-10 based on overlap with trading concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Technical analysis | High | chart, SMA, RSI, MACD, Bollinger, Donchian, breakout, support, resistance |
| Market environment | High | macro, FOMC, rate, volatility, VIX, risk-on, risk-off, correlation |
| Trading strategy | High | Turtle, momentum, mean-reversion, backtest, signal, entry, exit |
| Risk management | High | position size, stop-loss, drawdown, Kelly, ATR, risk/reward |
| Fundamental analysis | High | P/E, EPS, revenue, FCF, valuation, earnings |
| Sentiment & news | Medium | sentiment, news, FOMC minutes, earnings call, social buzz |
| Market breadth | Medium | advance-decline, distribution day, breadth, participation |
| Options trading | Medium | options, Greeks, IV, theta, covered call, spread |
| Product & UX | Low | UI, user flow, design |
| HR & organization | Low | hiring, culture, retention |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Market Environment** (via `trading-market-environment-analysis`):
   - Global market overview (US, EU, Asia, commodities, forex)
   - Macro regime classification (risk-on/risk-off)
   - Key economic indicators and upcoming catalysts

2. **Technical Analysis** (via `trading-technical-analyst`):
   - Trend identification (SMA 20/55/200, Donchian channels)
   - Support and resistance levels
   - Oscillator readings (RSI, MACD, Stochastic, ADX)
   - Chart pattern recognition

3. **Fundamental Assessment** (via `trading-us-stock-analysis`):
   - Financial metrics analysis (P/E, EPS, revenue growth, FCF)
   - Business quality evaluation
   - Valuation framework and fair value estimation

4. **Signal Analysis** (via `daily-stock-check`):
   - Turtle Trading signal assessment (MA + Donchian)
   - Bollinger Bands signal assessment
   - Buy/sell/neutral classification

5. **Sentiment & News** (via `alphaear-sentiment` + `alphaear-news`):
   - Financial news aggregation from multiple sources
   - Sentiment scoring (positive/negative/neutral)
   - News-driven signal identification

6. **Risk & Position** (via `trading-position-sizer`):
   - Position sizing recommendations (Fixed Fractional, ATR, Kelly)
   - Stop-loss placement and risk/reward analysis
   - Portfolio concentration check

7. **Scenario Planning** (via `trading-scenario-analyzer`):
   - 18-month scenario analysis (bull/base/bear)
   - 1st/2nd/3rd-order impact mapping
   - Probability-weighted outcome assessment

8. **Strategy Validation** (via `trading-backtest-expert`):
   - Strategy backtesting methodology
   - Parameter robustness assessment
   - Out-of-sample validation recommendations

9. **Trading Workflow Discovery** (via `workflow-miner`):
   - Discover trading analysis workflow patterns from interaction history
   - Identify recurring analysis sequences (e.g., market scan → signal → position → execute)
   - Recommend automation for repetitive trading workflows

10. **Financial Data Security** (via `semantic-guard`):
    - Validate financial data outputs for accuracy signals
    - Scan trading recommendations for unauthorized disclosures
    - Check portfolio data for sensitive information exposure

11. **Strategy Alignment** (via `intent-alignment-tracker`):
    - Measure alignment between trading goals and analysis outcomes
    - Track signal accuracy and strategy performance alignment
    - Identify strategy drift and alignment gaps

## Output Format

```markdown
# 트레이딩 전문가 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 트레이딩 요약 (3-5 bullets)
- ...

## 시장 환경
### 글로벌 매크로 상황
### 리스크 온/오프 판단
### 주요 경제 지표 & 촉매

## 기술적 분석
### 추세 분석 (이동평균)
### 지지/저항 수준
### 오실레이터 판독
### 차트 패턴

## 펀더멘털 평가
### 핵심 재무 지표
### 비즈니스 품질
### 적정 가치 평가

## 시그널 분석
### 터틀 트레이딩 시그널
### 볼린저 밴드 시그널
### 매수/매도/중립 판정

## 센티먼트 & 뉴스
### 금융 뉴스 종합
### 센티먼트 점수
### 뉴스 기반 시그널

## 리스크 & 포지션
### 포지션 사이징 권고
### 손절 배치 & 리스크/리워드
### 포트폴리오 집중도

## 시나리오 분석
### 강세/기본/약세 시나리오
### 파급 효과 (1차/2차/3차)
### 확률 가중 평가

## 전략 검증
### 백테스트 방법론
### 파라미터 로버스트니스
### 아웃오브샘플 검증

## 워크플로우 패턴 분석
### 발견된 트레이딩 분석 패턴
### 워크플로우 자동화 기회

## 금융 데이터 보안
### 데이터 정확성 검증
### 민감 정보 노출 점검

## 의도 정렬 평가
### IA 점수 (0-100)
### 전략 정렬 추적
### 개선 필요 영역

## 트레이딩 권고
### 즉시 실행 가능한 트레이드 아이디어
### 중기 전략 방향
### 리스크 관리 체크리스트
### 모니터링 포인트
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "Impact of FOMC rate decision on tech sector allocation"

**Relevance Score**: 9/10 (market environment + technical + fundamental + sentiment + risk)

**Analysis highlights**:
- Market: Rate-sensitive sectors (tech, REITs) face headwinds; risk-off regime shift possible
- Technical: NASDAQ 100 testing 200-day SMA support, RSI approaching oversold
- Fundamental: High P/E tech names most vulnerable; strong FCF companies resilient
- Signal: Turtle short triggered on QQQ; Bollinger squeeze on SPY
- Sentiment: FOMC minutes hawkish tone; social media fear spike (+40%)
- Risk: Reduce tech allocation to 20% max; tighten stops to 2-ATR
- Scenario: Bear case -15% if 50bps hike; bull case +8% if dovish surprise
- Workflow: Discovered pattern "FOMC preview → sector rotation → rebalance" (frequency: 6)
- Security: Portfolio allocation data scanned — no PII leakage detected
- Alignment: Strategy IA score 82/100, gap in "side effects" dimension (cross-sector impact)
