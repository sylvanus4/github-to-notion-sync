---
name: kwp-slack-slack-search
description: >-
  Guidance for effectively searching Slack to find messages, files, channels,
  and people. Do NOT use for tasks outside the slack domain. Korean triggers:
  "슬랙 검색", "메시지 찾기".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Slack Search

This skill provides guidance for effectively searching Slack to find messages, files, and information.

## Search Tools Overview

| Tool | Use When |
|------|----------|
| `slack_search_public` | Searching public channels only. Does not require user consent. |
| `slack_search_public_and_private` | Searching all channels including private, DMs, and group DMs. Requires user consent. |
| `slack_search_channels` | Finding channels by name or description. |
| `slack_search_users` | Finding people by name, email, or role. |

## Search Strategy

### Start Broad, Then Narrow

1. Begin with a simple keyword or natural language question.
2. If too many results, add filters (`in:`, `from:`, date ranges).
3. If too few results, remove filters and try synonyms or related terms.

### Choose the Right Search Mode

- **Natural language questions** (e.g., "What is the deadline for project X?") — Best for fuzzy, conceptual searches where you don't know exact keywords.
- **Keyword search** (e.g., `project X deadline`) — Best for finding specific, exact content.

### Use Multiple Searches

Don't rely on a single search. Break complex questions into smaller searches:
- Search for the topic first
- Then search for specific people's contributions
- Then search in specific channels

## Search Modifiers Reference

### Location Filters
- `in:channel-name` — Search within a specific channel
- `in:<#C123456>` — Search in channel by ID
- `-in:channel-name` — Exclude a channel
- `in:<@U123456>` — Search in DMs with a user

### User Filters
- `from:<@U123456>` — Messages from a specific user (by ID)
- `from:username` — Messages from a user (by Slack username)
- `to:me` — Messages sent directly to you

### Content Filters
- `is:thread` — Only threaded messages
- `has:pin` — Pinned messages
- `has:link` — Messages containing links
- `has:file` — Messages with file attachments
- `has::emoji:` — Messages with a specific reaction

### Date Filters
- `before:YYYY-MM-DD` — Messages before a date
- `after:YYYY-MM-DD` — Messages after a date
- `on:YYYY-MM-DD` — Messages on a specific date
- `during:month` — Messages during a specific month (e.g., `during:january`)

### Text Matching
- `"exact phrase"` — Match an exact phrase
- `-word` — Exclude messages containing a word
- `wild*` — Wildcard matching (minimum 3 characters before `*`)

## File Search

To search for files, use the `content_types="files"` parameter with type filters:
- `type:images` — Image files
- `type:documents` — Document files
- `type:pdfs` — PDF files
- `type:spreadsheets` — Spreadsheet files
- `type:canvases` — Slack Canvases

Example: `content_types="files" type:pdfs budget after:2025-01-01`

## Following Up on Results

After finding relevant messages:
- Use `slack_read_thread` to get the full thread context for any threaded message.
- Use `slack_read_channel` with `oldest`/`latest` timestamps to read surrounding messages for context.
- Use `slack_read_user_profile` to identify who a user is when their ID appears in results.

## Common Pitfalls

- **Boolean operators don't work.** `AND`, `OR`, `NOT` are not supported. Use spaces (implicit AND) and `-` for exclusion.
- **Parentheses don't work.** Don't try to group search terms with `()`.
- **Search is not real-time.** Very recent messages (last few seconds) may not appear in search results. Use `slack_read_channel` for the most recent messages.
- **Private channel access.** Use `slack_search_public_and_private` when you need to include private channels, but note this requires user consent.

## Examples

### Example 1: Typical request

**User says:** "I need help with slack slack search"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |