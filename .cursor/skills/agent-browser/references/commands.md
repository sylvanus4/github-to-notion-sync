# Agent Browser — Full Command Reference

All commands are prefixed with `agent-browser`.

## Table of Contents

- [Core Commands](#core-commands)
- [Get Info](#get-info) | [Check State](#check-state)
- [Find Elements](#find-elements-semantic-locators)
- [Wait](#wait) | [Mouse Control](#mouse-control)
- [Browser Settings](#browser-settings)
- [Cookies and Storage](#cookies-and-storage)
- [Network](#network) | [Tabs and Windows](#tabs-and-windows)
- [Frames](#frames) | [Dialogs](#dialogs)
- [Diff](#diff) | [Debug](#debug)
- [Auth State](#auth-state) | [Auth Vault](#auth-vault)
- [Navigation](#navigation) | [Setup](#setup)
- [Snapshot Options](#snapshot-options)

## Core Commands

```bash
open <url>                    # Navigate (aliases: goto, navigate)
click <sel>                   # Click element (--new-tab to open in new tab)
dblclick <sel>                # Double-click element
focus <sel>                   # Focus element
type <sel> <text>             # Type into element (appends)
fill <sel> <text>             # Clear and fill
press <key>                   # Press key (Enter, Tab, Control+a)
keyboard type <text>          # Type at current focus (no selector)
keyboard inserttext <text>    # Insert without key events
keydown <key>                 # Hold key down
keyup <key>                   # Release key
hover <sel>                   # Hover element
select <sel> <value>          # Select dropdown option
check <sel>                   # Check checkbox
uncheck <sel>                 # Uncheck checkbox
scroll <dir> [px]             # Scroll (up/down/left/right, --selector <sel>)
scrollintoview <sel>          # Scroll element into view
drag <from> <to>              # Drag and drop
upload <sel> <files>          # Upload files
screenshot [path]             # Screenshot (--full, --annotate)
pdf <path>                    # Save as PDF
snapshot                      # Accessibility tree with refs
eval <expr>                   # Run JavaScript (-b base64, --stdin piped)
connect <port>                # Connect to browser via CDP
close                         # Close browser (aliases: quit, exit)
```

## Get Info

```bash
get text <sel>                # Text content
get html <sel>                # innerHTML
get value <sel>               # Input value
get attr <sel> <name>         # Get attribute
get title                     # Page title
get url                       # Current URL
get count <sel>               # Count matching elements
get box <sel>                 # Bounding box
get styles <sel>              # Computed styles
```

## Check State

```bash
is visible <sel>              # Check if visible
is enabled <sel>              # Check if enabled
is checked <sel>              # Check if checked
```

## Find Elements (Semantic Locators)

```bash
find role <role> [action]           # By ARIA role (--name <name>, --exact)
find text <text> [action]           # By text content
find label <type> [action]          # By label
find placeholder <type> [action]    # By placeholder
find alt <text>                     # By alt text
find title <text>                   # By title attr
find testid <id> [action]           # By data-testid
find first <sel> [action]           # First match
find last <sel> [action]            # Last match
find nth <n> <sel> [action]         # Nth match
```

Actions: `click`, `fill`, `type`, `hover`, `focus`, `check`, `uncheck`, `text`

```bash
find role button click --name "Submit"
find text "Sign In" click
find label "Email" fill "test@test.com"
```

## Wait

```bash
wait <sel>                    # Wait for element visible
wait <ms>                     # Wait milliseconds
wait --text "Welcome"         # Wait for text
wait --url "**/dash"          # Wait for URL pattern
wait --load networkidle       # Wait for load state (load, domcontentloaded, networkidle)
wait --fn "window.ready"      # Wait for JS condition
wait --download ./file.zip    # Wait for download to complete
```

## Mouse Control

```bash
mouse move <x> <y>            # Move mouse
mouse down [button]           # Press (left/right/middle)
mouse up [button]             # Release
mouse wheel <dy> [dx]         # Scroll wheel
```

## Browser Settings

```bash
set viewport <w> <h>          # Set viewport size
set device <name>             # Emulate device ("iPhone 14")
set geo <lat> <lon>           # Set geolocation
set offline [on|off]          # Toggle offline mode
set headers <json>            # Extra HTTP headers
set credentials <user> <pass> # HTTP basic auth
set media [dark|light]        # Emulate color scheme
```

## Cookies and Storage

```bash
cookies                       # Get all cookies
cookies set <name> <value>    # Set cookie
cookies clear                 # Clear cookies

storage local                 # Get all localStorage
storage local <key>           # Get specific key
storage local set <k> <v>     # Set value
storage local clear           # Clear all

storage session               # Same for sessionStorage
```

## Network

```bash
network route <url>                # Intercept requests
network route <url> --abort        # Block requests
network route <url> --body <data>  # Mock response
network unroute [url]              # Remove routes
network requests                   # View tracked requests
network requests --filter api      # Filter requests
```

## Tabs and Windows

```bash
tab                           # List tabs
tab new [url]                 # New tab
tab <n>                       # Switch to tab n
tab close [n]                 # Close tab
window new                    # New window
```

## Frames

```bash
frame <sel>                   # Switch to iframe
frame main                    # Back to main frame
```

## Dialogs

```bash
dialog accept [text]          # Accept (with optional prompt text)
dialog dismiss                # Dismiss
```

## Diff

```bash
diff snapshot                              # Current vs last snapshot
diff snapshot --baseline before.txt        # Current vs saved file
diff snapshot --selector "#main" --compact # Scoped diff
diff screenshot --baseline before.png      # Visual pixel diff
diff screenshot --baseline b.png -o d.png  # Save diff image
diff screenshot --baseline b.png -t 0.2    # Color threshold (0-1)
diff url <url1> <url2>                     # Compare two URLs
diff url <url1> <url2> --screenshot        # Also visual diff
diff url <url1> <url2> --selector "#main"  # Scope to element
```

## Debug

```bash
trace start [path]            # Start recording trace
trace stop [path]             # Stop and save trace
profiler start                # Start Chrome DevTools profiling
profiler stop [path]          # Stop and save profile (.json)
console                       # View console messages
console --clear               # Clear console
errors                        # View page errors
errors --clear                # Clear errors
highlight <sel>               # Highlight element
```

## Auth State

```bash
state save <file>             # Save auth state
state load <file>             # Load auth state
state list                    # List saved state files
state show <name>             # Show state summary
state rename <old> <new>      # Rename state file
state clear [name]            # Clear states for session
state clear --all             # Clear all saved states
state clean --older-than <d>  # Delete old states
```

## Auth Vault

```bash
echo "pass" | auth save <name> --url <url> --username <user> --password-stdin
auth login <name>             # Login using saved profile
auth list                     # List profiles
auth show <name>              # Show profile
auth delete <name>            # Delete profile
```

## Navigation

```bash
back                          # Go back
forward                       # Go forward
reload                        # Reload page
```

## Setup

```bash
install                       # Download Chromium
install --with-deps           # Also install system deps (Linux)
```

## Snapshot Options

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Only interactive elements (buttons, links, inputs) |
| `-C, --cursor` | Include cursor-interactive elements (cursor:pointer, onclick) |
| `-c, --compact` | Remove empty structural elements |
| `-d, --depth <n>` | Limit tree depth |
| `-s, --selector <sel>` | Scope to CSS selector |
| `--json` | JSON output for programmatic parsing |
