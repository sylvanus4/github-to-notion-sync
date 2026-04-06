---
name: bespin-news-digest
description: >-
  Fetch the latest Bespin Global news email from Gmail, extract all article URLs,
  apply x-to-slack content extraction and research methodology (Jina content
  extraction + WebSearch + AI GPU Cloud classification + 3-message Slack thread)
  to EACH article sequentially, generate a rich DOCX with all findings, upload
  to Google Drive, and post a summary to #효정-할일. ALL articles are posted to
  #bespin-news — channel routing from x-to-slack is NOT used. Use when the user runs /bespin-news, asks to
  "process Bespin news", "뉴스 클리핑 분석", "bespin-news-digest", "베스핀 뉴스",
  or wants a detailed analysis of the latest Bespin Global news clipping.
  Do NOT use for general Gmail triage (use gmail-daily-triage).
  Do NOT use for single article analysis (use x-to-slack).
metadata:
  author: "thaki"
  version: "1.2.0"
  category: "execution"
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
RESEARCH_REPO="$HOME/thaki/research"
REGISTRY="$RESEARCH_REPO/scripts/intelligence/intel_registry.py"

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

**CRITICAL**: Process each article SEQUENTIALLY. Do NOT parallelize. Each article
MUST go through ALL sub-steps below. Never shortcut to a quick summary.

Load `articles` from `outputs/bespin-news-digest/{date}/phase-2-parse-articles.json` only — **not** from chat context.

Mark `manifest.json` phase `3` as `running` at the start of Phase 3; set `started_at` if not set.

For each article `{url, title}` (oldest/top-of-email first):

### Step 3a: Content Extraction

Fetch via Jina Reader for clean markdown:

```
WebFetch → https://r.jina.ai/{ARTICLE_URL}
```

Extract from the response:
- Article title (from markdown H1 or YAML frontmatter `title:`)
- Author (if present in frontmatter `author:`)
- Publication date (from `published:` or `date:` frontmatter)
- Domain / source publication
- Full body text (key paragraphs — aim for 300-600 chars of core content)

**Fallback**: If Jina Reader returns empty, error, or times out → `WebFetch {ARTICLE_URL}` directly.

**404 / unreachable**: Skip article, note in DOCX as "[접속 불가]", continue.

### Step 3b: Web Research (mandatory — never skip)

Based on the article content, identify 2-3 key topics, technologies, companies,
or entities. Run `WebSearch` for each:

1. `{topic1} 2026 최신 동향` — background and recent developments
2. `{topic2} AI 클라우드 시장 영향` — implications for AI/cloud sector
3. `{topic3} ThakiCloud OR GPU 클라우드 관련성` — (if relevant)

Collect for each query:
- 2-3 specific findings (concrete facts, numbers, quotes)
- 1-2 relevant URLs with page titles

### Step 3c: Topic Classification

Classify whether this article relates to **AI GPU Cloud**:

Criteria — if **any** match strongly:
- Mentions GPU, CUDA, NVIDIA, AMD ROCm, TPU, NPU, AI accelerators
- Discusses cloud infrastructure (AWS, GCP, Azure, NCP) in AI/ML context
- Covers ML training/inference infrastructure, model serving, AI platform services
- References GPU cluster management, Kubernetes for AI, MLOps, HPC
- Discusses AI chip market, GPU supply/demand, cloud GPU pricing

→ If AI GPU Cloud: use **Message 3A** template
→ Otherwise: use **Message 3B** template (topic-specific insights + action items)

### Step 3d: Post 3-Message Slack Thread

All messages use Slack mrkdwn. Rules:
- `*bold*` (single asterisk only, never `**`)
- `_italic_` (underscore)
- `<url|text>` for links
- No `## headers` — use `*bold*` on its own line
- Korean content
- Under 4000 characters per message

**Message 1 — Title (post to `#bespin-news` = `C0ANL38CBPG`)**

```
{1-2 line Korean title capturing the core insight of the article}
{original article URL}
>>>
```

Use MCP tool `slack_send_message` on server `plugin-slack-slack`.
**CRITICAL**: Capture `message_ts` from the response for thread replies.

**Message 2 — Detailed Summary (thread reply)**

Send with `thread_ts` from Message 1:

```
*아티클 요약*
- 출처: {publication name} ({domain})
- 제목: {article title}
- 작성자: {author, if available}

*핵심 내용*
{Article body를 한국어로 상세 요약. 구체적 수치, 기술명, 기업명, 정책명을 빠짐없이 포함.
최소 4-6 문장 이상. 단순 제목 반복 금지.}

*추가 조사 결과*
- *{토픽1}*: {배경 설명과 최신 동향 — 구체적 수치/사실 포함}
- *{토픽2}*: {기술적 의미와 영향 — 구체적 근거 포함}
- *{토픽3}*: {산업 맥락과 시사점 — (있는 경우)}

*참고 링크*
- <{url1}|{title1}>
- <{url2}|{title2}>
- <{url3}|{title3}>
```

**Message 3A — AI GPU Cloud Insights (thread reply, when AI GPU Cloud classified)**

```
*AI GPU Cloud 서비스 인사이트*

{이 기사 주제가 AI GPU Cloud / AI 플랫폼 서비스에 어떤 의미를 가지는지 분석.
ThakiCloud 관점에서 구체적으로 서술.}

*핵심 시사점*
- {GPU 클라우드 인프라 관점에서의 인사이트 — 구체적}
- {AI 플랫폼 서비스에 미칠 영향 — 구체적}
- {팀이 취해야 할 액션 또는 고려사항}

*적용 가능성*
{ThakiCloud 서비스에 구체적으로 어떻게 적용하거나 대응할 수 있는지.
제품/인프라/파트너십 중 해당하는 영역 명시.}
```

**Message 3B — Topic-Specific Insights (thread reply, when NOT AI GPU Cloud)**

```
*{주제 영역} 인사이트*

{이 기사 주제와 관련된 핵심 분석. 단순 요약 반복 금지.}

*핵심 시사점*
- {해당 분야의 트렌드 및 의미 — 구체적}
- {기술적/비즈니스적 영향 — 구체적}
- {주목할 점 또는 리스크}

*Action Items*
- {팀에서 검토하거나 논의할 사항}
- {추가 조사가 필요한 영역}
- {적용 또는 대응 방안}
```

### Step 3e: Rate Limiting

After posting all 3 messages for an article, wait **12 seconds** before
processing the next article. If a Slack rate limit error occurs, wait 20 seconds
and retry once.

### Step 3f: Per-Article Decision Check (skip if `skip-decisions`)

After posting Message 3 for an article, evaluate whether the article's insights
suggest a team-level or personal decision using `decision-router` rules.

Detection criteria for bespin-news articles:
- Cloud provider pricing/service change affecting ThakiCloud infrastructure → **team**, HIGH
- Partnership or vendor opportunity → **team**, MEDIUM
- Competitive product launch requiring strategic response → **team**, MEDIUM
- Product feature idea derived from industry trend → **team**, LOW

If a decision is detected, flag the article for Phase 7 (decision summary) consolidation. Store:
`{title, decision_scope, urgency, decision_summary, slack_thread_link}`.

### Step 3g: Intelligence Artifact Save & URL Registration (MANDATORY)

After posting the 3-message Slack thread, save an intelligence artifact to the centralized research repo and register the URL:

```bash
RESEARCH_REPO="$HOME/thaki/research"
REGISTRY="$RESEARCH_REPO/scripts/intelligence/intel_registry.py"
ARTIFACT_DIR="$RESEARCH_REPO/outputs/intelligence/$(date +%Y-%m-%d)"
mkdir -p "$ARTIFACT_DIR"
```

Generate a markdown artifact file with the article analysis:

```markdown
---
source: bespin-news-digest
url: {ARTICLE_URL}
title: {ARTICLE_TITLE}
date: {YYYY-MM-DD}
classification: {AI GPU Cloud | topic-specific}
---

# {ARTICLE_TITLE}

## Source
- Publication: {publication name} ({domain})
- Original URL: {ARTICLE_URL}

## Summary
{Korean content summary from Message 2 — 핵심 내용 section}

## Research Findings
{추가 조사 결과 from Message 2}

## Insights
{인사이트 from Message 3A or 3B}

## References
{참고 링크 list}
```

Save the artifact and register the URL:

```bash
python3 "$REGISTRY" save "{ARTICLE_URL}" "$ARTIFACT_DIR/{slug}.md"
```

If `$REGISTRY` is unavailable (research repo not found), save the artifact locally to `outputs/bespin-news-digest/{date}/intelligence/` as a fallback. Never skip artifact generation.

### Step 3h: Persist & manifest (per article)

After Steps 3a–3f for **one** article:

- Read/update `outputs/bespin-news-digest/{date}/phase-3-per-article-pipeline.json`:
  - Maintain `articles_processed`: array of objects with: `url`, `title`, `extraction`, `web_research`, `classification`, `slack_message_ts`, `thread_channel` (`C0ANL38CBPG`), `insights_template` (`3A`|`3B`), `decision_flag` (if any, for Phase 7), `quality_gate_checklist` (booleans)
  - Set `last_updated_article_index` and `total_articles` from `phase-2-parse-articles.json`
- Update `manifest.json` phase `3`: `summary` = progress e.g. `Article i/N complete: {title}`; keep `status` `running` until all articles done.

**Subagent** (if used per article): return only `{ "status", "file", "summary" }` — `file` may point to a **slice** file `phase-3-article-{index}.json` that the orchestrator merges into `phase-3-per-article-pipeline.json`, or the main phase-3 file if the orchestrator writes directly.

### Phase 3 — Persist & manifest (finalize)

When **all** articles are processed:

- Ensure `phase-3-per-article-pipeline.json` is complete and includes every article in `articles_processed`.
- Set `manifest.json` phase `3` → `status`: `completed`, `elapsed_ms`, final `summary` (e.g. `Processed N articles to #bespin-news`).

## Quality Gate

Each posted Slack thread MUST include ALL of the following. If any item is
missing, the thread is **incomplete** — retry before moving to next article:

- [ ] Article source publication name + domain
- [ ] Full content summary (minimum 4 sentences, includes specific facts/numbers)
- [ ] At least 2 WebSearch result bullets with specific findings (not generic)
- [ ] At least 2 reference links in `<url|title>` format
- [ ] Message 3 with topic-specific insights (never generic filler like "this is interesting")

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
| Gmail | Auth expired | Instruct: `gws auth login -s gmail` |
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
아마존 AWS가 세레브라스 웨이퍼급 AI칩 도입 — 엔비디아 독점 균열과 추론 인프라 판도 변화
https://www.yna.co.kr/view/AKR20260314003200091
>>>
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
