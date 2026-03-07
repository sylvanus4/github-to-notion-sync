# Bolt for JavaScript Patterns

Complete code patterns for building Slack agents with the official Bolt for JavaScript SDK.

## Project Stack

- **SDK**: `@slack/bolt` (official Slack SDK)
- **Runtime**: Node.js 18+
- **AI** (optional): AI SDK (`ai` package) or direct provider SDKs
- **Testing**: Vitest or Jest
- **Package Manager**: npm or pnpm

```json
{
  "dependencies": {
    "@slack/bolt": "^4.x",
    "ai": "^4.x",
    "@ai-sdk/anthropic": "latest",
    "zod": "^3.x"
  }
}
```

## App Initialization

### Socket Mode (recommended for local dev)

```typescript
import { App } from "@slack/bolt";

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡ Bot running in Socket Mode");
})();
```

### HTTP Mode (recommended for production)

```typescript
import { App, ExpressReceiver } from "@slack/bolt";

const receiver = new ExpressReceiver({
  signingSecret: process.env.SLACK_SIGNING_SECRET!,
});

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  receiver,
});

receiver.router.get("/health", (_req, res) => res.send("ok"));

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡ Bot running on HTTP");
})();
```

`ExpressReceiver` exposes an Express router for custom routes (health checks, webhooks, cron endpoints).

### AWS Lambda

```typescript
import { App, AwsLambdaReceiver } from "@slack/bolt";

const receiver = new AwsLambdaReceiver({
  signingSecret: process.env.SLACK_SIGNING_SECRET!,
});

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  receiver,
});

// Register event listeners here...

export const handler = async (event, context, callback) => {
  const handler = await receiver.start();
  return handler(event, context, callback);
};
```

## Event Listeners

### App Mention

```typescript
app.event("app_mention", async ({ event, client, logger }) => {
  try {
    await client.chat.postMessage({
      channel: event.channel,
      text: `Hi <@${event.user}>! How can I help?`,
      thread_ts: event.ts,
    });
  } catch (error) {
    logger.error("Failed to respond to mention:", error);
  }
});
```

### Direct Message

```typescript
app.event("message", async ({ event, client }) => {
  if (event.channel_type !== "im" || event.subtype) return;
  await client.chat.postMessage({
    channel: event.channel,
    text: "Got your DM! Let me look into that.",
    thread_ts: event.ts,
  });
});
```

### Slash Command

```typescript
app.command("/ask", async ({ command, ack, client }) => {
  await ack();
  const answer = await processQuestion(command.text);
  await client.chat.postMessage({
    channel: command.channel_id,
    text: answer,
  });
});
```

### Scheduled Message (Cron)

```typescript
// Using ExpressReceiver custom route
receiver.router.post("/api/cron/standup", async (req, res) => {
  const auth = req.headers.authorization;
  if (auth !== `Bearer ${process.env.CRON_SECRET}`) {
    return res.status(401).send("Unauthorized");
  }

  await app.client.chat.postMessage({
    channel: "#standup",
    text: "🌅 Time for standup! Reply in thread with your update.",
  });
  res.send("ok");
});
```

## AI Integration

### With AI SDK (recommended)

```typescript
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

app.event("app_mention", async ({ event, client }) => {
  const result = await generateText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: "You are a helpful assistant. Be concise.",
    prompt: event.text.replace(/<@[A-Z0-9]+>/g, "").trim(),
  });

  await client.chat.postMessage({
    channel: event.channel,
    text: result.text,
    thread_ts: event.ts,
  });
});
```

### With Anthropic SDK directly

```typescript
import Anthropic from "@anthropic-ai/sdk";
const anthropicClient = new Anthropic();

app.event("app_mention", async ({ event, client }) => {
  const response = await anthropicClient.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: event.text }],
  });

  await client.chat.postMessage({
    channel: event.channel,
    text: response.content[0].type === "text" ? response.content[0].text : "",
    thread_ts: event.ts,
  });
});
```

### Multi-turn Conversation (Thread Context)

```typescript
app.event("app_mention", async ({ event, client }) => {
  let messages = [{ role: "user" as const, content: event.text }];

  if (event.thread_ts) {
    const thread = await client.conversations.replies({
      channel: event.channel,
      ts: event.thread_ts,
    });
    messages = (thread.messages || []).map((m) => ({
      role: m.bot_id ? ("assistant" as const) : ("user" as const),
      content: m.text || "",
    }));
  }

  const result = await generateText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: "You are a helpful assistant.",
    messages,
  });

  await client.chat.postMessage({
    channel: event.channel,
    text: result.text,
    thread_ts: event.thread_ts || event.ts,
  });
});
```

## Block Kit Messages

```typescript
await client.chat.postMessage({
  channel: event.channel,
  blocks: [
    {
      type: "section",
      text: { type: "mrkdwn", text: "*Ticket Created*\nID: #12345" },
    },
    {
      type: "actions",
      elements: [
        {
          type: "button",
          text: { type: "plain_text", text: "View" },
          action_id: "view_ticket",
          value: "12345",
        },
        {
          type: "button",
          text: { type: "plain_text", text: "Close" },
          action_id: "close_ticket",
          value: "12345",
          style: "danger",
        },
      ],
    },
  ],
});
```

## Action Handlers

```typescript
app.action("view_ticket", async ({ action, ack, client, body }) => {
  await ack();
  const ticket = await getTicket(action.value);
  await client.chat.postMessage({
    channel: body.channel.id,
    text: `Ticket #${action.value}: ${ticket.title}\nStatus: ${ticket.status}`,
    thread_ts: body.message.ts,
  });
});
```

## Modal (Dialog)

```typescript
app.command("/feedback", async ({ command, ack, client }) => {
  await ack();
  await client.views.open({
    trigger_id: command.trigger_id,
    view: {
      type: "modal",
      callback_id: "feedback_modal",
      title: { type: "plain_text", text: "Feedback" },
      submit: { type: "plain_text", text: "Submit" },
      blocks: [
        {
          type: "input",
          block_id: "feedback_input",
          label: { type: "plain_text", text: "Your feedback" },
          element: { type: "plain_text_input", action_id: "feedback_text", multiline: true },
        },
      ],
    },
  });
});

app.view("feedback_modal", async ({ view, ack, client }) => {
  await ack();
  const feedback = view.state.values.feedback_input.feedback_text.value;
  // Process feedback
});
```

## Error Handler

Always add a global error handler:

```typescript
app.error(async (error) => {
  console.error("Unhandled error:", error);
});
```
