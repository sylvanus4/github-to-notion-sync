---
description: "KIS authentication management — check status, authenticate VPS/prod/WebSocket, switch modes"
---

# KIS Auth

## Skill Reference

Read and follow the skill at `.cursor/skills/trading/kis-order-executor/SKILL.md` for safety context.

## Your Task

User input: $ARGUMENTS

Manage KIS (Korea Investment & Securities) authentication. Parse `$ARGUMENTS` to determine the action:

| Input | Action |
|---|---|
| `모의`, `vps`, `paper` | VPS (paper trading) REST auth |
| `실전`, `prod`, `real` | Production REST auth |
| `ws 모의`, `ws vps` | VPS WebSocket auth |
| `ws 실전`, `ws prod` | Production WebSocket auth |
| `switch`, `전환` | Toggle mode (VPS↔prod) |
| (no args) | Check current status, then ask user |

## Execution Steps

### 1. Check current status

Run `uv run scripts/kis/auth.py` and inspect the JSON output.

### 2. Execute authentication

Based on parsed arguments, call `uv run scripts/kis/do_auth.py <args>`:

- REST auth: `do_auth.py <mode>` (where mode is `vps` or `prod`)
- WebSocket auth: `do_auth.py ws <mode>`
- Mode switch: `do_auth.py switch`

### 3. Verify result

Check the JSON output for `success`:
- **Success**: Report `action`, `mode_display`, and `expires` to the user.
- **Failure**: Report the `error` field message.

### 4. Re-check status

Run `uv run scripts/kis/auth.py` again to confirm the auth state is correctly reflected.

## Constraints

- NEVER output tokens, appkey, appsecret, or any credentials
- Only reference script JSON output — never read `kis_devlp.yaml` directly
- For **production (`prod`) auth**, require explicit user confirmation before proceeding
- For **mode switch (`switch`)**, warn that existing tokens will be invalidated
- For WebSocket auth, only confirm `approval_key` issuance — never output the key value
- Present final summary in Korean
