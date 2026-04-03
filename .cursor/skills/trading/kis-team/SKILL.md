---
name: kis-team
description: "Orchestrate the full KIS trading pipeline from strategy design through backtesting to signal-based order execution with stage-by-stage user confirmation. Coordinates kis-strategy-builder (Step 1), kis-backtester (Step 2), and kis-order-executor (Step 3) in sequence. Use when the user asks for 'end-to-end KIS flow', 'full pipeline', 'strategy to order', 'do everything', 'KIS team', '전략부터 주문까지', '다 해줘', 'KIS 파이프라인', '전체 프로세스'. Do NOT use for individual steps (invoke the specific kis-* skill directly). Do NOT use for Toss Securities operations (use toss-ops-orchestrator). Do NOT use for the daily stock pipeline (use today)."
---

# KIS Team Orchestrator

Coordinate the 3-stage KIS trading pipeline with explicit user confirmation between each stage.

## Stages

1. **Strategy Design** → `kis-strategy-builder`
   - Design indicators, entry/exit conditions, risk management
   - Output: `.kis.yaml` file

2. **Backtest Validation** → `kis-backtester`
   - Run the strategy against historical data
   - Evaluate metrics (Sharpe, drawdown, win rate)
   - If unsatisfactory, loop back to Stage 1

3. **Signal & Order Execution** → `kis-order-executor`
   - Generate live BUY/SELL/HOLD signals
   - Execute orders (VPS or prod) based on signal strength

## Rules

- Before Stage 1: check current KIS auth status via `scripts/kis/auth.py`
- Between each stage: present results and ask user whether to proceed, adjust, or stop
- Before Stage 3: if mode is `prod`, present a clear warning and require explicit confirmation
- On any stage failure: report the cause and ask whether to retry or adjust
- Never auto-advance without user confirmation
