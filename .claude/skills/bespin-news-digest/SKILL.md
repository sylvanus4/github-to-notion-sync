---
name: bespin-news-digest
description: >-
  Fetch the latest Bespin Global news email from Gmail, extract all article
  URLs, apply x-to-slack content extraction and research methodology (Jina
  content extraction + WebSearch + AI GPU Cloud classification + 3-message
  Slack thread) to EACH article sequentially, generate a rich DOCX with all
  findings, upload to Google Drive, and post a summary to #효정-할일. ALL articles
  are posted to "process Bespin news", "뉴스 클리핑 분석", "bespin-news-digest", "베스핀
  뉴스", or wants a detailed analysis of the latest Bespin Global news clipping.
  Do NOT use for general Gmail triage (use gmail-daily-triage). Do NOT use for
  single article analysis (use x-to-slack).
---

# Bespin News Digest

Fetch the latest Bespin News email, research each article with the full x-to-slack
pipeline, post a 3-message Slack thread per article to `#bespin-news`, generate a
comprehensive DOCX, and post a Drive-linked summary to `#효정-할일`.

> **Pattern**: mirrors `twitter-timeline-to-slack` — sequential processing with
> mandatory WebSearch per item. No shortcuts.

## Slack Channel Registry

| Channel | ID | Purpose |
|---|---|---|
| `bespin-news` | `C0ANL38CBPG` | Per-article threads (news/media) |
| `효정-할일` | `C0AA8NT4T8T` | Final summary post |
| `효정-insight` | `C0A8SSPC9RU` | (optional override for high-impact articles) |
| `효정-의사결정` | `C0ANBST3KDE` | Personal decision items (decision-router) |
| `7층-리더방` | `C0A6Q7007N2` | Team/CTO decision items (decision-router) |

## Configuration

- **Run date** `{date}`: `YYYY-MM-DD` for the pipeline run — use consistently in all paths under `outputs/bespin-news-digest/{date}/`.
- **Output root**: `outputs/bespin-news-digest/{date}/` (created at initialization).

## Pipeline Output Protocol (File-First)

This pipeline uses **file-first** persistence: every phase writes structured JSON to disk and updates `manifest.json`. Downstream phases and final Slack/DOCX steps **read inputs only from these files** (and `manifest.json`), not from in-context conversation memory.

### Paths and files

- **Output directory**: `outputs/bespin-news-digest/{date}/`
- **Per-phase artifacts**: `outputs/bespin-news-digest/{date}/phase-{N}-{label}.json`
  - Examples: `phase-1-gmail-fetch.json`, `phase-2-parse-articles.json`, `phase-3-per-article-pipeline.json`, `phase-4-docx-generation.json`, `phase-5-drive-upload.json`, `phase-6-summary-slack.json`, `phase-7-decision-summary.json`
- **Manifest**: `outputs/bespin-news-digest/{date}/manifest.json` — single source of truth for run status and phase bookkeeping.

### Subagent return contract

When a subagent (or delegated task) completes work for a phase, it returns **only**:

```json
{ "status": "completed|failed|skipped", "file": "outputs/bespin-news-digest/{date}/phase-N-label.json", "summary": "one-line outcome for manifest" }
```

The orchestrator merges `summary` into `manifest.json` and never relies on full subagent prose for downstream steps.

### Final aggregation rule

Phases that produce **summary posts, DOCX, or consolidated decision posts** MUST:

1. Read `manifest.json` to confirm phase completion and locate `output_file` paths.
2. Load the referenced `phase-*.json` files only.
3. Compose all user-facing content from those JSON payloads — **not** from chat history or uncached model context.

### `manifest.json` schema

```json
{
  "pipeline": "bespin-news-digest",
  "date": "YYYY-MM-DD",
  "started_at": "ISO8601",
  "completed_at": "ISO8601|null",
  "phases": [
    {
      "id": "1",
      "label": "gmail-fetch",
      "status": "pending|running|completed|failed|skipped",
      "output_file": "phase-1-gmail-fetch.json",
      "started_at": "ISO8601|null",
      "elapsed_ms": 0,
      "summary": "short human-readable outcome"
    }
  ],
  "flags": { "skip_decisions": false },
  "overall_status": "running|completed|failed",
  "warnings": ["string"]
}
```

Extend `phases[]` with one entry per logical phase (1–7). On completion, set `completed_at` and `overall_status`.

## Output Artifacts

| Phase | Stage | Output file | Notes |
| ----- | ----- | ----------- | ----- |
| Init | Directory + manifest | `manifest.json` | Created before Phase 1 |
| 1 | Gmail fetch | `phase-1-gmail-fetch.json` | Message id, subject, raw pointers |
| 2 | Parse article URLs | `phase-2-parse-articles.json` | `articles[]` |
| 3 | Per-article pipeline | `phase-3-per-article-pipeline.json` | Append/update per article; Slack ts, research, flags |
| 4 | DOCX generation | `phase-4-docx-generation.json` | Local path + metadata |
| 5 | Drive upload | `phase-5-drive-upload.json` | File ID, folder ID, links |
| 6 | Summary Slack | `phase-6-summary-slack.json` | Posted payload + channel |
| 7 | Decision summary (6.5) | `phase-7-decision-summary.json` | Decision items or skip |

## Initialization (before Phase 1)

1. Set `{date}` to the run date (`YYYY-MM-DD`).
2. `mkdir -p outputs/bespin-news-digest/{date}`.
3. Write **initial** `outputs/bespin-news-digest/{date}/manifest.json`:
   - `pipeline`: `bespin-news-digest`
   - `date`, `started_at` (now), `completed_at`: null
   - `phases`: one object per phase id `1`–`7`, each `status`: `pending`, `output_file` as in the table above, `summary`: `""`
   - `flags.skip_decisions`: per user (`skip-decisions` → true)
   - `overall_status`: `running`
   - `warnings`: `[]`

## Phase 1 — Gmail Fetch

Find the most recent email from `bespin_news@bespinglobal.com`:

```bash
gws gmail +triage \
  --query "from:bespin_news@bespinglobal.com" \
  --max 3 \
  --format json 2>&1
```

Skip the first line (`Using keyring backend: keyring`), parse JSON, and take
`messages[0]` (the most recent). Extract `id` and `subject` (date reference).

If no messages found → report error and exit.

Fetch the full message body:

```bash
gws gmail users messages get \
  --params '{"userId":"me","id":"{MESSAGE_ID}","format":"full"}' 2>&1
```

Decode the base64url HTML body:

```python
import base64, json, sys

lines = sys.stdin.read()
json_start = lines.find('{')
data = json.loads(lines[json_start:])
payload = data.get('payload', {})
parts = payload.get('parts', [])

def decode_part(parts):
    for part in parts:
        if part.get('mimeType') == 'text/html':
            body_data = part.get('body', {}).get('data', '')
            if body_data:
                return base64.urlsafe_b64decode(body_data + '==').decode('utf-8', errors='ignore')
        if 'parts' in part:
            result = decode_part(part['parts'])
            if result:
                return result
    # fallback: top-level body
    body_data = payload.get('body', {}).get('data', '')
    return base64.urlsafe_b64decode(body_data + '==').decode('utf-8', errors='ignore') if body_data else ''

html = decode_part(parts)
print(html)
```

### Phase 1 — Persist & manifest

- Write `outputs/bespin-news-digest/{date}/phase-1-gmail-fetch.json` with at least:
  - `message_id`, `subject`, `html_body` (full decoded HTML from this phase)
  - `source`: `bespin_news@bespinglobal.com`
- Update `manifest.json`: phase `id` `1` → `status`: `completed`, `started_at` / `elapsed_ms`, `summary` (e.g. `Fetched id={message_id}: {subject}`).
- On failure (no message, decode error): set phase `1` `status` to `failed`, `overall_status` to `failed`, append to `warnings`, exit.

**Subagent / delegated fetch**: if this phase runs in a subagent, return only `{ "status", "file", "summary" }` pointing at `phase-1-gmail-fetch.json`.

## Phase 2 — Parse Article URLs

Load `html_body` from `outputs/bespin-news-digest/{date}/phase-1-gmail-fetch.json` — **do not** rely on in-context HTML from Phase 1. Extract all article links and their titles from that HTML:

```python
import re

# Extract href + surrounding text
pattern = r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
links = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

articles = []
seen_urls = set()

SKIP_PATTERNS = [
    'unsubscribe', 'mailto:', 'bespinglobal.com/about', 'bespinglobal.com/privacy',
    'twitter.com', 'linkedin.com', 'facebook.com', 'instagram.com',
    '#', 'javascript:', 'bespinglobal.com/newsletter'
]

for url, title_html in links:
    # Skip navigation/footer/social links
    if any(p in url.lower() for p in SKIP_PATTERNS):
        continue
    if not url.startswith('http'):
        continue
    # Deduplicate
    clean_url = url.split('?')[0].rstrip('/')
    if clean_url in seen_urls:
        continue
    seen_urls.add(clean_url)

    # Clean title
    title = re.sub(r'<[^>]+>', '', title_html).strip()
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) < 3:
        continue

    articles.append({'url': url, 'title': title})

print(f"Found {len(articles)} articles")
```

### Phase 2 — Persist & manifest

- Write `outputs/bespin-news-digest/{date}/phase-2-parse-articles.json` with:
  - `articles`: `[{ "url", "title" }, ...]` (same order as processing: oldest/top-of-email first)
  - `count`: integer
- Update `manifest.json`: phase `id` `2` → `status`: `completed`, `elapsed_ms`, `summary` (e.g. `Parsed {count} article URLs`).

**Subagent**: return only `{ "status", "file", "summary" }` for `phase-2-parse-articles.json`.

## Phase 2.5 — Cross-Repo Dedup Check (MANDATORY)

Before processing articles, check each URL against the centralized intelligence registry to prevent duplicate analysis and Slack posting.

```bash
REGISTRY="scripts/intelligence/intel_registry.py"

# For each article URL from phase-2-parse-articles.json:
python3 "$REGISTRY" check "{ARTICLE_URL}"
# Exit code 0 = new URL (process it)
# Exit code 1 = already processed (skip it)
```

Filter the article list: remove any URL where `intel_registry.py check` returns exit code 1. Update `phase-2-parse-articles.json` with a `dedup_skipped` count and a `filtered_articles` array containing only new URLs. Log skipped URLs in `manifest.json` `warnings`.

If ALL articles are duplicates, skip to Phase 6 with a summary noting "All articles previously processed".

## Phase 3 — Per-Article Pipeline

> **CRITICAL — CHANNEL ROUTING**: ALL articles MUST be posted to `#bespin-news` (`C0ANL38CBPG`).
> Do NOT use x-to-slack topic classification for channel selection. The x-to-slack
> pipeline is used ONLY for its content extraction and research methodology, NOT for
> its channel routing. Never route articles to any channel other than `#bespin-news`.

### Architecture: Fat Subagent Prompt Pattern

Each article is processed by a dedicated `Task` subagent with a fresh context window.
The orchestrator reads `references/subagent-quality-contract.md` once and embeds its
full content into every subagent prompt alongside article-specific data.

**Why subagents**: Processing 5-15 articles sequentially in a single session causes
context window exhaustion. By article 3-5, accumulated FxTwitter/Jina responses,
WebSearch results, and Slack API responses degrade output quality. Each subagent
gets a fresh context, maintaining consistent quality across all articles.

### Dispatch Loop

Load `articles` from `outputs/bespin-news-digest/{date}/phase-2-parse-articles.json` only — **not** from chat context.

Mark `manifest.json` phase `3` as `running` at the start of Phase 3; set `started_at` if not set.

For each article `{url, title}` (oldest/top-of-email first, index 1-based):

1. **Read** the quality contract: `Read(.cursor/skills/pipeline/bespin-news-digest/references/subagent-quality-contract.md)`
2. **Dispatch** a `Task(subagent_type="generalPurpose")` with prompt containing:
   - The full quality contract content (verbatim from the reference file)
   - Article-specific variables: `ARTICLE_URL`, `ARTICLE_TITLE`, `ARTICLE_INDEX`, `RUN_DATE`, `OUTPUT_DIR`, `RESULT_FILE`, `REGISTRY`
   - Instruction: "Follow the quality contract exactly. Write your result JSON to `RESULT_FILE` and return it."
3. **Wait** for the subagent to complete
4. **Read** the result file: `outputs/bespin-news-digest/{date}/article-results/article-{index}.json`
5. **Validate** the returned `quality_score`:
   - `msg2_chars >= 800` (minimum content length)
   - `msg3_chars >= 400` (minimum insights length)
   - `websearch_count >= 2`
   - `content_sentences >= 4`
   - If validation fails, log a warning but continue (do not retry automatically)
6. **Rate limit**: Wait **12 seconds** before dispatching the next article subagent. If the subagent reported a Slack rate limit error, wait 20 seconds instead.
7. **Merge** the article result into `outputs/bespin-news-digest/{date}/phase-3-per-article-pipeline.json`:
   - Append to `articles_processed` array
   - Update `last_updated_article_index` and `total_articles`
8. **Update** `manifest.json` phase `3`: `summary` = `Article {i}/{N} complete: {title}`; keep `status` as `running`

### Subagent Return Contract

Each subagent writes a result JSON to `outputs/bespin-news-digest/{date}/article-results/article-{index}.json`:

```json
{
  "status": "completed|failed|skipped",
  "file": "outputs/bespin-news-digest/{date}/article-results/article-{index}.json",
  "summary": "one-line outcome",
  "article": {
    "url": "{ARTICLE_URL}",
    "title": "{extracted or original title}",
    "source_publication": "{publication name}",
    "domain": "{domain}",
    "classification": "ai-gpu-cloud|topic-specific",
    "extraction_failed": false
  },
  "slack": {
    "message_ts": "{ts from Message 1}",
    "thread_channel": "C0ANL38CBPG"
  },
  "decision_flag": null,
  "quality_score": {
    "msg2_chars": 1200,
    "msg3_chars": 600,
    "websearch_count": 3,
    "reference_links": 3,
    "content_sentences": 6
  },
  "intelligence_artifact": {
    "saved": true,
    "path": "{artifact path}"
  }
}
```

### Subagent Internal Processing (reference only)

Each subagent follows the quality contract in `references/subagent-quality-contract.md`, which covers:
- **Content Extraction**: Jina Reader → WebFetch fallback → curl fallback
- **Web Research**: 2-3 WebSearch queries per article (mandatory, never skip)
- **Topic Classification**: AI GPU Cloud vs topic-specific
- **Slack Thread**: 3-message thread to `#bespin-news` (C0ANL38CBPG)
- **Decision Check**: Flag articles with team/personal decision implications
- **Intelligence Artifact**: Save markdown to research repo and register URL
- **Quality Self-Check**: Character minimums, section completeness, specific facts/numbers

### Orchestrator Post-Dispatch Responsibilities

The orchestrator does NOT perform content extraction, web research, or Slack posting.
It handles only:
- Reading articles from Phase 2 output files
- Reading the quality contract reference file
- Dispatching one subagent per article with the fat prompt
- Rate limiting between subagent dispatches (12s default, 20s on rate limit errors)
- Merging result files into `phase-3-per-article-pipeline.json`
- Updating `manifest.json` progress
- Graceful degradation: if a subagent fails, log the error and continue to the next article

### Phase 3 — Persist & manifest (finalize)

When **all** articles are dispatched and results collected:

- Ensure `phase-3-per-article-pipeline.json` is complete and includes every article in `articles_processed`.
- Set `manifest.json` phase `3` → `status`: `completed`, `elapsed_ms`, final `summary` (e.g. `Processed N articles to #bespin-news`).

## Quality Gate

The orchestrator validates each subagent's returned `quality_score` metrics:

- `msg2_chars >= 800` — sufficient content depth
- `msg3_chars >= 400` — sufficient insights depth
- `websearch_count >= 2` — research was performed
- `content_sentences >= 4` — not a shallow summary
- `reference_links >= 2` — external sources cited

Subagents perform their own internal quality self-check before returning (defined
in `references/subagent-quality-contract.md`). The orchestrator validates the
scores as a second layer of defense.

## Phase 4 — DOCX Generation

**Inputs (files only):** Load and parse:

- `outputs/bespin-news-digest/{date}/phase-2-parse-articles.json` (counts / order)
- `outputs/bespin-news-digest/{date}/phase-3-per-article-pipeline.json` (`articles_processed[]` — source, summary, research_findings, insights, reference_links per your schema in 3h)
- `outputs/bespin-news-digest/{date}/manifest.json` (confirm phase 3 `completed`)

Do **not** use chat memory or uncached prior turns to build the document. Derive `processed_articles` by normalizing each `articles_processed` entry into the fields expected below (`source`, `url`, `title`, `summary`, `research_findings`, `insights`, `reference_links`).

After all articles are processed in Phase 3, generate a comprehensive document:

```python
from docx import Document
from docx.shared import Pt, RGBColor
from datetime import date
import json

run_date = date.today().strftime("%Y-%m-%d")
p3_path = f"outputs/bespin-news-digest/{run_date}/phase-3-per-article-pipeline.json"

# Load phase outputs from disk (adjust keys to match phase-3 JSON)
with open(p3_path, encoding="utf-8") as f:
    p3 = json.load(f)
processed_articles = p3["articles_processed"]  # map fields to docx schema

doc = Document()

# Cover
doc.add_heading(f"Bespin 뉴스클리핑 상세 분석 - {run_date}", 0)
doc.add_paragraph(f"총 {len(processed_articles)}건 기사 분석 | AI/GPU Cloud 인사이트 포함")
doc.add_paragraph()

for i, article in enumerate(processed_articles, 1):
    doc.add_heading(f'{i}. {article["title"]}', level=1)

    # Metadata
    p = doc.add_paragraph()
    p.add_run('출처: ').bold = True
    p.add_run(f'{article["source"]} | {article["url"]}')

    # Full content summary
    p = doc.add_paragraph()
    p.add_run('핵심 내용: ').bold = True
    p.add_run(article['summary'])

    # Web research
    doc.add_heading('추가 조사 결과', level=2)
    for finding in article['research_findings']:
        doc.add_paragraph(finding, style='List Bullet')

    # Insights
    doc.add_heading('인사이트', level=2)
    p = doc.add_paragraph()
    p.add_run(article['insights'])

    # Reference links
    if article['reference_links']:
        doc.add_heading('참고 링크', level=2)
        for link in article['reference_links']:
            doc.add_paragraph(link, style='List Bullet')

    doc.add_paragraph()

out_path = f"outputs/bespin-news-digest/{run_date}/bespin-news-{run_date}.docx"
doc.save(out_path)
```

Primary save path: `outputs/bespin-news-digest/{date}/bespin-news-{YYYY-MM-DD}.docx` (auditable; copy to `/tmp/` only if a tool requires it).

### Phase 4 — Persist & manifest

- Write `outputs/bespin-news-digest/{date}/phase-4-docx-generation.json` with:
  - `local_path`: absolute or repo-relative path to the `.docx`
  - `article_count`: from phase-2/3 files
  - `sha256` or `size_bytes`: optional integrity fields
- Update `manifest.json`: phase `id` `4` → `status`: `completed`, `summary` (e.g. `DOCX written: {local_path}`).

**Subagent**: return only `{ "status", "file", "summary" }` for `phase-4-docx-generation.json`.

## Phase 5 — Google Drive Upload

**Inputs (files only):** Read `phase-4-docx-generation.json` for `local_path`. Do not assume DOCX path from context.

```bash
# Create folder (reuse if already exists from google-daily today)
gws drive files create \
  --json '{"name":"Google Daily - YYYY-MM-DD","mimeType":"application/vnd.google-apps.folder"}'

# Upload DOCX (use path from phase-4-docx-generation.json)
gws drive +upload {LOCAL_DOCX_PATH} --parent {FOLDER_ID}
```

Save the resulting file ID and construct:

- Drive link: `https://drive.google.com/file/d/{FILE_ID}/view`
- Folder link: `https://drive.google.com/drive/folders/{FOLDER_ID}`

### Phase 5 — Persist & manifest

- Write `outputs/bespin-news-digest/{date}/phase-5-drive-upload.json` with:
  - `file_id`, `folder_id`, `drive_file_url`, `drive_folder_url`, `local_path` (echo from phase 4)
- Update `manifest.json`: phase `id` `5` → `status`: `completed`, `summary` (`Drive upload ok`).

**Subagent**: return only `{ "status", "file", "summary" }` for `phase-5-drive-upload.json`.

## Phase 6 — Summary Post to #효정-할일

**Inputs (files only):** Compose the Slack message **exclusively** from:

- `manifest.json` (phase statuses, warnings)
- `phase-2-parse-articles.json` (`count`)
- `phase-3-per-article-pipeline.json` (per-article `classification` / themes — derive AI/GPU Cloud vs other counts)
- `phase-5-drive-upload.json` (`drive_file_url`, file name)

Do **not** infer counts or themes from conversation memory; re-read these JSON files at post time.

Post a final summary to `#효정-할일` (`C0AA8NT4T8T`):

```
*Bespin 뉴스 다이제스트 완료* ({YYYY-MM-DD})

*처리 결과*
- 총 기사: {N}건
- AI/GPU Cloud 관련: {N}건
- 기타 주제: {N}건
- 각 기사별 3-message 쓰레드: #bespin-news 채널

*핵심 테마*
{Top 3 themes from today's news — 1 line each}

*상세 문서*
<{DRIVE_LINK}|bespin-news-{YYYY-MM-DD}.docx>

_각 기사 상세 분석은 #bespin-news 채널에서 확인하세요_
```

### Phase 6 — Persist & manifest

- Write `outputs/bespin-news-digest/{date}/phase-6-summary-slack.json` with:
  - `channel_id`: `C0AA8NT4T8T`
  - `message_text`: exact body posted (or redacted)
  - `message_ts`: if returned by API
- Update `manifest.json`: phase `id` `6` → `status`: `completed`, `summary` (`Posted summary to #효정-할일`).

**Subagent**: return only `{ "status", "file", "summary" }` for `phase-6-summary-slack.json`.

On **successful** completion of Phase 6, set `manifest.json` `completed_at` and set `overall_status` to `completed` if Phase 7 is skipped (`skip_decisions` true or no decision items). Otherwise leave `overall_status` `running` until Phase 7 completes.

## Phase 6.5 — Decision Summary Post (skip if `skip-decisions`)

**Inputs (files only):** Read `flags.skip_decisions` from `manifest.json` and `articles_processed[].decision_flag` (or equivalent) from `phase-3-per-article-pipeline.json`. Do **not** use ad-hoc memory of Step 3f.

After Phase 6, collect all articles flagged in Step 3f **from `phase-3-per-article-pipeline.json` only** and post consolidated
DECISION messages to `#7층-리더방` (`C0A6Q7007N2`).

If no decision items were flagged → skip this phase entirely; set `manifest.json` phase `7` `status` to `skipped` and finalize `overall_status` / `completed_at` if not already set.

For each flagged decision item, post a separate DECISION message using the
`decision-router` template:

```
*[DECISION]* {urgency_badge} | 출처: bespin-news-digest

*{Decision Title}*

*배경*
{1-3 sentence context from the article insights}

*판단 필요 사항*
{What the team/CTO needs to decide}

*옵션*
A. {action option} — {pro/con}
B. {alternative option} — {pro/con}
C. 보류 / 추가 조사 필요

*추천*
{recommended option with rationale}

*긴급도*: {HIGH / MEDIUM / LOW}
*원본*: <{slack_thread_link}|{article title} (#bespin-news)>
```

If there are 3+ decision items, also post a summary header message first:

```
*[Bespin 뉴스 의사결정 요약]* ({date})
오늘 뉴스 다이제스트에서 {N}건의 의사결정 항목이 감지되었습니다.
각 항목이 아래에 개별 메시지로 게시됩니다.
```

### Phase 7 — Persist & manifest (decision summary)

- Write `outputs/bespin-news-digest/{date}/phase-7-decision-summary.json` with:
  - `skipped`: boolean (`true` if `skip_decisions` or zero flagged items)
  - `decision_items_posted`: array of `{ title, urgency, channel_id, message_ts }` (empty if skipped)
- Update `manifest.json`: phase `id` `7` → `status`: `completed` or `skipped`, `summary` (e.g. `Posted N decision stubs` or `No decisions — skipped`).
- Set `manifest.json` `completed_at` (ISO8601) and `overall_status`: `completed` when Phase 7 finishes or is skipped.

**Subagent**: return only `{ "status", "file", "summary" }` for `phase-7-decision-summary.json`.

## Error Recovery

| Phase | Failure | Action |
|-------|---------|--------|
| Init / manifest | Write failure | Fix permissions on `outputs/`; re-run initialization |
| Gmail | No bespin_news email | Report and exit; `manifest.json` phase 1 `failed` |
| Gmail | Auth expired | Re-authenticate: `python3 ~/.config/gws/oauth2_manual.py` + `rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc` |
| Phase 2 | 0 articles parsed | Check HTML structure, try broader regex; inspect `phase-1-gmail-fetch.json` |
| Phase 3a | Jina Reader timeout/error | Fall back to direct WebFetch on URL |
| Phase 3a | 404 / unreachable | Skip article, add "[접속 불가]" in `phase-3` record and DOCX |
| Phase 3d | Slack rate limit | Wait 20s, retry once |
| Phase 3d | Missing `message_ts` | Use `slack_read_channel` to find latest posted message; update `phase-3-per-article-pipeline.json` |
| Phase 3 | Mid-pipeline crash | Resume from last good `phase-3-per-article-pipeline.json` + `manifest.json` phase 3 |
| Phase 4 | python-docx not installed | `pip install python-docx -q` then retry |
| Phase 4 | Missing fields in phase-3 JSON | Fix normalizer; re-read files only |
| Phase 5 | Drive upload failure | Provide local path from `phase-4-docx-generation.json` |
| Phase 6 | #효정-할일 post failure | Report; `phase-6-summary-slack.json` may be partial — inspect manifest `warnings` |
| Phase 7 | decision-router skip | Expected when no flags in `phase-3-per-article-pipeline.json` |

## MCP Tool Reference

| Tool | Server | Purpose |
|---|---|---|
| `slack_send_message` | `plugin-slack-slack` | Post channel message and thread replies |
| `slack_read_channel` | `plugin-slack-slack` | Fallback to find `message_ts` |

## Examples

### Example 1: Standard run

User says: `/bespin-news` or "베스핀 뉴스 분석해줘"

Actions:
0. Initialize `outputs/bespin-news-digest/{date}/` and `manifest.json`
1. Fetch latest `bespin_news@bespinglobal.com` email via gws → `phase-1-gmail-fetch.json`
2. Parse HTML → extract article URLs → `phase-2-parse-articles.json` (typically 10-30 links)
3. For EACH article (sequential): update `phase-3-per-article-pipeline.json` after each
   a. WebFetch Jina Reader for full content
   b. WebSearch 2-3 queries per article
   c. Classify: AI GPU Cloud or topic-specific
   d. Post 3-message Slack thread to #bespin-news
   e. Wait 12s
4. Generate DOCX from phase-2/3 JSON only → `phase-4-docx-generation.json`
5. Upload to Google Drive → `phase-5-drive-upload.json`
6. Post summary to #효정-할일 from JSON inputs only → `phase-6-summary-slack.json`
7. (If decisions) Post to #7층-리더방 from `phase-3` flags → `phase-7-decision-summary.json`; finalize `manifest.json`

### Example 2: Expected article thread quality

For article "아마존, 세레브라스 AI칩 도입":

**Message 1 (#bespin-news):**
```
*:cloud: 세레브라스 AI칩 — 아마존 AWS 도입으로 엔비디아 독점 균열과 추론 인프라 판도 변화*

웨이퍼스케일 WSE-3 칩으로 추론 단계 분리 효율화, GPU 독점 구조에 균열 시작
https://www.yna.co.kr/view/AKR20260314003200091
```

**Message 2 (thread reply):**
```
*아티클 요약*
- 출처: 연합뉴스 (yna.co.kr)
- 제목: 아마존, 세레브라스 'AI칩 도입…추론단계 분리해 효율화

*핵심 내용*
아마존 웹서비스(AWS)가 세레브라스 시스템즈의 웨이퍼스케일 AI 칩(WSE-3)을
추론(inference) 전용 인프라에 도입하기로 결정. 기존 엔비디아 H100 GPU 중심의
학습용 클러스터와 추론용 클러스터를 분리하는 이중 구조를 채택해
비용 효율을 극대화하는 전략. 세레브라스 WSE-3는 단일 다이로 900,000개
이상의 AI 코어를 탑재하고 메모리 대역폭이 GPU 대비 수십 배 높아
토큰 생성 속도에서 압도적 우위. AWS는 이를 Bedrock 추론 서비스 백엔드로
우선 활용할 계획인 것으로 알려짐.

*추가 조사 결과*
- *세레브라스 WSE-3 성능*: 900K AI 코어, 44GB 온칩 SRAM, 메모리 대역폭
  21.1 PB/s — 엔비디아 H100 대비 토큰 생성 속도 최대 20배 빠름 (Cerebras 공식)
- *AWS-엔비디아 관계 변화*: AWS는 자체 Trainium2 칩도 병행 개발 중.
  2026년 추론 시장에서 엔비디아 의존도 20% 감축 목표 (The Information 보도)
- *추론 인프라 분리 트렌드*: Google(TPU v5e), Meta(MTIA), MS(Maia 100)도
  추론 전용 칩으로 GPU 혼용 구조 탈피 가속

*참고 링크*
- <https://www.cerebras.net/blog/cerebras-wse-3|Cerebras WSE-3 공식 발표>
- <https://theinformation.com/aws-cerebras-2026|The Information: AWS-Cerebras 딜>
- <https://www.yna.co.kr/view/AKR20260314003200091|연합뉴스 원문>
```

**Message 3A (AI GPU Cloud thread reply):**
```
*AI GPU Cloud 서비스 인사이트*

AWS의 세레브라스 도입은 추론(inference) 시장의 칩 다변화가 본격화되었음을
의미합니다. 학습은 NVIDIA GPU, 추론은 특화 칩이라는 이중 구조가 클라우드
업계 표준이 될 경우 ThakiCloud의 GPU 인프라 전략도 재검토가 필요합니다.

*핵심 시사점*
- *추론 전용 칩 도입 검토 필요*: H100/B200 외 세레브라스·Trainium 등
  추론 특화 칩을 슬롯에 병행 지원하면 LLM 서빙 단가 경쟁력 확보 가능
- *고객 추론 비용 절감 포지셔닝*: "학습은 NVIDIA, 서빙은 더 저렴하게"라는
  메시지가 엔터프라이즈 고객에게 강력한 차별점
- *파트너십 기회*: 세레브라스는 클라우드 파트너 확장 중 —
  중소형 클라우드 사업자와의 협력 모델 탐색 시기

*적용 가능성*
단기: 추론 전용 인스턴스 가격 정책 재검토 (현재 H100 기준)
중기: Trainium2 / WSE-3 파일럿 도입 검토 및 Slinky 스케줄러 지원 확인
장기: 멀티칩 추론 클러스터 아키텍처 로드맵 수립
```


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
