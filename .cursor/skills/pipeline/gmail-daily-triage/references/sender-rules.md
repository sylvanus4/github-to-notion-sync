# Sender Classification Rules

Rules for classifying emails by sender pattern. Evaluated in order; first match wins.

## Category A -- Spam

Classify as spam if sender matches ANY of these patterns.
**Never open the email body for spam classification.**

| Pattern | Match Type | Example |
|---------|-----------|---------|
| `noreply@` from unknown domains | Prefix + domain check | `noreply@marketing-spam.com` |
| `no-reply@` from unknown domains | Prefix + domain check | `no-reply@promo.xyz` |
| Promotional/marketing domains | Domain blocklist | See blocklist below |
| Subject contains unsubscribe-heavy patterns | Subject keyword | "Limited offer", "Act now" |

### Known Spam Domains (extend as needed)

```
marketing-cloud.com
mailchimp.com (if not subscribed)
sendinblue.com
```

### Trusted Domains (never classify as spam)

```
thakicloud.co.kr
bespinglobal.com
google.com
github.com
notion.so
slack.com
microsoft.com
```

## Category B -- Low Priority Notifications

| Sender Pattern | Service | Action |
|---------------|---------|--------|
| `*@mail.notion.so` | Notion | Move to Low Priority |
| `notify@mail.notion.so` | Notion | Move to Low Priority |
| `notifications@github.com` | GitHub | Move to Low Priority |
| `noreply@github.com` | GitHub | Move to Low Priority |
| `*@runpod.io` | RunPod | Move to Low Priority |
| `*@email.runpod.io` | RunPod | Move to Low Priority |
| `calendar-notification@google.com` | Google Calendar | Move to Low Priority |
| Snippet contains "수락", "거절" | Calendar RSVP | Move to Low Priority |
| Snippet contains "accepted", "declined" | Calendar RSVP | Move to Low Priority |

## Category C -- Bespin News

| Sender Pattern | Action |
|---------------|--------|
| `bespin_news@bespinglobal.com` | Extract links, Playwright fetch, compile .docx |

## Category D -- Company Colleagues

| Domain | Company | Tone | Action |
|--------|---------|------|--------|
| `@thakicloud.co.kr` | ThakiCloud | Team-casual | Summarize + draft reply |
| `@bespinglobal.com` | Bespin Global | Formal business | Summarize + draft reply |

Triggers for ALL emails from these domains (not just those with attachments).
If attachments exist, also download and summarize them.

## Category E -- Needs Reply

An email needs reply if ALL of these conditions are met:
1. User's email is in TO or CC headers
2. Sender is NOT in Category A or B
3. Thread has no reply from user (no sent messages in the thread)
4. Email is not purely informational (no-reply sender)
5. Not a calendar notification

## Category F -- Calendar Accepts/Declines

Subset of Category B. Detected by:
- Sender: `calendar-notification@google.com`
- OR subject/snippet containing calendar RSVP keywords
- Keywords: "수락", "거절", "초대", "accepted", "declined", "invitation"
