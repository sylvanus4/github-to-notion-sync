# Paperclip Agent Adapter Configuration Examples

## claude_local

Local Claude Code agent. Spawns `claude` CLI in the specified directory.

```json
{
  "adapterType": "claude_local",
  "adapterConfig": {
    "cwd": "/path/to/project",
    "model": "claude-sonnet-4-20250514",
    "instructionsFilePath": "AGENTS.md"
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 300,
      "wakeOnDemand": true
    }
  }
}
```

## codex_local

Local OpenAI Codex agent.

```json
{
  "adapterType": "codex_local",
  "adapterConfig": {
    "cwd": "/path/to/project",
    "model": "o4-mini"
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 300,
      "wakeOnDemand": true
    }
  }
}
```

## cursor_local

Local Cursor agent.

```json
{
  "adapterType": "cursor_local",
  "adapterConfig": {
    "cwd": "/path/to/project",
    "model": "claude-sonnet-4-20250514"
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 600,
      "wakeOnDemand": true
    }
  }
}
```

## opencode_local

Local OpenCode agent.

```json
{
  "adapterType": "opencode_local",
  "adapterConfig": {
    "cwd": "/path/to/project",
    "model": "gpt-4"
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 300,
      "wakeOnDemand": true
    }
  }
}
```

## process

Generic process adapter. Spawns any command.

```json
{
  "adapterType": "process",
  "adapterConfig": {
    "command": "python",
    "args": ["agent.py", "--task", "{{taskId}}"],
    "cwd": "/path/to/agent",
    "env": {
      "OPENAI_API_KEY": "{{secret:openai_key}}"
    },
    "timeoutSec": 600
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 300,
      "wakeOnDemand": false
    }
  }
}
```

## http

External webhook agent. Paperclip POSTs to the URL on each heartbeat.

```json
{
  "adapterType": "http",
  "adapterConfig": {
    "url": "https://my-agent.example.com/heartbeat",
    "method": "POST",
    "headers": {
      "X-Agent-Auth": "{{secret:agent_auth_token}}"
    },
    "payloadTemplate": {
      "agentId": "{{agentId}}",
      "companyId": "{{companyId}}",
      "runId": "{{runId}}"
    }
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 600,
      "wakeOnDemand": true
    }
  }
}
```

## openclaw

OpenClaw SSE/webhook adapter.

```json
{
  "adapterType": "openclaw",
  "adapterConfig": {
    "callbackUrl": "http://localhost:8080/openclaw",
    "paperclipApiUrl": "http://localhost:3100"
  },
  "runtimeConfig": {
    "heartbeat": {
      "enabled": true,
      "intervalSec": 300,
      "wakeOnDemand": true
    }
  }
}
```

## Common runtimeConfig Fields

| Field | Type | Description |
|-------|------|-------------|
| `heartbeat.enabled` | boolean | Enable scheduled heartbeats |
| `heartbeat.intervalSec` | number | Seconds between heartbeats |
| `heartbeat.wakeOnDemand` | boolean | Wake on task assignment or @-mention |

## Environment Variables Injected into Agents

| Variable | Description |
|----------|-------------|
| `PAPERCLIP_AGENT_ID` | Agent's unique ID |
| `PAPERCLIP_COMPANY_ID` | Company scope |
| `PAPERCLIP_API_URL` | API base URL |
| `PAPERCLIP_API_KEY` | Short-lived run JWT |
| `PAPERCLIP_RUN_ID` | Current heartbeat run ID |
| `PAPERCLIP_TASK_ID` | Triggering task (if event-based) |
| `PAPERCLIP_WAKE_REASON` | Why this run was triggered |
| `PAPERCLIP_WAKE_COMMENT_ID` | Specific comment trigger |
| `PAPERCLIP_APPROVAL_ID` | Approval that triggered this run |
| `PAPERCLIP_APPROVAL_STATUS` | Approval status |
| `PAPERCLIP_LINKED_ISSUE_IDS` | Comma-separated linked issues |
