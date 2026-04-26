---
name: gws-email-reply
description: >-
  Compose and send email replies via Google Workspace CLI with AI-drafted
  responses, knowledge-based context retrieval, brand voice enforcement, and
  mandatory sentence polishing. Supports replying to specific emails by message
  ID, thread continuation, and batch reply to unread reply-needed emails. User
  identity: hyojung.han@thakicloud.co.kr. Use when the user asks to "reply to
  email", "answer this email", "이메일 답장", "메일 답장", "reply-email",
  "gws email reply", "이 메일에 답장해줘", "메일 답장 써줘", or wants to compose
  a reply to a specific Gmail message. Do NOT use for email triage without
  replies (use gmail-daily-triage), calendar-related email actions (use
  gws-calendar or smart-meeting-scheduler), Slack messaging (use
  kwp-slack-slack-messaging), auto-reply without human gate (use
  email-auto-reply), or sending new emails without a reply context (use
  gws-gmail directly).
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "comms-automation"
---
# GWS Email Reply

## Output language

Match the original email language for the reply body. When Korean is required, follow project norms: all user-visible reply text in natural Korean; technical terms in English where standard. This skill file is English.

AI-drafted email replies via Google Workspace CLI with context retrieval, brand voice, and mandatory sentence polishing.

## User Identity

```
Email: hyojung.han@thakicloud.co.kr
Display Name: Hyojung Han (use workspace-configured Korean display name in signatures when replying in Korean)
Organization: ThakiCloud
Default Language: Korean (English for technical terms)
```

## Composed Skills

| Skill | Role | Step |
|-------|------|------|
| `gws-gmail` | Read emails, send replies | 1, 7 |
| `recall` | Cross-session context retrieval | 3 |
| `cognee` | Knowledge graph for sender/topic context | 3 |
| `kwp-customer-support-response-drafting` | Response structure and tone templates | 4 |
| `kwp-brand-voice-brand-voice-enforcement` | Brand voice consistency | 4 |
| `sentence-polisher` | Grammar and sentence quality (MANDATORY) | 5 |
| `gmail-daily-triage` | Email classification patterns | 2 |
| `smart-meeting-scheduler` | Route meeting-related replies | 2 |

## Workflow

### Step 1: Fetch Target Email

**If message ID provided:**

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "MESSAGE_ID"}'
```

**If no message ID — list candidates:**

```bash
gws gmail +triage --max 5 --query 'is:unread'
```

Extract from the target email:
- `From` (sender email and name)
- `Subject`
- `To`, `Cc` (for reply-all decisions)
- `threadId` (for thread continuation)
- Body text (plain text preferred, strip HTML if needed)
- `Date` (for time-sensitive context — if >48 hours old, acknowledge the delay in the reply opening)

Present the email summary to the user and confirm which email to reply to if multiple candidates exist.

### Step 2: Classify Intent

Categorize the email using `gmail-daily-triage` classification patterns:

| Category | Action |
|----------|--------|
| reply-needed | Continue to Step 3 |
| FYI-only | Ask user: "This appears to be FYI — still want to reply?" |
| action-required | Continue; note required actions in draft |
| meeting-related | Suggest using `smart-meeting-scheduler`; continue if user insists |

### Step 3: Retrieve Context

Run two context queries in parallel:

**recall** — Search for prior session context about the sender or topic:
```
Search: "{sender name} {subject keywords}"
```

**cognee** — Query knowledge graph for:
- Sender history (prior exchanges, relationship)
- Related projects or decisions
- Relevant organizational context

If `cognee` is unavailable or returns empty, proceed with `recall`-only context. Note "limited context" in the draft metadata.

### Step 4: Draft Replies

Generate 2-3 reply options. Apply `kwp-customer-support-response-drafting` response structure for each:

**Draft A — Concise** (3-5 sentences)
- Acknowledgment (1 sentence)
- Core answer (1-2 sentences)
- Next step (1 sentence)

**Draft B — Detailed** (2-3 paragraphs)
- Acknowledgment + context
- Comprehensive response with supporting details
- Next steps with timeline
- Closing

**Draft C — Diplomatic** (for sensitive topics only; skip if not applicable)
- Empathetic acknowledgment
- Carefully worded position
- Constructive next steps
- Warm closing

For all drafts:
- Apply `kwp-brand-voice-brand-voice-enforcement` for ThakiCloud professional tone
- Match the language of the original email (Korean reply to Korean email, English to English)
- Include proper greeting matching the sender's formality level
- Sign off with the standard Korean business closing for this sender (name + formal closing) when replying in Korean, or "Best regards, Hyojung Han" in English
- Prepend "Re: " to subject if not already present
- **NEVER hallucinate facts**: only reference information present in the original email, recall context, or cognee results. If asked about pricing, features, or capabilities not found in context, defer politely in the reply language (Korean deferral equivalent of "I'll confirm and get back to you") instead of inventing details

### Step 5: Polish with sentence-polisher (MANDATORY)

This step MUST NOT be skipped. Run each draft through the `sentence-polisher` skill:

1. Read the `sentence-polisher` skill (`.cursor/skills/standalone/sentence-polisher/SKILL.md`)
2. Pass each draft with context: `purpose=email_reply`, `tone=<detected>`, `audience=<sender relationship>`
3. Apply all returned fixes
4. Preserve any `[REVIEW]` items to show the user

### Step 6: Present for Selection

Display all polished drafts with clear labels:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Replying to: {sender} — "{subject}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Draft A (Concise)
[polished text]
[change summary from polisher]

## Draft B (Detailed)
[polished text]
[change summary from polisher]

## Draft C (Diplomatic) — if applicable
[polished text]
[change summary from polisher]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Select a draft (A/B/C), edit, or request regeneration.
```

Wait for user selection. If the user edits, re-run `sentence-polisher` on the edited version before confirming.

### Step 7: Send

After user approval:

**Reply (recommended — auto-handles threading, In-Reply-To, References):**
```bash
gws gmail +reply \
  --message-id "MESSAGE_ID" \
  --body "APPROVED_REPLY_TEXT"
```

**Reply-all (when Cc recipients should be included — default when original email had Cc'd participants):**
```bash
gws gmail +reply-all \
  --message-id "MESSAGE_ID" \
  --body "APPROVED_REPLY_TEXT"
```

Use `--dry-run` to preview before actual send. Use `--cc` for additional recipients.

After successful send:
- Confirm to user: "Reply sent to {recipient}"
- If `cognee` is available, index the exchange for future context:
  - Add the reply content with sender/topic metadata

## Examples

### Example 1: Reply to a specific email

**User says:** "/reply-email 18e5a3b2c4d"

**Actions:**
1. Fetch message `18e5a3b2c4d` via `gws gmail users messages get`
2. Classify: reply-needed (question from colleague)
3. Recall finds prior discussion about the topic; cognee returns project context
4. Generate 2 drafts (Concise + Detailed) in Korean
5. Polish both with sentence-polisher (3 spacing fixes, 1 particle fix)
6. Present: user selects Draft A with minor edit
7. Re-polish edited version, send via `gws gmail +send`

### Example 2: Batch reply to unread emails

**User says:** "Summarize unread emails I still need to reply to"

**Actions:**
1. Fetch unread emails: `gws gmail +triage --max 5 --query 'is:unread'`
2. Filter to reply-needed (3 of 5 emails)
3. Process each sequentially: context → drafts → polish → present → send
4. Report: "3 replies sent, 2 emails skipped (FYI-only)"

### Example 3: Diplomatic reply to external partner

**User says:** "/reply-email --query 'from:partner@company.com' --tone diplomatic"

**Actions:**
1. Fetch latest email from partner@company.com
2. Classify: reply-needed (contract negotiation)
3. Context retrieval finds prior negotiation history
4. Generate 3 drafts including Diplomatic option
5. Polish all; sentence-polisher catches 2 tone misalignments
6. User selects Draft C (Diplomatic), sends

## Error Handling

| Error | Action |
|-------|--------|
| No target email specified | Show last 5 unread emails via `gws gmail +triage` and ask user to select |
| gws auth failure | Run `python3 ~/.config/gws/oauth2_manual.py` and clean caches (`rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`), then retry |
| Cognee unavailable | Proceed with recall-only context; add note to draft header |
| Recall returns no results | Proceed without prior context; draft from email content only |
| User rejects all drafts | Ask for specific feedback on tone/content, regenerate with adjustments |
| Send failure after approval | Retry once; if still failing, save as Gmail draft and notify user |
| Thread ID not found | Fall back to simple reply with "Re: " subject prefix |
| Very long email chain | Summarize the chain before drafting; focus reply on the latest message |
| Email has attachments | Acknowledge attachments in the reply language (e.g., confirm receipt without claiming review); do NOT claim to have read files that weren't extracted |
| Email contains URLs | Mention having reviewed the linked content only if actually fetched via defuddle/WebFetch |
