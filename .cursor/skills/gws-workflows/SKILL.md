---
name: gws-workflows
description: >-
  Cross-service Google Workspace productivity workflows via the gws CLI --
  daily standup reports, meeting preparation, weekly digests, email-to-task
  conversion, and file announcements. Use when the user asks for a standup
  summary, meeting prep, weekly digest, to convert email to a task, or to
  announce a file in Chat. Do NOT use for single-service operations (use
  gws-gmail, gws-calendar, gws-drive, gws-chat directly).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Google Workspace Workflows

Cross-service productivity workflows that combine Gmail, Calendar, Drive, Chat, and Tasks. Google Tasks is accessed through these workflow subcommands (no separate gws-tasks skill needed).

> **Prerequisites**: `gws` must be installed and authenticated. See `gws-workspace` skill.

## Standup Report

Generate a daily standup summary: today's meetings + open tasks.

```bash
gws workflow +standup-report
gws workflow +standup-report --format table
```

Combines Calendar agenda and Tasks data into a single standup view.

## Meeting Prep

Prepare for your next meeting: agenda, attendees, and linked docs.

```bash
gws workflow +meeting-prep
gws workflow +meeting-prep --calendar primary
```

| Flag | Default | Description |
|------|---------|-------------|
| `--calendar` | primary | Calendar to check |

Pulls the next upcoming event, lists attendees, extracts linked Drive documents from the event description, and summarizes everything.

## Weekly Digest

Generate a weekly summary: this week's meetings + unread email count.

```bash
gws workflow +weekly-digest
gws workflow +weekly-digest --format table
```

Best run on Monday mornings for weekly planning.

## Email to Task

Convert a Gmail message into a Google Tasks entry.

```bash
gws workflow +email-to-task --message-id <MSG_ID>
gws workflow +email-to-task --message-id MSG_ID --tasklist @default
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--message-id` | Yes | -- | Gmail message ID to convert |
| `--tasklist` | No | @default | Target task list |

Extracts subject and body from the email and creates a task with a link back to the original message.

> **Write command** -- confirm with the user before executing.

## File Announce

Announce a Drive file in a Google Chat space.

```bash
gws workflow +file-announce --file-id <FILE_ID> --space <SPACE>
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file-id` | Yes | -- | Drive file ID |
| `--space` | Yes | -- | Chat space name (e.g. `spaces/AAAAxxxx`) |
| `--message` | No | -- | Custom announcement text |
| `--format` | No | json | Output format |

Fetches file metadata from Drive and posts a formatted message to the Chat space.

> **Write command** -- confirm with the user before executing.

## Discovering Commands

```bash
gws workflow --help
```
