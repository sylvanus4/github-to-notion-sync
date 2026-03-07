## X-to-Slack

Analyze an X (Twitter) post and share structured intelligence to a Slack channel.

### Usage

Provide an X/Twitter URL and a Slack channel name (public or private):

```
https://x.com/username/status/1234567890 #channel-name
```

### Workflow

1. **Fetch tweet** -- Convert URL domain to `api.fxtwitter.com` and retrieve content via `WebFetch`
2. **Research** -- Run `WebSearch` on key topics from the tweet for additional context
3. **Find channel** -- Search public channels via `slack_search_channels`; if not found, fall back to `slack_search_public_and_private` for private channels
4. **Post title** -- Send 1-2 line Korean summary + original URL + `>>>` to the channel via `slack_send_message`
5. **Post summary** -- Reply in thread with detailed tweet summary + research findings in Korean
6. **Post insights** -- Reply in thread with AI GPU Cloud / AI Platform service insights in Korean

### Execution

Read and follow the `x-to-slack` skill (`.cursor/skills/x-to-slack/SKILL.md`) for detailed instructions, message templates, and error handling.

### Examples

Public channel:
```
https://x.com/kaboroevich/status/1892094882811285893 #ai-news
```

Private channel (same syntax -- auto-detected):
```
https://x.com/user/status/1234567890 #research
```
