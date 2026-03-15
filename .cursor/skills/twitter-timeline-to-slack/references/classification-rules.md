# Tweet Classification Rules

## Category Definitions

Each rule has: keywords (case-insensitive), a weight multiplier, and a target Slack channel.

### AI Coding (weight: 1.5x) → #ai-coding-radar
Keywords: cursor, copilot, claude code, windsurf, vscode, ide, codegen, code generation, mcp, tool use, function calling, agentic, ai agent, ai coding, devin, codex, openai codex, code review, ai developer, coding assistant, dev tool, github copilot, cline, aider, bolt, v0, replit, software engineering agent, swe-bench, swe agent

### Prompt Engineering (weight: 1.3x) → #prompt
Keywords: prompt, system prompt, few-shot, chain of thought, cot, instruction, prompt engineering, jailbreak, prompt injection, reasoning, thinking, xml tags, prompt template, zero-shot, in-context learning, icl

### Research (weight: 1.2x) → #deep-research
Keywords: paper, arxiv, research, transformer, llm architecture, benchmark, evaluation, pretraining, fine-tuning, rlhf, scaling law, attention, diffusion, multimodal, embedding, rag, retrieval, training, model, neural, deep learning, machine learning, compute, inference, quantization, distillation, mixture of experts, moe, vision language, openai, anthropic, google deepmind, meta ai, mistral

### Press/News (weight: 1.0x) → #press
Keywords: launch, announce, release, funding, acquisition, billion, million, ipo, series, startup, valuation, partnership, collaboration, breaking, exclusive, report, news, update, officially, introducing, unveiled

### Stock/Finance (weight: 1.3x) → #효정-주식
Keywords: stock, market, nvda, aapl, tsla, msft, amzn, goog, trading, invest, etf, earnings, portfolio, dividend, bull, bear, nasdaq, spy, qqq, s&p, dow, crypto, bitcoin, btc, ethereum, kospi, kosdaq, 주식, 투자, 매수, 매도, 시장, 코인, 상장, 급등, 급락, 선물, 레버리지, 배당, 종목, 수익률

### Ideas (weight: 0.9x) → #idea
Keywords: idea, concept, what if, imagine, shower thought, hot take, unpopular opinion, theory, hypothesis, proposal, vision, dream, build, create, prototype, experiment, hack, side project

### Insights (weight: 1.1x) → #효정-insight
Keywords: trend, analysis, insight, prediction, future, strategy, pattern, observation, lesson, takeaway, framework, mental model, principle, important, thread, deep dive, perspective, reflection, opinion, 인사이트, 전략, 분석, 비즈니스, 방향, 교훈, 패턴, 관점, 프레임워크, 핵심

### Tasks/Action (weight: 0.8x) → #효정-할일
Keywords: todo, must, need to, reminder, deadline, follow up, action item, check out, look into, try this, bookmark, save for later, read later

### Default → #random
No keyword matches or score of 0.

## Scoring Algorithm

1. For each category, count keyword matches in the tweet text (case-insensitive)
2. Short ASCII keywords (≤3 chars) use word boundary matching to prevent false positives (e.g., "btc" won't match inside "abstract")
3. Multiply match count by the category's weight
4. Select the highest-scoring category
5. Ties are broken by priority order (higher weight wins)
6. Score of 0 → default to #random
