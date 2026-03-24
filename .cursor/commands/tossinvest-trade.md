---
description: "Interactive Toss Securities trading with mandatory 6-layer Safety Model enforcement"
---

# Tossinvest Trade

## Skill Reference

Read and follow the skill at `.cursor/skills/tossinvest-trading/SKILL.md`.
Also reference `.cursor/skills/tossinvest-trading/references/safety-model.md` for the full 6-layer safety model.

## Your Task

User input: $ARGUMENTS

Execute a trading operation on Toss Securities following the **mandatory 6-layer Safety Model**. No layer may be skipped.

### Workflow

1. **Parse intent** from $ARGUMENTS — determine operation (buy/sell/cancel/amend), symbol, quantity, price.

2. **Layer 1 — Config check:** Run `tossctl config show` and verify all required config fields are enabled for this operation type. If any field is missing, list the exact fields that need to be set to `true` and STOP.

3. **Layer 2 — Permissions grant:** Run `tossctl order permissions grant --ttl 5m`. If permissions are already active, verify they have not expired.

4. **Layer 3 — Preview:** Run the order command WITHOUT `--execute` to get a preview and confirmation token. Present the full preview to the user in Korean including:
   - Operation type (매수/매도/취소/정정)
   - Symbol and name
   - Quantity and price
   - Estimated total cost or proceeds
   - Fees
   - The confirmation token

5. **User confirmation gate:** Ask the user to explicitly confirm. Use AskQuestion tool:
   - Option A: "확인 — 주문 실행" (Confirm — execute order)
   - Option B: "취소 — 주문 중단" (Cancel — abort order)

6. **IF user confirms (Option A):**
   - Layer 4+5+6: Execute with `--execute --dangerously-skip-permissions --confirm <TOKEN>`
   - Report the result (order ID, status)

7. **IF user cancels (Option B):**
   - Abort. Inform user the order was not placed.

8. **Post-execution:** Run `tossctl orders list --output json` to verify the order appears.

## Constraints

- **ALL 6 LAYERS ARE MANDATORY** — never skip any layer
- **NEVER fabricate a confirmation token** — only use the exact token from preview output
- **NEVER auto-confirm** — always wait for explicit user approval via AskQuestion
- **REAL MONEY is at stake** — treat every command as irreversible
- Present all information in Korean
- If any layer fails, explain why and STOP — do not attempt workarounds
