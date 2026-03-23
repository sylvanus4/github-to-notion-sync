---
name: agent-desk
description: Run multi-agent trading desk with bull/bear debate
---

Read the `trading-agent-desk` skill file at `.cursor/skills/trading-agent-desk/SKILL.md` and follow it to run the Agent Trading Desk pipeline.

Default behavior:
1. Load today's `analysis-{date}.json` and `screener-{date}.json` from `outputs/`
2. Select top 5 tickers with strongest BUY/SELL signals
3. Run the 4-phase pipeline per symbol: Analysts → Debate → Research Manager → Risk Evaluator
4. Save results to `outputs/agent-desk/{date}/desk-decisions.json`
5. Print a summary of decisions

User may provide:
- Specific symbols: `AAPL,TSLA,삼성전자` → run only those
- `--rounds N` → set debate rounds (default: 2)
- `--dry-run` → analyze but don't save to memory
- `--reflect` → run reflection on yesterday's decisions against actual returns
