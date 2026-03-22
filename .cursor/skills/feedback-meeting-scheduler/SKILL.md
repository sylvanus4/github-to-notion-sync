---
name: feedback-meeting-scheduler
description: >-
  Detect PRs and issues needing discussion (stale reviews, conflicting comments,
  blocked items) and proactively schedule 1:1 feedback meetings with relevant
  parties. Use when the user asks to "schedule feedback meetings", "find items
  needing discussion", "피드백 미팅 잡아줘", "리뷰 미팅 스케줄",
  "feedback-meeting-scheduler", or wants automated meeting proposals from sprint
  activity. Do NOT use for general meeting scheduling (use
  smart-meeting-scheduler), calendar management (use gws-calendar), or sprint
  triage without meetings (use sprint-orchestrator).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Feedback Meeting Scheduler

Proactively detect work items needing face-to-face discussion and schedule 1:1 meetings with auto-generated agendas.

## When to Use

- After `github-sprint-digest` runs — detect items needing discussion
- When PR reviews are stale (> 48 hours without response)
- When issue discussions have conflicting opinions
- As part of the sprint orchestrator pipeline

## Workflow

### Step 1: Detect Discussion-Worthy Items

Query GitHub for items needing attention:

**Stale PR Reviews** (no review response > 48h):
```bash
gh pr list --state open --json number,title,author,reviewRequests,reviews,updatedAt
```
Filter: PRs where `reviewRequests` exist but no `reviews` submitted, and `updatedAt` > 48h ago.

**Conflicting Discussions** (opposing review comments):
Look for PRs with both "Request changes" and approved reviews, or issues with > 5 comments with no resolution.

**Blocked Items** (labeled or commented as blocked):
Search for issues/PRs with `blocked` label or comments containing "blocked by", "waiting for", "dependency on".

**Failed CI with no action** (CI red > 24h):
PRs where CI checks failed and no new commits pushed since failure.

### Step 2: Identify Participants

For each discussion-worthy item:
- **PR author** + **requested reviewers** for stale reviews
- **All commenters** for conflicting discussions
- **Assignee** + **blocker owner** for blocked items
- Map GitHub usernames to Google Calendar email addresses using a team directory

### Step 3: Generate Meeting Agenda

Create a contextual agenda from the item:

```
Feedback Meeting: PR #42 — Add user authentication
==================================================
Context: PR open for 5 days, 2 review requests pending

Agenda:
1. Review scope and approach (author presents — 5 min)
2. Address security concerns from @reviewer1 comment (10 min)
3. Discuss API contract changes with backend team (10 min)
4. Agree on next steps and timeline (5 min)

Pre-read:
- PR: https://github.com/org/repo/pull/42
- Related issue: #38
```

### Step 4: Find Available Slots

Use `gws-calendar` to find mutual availability:
- Check next 3 business days
- Prefer morning slots (focus time protection)
- Duration: 30 minutes default
- Avoid back-to-back with existing meetings

### Step 5: Propose or Schedule

Two modes:
- **Propose mode** (default): Post meeting proposals to Slack for approval
- **Auto-schedule mode** (if enabled): Create calendar events directly

Slack proposal format:
```
📋 Feedback meeting suggested

PR #42 — Add user authentication
Participants: @author, @reviewer1, @reviewer2
Reason: Review pending > 48 hours
Proposed slot: Tomorrow 10:00-10:30

React ✅ to confirm, ❌ to decline, 🔄 for alternative time
```

### Step 6: Report

```
Feedback Meeting Report
=======================
Items needing discussion: 4
Meetings proposed: 3
Already resolved: 1

Proposed Meetings:
1. PR #42 — Auth implementation (author + 2 reviewers) → Tomorrow 10:00
2. Issue #55 — Blocked by API change (assignee + API owner) → Wed 14:00
3. PR #61 — Conflicting approaches (3 commenters) → Thu 09:30
```

## Error Handling

| Error | Action |
|-------|--------|
| Calendar API auth failure | Prompt user to re-authenticate via `gws auth login`; skip calendar steps and output text-only proposals |
| No reviewable PRs/issues found | Report "no items requiring discussion" and exit cleanly |
| Attendee email not found | Log warning with GitHub username; propose meeting without that attendee and note in report |
| All time slots occupied | Suggest next available day; offer to send async summary instead of meeting |
| gws CLI not installed | Show installation instructions (`npm i -g @anthropic-ai/gws`); fall back to text-only proposals |

## Examples

### Example 1: Post-digest check
User says: "Any items need discussion?"
Actions:
1. Scan open PRs and issues for discussion signals
2. Identify participants for each item
3. Propose meetings with agendas
Result: Meeting proposals posted to Slack

### Example 2: Auto-schedule mode
User says: "Schedule feedback meetings for stale PRs"
Actions:
1. Find PRs with reviews pending > 48h
2. Check participant calendars
3. Create calendar events with agendas
Result: Calendar events created, participants notified
