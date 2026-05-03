---
name: today
description: Daily stock data sync, screening, technical analysis, and Korean report generation pipeline.
disable-model-invocation: true
---

Run the full daily stock analysis pipeline.

## Pipeline Phases

1. **Data Sync**: Check DB vs CSV freshness, backfill via multi-provider fallback (Yahoo/Polygon/Tiingo/Alpha Vantage/Finnhub)
2. **Hot Stock Discovery**: Discover hot stocks from NASDAQ/KOSPI/KOSDAQ 100
3. **Multi-Factor Screening**: P/E, RSI, volume, MA crossovers, FCF yield
4. **Technical Analysis**: SMA 20/55/200, RSI, MACD, Stochastic, ADX for all tracked tickers
5. **News & Sentiment** (optional): Fetch news via alphaear-news, score via alphaear-sentiment
6. **Report Generation**: Korean .docx buy/sell report via anthropic-docx
7. **Strategy Engine**: 7-strategy backtested cards, output top 10
8. **Slack Distribution**: Post summary and strategy cards to #h-report
9. **KB Ingest**: Route daily outputs into trading-daily Knowledge Base

## Output

- `outputs/today/{date}/` directory with manifest.json
- Korean DOCX report
- Slack thread with BUY/SELL recommendations
- Strategy cards with commission-aware returns

## Options

- `--with-tradingview`: Cross-validate with TradingView MCP
- `--skip-tradingview`: Skip extended TradingView stages
- `--with-pine`: Generate Pine Script v5 indicators
