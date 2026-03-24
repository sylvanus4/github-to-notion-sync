# NotebookLM Slide Generation & Slack Distribution

Detailed instructions for Phase 6 (NLM slide generation) and Phase 7 (Slack
distribution) of the paper-review pipeline.

## Phase 6: NotebookLM Slide Generation

### Prerequisites

- `notebooklm-mcp` MCP server registered in `~/.cursor/mcp.json`
- Authenticated (`nlm login` or `refresh_auth` MCP tool)
- DOCX report from Phase 4 exists at `outputs/papers/{paper-id}-analysis-{DATE}.docx`
- Korean review markdown from Phase 2 available

### Step-by-Step

#### 6.1 Create Notebook

```
notebook_create(title="Paper Review: {Paper Title}")
```

Save the returned `notebook_id` for all subsequent calls.

#### 6.2 Add DOCX as Source

The DOCX contains the consolidated analysis — it becomes the primary source.

Use `notebook_add_text` with `file_path` to upload local files:

```
notebook_add_text(
  notebook_id=<notebook_id>,
  title="Paper Analysis Report",
  file_path="<WORKSPACE_ABSOLUTE_PATH>/outputs/papers/{paper-id}-analysis-{DATE}.docx"
)
```

**Critical**: Use the full absolute path (e.g., `/Users/hanhyojung/thaki/research/outputs/papers/...`).
The MCP server resolves paths from its own working directory, not the workspace.

#### 6.3 Add Review Markdown as Text Source

Adding the Korean review as a text source enriches slide content with detailed
analysis that may not be in the DOCX executive summary.

```
notebook_add_text(
  notebook_id=<notebook_id>,
  title="Korean Paper Review",
  content=<full review markdown content>
)
```

Alternatively, if the review is saved to a file:
```
notebook_add_text(
  notebook_id=<notebook_id>,
  title="Korean Paper Review",
  file_path="<WORKSPACE_ABSOLUTE_PATH>/outputs/papers/{paper-id}-review-{DATE}.md"
)
```

#### 6.4 Generate Slide Deck

```
slide_deck_create(
  notebook_id=<notebook_id>,
  format="detailed_deck",
  confirm=true
)
```

#### 6.5 Poll for Completion

```
studio_status(notebook_id=<notebook_id>)
```

Poll every 30 seconds. Typical generation time: **5-8 minutes** for
academic papers with rich source material. Max wait: 15 minutes.

If generation appears stuck after 15 minutes:
1. Check `studio_status` one more time
2. If still processing, the DOCX may be too large — try regenerating

#### 6.6 Download Slide PDF

After `studio_status` confirms generation is complete, download the slide deck
as a PDF using the `download_artifact` MCP tool:

```
download_artifact(
  notebook_id=<notebook_id>,
  artifact_type="slide_deck",
  output_path="<WORKSPACE_ABSOLUTE_PATH>/outputs/presentations/{paper-id}-nlm-slides-{DATE}.pdf"
)
```

**Critical**: Use the full absolute path. Verify the file was saved:

```bash
ls -la outputs/presentations/{paper-id}-nlm-slides-{DATE}.pdf
```

The downloaded PDF is uploaded to Slack in Phase 8. Do NOT share a notebook
link — always upload the PDF file directly.

---

## Phase 8: Slack Distribution

### Prerequisites

- `SLACK_BOT_TOKEN` set in `.env` (format: `xoxb-...`)
- Bot has scopes: `files:write`, `chat:write`, `channels:read`
- Bot is a member of the target channel
- Slack MCP server (`plugin-slack-slack`) connected for text messages

### Channel Resolution

Use the channel registry (fast path) or MCP search (fallback):

| Channel Name | Channel ID |
|---|---|
| `deep-research-trending` | `C0AN34G4QHK` |
| `research` | `C0A7GBRK2SW` |
| `press` | `C0A7NCP33LG` |
| `research-pr` | `C0A7FS8UC66` |

If the target channel is not in the registry:
```
slack_search_channels(query="<channel_name>")
```

### Step 8.1: Upload NLM Slides (Main Message)

Slack uses a 3-step upload flow (`files.upload` and `files.uploadV2` are deprecated):

1. `files.getUploadURLExternal` — get presigned upload URL + file_id
2. POST file to the presigned URL
3. `files.completeUploadExternal` — finalize and share to channel

Load the bot token:
```bash
source .env
```

**Step A — Get upload URL:**
```bash
FILE_SIZE=$(stat -f%z outputs/presentations/{paper-id}-nlm-slides-{DATE}.pdf)
UPLOAD_RESP=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename={paper-id}-nlm-slides.pdf&length=$FILE_SIZE")

UPLOAD_URL=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['file_id'])")
```

**Step B — Upload file:**
```bash
curl -s -X POST "$UPLOAD_URL" \
  -F "file=@outputs/presentations/{paper-id}-nlm-slides-{DATE}.pdf"
```

**Step C — Complete and share:**
```bash
COMPLETE_RESP=$(curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"files\": [{\"id\": \"$FILE_ID\", \"title\": \"📑 {Paper Title} - NLM Slide Deck\"}],
    \"channel_id\": \"<CHANNEL_ID>\",
    \"initial_comment\": \"*📄 논문 리뷰: {Paper Title}*\n{2-3 sentence Korean summary}\"
  }")
echo "$COMPLETE_RESP"
```

#### Extract Thread Timestamp

The response JSON contains file share info. Extract the `ts` for threading:

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

If the extraction fails, use `slack_read_channel` MCP tool to find the latest
message from the bot in the channel.

### Step 8.2: Thread Reply — Paper Summary

Use the Slack MCP tool for text-only thread replies:

```
slack_send_message(
  channel_id="<CHANNEL_ID>",
  thread_ts="<THREAD_TS>",
  message="*📋 논문 핵심 내용 요약*\n\n<detailed Korean summary>\n\n• 주요 기여 1\n• 주요 기여 2\n• 주요 기여 3\n\n*방법론*: <brief methodology>\n*결과*: <key results>\n*시사점*: <implications>"
)
```

The summary should be 500-1000 characters. Include:
- Key contributions (numbered)
- Core methodology
- Main results with numbers
- Practical implications

### Step 8.3: Thread Reply — Notion Link

Post the Notion main page URL from Phase 7 in the thread. Skip if
`--skip-notion` was used.

```
slack_send_message(
  channel_id="<CHANNEL_ID>",
  thread_ts="<THREAD_TS>",
  message="*📚 Notion 분석 페이지*\n\n논문 리뷰 및 PM 분석 전문은 아래 Notion 페이지에서 확인하세요:\n<NOTION_PAGE_URL>\n\n포함된 분석:\n• 논문 리뷰 (상세 8개 섹션)\n• PM 전략 분석 (SWOT, Lean Canvas)\n• 시장 조사 (TAM/SAM/SOM)\n• Product Discovery\n• GTM 분석\n• 통계·방법론 리뷰\n• 실행 계획"
)
```

Replace `<NOTION_PAGE_URL>` with the URL captured from Phase 7
(format: `https://www.notion.so/{page_id_without_dashes}`).

### Step 8.4: Thread Reply — Upload DOCX

Use the same 3-step upload flow, but with `thread_ts`:

```bash
FILE_SIZE=$(stat -f%z outputs/papers/{paper-id}-analysis-{DATE}.docx)
UPLOAD_RESP=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename={paper-id}-analysis.docx&length=$FILE_SIZE")
UPLOAD_URL=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['file_id'])")

curl -s -X POST "$UPLOAD_URL" -F "file=@outputs/papers/{paper-id}-analysis-{DATE}.docx"

curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"files\": [{\"id\": \"$FILE_ID\", \"title\": \"📝 Full Analysis Report (DOCX)\"}],
    \"channel_id\": \"<CHANNEL_ID>\",
    \"thread_ts\": \"$THREAD_TS\",
    \"initial_comment\": \"전체 분석 리포트 (DOCX) - 논문 리뷰 + PM 분석 + 통계 리뷰 포함\"
  }"
```

### Step 8.5: Thread Reply — Upload PPTX (Last)

Same 3-step flow for the Anthropic PPTX:

```bash
FILE_SIZE=$(stat -f%z outputs/presentations/{paper-id}-presentation-{DATE}.pptx)
UPLOAD_RESP=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename={paper-id}-presentation.pptx&length=$FILE_SIZE")
UPLOAD_URL=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['file_id'])")

curl -s -X POST "$UPLOAD_URL" -F "file=@outputs/presentations/{paper-id}-presentation-{DATE}.pptx"

curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"files\": [{\"id\": \"$FILE_ID\", \"title\": \"📊 Anthropic PPTX Presentation\"}],
    \"channel_id\": \"<CHANNEL_ID>\",
    \"thread_ts\": \"$THREAD_TS\",
    \"initial_comment\": \"프레젠테이션 (PPTX) - PptxGenJS 기반 상세 슬라이드\"
  }"
```

### Error Handling

| Error | Response | Fix |
|-------|----------|-----|
| `invalid_auth` | Token invalid or expired | Check `SLACK_BOT_TOKEN` in `.env` |
| `channel_not_found` | Channel ID wrong | Use `slack_search_channels` to find correct ID |
| `not_in_channel` | Bot not a member | Invite bot to channel: `/invite @bot-name` |
| `file_too_large` | File exceeds Slack limit | Compress or split; Slack free tier: 5GB total storage |
| Thread `ts` extraction fails | Malformed response | Fall back to reading channel history via MCP |

### Thread Structure Recap

```
#research channel
│
├── 📑 NLM Slides PDF + main summary (initial_comment)
│   ├── 📋 논문 핵심 내용 요약 (thread reply, MCP text)
│   ├── 📚 Notion 분석 페이지 링크 (thread reply, MCP text)
│   ├── 📝 Full Analysis DOCX (thread reply, curl upload)
│   └── 📊 Anthropic PPTX (thread reply, curl upload)
```

### Slack API Reference

File upload uses a 3-step flow (both `files.upload` and `files.uploadV2` are deprecated):

1. `files.getUploadURLExternal` — get presigned URL + file_id
2. POST file content to the presigned URL
3. `files.completeUploadExternal` — finalize and share to channel/thread

Required bot scopes:
- `files:write` — upload files
- `chat:write` — post messages (used by MCP `slack_send_message`)
- `channels:read` — list public channels (used by MCP `slack_search_channels`)

Rate limits: ~20 requests per minute for file uploads. Sufficient for this pipeline.
