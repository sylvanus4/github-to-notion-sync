---
description: "Run options theta trading analysis using 12 professional quant firm prompts (0DTE, iron condor, regime, skew, earnings IV crush, etc.)"
---

# Options Theta

## Skill Reference

Read and follow the skill at `.cursor/skills/trading-options-theta/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` names a specific strategy (e.g., "iron condor", "0DTE", "regime", "skew", "earnings") → route to that prompt
- If `$ARGUMENTS` is "daily" or "full" → run the combo workflow (regime → pre-market → trade setup → risk check)
- If `$ARGUMENTS` is "list" or "catalog" → show the prompt catalog from `references/prompt-catalog.md`
- If `$ARGUMENTS` contains market data (SPX price, VIX, ticker) → extract as parameters for the prompt
- If `$ARGUMENTS` is empty → show the catalog and ask the user to pick a strategy

### Step 2: Load Prompt

Read the matched prompt file from `.cursor/skills/trading-options-theta/references/prompt-XX-*.md`.

### Step 3: Collect Missing Parameters

Check the **Required inputs** section of the prompt file. If the user did not provide all required parameters, ask for the missing ones.

### Step 4: Execute

Fill the user's parameters into the `[ENTER ...]` placeholder and execute the complete prompt. Return the analysis in the format specified by the prompt.

### Step 5: Report

Summarize:
- Which strategy/prompt was used
- Key findings or trade setup details
- Append disclaimer: "This is not financial advice. Options trading involves significant risk of loss."

## Examples

Single strategy:
```
/options-theta 0DTE SPX 5850 VIX 18
```

Full daily workflow:
```
/options-theta daily SPX futures 5845 VIX 22
```

Earnings play:
```
/options-theta earnings NVDA March 12 IV 65% neutral
```

List all prompts:
```
/options-theta list
```

Weekly income setup:
```
/options-theta weekly $100k account moderate risk
```
