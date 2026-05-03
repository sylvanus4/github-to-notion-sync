---
name: agent-task-lifecycle
description: >-
  Design the full agent task lifecycle: queue management, progress reporting,
  token accounting, live message streaming with content redaction, and
  completion/failure handling. Use when designing task queue and distribution
  for agent execution platforms, building progress reporting and live output
  streaming, implementing per-task token usage tracking (Agent FinOps),
  designing content redaction for agent output persistence, building task
  completion/failure handling, or reviewing agent task execution code. Do NOT
  use for daemon↔server communication protocol (use agent-daemon-protocol),
  agent sandbox isolation (use agent-sandbox-platform PRD), LLM cost
  optimization at prompt level (use ecc-token-strategy rule), or general CI/CD
  pipeline design (use sre-devops-expert). Korean triggers: '태스크 라이프사이클',
  '에이전트 태스크', '토큰 추적', '실시간 메시지', '태스크 완료', '에이전트 FinOps'.
---

# Agent Task Lifecycle

Guide the design and implementation of the complete task execution lifecycle
for agent platforms — from task queuing through execution to completion, with
token accounting, live output streaming, and security redaction.

## Task State Machine

```
                    ┌──────────┐
         ┌─────────│ cancelled │
         │         └──────────┘
         │ (user cancels)
         │
    ┌────┴───┐     ┌─────────┐     ┌──────────┐
    │ queued ├────►│ running ├────►│completed │
    └────────┘     └────┬────┘     └──────────┘
      claim()           │
                        │         ┌──────────┐
                        └────────►│  failed  │
                                  └──────────┘
```

**State transitions:**
- `queued` → `running`: Atomic claim by daemon (see agent-daemon-protocol)
- `running` → `completed`: Daemon reports success with output + PR URL
- `running` → `failed`: Daemon reports failure with error message
- `queued`/`running` → `cancelled`: User or system cancellation
- No backward transitions — failed tasks create new queue entries if retried

## 1. Task Progress Reporting

During execution, the daemon periodically reports progress with step counts and
summaries for UI display.

```
POST /api/daemon/tasks/{taskId}/progress

Request:
{
  "summary": "Running test suite after applying fix",
  "step": 3,
  "total": 5
}

Response: 200 OK
{ "status": "ok" }
```

**Design constraints:**
- Progress updates are fire-and-forget — failures don't block execution
- Server broadcasts progress via WebSocket to connected clients
- `step/total` enables percentage display in UI
- `summary` is human-readable and displayed as-is
- Rate limit: max 1 progress update per 5 seconds per task

## 2. Task Completion

On successful completion, the daemon reports the result including any PR URL,
output summary, and session metadata for future resumption.

```
POST /api/daemon/tasks/{taskId}/complete

Request:
{
  "pr_url": "https://github.com/org/repo/pull/42",
  "output": "Fixed the login timeout by increasing connection pool size...",
  "session_id": "claude-session-abc-123",
  "work_dir": "/tmp/agent/workspaces/repo-xyz"
}

Response: 200 OK
{ "id": "...", "status": "completed", ... }
```

**Design constraints:**
- `session_id` + `work_dir` are stored for future task resumption
- `pr_url` is optional — not all tasks produce PRs
- `output` is the agent's final summary
- Server publishes completion event via WebSocket + NATS
- Completion triggers any downstream automations (e.g., PR review assignment)

## 3. Task Failure

```
POST /api/daemon/tasks/{taskId}/fail

Request:
{
  "error": "Build failed: missing dependency github.com/foo/bar v2.0"
}

Response: 200 OK
{ "id": "...", "status": "failed", ... }
```

## 4. Mid-execution Cancellation Check

The daemon periodically polls task status to detect user-initiated cancellations.

```
GET /api/daemon/tasks/{taskId}/status

Response: 200 OK
{ "status": "running" }     // continue
{ "status": "cancelled" }   // stop execution
```

**Design constraints:**
- Poll interval: 10s (configurable)
- On cancellation, daemon sends SIGTERM to agent CLI process
- If agent doesn't exit within 30s, send SIGKILL
- Alternative: use WebSocket push for instant cancellation (preferred)

## 5. Per-Task Token Usage Tracking

Track token consumption at task granularity for FinOps reporting and cost
attribution. Called independently of complete/fail so usage is captured even
when tasks fail.

```
POST /api/daemon/tasks/{taskId}/usage

Request:
{
  "usage": [
    {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "input_tokens": 15420,
      "output_tokens": 3200,
      "cache_read_tokens": 8500,
      "cache_write_tokens": 2100
    },
    {
      "provider": "anthropic",
      "model": "claude-haiku-3.5",
      "input_tokens": 2000,
      "output_tokens": 500,
      "cache_read_tokens": 0,
      "cache_write_tokens": 0
    }
  ]
}

Response: 200 OK
```

**Design constraints:**
- Usage is an array — a single task may use multiple models
- UPSERT semantics — repeated reports for the same model accumulate
- `cache_read_tokens` and `cache_write_tokens` track prompt caching efficiency
- Provider field distinguishes Anthropic / OpenAI / custom endpoints
- Usage data feeds into:
  - Per-workspace cost dashboards
  - Per-agent cost attribution
  - Model selection optimization (ROI per model)
  - Budget alerting and rate limiting

### Database Schema

```sql
CREATE TABLE task_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES agent_task_queue(id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    input_tokens BIGINT NOT NULL DEFAULT 0,
    output_tokens BIGINT NOT NULL DEFAULT 0,
    cache_read_tokens BIGINT NOT NULL DEFAULT 0,
    cache_write_tokens BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(task_id, provider, model)
);
```

### Cost Calculation

```
effective_input = input_tokens - cache_read_tokens
billable_input_cost = effective_input * input_price + cache_read_tokens * cache_price
total_cost = billable_input_cost + output_tokens * output_price
savings_from_caching = cache_read_tokens * (input_price - cache_price)
```

## 6. Live Task Message Streaming

During execution, the daemon batches agent output messages and sends them to the
server for persistence and real-time broadcasting.

```
POST /api/daemon/tasks/{taskId}/messages

Request:
{
  "messages": [
    {
      "seq": 1,
      "type": "assistant",
      "content": "I'll start by examining the error logs..."
    },
    {
      "seq": 2,
      "type": "tool_use",
      "tool": "Read",
      "input": { "path": "/var/log/app.log" }
    },
    {
      "seq": 3,
      "type": "tool_result",
      "tool": "Read",
      "output": "2024-01-15 Error: Connection refused..."
    }
  ]
}

Response: 200 OK
```

**Design constraints:**
- Batched for efficiency — daemon buffers ~5 seconds of messages
- `seq` ensures correct ordering even with out-of-order delivery
- Message types: `assistant`, `tool_use`, `tool_result`, `error`, `system`
- Server persists messages in `task_message` table
- Server broadcasts via WebSocket to connected clients watching this task

### Content Redaction

**All message content MUST be redacted before persistence or broadcast.**

Redaction targets:
- API keys and tokens (`sk-...`, `Bearer ...`, `ghp_...`, `AKIA...`)
- Passwords and secrets in environment variables
- Personal identifiable information (emails, phone numbers)
- Database connection strings with credentials
- Private SSH keys and certificates

```
Redaction pipeline:
1. Daemon captures raw agent output
2. Client-side pre-redaction (fast regex patterns)
3. Server receives batch → applies server-side redaction
4. Redacted content persisted to database
5. Redacted content broadcast via WebSocket
```

```go
// Redaction applies to all string fields in task messages
msg.Content = redact.Text(msg.Content)
msg.Output  = redact.Text(msg.Output)
msg.Input   = redact.InputMap(msg.Input)
```

### Database Schema

```sql
CREATE TABLE task_message (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES agent_task_queue(id) ON DELETE CASCADE,
    seq INT NOT NULL,
    type TEXT NOT NULL,
    tool TEXT,
    content TEXT,
    input JSONB,
    output TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_task_message_task_seq ON task_message(task_id, seq);
```

## Integration with ThakiCloud Agent Cloud

This pattern maps to the following Agent Cloud roadmap items:
- **Phase 0**: Core task execution flow for API Server
- **Phase 1**: Token tracking feeds Telemetry Pipeline
- **Phase 2**: Agent FinOps Engine uses accumulated usage data
- **Phase 3**: Live streaming powers Web Agent Studio real-time view
- **Cursor Self-Hosted Agents**: Full lifecycle for K8s-based agent pods

Adapt for K8s:
- Task messages route through NATS JetStream for durability
- Token usage aggregated at pod level, correlated with K8s resource metrics
- Redaction service runs as a sidecar for consistent security enforcement
- Progress reporting maps to K8s Job status annotations

## Examples

### Typical task execution flow

```
1. User submits "Fix login timeout" → task created as `queued`
2. Daemon claims task → status transitions to `running`
3. Every 5s: daemon sends progress update (step 1/5, "Analyzing logs")
4. Every 5s: daemon batches agent output messages → POST /messages
5. Server redacts secrets from messages → persists + broadcasts via WebSocket
6. Agent completes → daemon calls POST /complete with PR URL + session_id
7. Daemon reports token usage: { anthropic/sonnet: 15K in + 3K out }
8. Server calculates cost, updates dashboard, publishes completion event
```

### Token usage accumulation

```
Task uses Sonnet for analysis (15K in / 3K out), then Haiku for formatting (2K in / 500 out)

POST /usage with array:
  [{ model: "sonnet", input: 15420, output: 3200, cache_read: 8500 },
   { model: "haiku",  input: 2000,  output: 500,  cache_read: 0 }]

Cost = (15420-8500)*sonnet_in_price + 8500*cache_price + 3200*sonnet_out_price
     + 2000*haiku_in_price + 500*haiku_out_price
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| 404 on progress | Task ID not found or already completed | Stop reporting, check task status |
| 409 on complete | Task already completed/cancelled | Idempotent — ignore duplicate |
| 500 on messages | Server-side redaction failure | Retry with exponential backoff; drop batch after 3 failures |
| Task stuck in `running` | Daemon crashed without reporting | Server detects via heartbeat timeout → marks `failed` |
| Usage report fails | Network error | Cache locally, retry on next cycle; usage must not block completion |

## Gotchas

- Progress reporting is fire-and-forget — NEVER block task execution on progress delivery failures
- Token usage MUST be reported independently of complete/fail — a failed task still incurs costs
- Message batching interval (5s) and progress rate limit (5s) should be tuned independently; they serve different purposes
- Redaction MUST happen at BOTH client (daemon) and server layers — defense in depth against secret leakage
- `seq` ordering in messages is critical for UI display — gaps are acceptable but out-of-order display breaks UX
- UPSERT on `(task_id, provider, model)` means usage reports are idempotent — safe to retry
- Cancellation poll (10s) adds latency to user cancel — prefer WebSocket push for production systems

## Checklist

- [ ] Define task state machine with explicit transition rules
- [ ] Implement progress reporting with WebSocket broadcast
- [ ] Build completion handler with session metadata persistence
- [ ] Build failure handler with error capture
- [ ] Implement mid-execution cancellation detection
- [ ] Design per-task token usage tracking schema (UPSERT)
- [ ] Build cost calculation from usage data (with cache awareness)
- [ ] Implement live message batching and streaming
- [ ] Build content redaction pipeline (client + server layers)
- [ ] Create WebSocket subscription for task-specific message streams
- [ ] Add rate limiting for progress and message endpoints
- [ ] Write integration tests for concurrent task lifecycle scenarios
- [ ] Build FinOps dashboard queries (per-workspace, per-agent, per-model)
