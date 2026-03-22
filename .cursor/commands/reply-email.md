---
description: "Reply to emails with AI-drafted responses via Google Workspace CLI"
---

## Reply Email

AI-drafted email replies with context retrieval, brand voice, and mandatory sentence polishing.

### Usage

```
/reply-email                         # show unread reply-needed emails
/reply-email <MESSAGE_ID>            # reply to specific email
/reply-email --query "from:boss"     # filter emails to reply to
/reply-email --tone diplomatic       # force diplomatic tone
/reply-email --lang ko               # force Korean reply
/reply-email --lang en               # force English reply
/reply-email --batch                 # process all unread reply-needed
```

### Workflow

1. **Fetch** target email(s) via gws-gmail
2. **Classify** intent and urgency
3. **Retrieve** context (recall + cognee)
4. **Generate** 2-3 reply drafts with brand voice
5. **Polish** all drafts with sentence-polisher (mandatory)
6. **Present** for user selection and approval
7. **Send** approved reply via gws-gmail

### Execution

Read and follow the `gws-email-reply` skill (`.cursor/skills/gws-email-reply/SKILL.md`) for the full pipeline, composed skills, and error handling.

### Examples

List unread emails and pick one to reply to:
```
/reply-email
```

Reply to a specific message by ID:
```
/reply-email 18e5a3b2c4d
```

Reply with a specific tone to a filtered email:
```
/reply-email --query "from:investor@vc.com" --tone diplomatic
```

Batch process all unread reply-needed emails:
```
/reply-email --batch
```

Force English reply regardless of original email language:
```
/reply-email 18e5a3b2c4d --lang en
```
