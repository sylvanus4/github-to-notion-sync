---
name: obsidian-dev
description: >-
  Access Obsidian developer tools via the CLI — open DevTools, evaluate
  JavaScript in the app console, take screenshots, inspect CSS/DOM, read
  console logs, and connect via Chrome DevTools Protocol (CDP). Use when the
  user asks to open developer tools, run JavaScript in Obsidian, take a
  screenshot, inspect CSS, debug plugins, read console output, or use CDP with
  Obsidian. Do NOT use for file CRUD (use obsidian-files), daily notes (use
  obsidian-daily), search (use obsidian-search), note metadata (use
  obsidian-notes), or plugin management (use obsidian-admin). Korean triggers:
  "옵시디언 개발", "개발자 도구", "스크린샷", "자바스크립트 실행", "옵시디언 디버그", "CSS 검사", "콘솔 로그",
  "CDP 연결".
---

# Obsidian CLI — Developer Tools

> **Requires:** Obsidian app running, CLI in PATH. See `obsidian-setup`.

## Prerequisites

- Obsidian CLI configured (`obsidian-setup`)
- Target vault open in Obsidian
- Some commands require developer mode or plugin development context

## Quick Commands

### DevTools

```bash
obsidian dev:open                              # open Chromium DevTools
obsidian dev:close                             # close DevTools
```

### JavaScript Evaluation

```bash
# Run JS in the Obsidian app context
obsidian dev:eval code="app.vault.getFiles().length"
obsidian dev:eval code="app.workspace.getActiveFile()?.path"
obsidian dev:eval code="app.plugins.enabledPlugins"

# Multi-line (use quotes)
obsidian dev:eval code="
  const files = app.vault.getMarkdownFiles();
  files.map(f => f.path).join('\n');
"
```

### Screenshots

```bash
obsidian dev:screenshot path="screenshot.png"           # full window
obsidian dev:screenshot path="screen.png" fullPage=true # full page
```

### Console

```bash
obsidian dev:console                           # read recent console output
obsidian dev:console:clear                     # clear console
```

### CSS Inspection

```bash
obsidian dev:css                               # dump current CSS variables
obsidian dev:css selector=".workspace-leaf"    # inspect specific element
```

### DOM Inspection

```bash
obsidian dev:dom selector=".workspace"         # inspect DOM structure
obsidian dev:dom selector=".nav-folder"        # inspect file explorer
```

### Chrome DevTools Protocol

```bash
obsidian dev:cdp                               # get CDP endpoint URL
obsidian dev:cdp:send method="Page.reload"     # send CDP command
```

## Discovering Commands

```bash
obsidian help dev              # developer tool commands
obsidian help dev:eval         # JavaScript eval details
obsidian help dev:screenshot   # screenshot options
obsidian help dev:cdp          # CDP protocol details
```

## Common Patterns

### Plugin development workflow

```bash
obsidian plugin:reload id="my-plugin"          # reload after code change
obsidian dev:open                              # open DevTools for debugging
obsidian dev:console                           # check for errors
```

### Capture current state

```bash
obsidian dev:screenshot path="before.png"
# ... make changes ...
obsidian dev:screenshot path="after.png"
```

### Query vault programmatically

```bash
# Count notes by folder
obsidian dev:eval code="
  const files = app.vault.getMarkdownFiles();
  const folders = {};
  files.forEach(f => {
    const dir = f.parent?.path || '/';
    folders[dir] = (folders[dir] || 0) + 1;
  });
  JSON.stringify(folders, null, 2);
"

# List enabled plugins
obsidian dev:eval code="Array.from(app.plugins.enabledPlugins).join('\n')"
```

### Extract theme CSS variables

```bash
obsidian dev:css | grep "color"    # find color tokens
```

## Safety

- `dev:eval` runs arbitrary JavaScript in the app — review code before execution
- Avoid destructive vault operations via eval; prefer dedicated CLI commands
- CDP connections can interfere with the app — disconnect when done
- Screenshots may capture sensitive content — handle output files carefully

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `DevTools already open` | Duplicate open call | Close first with `dev:close` |
| `Eval error` | JavaScript syntax or runtime error | Check code and Obsidian API docs |
| `Screenshot failed` | Invalid path or permissions | Use absolute path or writable directory |
| `CDP connection refused` | DevTools not enabled | Run `dev:open` first |
