# Wizard Phases

Detailed step-by-step guide for each phase of the Slack agent setup wizard.

## Phase 1: Project Setup

1. **Ask the user** what kind of agent they want to build
   - Refer to [agent-archetypes.md](agent-archetypes.md) for common patterns
2. **Generate implementation plan** tailored to the use case:
   - System prompt design
   - Required tools (built-in + custom)
   - AI provider choice (Anthropic, OpenAI, etc.)
   - Deployment target (Docker, K8s, serverless, PaaS)
3. **Present plan** for approval (Phase 1b)

### Scaffold Project

```bash
mkdir my-slack-bot && cd my-slack-bot
npm init -y
npm install @slack/bolt ai @ai-sdk/anthropic zod
npm install -D typescript @types/node vitest
npx tsc --init
```

Create `src/app.ts`:

```typescript
import { App } from "@slack/bolt";

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

app.event("app_mention", async ({ event, client }) => {
  await client.chat.postMessage({
    channel: event.channel,
    text: `Hello <@${event.user}>!`,
    thread_ts: event.ts,
  });
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡ Bot running!");
})();
```

## Phase 1b: Plan Approval

Present the generated plan with:
- Agent description and personality
- List of tools (built-in + custom)
- System prompt draft
- Architecture decisions (AI provider, deployment target)

Wait for explicit user approval before proceeding.

## Phase 2: Create Slack App

1. **Create `manifest.json`**:

```json
{
  "display_information": {
    "name": "My Bot",
    "description": "An AI-powered assistant"
  },
  "features": {
    "bot_user": { "display_name": "mybot", "always_online": true }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "app_mentions:read",
        "channels:history", "channels:read",
        "chat:write",
        "groups:history", "groups:read",
        "im:history", "im:read", "im:write",
        "users:read"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "bot_events": ["app_mention", "message.im"]
    },
    "interactivity": { "is_enabled": true },
    "socket_mode_enabled": true
  }
}
```

2. **Create app in Slack console**:
   - Open https://api.slack.com/apps
   - Click "Create New App" → "From an app manifest"
   - Select workspace → Paste `manifest.json` → Create

3. **Install to workspace**:
   - Go to "Install App" → "Install to Workspace" → Authorize

## Phase 3: Configure Environment

1. **Create `.env` file**:
   ```env
   SLACK_BOT_TOKEN=xoxb-...        # OAuth & Permissions > Bot User OAuth Token
   SLACK_SIGNING_SECRET=...         # Basic Information > Signing Secret
   SLACK_APP_TOKEN=xapp-...         # Basic Information > App-Level Tokens > Generate Token
   ANTHROPIC_API_KEY=...            # Or OPENAI_API_KEY, depending on provider
   ```

2. **Guide user** to find each value:
   - Bot Token: Slack App > OAuth & Permissions > Bot User OAuth Token
   - Signing Secret: Slack App > Basic Information > App Credentials
   - App Token: Slack App > Basic Information > App-Level Tokens > Generate (scope: `connections:write`)

## Phase 4: Local Testing

### Option A: Socket Mode (recommended for local dev)

No ngrok needed. Socket Mode connects via WebSocket.

1. Enable Socket Mode in `manifest.json` (already done in Phase 2)
2. Start the bot: `npx tsx src/app.ts`
3. Test in Slack: `@mybot hello`

### Option B: HTTP Mode with ngrok

1. Switch app to HTTP mode (disable Socket Mode)
2. Start bot: `npx tsx src/app.ts`
3. Start ngrok: `ngrok http 3000`
4. Update Slack app:
   - Event Subscriptions Request URL → `https://<ngrok-url>/slack/events`
   - Interactivity Request URL → same
5. Test in Slack: `@mybot hello`

## Phase 5: Production Deployment

Ask the user which platform they want to deploy to. Common options:

### Docker / Kubernetes

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY dist/ ./dist/
EXPOSE 3000
CMD ["node", "dist/app.js"]
```

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: slack-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: slack-bot
  template:
    metadata:
      labels:
        app: slack-bot
    spec:
      containers:
        - name: slack-bot
          image: registry.example.com/slack-bot:latest
          ports:
            - containerPort: 3000
          envFrom:
            - secretRef:
                name: slack-bot-secrets
```

For production HTTP mode:
- Switch from Socket Mode to `ExpressReceiver`
- Set Event Subscriptions URL to your production endpoint
- Use K8s `Secret` for env vars

### Railway / Render / Fly.io

1. Push to Git repository
2. Connect to platform, set env vars
3. Auto-deploys on push

### AWS Lambda

Use `AwsLambdaReceiver` from `@slack/bolt`:

```typescript
import { App, AwsLambdaReceiver } from "@slack/bolt";

const receiver = new AwsLambdaReceiver({
  signingSecret: process.env.SLACK_SIGNING_SECRET!,
});
const app = new App({ token: process.env.SLACK_BOT_TOKEN, receiver });

// ... register listeners ...

export const handler = async (event, context, callback) => {
  const lambdaHandler = await receiver.start();
  return lambdaHandler(event, context, callback);
};
```

### Post-Deployment Checklist

1. Update Slack app URLs to production endpoint
2. Verify bot responds in Slack
3. Disable Socket Mode if using HTTP in production
4. Set up monitoring/logging

## Phase 6: Setup Testing

1. **Configure Vitest**:
   ```bash
   npm install -D vitest
   ```

2. **Add test scripts** to `package.json`:
   ```json
   {
     "scripts": {
       "test": "vitest run",
       "test:watch": "vitest"
     }
   }
   ```

3. **Write unit tests** for all tools and event handlers.

See [quality-standards.md](quality-standards.md) for test requirements.
