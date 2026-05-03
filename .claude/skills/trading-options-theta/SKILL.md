---
name: trading-options-theta
description: >-
  Run professional-grade options theta trading analysis using 12
  quant-firm-style prompts covering 0DTE credit spreads, market regime
  classification, iron condors, theta decay tracking, strike selection,
  pre-market analysis, risk management, volatility skew exploitation, weekly
  income calendars, earnings IV crush, EOD scalping, and monthly performance
  dashboards. Use when the user asks for "options theta", "credit spread
  setup", "iron condor", "0DTE trade", "theta decay", "premium selling", "IV
  crush", "skew trade", "market regime", "theta scalp", "options income", "옵션
  세타", "세타 매매", "프리미엄 매도", "아이언 콘도르", "크레딧 스프레드", or any options
  premium-selling / theta income strategy request. Do NOT use for stock
  fundamental analysis (use daily-stock-check). Do NOT use for futures or
  commodity trading. Do NOT use for crypto options. Do NOT use for long
  options buying strategies (these are short premium / theta strategies only).
---

# Options Theta Trading — 12 Quant Firm Prompts

Professional options theta income strategies modeled after methodologies from Tastytrade, Citadel, SIG, Two Sigma, D.E. Shaw, Jane Street, Wolverine Trading, Akuna Capital, Peak6, IMC Trading, and Optiver.

For the full prompt catalog, see [references/prompt-catalog.md](references/prompt-catalog.md).
For source attribution, see [references/source-attribution.md](references/source-attribution.md).

## Input

The user provides:
1. **Strategy type** — specific strategy name, keyword, or "daily"/"full" for combo workflow
2. **Market parameters** — varies by prompt (SPX price, VIX, account size, positions, etc.)

## Workflow

### Step 1: Identify Strategy

Map the user's request to one or more prompts using this routing table:

| User Says | Prompt(s) | File |
|-----------|-----------|------|
| "0DTE", "credit spread", "SPX spread" | 01 | [prompt-01-0dte-credit-spread.md](references/prompt-01-0dte-credit-spread.md) |
| "regime", "market conditions", "green yellow red" | 02 | [prompt-02-market-regime.md](references/prompt-02-market-regime.md) |
| "theta decay", "theta calculator", "hourly income" | 03 | [prompt-03-theta-decay.md](references/prompt-03-theta-decay.md) |
| "strike selection", "probability", "delta" | 04 | [prompt-04-strike-selection.md](references/prompt-04-strike-selection.md) |
| "iron condor", "both sides", "range trade" | 05 | [prompt-05-iron-condor.md](references/prompt-05-iron-condor.md) |
| "pre-market", "morning briefing", "8 AM" | 06 | [prompt-06-pre-market-edge.md](references/prompt-06-pre-market-edge.md) |
| "risk management", "loss limit", "circuit breaker" | 07 | [prompt-07-risk-management.md](references/prompt-07-risk-management.md) |
| "skew", "jade lizard", "broken wing" | 08 | [prompt-08-volatility-skew.md](references/prompt-08-volatility-skew.md) |
| "weekly", "weekly calendar", "mon-fri" | 09 | [prompt-09-weekly-income.md](references/prompt-09-weekly-income.md) |
| "earnings", "IV crush", "earnings play" | 10 | [prompt-10-earnings-crush.md](references/prompt-10-earnings-crush.md) |
| "EOD", "end of day", "final 90 minutes", "scalp" | 11 | [prompt-11-eod-theta-scalp.md](references/prompt-11-eod-theta-scalp.md) |
| "dashboard", "performance", "monthly review" | 12 | [prompt-12-monthly-dashboard.md](references/prompt-12-monthly-dashboard.md) |
| "daily", "full", "morning workflow" | Combo: 02 → 06 → 01/05 → 07 | See [Combo Workflow](#combo-workflow) |
| "list", "catalog", "show prompts" | — | Show the prompt catalog table |

If the user's intent is ambiguous, show the catalog table and ask which strategy they want.

### Step 2: Collect Parameters

Read the matched prompt file from `references/`. Check the **Required inputs** and **Input Template** sections. Ask the user for any missing parameters.

### Step 3: Execute Prompt

Fill the user's parameters into the `[ENTER ...]` placeholder at the end of the prompt. Execute the complete prompt and return the analysis.

### Step 4: Report

Present the analysis in the format specified by the prompt (trade ticket, regime report, dashboard, etc.). Always append the disclaimer: "This is not financial advice. Options trading involves significant risk of loss."

#### Global Wrapper (Apply to Every Prompt Output)

After executing a prompt file, wrap the result with these **additional** labeled blocks (prepend summary, append risk):

1. `### Executive Summary` — 3–5 bullets: regime (if any), structure name, **≥3 user-supplied numbers** echoed (e.g., SPX 5850, VIX 18, width $X).
2. `### Trade Structure` — Strikes, widths, credit/debit, max loss/profit — **numeric**; use `[USER INPUT]` placeholders only when data missing (and ask).
3. `### Action Plan` — Entry, management, exit — **actionable** ordered steps.
4. `### Risk & Invalidation` — Min **one** of: max loss, stop as % of premium, or “exit if underlying crosses **price**”; tail/gap risk for 0DTE.
5. `### Data Provenance` — List which figures came from user vs model assumption; **no** invented earnings dates or strikes.

If the user request maps to **covered call** or other long-premium strategies, reply that this skill is **short premium / theta only** and point to `trading-options-strategy-advisor`.

**Closing line:** One sentence — trade **on / modified / pass** for the session.

## Combo Workflow

When the user asks for a "daily" or "full" workflow, chain prompts in this sequence:

1. **Regime check** — Run prompt 02 (Citadel Market Regime Classifier)
   - If RED → recommend sitting in cash, stop here
   - If YELLOW → proceed with wider strikes
   - If GREEN → proceed normally
2. **Pre-market briefing** — Run prompt 06 (Jane Street Pre-Market Edge)
3. **Trade setup** — Based on regime output:
   - Range-bound market → Run prompt 05 (D.E. Shaw Iron Condor)
   - Trending market → Run prompt 01 (Tastytrade 0DTE Credit Spread, directional side only)
4. **Strike optimization** — Run prompt 04 (Two Sigma Strike Selection) for the chosen setup
5. **Risk check** — Run prompt 07 (Wolverine Risk Management) against the proposed trades

Pass the output of each step as context to the next step for coherent analysis.

## Examples

### Example 1: Single prompt — 0DTE setup

User says: "Set up a 0DTE credit spread. SPX is at 5850, VIX is 18, no major events today."

Actions:
1. Route to prompt 01 (Tastytrade 0DTE Credit Spread Scanner)
2. Read `references/prompt-01-0dte-credit-spread.md`
3. Fill template: "Today's setup: March 8, 2026, SPX at 5850, VIX at 18, no major economic events"
4. Execute and return Tastytrade-style trade ticket

Result: Complete 0DTE trade setup with exact strikes, entry price, max profit/loss, and exit rules.

### Example 2: Combo daily workflow

User says: "Run the full daily theta workflow. SPX futures at 5845, VIX at 22."

Actions:
1. Run prompt 02 → Regime verdict: YELLOW (elevated VIX, sell conservatively)
2. Run prompt 06 → Morning briefing with scenario playbook
3. Run prompt 05 → Iron condor with wider strikes per YELLOW regime
4. Run prompt 04 → Optimized strikes at 0.10 delta for higher probability
5. Run prompt 07 → Risk check: position size within limits

Result: Complete morning analysis package with regime, briefing, trade setup, and risk validation.

### Example 3: Earnings play

User says: "NVDA earnings next week, IV is at 65%, I'm neutral."

Actions:
1. Route to prompt 10 (IMC Trading Earnings Theta Crusher)
2. Fill template: "NVDA, earnings March 12, current IV 65%, neutral bias"
3. Execute and return IV crush trade plan

Result: IMC-style earnings volatility plan with strike placement, position sizing, and post-earnings exit protocol.

### Example 4: Show catalog

User says: "What theta prompts do you have?"

Actions:
1. Read `references/prompt-catalog.md`
2. Present the full table with categories and recommended daily workflow

Result: Organized catalog of all 12 prompts with usage guidance.

## Error Handling

| Error | Action |
|-------|--------|
| No market data provided | Ask user for SPX price and VIX level at minimum |
| Unknown strategy keyword | Show the routing table and ask user to pick |
| Prompt file not found | List available files in `references/` and suggest closest match |
| Multiple strategies match | Present matched options and ask user to choose |
| User asks for long options | Explain this skill is for short premium / theta only; suggest other resources |
| Missing account size for risk prompts | Default to hypothetical $50,000 account with disclaimer |
