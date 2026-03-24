# Tweet Classification Rules

## Channel Philosophy

- **#press** is the default catch-all. Anything that doesn't clearly fit another category goes here.
- **#random** is NEVER used as a destination.
- **#ai-coding-radar** is very strict: only practical Claude Code / Cursor workflow content.
- **#idea** has a high bar: truly insightful ideas relevant to AI GPU Cloud business.

## Category Definitions

Each rule has: keywords (case-insensitive), a weight multiplier, and a target Slack channel.

### AI Coding (weight: 1.3x) → #ai-coding-radar
Scope: Practical Claude Code / Cursor tips that help developers in daily work. NOT general AI agent news.
Keywords: claude code, cursor, copilot, windsurf, cline, aider, github copilot, claude cowork, cursor rule, cursor skill, cursor plugin, .cursorrules, agents.md, harness engineering, autoresearch

### Prompt Engineering (weight: 1.3x) → #prompt
Keywords: prompt, system prompt, few-shot, chain of thought, cot, instruction, prompt engineering, jailbreak, prompt injection, reasoning, thinking, xml tags, prompt template, zero-shot, in-context learning, icl

### Research (weight: 1.3x) → #deep-research-trending
Scope: Academic papers, new model releases/architectures, benchmarks. NOT general AI news.
Keywords: paper, arxiv, transformer, llm architecture, benchmark, evaluation, pretraining, fine-tuning, rlhf, scaling law, attention, diffusion, multimodal, embedding, rag, retrieval, quantization, distillation, mixture of experts, moe, vision language, qwen, llama, gemma, phi, nemotron, glm, deepseek, gemini, abliterated, uncensored

### Stock/Finance (weight: 1.5x) → #효정-주식
Scope: Crypto, stocks, trading, market analysis, macro economics, prediction markets.
Keywords: stock, nvda, aapl, tsla, msft, amzn, goog, trading, invest, etf, earnings, portfolio, dividend, bull, bear, nasdaq, spy, qqq, s&p, dow, crypto, bitcoin, btc, ethereum, kospi, kosdaq, polymarket, prediction market, 예측시장, 부동산, 금리, fed, fomc, 환율, forex, 원유, oil, commodity, cpi, 인플레이션, 채권, bond, 금값, gold, defi, nft, blockchain, stablecoin, 스테이블코인, binance, 바이낸스, 주식, 투자, 매수, 매도, 코인, 상장, 급등, 급락, 선물, 레버리지, 배당, 종목, 수익률, 트레이딩, 드러켄밀러, 버핏, 단타, 수익, wall street, trader

### Ideas (weight: 1.3x) → #idea
Scope: Business insights, AI GPU Cloud ideas, practical frameworks, and actionable patterns. Absorbs business-relevant keywords from insights.
Keywords: idea, what if, imagine, shower thought, hot take, unpopular opinion, proposal, prototype, experiment, hack, side project, gpu cloud, ai infrastructure, ai platform, gpu cluster, inference service, ai startup, monetization, competitive advantage, 아이디어, game changer, use case, opportunity, disruption, 1인개발, 사이드프로젝트, saas, business model, solo developer, indie dev, built my own, i built, 비즈니스, framework, 프레임워크, pattern, 패턴, 핵심, insight, 인사이트, observation

### Insights (weight: 0.9x) → #효정-insight (축소)
Scope: Pure analysis, learning methods, strategic lessons — NOT business ideas or frameworks.
Keywords: trend, analysis, prediction, future, strategy, lesson, takeaway, mental model, principle, thread, deep dive, perspective, reflection, opinion, 전략, 분석, 방향, 교훈, 관점

### Tasks/Action (weight: 0.8x) → #효정-할일
Keywords: todo, must, need to, reminder, deadline, follow up, action item, check out, look into, try this, bookmark, save for later, read later

### Press/News (weight: 1.1x) → #press (DEFAULT)
Scope: General news, announcements, and the catch-all for anything that doesn't match above categories.
Keywords: launch, announce, release, funding, acquisition, billion, million, ipo, series, startup, valuation, partnership, collaboration, breaking, exclusive, report, news, update, officially, introducing, unveiled, open source, open-source, github, star, trending, viral, just dropped, 공개, 출시, 발표, 속보, 등장

## Scoring Algorithm

1. For each category, count keyword matches in the tweet text (case-insensitive)
2. Short ASCII keywords (≤3 chars) use word boundary matching to prevent false positives (e.g., "btc" won't match inside "abstract")
3. Multiply match count by the category's weight
4. Select the highest-scoring category
5. Ties are broken by priority order (higher weight wins)
6. Score of 0 → default to #press
