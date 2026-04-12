# x-to-notion

Fetch an X (Twitter) post or article, parse content into structured Markdown, translate to Korean, and publish to Notion. Designed for long-form X Articles but also handles regular tweets.

## Triggers

- User asks to "post tweet to Notion", "X to Notion", "트윗 노션에 올려", "X 아티클 노션", "x-to-notion", "tweet to notion", "트윗 번역해서 노션", "X 글 노션 업로드"
- User provides an x.com or twitter.com URL with Notion publishing intent
- Invoked via `/x-to-notion` command
- **Automatically invoked** by `x-to-slack` (Step 5) and `twitter-timeline-to-slack` (Step 3h) when long-form content is detected (tweet > 500 chars, X Article, 3+ self-reply thread, or quote+body > 400 chars)

## Do NOT Use

- For posting tweets to Slack (use `x-to-slack`)
- For general web page content extraction (use `defuddle`)
- For uploading existing markdown to Notion (use `md-to-notion`)
- For general Notion page creation without tweet source (use Notion MCP directly)

## Authentication Strategy

This skill uses **token-first** Notion authentication:

1. **Primary (Token)**: Uses `NOTION_TOKEN` from `.env` via `scripts/notion_api.py`.
2. **Fallback (MCP)**: Only when `NOTION_TOKEN` is NOT available, fall back
   to `plugin-notion-workspace-notion` MCP server.

## Prerequisites

- `requests` Python package (for Notion API)
- `NOTION_TOKEN` environment variable in `.env` (primary auth)
- `scripts/notion_api.py` shared utility
- Internet access for FxTwitter API and Notion API
- `scripts/parse_article.py` for X Article block parsing

## Inputs

| Parameter | Required | Description |
|---|---|---|
| `url` | Yes | X/Twitter post URL (x.com or twitter.com) |
| `parent_page_id` | No | Notion parent page ID. Default: `3239eddc34e680e8a7a5d5b5eac18b38` (AI 자동 정리) |
| `skip-translate` | No | If set, publish English markdown without Korean translation |

## Workflow

### Phase 0.5: Cross-Repo Dedup Check (MANDATORY)

Before any processing, check the central intelligence registry. When invoked standalone (not as a sub-step of x-to-slack), verify the URL has not already been published to Notion.

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" check "<tweet_url>"
```

- **Exit 0 (new)**: Proceed with the pipeline.
- **Exit 1 (duplicate)**: If invoked standalone, report duplicate and STOP. If invoked by x-to-slack (Step 5), the parent pipeline already passed the check -- proceed.

If the research repo or `intel_registry.py` is not found, log a warning and proceed (graceful degradation).

### Phase 1: Fetch (fetch)

Retrieve tweet content via the FxTwitter API.

1. Extract tweet ID from the URL (strip query params, get last path segment)
2. Extract username from URL path
3. Call `https://api.fxtwitter.com/{username}/status/{tweet_id}`
4. Save raw JSON to `output/x-to-notion/{date}/raw-tweet.json`
5. Detect content type:
   - **X Article**: `tweet.article` exists → use `parse_article.py`
   - **Regular tweet**: use `tweet.text` directly

### Phase 2: Parse (parse)

Convert raw API response into structured Markdown.

**For X Articles** (long-form posts):

Run `scripts/parse_article.py`:

```bash
python .cursor/skills/pipeline/x-to-notion/scripts/parse_article.py \
  output/x-to-notion/{date}/raw-tweet.json \
  output/x-to-notion/{date}/{slug}.en.md
```

The parser handles:
- Block types: `unstyled`, `header-two`, `ordered-list-item`, `unordered-list-item`, `atomic`
- Inline styles: Bold, Italic
- Entity types: LINK (URLs), MEDIA (images/videos), MARKDOWN (code blocks), DIVIDER, TWEET (embedded)
- Media entity lookup for image/video URLs
- Article metadata: title, author, date, engagement stats

**For regular tweets**:

Construct structured markdown with the following sections:

1. **Header**: Title (first ~60 chars of tweet text), author info, engagement stats, original URL
2. **Body**: Full tweet text
3. **Media** (CRITICAL — do NOT skip): Extract ALL media from the FxTwitter API response:
   - **Photos**: `tweet.media.photos[]` → for each photo, emit `![photo](photo.url)` on its own line
   - **Videos**: `tweet.media.videos[]` → for each video, emit `[▶ Video](variant.url)` using the highest-quality `video/mp4` variant from `video.variants[]`
   - **GIFs**: `tweet.media.videos[]` where `type == "gif"` → treat as video, emit `[▶ GIF](variant.url)`
   - If `tweet.media` is absent or empty, check `tweet.media_extended[]` as a fallback
   - Each media item MUST be on its own line so `md_to_blocks` can parse it into a Notion `image` or `video` block
4. **Quote tweets**: If `tweet.quote` exists, add a blockquote section with the quoted tweet's text and media (same extraction rules)
5. **Thread**: If the tweet is a self-reply thread, concatenate all thread tweets with their media

Save output to `output/x-to-notion/{date}/{slug}.en.md`

### Phase 3: Translate (translate)

Translate the English markdown to Korean.

Rules:
- Preserve all code blocks unchanged
- Preserve all URLs, image links, and markdown formatting
- Keep technical terms as-is: Claude Code, Cursor, MCP, API, Git, Docker, etc.
- Keep proper nouns: company names, product names, person names
- Keep file paths and command examples unchanged
- Translate prose, descriptions, and explanations to natural Korean

Save output to `output/x-to-notion/{date}/{slug}.ko.md`

### Phase 4: Publish (publish-notion)

Upload the Korean markdown to Notion.

1. Read the `.ko.md` file
2. Convert markdown to Notion API blocks via `NotionClient.md_to_blocks()`:
   - Headings → `heading_2`, `heading_3`
   - Code blocks → `code` with language
   - Bullet lists → `bulleted_list_item`
   - Numbered lists → `numbered_list_item`
   - Blockquotes → `quote`
   - `![alt](url)` → `image` (external URL)
   - `[text](url.mp4)` → `video` (external URL)
   - Bare image URLs → `image` (external URL)
   - Dividers → `divider`
   - Paragraphs → `paragraph`
3. Publish via `scripts/notion_api.py`:
   ```python
   from scripts.notion_api import NotionClient
   client = NotionClient()
   blocks = NotionClient.md_to_blocks(content)
   page = client.create_page(
       parent_id="<parent-id>",
       title="<title>",
       children=blocks,
       icon_emoji="🐦",
   )
   ```
   The client handles batching (100 blocks/request) and retry automatically.
4. **Fallback**: If `NOTION_TOKEN` not available, use Notion MCP
   `notion-create-pages` with `parent: {"page_id": "..."}`.

**Auth**: Primary — `NOTION_TOKEN` from `.env` via `scripts/notion_api.py`.
Fallback — Notion MCP browser auth.

### Phase 5: Verify & Manifest (verify)

1. Confirm Notion page exists by querying `GET /v1/pages/{page_id}`
2. Write `output/x-to-notion/{date}/manifest.json` with:
   - Pipeline name, date, overall status
   - Per-phase status, file paths, summaries
   - Source metadata (URL, author, title)
   - Notion page ID and URL

### Phase 6: Intelligence Registry Update (MANDATORY)

After successful Notion publishing, register the URL and Notion page ID in the central intelligence registry.

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" save \
  "{tweet_url}" "output/x-to-notion/{date}/{slug}.ko.md" \
  --type notion-article \
  --topic intelligence
```

This ensures the Notion page artifact is saved to `~/thaki/research/outputs/intelligence/` and the URL is registered for cross-repo dedup.

If the research repo is not found, log a warning and skip (graceful degradation). The Notion page is already published.

## Intermediate Persistence

All outputs are persisted to `output/x-to-notion/{date}/`:

```
output/x-to-notion/2026-04-02/
├── manifest.json              # Pipeline status tracker
├── raw-tweet.json             # Phase 1: Raw FxTwitter API response
├── claude-code-guide.en.md    # Phase 2: Parsed English markdown
└── claude-code-guide.ko.md    # Phase 3: Translated Korean markdown
```

Each phase reads only from files, never from in-context memory. Subagents return `{ status, file, summary }`.

## Error Handling

| Phase | Error | Recovery |
|---|---|---|
| Fetch | FxTwitter API error / rate limit | Retry once after 5s; if still failing, report and stop |
| Fetch | Tweet not found (404) | Report "Tweet not found or deleted" and stop |
| Parse | Missing `tweet.article` for article URL | Fall back to regular tweet parsing |
| Translate | Content too large for single LLM call | Split by sections (## headings), translate each, merge |
| Publish | Notion API 401 | Check NOTION_TOKEN validity |
| Publish | Notion API 400 (block limit) | Split into batches of 100 blocks |
| Publish | Network failure | Retry up to 2 times |

## Output

- Korean markdown file at `output/x-to-notion/{date}/{slug}.ko.md`
- Notion page under the specified parent page
- Pipeline manifest at `output/x-to-notion/{date}/manifest.json`

## Examples

### Basic usage

```
User: "이 트윗 노션에 올려줘 https://x.com/user/status/123456"
```

### With custom parent page

```
User: "x-to-notion https://x.com/user/status/123456 parent=abcdef1234"
```

### Skip translation (English only)

```
User: "x-to-notion https://x.com/user/status/123456 skip-translate"
```

### Pipeline output example

```
✅ Phase 1: Fetched tweet — X Article with 30 blocks
✅ Phase 2: Parsed to markdown — 12,294 chars
✅ Phase 3: Translated to Korean — preserving 15 code blocks
✅ Phase 4: Published to Notion — 95 blocks
   📄 https://www.notion.so/Claude-Code-xxxxx

Pipeline complete: output/x-to-notion/2026-04-02/manifest.json
```
