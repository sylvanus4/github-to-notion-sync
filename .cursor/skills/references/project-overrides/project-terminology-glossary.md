# Project Terminology Glossary — AI Stock Analytics

> Override for cloud-platform terminology references.
> Source: `docs/policies/01-product-identity.md` (POL-001)

## Product Identity

| Key | Value |
|-----|-------|
| Product Name | AI Stock Analytics |
| Korean Name | AI 주식 분석 플랫폼 |
| Abbreviation | ASA |
| Domain | Financial Data Analysis · Event Study · Trading Strategy |

## Forbidden Terms

| Forbidden | Replacement | Reason |
|-----------|-------------|--------|
| Instance | 종목 / Ticker | Cloud computing term |
| Provisioning | 데이터 동기화 | Infra term |
| Quota | 한도 / 제한 | Cloud resource allocation |
| Tenant | 사용자 / 계정 | Multi-tenant SaaS |
| Namespace | 카테고리 / 섹터 | Kubernetes |
| Thaki Cloud | AI Stock Analytics | Other project |
| TDS / @thakicloud/shared | Tailwind + Radix | Other design system |
| Console | 대시보드 | Cloud console |
| Workload | 분석 / 백테스트 실행 | Container orchestration |

## Core Domain Terms

### Market & Trading
- 종목 (Ticker/Stock), 시가 (Open), 고가 (High), 저가 (Low), 종가 (Close)
- 거래량 (Volume), 매수 (Buy/Long), 매도 (Sell/Short), 포지션 (Position)
- 손익 (P&L), 손절 (Stop-loss), 포트폴리오 (Portfolio)

### Technical Analysis
- 이동평균선 (MA), 볼린저 밴드 (Bollinger Bands), RSI, MACD, ADX
- 돈치안 채널 (Donchian Channel), ATR, 스퀴즈 (Squeeze), 돌파 (Breakout)
- 눌림목 (Pullback), 시그널 (Signal)

### Event Study
- 누적 비정상 수익률 (CAR), 이벤트 윈도우, 벤치마크, 교란 요인, 유의성

### Strategy & Backtest
- 백테스트 (Backtest), 샤프 비율 (Sharpe Ratio), 최대 낙폭 (Max Drawdown)
- 승률 (Win Rate), 수익 팩터 (Profit Factor), 자본 곡선 (Equity Curve)
- 피라미딩 (Pyramiding), 유닛 (Unit), 리밸런싱 (Rebalancing)

### Sector Categories
`ai_semiconductor`, `ai_datacenter`, `defense`, `power`, `bio`, `hyperscaler`,
`platform`, `china_tech`, `benchmark`, `automotive`, `industrial`, `financial`

## User Personas

1. **개인 투자자 (김민수, 35세)** — 퇴근 후 효율적 분석, 감정적 매매 방지
2. **퀀트 트레이더 (이서연, 28세)** — 백테스트, GenAI 피처 탐색
3. **금융 분석가 (박준혁, 42세)** — AI 모델 발표가 주가에 미치는 영향 분석
