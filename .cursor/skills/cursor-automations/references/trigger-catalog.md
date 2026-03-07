# Trigger Catalog

Triggers decide when an automation runs. An automation can have **multiple triggers** and runs when any trigger fires.

## 1. Scheduled Triggers

Run on a recurring schedule using preset options or cron expressions.

### Preset Options

| Preset | Cron Equivalent |
|--------|----------------|
| Every hour | `0 * * * *` |
| Every day at 10:00 UTC | `0 10 * * *` |
| Every day at 17:00 UTC | `0 17 * * *` |
| Every Monday at 9:00 UTC | `0 9 * * 1` |

### Cron Expression Format

```
┌─── minute (0-59)
│ ┌─── hour (0-23)
│ │ ┌─── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

### Common Cron Patterns

| Pattern | Expression | Use Case |
|---------|-----------|----------|
| Every weekday at 6 AM | `0 6 * * 1-5` | Morning test coverage |
| Every 2 hours | `0 */2 * * *` | Frequent monitoring |
| Every Monday and Thursday | `0 9 * * 1,4` | Bi-weekly digest |
| First of every month | `0 0 1 * *` | Monthly cleanup |
| Every 30 minutes | `*/30 * * * *` | High-frequency checks |

### Notes

- Scheduled triggers may run with a delay but will not start before the indicated time
- You must also choose a **repository** and **branch** for scheduled triggers

---

## 2. GitHub Triggers

Respond to GitHub events. The repository is inferred from the event.

### Event Types

| Event | Fires When | Use Case |
|-------|-----------|----------|
| **PR opened** | Non-draft PR created or draft marked ready | Security review, reviewer assignment |
| **Draft opened** | Draft PR created | Early review, WIP monitoring |
| **PR pushed** | New commits pushed to existing PR | Re-review after changes |
| **PR commented** | Someone comments on a PR | Respond to review feedback |
| **PR merged** | PR is merged | Post-merge cleanup, notifications |
| **Push to branch** | Commits pushed to a branch outside a PR | Main branch monitoring |
| **CI completed** | GitHub Check finishes on PR or branch | Post-CI analysis, fix failures |

### Common Combinations

| Automation | Triggers |
|-----------|----------|
| Security review | PR opened + PR pushed |
| Auto-assign reviewers | PR opened + PR pushed |
| Post-merge digest | PR merged |
| CI failure investigation | CI completed |

---

## 3. Slack Triggers

Respond to Slack events. Requires the [Cursor Slack integration](https://cursor.com/docs/integrations/slack).

### Event Types

| Event | Fires When | Notes |
|-------|-----------|-------|
| **New message in channel** | Message sent to a connected public channel | Only top-level messages by default; add keyword/regex filter for thread replies |
| **Channel created** | New public channel created in workspace | Channel setup automation |

### Message Filters

Add filters to control which messages trigger the automation:

- **Keyword filter**: Only fire on messages containing specific words (e.g., "bug", "error", "broken")
- **Regex filter**: Pattern-based matching for structured messages
- Without a filter, only top-level channel messages trigger the automation

### Notes

- Only public Slack channels are visible to Slack triggers
- You must choose a **repository** and **branch** for Slack triggers
- For Slack-triggered automations, the agent automatically replies in the triggering message's thread

---

## 4. Linear Triggers

Respond to Linear events. Requires the [Cursor Linear integration](https://cursor.com/docs/integrations/linear).

### Event Types

| Event | Fires When | Use Case |
|-------|-----------|----------|
| **Issue created** | New issue created | Auto-triage, investigation |
| **Status changed** | Issue status changes | Workflow automation |
| **End of cycle** | Linear cycle completes | Sprint summary, cleanup |

### Configuration

Assign issues to `Cursor` in Linear or mention `@Cursor` in comments to trigger agents directly without automations.

### Repository Selection for Linear

Priority order:
1. Issue description/comments: `[repo=owner/repository]` syntax
2. Issue labels: Parent label "repo" with child labels as `owner/repo`
3. Project labels: Same structure at project level
4. Default repository in Cursor dashboard

---

## 5. PagerDuty Triggers

Respond to PagerDuty incident events for automated incident response.

### Event Types

| Event | Fires When | Use Case |
|-------|-----------|----------|
| **Incident triggered** | New incident created | Auto-investigate, notify on-call |
| **Incident acknowledged** | Incident acknowledged | Provide investigation context |
| **Incident resolved** | Incident resolved | Post-mortem, cleanup |
| **Any incident event** | Matches all event types | Broad incident monitoring |

### Typical Pattern

1. PagerDuty incident triggers automation
2. Agent uses MCP (e.g., Datadog) to investigate logs
3. Agent checks codebase for recent changes
4. Agent posts findings to Slack channel
5. Agent optionally opens a PR with a proposed fix

---

## 6. Webhook Triggers

Create a private HTTP endpoint for custom event sources.

### Setup

1. Create the automation with a webhook trigger
2. **Save the automation** — this generates the webhook URL and API key
3. Configure your external system to POST to the endpoint

### Endpoint Format

```
POST https://cursor.com/api/automations/<automation-id>/webhook
Authorization: Bearer <api-key>
Content-Type: application/json

{
  "event": "your-custom-event",
  "data": {
    "key": "value"
  }
}
```

### Webhook Verification (Outbound)

When an agent finishes, Cursor sends a webhook to your configured URL. Verify authenticity:

**Headers sent by Cursor:**

| Header | Value |
|--------|-------|
| `User-Agent` | `Cursor-Agent-Webhook/1.0` |
| `X-Webhook-Event` | Event type (`statusChange`) |
| `X-Webhook-ID` | Unique delivery identifier |
| `X-Webhook-Signature` | HMAC-SHA256 signature |

**Signature verification (JavaScript):**

```javascript
const crypto = require("crypto");

function verifyWebhook(secret, rawBody, signature) {
  const expected =
    "sha256=" +
    crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
  return signature === expected;
}
```

**Signature verification (Python):**

```python
import hmac
import hashlib

def verify_webhook(secret, raw_body, signature):
    expected = 'sha256=' + hmac.new(
        secret.encode(), raw_body, hashlib.sha256
    ).hexdigest()
    return signature == expected
```

### Outbound Webhook Payload

```json
{
  "event": "statusChange",
  "timestamp": "2024-01-15T10:30:00Z",
  "id": "bc_abc123",
  "status": "FINISHED",
  "source": {
    "repository": "https://github.com/your-org/your-repo",
    "ref": "main"
  },
  "target": {
    "url": "https://cursor.com/agents?id=bc_abc123",
    "branchName": "cursor/add-readme-1234",
    "prUrl": "https://github.com/your-org/your-repo/pull/1234"
  },
  "summary": "Added README.md with installation instructions"
}
```

### Webhook Best Practices

- Store raw payloads for debugging
- Use HTTPS URLs in production
- Return 2xx status codes quickly
- Handle retries for error responses
- Always verify signatures

### Use Cases

| Source System | Event | Agent Action |
|--------------|-------|-------------|
| Monitoring (Datadog, Grafana) | High error rate | Investigate + notify |
| CI/CD pipeline | Deploy completed | Smoke test + report |
| Internal tooling | Feature flag change | Validate + cleanup |
| Security scanner | Vulnerability found | Assess + patch |
