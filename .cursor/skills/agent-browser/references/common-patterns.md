# Agent Browser — Common Patterns

Reusable recipes for frequent browser automation scenarios.

## Table of Contents

- [Form Submission](#form-submission)
- [Authentication with Auth Vault](#authentication-with-auth-vault)
- [Authentication with State Persistence](#authentication-with-state-persistence)
- [Session Persistence](#session-persistence-auto-saverestore)
- [Persistent Browser Profile](#persistent-browser-profile)
- [Data Extraction](#data-extraction)
- [Parallel Sessions](#parallel-sessions)
- [Connect to Existing Chrome](#connect-to-existing-chrome-cdp)
- [iOS Simulator](#ios-simulator-mobile-safari)
- [Headed Mode](#headed-mode-visual-debugging)
- [Local Files](#local-files) | [Downloads](#downloads)
- [Color Scheme](#color-scheme-dark-mode)
- [Cloud Browser Providers](#cloud-browser-providers)

## Form Submission

```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4
agent-browser click @e5
agent-browser wait --load networkidle
agent-browser snapshot -i  # verify result
```

## Authentication with Auth Vault

Store credentials encrypted locally so the LLM never sees passwords:

```bash
# Save once (pipe password to avoid shell history)
echo "$PASSWORD" | agent-browser auth save github \
  --url https://github.com/login \
  --username "$USERNAME" \
  --password-stdin

# Login using saved profile
agent-browser auth login github

# Manage profiles
agent-browser auth list
agent-browser auth show github
agent-browser auth delete github
```

## Authentication with State Persistence

Login once, save state, reuse across sessions:

```bash
# Login flow
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Future sessions
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Session Persistence (Auto-Save/Restore)

Cookies and localStorage persist across browser restarts:

```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # state auto-saved

# Next time, state auto-loaded
agent-browser --session-name myapp open https://app.example.com/dashboard
```

Encrypt state at rest:

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com
```

## Persistent Browser Profile

Full browser state (cookies, IndexedDB, cache, service workers) persists:

```bash
agent-browser --profile ~/.myapp-profile open https://myapp.com
# login once, then reuse:
agent-browser --profile ~/.myapp-profile open https://myapp.com/dashboard
```

## Data Extraction

```bash
agent-browser open https://example.com/products
agent-browser wait --load networkidle

# Specific element text
agent-browser get text @e5

# All page text
agent-browser get text body > page.txt

# JSON output for parsing
agent-browser snapshot -i --json
agent-browser get text @e1 --json

# Complex extraction via JS
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(
  Array.from(document.querySelectorAll(".product"))
    .map(p => ({
      name: p.querySelector(".name")?.textContent,
      price: p.querySelector(".price")?.textContent
    }))
)
EVALEOF
```

## Parallel Sessions

Run multiple independent browser instances:

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com

agent-browser --session site1 snapshot -i
agent-browser --session site2 snapshot -i

agent-browser session list

# Cleanup
agent-browser --session site1 close
agent-browser --session site2 close
```

## Connect to Existing Chrome (CDP)

```bash
# Auto-discover running Chrome with remote debugging
agent-browser --auto-connect snapshot

# Explicit CDP port
agent-browser --cdp 9222 snapshot

# Remote WebSocket URL
agent-browser --cdp "wss://browser-service.com/cdp?token=..." snapshot
```

## iOS Simulator (Mobile Safari)

Requires macOS with Xcode, Appium (`npm install -g appium && appium driver install xcuitest`).

```bash
agent-browser device list

# Launch on specific device
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios fill @e2 "text"
agent-browser -p ios swipe up
agent-browser -p ios screenshot mobile.png
agent-browser -p ios close
```

Environment variables alternative:

```bash
export AGENT_BROWSER_PROVIDER=ios
export AGENT_BROWSER_IOS_DEVICE="iPhone 16 Pro"
agent-browser open https://example.com
```

## Headed Mode (Visual Debugging)

```bash
agent-browser --headed open https://example.com
agent-browser highlight @e1
agent-browser profiler start
# ... actions ...
agent-browser profiler stop trace.json
```

## Local Files

```bash
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser screenshot output.png
```

## Downloads

```bash
agent-browser download @e1 ./file.pdf          # click to trigger download
agent-browser wait --download ./output.zip      # wait for download
agent-browser --download-path ./downloads open <url>  # set download dir
```

## Color Scheme (Dark Mode)

```bash
agent-browser --color-scheme dark open https://example.com
# or persist for session:
agent-browser set media dark
```

## Cloud Browser Providers

### Browserbase

```bash
export BROWSERBASE_API_KEY="your-api-key"
export BROWSERBASE_PROJECT_ID="your-project-id"
agent-browser -p browserbase open https://example.com
```

### Browser Use

```bash
export BROWSER_USE_API_KEY="your-api-key"
agent-browser -p browseruse open https://example.com
```

### Kernel

```bash
export KERNEL_API_KEY="your-api-key"
agent-browser -p kernel open https://example.com
```
