## Agent Browser

Automate headless browser tasks via the `agent-browser` CLI — navigate, interact, screenshot, extract, and diff web pages.

### Usage

```
/agent-browser <url> [action]
/agent-browser                    # interactive — describe what to automate
```

### Workflow

1. **Navigate** — `agent-browser open <url>`
2. **Snapshot** — `agent-browser snapshot -i` (get element refs `@e1`, `@e2`)
3. **Interact** — Use refs to click, fill, select, scroll
4. **Re-snapshot** — After navigation or DOM changes, get fresh refs

### Execution

Read and follow the `agent-browser` skill (`.cursor/skills/agent-browser/SKILL.md`) for the full workflow, command reference, patterns, and error handling.

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
/agent-browser https://shop.example.com/catalog — extract all product names as JSON
```

Compare two pages:
```
/agent-browser — diff the staging and production homepages visually
```
