---
name: paper-review
description: >-
  End-to-end academic paper review pipeline: deep analysis with venue-quality
  peer review (severity-graded FATAL/MAJOR/MINOR, inline annotations),
  dual-audience NLM slides (elementary student + Steve Jobs expert, Korean),
  DOCX detailed report uploaded to Google Drive, and Slack distribution
  (#deep-research-trending summary + threaded slides).
  Use when the user asks to "review a paper", "paper review", "논문 리뷰",
  "논문 분석", "analyze this paper", "peer review", "critique this paper",
  "피어 리뷰", "논문 비평", "약점 분석", "find weaknesses", "submission review",
  "학회 리뷰 시뮬레이션", "review before submission", "/paper-review",
  "논문 요약 분석", "논문 정리", "논문 심층 분석",
  or any request to deeply analyze and critique an academic paper.
  Do NOT use for paper analysis + PM/business perspectives + distribution
  pipeline (use paper-review-pipeline).
  Do NOT use for arXiv-to-slides without review (use nlm-arxiv-slides).
  Do NOT use for general PDF reading (use anthropic-pdf).
  Do NOT use for paper-code consistency checks (use feynman-paper-audit).
  Do NOT use for comparing multiple papers (use feynman-source-comparison).
  Do NOT use for paper summarization only (use alphaxiv-paper-lookup).
metadata:
  author: thaki
  version: 4.0.0
  category: research
---

# Paper Review (Deep Analysis + Peer Review)

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Deep paper analysis combining a structured Korean review with a rigorous
evidence-based peer review. Produces comprehensive analysis of the paper's
contributions, methodology, experiments, and limitations — with severity-graded
weaknesses, inline annotations, and an actionable revision plan.

## Reference Files

Read these as needed during execution:

- `references/review-template.md` — Korean paper review markdown template (Phase 2)

## Pipeline Overview

```
Phase 1: Ingest Paper (PDF/URL/markdown → structured text)
Phase 2: Generate Korean Paper Review (structured analysis, core deliverable)
Phase 3: Evidence-Based Peer Review (severity-graded critique + inline annotations)
Phase 4: Verification Pass (re-check FATAL issues if user provides fixes)
Phase 5: Consolidated Delivery (unified report + key findings)
Phase 6: DOCX Detailed Report + Google Drive Upload
Phase 7: NLM Dual-Audience Slides (초등학생용 + 스티브잡스 발표자료용, Korean)
Phase 8: Slack Distribution (#deep-research-trending summary + threaded slides)
```

---

## Content Quality Requirements

Every phase must produce substantive, detailed output. Thin or placeholder
content is a pipeline failure.

| Phase | Minimum Output | Quality Gate |
|-------|---------------|-------------|
| Phase 2: Review | 150+ lines | Every section filled with specific evidence, numbers, and paper citations |
| Phase 3: Peer Review | 100+ lines | Every weakness cites a specific passage; inline annotations quote exact text |

### Language Requirements

- Follow **Output language** above for every deliverable.
- English only for proper nouns and technical terms with no standard Korean equivalent.
- Section headings, labels, titles, bullets, analysis, and conclusions: Korean.

### Depth Expectations

- **Do NOT** produce skeleton or template-only output. Every section must contain
  analysis specific to the paper under review.
- **Cite** specific sections, figures, tables, and numbers from the paper.
- **Quantify** wherever possible: performance deltas, cost comparisons, sample sizes.
- **Compare** against real competitors and related work from the paper.

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

Even when AlphaXiv overview is available, extract full text for sections
the overview may not cover (equations, tables, appendices).

**Primary**: OpenDataLoader (high-fidelity Markdown with layout, tables, LaTeX):

```python
import opendataloader_pdf, os

output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)
opendataloader_pdf.convert(
    input_path=f"/tmp/arxiv-{ID}.pdf",
    output_dir=output_dir,
    format="markdown",
    quiet=True,
)
md_path = os.path.join(output_dir, f"arxiv-{ID}.md")
with open(md_path) as f:
    text = f.read()
with open(f"/tmp/arxiv-{ID}-extracted.md", "w") as f:
    f.write(text)
```

**Fallback** (if OpenDataLoader is unavailable — no JDK or package not installed):

```python
import pdfplumber
with pdfplumber.open(f"/tmp/arxiv-{ID}.pdf") as pdf:
    text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
with open(f"/tmp/arxiv-{ID}-extracted.md", "w") as f:
    f.write(text)
```

**Step 4 — Combine sources for Phase 2:**

When AlphaXiv overview is available, provide BOTH the structured overview AND
the extracted text to Phase 2. The overview supplies pre-analyzed
structure (problem, approach, results, limitations); the raw text provides
verbatim evidence (figures, tables, equations) for citation.

### Local PDF Input

Extract text directly using OpenDataLoader (or pdfplumber fallback) with
the same pattern above. Infer title and authors from the first page content.

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
{section-segmented extracted text from OpenDataLoader (or pdfplumber fallback)}
```

Identify section boundaries (Introduction, Related Work, Methods, Experiments,
Discussion, Conclusion) by scanning for heading patterns in the extracted text.

---

## Phase 2: Structured Korean Paper Review

Read `references/review-template.md` for the complete template.

Generate a detailed Korean review by filling every section of the template
using the extracted paper content. This is the **core deliverable** and must
always be produced.

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

## Phase 3: Evidence-Based Peer Review

This phase produces a venue-quality peer review with severity-graded weaknesses
and inline annotations. Determine the target venue if known (NeurIPS, ICML,
ACL, CVPR, etc.) to calibrate review standards.

### Step 3.1: Evidence Gathering (Subagent)

For non-trivial papers, spawn a `generalPurpose` subagent:

```
You are a research evidence agent. Your task:

1. Read the paper/artifact thoroughly
2. For each major claim, search for:
   - Cited works — do they actually support the claim?
   - Missing baselines — what should have been compared?
   - Related work gaps — what important papers are missing?
   - Benchmark contamination risks
   - Statistical significance of reported results
3. Build an evidence file at `outputs/papers/{paper-id}-review-evidence-{DATE}.md` with:
   - Evidence table (source, claim, verification status)
   - List of missing references
   - Baseline comparison gaps
4. Return a one-line summary.

Skip this phase for short drafts or early-stage work where evidence gathering
is overkill.
```

### Step 3.2: Peer Review Generation (Subagent)

Spawn a `generalPurpose` subagent with the Phase 2 review + Phase 1 extracted
content + evidence file (if available):

```
You are a skeptical but fair AI research peer reviewer. All output in Korean.

Read the paper and evidence file (if available). Produce a review with TWO parts:

## Part 1: 구조화된 리뷰

### 요약
1-2 paragraph summary of contributions and approach.

### 강점
- [S1] Specific strength with evidence...
- [S2] ...

### 약점
- [W1] **FATAL:** Issue that would block acceptance. Cite specific section/passage.
- [W2] **MAJOR:** Significant concern requiring revision. Cite specific section/passage.
- [W3] **MINOR:** Polish issue or suggestion. Cite specific section/passage.

### 저자에게 보내는 질문
- [Q1] Specific question tied to a claim or method choice...

### 판정
Overall assessment, confidence score (1-5), and venue-calibrated recommendation:
- Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject

### 개정 계획
Prioritized, concrete steps to address each weakness, ordered by severity.

## Part 2: 인라인 주석

Quote specific passages and annotate them:

> "We achieve state-of-the-art results on all benchmarks"
**[W1] FATAL:** Table 3 shows the method underperforms on 2 of 5 benchmarks.

> "Our approach is novel in combining X with Y"
**[W3] MINOR:** Z et al. (2024) combined X with Y. Clarify the distinction.

Rules:
- Every weakness MUST reference a specific passage or section
- Keep looking after the first major problem — do not stop at one issue
- Distinguish fatal/major/minor clearly
- Preserve uncertainty — if it might pass depending on venue norms, say so
- Do not praise vaguely — tie positives to specific evidence
- Challenge "verified" or "confirmed" statements that lack the actual check
- Check for notation drift, inconsistent terminology, conclusions stronger than evidence
```

Save to: `outputs/papers/{paper-id}-peer-review-{DATE}.md`

### Severity Classification Guide

| Level | Criteria | Impact |
|-------|----------|--------|
| **FATAL** | Incorrect claims, fabricated results, fundamental methodology flaws | Blocks acceptance at any venue |
| **MAJOR** | Missing baselines, insufficient ablations, overclaimed novelty, reproducibility gaps | Requires revision before acceptance |
| **MINOR** | Writing clarity, missing citations, notation inconsistency, cosmetic issues | Should fix but not blocking |

---

## Phase 4: Verification Pass (Optional)

Triggers when Phase 3 found FATAL issues:

1. Inform the user of the critical findings
2. If the user provides fixes or clarifications, run one more verification-style
   review pass against the updated content
3. Save the updated review as `outputs/papers/{paper-id}-peer-review-v2-{DATE}.md`

---

## Phase 5: Consolidated Delivery

1. **Unified report**: Combine Phase 2 (Korean review) and Phase 3 (peer review)
   into a single consolidated markdown at
   `outputs/papers/{paper-id}-analysis-{DATE}.md`
2. **Key findings summary**: Present the top 3-5 most impactful findings to the user:
   - FATAL/MAJOR weaknesses first
   - Key strengths that distinguish the paper
   - Verdict and confidence score
3. **Sources**: List any externally inspected sources used during evidence gathering

---

## Phase 6: DOCX Detailed Report + Google Drive Upload

Generate a professional Word document containing the full consolidated review
(Phase 5 output) and upload it to Google Drive for sharing.

### Steps

1. **Generate DOCX** via `anthropic-docx` skill:
   - Input: `outputs/papers/{paper-id}-analysis-{DATE}.md` (Phase 5 consolidated report)
   - Style: 맑은 고딕 본문, A4, 테이블 여백 넉넉, 코드블록 모노스페이스+음영
   - Render Mermaid diagrams as PNG images before inserting (use `mermaid-render` if present)
   - Output: `outputs/papers/{paper-id}-analysis-{DATE}.docx`

2. **Upload to Google Drive** via `gws drive upload`:
   ```bash
   gws drive upload "outputs/papers/{paper-id}-analysis-{DATE}.docx" --parent "논문 리뷰"
   ```

3. **Capture shareable link** from the upload response (`webViewLink`).
   Store link for Phase 8 Slack distribution.

---

## Phase 7: NLM Dual-Audience Slides (Korean)

Generate two slide decks via NotebookLM targeting different audiences.
Both decks MUST be in Korean (한국어).

### Steps

1. **Create NotebookLM notebook** via `notebooklm` skill:
   - Title: `{Paper Title} 리뷰`
   - Add source: the consolidated review markdown from Phase 5

2. **Generate Slide Deck A — 초등학생용 (Elementary Student)**:
   - Persona instruction to NLM:
     ```
     초등학교 5학년 학생이 이해할 수 있도록 쉬운 한국어로 설명하세요.
     전문 용어는 비유와 그림으로 풀어서 설명하고,
     핵심 개념 3-5개만 슬라이드로 만드세요.
     ```
   - Use `notebooklm-studio` → `studio_create` with type `slide_deck`
   - Download PDF artifact → `outputs/papers/{paper-id}-slides-elementary-{DATE}.pdf`

3. **Generate Slide Deck B — 스티브잡스 발표자료용 (Steve Jobs Expert)**:
   - Persona instruction to NLM:
     ```
     스티브 잡스 스타일의 전문가 발표 자료를 만드세요.
     흰색 배경에 핵심 메시지 하나씩, 데이터와 인사이트 중심,
     청중을 설득하는 스토리텔링 구조로 한국어 슬라이드를 생성하세요.
     ```
   - Use `notebooklm-studio` → `studio_create` with type `slide_deck`
   - Download PDF artifact → `outputs/papers/{paper-id}-slides-expert-{DATE}.pdf`

---

## Phase 8: Slack Distribution (#deep-research-trending)

Post the review summary and slide decks to Slack.

### Steps

1. **Main thread message** to `#deep-research-trending`:
   - Format:
     ```
     📄 논문 리뷰: {Paper Title}

     🔬 핵심 기여: {1-2 line summary of contributions}
     ⚠️ 주요 약점: {top FATAL/MAJOR weakness, 1 line}
     📊 판정: {verdict} (신뢰도: {confidence}/5)
     📎 상세 리뷰: {Google Drive link from Phase 6}
     ```
   - Use `scripts/slack_post_message.py` with channel `#deep-research-trending`

2. **Thread reply 1 — 초등학생용 슬라이드**:
   - Upload `outputs/papers/{paper-id}-slides-elementary-{DATE}.pdf` as file
   - Message: `📚 초등학생용 슬라이드 (쉬운 설명 버전)`
   - Post as thread reply to the main message

3. **Thread reply 2 — 스티브잡스 발표자료용 슬라이드**:
   - Upload `outputs/papers/{paper-id}-slides-expert-{DATE}.pdf` as file
   - Message: `🎤 전문가 발표자료 (Steve Jobs 스타일)`
   - Post as thread reply to the main message

---

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--venue <name>` | Target venue to calibrate review standards (NeurIPS, ICML, ACL, etc.) | None (generic) |
| `--skip-evidence` | Skip Phase 3.1 evidence gathering subagent | Evidence enabled |
| `--draft-mode` | Lighter review for early-stage drafts (relaxed quality bar) | Full review |
| `--skip-slides` | Skip Phase 7 NLM slide generation | Slides enabled |
| `--skip-slack` | Skip Phase 8 Slack distribution | Slack enabled |
| `--skip-docx` | Skip Phase 6 DOCX generation and Drive upload | DOCX enabled |

## Output Convention

```
outputs/papers/
├── {paper-id}-review-{DATE}.md              # Phase 2: Structured Korean review
├── {paper-id}-review-evidence-{DATE}.md     # Phase 3.1: Evidence gathering (if run)
├── {paper-id}-peer-review-{DATE}.md         # Phase 3.2: Peer review with annotations
├── {paper-id}-analysis-{DATE}.md            # Phase 5: Consolidated report
├── {paper-id}-analysis-{DATE}.docx          # Phase 6: DOCX detailed report
├── {paper-id}-slides-elementary-{DATE}.pdf  # Phase 7: 초등학생용 slides
└── {paper-id}-slides-expert-{DATE}.pdf      # Phase 7: 스티브잡스 발표자료용 slides
```

## Example

```
/paper-review https://arxiv.org/abs/2509.04664
```

This will:
1. Download PDF, fetch AlphaXiv overview, and extract full text
2. Generate a comprehensive Korean paper review (150+ lines)
3. Gather evidence against claims, search for missing baselines/references
4. Produce a severity-graded peer review with inline annotations and revision plan
5. Deliver a consolidated analysis report with top findings
6. Generate a DOCX report and upload to Google Drive
7. Create dual-audience NLM slides (초등학생용 + 스티브잡스 발표자료용) in Korean
8. Post summary to #deep-research-trending with slide PDFs in thread

```
/paper-review /path/to/paper.pdf --venue NeurIPS --skip-slides
```

NeurIPS-calibrated review without slide generation.

```
/paper-review draft.md --draft-mode --skip-evidence --skip-docx --skip-slack
```

Lightweight review for early drafts — analysis only, no distribution.

## Prerequisites

- `opendataloader-pdf` Python package + JDK 11+ (preferred PDF parser; `pip install opendataloader-pdf`)
- `pdfplumber` Python package (`pip install pdfplumber`) — fallback PDF parser
- `curl` for arXiv PDF download and Defuddle extraction
- `gws` CLI configured with Google Drive access (Phase 6)
- NotebookLM MCP server (`user-notebooklm-mcp`) connected (Phase 7)
- Slack MCP server (`plugin-slack-slack`) connected (Phase 8)

## Skills Composed

| Skill | Phase | Purpose |
|-------|-------|---------|
| alphaxiv-paper-lookup | 1 | Structured arXiv paper overview (token-efficient, primary metadata source) |
| defuddle | 1 | Extract arXiv abstract metadata (fallback when AlphaXiv unavailable) |
| opendataloader | 1 | High-fidelity PDF-to-Markdown conversion (primary parser) |
| anthropic-pdf | 1 | PDF text extraction patterns (fallback) |
| anthropic-docx | 6 | Generate professional Word document from consolidated review |
| gws-drive | 6 | Upload DOCX to Google Drive and retrieve shareable link |
| notebooklm | 7 | Create notebook and add review as source |
| notebooklm-studio | 7 | Generate dual-audience slide deck PDFs |
| kwp-slack-slack-messaging | 8 | Post summary + threaded slide uploads to #deep-research-trending |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| opendataloader-pdf not found | `pip install opendataloader-pdf` + verify JDK 11+ (`java -version`); falls back to pdfplumber |
| pdfplumber not found | `pip install pdfplumber` (fallback parser) |
| PDF text garbled | Complex layouts; extract what you can, note gaps |
| arXiv download fails | Check URL format; try adding version suffix (e.g., `v1`) |
| Defuddle fails | Fall back to extracting metadata from PDF first page |
| gws drive upload fails | Check `gws auth status`; ensure Drive scope authorized |
| NLM slide generation fails | Verify `user-notebooklm-mcp` MCP connected; check notebook source added |
| Slack post fails | Verify `plugin-slack-slack` MCP connected; check channel name |
| Slide PDF download fails | Check NLM artifact ID; retry `studio_download` |

## Related Skills

- **paper-review-pipeline** — Full pipeline with PM/business analysis + distribution (Notion/Slack/DOCX/PPTX/NLM)
- **feynman-paper-audit** — Paper-code consistency checks
- **feynman-source-comparison** — Compare multiple papers/approaches
- **feynman-replication** — Replicate and verify paper results
- **feynman-research-watch** — Set up recurring paper monitoring
- **alphaxiv-paper-lookup** — Quick structured paper overview
- **paper-archive** — Central paper catalog and search hub
- **nlm-arxiv-slides** — arXiv paper to NotebookLM slide decks (without review)
- **nlm-dual-slides** — Standalone dual-audience slide generation

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share the **full paper review from Phase 2** + extracted content from Phase 1
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt
- Evidence subagent: focus on claim verification, not general summarization
- Review subagent: must produce BOTH structured review AND inline annotations

## Verification Before Completion

- [ ] Every weakness cites a specific passage or section
- [ ] Inline annotations quote exact text from the paper
- [ ] Severity levels are consistently applied (FATAL/MAJOR/MINOR)
- [ ] Revision plan is actionable and prioritized
- [ ] Output files exist at documented paths
- [ ] Consolidated report combines Phase 2 + Phase 3 outputs
- [ ] DOCX uploaded to Google Drive with shareable link obtained
- [ ] Two NLM slide PDFs generated (elementary + expert) in Korean
- [ ] Slack main post sent to #deep-research-trending
- [ ] Slide PDFs uploaded as thread replies
