# Tool Catalog

Automations include base cloud agent tools (file read/write, terminal, browser) plus these configurable tools.

## Built-In Tools

### 1. Open Pull Request

Create branches and open PRs on GitHub.

**Capabilities:**
- Write code, create branches, and open PRs
- Uses the repository from the GitHub trigger or trigger settings
- Agent can commit changes across multiple files

**When to enable:** Automations that should make code changes (bug fixes, test additions, cleanup).

**When to skip:** Review-only automations that just comment or notify.

---

### 2. Comment on Pull Request

Post comments on the triggering PR.

**Capabilities:**
- Top-level review comments
- Inline code comments on specific lines
- If approvals enabled: approve, request changes, dismiss reviews

**Requirements:** Requires a pull request trigger (PR opened, PR pushed, etc.)

**Approval option:** Enable separately — allows the agent to approve PRs or request changes.

---

### 3. Request Reviewers

Assign reviewers on the triggering PR.

**Capabilities:**
- Use `git blame`, `git log`, and memory to identify domain experts
- Assign up to 2 reviewers based on contribution history
- Check for existing reviewer assignments to avoid duplicates

**Requirements:** Requires a pull request trigger.

---

### 4. Send to Slack

Send messages to Slack channels.

**Capabilities:**
- Target a specific channel or let the agent choose dynamically
- For Slack-triggered automations: automatically replies in the triggering thread
- When "any channel" is allowed: includes read access to discover public channels

**Configuration options:**
- **Specific channel**: Agent posts only to the selected channel
- **Any channel**: Agent can discover and post to any public channel

---

### 5. Read Slack Channels

Read-only access to Slack channel messages.

**Capabilities:**
- List public channels
- Read messages and thread history
- Download shared files (screenshots, logs, code samples)

**When to enable:** When the agent needs context from Slack before acting (e.g., reading a bug report thread before investigating).

**Note:** Even without Read Slack, an agent with Send to Slack can read channels it can post to.

---

### 6. MCP Server

Connect external tools and data sources via Model Context Protocol.

**Capabilities:**
- Access any tool exposed by the connected MCP server
- Databases, monitoring, issue trackers, APIs

**Transport options:**

| Transport | How It Works | Security | Recommendation |
|-----------|-------------|----------|----------------|
| **HTTP** | Server runs externally; tool calls proxied through backend | Credentials never in VM | **Recommended** |
| **Stdio** | Server runs inside agent VM | Agent has access to env vars | Use when HTTP unavailable |

**Configuration:**
- Add MCP servers through the MCP dropdown at [cursor.com/agents](https://cursor.com/agents)
- Cloud agents support OAuth for MCP servers that need it
- Sensitive fields (CLIENT_SECRET, headers, env) are encrypted at rest and redacted after saving

**Common MCP servers for automations:**

| MCP Server | Use Case |
|------------|----------|
| Datadog | Log investigation, monitoring queries |
| Linear | Issue creation, status updates |
| Notion | Knowledge base updates, logging |
| PlanetScale / Neon | Database queries, schema checks |
| Sentry | Error tracking, issue analysis |

---

## Memory

Memory is a built-in tool (enabled by default) that persists notes across automation runs.

### How It Works

- Agent reads memories at the start of each run
- Agent writes new memories during the run
- Memories persist across all runs of the same automation
- View and edit memories from the tool configuration UI

### Use Cases

- Track known false positives to avoid re-flagging
- Remember team preferences and coding conventions
- Build a knowledge base of past decisions
- Record patterns from previous bug fixes

### Caution

Memories persist and influence future runs. For automations handling **untrusted input** (e.g., Slack messages from external users), consider disabling memory to prevent adversarial memory injection.

---

## Environment Configuration

### When to Enable

| Scenario | Environment |
|----------|------------|
| Review code, post comments, send Slack messages | **Disabled** (faster) |
| Run tests, build code, execute scripts | **Enabled** |
| Create PRs with code changes | **Enabled** |
| Read-only analysis with MCP tools | **Disabled** |

### Configuration Files

#### `.cursor/environment.json`

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "install": "npm install",
  "terminals": [
    {
      "name": "Run dev server",
      "command": "npm run dev"
    }
  ]
}
```

- `install`: Update command run before agent starts (should be idempotent)
- `terminals`: Processes started in tmux after boot
- `build.dockerfile`: Path relative to `.cursor/` directory

#### Resolution Order

1. Team environment configuration
2. Personal environment configuration
3. `.cursor/environment.json` in repository

### Secrets Management

Add secrets at [cursor.com/dashboard?tab=cloud-agents](https://cursor.com/dashboard?tab=cloud-agents):

- Key-value pairs shared across cloud agents
- Encrypted at rest with KMS
- **Redacted** option: scanned in commits to prevent accidental leaking

### Resource Limits

- Default VM profile with limited memory and CPU
- Enterprise plans: contact support for increased limits
- Docker-in-Docker supported for multi-service repos

---

## Automation Settings

### Model Selection

Same models as cloud agents, tailored for autonomous use. Cursor picks a default.

### Permissions

| Level | Visibility | Management |
|-------|-----------|------------|
| **Team Owned** | Team members can view | Team admins manage |
| **Team Visible** | Team members can view | Only you manage |
| **Private** | Only you and team admins | Only you manage |

### CI Auto-Fix

Cloud agents automatically attempt to fix CI failures on PRs they create:

- Ignores failing checks also failing on base commit
- Only GitHub Actions supported
- Disable per-PR: comment `@cursor autofix off`
- Disable globally: Dashboard > Cloud Agents > My Settings
