# Meeting Digest Slack Ship Template

Slack mrkdwn message templates and file upload script for posting meeting
digests to `#효정-할일` (ID: `C0AA8NT4T8T`).

## Prerequisites

- `SLACK_BOT_TOKEN` set in `.env` (format: `xoxb-...`)
- Bot has scopes: `files:write`, `chat:write`, `channels:read`
- Bot is a member of `#효정-할일`
- Slack MCP server (`plugin-slack-slack`) connected for text messages

## Thread Structure

```
#효정-할일
│
├── 📄 meeting-digest.docx + main summary (file upload, initial_comment)
│   ├── 📋 핵심 논의 사항 (thread reply, MCP text)
│   ├── ✅ 액션 아이템 대시보드 (thread reply, MCP text)
│   ├── 🔗 Drive 링크 + 다음 단계 (thread reply, MCP text, if --drive)
│   └── 📊 meeting-summary.pptx (thread reply, file upload, if --pptx)
```

## Step 1: Upload DOCX (Main Message)

Uses the 3-step Slack API file upload flow.

### Load Token

```bash
source .env
```

### Step A — Get upload URL

```bash
DOCX_PATH="output/meetings/{date}/{slug}/meeting-digest.docx"
FILE_SIZE=$(stat -f%z "$DOCX_PATH")
UPLOAD_RESP=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename=meeting-digest.docx&length=$FILE_SIZE")

UPLOAD_URL=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['file_id'])")
```

### Step B — Upload file

```bash
curl -s -X POST "$UPLOAD_URL" -F "file=@$DOCX_PATH"
```

### Step C — Complete and share

```bash
COMPLETE_RESP=$(curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"files\": [{\"id\": \"$FILE_ID\", \"title\": \"회의요약_{MEETING_TITLE}_{DATE}.docx\"}],
    \"channel_id\": \"C0AA8NT4T8T\",
    \"initial_comment\": \"*📄 회의 요약: {MEETING_TITLE}*\n_{MEETING_TYPE} | {DATE}_\n\n{ONE_LINE_SUMMARY}\"
  }")
echo "$COMPLETE_RESP"
```

### Extract Thread Timestamp

```bash
THREAD_TS=$(echo "$COMPLETE_RESP" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('ok'):
    for f in data.get('files', []):
        shares = f.get('shares', {})
        for scope in ['public', 'private']:
            channels = shares.get(scope, {})
            for ch_id, msgs in channels.items():
                if msgs:
                    print(msgs[0]['ts'])
                    sys.exit(0)
")
```

If extraction fails, use `slack_read_channel` MCP tool to find the latest
bot message in the channel.

## Step 2: Thread Reply — Key Discussion Points

Use MCP for text-only thread messages:

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_send_message",
  arguments={
    "channel_id": "C0AA8NT4T8T",
    "text": "<discussion-summary-mrkdwn>",
    "thread_ts": "<THREAD_TS>"
  }
)
```

### Message Template

```
*📋 핵심 논의 사항*

*1. {TOPIC_1_TITLE}*
{TOPIC_1_SUMMARY_2_3_LINES}

*2. {TOPIC_2_TITLE}*
{TOPIC_2_SUMMARY_2_3_LINES}

*3. {TOPIC_3_TITLE}*
{TOPIC_3_SUMMARY_2_3_LINES}

_총 {N}개 주제 논의 | 상세 내용은 첨부 문서 참조_
```

Max 4000 characters. If content exceeds this, truncate to the top 3-4
most important topics and add `_... 외 {N}건은 첨부 문서 참조_`.

## Step 3: Thread Reply — Action Items Dashboard

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_send_message",
  arguments={
    "channel_id": "C0AA8NT4T8T",
    "text": "<action-items-mrkdwn>",
    "thread_ts": "<THREAD_TS>"
  }
)
```

### Message Template

```
*✅ 액션 아이템 대시보드*

🔴 *긴급*
• {ACTION_ITEM} — 담당: {OWNER} | 마감: {DUE_DATE}
• {ACTION_ITEM} — 담당: {OWNER} | 마감: {DUE_DATE}

🟡 *높음*
• {ACTION_ITEM} — 담당: {OWNER} | 마감: {DUE_DATE}

🟢 *보통*
• {ACTION_ITEM} — 담당: {OWNER} | 마감: {DUE_DATE}

_총 {TOTAL}건 | 긴급 {N_URGENT}건 · 높음 {N_HIGH}건 · 보통 {N_NORMAL}건_
```

## Step 4: Thread Reply — Drive Link + Next Steps

Only posted when `--drive` was used. Otherwise, just post next steps.

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_send_message",
  arguments={
    "channel_id": "C0AA8NT4T8T",
    "text": "<drive-link-mrkdwn>",
    "thread_ts": "<THREAD_TS>"
  }
)
```

### Message Template (with Drive)

```
*🔗 문서 링크*

📁 Google Drive: <{DRIVE_DOCX_URL}|회의요약 DOCX>
{IF_PPTX: 📊 Google Drive: <{DRIVE_PPTX_URL}|프레젠테이션 PPTX>}

*📌 다음 단계*
1. {NEXT_STEP_1}
2. {NEXT_STEP_2}
3. {NEXT_STEP_3}

_다음 회의: {NEXT_MEETING_DATE_IF_KNOWN}_
```

### Message Template (without Drive)

```
*📌 다음 단계*
1. {NEXT_STEP_1}
2. {NEXT_STEP_2}
3. {NEXT_STEP_3}

_다음 회의: {NEXT_MEETING_DATE_IF_KNOWN}_
```

## Step 5: Thread Reply — Upload PPTX (Optional)

Only when `--pptx` was used. Uses the same 3-step upload flow with `thread_ts`.

```bash
PPTX_PATH="output/meetings/{date}/{slug}/meeting-summary.pptx"
FILE_SIZE=$(stat -f%z "$PPTX_PATH")
UPLOAD_RESP=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename=meeting-summary.pptx&length=$FILE_SIZE")
UPLOAD_URL=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['file_id'])")

curl -s -X POST "$UPLOAD_URL" -F "file=@$PPTX_PATH"

curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"files\": [{\"id\": \"$FILE_ID\", \"title\": \"회의요약_{MEETING_TITLE}_{DATE}.pptx\"}],
    \"channel_id\": \"C0AA8NT4T8T\",
    \"thread_ts\": \"$THREAD_TS\",
    \"initial_comment\": \"📊 프레젠테이션 슬라이드 — 회의 핵심 내용 요약\"
  }"
```

## Fallback: Text-Only Posting

If `SLACK_BOT_TOKEN` is not available, fall back to text-only posting using
the MCP `slack_send_message` tool only (no file uploads).

Post a main message + 3 threaded replies covering the same content, but
without file attachments. Include a warning:

```
⚠️ _SLACK_BOT_TOKEN이 설정되지 않아 파일 업로드를 건너뛰었습니다.
문서 파일은 로컬에 저장되어 있습니다: `output/meetings/{date}/{slug}/`_
```

## Error Handling

| Error | Response | Fix |
|-------|----------|-----|
| `invalid_auth` | Token invalid or expired | Check `SLACK_BOT_TOKEN` in `.env` |
| `channel_not_found` | Channel ID wrong | Verify `C0AA8NT4T8T` |
| `not_in_channel` | Bot not a member | Invite bot: `/invite @bot-name` in `#효정-할일` |
| `file_too_large` | File exceeds Slack limit | Compress or post Drive link only |
| Thread `ts` extraction fails | Malformed response | Use `slack_read_channel` MCP fallback |

## Character Limits

- Each Slack message: max 4000 characters
- `initial_comment` in file upload: max 4000 characters
- If content exceeds limit, truncate and add `_상세 내용은 첨부 문서 참조_`
- For very long meeting digests, prioritize:
  1. Top 3-4 discussion topics
  2. Top-priority action items
  3. Immediate next steps
