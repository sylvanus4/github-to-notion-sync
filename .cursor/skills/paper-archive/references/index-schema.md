# Paper Archive Index Schema

JSON schema for `outputs/papers/index.json` — the central catalog of all
archived papers.

## Top-Level Structure

```json
{
  "version": "1.0.0",
  "updated_at": "ISO 8601 timestamp",
  "papers": [ PaperEntry, ... ],
  "relationships": [ Relationship, ... ]
}
```

- `version` — Schema version. Bump minor for additive changes, major for
  breaking changes.
- `updated_at` — Automatically set to current ISO 8601 timestamp on every
  write operation.

## PaperEntry

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Primary key. arXiv ID (e.g. `2603.03823`) for arXiv papers; slugified title hash for non-arXiv papers (e.g. `attention-is-all-you-need`) |
| `title` | string | yes | Full paper title in original language |
| `title_ko` | string | no | Korean title if available from review |
| `authors` | string[] | yes | Author list. Use "Lastname, Firstname" format |
| `institutions` | string[] | no | Affiliating institutions (e.g. `["Google DeepMind", "Stanford"]`) |
| `arxiv_url` | string | no | Full arXiv abstract URL |
| `arxiv_category` | string | no | Primary arXiv category (e.g. `cs.CL`) |
| `date_published` | string | no | Paper publication date (YYYY-MM-DD) |
| `date_archived` | string | yes | Date added to the archive (YYYY-MM-DD) |
| `tags` | string[] | yes | Topic tags for search/filter. Lowercase, hyphenated (e.g. `["llm-agents", "code-generation"]`) |
| `status` | enum | yes | One of: `discovered`, `overview-only`, `reviewed`, `archived` |
| `one_line_summary` | string | no | Single sentence summary (Korean preferred) |
| `artifacts` | ArtifactMap | yes | Relative paths to generated files |
| `notion_page_id` | string | no | Notion page ID if synced |
| `nlm_notebook_id` | string | no | NotebookLM notebook ID if synced |
| `related_papers` | string[] | no | IDs of related papers in this archive |
| `discovered_from` | string | no | ID of the paper that led to discovering this one (via related-papers-scout) |
| `source_skill` | string | yes | Skill that created this entry: `paper-review`, `related-papers-scout`, `alphaxiv-paper-lookup`, `nlm-arxiv-slides`, `manual` |

## ArtifactMap

All paths are relative to the project root.

| Field | Type | Description |
|---|---|---|
| `review` | string | Paper review markdown |
| `pm_analyses` | string[] | PM perspective analysis markdowns |
| `docx` | string | Consolidated Word report |
| `pptx` | string | PowerPoint presentation |
| `nlm_slides` | string | NotebookLM slide deck PDF |
| `overview` | string | AlphaXiv overview markdown |
| `related_report` | string | Related papers scout report |
| `extracted_text` | string | Raw extracted paper text |

All fields are optional — a `discovered` paper may have no artifacts yet.

## Relationship

| Field | Type | Required | Description |
|---|---|---|---|
| `from` | string | yes | Source paper ID |
| `to` | string | yes | Target paper ID |
| `type` | enum | yes | One of: `cites`, `extends`, `contradicts`, `related`, `supersedes` |
| `discovered_by` | string | yes | Skill or agent that identified this relationship |
| `date_added` | string | yes | Date the relationship was recorded (YYYY-MM-DD) |

## Status Lifecycle

```
discovered ──────► overview-only ──────► reviewed ──────► archived
   │                    │                    │
   │  alphaxiv-lookup   │   paper-review     │  sync-nlm + sync-notion
   │                    │                    │
   └────────────────────┴────────────────────┘
         Can jump directly to any later status
```

- **discovered** — Found by related-papers-scout but not yet reviewed.
  Minimal metadata only (title, authors, arxiv_url).
- **overview-only** — AlphaXiv overview fetched. Has `artifacts.overview`.
- **reviewed** — Full paper-review completed. Has `artifacts.review`,
  `artifacts.pm_analyses`, `artifacts.docx`, etc.
- **archived** — Reviewed AND synced to NotebookLM Paper Library notebook
  AND Notion database. Has `nlm_notebook_id` and `notion_page_id`.

## Validation Rules

1. `id` must be unique across all papers.
2. `status` must be a valid enum value.
3. `date_archived` must be a valid YYYY-MM-DD string.
4. `artifacts` paths, when present, should point to existing files (warn on
   missing, do not reject).
5. `relationships[].from` and `relationships[].to` must reference existing
   paper IDs (warn on dangling references).
6. `tags` must be lowercase with hyphens (no spaces, no uppercase).

## Migration Strategy

- **v1.0 → v1.1**: Additive fields only. Old index files are valid v1.1.
  New fields default to `null`.
- **Major version bump**: Write a migration script at
  `scripts/paper-archive/migrate-v{N}.py` that transforms the old index to
  the new schema. Keep a backup at `outputs/papers/index.v{N-1}.json`.
- If the corpus exceeds ~500 papers, consider migrating to SQLite at
  `outputs/papers/archive.db` with the same field structure.
