---
name: github-sprint-digest
description: >-
  Fetch overnight GitHub activity (issues, PRs, reviews, comments) per user
  across multiple projects, generate a Korean summary, and post structured
  digests to Notion sub-pages and Slack. Use when the user asks to "summarize
  GitHub activity", "sprint digest", "GitHub 스프린트 요약", "깃헙 활동 정리",
  "밤새 PR 정리", "github-sprint-digest", or wants a daily development activity
  summary across projects. Do NOT use for creating GitHub issues from commits
  (use commit-to-issue), PR review (use pr-review-captain), or full CI pipeline
  checks (use ci-quality-gate).
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "sprint-management"
---
# github-sprint-digest

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Fetch overnight GitHub activity per user across multiple projects and distribute Korean summaries.

## Workflow

1. **Fetch activity** — Use `gh` CLI to pull last 24h of GitHub events across configured repositories: new issues, PR opens/merges/reviews, review comments, CI status changes
2. **Per-user aggregation** — Group activity by contributor: what each person worked on, PRs awaiting review, blocked items, completed items
3. **Sprint context** — Cross-reference with current sprint milestones and project board status
4. **Generate digest** — Produce Korean summary per user with: completed items, in-progress items, blocked items, items needing feedback
5. **Distribute** — Create Notion sub-pages per user under the sprint parent page; post team-level summary to Slack sprint channel; flag items needing immediate feedback

## Composed Skills

- GitHub CLI (`gh`) — Issue/PR/review data fetching
- Notion MCP — Sub-page creation for per-user digests
- Slack MCP — Team-level summary posting

## Configuration

Target repositories (default — update per project):

```yaml
repositories:
  - ThakiCloud/ai-platform-webui
  - ThakiCloud/tkai-deploy
  - ThakiCloud/tkai-agents
  - ThakiCloud/research
  - ThakiCloud/ai-template
```

## Error Handling

| Error | Action |
|-------|--------|
| `gh` CLI not authenticated | Prompt user to run `gh auth login` |
| Repository access denied | Skip inaccessible repo, note in summary, continue with remaining |
| No activity in last 24h for a repo | Report "No activity" for that repo, don't create empty Notion page |
| Notion MCP unavailable | Fall back to Slack-only distribution |
| GitHub API rate limit | Reduce scope to last 12h or most-active repos first |

## Examples

```
User: "Summarize GitHub activity from last night to now"
→ Fetches 24h activity across configured repos → groups by user → creates Notion pages → posts Slack summary

User: "github-sprint-digest"
→ Full pipeline: fetch → aggregate → contextualize → generate → distribute
```
