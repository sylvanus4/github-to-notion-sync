---
name: carbonyl-browser
description: >-
  Browse the web inside the terminal using Carbonyl — a Chromium-based browser
  that renders real web pages with Unicode and ANSI escape sequences. Supports
  interactive browsing, zoom, frame rate control, and bitmap rendering. Use when
  the user asks to "browse in terminal", "terminal browser", "open a page in the
  terminal", "carbonyl", "터미널 브라우저", "터미널에서 웹", "CLI 브라우저",
  "터미널에서 사이트 열어", "headless browsing without GUI", "carbonyl-browser",
  "SSH에서 웹 열기", or any request to view web pages directly in the terminal
  without a GUI. Do NOT use for programmatic browser automation with element
  refs/snapshots (use agent-browser). Do NOT use for Playwright E2E test suites
  (use e2e-testing). Do NOT use for web content extraction to markdown (use
  defuddle or WebFetch). Do NOT use for MCP-based interactive browser sessions
  (use cursor-ide-browser MCP).
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "fathyb/carbonyl@0.0.3"
  category: "execution"
---

# Carbonyl Browser — Chromium in the Terminal

Browse real web pages directly in the terminal. Carbonyl forks Chromium to render
using Unicode characters and ANSI escape sequences — full HTML/CSS/JS support
including WebGL, WebGPU, WebAssembly, audio, and video.

## Prerequisites

```bash
which carbonyl || npm install -g carbonyl
```

Docker alternative (no install needed):

```bash
docker run --rm -ti fathyb/carbonyl https://example.com
```

## Core Usage

```bash
carbonyl [options] [url]
```

### Browse a URL

```bash
carbonyl https://example.com
carbonyl https://news.ycombinator.com
carbonyl https://github.com
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-f, --fps=<fps>` | Max frames per second | 60 |
| `-z, --zoom=<zoom>` | Zoom level in percent | 100 |
| `-b, --bitmap` | Render text as bitmaps (higher fidelity, slower) | off |
| `-d, --debug` | Enable debug logs | off |

### Examples

```bash
# Standard browsing
carbonyl https://example.com

# Low-bandwidth mode (reduce frame rate)
carbonyl -f 10 https://example.com

# Zoom out to fit more content
carbonyl -z 75 https://example.com

# High-fidelity bitmap rendering
carbonyl -b https://example.com

# Combine options
carbonyl -f 30 -z 80 https://example.com
```

## Docker Usage

For environments where npm install is not available or you want isolation:

```bash
# Basic browsing
docker run --rm -ti fathyb/carbonyl https://example.com

# With options
docker run --rm -ti fathyb/carbonyl --fps 30 --zoom 80 https://example.com

# Bitmap mode
docker run --rm -ti fathyb/carbonyl --bitmap https://github.com
```

## Keyboard Controls (Inside Carbonyl)

Carbonyl supports standard Chromium keyboard shortcuts:

| Shortcut | Action |
|----------|--------|
| `Tab` / `Shift+Tab` | Navigate between links/inputs |
| `Enter` | Activate focused link/button |
| `Arrow keys` | Scroll page |
| `Ctrl+L` | Focus address bar |
| `Ctrl+R` | Reload page |
| `Ctrl+Q` | Quit |
| `Backspace` | Go back |

## Use Cases

1. **SSH environments**: Browse web pages when connected to a remote server
   with no GUI
2. **Server consoles**: Check web dashboards from safe-mode or minimal consoles
3. **Lightweight containers**: View web interfaces inside Docker/K8s pods
4. **Quick web checks**: Rapidly verify a URL renders correctly without
   launching a full browser
5. **Low-bandwidth connections**: Terminal rendering uses far less bandwidth
   than full graphical browsing

## Performance

- Startup: < 1 second
- Rendering: up to 60 FPS
- Idle CPU: 0%
- Memory: significantly less than full Chromium

## Workflow: Agent-Assisted Terminal Browsing

When the user asks to view a web page in the terminal:

```
1. Verify carbonyl is installed  →  which carbonyl || npm install -g carbonyl
2. Open the URL                  →  carbonyl <url>
3. Optional: adjust settings     →  carbonyl -z 75 -f 30 <url>
```

**IMPORTANT**: Carbonyl is an interactive terminal application. It takes over the
terminal and renders the page visually. It is NOT a headless automation tool —
for programmatic browsing, use `agent-browser` or `playwright` instead.

## Limitations

- No Chrome DevTools Protocol (CDP) support — cannot be controlled
  programmatically by Playwright/Puppeteer
- No built-in screenshot export or content extraction API
- Fullscreen mode is limited by terminal dimensions
- Some Google services may trigger CAPTCHA
- No file download or bookmark support
- Last release: v0.0.3 (2023), with limited maintenance since 2024

## Troubleshooting

```bash
# Verify installation
which carbonyl && carbonyl --version

# If npm install fails, try Docker
docker run --rm -ti fathyb/carbonyl https://example.com

# If rendering looks broken, try bitmap mode
carbonyl -b https://example.com

# If too slow, reduce frame rate
carbonyl -f 15 https://example.com

# Debug mode for diagnosing issues
carbonyl -d https://example.com
```
