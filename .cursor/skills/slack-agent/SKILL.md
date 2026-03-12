---
name: slack-agent
description: >-
  Build and deploy Slack bots/agents using Bolt for JavaScript or Express.
  Guides through project setup, Slack app creation, environment configuration,
  local testing, and production deployment via an interactive wizard. Deployment
  target is user's choice: Docker/K8s, serverless, PaaS, or any Node.js host.
  Use when the user asks to "build a Slack bot", "create a Slack agent", "deploy
  a Slack app", "slack-agent", or mentions Slack bot development. Do NOT use for
  general Slack messaging (use kwp-slack-slack-messaging), Slack search (use
  kwp-slack-slack-search). Korean triggers: "슬랙 봇", "봇 만들기", "슬랙 앱".
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "execution"
---
# Slack Agent Development

Build Slack bots and AI agents with the official Slack SDK. Framework-agnostic deployment — run on Docker, Kubernetes, serverless, PaaS, or any Node.js host.

## Supported Frameworks

| Aspect | Bolt for JavaScript (Recommended) | Express + Web API |
|--------|-----------------------------------|-------------------|
| **Best for** | Most projects, event-driven bots | Simple webhook-only bots |
| **Package** | `@slack/bolt` | `express` + `@slack/web-api` |
| **Events** | `app.event()`, `app.command()`, `app.action()` | Manual webhook handler |
| **Messages** | `client.chat.postMessage(...)` | `web.chat.postMessage(...)` |
| **UI** | Block Kit JSON via Bolt helpers | Raw Block Kit JSON |
| **Socket Mode** | Built-in support | Manual implementation |
| **Complexity** | Low — handles auth, retry, ack automatically | Higher — manual signature verification |

**Bolt is recommended** for all new projects. It handles signature verification, event acknowledgment (3-second rule), retry logic, and middleware automatically.

## Command Routing

When invoked via `/slack-agent`, check for arguments:

| Argument | Action |
|----------|--------|
| `new` | Start wizard Phase 1: ask what agent to build, generate plan |
| `configure` | Start wizard at Phase 2 or 3 for existing projects |
| `deploy` | Start wizard at Phase 5 for production deployment |
| `test` | Start wizard at Phase 6 to set up testing |
| (none) | Auto-detect project state (see below) |

### Auto-Detection (No Argument)

1. **No `package.json` with `@slack/bolt`** → Treat as `new`, Phase 1
2. **Has project but no `manifest.json`** → Phase 2
3. **Has project but no `.env`** → Phase 3
4. **Has `.env` but not tested** → Phase 4
5. **Tested but not deployed** → Phase 5
6. **Otherwise** → General development assistance

## Wizard Overview

The wizard has 6 phases. For detailed step-by-step instructions, see [references/wizard-phases.md](references/wizard-phases.md).

| Phase | Name | What Happens |
|-------|------|-------------|
| 1 | Project Setup | Ask purpose, generate implementation plan |
| 1b | Plan Approval | Present plan for user review before scaffolding |
| 2 | Create Slack App | Customize `manifest.json`, create app in Slack console |
| 3 | Configure Environment | Set signing secret, bot token, API keys in `.env` |
| 4 | Local Testing | Start dev server (Socket Mode or ngrok), test in Slack |
| 5 | Production Deploy | Deploy to user's chosen platform |
| 6 | Setup Testing | Configure test framework, write unit and integration tests |

**IMPORTANT for `new` projects:**
1. Ask what kind of agent the user wants (see [references/agent-archetypes.md](references/agent-archetypes.md))
2. Generate a custom implementation plan
3. Get user approval BEFORE scaffolding

## Key Patterns

### Bolt App Setup

```typescript
import { App } from "@slack/bolt";

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,                          // For local dev; switch to HTTP for production
  appToken: process.env.SLACK_APP_TOKEN,     // Required for Socket Mode
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡ Slack bot is running!");
})();
```

### Event Handling

```typescript
app.event("app_mention", async ({ event, client }) => {
  await client.chat.postMessage({
    channel: event.channel,
    text: `Hello <@${event.user}>! How can I help?`,
    thread_ts: event.ts,
  });
});

app.command("/ask", async ({ command, ack, client }) => {
  await ack();
  const answer = await generateAnswer(command.text);
  await client.chat.postMessage({
    channel: command.channel_id,
    text: answer,
  });
});
```

### AI Integration

Use any LLM provider directly. The `ai` package (Vercel AI SDK) is open-source and works anywhere:

```typescript
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

app.event("app_mention", async ({ event, client }) => {
  const result = await generateText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: "You are a helpful support agent.",
    prompt: event.text,
  });
  await client.chat.postMessage({
    channel: event.channel,
    text: result.text,
    thread_ts: event.ts,
  });
});
```

Or use provider SDKs directly (OpenAI, Anthropic, etc.):

```typescript
import Anthropic from "@anthropic-ai/sdk";
const anthropic = new Anthropic();

const response = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: event.text }],
});
```

### Tool Definition (with AI SDK)

```typescript
import { tool } from "ai";
import { z } from "zod";

const lookupCustomer = tool({
  description: "Look up a customer record by email",
  parameters: z.object({
    email: z.string().describe("Customer email address"),
  }),
  execute: async ({ email }) => {
    const customer = await db.customers.findByEmail(email);
    return { success: true, customer };
  },
});
```

### Human-in-the-Loop (Approval via Block Kit)

```typescript
app.event("app_mention", async ({ event, client }) => {
  if (requiresApproval(event.text)) {
    await client.chat.postMessage({
      channel: event.channel,
      thread_ts: event.ts,
      blocks: [
        { type: "section", text: { type: "mrkdwn", text: `*Approval Required*\nAction: ${event.text}` } },
        { type: "actions", elements: [
          { type: "button", text: { type: "plain_text", text: "Approve" }, action_id: "approve_action", style: "primary", value: event.ts },
          { type: "button", text: { type: "plain_text", text: "Reject" }, action_id: "reject_action", style: "danger", value: event.ts },
        ]},
      ],
    });
  }
});

app.action("approve_action", async ({ action, ack, client, body }) => {
  await ack();
  await executeApprovedAction(action.value);
  await client.chat.update({
    channel: body.channel.id,
    ts: body.message.ts,
    text: "✅ Approved and executed.",
  });
});
```

For complete patterns, see:
- [references/bolt-patterns.md](references/bolt-patterns.md)
- [references/express-patterns.md](references/express-patterns.md)

## Deployment Options

| Platform | Best For | Deploy Command |
|----------|----------|----------------|
| **Docker / K8s** | Production, self-hosted | `docker build && kubectl apply` |
| **Railway** | Quick prototyping | `railway up` |
| **Render** | Free tier available | Git push to Render |
| **Fly.io** | Edge deployment | `fly deploy` |
| **AWS Lambda** | Serverless, pay-per-use | SAM / Serverless Framework |
| **Google Cloud Run** | Serverless containers | `gcloud run deploy` |

For Docker deployment (recommended for this project):

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "dist/app.js"]
```

## Required Environment Variables

| Variable | Source | Required |
|----------|--------|----------|
| `SLACK_BOT_TOKEN` | Slack App > OAuth & Permissions | Yes |
| `SLACK_SIGNING_SECRET` | Slack App > Basic Information | Yes |
| `SLACK_APP_TOKEN` | Slack App > Basic Information (Socket Mode) | Socket Mode only |
| `ANTHROPIC_API_KEY` | Provider dashboard | For AI (example) |
| `OPENAI_API_KEY` | Provider dashboard | For AI (example) |

## Examples

### Example 1: New support bot

User says: "Slack 봇 만들어줘. 내부 문서 기반으로 질문에 답변하는 지원 봇이야."

Actions:
1. Detect no existing Slack project → Phase 1
2. Propose Bolt + RAG tool plan
3. After approval, scaffold project with `@slack/bolt`
4. Walk through Slack app creation, env config, testing, deployment

Result: Deployed support bot responding to mentions with RAG-powered answers.

### Example 2: Add custom tool to existing bot

User says: "기존 Slack 봇에 Jira 티켓 생성 도구를 추가해줘"

Actions:
1. Detect existing Bolt project → General assistance
2. Create `createJiraTicket` tool
3. Register in agent's tool list
4. Add unit test, run quality checks

Result: Bot can create Jira tickets when asked in Slack.

### Example 3: Deploy to Kubernetes

User says: "Slack 봇 로컬 테스트 끝났으니 K8s에 배포해줘"

Actions:
1. Detect tested project → Phase 5
2. Create Dockerfile and K8s manifests (Deployment, Service, Secret)
3. Build image, push to registry, apply manifests
4. Update Slack app URLs to production endpoint

Result: Bot running on K8s cluster with env vars from Secrets.

## Error Handling

| Issue | Solution |
|-------|----------|
| Slack 3-second timeout | Use `ack()` immediately, process in background |
| `dispatch_failed` event | Add `app.event("dispatch_failed", ...)` handler |
| OAuth scope missing | Check `manifest.json` scopes match required permissions |
| Signature verification fails | Verify `SLACK_SIGNING_SECRET` is correct |
| Bot not responding to mentions | Ensure `app_mentions:read` scope and event subscription |
| ngrok tunnel not connecting | Restart ngrok, update Request URL in Slack app |
| Socket Mode disconnects | Check `SLACK_APP_TOKEN` is valid App-Level Token |
| Private channel access | Bot must be invited to the channel first |

## Quality Standards

For lint, test, and typecheck requirements, see [references/quality-standards.md](references/quality-standards.md).

## Additional Resources

- [Slack Bolt for JavaScript Docs](https://slack.dev/bolt-js/)
- [Slack API Documentation](https://api.slack.com/)
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- [AI SDK Documentation](https://sdk.vercel.ai/) (open-source, works anywhere)
