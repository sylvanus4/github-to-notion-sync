---
name: tossinvest-setup
description: >-
  Install tossctl CLI, authenticate via Playwright browser login, configure
  trading permissions, and run diagnostics for Toss Securities integration.
  Use when the user asks to "install tossctl", "toss login", "toss setup",
  "토스증권 설치", "토스 로그인", "토스 설정", or needs to configure tossctl for the first
  time. Do NOT use for read-only account/portfolio queries (use
  tossinvest-cli). Do NOT use for live trading operations (use
  tossinvest-trading). Do NOT use for general brokerage setup unrelated to
  Toss Securities.
---

# tossinvest-setup

Install, authenticate, configure, and diagnose the tossctl CLI for Toss Securities integration.

## When to Use

Use when the user asks to install tossctl, log in to Toss Securities, configure trading permissions, run tossctl diagnostics, or troubleshoot authentication issues.

## When NOT to Use

- For read-only queries (account, portfolio, quotes) → use `tossinvest-cli`
- For trading operations (buy, sell, cancel, amend) → use `tossinvest-trading`
- For Kiwoom Securities → use `tab-kiwoom`

## Prerequisites

- macOS or Linux (no Windows support)
- Python 3.9+ (for Playwright auth-helper)
- Internet access for initial installation
- A Toss Securities account with mobile app for login verification

## Procedure

### Step 1: Install tossctl

Check if tossctl is already installed:

```bash
command -v tossctl && tossctl version
```

If not installed, run the official installer:

```bash
curl -fsSL https://raw.githubusercontent.com/JungHoonGhae/tossinvest-cli/main/install.sh | bash
```

This installs:
- `tossctl` binary to `~/.local/bin/tossctl`
- `tossctl-auth-helper` Python package to `~/.local/share/tossctl/auth-helper/`

Verify `~/.local/bin` is in PATH:

```bash
echo $PATH | tr ':' '\n' | grep -q "$HOME/.local/bin" && echo "OK" || echo "Add ~/.local/bin to PATH"
```

### Step 2: Install Playwright Prerequisites

The auth-helper uses Playwright for browser-based login:

```bash
cd ~/.local/share/tossctl/auth-helper
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

### Step 3: Run Doctor Check

Verify everything is ready:

```bash
tossctl doctor
```

Expected output: all checks should pass. If any fail, follow the remediation hints.

For auth-specific diagnostics:

```bash
tossctl auth doctor
```

### Step 4: Initialize Configuration

Create the default config.json (all trading features disabled):

```bash
tossctl config init
```

View the current config:

```bash
tossctl config show
```

Config location: `~/.config/tossctl/config.json`

### Step 5: Authenticate (Browser Login)

Start the Playwright browser login flow:

```bash
tossctl auth login
```

This opens a Chromium browser window. The user must:
1. Log in to Toss Securities via the web interface
2. Complete mobile app verification if prompted
3. Wait for the CLI to capture the session

Verify the session:

```bash
tossctl auth status
```

### Step 6: Configure Trading Permissions (Optional)

Trading is **disabled by default**. Each capability must be explicitly enabled in `config.json`:

| Field | Default | Purpose |
|-------|---------|---------|
| `trading.grant` | `false` | Allow granting temporary execution permissions |
| `trading.place` | `false` | Allow placing new orders |
| `trading.sell` | `false` | Allow sell orders (requires `place`) |
| `trading.kr` | `false` | Allow Korean market orders |
| `trading.fractional` | `false` | Allow US fractional/market orders |
| `trading.cancel` | `false` | Allow canceling pending orders |
| `trading.amend` | `false` | Allow amending pending orders |
| `trading.allow_live_order_actions` | `false` | Master switch for all live mutations |
| `trading.dangerous_automation.*` | `false` | Automation flags for trade auth, product ack, FX consent |

Edit manually: `$EDITOR ~/.config/tossctl/config.json`

### Step 7: Session Management

Check session status:

```bash
tossctl auth status --output json
```

Clear session (logout):

```bash
tossctl auth logout
```

Import Playwright state from external source:

```bash
tossctl auth import-playwright-state <path-to-state.json>
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `command not found: tossctl` | Not installed or not in PATH | Re-run installer, add `~/.local/bin` to PATH |
| `No active session` | Not logged in or session expired | Run `tossctl auth login` |
| `playwright not found` | Auth-helper dependencies missing | Install via `pip3 install playwright && python3 -m playwright install chromium` |
| `Session: expired` | Toss web session timed out | Run `tossctl auth login` again |
| `config init` fails | Config directory not writable | Check permissions on `~/.config/tossctl/` |

## Local State Files

| File | Location | Purpose |
|------|----------|---------|
| `config.json` | `~/.config/tossctl/config.json` | Trading permission flags |
| `session.json` | `~/.config/tossctl/session.json` | Browser session cookies/tokens |
| `trading-permission.json` | `~/.config/tossctl/trading-permission.json` | TTL-based execution grants |
| `trading-lineage.json` | `~/.config/tossctl/trading-lineage.json` | Order ID lineage cache |

## Examples

### Example 1: Fresh installation

User: "토스증권 CLI 설치해줘"

Actions:
1. Check Go installed → `go version`
2. Install tossctl → `go install github.com/JungHoonGhae/tossinvest-cli/cmd/tossctl@latest`
3. Install Playwright → `pip install playwright && playwright install chromium`
4. Initialize config → `tossctl config init`
5. Run diagnostics → `tossctl doctor`
6. Report status

### Example 2: Re-authentication

User: "토스 세션 만료됐어"

Actions:
1. Check session status → `tossctl auth status`
2. Confirm expired
3. Re-login → `tossctl auth login`
4. Verify → `tossctl auth status`

## Important Notes

- **Unofficial API:** tossctl uses undocumented Toss Securities web APIs that may change without notice
- **TOS risk:** Usage may violate Toss Securities terms of service — user assumes responsibility
- **Session expiry:** Browser sessions expire; re-authenticate periodically
- **No API key:** Authentication is session-based via browser login, not API-key-based
