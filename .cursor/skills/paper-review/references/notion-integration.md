# Notion Distribution

Detailed instructions for Phase 7 (Notion page creation) of the paper-review
pipeline. Creates a structured page hierarchy from generated analysis documents.

## Prerequisites

- `plugin-notion-workspace-notion` MCP server connected
- Parent page ID configured (default or `--notion-parent` override)
- All Phase 2-5 outputs exist (review markdown, perspective markdowns, DOCX, PPTX)

## Default Parent Page

| Workspace | Page Name | Page ID |
|---|---|---|
| ThakiCloud | 논문 리뷰 | `3209eddc34e6801b8921f55d85153730` |

Override with `--notion-parent <page_id>`.

## Content Formatting Rules

Notion-flavored Markdown differs from standard Markdown:

1. **No pipe tables** — Notion does NOT support `| col1 | col2 |` syntax.
   Convert all tables to bulleted lists or `<table>` HTML blocks.
2. **No frontmatter** — Strip any YAML frontmatter before inserting content.
3. **Title not in content** — The page title goes in `properties.title`, NOT
   in the content body. Do not duplicate the title as an `# H1` heading.
4. **Unicode safety** — Escape or remove Unicode characters that break JSON
   serialization (e.g., `\u` sequences in code blocks).

### Table Conversion Strategy

When the source markdown contains pipe tables, convert to structured text:

**Before (pipe table):**
```
| Metric | Value |
|--------|-------|
| Accuracy | 47.4% |
| Cost | $0.384 |
```

**After (Notion-compatible):**
```
**주요 지표**
- **Accuracy**: 47.4%
- **Cost**: $0.384
```

## Page Hierarchy

```
Parent Page (--notion-parent)
└── {Paper Title} 논문 분석 ({DATE})          ← Main overview page
    ├── 1. 논문 리뷰                           ← Phase 2 review
    ├── 2. PM 전략 분석                        ← pm-strategy
    ├── 3. 시장 조사 분석                      ← market-research
    ├── 4. Product Discovery 분석              ← discovery
    ├── 5. GTM 분석                            ← gtm
    ├── 6. 통계·방법론 리뷰                    ← statistics
    └── 7. 실행 계획 분석                      ← execution
```

## Step-by-Step

### 7.1 Create Main Overview Page

Build a summary page with paper metadata, key metrics, overall score, and
links to sub-pages (Notion auto-links child pages).

```
notion-create-pages(
  parent: { page_id: "<PARENT_PAGE_ID>" },
  pages: [{
    properties: { title: "{Paper Title} 논문 분석 ({DATE})" },
    content: "<overview content>"
  }]
)
```

Save the returned `page_id` for sub-page creation.

**Overview content template:**

```markdown
> **arXiv**: {paper-id}
> **저자**: {authors}
> **분석일**: {DATE}

---

## 한줄 요약

{One-paragraph Korean summary of the paper's core contribution and results}

---

## 핵심 수치

{Key metrics as bulleted list — accuracy, cost, training efficiency, etc.}

---

## 종합 평가 ({score}/10)

{Dimension scores as bulleted list — novelty, soundness, experiments, clarity, impact}

---

## 생성 문서 목록

아래 하위 페이지에서 각 분석 문서의 전체 내용을 확인할 수 있습니다.

1. **논문 리뷰** — {brief description}
2. **PM 전략 분석** — {brief description}
3. **시장 조사 분석** — {brief description}
4. **Product Discovery** — {brief description}
5. **GTM 분석** — {brief description}
6. **통계·방법론 리뷰** — {brief description}
7. **실행 계획** — {brief description}

---

> **참고**: DOCX와 PPTX 파일은 Notion API로 직접 업로드가 불가하여,
> 각 분석 내용을 하위 페이지로 정리했습니다. 원본 파일은
> `outputs/papers/` 및 `outputs/presentations/` 디렉토리에서 확인 가능합니다.
```

### 7.2 Create Sub-Pages (Parallel-Safe)

Create sub-pages under the main page. Each sub-page contains the full content
of one perspective markdown file, adapted to Notion format.

Launch up to 2 parallel `notion-create-pages` calls at a time to stay within
API rate limits.

| Sub-Page | Source File |
|---|---|
| 1. 논문 리뷰 | `{paper-id}-review-{DATE}.md` |
| 2. PM 전략 분석 | `{paper-id}-pm-strategy-{DATE}.md` |
| 3. 시장 조사 분석 | `{paper-id}-market-research-{DATE}.md` |
| 4. Product Discovery 분석 | `{paper-id}-discovery-{DATE}.md` |
| 5. GTM 분석 | `{paper-id}-gtm-{DATE}.md` |
| 6. 통계·방법론 리뷰 | `{paper-id}-statistics-{DATE}.md` |
| 7. 실행 계획 분석 | `{paper-id}-execution-{DATE}.md` |

For each sub-page:

1. Read the source markdown file
2. Strip YAML frontmatter (if any)
3. Convert pipe tables to bulleted lists
4. Remove the first `# H1` heading (it becomes the page title)
5. Truncate content if it exceeds ~60KB (Notion API limit per request)

```
notion-create-pages(
  parent: { page_id: "<MAIN_PAGE_ID>" },
  pages: [{
    properties: { title: "{N}. {Perspective Name}" },
    content: "<adapted markdown content>"
  }]
)
```

### 7.3 Capture Main Page URL

The `notion-create-pages` response includes the page URL. Save it for
inclusion in the Slack thread (Phase 8):

```
https://www.notion.so/{page_id_without_dashes}
```

## Content Adaptation Function

When converting markdown for Notion, apply these transformations in order:

1. **Strip frontmatter**: Remove everything between opening and closing `---`
2. **Convert tables**: Replace pipe tables with bulleted lists
3. **Fix headings**: Remove the first H1 (becomes page title); keep H2+ as-is
4. **Escape special chars**: Ensure no raw `\u` sequences in code blocks
5. **Trim length**: If content exceeds 60KB, truncate with a note:
   `\n\n---\n> ⚠️ 내용이 Notion API 제한으로 일부 잘렸습니다. 전체 내용은 원본 마크다운 파일을 참조하세요.`

## Skip Behavior

If `--skip-pm` was used (no Phase 3 outputs), create only:
- Main overview page
- Sub-page 1 (논문 리뷰)

If specific `--perspectives` were selected, create sub-pages only for
the perspectives that were actually generated.

## Error Handling

| Error | Fix |
|-------|-----|
| `Bad Unicode escape` | Re-serialize content; remove or escape `\u` in code blocks |
| `body.pages[0].content too long` | Truncate content to < 60KB |
| `Could not find page` | Verify parent page ID; check workspace permissions |
| `Rate limited` | Wait 1 second between calls; max 2 parallel |
| `Validation error` | Check for unsupported Markdown syntax (pipe tables, footnotes) |

## Notion Page URL in Slack Thread

After all Notion pages are created, include the main page URL in the Slack
thread (Phase 8, Step 8.5). See `nlm-slack-integration.md` for the exact
Slack message format.

## Skills Used

- **plugin-notion-workspace-notion** MCP server (`notion-create-pages` tool)
