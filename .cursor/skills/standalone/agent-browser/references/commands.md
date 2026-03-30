# Command Reference

Complete reference for all agent-browser commands (v0.16.3). For quick start and common patterns, see SKILL.md.

## Navigation

```bash
agent-browser open <url>      # Navigate to URL (aliases: goto, navigate)
                              # Supports: https://, http://, file://, about:, data://
                              # Auto-prepends https:// if no protocol given
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser (aliases: quit, exit)
agent-browser connect 9222    # Connect to browser via CDP port
```

## Snapshot (page analysis)

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -i -C      # Include cursor-interactive elements (divs with onclick)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
agent-browser snapshot --json     # JSON output for programmatic parsing
```

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Only interactive elements (buttons, links, inputs) |
| `-C, --cursor` | Include cursor-interactive elements (cursor:pointer, onclick) |
| `-c, --compact` | Remove empty structural elements |
| `-d, --depth <n>` | Limit tree depth |
| `-s, --selector <sel>` | Scope to CSS selector |
| `--json` | JSON output for parsing |

## Interactions (use @refs from snapshot)

```bash
agent-browser click @e1           # Click
agent-browser click @e1 --new-tab # Click and open in new tab
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key (alias: key)
agent-browser press Control+a     # Key combination
agent-browser keyboard type "text"     # Type at current focus (no selector)
agent-browser keyboard inserttext "t"  # Insert without key events
agent-browser keydown Shift       # Hold key down
agent-browser keyup Shift         # Release key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown option
agent-browser select @e1 "a" "b"  # Select multiple options
agent-browser scroll down 500     # Scroll page (default: down 300px)
agent-browser scroll down 500 --selector "div.content"  # Scroll container
agent-browser scrollintoview @e1  # Scroll element into view (alias: scrollinto)
agent-browser drag @e1 @e2        # Drag and drop
agent-browser upload @e1 file.pdf # Upload files
```

## Get Information

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box
agent-browser get styles @e1      # Get computed styles (font, color, bg, etc.)
```

## Check State

```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

## Semantic Locators (alternative to refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find text "Sign In" click --exact      # Exact match only
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find alt "Logo" click
agent-browser find title "Close" click
agent-browser find testid "submit-btn" click
agent-browser find first ".item" click
agent-browser find last ".item" click
agent-browser find nth 2 "a" hover
```

Actions: `click`, `fill`, `type`, `hover`, `focus`, `check`, `uncheck`, `text`

## Screenshots and PDF

```bash
agent-browser screenshot          # Save to temporary directory
agent-browser screenshot path.png # Save to specific path
agent-browser screenshot --full   # Full page
agent-browser screenshot --annotate  # Annotated with numbered labels
agent-browser pdf output.pdf      # Save as PDF
```

## Video Recording

```bash
agent-browser record start ./demo.webm    # Start recording
agent-browser record stop                 # Stop and save video
agent-browser record restart ./take2.webm # Stop current + start new
```

## Wait

```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text (or -t)
agent-browser wait --url "**/dashboard"    # Wait for URL pattern (or -u)
agent-browser wait --load networkidle      # Wait for network idle (or -l)
agent-browser wait --fn "window.ready"     # Wait for JS condition (or -f)
agent-browser wait --download ./file.zip   # Wait for download to complete
```

## Downloads

```bash
agent-browser download @e1 ./file.pdf          # Click element to trigger download
agent-browser wait --download ./output.zip     # Wait for any download
agent-browser --download-path ./downloads open <url>  # Set download directory
```

## Mouse Control

```bash
agent-browser mouse move 100 200      # Move mouse
agent-browser mouse down left         # Press button
agent-browser mouse up left           # Release button
agent-browser mouse wheel 100         # Scroll wheel
```

## Browser Settings

```bash
agent-browser set viewport 1920 1080          # Set viewport size
agent-browser set device "iPhone 14"          # Emulate device
agent-browser set geo 37.7749 -122.4194       # Set geolocation
agent-browser set offline on                  # Toggle offline mode
agent-browser set headers '{"X-Key":"v"}'     # Extra HTTP headers
agent-browser set credentials user pass       # HTTP basic auth
agent-browser set media dark                  # Emulate color scheme
agent-browser set media light reduced-motion  # Light mode + reduced motion
```

## Cookies and Storage

```bash
agent-browser cookies                     # Get all cookies
agent-browser cookies set name value      # Set cookie
agent-browser cookies set name val --url "https://..." --domain ".example.com"
agent-browser cookies clear               # Clear cookies

agent-browser storage local               # Get all localStorage
agent-browser storage local key           # Get specific key
agent-browser storage local set k v       # Set value
agent-browser storage local clear         # Clear all
agent-browser storage session             # Same for sessionStorage
```

## Network

```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body '{}'  # Mock response
agent-browser network unroute [url]            # Remove routes
agent-browser network requests                 # View tracked requests
agent-browser network requests --filter api    # Filter requests
```

## Tabs and Windows

```bash
agent-browser tab                 # List tabs
agent-browser tab new [url]       # New tab
agent-browser tab 2               # Switch to tab by index
agent-browser tab close           # Close current tab
agent-browser tab close 2         # Close tab by index
agent-browser window new          # New window
```

## Frames

```bash
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
```

## Dialogs

```bash
agent-browser dialog accept [text]  # Accept dialog
agent-browser dialog dismiss        # Dismiss dialog
```

## JavaScript

```bash
agent-browser eval "document.title"          # Simple expressions only
agent-browser eval -b "<base64>"             # Any JS (base64 encoded)
agent-browser eval --stdin                   # Read script from stdin
```

## Diff

```bash
agent-browser diff snapshot                              # Current vs last
agent-browser diff snapshot --baseline before.txt        # Current vs saved
agent-browser diff snapshot --selector "#main" --compact # Scoped diff
agent-browser diff screenshot --baseline before.png      # Visual pixel diff
agent-browser diff screenshot --baseline b.png -o d.png  # Save diff image
agent-browser diff screenshot --baseline b.png -t 0.2    # Color threshold
agent-browser diff url <url1> <url2>                     # Compare two URLs
agent-browser diff url <url1> <url2> --screenshot        # Also visual diff
agent-browser diff url <url1> <url2> --selector "#main"  # Scope to element
agent-browser diff url <url1> <url2> --wait-until networkidle
```

## Debug

```bash
agent-browser --headed open example.com   # Show browser window
agent-browser --cdp 9222 snapshot         # Connect via CDP port
agent-browser connect 9222                # Alternative: connect command
agent-browser console                     # View console messages
agent-browser console --clear             # Clear console
agent-browser errors                      # View page errors
agent-browser errors --clear              # Clear errors
agent-browser highlight @e1               # Highlight element
agent-browser trace start                 # Start recording trace
agent-browser trace stop trace.zip        # Stop and save trace
agent-browser profiler start              # Start Chrome DevTools profiling
agent-browser profiler stop trace.json    # Stop and save profile
```

## Auth State

```bash
agent-browser state save <file>             # Save auth state
agent-browser state load <file>             # Load auth state
agent-browser state list                    # List saved state files
agent-browser state show <name>             # Show state summary
agent-browser state rename <old> <new>      # Rename state file
agent-browser state clear [name]            # Clear states for session
agent-browser state clear --all             # Clear all saved states
agent-browser state clean --older-than <d>  # Delete old states
```

## Auth Vault

```bash
echo "pass" | agent-browser auth save <name> --url <url> --username <user> --password-stdin
agent-browser auth login <name>             # Login using saved profile
agent-browser auth list                     # List profiles
agent-browser auth show <name>              # Show profile
agent-browser auth delete <name>            # Delete profile
```

## Setup

```bash
agent-browser install                       # Download Chromium
agent-browser install --with-deps           # Also install system deps (Linux)
```

## Global Options

```bash
agent-browser --session <name> ...    # Isolated browser session
agent-browser --session-name <name> . # Auto-save/restore state
agent-browser --profile <path> ...    # Persistent browser profile
agent-browser --state <file> ...      # Load storage state
agent-browser --headers <json> ...    # HTTP headers scoped to URL's origin
agent-browser --executable-path <p>   # Custom browser executable
agent-browser --extension <path> ...  # Load extension (repeatable)
agent-browser --args <args> ...       # Browser launch args
agent-browser --user-agent <ua> ...   # Custom User-Agent
agent-browser --proxy <url> ...       # Proxy server
agent-browser --proxy-bypass <hosts>  # Hosts to bypass proxy
agent-browser --ignore-https-errors   # Ignore SSL certificate errors
agent-browser --allow-file-access     # Allow file:// URLs
agent-browser -p <provider> ...       # Cloud browser provider (--provider)
agent-browser --device <name> ...     # iOS device name
agent-browser --json ...              # JSON output
agent-browser --full, -f ...          # Full page screenshot
agent-browser --annotate ...          # Annotated screenshot
agent-browser --headed ...            # Show browser window
agent-browser --cdp <port/url> ...    # Connect via CDP
agent-browser --auto-connect ...      # Auto-discover Chrome
agent-browser --color-scheme <s> ...  # Color scheme (dark/light)
agent-browser --download-path <p> ... # Download directory
agent-browser --config <path> ...     # Custom config file
agent-browser --native ...            # Experimental Rust daemon
agent-browser --engine <name> ...     # Browser engine (chrome/lightpanda)
agent-browser --debug ...             # Debug output
```

## Environment Variables

```bash
AGENT_BROWSER_DEFAULT_TIMEOUT=25000         # Playwright timeout (ms)
AGENT_BROWSER_SESSION="name"                # Default session name
AGENT_BROWSER_SESSION_NAME="name"           # Auto-save/restore persistence
AGENT_BROWSER_PROFILE="/path"               # Persistent browser profile
AGENT_BROWSER_ENCRYPTION_KEY="64-hex"       # AES-256-GCM encryption key
AGENT_BROWSER_STATE_EXPIRE_DAYS=30          # Auto-delete old states
AGENT_BROWSER_EXECUTABLE_PATH="/path"       # Custom browser path
AGENT_BROWSER_EXTENSIONS="/ext1,/ext2"      # Extension paths
AGENT_BROWSER_ARGS="--flag1,--flag2"        # Browser launch args
AGENT_BROWSER_USER_AGENT="ua-string"        # Custom User-Agent
AGENT_BROWSER_PROXY="http://proxy:8080"     # Proxy server
AGENT_BROWSER_PROXY_BYPASS="localhost"      # Bypass proxy
AGENT_BROWSER_COLOR_SCHEME="dark"           # Color scheme
AGENT_BROWSER_DOWNLOAD_PATH="./downloads"   # Download directory
AGENT_BROWSER_ANNOTATE=1                    # Default annotated screenshots
AGENT_BROWSER_AUTO_CONNECT=1                # Auto-discover Chrome
AGENT_BROWSER_HEADED=1                      # Show browser window
AGENT_BROWSER_NATIVE=1                      # Use native Rust daemon
AGENT_BROWSER_ENGINE="lightpanda"           # Browser engine
AGENT_BROWSER_STREAM_PORT=9223              # WebSocket streaming port
AGENT_BROWSER_PROVIDER="browserbase"        # Cloud provider
AGENT_BROWSER_IOS_DEVICE="iPhone 16 Pro"    # iOS simulator device
AGENT_BROWSER_CONTENT_BOUNDARIES=1          # LLM-safe output markers
AGENT_BROWSER_ALLOWED_DOMAINS="*.example.com"  # Domain allowlist
AGENT_BROWSER_ACTION_POLICY="./policy.json" # Action policy file
AGENT_BROWSER_CONFIRM_ACTIONS="eval,download"  # Require confirmation
AGENT_BROWSER_MAX_OUTPUT=50000              # Output length limit
AGENT_BROWSER_CONFIG="./config.json"        # Custom config file
```
