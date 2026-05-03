---
name: proactive-meeting-scheduler
description: >-
  Detect implicit meeting requests in emails ("let's discuss", "can we sync",
  "need to talk about") and proactively propose meetings with context-derived
  agendas. Runs after gmail-daily-triage to identify emails that imply a
  meeting is needed. Use when the user asks to "detect meeting needs from
  email", "auto-schedule from inbox", "proactive meeting", "이메일에서 미팅 감지", "자동
  미팅 제안", "proactive-meeting-scheduler", or wants meetings proposed from email
  context. Do NOT use for explicit meeting scheduling requests (use
  smart-meeting-scheduler), calendar management (use gws-calendar), or email
  triage without meetings (use gmail-daily-triage).
---

# Proactive Meeting Scheduler

Scan processed emails for implicit meeting signals and automatically propose meetings with agendas derived from email context.

## When to Use

- After `gmail-daily-triage` completes — scan reply-needed emails for meeting signals
- As part of the Comms track in the daily pipeline
- When the user wants the system to detect meeting needs autonomously

## Meeting Signal Detection

### Explicit Signals (high confidence)
- "Let's schedule a meeting"
- "Can we set up a call?"
- "I'd like to discuss this in person"
- "Let's sync on this"

### Implicit Signals (medium confidence)
- "We need to talk about..."
- "Can you walk me through..."
- "I have concerns about..."
- "This needs more discussion"
- Long email thread (> 5 replies) without resolution

### Korean Signals
- "미팅을 잡아주세요"
- "한번 얘기해 봐요"
- "회의가 필요할 것 같습니다"
- "논의가 필요합니다"
- "통화 가능하신가요"

## Workflow

### Step 1: Scan Triage Results

Read the output of `gmail-daily-triage` — specifically the "reply-needed" emails:

```bash
gws gmail list --label reply-needed --after yesterday --format json
```

### Step 2: Detect Meeting Signals

For each reply-needed email, analyze with LLM:
- Does this email imply a meeting is needed?
- Who should attend? (extract from To, CC, and mentioned names)
- What is the topic? (extract from subject and body)
- What is the urgency? (immediate, this week, next week)
- Confidence score: 0.0 - 1.0

Filter: Only propose meetings for confidence >= 0.7.

### Step 3: Extract Meeting Context

From the email thread, extract:
- **Topic**: Main subject of discussion
- **Background**: Key points from the email chain
- **Decision needed**: What outcome is expected
- **Pre-read materials**: Any links or attachments mentioned
- **Participants**: All relevant parties from the thread

### Step 4: Generate Agenda

Create a structured agenda from email context:

```
Meeting: <Topic from email subject>
Duration: 30 minutes (default)
Context: <1-2 sentence summary of email thread>

Agenda:
1. Background review (5 min)
   - <key point from email>
2. Discussion: <main topic> (15 min)
   - <specific question from email>
3. Decision and next steps (10 min)

Pre-read:
- Email thread: <link or message ID>
- <any attachments or links mentioned>
```

### Step 5: Find Available Slots

Use `gws-calendar` to check availability:
- Check all participants' calendars for next 3 business days
- Prefer 30-minute slots
- Avoid early morning (before 9:00) and late afternoon (after 17:00)
- Prefer gaps between existing meetings

### Step 6: Propose via Slack

Post meeting proposals to the user's Slack channel for approval:

```
🗓️ Meeting proposal detected from email

From: john@company.com
Subject: API Migration Timeline
Signal: "We need to discuss the migration plan"
Confidence: 0.85

Proposed meeting:
  Topic: API Migration Timeline Discussion
  Participants: You, John, Sarah
  Suggested slot: Tomorrow 10:00-10:30
  Agenda: [auto-generated from email]

React ✅ to schedule, 📝 to edit agenda, ❌ to skip
```

### Step 7: Schedule on Approval

If user approves (✅ reaction or explicit confirmation):
1. Create calendar event via `gws-calendar`
2. Send calendar invite to all participants
3. Attach agenda to the event
4. Draft a reply to the original email confirming the meeting

## Output

```
Proactive Meeting Report
========================
Emails Scanned: 12 (reply-needed)
Meeting Signals Detected: 3
Meetings Proposed: 2 (1 below confidence threshold)

Proposals:
1. API Migration Timeline — john@, sarah@ → Tomorrow 10:00
   Signal: "We need to discuss" | Confidence: 0.85
2. Q2 Budget Review — finance@, cto@ → Wed 14:00
   Signal: "Let's sync on the numbers" | Confidence: 0.78

Skipped (low confidence):
1. "Quick question about deploy" — Confidence: 0.45 (likely just needs a reply)
```

## Error Handling

| Error | Action |
|-------|--------|
| Gmail API auth failure | Run `python ~/.config/gws/oauth2_manual.py && rm ~/.config/gws/token_cache.json credentials.enc 2>/dev/null`; verify with `gws gmail +triage --max 1` |
| No reply-needed emails found | Exit cleanly with "no meeting signals to process"; no Slack post |
| Calendar availability check fails | Propose meeting without specific slot; ask user to pick time manually |
| Recipient email not found | Skip that proposal; log missing participant; continue with other emails |
| Meeting proposal rejected by user | Log rejection; do not create calendar event; optionally draft "decline" reply for user review |

## Examples

### Example 1: Morning email scan
Automated trigger: After gmail-daily-triage
Actions:
1. Scan reply-needed emails for meeting signals
2. Generate agendas from email context
3. Find available time slots
4. Post proposals to Slack
Result: Meeting proposals ready for user approval

### Example 2: Manual trigger
User says: "Check if any emails need meetings"
Actions:
1. Scan recent inbox for meeting signals
2. Present findings with confidence scores
3. Allow user to approve/decline each proposal
Result: Curated list of meeting-worthy emails
