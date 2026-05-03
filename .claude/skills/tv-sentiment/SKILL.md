---
name: tv-sentiment
description: >-
  Analyze market sentiment via Reddit social data and financial news through
  TradingView MCP (`market_sentiment`, `financial_news`, `combined_analysis`).
---

# TV Sentiment

Analyze market sentiment via Reddit social data and financial news through TradingView MCP (`market_sentiment`, `financial_news`, `combined_analysis`).

## Triggers

Use when the user asks to "check Reddit sentiment via TV", "TV sentiment", "financial news via MCP", "combined TA + sentiment", "TradingView 감성 분석", "TV 레딧 감성", "TV 금융 뉴스", "TV 결합 분석", "tv-sentiment", or wants MCP-powered sentiment and news analysis.

Do NOT use for AlphaEar sentiment scoring (use `alphaear-sentiment`). Do NOT use for AlphaEar news aggregation (use `alphaear-news`). Do NOT use for general web search news (use `WebSearch`).

## Adapter

`backend/app/services/tradingview_mcp_adapter.py` — `TradingViewSentimentService` singleton: `sentiment_service`

## Workflow

### Mode 1: Reddit Sentiment

1. Call `sentiment_service.get_reddit_sentiment(symbol, category, limit)`
2. Categories: `stocks`, `crypto`, `options`, `wallstreetbets`
3. Returns: post count, bullish/bearish ratio, top discussions, sentiment score

### Mode 2: Financial News

1. Call `sentiment_service.get_financial_news(symbol, category, limit)`
2. Returns: recent headlines with source, timestamp, relevance score
3. Optional symbol filter for ticker-specific news

### Mode 3: Combined Analysis (TA + Sentiment + News)

1. Call `sentiment_service.combined_analysis(symbol, exchange, timeframe)`
2. Confluence of technical analysis, Reddit sentiment, and financial news
3. Produces a unified bullish/bearish/neutral verdict with confidence score

## Output Format

Report results in Korean with:
- Sentiment scores (bullish/bearish/neutral percentages)
- Key discussion themes and catalysts
- News headline summary with impact assessment
- Combined verdict with confidence level when using Mode 3
