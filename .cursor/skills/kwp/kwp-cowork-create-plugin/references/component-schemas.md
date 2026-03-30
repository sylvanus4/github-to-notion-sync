# Component Schemas

Detailed format specifications for every plugin component type.

## Commands (`commands/*.md`)

Commands are slash-command-triggered instructions for Claude. Each command is a single Markdown file with YAML frontmatter.

### Schema

```markdown
---
name: command-name
description: One sentence describing what the command does (shown in the slash menu)
arguments:
  - name: arg_name
    description: What this argument is for
    required: true
    type: string
allowed_tools:
  - Read
  - Write
  - Shell
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Command Title

[Instructions for Claude to follow when this command is invoked.
Write these as directives, not documentation.]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | kebab-case identifier, used as `/name` in the chat |
| `description` | Yes | Shown in the slash command menu. Keep under 100 characters. |
| `arguments` | No | Positional arguments the command accepts |
| `allowed_tools` | No | Restrict which tools Claude can use. Omit to allow all. |

### Argument Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Argument identifier |
| `description` | Yes | Explanation of the argument |
| `required` | No | Whether the argument must be provided (default: false) |
| `type` | No | `string` (default), `number`, `boolean` |

### Body Guidelines

- Write instructions FOR Claude, not documentation for the user
- Use imperative style: "Read the file", "Generate a report", "Ask the user"
- Structure as numbered steps for multi-step workflows
- Reference skills by name when the command should load domain knowledge
- Include output format specifications

### Example

```markdown
---
name: daily-brief
description: Generate a prioritized daily briefing from connected tools
---

# Daily Briefing

Generate a prioritized daily briefing for the user.

## Steps

1. Check connected sources for today's context:
   - Calendar: meetings and deadlines
   - Chat: unread mentions and threads needing response
   - Email: flagged or urgent messages
   - Tasks: items due today or overdue

2. Synthesize into a prioritized briefing using this format:

   ## Today's Briefing — [Date]

   ### Must Do Today
   - [Highest priority items with deadlines]

   ### Meetings
   - [Time] [Meeting] — [Key context or prep needed]

   ### Follow Up
   - [Items needing response or action]

   ### FYI
   - [Informational items, no action needed]

3. Ask: "Want me to prep for any of these meetings or draft any responses?"
```

---

## Skills (`skills/*/SKILL.md`)

Skills are domain knowledge packs loaded on demand. Each skill lives in its own subdirectory with a `SKILL.md` file and optional `references/` for detailed content.

### Schema

```markdown
---
name: skill-name
description: >
  Third-person description with specific trigger phrases.
  "Use when the user asks to [trigger 1], [trigger 2], or [trigger 3]."
  "Do NOT use for [exclusion]."
metadata:
  author: author-name
  version: 1.0.0
---

# Skill Title

[Concise overview of what this skill provides — 1-2 sentences]

## [Section 1: Core Knowledge]

[Domain expertise, frameworks, methodologies]

## [Section 2: Workflow / Process]

[Step-by-step procedures if applicable]

## Reference Files

- **`references/file-name.md`** — [What it contains]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | kebab-case identifier |
| `description` | Yes | Third-person trigger description with specific phrases and exclusions |
| `metadata.author` | No | Author identifier |
| `metadata.version` | No | Semver version |

### Body Guidelines

- Keep the main SKILL.md body under 3,000 words
- Put detailed reference material in `references/*.md`
- Use progressive disclosure: essential knowledge in SKILL.md, deep dives in references
- Write in imperative style for instructions, declarative for knowledge
- Include "We Are / We Are Not" or scope boundaries where useful

### Directory Structure

```
skills/
  my-skill/
    SKILL.md              # Required: main skill file
    references/           # Optional: detailed reference content
      detailed-guide.md
      examples.md
      templates.md
```

---

## MCP Servers (`.mcp.json`)

MCP (Model Context Protocol) server configurations enable Claude to connect to external tools and services.

### Schema

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@package/server"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### Server Types

| Type | Use Case | Fields |
|------|----------|--------|
| `stdio` | Local process communicating via stdin/stdout | `command`, `args`, `env` |
| `sse` | Remote server with Server-Sent Events | `url`, `headers` |
| `http` | REST API endpoint | `url`, `headers` |

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `stdio`, `sse`, or `http` |
| `command` | string | Executable to run (stdio only) |
| `args` | string[] | Command arguments (stdio only) |
| `env` | object | Environment variables. Use `${VAR}` for user-provided values. |
| `url` | string | Server URL (sse/http only) |
| `headers` | object | HTTP headers (sse/http only) |

### Path References

Always use `${CLAUDE_PLUGIN_ROOT}` for paths within the plugin:

```json
{
  "mcpServers": {
    "local-server": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/my-server.js"]
    }
  }
}
```

---

## Agents (`agents/*.md`)

Agents are autonomous sub-agents that can be triggered by other components or by Claude's judgment. Less commonly used in Cowork plugins.

### Schema

```markdown
---
name: agent-name
description: >
  When to trigger this agent, with example blocks.
  <example>
  Context: [situation description]
  user: "[user message that should trigger this agent]"
  </example>
model: default
tools:
  - Read
  - Write
  - Shell
---

# Agent System Prompt

[Instructions the agent follows when activated.
This is the agent's system prompt.]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | kebab-case identifier |
| `description` | Yes | Trigger conditions with `<example>` blocks |
| `model` | No | Model to use (`default`, `fast`, etc.) |
| `tools` | No | Tools the agent can use |

---

## Hooks (`hooks/hooks.json`)

Hooks run automatically on specific events. Used for enforcing policies, adding context, or validating operations. Rarely needed in Cowork plugins.

### Schema

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hook": {
          "type": "prompt",
          "prompt": "Check if the file being written follows the project's naming conventions."
        }
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Shell",
        "hook": {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
        }
      }
    ]
  }
}
```

### Event Types

| Event | When It Fires |
|-------|---------------|
| `PreToolUse` | Before Claude executes a tool |
| `PostToolUse` | After a tool execution completes |
| `SessionStart` | When a new session begins |
| `Stop` | When Claude is about to end its turn |

### Hook Types

| Type | Description |
|------|-------------|
| `prompt` | LLM-evaluated: Claude reads the prompt and decides what to do |
| `command` | Deterministic: runs a script/command, uses exit code for pass/fail |

### Matcher

The `matcher` field filters which tool invocations trigger the hook:
- Exact tool name: `"Write"`, `"Shell"`, `"Read"`
- Glob pattern: `"*"` (all tools)

---

## CONNECTORS.md (Optional)

Only needed when the plugin uses `~~category` placeholders for tool-agnostic references. See the `~~` placeholders section in the main SKILL.md.

```markdown
# Connectors

## Connectors for this plugin

| Category | Placeholder | Options |
|----------|-------------|---------|
| Chat | `~~chat` | Slack, Microsoft Teams, Discord |
| Project tracker | `~~project tracker` | Linear, Asana, Jira |
| CRM | `~~CRM` | Salesforce, HubSpot, Pipedrive |
```
