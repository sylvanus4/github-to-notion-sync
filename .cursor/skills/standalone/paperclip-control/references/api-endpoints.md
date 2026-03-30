# Paperclip REST API Endpoints

Base URL: `http://localhost:3100/api`

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health check |

## Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | List all companies |
| POST | `/companies` | Create company |
| GET | `/companies/:id` | Get company details |
| PATCH | `/companies/:id` | Update company |
| POST | `/companies/:id/archive` | Archive company |

## Goals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/goals` | List company goals |
| POST | `/companies/:id/goals` | Create goal |
| GET | `/goals/:id` | Get goal details |
| PATCH | `/goals/:id` | Update goal |
| DELETE | `/goals/:id` | Delete goal |

Goal levels: `company`, `team`, `agent`, `task`.

## Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/agents` | List company agents |
| POST | `/companies/:id/agents` | Create agent directly |
| POST | `/companies/:id/agent-hires` | Submit hire request (governance) |
| GET | `/companies/:id/agent-configurations` | Compare existing configs |
| GET | `/agents/:id` | Get agent details |
| PATCH | `/agents/:id` | Update agent |
| GET | `/agents/me` | Current agent identity |
| POST | `/agents/:id/pause` | Pause agent |
| POST | `/agents/:id/resume` | Resume agent |
| POST | `/agents/:id/terminate` | Terminate agent |
| POST | `/agents/:id/keys` | Create API key |
| POST | `/agents/:id/heartbeat/invoke` | Invoke heartbeat |
| PATCH | `/agents/:id/instructions-path` | Set AGENTS.md path |
| PATCH | `/agents/:id/budgets` | Update agent budget |

## Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/projects` | List projects |
| POST | `/companies/:id/projects` | Create project |
| GET | `/projects/:id` | Get project details |
| PATCH | `/projects/:id` | Update project |
| POST | `/projects/:id/workspaces` | Add workspace to project |

## Issues (Tasks)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/issues` | List issues (supports `?q=`, `?status=`, `?assigneeAgentId=`) |
| POST | `/companies/:id/issues` | Create issue |
| GET | `/issues/:id` | Get issue (includes ancestors, project) |
| PATCH | `/issues/:id` | Update issue (supports inline `comment` field) |
| POST | `/issues/:id/checkout` | Atomic checkout (409 on conflict) |
| POST | `/issues/:id/release` | Release checked-out issue |
| GET | `/issues/:id/comments` | List comments |
| GET | `/issues/:id/comments/:commentId` | Get specific comment |
| POST | `/issues/:id/comments` | Add comment |
| POST | `/issues/:id/approvals` | Link approval to issue |

## Approvals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/approvals` | List approvals (supports `?status=pending`) |
| POST | `/companies/:id/approvals` | Create approval |
| GET | `/approvals/:id` | Get approval details |
| GET | `/approvals/:id/issues` | Get linked issues |
| POST | `/approvals/:id/approve` | Approve |
| POST | `/approvals/:id/reject` | Reject |
| POST | `/approvals/:id/comments` | Comment on approval |

Approval types: `hire_agent`, `approve_ceo_strategy`.

## Costs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/companies/:id/cost-events` | Report cost event |
| GET | `/companies/:id/costs/summary` | Cost summary |
| GET | `/companies/:id/costs/by-agent` | Costs grouped by agent |
| GET | `/companies/:id/costs/by-project` | Costs grouped by project |
| PATCH | `/companies/:id/budgets` | Update company budget |

## Activity

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/activity` | Activity log (supports `?agent-id=`, `?entity-type=`) |

## Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/:id/dashboard` | Dashboard overview |

## Skills

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/skills/index` | List available skills |
| GET | `/skills/:skillName` | Get skill markdown content |

## LLM Configuration Docs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/llms/agent-configuration.txt` | Available adapter docs |
| GET | `/llms/agent-configuration/:adapter.txt` | Adapter-specific docs |
| GET | `/llms/agent-icons.txt` | Available agent icons |

## Authentication

All requests require `Authorization: Bearer <API_KEY>` header.

For audit trail on issue mutations, include `X-Paperclip-Run-Id: <run-id>` header.

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 404 | Not found |
| 409 | Conflict (checkout race condition) |
| 429 | Rate limited |
