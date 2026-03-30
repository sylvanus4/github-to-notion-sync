# config.json Schema Reference

Schema version: 2 (`schema_version: 2`)

Location: `~/.config/tossctl/config.json`

## Full Schema

```json
{
  "schema_version": 2,
  "trading": {
    "grant": false,
    "place": false,
    "sell": false,
    "kr": false,
    "fractional": false,
    "cancel": false,
    "amend": false,
    "allow_live_order_actions": false,
    "dangerous_automation": {
      "complete_trade_auth": false,
      "accept_product_ack": false,
      "accept_fx_consent": false
    }
  }
}
```

## Field Descriptions

### Top-Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | integer | yes | Must be `2` |
| `trading` | object | yes | Trading permission configuration |

### trading

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `grant` | boolean | `false` | Allow `tossctl order permissions grant` to set a time-limited execution window |
| `place` | boolean | `false` | Allow placing new buy orders |
| `sell` | boolean | `false` | Allow sell orders (requires `place` to also be `true`) |
| `kr` | boolean | `false` | Allow Korean market (KRX) orders |
| `fractional` | boolean | `false` | Allow US fractional-share and market orders |
| `cancel` | boolean | `false` | Allow canceling pending orders |
| `amend` | boolean | `false` | Allow amending pending orders (price/quantity changes) |
| `allow_live_order_actions` | boolean | `false` | Master switch — must be `true` for any mutation to proceed |
| `dangerous_automation` | object | — | Automation flags for bypassing interactive confirmations |

### trading.dangerous_automation

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `complete_trade_auth` | boolean | `false` | Auto-complete trade authorization dialogs |
| `accept_product_ack` | boolean | `false` | Auto-accept product risk acknowledgements |
| `accept_fx_consent` | boolean | `false` | Auto-accept foreign exchange consent dialogs |

## Safety Implications

- All fields default to `false` — no trading is possible until explicitly enabled
- `allow_live_order_actions` is the master kill-switch: if `false`, no mutations execute regardless of other settings
- `dangerous_automation` fields bypass interactive safety dialogs — enable only for fully automated pipelines with separate risk controls
- Config changes take effect immediately on next command execution

## Validation

The JSON schema file is at: `~/thaki/tossinvest-cli/schemas/config.schema.json`

Validate with:

```bash
tossctl config show  # displays current config with any schema warnings
```
