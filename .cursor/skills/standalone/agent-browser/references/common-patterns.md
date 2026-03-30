# Common Patterns

Reusable recipes for frequent browser automation scenarios.

**Related**: [commands.md](commands.md) for full command reference, [SKILL.md](../SKILL.md) for quick start.

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

## Authentication with Auth Vault (Recommended)

Store credentials encrypted locally so the LLM never sees passwords:

```bash
echo "$PASSWORD" | agent-browser auth save github \
  --url https://github.com/login \
  --username "$USERNAME" --password-stdin

agent-browser auth login github
agent-browser auth list / auth show github / auth delete github
```

## Authentication with State Persistence

Login once, save state, reuse across sessions:

```bash
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

# Encrypt state at rest
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com
```

## Persistent Browser Profile

Full browser state (cookies, IndexedDB, cache, service workers) persists:

```bash
agent-browser --profile ~/.myapp-profile open https://myapp.com
agent-browser --profile ~/.myapp-profile open https://myapp.com/dashboard
```

## Data Extraction

```bash
agent-browser open https://example.com/products
agent-browser wait --load networkidle

agent-browser get text @e5           # Specific element
agent-browser get text body > page.txt  # All page text

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

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser --session site1 snapshot -i
agent-browser --session site2 snapshot -i
agent-browser session list
agent-browser --session site1 close
agent-browser --session site2 close
```

## Connect to Existing Chrome (CDP)

```bash
agent-browser --auto-connect snapshot          # Auto-discover running Chrome
agent-browser --cdp 9222 snapshot              # Explicit CDP port
agent-browser --cdp "wss://browser.com/cdp?token=..." snapshot  # Remote WebSocket
```

## iOS Simulator (Mobile Safari)

Requires macOS with Xcode, Appium (`npm install -g appium && appium driver install xcuitest`).

```bash
agent-browser device list
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios fill @e2 "text"
agent-browser -p ios swipe up
agent-browser -p ios screenshot mobile.png
agent-browser -p ios close

# Environment variables alternative
export AGENT_BROWSER_PROVIDER=ios
export AGENT_BROWSER_IOS_DEVICE="iPhone 16 Pro"
```

## Headed Mode (Visual Debugging)

```bash
agent-browser --headed open https://example.com
agent-browser highlight @e1
agent-browser record start demo.webm
agent-browser profiler start
agent-browser profiler stop trace.json
```

Use `AGENT_BROWSER_HEADED=1` to enable via env var. Extensions work in both headed and headless mode.

## Local Files (PDFs, HTML)

```bash
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

## Downloads

```bash
agent-browser download @e1 ./file.pdf          # Click to trigger download
agent-browser wait --download ./output.zip     # Wait for download
agent-browser --download-path ./downloads open <url>  # Set download dir
```

## Color Scheme (Dark Mode)

```bash
agent-browser --color-scheme dark open https://example.com
agent-browser set media dark  # Persist for session
# Or: AGENT_BROWSER_COLOR_SCHEME=dark
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
# Optional: KERNEL_STEALTH=true, KERNEL_PROFILE_NAME=myprofile
```

## Streaming (Live Browser Preview)

```bash
AGENT_BROWSER_STREAM_PORT=9223 agent-browser open https://example.com
# Connect WebSocket client to ws://localhost:9223 for live viewport stream
```

## Native Mode (Experimental)

```bash
agent-browser --native open example.com
# Or persist: export AGENT_BROWSER_NATIVE=1
# Use agent-browser close before switching modes
```

## Browser Engine Selection

```bash
agent-browser --engine lightpanda open example.com  # 10x faster
# Or: export AGENT_BROWSER_ENGINE=lightpanda
```

## Proxy Configuration

```bash
agent-browser --proxy "http://proxy:8080" open https://example.com
agent-browser --proxy "http://user:pass@proxy:8080" --proxy-bypass "localhost" open https://example.com  # pragma: allowlist secret
```

For detailed proxy patterns, see [proxy-support.md](proxy-support.md).

## Semantic Locators (Alternative to Refs)

```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```
