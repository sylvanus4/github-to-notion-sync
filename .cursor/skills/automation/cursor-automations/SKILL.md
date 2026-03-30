---
name: cursor-automations
description: >-
  Create, configure, and manage Cursor Automations — always-on cloud agents
  that run on schedules or respond to events from GitHub, Slack, Linear,
  PagerDuty, and webhooks. Guides through trigger selection, tool configuration,
  MCP setup, memory management, and prompt writing. Use when the user asks to
  "create an automation", "set up a cron agent", "automate PR reviews",
  "schedule a daily digest", "cursor automation", "always-on agent",
  "자동화 설정", or any task involving recurring/event-driven cloud agents.
  Do NOT use for local CI checks (use ci-quality-gate), one-time cloud agent
  runs, or Cursor IDE hooks (use hooks configuration).
metadata:
  author: thaki
  version: "1.0.0"
  category: automation
---

# Cursor Automations — Always-On Cloud Agents

Cursor Automations run cloud agents in the background on schedules or in response to events. They spin up an isolated Ubuntu VM, follow your prompt using configured tools and MCPs, and verify their own output.

Create automations at [cursor.com/automations/new](https://cursor.com/automations/new) or start from a [marketplace template](https://cursor.com/marketplace#automations).

## When to Use

- Setting up recurring code review, security scanning, or test coverage agents
- Automating bug triage from Slack channels
- Creating daily/weekly digest summaries posted to Slack
- Responding to GitHub PR events, Linear issues, or PagerDuty incidents
- Building custom event-driven workflows via webhooks

## Quick Start

Four steps to create an automation:

1. **Choose a trigger** — when should it run? (schedule, GitHub event, Slack message, etc.)
2. **Enable tools** — what can the agent do? (open PRs, send Slack messages, use MCP)
3. **Write a prompt** — what should the agent do? (instructions, quality bar, output format)
4. **Launch** — save and watch it run

## Automation Categories

### Review and Monitoring

Automations that catch issues before they reach production.

| Use Case | Trigger | Tools | Template |
|----------|---------|-------|----------|
| Security review | PR opened / PR pushed | PR Comment, Send Slack | `find-vulnerabilities` |
| Agentic codeowners | PR opened / PR pushed | PR Comment, Reviewers, Send Slack | `assign-pr-reviewers` |
| Critical bug detection | Daily schedule | Pull Request, Send Slack | `find-bugs` |
| Feature flag cleanup | Daily schedule | Pull Request, Send Slack | `clean-up-feature-flags` |

### Chores

Automations that handle everyday tasks and knowledge work.

| Use Case | Trigger | Tools | Template |
|----------|---------|-------|----------|
| Daily/weekly digest | Scheduled (cron) | Send Slack | `daily-digest` |
| Test coverage | Daily schedule | Pull Request, Send Slack | `add-test-coverage` |
| Bug triage from Slack | Slack message | Read Slack, Send Slack, Pull Request | `fix-slack-bugs` |
| Incident response | PagerDuty incident | Send Slack, Pull Request, MCP (Datadog) | Custom |

## Trigger Selection Guide

Choose based on **when** you want the agent to act:

| Question | Trigger Type |
|----------|-------------|
| On a recurring schedule? | **Scheduled** — cron expression or preset |
| When a PR is opened/pushed/merged? | **GitHub** — PR events |
| When code is pushed to a branch? | **GitHub** — Push to branch |
| When CI finishes? | **GitHub** — CI completed |
| When someone posts in Slack? | **Slack** — New message in channel |
| When a Linear issue changes? | **Linear** — Issue created / Status changed |
| When a PagerDuty incident fires? | **PagerDuty** — Incident triggered |
| From an internal system or CI pipeline? | **Webhook** — Custom HTTP POST |

An automation can have **multiple triggers** — it runs when any trigger fires.

For full trigger configuration details, see [references/trigger-catalog.md](references/trigger-catalog.md).

## Tool Configuration

Enable tools based on what the agent needs to do:

| Tool | Purpose | Requires |
|------|---------|----------|
| **Open Pull Request** | Create branches and open PRs | GitHub connection |
| **Comment on Pull Request** | Post review comments, approve/request changes | PR trigger |
| **Request Reviewers** | Assign reviewers using git blame/history | PR trigger |
| **Send to Slack** | Post messages to channels or reply in threads | Slack integration |
| **Read Slack Channels** | Read messages for context before acting | Slack integration |
| **MCP Server** | Connect external tools (Datadog, databases, APIs) | MCP configuration |

### Memory

Memory lets agents read/write persistent notes across runs. Enabled by default.

- Use memory to track patterns, known false positives, or team preferences
- Agents improve over time by learning from past runs
- View and edit memories from the tool configuration UI
- Disable for automations handling untrusted input

### Environment

- **Disabled** (default): Agent only reads/reviews code — faster startup
- **Enabled**: Agent installs dependencies, builds, runs tests — needed for code changes

Configure environment and secrets at [cursor.com/dashboard?tab=cloud-agents](https://cursor.com/dashboard?tab=cloud-agents).

For full tool details and MCP setup, see [references/tool-catalog.md](references/tool-catalog.md).

## Prompt Writing

The prompt defines what the agent does. Write it like instructions for a cloud agent.

### Structure Pattern

```
You are a [role] for [scope].

## Goal
[One sentence: what the agent should achieve]

## Investigation / Review Checklist
- [Specific check 1]
- [Specific check 2]

## Decision Rules
- [When to act vs skip]
- [Quality bar for PRs/comments]

## Output Format
- [What to post, where, and how]
```

### Key Principles

1. **Describe the output format** — Slack message structure, PR body template
2. **Set a quality bar** — when to open a PR vs comment vs do nothing
3. **Include decision rules** — what to do in different cases
4. **Reference enabled tools** — mention them by name or @-mention in the prompt
5. **Be specific** — what to check, change, or produce

For detailed prompt patterns and anti-patterns, see [references/prompt-writing-guide.md](references/prompt-writing-guide.md).

## Workflow

When helping a user create an automation:

### Step 1: Identify the Use Case

Ask the user what they want to automate. Match against known categories:

- **Review/Monitoring**: security, code quality, PR review, codeowners
- **Chores**: digest, test coverage, bug triage, incident response, cleanup

### Step 2: Select a Starting Point

Check if a marketplace template fits:

- Browse templates at [cursor.com/marketplace#automations](https://cursor.com/marketplace#automations)
- See [references/template-library.md](references/template-library.md) for full prompts

If no template fits, start from scratch at [cursor.com/automations/new](https://cursor.com/automations/new).

### Step 3: Configure Triggers and Tools

Use the trigger selection guide and tool configuration tables above. Help the user pick the right combination.

### Step 4: Write or Customize the Prompt

Either adapt a template prompt or write one from scratch using the structure pattern.

### Step 5: Set Permissions and Environment

- **Permissions**: Team Owned (shared) vs Private (personal)
- **Environment**: Enable only if the agent needs to build/test code
- **Model**: Default is fine; specify only if user has a preference

### Step 6: Launch and Iterate

Save the automation and monitor the first run. Use memory to improve over time.

## Examples

### Example 1: Daily Slack digest of repo changes

User says: "I want a daily summary of what changed in our repo posted to Slack"

Actions:
1. Start from `daily-digest` template
2. Trigger: Scheduled — every day at 17:00 UTC
3. Tools: Send to Slack (target channel)
4. Prompt: Summarize merged PRs, bug fixes, risks from last 24 hours
5. Create at cursor.com/automations/new

Result: Automation posts a structured digest to Slack every day at 5 PM UTC

### Example 2: Security review on every PR

User says: "Review all PRs for security vulnerabilities"

Actions:
1. Start from `find-vulnerabilities` template
2. Triggers: PR opened + PR pushed
3. Tools: Comment on PR, Send to Slack
4. Prompt: Threat-focused review for injection, auth bypass, secrets, SSRF, XSS
5. Create at cursor.com/automations/new

Result: Agent comments on PRs with prioritized findings and remediation guidance

### Example 3: Bug triage from Slack

User says: "When someone reports a bug in #bugs, investigate and fix it"

Actions:
1. Start from `fix-slack-bugs` template
2. Trigger: Slack — New message in #bugs channel
3. Tools: Read Slack, Send Slack, Open Pull Request
4. Prompt: Read thread context, investigate codebase, fix and open PR, reply in thread
5. Create at cursor.com/automations/new

Result: Agent reads bug reports, investigates root cause, opens fix PRs, and replies

### Example 4: Custom webhook-triggered automation

User says: "When our monitoring system detects high error rates, investigate and notify"

Actions:
1. Create new automation from scratch
2. Trigger: Webhook — POST to generated endpoint
3. Tools: Send to Slack, MCP (monitoring tool)
4. Prompt: Parse webhook payload, investigate codebase and logs via MCP, post findings to #incidents
5. Configure monitoring system to POST to the webhook URL with API key

Result: Automated incident investigation triggered by external monitoring

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Automation doesn't run | Trigger misconfigured | Verify trigger settings; check cron expression |
| Agent can't find files | Environment disabled | Enable environment if agent needs to build/test |
| Slack messages not sent | Integration not connected | Connect Slack at Dashboard > Integrations |
| MCP tools fail | Stdio server incompatible | Switch to HTTP MCP transport (recommended) |
| Webhook not triggering | Missing API key | Save automation first to generate webhook URL and key |
| Agent keeps making same mistakes | Memory disabled | Enable memory for self-improving behavior |
| CI failures on agent PRs | Auto-fix disabled | Enable "Automatically fix CI Failures" in dashboard |

## Identity

- Slack messages: sent as Cursor bot
- Private automation PRs: opened as your GitHub account
- Team-scoped automation PRs: opened as `cursor`
- GitHub comments/reviews/reviewer requests: run as `cursor`

## Billing

Automations create cloud agents and are billed based on cloud agent usage. See [cloud agent pricing](https://cursor.com/docs/account/pricing#cloud-agent).

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `security-expert` | Use findings to write security review automation prompts |
| `pr-review-captain` | Complement with automated PR review automations |
| `ci-quality-gate` | Automations can replace parts of local CI with cloud review |
| `simplify` / `deep-review` | Automation prompts can encode review agent patterns |
| `slack-agent` | For custom Slack bots beyond Cursor's built-in integration |

## References

- [Trigger Catalog](references/trigger-catalog.md) — All trigger types with configuration details
- [Tool Catalog](references/tool-catalog.md) — Tools, MCP setup, permissions
- [Template Library](references/template-library.md) — Marketplace templates with full prompts
- [Prompt Writing Guide](references/prompt-writing-guide.md) — Prompt structure and best practices
- [Cursor Automations Docs](https://cursor.com/docs/cloud-agent/automations) — Official documentation
- [Marketplace Templates](https://cursor.com/marketplace#automations) — Browse and install templates
