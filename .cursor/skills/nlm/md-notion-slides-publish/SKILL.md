---
name: md-notion-slides-publish
description: >-
  End-to-end pipeline that publishes a local markdown file to Notion, generates
  dual-audience NotebookLM slide decks (elementary + Steve Jobs white-bg expert),
  downloads both PDFs, uploads them to Google Drive, and posts a consolidated
  summary with all links and key content to Slack #효정-할일. Orchestrates
  md-to-notion, notebooklm, notebooklm-studio, gws-drive, and Slack MCP.
  Use when the user asks to "publish markdown to Notion and slides",
  "마크다운 노션 슬라이드 발행", "md-notion-slides-publish", "노션 올리고 슬라이드 만들어줘",
  "마크다운 노션 + NLM 슬라이드 + 드라이브 + 슬랙", "전체 퍼블리시 파이프라인",
  "마크다운 올리고 발표자료 만들어", "노션이랑 슬라이드 한번에",
  "노션에 올리고 발표 슬라이드도 만들어줘", "문서 퍼블리시 풀 파이프라인",
  or any request to convert a markdown file into Notion pages AND NotebookLM
  slides AND distribute to Drive + Slack in one pipeline.
  Do NOT use for Notion upload only (use md-to-notion).
  Do NOT use for slides only without Notion (use nlm-dual-slides).
  Do NOT use for ad-hoc studio_create on existing notebooks (use notebooklm-studio).
  Do NOT use for single-audience slides (use nlm-slides).
  Do NOT use for Google Drive upload only (use gws-drive directly).
metadata:
  author: "thaki"
  version: "1.3.0"
  category: "pipeline"
  composedSkills:
    - md-to-notion
    - notebooklm
    - notebooklm-studio
    - gws-drive
    - plugin-slack-slack
---

# MD → Notion + Slides Publish Pipeline

One command transforms a local markdown file into:

1. A structured Notion sub-page
2. Two NotebookLM slide decks (elementary + Steve Jobs white-background expert)
3. Google Drive–hosted PDFs
4. A consolidated Slack report in **#효정-할일** with every link and a key summary

---

## State Variables

Track these across all phases. Every phase MUST capture its outputs before proceeding.

| Variable | Set in | Used in | Description |
|----------|--------|---------|-------------|
| `$TITLE` | Phase 1 | All | H1 title extracted from markdown |
| `$NOTION_URL` | Phase 1 | Phase 7 | Full Notion page URL |
| `$NOTION_PAGE_ID` | Phase 1 | Phase 7 | Notion page ID |
| `$EXPERT_NOTEBOOK_ID` | Phase 3 | Phase 4, 7 | NLM notebook ID for expert slides |
| `$ELEMENTARY_NOTEBOOK_ID` | Phase 3 | Phase 4, 7 | NLM notebook ID for elementary slides |
| `$EXPERT_DRIVE_URL` | Phase 5 | Phase 7 | Google Drive link for expert slides |
| `$ELEMENTARY_DRIVE_URL` | Phase 5 | Phase 7 | Google Drive link for elementary slides |

---

## Inputs

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `file` | **Yes** | — | Path to the local `.md` file |
| `notion_parent` | No | — | Notion parent page ID. If omitted, ask the user |
| `drive_folder` | No | — | Google Drive folder name or ID. If omitted, upload to root |
| `slack_channel` | No | `C0AA8NT4T8T` | Slack channel ID (`#효정-할일`) |
| `slide_format` | No | `pdf` | Output format for NLM slides: `pdf` (default) or `pptx` |

---

## Pipeline Phases

### Phase 1 — Notion Upload

Publish the markdown file as a Notion sub-page using the **md-to-notion** workflow.

1. Read the markdown file and extract the H1 title (first `# ` line). If no H1, use the filename without extension.
2. Run `scripts/convert_tables.py` on the file to convert pipe tables to Notion-compatible `<table>` HTML blocks. If the script is unavailable, skip this step.
3. If the file exceeds 15 KB, split into sub-sections at `## ` boundaries.
4. Create Notion page(s) — **token-first**:
   - **Primary**: Use `scripts/notion_api.py` (`NotionClient.create_page()`) with
     `NOTION_TOKEN` from `.env`
   - **Fallback**: Use **plugin-notion-workspace-notion** MCP `notion-create-pages`
     when `NOTION_TOKEN` is not available
   - `title`: the H1 title
   - `parent`: `{"page_id": "<notion_parent>"}`
   - `content_markdown`: the converted markdown content
5. Capture the returned `page_id` and construct the Notion URL: `https://www.notion.so/<page_id_without_hyphens>`
6. Store `$NOTION_URL` and `$NOTION_PAGE_ID` for later use.

### Phase 2 — Content Rewrite (Dual Audience)

Transform the original markdown into two audience-tailored documents for NotebookLM ingestion. Each rewrite is a COMPLETE document — not a diff or patch.

**Expert version (Steve Jobs white-background style):**
- Read [references/expert-prompt.md](references/expert-prompt.md) FIRST — it defines the full rewrite rules
- For EACH `## ` section in the original markdown:
  1. Write a Korean version: authoritative, data-driven, natural Korean business tone, one core insight per section
  2. Add `[Visual: ...]` annotations describing the ideal diagram, chart, or table
- Style constraints: white background mandatory, no decorative elements, bold metrics, active voice
- Steve Jobs principles: one idea per slide, dramatic reveals, concrete metaphors

**Elementary version:**
- Read [references/elementary-prompt.md](references/elementary-prompt.md) FIRST — it defines the full rewrite rules
- For EACH `## ` section in the original markdown:
  1. Write a Korean version: playful tone with 존댓말, analogies to school/games/cooking
  2. Add `[Visual: ...]` annotations with colorful icons and character suggestions
- Style constraints: max 15 words per sentence, 2-3 bullets per section, NO equations, NO jargon, NO acronyms

**Save both rewrites as temporary files in the same directory as the source file:**
- `_expert_rewrite.md`
- `_elementary_rewrite.md`

**Anti-pattern:** Do NOT feed the original markdown directly to NotebookLM without rewriting. NLM produces generic slides from raw markdown — the rewrite step is what makes the two versions distinct and high-quality.

### Phase 3 — NotebookLM Notebook Creation & Source Upload

Create two separate NotebookLM notebooks via **user-notebooklm-mcp** MCP and upload the rewritten content.

1. **Expert notebook:**
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="notebook_create",
     arguments={"title": "$TITLE — Expert Slides"})
   ```
   Capture `notebook_id` from the response → store as `$EXPERT_NOTEBOOK_ID`
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="source_add",
     arguments={"notebook_id": "$EXPERT_NOTEBOOK_ID", "source_type": "text",
                "text": "<full content of _expert_rewrite.md>"})
   ```

2. **Elementary notebook:**
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="notebook_create",
     arguments={"title": "$TITLE — Elementary Slides"})
   ```
   Capture `notebook_id` → store as `$ELEMENTARY_NOTEBOOK_ID`
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="source_add",
     arguments={"notebook_id": "$ELEMENTARY_NOTEBOOK_ID", "source_type": "text",
                "text": "<full content of _elementary_rewrite.md>"})
   ```

**Anti-pattern:** Do NOT create a single notebook with both versions as sources — each audience needs its own isolated notebook so NLM generates focused slides.

### Phase 4 — Slide Generation & Download

Generate slide decks from both notebooks and download them. Run both generations in parallel when possible.

1. **Expert slides — create:**
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="studio_create",
     arguments={"notebook_id": "$EXPERT_NOTEBOOK_ID", "artifact_type": "slides", "language": "ko"})
   ```

2. **Elementary slides — create:**
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="studio_create",
     arguments={"notebook_id": "$ELEMENTARY_NOTEBOOK_ID", "artifact_type": "slides", "language": "ko"})
   ```

3. **Poll both for completion.** Check `studio_status` every 15 seconds, max 20 attempts (5 minutes). If not complete after 5 minutes, report timeout with notebook IDs.

4. **Download both:**
   ```
   CallMcpTool(server="user-notebooklm-mcp", toolName="download_artifact",
     arguments={"notebook_id": "$EXPERT_NOTEBOOK_ID", "artifact_type": "slides"})
   CallMcpTool(server="user-notebooklm-mcp", toolName="download_artifact",
     arguments={"notebook_id": "$ELEMENTARY_NOTEBOOK_ID", "artifact_type": "slides"})
   ```

5. Locate downloaded files (typically `~/Downloads/` or the path returned by `download_artifact`).
   Rename files for clarity using Shell tool:
   - `$TITLE-expert-slides.pdf`
   - `$TITLE-elementary-slides.pdf`

**Anti-pattern:** Do NOT poll `studio_status` with no wait between calls — you will hit rate limits. Always sleep 15 seconds between status checks.

### Phase 5 — Google Drive Upload

Upload both slide files to Google Drive via gws CLI.

```bash
gws drive +upload "$TITLE-expert-slides.pdf"
```
Capture the file URL from the CLI output → store as `$EXPERT_DRIVE_URL`.

```bash
gws drive +upload "$TITLE-elementary-slides.pdf"
```
Capture the file URL from the CLI output → store as `$ELEMENTARY_DRIVE_URL`.

**Note:** `gws drive +upload` does NOT support `--folder` flag. Files upload to the root of My Drive. If `drive_folder` input was specified, report that manual folder move is needed after upload.

**Fallback:** If `gws` upload fails, report local file paths for manual upload and continue to Phase 6.

### Phase 6 — Key Summary Extraction

Before posting to Slack, extract a concise summary from the original markdown:

1. Read the original markdown file
2. Extract:
   - **Title** (H1)
   - **3-5 key points** (most important findings, conclusions, or action items)
   - **Total section count** for context

Format the summary as a bullet list in Korean.

### Phase 7 — Slack Consolidated Report

Post a single consolidated message to `#효정-할일` (`C0AA8NT4T8T`) via **plugin-slack-slack** MCP.

```
python3 scripts/slack_post_message.py --channel C0AA8NT4T8T --message "<main message>"
```

Capture the `ts` from the response for the thread reply.

**Main message template (Slack mrkdwn format):**

```
📋 *$TITLE — 퍼블리시 완료*

*📌 핵심 요약*
• [Key point 1 — Korean]
• [Key point 2 — Korean]
• [Key point 3 — Korean]

*🔗 링크*
• Notion: <$NOTION_URL>
• Expert 슬라이드 (Drive): <$EXPERT_DRIVE_URL>
• Elementary 슬라이드 (Drive): <$ELEMENTARY_DRIVE_URL>

*📊 생성 산출물*
• Notion 페이지 1건
• Expert 슬라이드 (Steve Jobs 스타일) 1건
• Elementary 슬라이드 (초등학생 버전) 1건
```

**Thread reply** with detailed metadata:

```
python3 scripts/slack_post_message.py --channel C0AA8NT4T8T --thread-ts <main_message_ts> --message "
             "text": "<detail message>"})
```

```
*상세 정보*
• 원본 파일: [source file path]
• Notion 부모 페이지: [parent page title or ID]
• Drive 폴더: [folder info or "My Drive root"]
• Expert NLM 노트북 ID: $EXPERT_NOTEBOOK_ID
• Elementary NLM 노트북 ID: $ELEMENTARY_NOTEBOOK_ID
• 슬라이드 형식: pdf
```

**Anti-pattern:** Do NOT use `useToast()` or `showToast()` for Slack posting — use `python3 scripts/slack_post_message.py` directly.

---

## Error Handling

| Phase | Failure | Action |
|-------|---------|--------|
| 1 | Notion upload fails | Retry once. If still fails, report error and continue with remaining phases |
| 2 | Rewrite generation fails | Use original markdown content as fallback for NLM upload |
| 3 | Notebook creation fails | Stop pipeline and report — NLM is required for slides |
| 4 | Slide generation times out | Report timeout, provide notebook IDs for manual retry |
| 5 | Drive upload fails | Report error with local file paths for manual upload |
| 6 | Summary extraction fails | Use H1 title + first 3 `## ` headings as fallback summary |
| 7 | Slack post fails | Print the message content to terminal as fallback |

---

## Cleanup

After successful Slack posting, delete temporary rewrite files:
- `_expert_rewrite.md`
- `_elementary_rewrite.md`

Do NOT delete downloaded slide files — the user may need them.

---

## Constraints

- All Slack messages in Korean (links, titles, and technical terms may be English)
- Notion page title uses the original H1 heading verbatim
- Expert slides: Steve Jobs principles — one idea per slide, **white background mandatory**, minimal text, bold data-driven visuals
- Elementary slides: playful, icon-rich, colorful — max 15 words per sentence, no jargon
- Report progress after each phase (e.g., "Phase 1 완료: Notion URL 확보")
- NotebookLM MCP server: `user-notebooklm-mcp` — requires absolute paths for local file sources
- `gws drive +upload` is the correct upload subcommand — `--folder` flag is NOT supported
- Slack channel `#효정-할일` ID is `C0AA8NT4T8T` — never send to DM
- Every phase MUST capture its state variables before proceeding to the next phase
- Do NOT skip the content rewrite phase — raw markdown produces poor NLM slides

---

## Examples

**Example 1 — Basic usage**

```
User: "docs/vc-pitch-v3/research/mac-mini-agent-sandbox-economics.md 를
      노션에 올리고 슬라이드 두 버전 만들어서 드라이브에 올리고 슬랙에 알려줘"

Agent:
1. Read file → $TITLE = "Mac Mini Agent Sandbox Economics"
2. md-to-notion → $NOTION_URL = https://notion.so/abc123
3. Dual rewrite → _expert_rewrite.md + _elementary_rewrite.md
4. NLM notebook_create × 2 → $EXPERT_NOTEBOOK_ID, $ELEMENTARY_NOTEBOOK_ID
5. source_add × 2 → upload rewritten content
6. studio_create × 2 → poll studio_status (15s interval, max 20)
7. download_artifact × 2 → rename to .pdf
8. gws drive +upload × 2 → $EXPERT_DRIVE_URL, $ELEMENTARY_DRIVE_URL
9. Extract key summary (3-5 bullets, Korean)
10. python3 scripts/slack_post_message.py → main report + threaded detail
11. Cleanup: delete _expert_rewrite.md, _elementary_rewrite.md
```

**Example 2 — With custom Notion parent**

```
User: "output/research/agent-cloud-analysis.md 노션 3209eddc... 아래에 올리고
      슬라이드 만들어서 전체 파이프라인 돌려줘"

Agent:
(same 11 steps, but Phase 1 uses notion_parent_id = "3209eddc...")
```
