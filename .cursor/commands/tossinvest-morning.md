---
description: "Morning portfolio briefing — account state, positions with overnight P&L, pending orders, risk snapshot, and market context from Toss Securities"
---

# Tossinvest Morning Briefing

## Skill Reference

Read and follow the skill at `.cursor/skills/toss-morning-briefing/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the comprehensive Toss Securities morning portfolio briefing:

1. **Auth check:** Verify session is active via `tossctl auth status --output json`. If expired, prompt re-auth and stop.

2. **Account snapshot:** Fetch account summary, portfolio positions, and pending orders.

3. **Yesterday comparison:** Load previous day's snapshot from `outputs/toss/` to compute overnight P&L changes.

4. **Risk snapshot:** Run inline risk assessment (concentration, buying power utilization, drawdown).

5. **Compose briefing:** Generate a comprehensive Korean morning briefing with:
   - Total assets, cash, and buying power
   - Top 5 holdings with current prices and P&L
   - Overnight changes (biggest movers)
   - Pending orders summary
   - Risk scorecard (GREEN/YELLOW/RED)

6. **Post to Slack:** Post to `#h-daily-stock-check` with threaded details.

If $ARGUMENTS contains "snapshot", also run `toss-daily-snapshot` to archive today's state.

## Constraints

- All commands are read-only — no trading mutations
- Requires tossctl installed and authenticated
- Use `--output json` for all commands
- Present final briefing in Korean
