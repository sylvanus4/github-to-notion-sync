# Paper Archive — Integration Hooks

How paper-review, related-papers-scout, alphaxiv-paper-lookup, and
nlm-arxiv-slides auto-register papers into the archive after completing
their pipelines.

## Principle

Each source skill appends a registration step at the end of its pipeline.
The step is **best-effort** — if the archive registration fails, the
source skill's primary outputs are unaffected. Log a warning and continue.

---

## paper-review — Phase 9: Archive Registration

**Trigger**: After Phase 8 (Slack Distribution) completes, or after the
last enabled phase if Slack is skipped.

### What to Register

| Field | Value |
|---|---|
| `id` | `{paper-id}` from Phase 1 |
| `title` | Paper title from Phase 1 metadata |
| `title_ko` | Korean title from Phase 2 review (논문 정보 table) |
| `authors` | Authors from Phase 1 metadata |
| `arxiv_url` | arXiv URL if input was arXiv |
| `date_published` | Publication date from metadata |
| `date_archived` | Today (YYYY-MM-DD) |
| `tags` | Extract 3-5 topic tags from the review (key terms, research area) |
| `status` | `reviewed` |
| `one_line_summary` | "한줄 요약" from Phase 2 review |
| `artifacts.review` | `outputs/papers/{paper-id}-review-{DATE}.md` |
| `artifacts.pm_analyses` | List of all perspective markdown paths |
| `artifacts.docx` | `outputs/papers/{paper-id}-analysis-{DATE}.docx` |
| `artifacts.pptx` | `outputs/presentations/{paper-id}-presentation-{DATE}.pptx` |
| `artifacts.nlm_slides` | `outputs/presentations/{paper-id}-nlm-slides-{DATE}.pdf` |
| `notion_page_id` | Captured from Phase 7 (if not skipped) |
| `nlm_notebook_id` | Captured from Phase 6 (if not skipped) |
| `source_skill` | `paper-review` |

### Implementation Steps

1. Load `outputs/papers/index.json` (create scaffold if missing).
2. Check if `{paper-id}` already exists:
   - If yes: **update** the existing entry with new/additional artifacts
     and promote status to `reviewed` if it was lower.
   - If no: **append** a new entry.
3. Save `index.json` with updated `updated_at`.
4. Append a memory entry to `memory/sessions/paper-archive-{DATE}.md`.

### Skippable Artifacts

If certain phases were skipped (e.g., `--skip-pptx`), set those artifact
fields to `null` rather than omitting them.

---

## related-papers-scout — Phase 7: Archive Registration

**Trigger**: After Phase 6 (Slack Distribution) completes, or after
Phase 5 (Report) if Slack is skipped.

### What to Register

Register **each discovered paper** (up to 5) as a separate entry, plus
update the **input paper** if it exists.

#### Per Discovered Paper

| Field | Value |
|---|---|
| `id` | arXiv ID of the discovered paper |
| `title` | Title from Phase 4 deep dive summary |
| `authors` | Authors from Phase 4 |
| `institutions` | Institutions from Phase 3 scoring |
| `arxiv_url` | arXiv URL |
| `date_published` | Publication date if known |
| `date_archived` | Today |
| `tags` | Key terms from the discovered paper |
| `status` | `discovered` |
| `one_line_summary` | "왜 이 논문을 봐야 하는가" summary (first reason) |
| `artifacts` | `{}` (empty — no local artifacts yet) |
| `discovered_from` | Input paper's arXiv ID |
| `source_skill` | `related-papers-scout` |

#### Relationships

For each discovered paper, add a relationship:

```json
{
  "from": "{input-paper-id}",
  "to": "{discovered-paper-id}",
  "type": "related",
  "discovered_by": "related-papers-scout",
  "date_added": "{DATE}"
}
```

#### Input Paper Update

If the input paper exists in the index, update its `related_papers` array
with the IDs of all discovered papers.

If the input paper does NOT exist, register it with status `discovered`
and the available metadata.

### Implementation Steps

1. Load `outputs/papers/index.json` (create scaffold if missing).
2. For each of the top-N discovered papers:
   a. Check if `{discovered-id}` already exists — skip if yes.
   b. Append a new `discovered` entry.
   c. Append a relationship entry.
3. Update or create the input paper entry.
4. Save `index.json`.
5. Append memory entries for all newly registered papers.

---

## alphaxiv-paper-lookup — Post-Save Hook

**Trigger**: After saving the overview to `outputs/papers/{ID}-overview.md`.

### What to Register

| Field | Value |
|---|---|
| `id` | arXiv ID |
| `title` | Title from AlphaXiv overview |
| `authors` | Authors from overview |
| `arxiv_url` | `https://arxiv.org/abs/{ID}` |
| `date_archived` | Today |
| `tags` | Extract from overview topics |
| `status` | `overview-only` |
| `one_line_summary` | First paragraph of the overview |
| `artifacts.overview` | `outputs/papers/{ID}-overview.md` |
| `source_skill` | `alphaxiv-paper-lookup` |

### Dedup

If the paper already exists with a higher status (`reviewed`, `archived`),
only update `artifacts.overview` — do not downgrade status.

---

## nlm-arxiv-slides — Post-Download Hook

**Trigger**: After downloading the slide deck PDF.

### What to Register

| Field | Value |
|---|---|
| `id` | arXiv ID (extracted from URL) |
| `title` | Paper title from analysis |
| `arxiv_url` | `https://arxiv.org/abs/{ID}` |
| `date_archived` | Today |
| `status` | `reviewed` |
| `artifacts.nlm_slides` | `outputs/presentations/arxiv-{ID}-slides-{DATE}.pdf` |
| `artifacts.extracted_text` | `outputs/papers/arxiv-{ID}-analysis-{DATE}.md` |
| `nlm_notebook_id` | Notebook ID from the pipeline |
| `source_skill` | `nlm-arxiv-slides` |

### Dedup

If the paper already exists, merge artifacts (add `nlm_slides` and
`nlm_notebook_id` without overwriting existing fields). Promote status to
`reviewed` if it was lower.

---

## Error Handling for All Hooks

| Error | Behavior |
|-------|----------|
| `index.json` doesn't exist | Create empty scaffold and proceed |
| `index.json` parse error | Log warning, back up file, create fresh scaffold |
| Duplicate paper ID | Update existing entry (merge artifacts, keep higher status) |
| Write permission error | Log warning, do not block the source skill's output |
| Memory directory missing | Create `memory/sessions/` and proceed |
