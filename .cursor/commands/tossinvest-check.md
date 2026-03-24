---
description: "Consolidated Toss Securities check — account summary, portfolio positions, pending orders, and session status"
---

# Tossinvest Check

## Skill Reference

Read and follow the skill at `.cursor/skills/tossinvest-cli/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run a consolidated Toss Securities health check. Execute these steps sequentially:

1. **Auth check:** `tossctl auth status --output json` — verify session is active. If expired, inform user and suggest `tossctl auth login`.

2. **Account summary:** `tossctl account summary --output json` — display balances and buying power.

3. **Portfolio positions:** `tossctl portfolio positions --output json` — display current holdings with P&L.

4. **Pending orders:** `tossctl orders list --output json` — display any open/pending orders.

5. **Summary:** Present a consolidated Korean summary with:
   - Total asset value and cash balance
   - Top holdings by value with P&L percentage
   - Any pending orders with status
   - Alerts: large unrealized losses (> -5%), pending orders near limit

If $ARGUMENTS contains specific symbols, also fetch quotes for those symbols via `tossctl quote batch`.

## Constraints

- All commands are read-only — no trading mutations
- Requires tossctl installed and authenticated
- Use `--output json` for all commands to enable structured parsing
- Present final summary in Korean
