---
name: paper-review
description: >-
  End-to-end academic paper review pipeline that ingests a paper (arXiv URL, PDF,
  or markdown), produces a structured Korean review markdown, runs multi-perspective
  PM/research analysis using 7 PM skills, optionally generates a consolidated Word
  document and PowerPoint presentation (off by default, enable with --with-docx /
  --with-pptx), generates NotebookLM slide decks, creates structured Notion pages,
  and distributes everything to Slack with threaded summaries, Notion links, and
  file uploads.
  Use when the user asks to "review a paper", "paper review", "논문 리뷰",
  "논문 분석", "analyze this paper", "academic paper review", "연구 논문 리뷰",
  "paper review pipeline", "/paper-review", "논문 요약 분석", "논문 정리",
  or any request to systematically review and analyze an academic paper from
  multiple business/research perspectives.
  Do NOT use for arXiv-to-slides without review (use nlm-arxiv-slides).
  Do NOT use for general PDF reading (use anthropic-pdf).
  Do NOT use for market research without a paper (use pm-market-research).
  Do NOT use for ad-hoc Notion page creation (use Notion MCP directly).
metadata:
  author: thaki
  version: 2.1.0
  category: research
---

# Paper Review Pipeline

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

End-to-end pipeline that transforms an academic paper into a structured Korean
review, multi-perspective PM/research analysis documents, a consolidated Word
report, a PowerPoint presentation, NotebookLM slide decks, distributes
structured pages to Notion, and posts threaded summaries with file uploads
and Notion links to Slack.

## Prerequisites

- `pdfplumber` Python package (`pip install pdfplumber`)
- `curl` for arXiv PDF download and Defuddle extraction
- `docx` npm package (`npm install -g docx`) for Word generation
- `pptxgenjs` npm package (`npm install -g pptxgenjs`) for PowerPoint generation
- `defusedxml` and `lxml` for DOCX validation (`pip install defusedxml lxml`)
- `notebooklm-mcp` MCP server authenticated (run `nlm login` if needed)
- `NOTION_TOKEN` in `.env` for Notion API (primary); `plugin-notion-workspace-notion` MCP as fallback
- `SLACK_BOT_TOKEN` in `.env` for Slack file uploads

When running Node.js scripts for DOCX/PPTX generation, set `NODE_PATH` so
globally installed packages are resolved:
```bash
NODE_PATH="$(npm root -g)" node /tmp/script.js
```

## Reference Files

Read these as needed during execution:

- `references/review-template.md` — Korean paper review markdown template (Phase 2)
- `references/analysis-perspectives.md` — PM/research perspective definitions and skill mapping (Phase 3)
- `references/docx-structure.md` — Word document assembly instructions (Phase 4)
- `references/pptx-structure.md` — PowerPoint slide mapping instructions (Phase 5)
- `references/notion-integration.md` — Notion page creation and distribution (Phase 7)
- `references/nlm-slack-integration.md` — NotebookLM slide generation and Slack distribution (Phase 6, 8)

## Pipeline Overview

```
Phase 1: Ingest Paper (PDF/URL/markdown → structured text)
Phase 2: Generate Korean Paper Review (core deliverable, always produced)
Phase 3: Multi-Perspective PM Analysis (parallel subagents, optional)
Phase 4: Consolidate into DOCX (optional, --with-docx)
Phase 5: Generate PPTX (optional, --with-pptx)
Phase 6: Generate NLM Slides (NotebookLM slide deck from review markdown)
Phase 7: Distribute to Notion (main page + sub-pages per perspective)
Phase 8: Distribute to Slack (NLM slides + Notion link + files in thread)
Phase 9: Archive Registration (register paper in paper-archive index)
```

---

## Content Quality Requirements

Every phase must produce substantive, detailed output. Thin or placeholder
content is a pipeline failure.

| Phase | Minimum Output | Quality Gate |
|-------|---------------|-------------|
| Phase 2: Review | 150+ lines | Every section filled with specific evidence, numbers, and paper citations |
| Phase 3: Each perspective | 80+ lines per file | Concrete analysis with paper-specific data, not generic framework skeletons |
| Phase 4: DOCX (if `--with-docx`) | 15+ pages | Must consolidate ALL Phase 2 + Phase 3 outputs in full; no summaries or truncation |
| Phase 5: PPTX (if `--with-pptx`) | 25-35 slides | Substantive bullet points with specific numbers, not placeholder text |

### Language Requirements

- Follow **Output language** above for every deliverable (markdown, DOCX, PPTX).
- English only for proper nouns and technical terms with no standard Korean equivalent.
- Section headings, labels, titles, bullets, analysis, and conclusions: Korean.
- DOCX/PPTX structure: see `references/docx-structure.md` and `references/pptx-structure.md`.

### Depth Expectations

- **Do NOT** produce skeleton or template-only output. Every section must contain
  analysis specific to the paper under review.
- **Cite** specific sections, figures, tables, and numbers from the paper.
- **Quantify** wherever possible: performance deltas, cost comparisons, sample sizes.
- **Compare** against real competitors and related work from the paper.
- Phase 3 perspectives must go beyond restating the paper — they must apply
  frameworks (SWOT, TAM/SAM/SOM, lean canvas, etc.) with concrete, paper-specific data.

---

## Phase 1: Paper Ingestion

Determine input type and extract structured content.

### arXiv URL Input

Extract paper ID from the URL (e.g., `2509.04664` from `https://arxiv.org/abs/2509.04664`).

**Step 1 — AlphaXiv-first fetch (token-efficient structured overview):**

Run three commands in parallel:

```bash
curl -sL --max-time 30 "https://alphaxiv.org/overview/{ID}.md"
curl -L -o /tmp/arxiv-{ID}.pdf "https://arxiv.org/pdf/{ID}"
curl -s "https://defuddle.md/arxiv.org/abs/{ID}"
```

**Step 2 — Choose metadata source (priority order):**

1. **AlphaXiv overview** (preferred): If the first curl returns a valid markdown
   report (non-empty, no 404), parse it for title, authors, abstract, date, and
   structured analysis content. Save the overview to `/tmp/arxiv-{ID}-alphaxiv.md`.
2. **Defuddle** (fallback): If AlphaXiv returns 404, use Defuddle output for
   title, authors, abstract, date.

**Step 3 — Full text extraction (still required for deep review):**

Even when AlphaXiv overview is available, extract full text with pdfplumber for
sections the overview may not cover (equations, tables, appendices):

```python
import pdfplumber
with pdfplumber.open("/tmp/arxiv-{ID}.pdf") as pdf:
    text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
with open("/tmp/arxiv-{ID}-extracted.md", "w") as f:
    f.write(text)
```

**Step 4 — Combine sources for Phase 2:**

When AlphaXiv overview is available, provide BOTH the structured overview AND
the pdfplumber-extracted text to Phase 2. The overview supplies pre-analyzed
structure (problem, approach, results, limitations); the raw text provides
verbatim evidence (figures, tables, equations) for citation.

### Local PDF Input

Extract text directly with pdfplumber using the same pattern above.
Infer title and authors from the first page content.

### Local Markdown/Text Input

Read the file directly. Parse any YAML frontmatter for metadata.

### Output Format

Combine into a structured document:

```markdown
# {Paper Title}
**Authors:** {authors}
**Venue:** {venue/journal/year if known}
**Date:** {date}

## Abstract
{abstract}

## AlphaXiv Structured Overview
{alphaxiv overview content, if available — omit this section if 404}

## Full Paper Content
{section-segmented extracted text from pdfplumber}
```

Identify section boundaries (Introduction, Related Work, Methods, Experiments,
Discussion, Conclusion) by scanning for heading patterns in the extracted text.

---

## Phase 2: Paper Review (Korean)

Read `references/review-template.md` for the complete template.

Generate a detailed Korean review by filling every section of the template
using the extracted paper content. This is the **core deliverable** and must
always be produced regardless of options.

Key requirements:
- Write in formal Korean academic tone
- Every claim must reference specific sections, figures, or tables from the paper
- Contributions should be individually numbered and explained
- Strengths and weaknesses must be concrete and specific, not generic
- Experiments section must include actual numbers from the paper

Save to: `outputs/papers/{paper-id}-review-{DATE}.md`

The `{paper-id}` is derived from:
- arXiv: the paper ID (e.g., `2509.04664`)
- PDF: filename without extension (e.g., `attention-is-all-you-need`)
- Markdown: filename without extension

---

## Phase 3: Multi-Perspective PM/Research Analysis

Skip this phase if `--skip-pm` is set.

Read `references/analysis-perspectives.md` for detailed perspective definitions.

Launch parallel subagents (max 4 concurrent) that apply PM/research skill
frameworks to the paper's proposed method, system, or technology.

Each subagent receives:
1. The paper review markdown from Phase 2
2. The extracted paper content from Phase 1
3. Perspective-specific instructions from `references/analysis-perspectives.md`

### Batch 1 (4 parallel subagents)

| Agent | Skill | Analysis Focus |
|-------|-------|---------------|
| PM Strategy | pm-product-strategy | SWOT, value proposition, lean canvas for the proposed method |
| Market Research | pm-market-research | Market sizing, competitive landscape, user personas |
| Product Discovery | pm-product-discovery | Assumption identification, OST, experiment design |
| GTM Analysis | pm-go-to-market | GTM strategy, ICP, beachhead for commercialization |

### Batch 2 (2 sequential or parallel)

| Agent | Skill | Analysis Focus |
|-------|-------|---------------|
| Statistical Review | kwp-data-statistical-analysis | Methodology rigor, statistical validity |
| Execution Planning | pm-execution + pm-marketing-growth | PRD, positioning, North Star metric |

Each agent MUST use the Write tool to save its output to:
`outputs/papers/{paper-id}-{perspective}-{DATE}.md`

Use `--perspectives "strategy,market,discovery,gtm,statistics,execution"` to
select specific perspectives (comma-separated).

### Post-Phase-3 Verification (MANDATORY)

After all Phase 3 subagents complete, verify that every expected markdown file
exists and meets the minimum quality bar. Run:

```bash
ls -la outputs/papers/{paper-id}-pm-strategy-{DATE}.md
ls -la outputs/papers/{paper-id}-market-research-{DATE}.md
ls -la outputs/papers/{paper-id}-discovery-{DATE}.md
ls -la outputs/papers/{paper-id}-gtm-{DATE}.md
ls -la outputs/papers/{paper-id}-statistics-{DATE}.md
ls -la outputs/papers/{paper-id}-execution-{DATE}.md
```

For each file:
1. If the file is **missing**, the subagent failed to save — regenerate it immediately.
2. Check the line count: `wc -l outputs/papers/{paper-id}-{perspective}-{DATE}.md`
3. If the file has **fewer than 80 lines**, regenerate with more detail.

Do NOT proceed to Phase 4 until all 6 perspective files pass verification.

---

## Phase 4: DOCX Consolidation (optional)

**Skip this phase unless `--with-docx` is explicitly set.**

Read `references/docx-structure.md` for detailed assembly instructions.

Create a professional Word document consolidating all outputs using the
`anthropic-docx` skill pattern (Node.js `docx` package → `Packer.toBuffer()`).

Document structure (all headings and labels in Korean in the file):
1. Cover — paper title, authors, analysis date, report title per template
2. Table of contents
3. Executive synthesis — consolidated findings across perspectives (2–3 pages, concrete numbers)
4. Full paper review — complete Phase 2 output, no omission
5. PM/research analysis — one chapter per perspective (all six in full)
6. Appendix — metadata, methodology notes

**CRITICAL**: Read EVERY perspective markdown file from `outputs/papers/` and
include its FULL content in the DOCX. Do not summarize or truncate. The DOCX
must be a comprehensive document of 15+ pages.

Save to: `outputs/papers/{paper-id}-analysis-{DATE}.docx`

Validate after creation using the anthropic-docx skill's validator:
```bash
python .cursor/skills/anthropic-docx/scripts/office/validate.py output.docx
```

---

## Phase 5: PPTX Generation (optional)

**Skip this phase unless `--with-pptx` is explicitly set.**

Read `references/pptx-structure.md` for detailed slide mapping instructions.

Create a PowerPoint presentation using the `anthropic-pptx` skill pattern
(PptxGenJS from scratch).

Slide structure (~25-35 slides):
1. Title slide (1)
2. Executive summary (2-3)
3. Paper review highlights (5-8)
4. Per-perspective analysis (2-3 per perspective, ~12-18 total)
5. Key takeaways and next steps (2-3)
6. Appendix (2-3)

Save to: `outputs/presentations/{paper-id}-presentation-{DATE}.pptx`

---

## Phase 6: NotebookLM Slide Generation

Skip this phase if `--skip-nlm` is set.

Read `references/nlm-slack-integration.md` for detailed instructions.

1. **Create notebook**: `notebook_create(title="Paper Review: {Paper Title}")`
2. **Add DOCX as source** (if `--with-docx` was set and DOCX exists): `notebook_add_text(notebook_id, title="Paper Analysis Report", file_path="<ABSOLUTE_PATH>/outputs/papers/{paper-id}-analysis-{DATE}.docx")`
3. **Add review as text source**: `notebook_add_text(notebook_id, title="Korean Review", file_path="<ABSOLUTE_PATH>/outputs/papers/{paper-id}-review-{DATE}.md")`
   — If DOCX was not generated, also add each perspective markdown as a separate source.
4. **Generate slides**: `slide_deck_create(notebook_id, format="detailed_deck", confirm=true)`
5. **Poll status**: `studio_status(notebook_id)` every 30s until complete (5-8 min typical)
6. **Download PDF**: `download_artifact(notebook_id, artifact_type="slide_deck", output_path="<ABSOLUTE_PATH>/outputs/presentations/{paper-id}-nlm-slides-{DATE}.pdf")`

Use **absolute paths** for all MCP file operations — the MCP server resolves from its own cwd.

Skills used: **notebooklm**, **notebooklm-studio**

---

## Phase 7: Notion Distribution

Skip this phase if `--skip-notion` is set.

Read `references/notion-integration.md` for detailed instructions.

No default parent page — provide via `--notion-parent <page_id>`.

### Authentication Strategy

Uses **token-first** Notion authentication:
- **Primary**: `NOTION_TOKEN` from `.env` via `scripts/notion_api.py`
- **Fallback**: `plugin-notion-workspace-notion` MCP when token unavailable

### Distribution Steps

#### Path A: Token-based (preferred)

When `NOTION_TOKEN` is available:

```python
from scripts.notion_api import NotionClient

client = NotionClient()
overview_blocks = NotionClient.md_to_blocks(overview_md)
main_page = client.create_page(
    parent_id="<parent-id>",
    title="{Paper Title} — 논문 분석 ({DATE})",
    children=overview_blocks,
    icon_emoji="📄",
)
# Create sub-pages under main_page["id"]
for perspective_md in perspective_files:
    blocks = NotionClient.md_to_blocks(perspective_md)
    client.create_page(parent_id=main_page["id"], title=title, children=blocks)
```

#### Path B: MCP fallback

When `NOTION_TOKEN` is NOT available:

1. **Create main page** — `notion-create-pages` MCP tool under the parent page
   with title pattern `{Paper Title} — paper analysis ({DATE})`
2. **Create sub-pages** — One sub-page per analysis perspective under the main
   page via MCP

Sub-pages are created 2 at a time (parallel-safe within Notion API limits).

3. **Capture page URL** — Save the main page URL for inclusion in the Slack
   thread (Phase 8)

If `--skip-pm` was used, only the review sub-page is created.

Skills used: **scripts/notion_api.py** (primary), **plugin-notion-workspace-notion** MCP (fallback)

---

## Phase 8: Slack Distribution

Skip this phase if `--skip-slack` is set.

Read `references/nlm-slack-integration.md` for detailed instructions.

No default channel — provide via `--channel <name>`.

If the channel name is provided, use `slack_search_channels` MCP tool to resolve its ID.

### Distribution Steps

1. **Main message** — Upload NLM slides PDF via 3-step Slack API (`getUploadURLExternal` → upload → `completeUploadExternal`) with paper title + Korean summary as `initial_comment`; capture `ts` from response. If NLM slides PDF is unavailable (Phase 6 skipped), fall back to `slack_send_message` text-only post.
2. **Thread: Paper Summary** — `slack_send_message` MCP tool with detailed Korean summary (500-1000 chars)
3. **Thread: Notion Link** — `slack_send_message` MCP tool with the Notion main page URL from Phase 7 (skip if `--skip-notion`)
4. **Thread: Upload DOCX** — 3-step Slack upload with `thread_ts` from step 1 (only if `--with-docx` was set)
5. **Thread: Upload PPTX** — 3-step Slack upload with `thread_ts` from step 1 (only if `--with-pptx` was set)

See `references/nlm-slack-integration.md` for exact curl commands, `ts` extraction, and error handling.

Skills used: **Slack MCP** (text messages), **curl** (3-step file upload via `getUploadURLExternal` + `completeUploadExternal`)

---

## Phase 9: Archive Registration

Always runs as the final step — cannot be skipped. Best-effort: failures
do NOT block the pipeline.

Register the reviewed paper in the paper-archive index at
`outputs/papers/index.json`. Collects all metadata from Phase 1,
`title_ko` and `one_line_summary` from Phase 2, all artifact paths from
Phases 2-8, `notion_page_id` from Phase 7, and `nlm_notebook_id` from
Phase 6. Sets status to `reviewed`.

For the full field mapping and implementation steps, see
[paper-archive integration hooks](../paper-archive/references/integration-hooks.md).

Skills used: **paper-archive**

## Phase 10: Research Repo Sync (MANDATORY)

Always runs after Phase 9. Best-effort: failures do NOT block the pipeline.

Copy the paper review markdown and key artifacts to the centralized research repository for Karpathy KB accumulation, and register the paper URL in the central intelligence registry.

1. Copy the review markdown to `~/thaki/research/outputs/papers/{date}/{slug}.md`.
2. Register the paper URL in the central dedup registry:

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" save \
  "{paper_url}" "outputs/papers/{paper_review_filename}" \
  --type paper \
  --topic ai-research
```

This enables:
- Cross-repo deduplication: the same paper won't be reviewed twice from different repos/machines.
- Automatic KB ingestion: `kb_intel_router.py` routes `outputs/papers/` artifacts to the `ai-research` Karpathy KB.
- Compound knowledge growth: paper reviews accumulate in the wiki and become queryable via `kb-query`.

If the research repo is not found, log a warning and skip (graceful degradation).

---

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-pm` | Skip Phase 3 PM analysis; produce review only | PM enabled |
| `--with-docx` | Enable Phase 4 Word document generation | DOCX skipped |
| `--with-pptx` | Enable Phase 5 PowerPoint generation | PPTX skipped |
| `--skip-nlm` | Skip Phase 6 NotebookLM slide generation | NLM enabled |
| `--skip-notion` | Skip Phase 7 Notion page creation | Notion enabled |
| `--notion-parent <id>` | Notion parent page ID for Phase 7 | Required if Notion enabled |
| `--skip-slack` | Skip Phase 8 Slack distribution | Slack enabled |
| `--channel <name>` | Slack channel name for Phase 8 | Required if Slack enabled |
| `--perspectives "..."` | Comma-separated list of perspectives to run | All 6 |
| `--lang ko` | Review in Korean only (default) | Korean |
| `--lang both` | Review in both Korean and English | Korean |

## Output Convention

`outputs/papers/`: review, pm-strategy, market-research, discovery, gtm, statistics, execution, analysis.docx. `outputs/presentations/`: presentation.pptx, nlm-slides.pdf.

## Example

```
/paper-review https://arxiv.org/abs/2509.04664
```

This will:
1. Download PDF and extract text + metadata
2. Generate Korean paper review markdown
3. Run 6 PM/research perspectives in parallel
4. Consolidate into a Word report (only if `--with-docx`)
5. Generate a PowerPoint presentation (only if `--with-pptx`)
6. Generate NotebookLM slide deck from review markdown (+ DOCX if available)
7. Create Notion pages (main + 7 sub-pages) under the specified parent
8. Post Korean summary + Notion link + optional DOCX/PPTX to the specified Slack channel in thread
9. Register the paper in the paper-archive index

```
/paper-review /path/to/paper.pdf --skip-pm --skip-slack
```

This will produce only the paper review markdown, Word doc, PowerPoint, and
NLM slides — without PM analysis, Notion, or Slack posting.

```
/paper-review paper.md --perspectives "strategy,statistics" --channel "research-pr"
```

This will run only Strategy and Statistical perspectives, posting to `#research-pr`.

```
/paper-review paper.pdf --skip-nlm --skip-pptx
```

This will produce only the paper review, DOCX, Notion pages, and post to Slack without NLM slides or PPTX.

```
/paper-review paper.pdf --notion-parent abc123def456 --skip-slack
```

This will create Notion pages under a custom parent page without posting to Slack.

## Skills Composed

| Skill | Phase | Purpose |
|-------|-------|---------|
| alphaxiv-paper-lookup | 1 | Structured arXiv paper overview (token-efficient, primary metadata source) |
| defuddle | 1 | Extract arXiv abstract metadata (fallback when AlphaXiv unavailable) |
| anthropic-pdf | 1 | PDF text extraction patterns |
| pm-product-strategy | 3 | SWOT, lean canvas, value proposition |
| pm-market-research | 3 | Market sizing, competitive, personas |
| pm-product-discovery | 3 | Assumptions, OST, experiments |
| pm-go-to-market | 3 | GTM, ICP, beachhead |
| pm-marketing-growth | 3 | Positioning, North Star |
| pm-execution | 3 | PRD, stakeholder map |
| kwp-data-statistical-analysis | 3 | Statistical methodology review |
| anthropic-docx | 4 | Word document generation |
| anthropic-pptx | 5 | PowerPoint generation |
| notebooklm | 6 | Notebook creation, source upload |
| notebooklm-studio | 6 | Slide deck generation + download |
| Notion MCP | 7 | Page creation and content distribution |
| x-to-slack | 8 | Channel registry pattern |
| Slack MCP + curl | 8 | Text messages + file uploads |
| paper-archive | 9 | Archive index registration |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| pdfplumber not found | `pip install pdfplumber` |
| docx npm not found | `npm install -g docx` |
| pptxgenjs not found | `npm install -g pptxgenjs` |
| PDF text garbled | Complex layouts; extract what you can, note gaps |
| arXiv download fails | Check URL format; try adding version suffix (e.g., `v1`) |
| Defuddle fails | Fall back to extracting metadata from PDF first page |
| DOCX validation fails | Run `.cursor/skills/anthropic-docx/scripts/office/validate.py`; unpack, fix XML, repack |
| Too many parallel agents | Respect 4-agent limit; use Batch 1 + Batch 2 |
| Notion page creation fails | Check parent page ID; verify MCP server is connected |
| Notion Bad Unicode escape | Re-serialize content; remove `\u` sequences from code blocks |
| Notion content too long | Truncate to < 60KB; add overflow note |
| Notion pipe tables break | Convert all `|` tables to bulleted lists before uploading |
| NLM MCP not in server list | Restart Cursor after adding `notebooklm-mcp` to `~/.cursor/mcp.json` |
| NLM auth expired | Run `notebooklm-mcp auth` in terminal, then `refresh_auth` MCP tool |
| NLM slides timeout | Poll `studio_status` every 30-60s; slides take 5-8 min |
| NLM download path error | Use **absolute paths** — MCP server resolves from its own cwd |
| Slack upload fails | Verify `SLACK_BOT_TOKEN` in `.env`; check bot has `files:write` + `chat:write` scopes |
| Slack channel not found | Use `slack_search_channels` MCP tool; verify channel exists and bot is a member |
| Thread reply fails | Ensure `ts` from initial upload was captured correctly from the response JSON |

## Related Skills

- **alphaxiv-paper-lookup** — Structured arXiv paper overview (used in Phase 1 for token-efficient ingestion)
- **paper-archive** — Central paper catalog and search hub
- **nlm-arxiv-slides** — arXiv paper to NotebookLM slide decks
- **nlm-deep-learn** — Accelerated learning from paper sources
- **anthropic-pdf** — PDF manipulation
- **anthropic-docx** — Word document creation
- **anthropic-pptx** — PowerPoint creation
- **notebooklm** — Notebook/source CRUD and querying
- **notebooklm-studio** — Studio content generation + download
- **Notion MCP** — Page creation and workspace management
- **x-to-slack** — Channel registry and Slack posting patterns

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
