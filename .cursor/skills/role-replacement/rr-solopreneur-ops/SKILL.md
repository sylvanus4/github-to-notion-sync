---
name: rr-solopreneur-ops
version: 1.0.0
description: >-
  Role Replacement Case Study: Solopreneur Operations Manager — autonomous daily
  operations pipeline that replaces a dedicated ops/admin hire by orchestrating
  email triage, calendar management, CRM deal tracking, meeting scheduling, and
  workspace cleanup into a unified end-of-day-ready operations cycle with morning
  routine automation and Supervisor-pattern exception handling.
tags: [role-replacement, harness, operations, solopreneur, automation]
triggers:
  - rr-solopreneur-ops
  - ops agent
  - solopreneur ops
  - 운영 에이전트
  - 오퍼레이션 에이전트
  - 1인 기업 운영
  - operations agent
  - daily ops automation
  - 일일 운영 자동화
do_not_use:
  - Full Google Workspace setup or CLI installation (use gws-workspace)
  - Stock trading or portfolio management (use toss-ops-orchestrator or today)
  - Code shipping or git operations (use eod-ship or sod-ship)
  - Content creation or marketing campaigns (use rr-solopreneur-content)
  - Deep research or paper review (use rr-solopreneur-researcher)
composes:
  - google-daily
  - gmail-daily-triage
  - smart-meeting-scheduler
  - deal-stage-guardian
  - slack-orphan-cleaner
  - calendar-daily-briefing
  - gws-email-reply
  - email-auto-reply
  - proactive-meeting-scheduler
  - decision-router
---

# Role Replacement: Solopreneur Operations Manager

Thin harness that replaces a dedicated operations/admin hire for solo founders and
small teams by orchestrating existing Google Workspace, Slack, and CRM skills into
a 5-phase daily operations pipeline with Supervisor-pattern exception escalation.

## What This Replaces

| Human Ops Role Task | Automated By | Skill |
|---|---|---|
| Morning inbox triage (spam, archive, flag) | Gmail rule-based triage with AI classification | `gmail-daily-triage` |
| Calendar briefing & meeting prep | Event extraction + preparation alerts | `calendar-daily-briefing` |
| Meeting scheduling from email context | Implicit meeting detection + slot finder | `smart-meeting-scheduler` + `proactive-meeting-scheduler` |
| Email reply drafting | Knowledge-based reply generation with approval gate | `email-auto-reply` + `gws-email-reply` |
| CRM pipeline stage tracking | Notion DB monitoring + checklist enforcement | `deal-stage-guardian` |
| Slack workspace cleanup | Orphaned thread detection and deletion | `slack-orphan-cleaner` |
| Decision routing | Pipeline output classification to correct channels | `decision-router` |
| Daily Google Workspace orchestration | Sequential calendar + email + drive workflow | `google-daily` |

## Prerequisites

- `gws` CLI authenticated (`gws auth status` returns `token_valid: true`)
- Slack MCP connected with `SLACK_USER_TOKEN` in `.env`
- Notion MCP connected (for `deal-stage-guardian` CRM tracking)
- No additional API keys required for core pipeline

## Architecture

```
Phase 1: MORNING ROUTINE (sequential)
  ├── calendar-daily-briefing (today's events + prep alerts)
  ├── gmail-daily-triage (spam delete, low-priority archive, flag action items)
  └── Output: morning_status { events_today, emails_flagged, urgent_items }

Phase 2: EMAIL PROCESSING (sequential with Supervisor)
  ├── proactive-meeting-scheduler (detect implicit meeting requests)
  ├── email-auto-reply (generate reply drafts for flagged emails)
  ├── SUPERVISOR: if reply confidence < 0.7 → escalate to user
  └── gws-email-reply (send approved replies)

Phase 3: CRM & DEAL TRACKING (sequential)
  ├── deal-stage-guardian (check stage transitions, enforce checklists)
  ├── decision-router (route deal decisions to #효정-의사결정)
  └── Output: crm_status { deals_moved, blockers, follow_ups }

Phase 4: MEETING MANAGEMENT (on-demand)
  ├── smart-meeting-scheduler (schedule meetings from flagged emails)
  ├── Conflict detection + free-slot discovery
  └── Output: meetings_scheduled []

Phase 5: EOD CLEANUP (sequential)
  ├── slack-orphan-cleaner (remove orphaned thread replies)
  ├── google-daily (full GWS cycle if not run in morning)
  └── Output: cleanup_status { threads_removed, workspace_state }
```

## Execution Modes

### Mode 1: Full Day Pipeline (default)
```
Input: "운영 에이전트" or "ops agent"
Output: Complete morning-to-EOD operations cycle
```

### Mode 2: Morning Only
```
Input: "운영 에이전트: 아침 루틴만" or "ops agent: morning only"
Output: Phase 1 + Phase 2 only (briefing + email processing)
```

### Mode 3: CRM Focus
```
Input: "운영 에이전트: CRM 체크" or "ops agent: deal tracking"
Output: Phase 3 only (deal stage monitoring + decision routing)
```

### Mode 4: Cleanup Only
```
Input: "운영 에이전트: 정리" or "ops agent: cleanup"
Output: Phase 5 only (Slack cleanup + workspace maintenance)
```

## Phase Details

### Phase 1: Morning Routine

1. Run `calendar-daily-briefing`:
   - Fetch today's Google Calendar events
   - Identify meetings requiring preparation (interviews, customer calls)
   - Generate preparation alerts with attendee context
2. Run `gmail-daily-triage`:
   - Delete spam and low-value notifications (Notion, RunPod, GitHub auto-emails)
   - Archive calendar accepts and read receipts
   - Flag emails requiring human response
   - Summarize unanswered emails with action items
3. Output morning status summary (Korean):
   - 오늘 일정 N건, 준비 필요 미팅 N건
   - 메일 처리: 삭제 N, 보관 N, 응답 필요 N
   - 긴급 항목: [list]

### Phase 2: Email Processing (Supervisor Pattern)

1. Run `proactive-meeting-scheduler`:
   - Scan flagged emails for implicit meeting requests ("let's discuss", "can we sync")
   - Propose meetings with context-derived agendas
2. Run `email-auto-reply`:
   - Generate 2-3 reply options per flagged email
   - Retrieve context from Cognee KG and recall memory
   - Score reply confidence (0-1)
3. SUPERVISOR GATE:
   - Confidence >= 0.7: present drafts for quick user approval
   - Confidence < 0.7: escalate with context summary, await user direction
   - NEVER auto-send without explicit approval
4. Run `gws-email-reply` for approved drafts:
   - Apply sentence polishing
   - Send via user identity (hyojung.han@thakicloud.co.kr)

### Phase 3: CRM & Deal Tracking

1. Run `deal-stage-guardian`:
   - Monitor Notion pipeline DB for stage changes
   - Enforce checklist completion at each stage gate
   - Identify stale deals (no activity > 7 days)
   - Generate handoff docs for stage transitions
2. Run `decision-router`:
   - Classify deal decisions (personal vs team)
   - Route to #효정-의사결정 or #7층-리더방 as appropriate
3. Output CRM status:
   - 딜 상태 변경: N건
   - 블로커: [list]
   - 팔로업 필요: [list with dates]

### Phase 4: Meeting Management

1. Run `smart-meeting-scheduler` for detected meeting needs:
   - Find conflict-free calendar slots
   - Generate agenda from email/Slack context
   - Create calendar event with pre-read materials
2. Conflict resolution:
   - If no mutual free slot found: propose 3 alternative options
   - If attendee info missing: ask user for clarification

### Phase 5: EOD Cleanup

1. Run `slack-orphan-cleaner`:
   - Scan registered channels for orphaned replies
   - Dry-run first, then execute deletion
   - Report threads removed count
2. Run `google-daily` (if not already run in morning):
   - Full GWS cycle: calendar + email + drive + Slack notification
3. Generate EOD summary:
   - 오늘 처리: 메일 N건, 미팅 예약 N건, 딜 업데이트 N건
   - 내일 준비 사항: [list]
   - 미완료 항목: [carry over to tomorrow]

## Supervisor Pattern Details

The Operations Agent employs a Supervisor pattern for decisions requiring human judgment:

| Situation | Automatic | Escalate |
|---|---|---|
| Spam deletion | Yes | Never |
| Calendar accept notifications | Yes (archive) | Never |
| Reply to known colleague (routine) | Draft + approve gate | If tone unclear |
| Reply to customer/external | Always escalate | Always |
| Meeting scheduling (internal) | Propose + approve | If conflict |
| Meeting scheduling (external) | Always escalate | Always |
| Deal stage transition | Notify | If checklist incomplete |
| Slack thread cleanup | Execute after dry-run | If parent msg ambiguous |

## Overlap & Differentiation

| Existing Agent | Overlap Area | Differentiation |
|---|---|---|
| `rr-executive-assistant` | Calendar + email + decision routing | EA is broader (full Google Daily + Slack cleanup combined); Ops focuses on CRM + meeting automation |
| `rr-inbox-zero-curator` | Email triage + Slack routing | Inbox Zero curates news/content; Ops handles action-required emails + replies |
| `rr-personal-coo` | 6-axis orchestration including life axis | COO is meta-orchestrator; Ops is focused single-axis operations |
| `google-daily` | GWS automation | google-daily is a sub-component; Ops adds CRM, reply generation, Supervisor |

## Error Handling

- gws CLI not authenticated → warn user, skip GWS phases, proceed with Slack/CRM only
- No emails flagged → skip Phase 2, proceed to Phase 3
- deal-stage-guardian Notion DB not configured → skip Phase 3, note in output
- Slack MCP unavailable → skip Phase 5 slack-orphan-cleaner, note in output
- All phases skippable independently; agent reports partial results rather than failing

## Invocation Examples

```
"운영 에이전트"
"ops agent: run full pipeline"
"오퍼레이션 에이전트: 아침 루틴"
"1인 기업 운영: CRM 딜 체크해줘"
"daily ops automation: cleanup slack and email"
"운영 에이전트: 내일 미팅 잡아줘 — 김OO 팀장님과 AI 플랫폼 논의"
```
