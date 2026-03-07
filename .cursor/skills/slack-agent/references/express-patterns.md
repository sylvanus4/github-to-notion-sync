# Express + Web API Patterns

Lightweight Slack bot patterns using Express and the Slack Web API directly.
Use when you want minimal dependencies and full control over the HTTP layer.

## Project Stack

- **Server**: Express
- **Slack SDK**: `@slack/web-api` (for sending messages)
- **Verification**: `@slack/events-api` or manual HMAC
- **AI** (optional): AI SDK or direct provider SDKs
- **Package Manager**: npm or pnpm

```json
{
  "dependencies": {
    "express": "^4.x",
    "@slack/web-api": "^7.x",
    "ai": "^4.x",
    "@ai-sdk/anthropic": "latest"
  }
}
```

## Basic Server

```typescript
import express from "express";
import crypto from "crypto";
import { WebClient } from "@slack/web-api";

const app = express();
const web = new WebClient(process.env.SLACK_BOT_TOKEN);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/health", (_req, res) => res.send("ok"));

app.post("/api/slack/events", async (req, res) => {
  // URL verification challenge
  if (req.body.type === "url_verification") {
    return res.json({ challenge: req.body.challenge });
  }

  // Verify signature
  if (!verifySlackSignature(req)) {
    return res.status(401).send("Invalid signature");
  }

  // Acknowledge immediately (Slack 3-second rule)
  res.status(200).send();

  // Process event in background
  handleEvent(req.body.event).catch(console.error);
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Bot running on port 3000");
});
```

## Signature Verification

```typescript
function verifySlackSignature(req: express.Request): boolean {
  const timestamp = req.headers["x-slack-request-timestamp"] as string;
  const signature = req.headers["x-slack-signature"] as string;
  const body = JSON.stringify(req.body);

  const fiveMinAgo = Math.floor(Date.now() / 1000) - 60 * 5;
  if (parseInt(timestamp) < fiveMinAgo) return false;

  const sigBasestring = `v0:${timestamp}:${body}`;
  const mySignature = "v0=" + crypto
    .createHmac("sha256", process.env.SLACK_SIGNING_SECRET!)
    .update(sigBasestring)
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(mySignature),
    Buffer.from(signature)
  );
}
```

## Event Handler

```typescript
async function handleEvent(event: any) {
  if (event.type === "app_mention") {
    const result = await generateText({
      model: anthropic("claude-sonnet-4-20250514"),
      prompt: event.text,
    });

    await web.chat.postMessage({
      channel: event.channel,
      text: result.text,
      thread_ts: event.ts,
    });
  }
}
```

## Slash Command Handler

```typescript
app.post("/api/slack/commands", async (req, res) => {
  if (!verifySlackSignature(req)) {
    return res.status(401).send("Invalid signature");
  }

  // Acknowledge immediately
  res.json({ response_type: "in_channel", text: "Processing..." });

  // Process in background
  const { command, text, channel_id } = req.body;
  const answer = await processCommand(command, text);
  await web.chat.postMessage({ channel: channel_id, text: answer });
});
```

## When to Use Express Over Bolt

| Scenario | Recommendation |
|----------|---------------|
| Standard Slack bot with events, commands, actions | **Use Bolt** — handles everything automatically |
| Simple webhook receiver only | Express is fine |
| Need full control over HTTP middleware | Express |
| Integrating into existing Express server | Express |
| All other cases | **Use Bolt** |

Bolt is essentially Express + Slack plumbing. For most projects, Bolt saves significant boilerplate.
