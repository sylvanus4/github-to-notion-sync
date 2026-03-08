## Agent Browser

Automate headless browser tasks via the `agent-browser` CLI — navigate, interact, screenshot, extract, diff, record, profile, and test web pages.

### Usage

```
/agent-browser <url> [action]              # Default: open URL and perform described action
/agent-browser --screenshot <url>          # Take screenshot (full page, annotated)
/agent-browser --scrape <url> [selector]   # Extract data from page (text, JSON, structured)
/agent-browser --diff <url1> <url2>        # Visual/snapshot diff between two URLs
/agent-browser --form <url>                # Interactive form discovery and filling
/agent-browser --auth <url>                # Login with auth vault or state persistence
/agent-browser --monitor <url>             # Watch for page changes over time
/agent-browser --test <url>                # Quick smoke test (load, screenshot, errors)
/agent-browser --mobile <url>              # iOS simulator testing (requires macOS + Xcode)
/agent-browser --record <url>              # Record browser session as video
/agent-browser --profile <url>             # Chrome DevTools performance profiling
/agent-browser --headed <url>              # Visual debugging with browser window
/agent-browser                             # Interactive — describe what to automate
```

### Skill Reference

Read and follow the `agent-browser` skill (`.cursor/skills/agent-browser/SKILL.md`) for the full workflow, command reference, patterns, and error handling.

### Mode Details

#### Default Mode (`/agent-browser <url> [action]`)
Open the URL and perform the described action using the snapshot-ref workflow:
1. `agent-browser open <url>` + `wait --load networkidle`
2. `agent-browser snapshot -i` to get element refs
3. Perform the described action using refs
4. Re-snapshot after page changes

#### Screenshot (`--screenshot`)
Take a full-page annotated screenshot and report interactive elements.
```
/agent-browser --screenshot https://example.com
```

#### Scrape (`--scrape`)
Extract structured data from the page — text content, product listings, tables, links.
Optionally scope to a CSS selector.
```
/agent-browser --scrape https://shop.example.com/catalog .product-card
/agent-browser --scrape https://example.com — extract all headings as JSON
```

#### Diff (`--diff`)
Compare two URLs visually and structurally. Reports snapshot differences and optionally
produces a visual diff image with changed pixels highlighted.
```
/agent-browser --diff https://staging.app.com https://prod.app.com
```

#### Form (`--form`)
Navigate to the form page, snapshot to discover form fields, and fill them interactively.
```
/agent-browser --form https://example.com/signup
```

#### Auth (`--auth`)
Login to a site using auth vault (recommended) or manual credential entry with state persistence.
```
/agent-browser --auth https://github.com/login
```

#### Monitor (`--monitor`)
Take periodic snapshots of a page and report changes. Useful for detecting content updates.
```
/agent-browser --monitor https://status.example.com — check every 30 seconds for 5 minutes
```

#### Test (`--test`)
Quick smoke test: load page, check for console errors, take screenshot, report status.
```
/agent-browser --test https://my-app.com/dashboard
```

#### Mobile (`--mobile`)
Test on iOS Simulator with Mobile Safari. Requires macOS, Xcode, and Appium.
```
/agent-browser --mobile https://example.com — test on iPhone 16 Pro
```

#### Record (`--record`)
Record the browser session as a WebM video for debugging or documentation.
```
/agent-browser --record https://example.com — navigate through the signup flow
```

#### Profile (`--profile`)
Run Chrome DevTools profiling during page interaction. Saves trace JSON for analysis.
```
/agent-browser --profile https://my-app.com — profile the dashboard load time
```

#### Headed (`--headed`)
Open a visible browser window for visual debugging. Useful with `highlight` commands.
```
/agent-browser --headed https://example.com — debug the login form
```

### Examples

Navigate and screenshot:
```
/agent-browser https://example.com — take a full-page screenshot
```

Fill a form and submit:
```
/agent-browser https://my-app.com/login — login with test credentials and screenshot the dashboard
```

Extract data:
```
/agent-browser --scrape https://shop.example.com/catalog — extract all product names as JSON
```

Compare environments:
```
/agent-browser --diff https://staging.app.com https://prod.app.com
```

Mobile testing:
```
/agent-browser --mobile https://example.com — test responsive layout on iPhone 16 Pro
```

Performance profiling:
```
/agent-browser --profile https://my-app.com — measure dashboard load time
```

Record a demo:
```
/agent-browser --record https://my-app.com — walk through the onboarding flow
```

Quick smoke test:
```
/agent-browser --test https://my-app.com/dashboard
```
