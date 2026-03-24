# 6-Layer Safety Model — Detailed Reference

## Overview

The tossctl 6-layer safety model prevents accidental live trading by requiring explicit opt-in at every stage. Each layer is a distinct gate that must be passed — no layer can be bypassed.

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: config.json                                │
│   Static gate — operation type must be allowed      │
│   File: ~/.config/tossctl/config.json               │
├─────────────────────────────────────────────────────┤
│ Layer 2: permissions grant --ttl                    │
│   Temporal gate — time-limited execution window     │
│   File: ~/.config/tossctl/trading-permission.json   │
├─────────────────────────────────────────────────────┤
│ Layer 3: preview (no --execute)                     │
│   Informational gate — shows what would happen      │
│   Outputs: order details + confirmation token       │
├─────────────────────────────────────────────────────┤
│ Layer 4: --execute flag                             │
│   Intent gate — explicit "I want to mutate" signal  │
├─────────────────────────────────────────────────────┤
│ Layer 5: --dangerously-skip-permissions             │
│   Risk acknowledgement gate                         │
│   "I understand this is a live trade"               │
├─────────────────────────────────────────────────────┤
│ Layer 6: --confirm <token>                          │
│   Cryptographic gate — token from Layer 3 preview   │
│   Proves the execution matches a specific preview   │
└─────────────────────────────────────────────────────┘
```

## Layer Details

### Layer 1: Static Configuration

**What:** JSON config file that acts as an allowlist for operation types.
**Where:** `~/.config/tossctl/config.json`
**Persistence:** Until manually edited.
**Bypass:** Not possible via CLI. Must edit the file directly.

Config matrix:

| I want to… | Required fields set to `true` |
|------------|-------------------------------|
| Buy US stock (limit) | `place`, `allow_live_order_actions` |
| Buy KR stock | `place`, `kr`, `allow_live_order_actions` |
| Buy US fractional/market | `place`, `fractional`, `allow_live_order_actions` |
| Sell any | `sell`, `place`, `allow_live_order_actions` |
| Cancel pending | `cancel`, `allow_live_order_actions` |
| Amend pending | `amend`, `allow_live_order_actions` |

### Layer 2: Temporal Permissions

**What:** Time-limited execution window stored in a local permission file.
**Where:** `~/.config/tossctl/trading-permission.json`
**TTL options:** `1m`, `5m`, `10m`, `15m`, `30m`
**Recommended:** `5m` for manual trading. Shorter is safer.

```bash
# Grant
tossctl order permissions grant --ttl 5m

# Check status
tossctl order permissions status
```

The permission file records:
- Grant timestamp
- Expiry timestamp
- Granting user context

### Layer 3: Preview

**What:** Dry-run that shows exactly what would happen without mutating anything.
**Output includes:**
- Order type, side, symbol, quantity, price
- Estimated total cost / proceeds
- Fee estimates
- Market status
- A **confirmation token** (opaque string)

The confirmation token is a hash binding the specific preview parameters. It cannot be reused for different order parameters.

### Layer 4: --execute Flag

**What:** Boolean CLI flag that signals intent to perform a live mutation.
**Without it:** Command runs in preview-only mode (Layer 3).
**With it:** Proceeds to Layer 5 and 6 checks.

### Layer 5: --dangerously-skip-permissions

**What:** Explicit acknowledgement flag. The name is deliberately alarming.
**Purpose:** Forces the operator to consciously acknowledge the risk.
**Note:** Despite the name, this does NOT actually skip the Layer 2 permission check — it is an additional acknowledgement on top of it.

### Layer 6: --confirm <token>

**What:** The confirmation token from Layer 3 preview output.
**Purpose:** Cryptographically binds execution to a specific preview.
**Rules:**
- Must match the exact token from the most recent preview
- Tokens are single-use
- Tokens expire (tied to the preview session)
- Different order parameters produce different tokens

## Agent Enforcement Protocol

When an AI agent handles a trading request:

1. **Read config** → Check Layer 1 requirements
2. **IF config insufficient** → Tell user which fields to enable, STOP
3. **Grant permissions** → Layer 2 with appropriate TTL
4. **Run preview** → Layer 3, capture the output including token
5. **Present preview to user** → Show all details clearly
6. **WAIT for user confirmation** → Never auto-confirm
7. **IF user confirms** → Execute with all three flags (Layer 4+5+6)
8. **Verify execution result** → Check for success/failure
9. **Report outcome** → Show order ID, status

## Order Lineage

Successful executions are recorded in `~/.config/tossctl/trading-lineage.json`. This file tracks:
- Order IDs
- Timestamps
- Operation types
- Parameters used

This enables order recovery and audit trails.
