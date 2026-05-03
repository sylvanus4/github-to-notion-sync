---
name: hookify
description: >-
  Interactive Cursor hook builder — guides through selecting hook event types,
  defining conditions, writing scripts, registering in hooks.json, and
  testing.
---

# Hookify — Cursor Hook Builder

Interactive wizard for creating Cursor hooks. Guides through the full lifecycle: select event type, define trigger conditions, write the hook script, register in `hooks.json`, and validate with a dry-run.

## Trigger Phrases

- "create hook", "add hook", "hookify", "hook builder", "new cursor hook"
- "훅 생성", "커서 훅 만들기", "훅 빌더", "새 훅 추가"
- `/hookify` command

## Do NOT Use For

- Marketing hook phrases for content (use `hook-generator` skill / `/hooks` command)
- Git hooks (pre-commit, pre-push) configuration (edit `.pre-commit-config.yaml` directly)
- GitHub Actions workflows (use `pipeline-builder` or `sre-devops-expert`)
- MCP server setup (use `anthropic-mcp-builder`)

## Supported Hook Event Types

| Event | File Key | When It Fires | Use Cases |
|-------|----------|---------------|-----------|
| After File Edit | `afterFileEdit` | After agent edits a file | Auto-format, lint check, import sort |
| Before Shell Execution | `beforeShellExecution` | Before a shell command runs | Safety gates, command rewriting, tmux suggestions |
| Before Prompt Submit | `beforeSubmitPrompt` | Before user prompt is sent | Context injection, reminder appending |
| Before Tab File Read | `beforeTabFileRead` | Before reading a file for tab context | File filtering, content preprocessing |
| Session Start | `sessionStart` | When a new agent session begins | Context loading, environment checks |
| Session End | `sessionEnd` | When an agent session ends | Cleanup, summary generation, memory sync |

## Workflow

### Step 1: Discover Intent
Ask the user:
1. What should happen? (the action)
2. When should it happen? (the event type from the table above)
3. Under what conditions? (filtering criteria)

### Step 2: Read Current Hooks
```
Read .cursor/hooks/hooks.json
```
- List existing hooks to avoid naming conflicts
- Identify the existing script patterns and utilities (e.g., `lib/utils.js`, `lib/hook-flags.js`)

### Step 3: Design the Hook

Determine:
- **Event type** from the supported list
- **Hook ID** for the `hook-flags` system (format: `{event-prefix}:{category}:{name}`)
- **Security level** (`standard` or `strict`)
- **Script filename** (kebab-case, descriptive)

### Step 4: Write the Script

Create a new JavaScript file in `.cursor/hooks/scripts/` following the existing patterns:

```javascript
#!/usr/bin/env node
'use strict';

const { readStdin } = require('./lib/utils');
const { isHookEnabled } = require('./lib/hook-flags');

readStdin().then(raw => {
  try {
    const input = JSON.parse(raw || '{}');

    if (isHookEnabled('{hook-id}', ['{security-level}'])) {
      // Hook logic here
    }
  } catch {
    // noop — never break the editor
  }

  process.stdout.write(raw);
}).catch(() => process.exit(0));
```

Key rules:
- Always pass through `raw` via `process.stdout.write(raw)` at the end
- Never block the editor — catch all errors
- Use `console.error()` for warnings/tips (stderr, visible but non-blocking)
- Use `process.exit(2)` ONLY for hard blocks (dangerous commands)
- Use the `isHookEnabled` flag system for conditional activation

### Step 5: Register in hooks.json

Add the new hook entry to `.cursor/hooks/hooks.json`:

```json
{
  "event": "{eventType}",
  "script": "scripts/{script-name}.js",
  "description": "{one-line description}"
}
```

### Step 6: Validate

- Verify the script is syntactically valid: `node -c .cursor/hooks/scripts/{script-name}.js`
- Check that `hooks.json` is valid JSON
- Confirm no duplicate event handlers conflict

### Step 7: Report

```
Hook Created Successfully
━━━━━━━━━━━━━━━━━━━━━━━━
Event: beforeShellExecution
Script: .cursor/hooks/scripts/{name}.js
Hook ID: pre:bash:{name}
Level: standard

Test: Run a matching command to verify the hook fires.
```

## Hook Script Patterns

### Pattern A: Warning (Advisory)
```javascript
console.error('[Hook] Tip: Consider doing X instead of Y');
```

### Pattern B: Block (Hard Stop)
```javascript
console.error('[Hook] BLOCKED: Reason');
process.exit(2);
```

### Pattern C: Transform (Modify Input)
```javascript
const modified = { ...input, command: input.command.replace('foo', 'bar') };
process.stdout.write(JSON.stringify(modified));
return; // skip the final raw write
```

### Pattern D: Log (Silent Record)
```javascript
const fs = require('fs');
fs.appendFileSync('/tmp/cursor-hook-log.txt', `${new Date().toISOString()} ${cmd}\n`);
```

## Examples

### Example 1: Secret Detection Hook
```
User: "Create a hook that warns when I'm about to commit files containing API keys"
Agent: Creates afterFileEdit hook → Scans for patterns like API_KEY=, SECRET= → Warns via stderr
```

### Example 2: Auto-Format on Save
```
User: "Add a hook to run prettier after editing .tsx files"
Agent: Creates afterFileEdit hook → Checks file extension → Runs prettier on .tsx files
```

### Example 3: Context Injection
```
User: "I want to inject project context before every prompt"
Agent: Creates beforeSubmitPrompt hook → Reads CODEMAP.md → Appends to prompt context
```

## Error Handling

- If `.cursor/hooks/hooks.json` doesn't exist, create it with an empty array
- If `.cursor/hooks/scripts/lib/` utilities are missing, create minimal stubs
- If the script has a syntax error, report and fix before registering
- If a hook with the same event + name exists, ask whether to replace or rename
