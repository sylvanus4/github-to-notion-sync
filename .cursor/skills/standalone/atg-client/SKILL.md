---
name: atg-client
description: >-
  Route Notion, Slack, and GitHub tool calls through the Agent Tool Gateway
  (ATG) HTTP API for caching, deduplication, and compression benefits. Falls
  back to direct MCP calls when ATG is unavailable. Use when a skill needs to
  call Notion, Slack, or GitHub APIs and the ATG server is running locally.
  Triggers: "call ATG", "ATG route", "gateway call", "ATG 호출", "게이트웨이
  라우팅", "atg-client". Do NOT use for tools not supported by ATG (Figma,
  Browser, Daiso, Context7, NotebookLM, HuggingFace — use their MCP servers
  directly). Do NOT use for ATG server development (edit Go code directly). Do
  NOT use for skill optimization analysis (use atg-skill-engineer).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "standalone"
---

# ATG Client

Route Notion, Slack, and GitHub tool calls through the Agent Tool Gateway for response caching, request deduplication, schema filtering, and response compression.

## Gateway Discovery

The ATG server URL is resolved in this order:

1. Environment variable `ATG_URL` (e.g., `http://localhost:4000`)
2. Default: `http://localhost:4000`

## Health Check

Before routing calls through ATG, verify the gateway is healthy:

```bash
curl -sf http://localhost:4000/api/v1/health
```

A healthy response returns HTTP 200. Any other response or timeout means ATG is unavailable — use MCP fallback.

## Tool Call Pattern

Route supported tool calls via `POST /api/v1/tools/call`:

```bash
curl -X POST http://localhost:4000/api/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "notion_search",
    "connector": "notion",
    "arguments": {"query": "project status"},
    "agent_id": "meeting-digest",
    "session_id": "session-abc",
    "compress": true
  }'
```

### Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| `tool` | yes | Tool name (e.g., `notion_search`, `slack_send_message`) |
| `connector` | no | Connector hint (`notion`, `slack`, `github`). Auto-detected from tool prefix if omitted |
| `arguments` | yes | Tool-specific arguments as key-value pairs |
| `agent_id` | no | Calling skill name for audit trail |
| `session_id` | no | Session identifier for deduplication grouping |
| `request_id` | no | Idempotency key |
| `auth_token` | no | Override connector auth token |
| `skip_cache` | no | Force fresh fetch, bypassing cache |
| `compress` | no | Request compressed response (85-96% size reduction) |

### Response Fields

| Field | Description |
|-------|-------------|
| `request_id` | Unique request identifier |
| `tool` | Tool that was called |
| `data` | Tool response payload |
| `cached` | Whether response was served from cache |
| `deduped` | Whether request was deduplicated with a concurrent identical request |
| `compressed` | Whether response was compressed |
| `latency_ms` | End-to-end latency in milliseconds |

## Schema Retrieval

Fetch filtered tool schemas to reduce context token usage:

```bash
curl http://localhost:4000/api/v1/tools/schema?connector=notion
```

Returns only schemas for the specified connector instead of all 40+ tools.

## Batch Execution

Submit multiple independent tool calls as a batch:

```bash
curl -X POST http://localhost:4000/api/v1/tools/batch \
  -H "Content-Type: application/json" \
  -d '{
    "calls": [
      {"tool": "notion_search", "connector": "notion", "arguments": {"query": "PRD"}},
      {"tool": "slack_list_channels", "connector": "slack", "arguments": {}},
      {"tool": "github_list_issues", "connector": "github", "arguments": {"repo": "ThakiCloud/ai-platform-webui"}}
    ],
    "agent_id": "daily-am-orchestrator"
  }'
```

The gateway executes independent calls in parallel and returns all results.

## Fallback Logic

When ATG is unavailable, fall back to direct MCP calls transparently:

```
1. GET {ATG_URL}/api/v1/health
2. If HTTP 200:
   → Route via POST {ATG_URL}/api/v1/tools/call
3. If connection refused, timeout, or non-200:
   → Fall back to CallMcpTool:
     - notion_* → server="plugin-notion-workspace-notion"
     - slack_*  → server="plugin-slack-slack"
     - github_* → server="user-GitHub"
   → Log: "ATG unavailable, using direct MCP fallback"
```

Skills MUST NOT fail when ATG is down. The gateway is an accelerator, not a dependency.

## Routing Matrix

| Tool Prefix | ATG Status | Route | MCP Fallback Server |
|-------------|------------|-------|---------------------|
| `notion_*` | Implemented | ATG | `plugin-notion-workspace-notion` |
| `slack_*` | Implemented | ATG | `plugin-slack-slack` |
| `github_*` | Implemented | ATG | `user-GitHub` |
| `figma_*` | Not supported | Direct MCP | `plugin-figma-figma` |
| `browser_*` | Not supported | Direct MCP | `cursor-ide-browser` |
| `daiso_*` | Not supported | Direct MCP | `user-daiso-mcp` |
| Others | Not supported | Direct MCP | Respective MCP server |

## Available Tools (40 Total)

### Notion Connector (14 tools)

| Tool | Cacheable | ReadOnly |
|------|-----------|----------|
| `notion_search` | yes | yes |
| `notion_get_page` | yes | yes |
| `notion_get_database` | yes | yes |
| `notion_query_database` | yes | yes |
| `notion_get_block_children` | yes | yes |
| `notion_create_page` | no | no |
| `notion_update_page` | no | no |
| `notion_get_page_incremental` | no | yes |
| `notion_structured_search` | yes | yes |
| `notion_batch_append_blocks` | no | no |
| `notion_batch_flush` | no | no |
| `notion_batch_status` | no | yes |
| `notion_recent_changes` | no | yes |
| `notion_invalidate_cache` | no | no |

### Slack Connector (17 tools)

| Tool | Cacheable | ReadOnly |
|------|-----------|----------|
| `slack_send_message` | no | no |
| `slack_list_channels` | yes | yes |
| `slack_get_channel_info` | yes | yes |
| `slack_get_history` | yes | yes |
| `slack_get_replies` | yes | yes |
| `slack_search_messages` | yes | yes |
| `slack_list_users` | yes | yes |
| `slack_get_user_info` | yes | yes |
| `slack_add_reaction` | no | no |
| `slack_create_canvas` | no | no |
| `slack_post_thread` | no | no |
| `slack_render_template` | no | yes |
| `slack_list_templates` | yes | yes |
| `slack_queued_send` | no | no |
| `slack_queue_status` | no | yes |
| `slack_recent_events` | no | yes |
| `slack_channel_activity` | no | yes |

### GitHub Connector (9 tools)

| Tool | Cacheable | ReadOnly |
|------|-----------|----------|
| `github_list_repos` | yes | yes |
| `github_get_repo` | yes | yes |
| `github_list_issues` | yes | yes |
| `github_get_issue` | yes | yes |
| `github_create_issue` | no | no |
| `github_list_pulls` | yes | yes |
| `github_search_code` | yes | yes |
| `github_search_issues` | yes | yes |
| `github_graphql` | no | no |

## Docker Quick Start

```bash
cd ai-platform/agent-tool-gateway
docker compose -f docker-compose.monitoring.yml up -d
curl http://localhost:4000/api/v1/health
```

Requires `.env` file with `NOTION_API_TOKEN`, `SLACK_BOT_TOKEN`, and `GITHUB_TOKEN`.
