---
name: related-papers-scout
description: >-
  Discover hot related papers from elite institutions (Google, MIT, Stanford,
  NVIDIA) or with high Twitter/GitHub traction given an input paper. Searches
  Semantic Scholar, arXiv, Papers With Code, and Twitter; ranks by institution,
  citations, GitHub stars, and community buzz; posts structured Slack thread.
  Use when the user asks to "find related papers", "similar papers",
  "hot papers", "관련 논문", "유사 논문", "핫한 논문", "논문 추천",
  "scout papers", "related work", "/related-papers-scout".
  Do NOT use for paper review (use paper-review), arXiv-to-slides
  (use nlm-arxiv-slides), or general web search (use parallel-web-search).
metadata:
  author: thaki
  version: 1.0.0
  category: research
---

# Related Papers Scout

Multi-source pipeline that discovers 5 hot related papers from elite
institutions or with high community traction, given an input paper.

## Prerequisites

- `opendataloader-pdf` Python package + JDK 11+ (preferred PDF parser); `pdfplumber` as fallback
- `curl` for arXiv PDF download and Defuddle extraction
- Internet access for Semantic Scholar API, WebSearch, and Slack MCP
- `SLACK_BOT_TOKEN` in `.env` for Slack distribution (Phase 6)
- Slack MCP server (`plugin-slack-slack`) connected

## Pipeline Overview

```
Phase 1: Ingest Paper       (extract title, abstract, key terms, arXiv ID)
Phase 2: Multi-Source Search (4 parallel agents across Semantic Scholar, arXiv, PapersWithCode, Twitter/GitHub)
Phase 3: Filter & Rank      (score candidates, select top 5)
Phase 4: Deep Dive          (parallel subagents produce structured summaries per paper)
Phase 5: Report Generation  (consolidated markdown report)
Phase 6: Slack Distribution  (main message + 5 threaded paper summaries)
Phase 7: Archive Registration (register discovered papers in paper-archive index)
```

---

## Phase 1: Paper Ingestion

Determine input type and extract structured metadata for search queries.

### arXiv URL Input

Extract paper ID from the URL (e.g., `2509.04664` from `https://arxiv.org/abs/2509.04664`).

**Step 1 — AlphaXiv-first fetch (preferred, token-efficient):**

```bash
curl -sL --max-time 30 "https://alphaxiv.org/overview/{ID}.md"
```

**Step 2 — If AlphaXiv overview is available** (non-empty, no 404):

Use the structured report directly. It contains title, authors, abstract,
key contributions, methodology, and results — everything needed to build
the search profile. Skip PDF download and pdfplumber entirely.

**Step 3 — If AlphaXiv returns 404** (fallback to PDF flow):

Run two commands in parallel:

```bash
curl -L -o /tmp/arxiv-{ID}.pdf "https://arxiv.org/pdf/{ID}"
curl -s "https://defuddle.md/arxiv.org/abs/{ID}"
```

Parse Defuddle output for title, authors, abstract, date, and arXiv categories.

Extract text from the first 5 pages (OpenDataLoader preferred, pdfplumber fallback):

```python
import opendataloader_pdf, os

pdf_path = "/tmp/arxiv-{ID}.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

try:
    opendataloader_pdf.convert(input_path=pdf_path, output_dir=output_dir, format="markdown", quiet=True)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    with open(os.path.join(output_dir, f"{stem}.md"), "r") as f:
        text = f.read()
except Exception:
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages[:5])

with open("/tmp/arxiv-{ID}-extracted.md", "w") as f:
    f.write(text)
```

Only the first 5 pages are needed — sufficient for title, abstract, intro, and
related work which contain the key terms needed for search.

### Local PDF Input

Extract text with OpenDataLoader (fallback: pdfplumber, first 5 pages). Infer title and authors from
the first page content.

### Local Markdown/Text Input

Read the file directly. Parse any YAML frontmatter for metadata.

### Output: Search Profile

From the extracted content, produce the following search profile:

| Field | Source | Example |
|-------|--------|---------|
| `title` | Defuddle or first page | "Attention Is All You Need" |
| `abstract` | Defuddle or extracted text | Full abstract text |
| `arxiv_id` | URL or extracted | `1706.03762` |
| `arxiv_category` | Defuddle metadata | `cs.CL` |
| `key_terms` | Top 8-10 domain terms from abstract + intro | `["transformer", "self-attention", "sequence-to-sequence", ...]` |
| `authors` | Defuddle or first page | `["Vaswani et al."]` |

To extract `key_terms`, scan the abstract and introduction for:
- Proper nouns and technical terms (capitalized multi-word phrases)
- Terms that appear 2+ times in the abstract
- Method/model names explicitly introduced by the paper
- Exclude generic academic words (e.g., "approach", "results", "paper")

---

## Phase 2: Multi-Source Discovery (4 Parallel Subagents)

Launch 4 parallel subagents (max 4 concurrent). Each agent returns a list
of candidate papers with metadata.

| Agent | Source | Purpose |
|-------|--------|---------|
| Agent 1 | Semantic Scholar API | Recommendations + citing papers, institution filtering |
| Agent 2 | Google Scholar + arXiv (WebSearch) | Keyword-based discovery with institution filters |
| Agent 3 | Papers With Code + GitHub (WebSearch) | Implementation traction signal |
| Agent 4 | Twitter/X + community (WebSearch) | Social traction and buzz signal |

For detailed search queries and instructions per agent, see
[references/search-agents.md](references/search-agents.md).

---

## Phase 3: Filter, Rank, and Select Top 5

Aggregate all candidates from the 4 agents into a unified list.
Deduplicate by arXiv ID or by title similarity (>90% overlap = same paper).

Discard any candidate published more than `--recency-months` ago (default: 9
months). Then score remaining candidates across 5 weighted dimensions:
institution match (30%), citation count (20%), GitHub traction (20%),
Twitter/community buzz (15%), and recency (15%). Select top 5 after enforcing
institution diversity and subtopic coverage rules.

For the detailed scoring rubric, thresholds, and selection rules, see
[references/scoring-rubric.md](references/scoring-rubric.md).

---

## Phase 4: Deep Dive (Parallel Subagents)

For each of the 5 selected papers, launch a subagent (Batch 1: papers 1-4
in parallel, Batch 2: paper 5).

Each subagent:
1. Fetches the full abstract via `defuddle` (`curl -s "https://defuddle.md/arxiv.org/abs/{arxiv_id}"`) or Semantic Scholar API
2. Runs 1-2 WebSearch queries for blog posts, GitHub repos, and community discussion
3. Produces a structured Korean summary with metadata, "why read this" evidence, content summary, and reference links

For the exact summary template, see the "Deep Dive Summary Template" section
in [references/scoring-rubric.md](references/scoring-rubric.md).

---

## Phase 5: Report Generation

Compile all 5 paper summaries into a single markdown report.

Save to: `outputs/papers/{input-paper-id}-related-papers-{DATE}.md`

Where `{DATE}` is `YYYY-MM-DD` format (e.g., `2026-03-11`).

### Report Structure

1. **Header** — input paper title, authors, arXiv URL, analysis date
2. **탐색 방법론** — search sources, candidate count, filtering criteria
3. **추천 논문** — all 5 paper summaries (from Phase 4), separated by `---`
4. **교차 분석** — common themes, research trajectory, open questions
5. **검색 쿼리 및 소스** — actual queries used (for reproducibility)

### Verification

After generating the report:

```bash
wc -l outputs/papers/{input-paper-id}-related-papers-{DATE}.md
```

The report should be at least 200 lines. If shorter, the deep dive summaries
are likely too thin — regenerate with more detail.

---

## Phase 6: Slack Distribution

Skip this phase if `--skip-slack` is set.

Default channel: `#deep-research-trending` (ID: `C0AN34G4QHK`). Override with `--channel <name>`.

### Channel Registry

| Channel Name | Channel ID | Type |
|---|---|---|
| `deep-research-trending` | `C0AN34G4QHK` | private |
| `research` | `C0A7GBRK2SW` | private |
| `press` | `C0A7NCP33LG` | public |
| `research-pr` | `C0A7FS8UC66` | public |

If the target channel is not in the registry, use `slack_search_channels`
MCP tool (server: `plugin-slack-slack`) to resolve. For private channels,
fall back to `slack_search_public_and_private` with `in:{channel_name}`.

### Message Format

All messages use Slack mrkdwn format. Rules:
- Use `*bold*` (single asterisk), `_italic_` (underscore)
- Do NOT use `**double asterisks**` or `## headers`
- Write content in Korean
- Limit each message to under 4000 characters

### Step 6.1: Main Message

Post to the channel using `slack_send_message` MCP tool:

```
slack_send_message(
  channel_id="<CHANNEL_ID>",
  message="*🔍 관련 핫 논문 Top 5: {Input Paper Title}*\n\n원본 논문: {arxiv_url}\n\n{2-3 sentence overview of what was searched and why these 5 were selected}\n\n*선정 기준*: 기관 (Google/MIT/Stanford/NVIDIA), 인용수, GitHub Stars, 커뮤니티 반응\n*검색 소스*: Semantic Scholar, arXiv, Papers With Code, Twitter/X\n\n각 논문의 상세 분석은 아래 스레드를 확인하세요 👇"
)
```

**CRITICAL**: Capture the `message_ts` from the response. This is needed
for all thread replies.

### Step 6.2: Thread Replies (5 Papers)

For each of the 5 papers, send a thread reply:

```
slack_send_message(
  channel_id="<CHANNEL_ID>",
  thread_ts="<THREAD_TS>",
  message="*{rank}. {Paper Title}*\n저자: {authors} ({institution})\narXiv: {arxiv_url}\n인용수: {citations} | GitHub Stars: {stars}\n\n*왜 이 논문을 봐야 하는가*\n• {reason_1}\n• {reason_2}\n• {reason_3}\n\n*핵심 내용*\n{3-5 sentence summary}\n\n참고: {blog_url or github_url}"
)
```

Post papers in order (1 through 5). Each message should be self-contained
and under 4000 characters.

### Error Handling

| Error | Fix |
|-------|-----|
| Channel not found | Use `slack_search_channels` MCP; verify bot membership |
| Missing `message_ts` | Use `slack_read_channel` to find the most recent bot message |
| Message too long | Truncate the summary section; keep reasons and metadata |

---

## Phase 7: Archive Registration

Always runs as the final step — cannot be skipped.

Register all discovered papers and the input paper in the paper-archive
index at `outputs/papers/index.json`. See
`../paper-archive/references/integration-hooks.md` for the full field mapping.

### Steps

1. Load `outputs/papers/index.json` (create empty scaffold if missing).
2. For each of the top-N discovered papers from Phase 4:
   a. Extract arXiv ID, title, authors, institutions from the deep dive summary.
   b. Check if this ID already exists in the index — skip if yes.
   c. Append a new entry with status `discovered`, setting `discovered_from`
      to the input paper's ID.
   d. Add a `related` relationship from the input paper to this discovered paper.
3. Check if the input paper exists in the index:
   - If yes: update its `related_papers` array with newly discovered IDs.
     Add `artifacts.related_report` path.
   - If no: register the input paper with status `discovered` and the
     available metadata from Phase 1.
4. Save `index.json` with updated `updated_at` timestamp.
5. Append summaries to `memory/sessions/paper-archive-{DATE}.md` for the
   recall system.

### Error Handling

If archive registration fails, log a warning but do NOT fail the overall
pipeline. The report and Slack outputs from Phases 5-6 are unaffected.

Skills used: **paper-archive**

---

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-slack` | Skip Phase 6 Slack distribution | Slack enabled |
| `--channel <name>` | Target Slack channel name | `deep-research-trending` |
| `--top N` | Number of papers to discover | 5 |
| `--institutions "..."` | Comma-separated institution filter | `google,mit,stanford,nvidia` |
| `--recency-months N` | Max age of papers in months (older papers are skipped) | 9 |

## Output Convention

```
outputs/
└── papers/
    └── {input-paper-id}-related-papers-{DATE}.md
```

## Example

```
/related-papers-scout https://arxiv.org/abs/2509.04664
```

This will:
1. Extract paper metadata and key terms from the arXiv paper
2. Search Semantic Scholar, arXiv, Papers With Code, and Twitter/X in parallel
3. Score and rank candidates by institution, citations, GitHub stars, community buzz, and recency
4. Deep-dive into the top 5 with structured Korean summaries
5. Save a consolidated report to `outputs/papers/`
6. Post a main summary + 5 threaded paper summaries to `#deep-research-trending`
7. Register all 5 discovered papers + input paper in the paper-archive index

```
/related-papers-scout /path/to/paper.pdf --skip-slack
```

Discover related papers and save the report without Slack posting.

```
/related-papers-scout https://arxiv.org/abs/2509.04664 --top 10 --institutions "google,meta,nvidia,microsoft"
```

Find 10 papers, expanding the institution filter to include Meta and Microsoft.

```
/related-papers-scout paper.md --channel "press" --recency-months 6
```

Only consider papers from the last 6 months (stricter than default 9) and post to `#press`.

## Skills Composed

| Skill | Phase | Purpose |
|-------|-------|---------|
| alphaxiv-paper-lookup | 1 | Structured arXiv overview (primary source, replaces PDF + pdfplumber) |
| defuddle | 1, 4 | Extract arXiv abstract and metadata (fallback when AlphaXiv unavailable) |
| WebSearch | 2, 4 | Multi-source paper discovery and evidence gathering |
| parallel-web-search | 2 | Bulk search for related papers (if `parallel-cli` available) |
| Slack MCP | 6 | Channel resolution + threaded message posting |
| x-to-slack | 6 | Channel registry pattern (reused, not invoked) |
| paper-archive | 7 | Archive index registration for discovered papers |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Semantic Scholar API 429 | Rate limited; add 3-second delays between requests |
| Semantic Scholar returns empty | Paper may be too new; fall back to WebSearch-only discovery. Also try Exa Search via agent-reach: `mcporter call 'exa.web_search_exa(query: "related:{paper_title}", numResults: 10)'` |
| opendataloader-pdf not found | `pip install opendataloader-pdf` + verify JDK 11+; falls back to pdfplumber |
| pdfplumber not found | `pip install pdfplumber` (fallback parser) |
| Defuddle fails | Fall back to extracting metadata from PDF first page |
| WebSearch returns too few results | Supplement with Exa Search (agent-reach MCP channel): `mcporter call 'exa.find_similar(url: "https://arxiv.org/abs/{arxiv_id}", numResults: 10)'` for semantically similar papers |
| Too few institution matches | Relax institution filter per Phase 3 selection rules |
| Slack channel not found | Use `slack_search_channels`; verify bot is a channel member |
| Thread reply fails | Ensure `message_ts` was captured from main message response |

## Related Skills

- **alphaxiv-paper-lookup** — Structured arXiv paper overview (used in Phase 1 for token-efficient ingestion)
- **paper-archive** — Central paper catalog and search hub
- **paper-review** — Full paper review pipeline (review + PM analysis + DOCX + PPTX + NLM)
- **nlm-arxiv-slides** — arXiv paper to NotebookLM slide decks
- **alphaear-search** — Finance-specific web search
- **parallel-web-search** — General web search
- **parallel-deep-research** — Deep exhaustive web research

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
