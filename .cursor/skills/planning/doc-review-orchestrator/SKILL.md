---
name: doc-review-orchestrator
description: >-
  Orchestrate end-to-end document review workflows: create review requests in
  Notion, auto-assign reviewers by document type, send Slack notifications,
  track responses, escalate unresponsive reviewers after 48h, run quality gate,
  and update doc status with related doc links. Use when the user asks to
  "start document review", "문서 리뷰 요청", "리뷰 오케스트레이션", "문서 검토
  시작", "doc review request", "리뷰어 배정", "문서 검수 프로세스", or needs to
  initiate and track a structured document review. Do NOT use for document
  quality scoring only (use doc-quality-gate), meeting digest (use
  meeting-digest), or code review (use code-reviewer).
metadata:
  author: thaki
  version: "1.0.1"
  category: orchestrator
---

# Doc Review Orchestrator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

End-to-end pipeline for structured document review. Creates review requests, assigns reviewers, manages notifications and escalations, runs quality gates, and maintains review audit trail in Notion.

## Input

The user provides:
1. **Document** — Notion page URL, file path, or document title to review
2. **Review type** — One of: `standard` (48h), `expedited` (24h), `async` (1 week)
3. **Reviewers** — Optional: specific reviewer names; default: auto-assign by doc type
4. **Quality gate** — Optional: run `doc-quality-gate` before sending to reviewers (default: yes)

## Workflow

### Phase 1: Pre-Review Quality Gate

Before sending to human reviewers, run automated quality check:

1. Invoke `doc-quality-gate` on the document
2. If score < 5/6: return feedback to author with required fixes; do NOT proceed to review
3. If score >= 5/6: proceed to Phase 2

This prevents wasting reviewer time on documents with basic quality issues.

### Phase 2: Create Review Request

1. Create a review request entry in Notion:
   - Title: `[Review] {document title} — {date}`
   - Properties: document link, author, review type, deadline, status (Pending)
2. Link the review request to the source document as a related page

### Phase 3: Assign Reviewers

Auto-assign based on document type if not specified:

| Document Type | Default Reviewers | Min Reviewers |
|---------------|-------------------|---------------|
| PRD | PM lead + Tech lead | 2 |
| Design spec | Design lead + PM | 2 |
| Policy | Legal + PM lead | 2 |
| Technical spec | Tech lead + Senior engineer | 2 |
| Postmortem | Engineering manager + SRE lead | 2 |
| Research | Research lead + PM | 1 |

Record assigned reviewers in the Notion review request.

### Phase 4: Notify Reviewers

Send Slack notifications:

1. **Channel notification** — Post to the planning automation Slack channel (e.g. team default) with:
   - Document title and link
   - Review type and deadline
   - Assigned reviewers (mentions)
2. **Individual DMs** — Send DM to each reviewer with:
   - Document link
   - What to review (scope and focus areas)
   - Deadline
   - How to submit feedback (Notion comment or Slack thread)

### Phase 5: Track Responses

Monitor reviewer activity:

1. Poll Notion review request page for comments every 12h
2. Track per-reviewer status:
   - `notified` — DM sent, no response yet
   - `acknowledged` — Reviewer opened the document
   - `reviewing` — Reviewer added comments
   - `completed` — Reviewer submitted final feedback
   - `overdue` — Past deadline with no response

### Phase 6: Escalation

When a reviewer is overdue:

| Timeline | Action |
|----------|--------|
| Deadline reached | Slack reminder DM to reviewer |
| +24h after deadline | Escalation to reviewer's manager via Slack |
| +48h after deadline | Mark as "unresponsive"; notify document author to proceed without this review |

### Phase 7: Consolidate and Close

When all reviewers have responded (or escalation resolves):

1. Aggregate all review comments from Notion
2. Categorize feedback:
   - **Blocking**: Must fix before approval
   - **Suggestion**: Recommended but not required
   - **Praise**: Positive feedback (no action needed)
3. Update review request status to "Review Complete"
4. Notify document author with consolidated feedback summary
5. If no blocking feedback: update document status to "Approved"
6. Run `cross-domain-sync-checker` to check if approved doc is in sync with design/code

## Skill Chain

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | doc-quality-gate | Pre-review automated quality check |
| 2 | Notion MCP | Create review request, track comments |
| 3 | Slack MCP | Notify reviewers, send reminders, escalate |
| 4 | cross-domain-sync-checker | Post-approval sync check |
| 5 | md-to-notion | Publish review summary |

## Output Format

```markdown
## Document Review Summary

**Document**: [title]
**Review Type**: [standard/expedited/async]
**Duration**: [start date] → [end date]
**Quality Gate**: PASSED ([score]/6)

### Reviewer Status
| Reviewer | Status | Response Date | Feedback Type |
|----------|--------|---------------|---------------|
| [name] | Completed | 2026-03-24 | 2 blocking, 3 suggestions |
| [name] | Completed | 2026-03-25 | 0 blocking, 5 suggestions |

### Consolidated Feedback
#### Blocking Items
1. [feedback item] — Reviewer: [name]

#### Suggestions
1. [feedback item] — Reviewer: [name]

### Verdict: APPROVED / REVISION REQUIRED
```

## Examples

### Example 1: Standard PRD review

User says: "Start a review for this PRD: [Notion URL]"

Actions:
1. Quality gate: 6/6 PASSED
2. Create review request in Notion
3. Auto-assign: PM lead + Tech lead
4. DM both reviewers with deadline (48h)
5. After 36h: PM lead completed, Tech lead reviewing
6. After 48h: both completed
7. Consolidate: 1 blocking item, 4 suggestions

Result: Review summary posted, document status updated

### Example 2: Expedited review with escalation

User says: "Expedited policy doc review — need it within 24 hours"

Actions:
1. Quality gate: 5/6 PASSED (proceed)
2. Review type: expedited (24h)
3. Assign: Legal + PM lead
4. DM both with 24h deadline
5. After 24h: Legal completed, PM lead no response
6. Escalation: Slack reminder to PM lead
7. +24h: PM lead still unresponsive, escalate to manager
8. PM lead responds after escalation

Result: Review completed with escalation logged in audit trail

## Error Handling

| Error | Action |
|-------|--------|
| Document not found | Ask user for correct URL or title |
| Quality gate fails (<5/6) | Return quality feedback; do NOT proceed to review |
| Reviewer not found in Slack | Ask user for correct Slack handle; skip DM for unfound reviewer |
| Notion MCP unavailable | Fall back to Slack-only workflow; track in thread instead |
| All reviewers unresponsive | After full escalation cycle, notify author to proceed with available feedback |
| Review request already exists | Show existing request status; ask if user wants to create a new one |
