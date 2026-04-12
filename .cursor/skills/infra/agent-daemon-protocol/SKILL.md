---
name: agent-daemon-protocol
description: "Design the daemon↔server communication protocol for agent platforms: registration, heartbeat, runtime discovery, task claiming, and session resumption. Use when designing daemon↔server APIs, implementing daemon registration, building heartbeat mechanisms, designing task claiming protocols, implementing session resumption, or reviewing daemon communication code. Do NOT use for agent sandbox isolation (use agent-sandbox-platform PRD), agent CRUD without daemon context (use cursor-self-hosted-agents PRD), LLM API integration (use anthropic-claude-api), or general WebSocket patterns without agent context. Korean triggers: '데몬 프로토콜', '에이전트 데몬', '하트비트 설계', '런타임 등록', '태스크 클레이밍'."
tags: [agent, daemon, protocol, websocket, heartbeat, infrastructure]
version: "1.0.0"
metadata:
  author: thakicloud
  category: infrastructure
---

# Agent Daemon Protocol

Guide the design and implementation of the communication protocol between local
agent daemons and the platform server. Covers runtime registration, health
monitoring, task distribution, and session continuity.

## Core Protocol Patterns

### 1. Daemon Registration

The daemon is a local process that manages one or more AI agent CLI runtimes
(e.g., Claude Code, Codex, OpenCode). On startup, the daemon registers with the
server, declaring its identity and available runtimes.

```
POST /api/daemon/register

Request:
{
  "workspace_id": "uuid",
  "daemon_id": "unique-device-id",
  "device_name": "macbook-pro-office",
  "cli_version": "0.5.2",
  "runtimes": [
    {
      "name": "claude-code",
      "type": "claude",
      "version": "1.0.32",
      "status": "online"
    }
  ]
}

Response: 200 OK
{
  "status": "registered",
  "daemon_token": "jwt-or-opaque-token"
}
```

**Design constraints:**
- Daemon ID must be deterministic per device (e.g., machine-id hash)
- Registration is idempotent — re-registering updates metadata
- Server stores runtime capabilities for task routing
- Token returned is used for all subsequent daemon API calls

### 2. Heartbeat Protocol

Daemons send periodic heartbeats to maintain their online status. Missed
heartbeats trigger runtime status reconciliation.

```
POST /api/daemon/heartbeat

Request:
{
  "runtimes": [
    { "name": "claude-code", "type": "claude", "status": "online" }
  ]
}

Response: 200 OK
{
  "status": "ok"
}
```

**Design constraints:**
- Heartbeat interval: 30s (configurable)
- Server marks runtimes offline after 3 missed heartbeats (90s)
- Heartbeat carries current runtime status — server reconciles state
- Lightweight payload — no task data in heartbeat path

### 3. Deregistration

Clean shutdown sends explicit deregistration. Server marks all runtimes offline.

```
POST /api/daemon/deregister

Response: 200 OK
```

### 4. Task Claiming (Pull Model)

Tasks are assigned via a pull model — the daemon requests the next available task
for a specific runtime type. Atomic claiming prevents double-assignment.

```
POST /api/daemon/tasks/claim

Request:
{
  "runtime_type": "claude"
}

Response: 200 OK
{
  "id": "task-uuid",
  "type": "issue",
  "title": "Fix login timeout",
  "description": "Users report 504 on /api/auth/login...",
  "agent": {
    "name": "backend-fixer",
    "instructions": "You are a Go backend specialist...",
    "skills": [
      { "name": "error-handling", "content": "..." }
    ]
  },
  "repos": [
    {
      "url": "https://github.com/org/repo.git",
      "branch": "main",
      "default_branch": "main"
    }
  ],
  "prior_session_id": "session-abc-123",
  "prior_work_dir": "/tmp/multica/workspaces/repo-xyz"
}
```

**Design constraints:**
- Claiming is atomic — database-level row lock or `FOR UPDATE SKIP LOCKED`
- Only tasks matching the daemon's runtime type are returned
- Response includes everything the daemon needs to set up the execution
  environment: agent instructions, skills, repo URLs, and prior session context
- `prior_session_id` + `prior_work_dir` enable session resumption for
  continuation tasks on the same issue
- Return 204 No Content when no tasks are available
- Claimed task transitions from `queued` → `running`

### 5. Session Resumption

When a task relates to an issue that had a prior completed task, the server
includes the previous session ID and working directory. The daemon uses these
to resume the agent CLI with existing context.

```
Resumption flow:
1. Server looks up prior completed task for same issue
2. If found, includes prior_session_id and prior_work_dir in claim response
3. Daemon passes --resume <session_id> to agent CLI
4. Agent continues from where it left off with full conversation history
```

**Design constraints:**
- Only resume from the most recent completed (not failed) task
- Work directory must still exist on the daemon's filesystem
- Daemon should fall back to fresh session if resume fails
- Session ID format is agent-CLI-specific (Claude Code uses UUIDs)

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│  Platform Server (Go)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ REST API │  │WebSocket │  │ Task Queue   │  │
│  │ (daemon) │  │ (events) │  │ (PostgreSQL) │  │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       │              │               │          │
└───────┼──────────────┼───────────────┼──────────┘
        │              │               │
   ─────┼──────────────┼───────────────┼────── Network
        │              │               │
┌───────┼──────────────┼───────────────┼──────────┐
│       │              │               │          │
│  ┌────▼─────┐  ┌─────▼────┐  ┌──────▼───────┐  │
│  │ Register │  │ Subscribe│  │ Claim Task   │  │
│  │ Heartbeat│  │ Events   │  │ Report Status│  │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       │              │               │          │
│  ┌────▼──────────────▼───────────────▼───────┐  │
│  │            Agent Daemon                    │  │
│  │  ┌────────────┐  ┌────────────┐           │  │
│  │  │ Claude CLI │  │ Codex CLI  │   ...     │  │
│  │  └────────────┘  └────────────┘           │  │
│  └───────────────────────────────────────────┘  │
│  Local Machine                                  │
└─────────────────────────────────────────────────┘
```

## Database Schema Reference

```sql
CREATE TABLE daemon_connection (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspace(id),
    daemon_id TEXT NOT NULL,
    device_name TEXT NOT NULL DEFAULT '',
    cli_version TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'online',
    connected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_heartbeat_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(workspace_id, daemon_id)
);

CREATE TABLE agent_runtime (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    daemon_connection_id UUID NOT NULL REFERENCES daemon_connection(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type TEXT NOT NULL,         -- 'claude', 'codex', 'opencode'
    version TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'offline',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## Security Considerations

- Daemon tokens must be short-lived and workspace-scoped
- Heartbeat endpoint must validate the daemon token
- Task claim must verify the daemon belongs to the task's workspace
- Skill content in claim response must be sanitized (no path traversal)
- Consider mTLS for daemon↔server in production deployments

## Integration with ThakiCloud Agent Cloud

This pattern maps to the following Agent Cloud roadmap items:
- **Phase 0**: API Server (Go/Fiber) — daemon endpoints
- **Phase 1**: Sandbox Runtime — daemon manages sandbox lifecycle
- **Phase 2**: Agent Identity Registry — daemon registration feeds identity
- **Cursor Self-Hosted Agents**: Pod-based daemons in K8s

Adapt the protocol for K8s environments:
- Daemon runs as a sidecar or init container in agent pods
- Registration uses K8s service account tokens instead of workspace tokens
- Heartbeat aligns with K8s liveness/readiness probes
- Task claiming uses NATS JetStream instead of HTTP polling for lower latency

## Examples

### Daemon startup sequence

```
1. Daemon starts → detects local runtimes (claude-code v1.0.32)
2. POST /api/daemon/register → receives daemon_token
3. Starts heartbeat goroutine (30s interval)
4. Enters task claiming loop: POST /api/daemon/tasks/claim
5. On claim: spawns agent CLI subprocess with instructions + skills
6. On completion: reports result, resumes claiming loop
```

### Session resumption scenario

```
Task A: "Fix login timeout" → completed, session_id=abc, work_dir=/tmp/ws/repo
Task B: "Add retry logic to the same fix" → claim response includes prior_session_id=abc
Daemon: claude --resume abc --work-dir /tmp/ws/repo
Agent resumes with full conversation history from Task A
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| 401 on register | Invalid workspace credentials | Re-authenticate, retry |
| 409 on register | Daemon ID already registered | Treat as update (idempotent) |
| 204 on claim | No tasks available | Back off exponentially (5s → 30s) |
| 409 on claim | Task already claimed by another daemon | Retry claim for next task |
| Heartbeat timeout (90s) | Network partition | Server marks offline; daemon re-registers on reconnect |
| Resume fails | Work directory deleted | Fall back to fresh session |

## Gotchas

- Daemon ID must be deterministic per machine — random UUIDs cause ghost registrations after restarts
- Heartbeat MUST NOT carry task data — mixing control plane and data plane causes cascading failures under load
- Task claim MUST use `FOR UPDATE SKIP LOCKED` — plain `FOR UPDATE` causes convoy effect with multiple daemons
- Session resumption depends on the work directory persisting on disk — ephemeral containers need volume mounts
- Re-registration after network recovery should NOT create a new daemon_connection row — use UPSERT on (workspace_id, daemon_id)

## Checklist

- [ ] Define daemon registration endpoint with runtime discovery
- [ ] Implement heartbeat with configurable interval and offline detection
- [ ] Build atomic task claiming with row-level locking
- [ ] Include agent instructions + skills in claim response
- [ ] Implement session resumption via prior_session_id/prior_work_dir
- [ ] Add daemon token authentication middleware
- [ ] Design WebSocket event subscription for real-time task updates
- [ ] Write integration tests for concurrent task claiming
- [ ] Document protocol versioning strategy for backward compatibility
