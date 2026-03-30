---
name: slack-orphan-cleaner
description: >-
  Delete orphaned Slack thread replies where the parent message has been deleted
  but reply messages remain. Scans registered channels (#press, #deep-research,
  #ai-coding-radar, #idea, #prompt, #deep-research-trending, #research) or a custom channel, runs dry-run first, then
  executes deletion using SLACK_USER_TOKEN. Use when the user asks to "clean
  orphaned threads", "delete orphan replies", "Slack cleanup", "slack thread
  cleanup", "고아 쓰레드 삭제", "슬랙 고아 정리", "삭제된 메시지 쓰레드 정리",
  "orphaned thread cleanup", "slack-orphan-cleaner", or when invoked by the
  google-daily pipeline. Do NOT use for general Slack messaging (use
  kwp-slack-slack-messaging). Do NOT use for channel management or Slack bot
  development (use slack-agent). Do NOT use for Slack search (use
  kwp-slack-slack-search).
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# slack-orphan-cleaner

## Prerequisites

- `SLACK_USER_TOKEN` (xoxp-...) in `.env` — required for deleting messages posted by other users/bots
- `SLACK_BOT_TOKEN` (xoxb-...) in `.env` — used for reading channel history
- `requests` Python package installed

## Channel Registry

| Channel | ID |
|---|---|
| #press | `C0A7NCP33LG` |
| #deep-research | `C0A6X68LTN1` |
| #ai-coding-radar | `C0A7K3TBPK7` |
| #idea | `C0A6U3HE3GS` |
| #prompt | `C0A98HXSVMK` |
| #deep-research-trending | `C0AN34G4QHK` |
| #research | `C0A7GBRK2SW` |

## Workflow

### Step 1 — Dry-run

Source environment variables and run in dry-run mode to see what would be deleted:

```bash
set -a && source .env && set +a
python backend/scripts/cleanup_orphaned_threads.py
```

Optionally target specific channels:

```bash
python backend/scripts/cleanup_orphaned_threads.py --channels press,idea
```

### Step 2 — Review

Present the dry-run output to the user. Show:
- Number of orphaned threads per channel
- Total reply messages that would be deleted
- Any channels with zero orphans (skip confirmation for those)

### Step 3 — Execute

After user confirmation, run with `--execute`:

```bash
set -a && source .env && set +a
python backend/scripts/cleanup_orphaned_threads.py --execute
```

Report per-channel and aggregate results (deleted, failed counts).

## Integration Mode (google-daily)

When invoked as part of the `google-daily` pipeline, skip the dry-run/confirmation cycle and auto-execute with JSON output:

```bash
set -a && source .env && set +a
python backend/scripts/cleanup_orphaned_threads.py --execute --json
```

Parse the JSON output and include a one-line summary in the Slack notification thread:
`Orphan cleanup: {deleted} deleted, {failed} failed across {N} channels`

This phase is non-blocking — failures are logged but do not fail the pipeline.

## CLI Reference

```
--execute          Actually delete (default: dry-run)
--channels NAME    Comma-separated channel names (default: all registered)
--channel-id ID    Ad-hoc single channel ID (overrides --channels)
--json             JSON summary to stdout (suppresses human-readable output)
```

## Error Handling

- `cant_delete_message` errors (Slackbot or other bot messages) are logged and skipped — processing continues
- API rate limits are handled with a 1.2s pause between requests
- Channel access errors are logged per-channel; other channels continue processing
- Missing tokens cause an immediate exit with a clear error message

## Examples

### Example 1: User requests orphan cleanup

User says: "슬랙 고아 쓰레드 정리해줘"

Actions:
1. Source `.env` and run dry-run across all 7 channels
2. Present per-channel orphan counts to user
3. After user confirms, run with `--execute`
4. Report deleted/failed counts

### Example 2: Pipeline integration (google-daily Phase 6)

Invoked automatically at the end of `/google`:
1. Run `--execute --json` without user confirmation
2. Parse JSON output
3. Post one-line summary to Slack thread: `Orphan cleanup: 12 deleted, 1 failed across 7 channels`

### Example 3: Target specific channel

User says: "deep-research 채널만 고아 정리해"

Actions:
1. Run `--channels deep-research` in dry-run
2. Present results, confirm
3. Run `--channels deep-research --execute`

## Output

Per-channel summary includes: orphaned threads found, total replies, deleted count, failed count. Aggregate totals are printed at the end.
