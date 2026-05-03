---
name: nlm-obsidian-sync
description: >-
  NLM notebook -> Obsidian vault: wikilinked source notes, passage citations,
  Q&A logs, source dashboard. Triggers: "NLM 옵시디언 동기화", "노트북 볼트 내보내기",
  "NLM Obsidian export", "연구 결과 옵시디언". NOT for: vault CRUD
  (obsidian-files), NLM CRUD (notebooklm), KB bridge (obsidian-kb-bridge).
---

# NLM Obsidian Sync

Export a NotebookLM research session into a graph-ready Obsidian vault structure with passage-level citations and cross-linked notes.

## Prerequisites

- Obsidian CLI configured + vault open (`obsidian-setup`)
- Research data available (from `nlm-research-terminal` or manual)

## Input

| Parameter | Required | Source | Description |
|-----------|----------|--------|-------------|
| `topic` | Yes | user or caller skill | Research topic name |
| `slug` | Yes | derived | URL-safe topic slug |
| `notebook_id` | Yes | NLM | NotebookLM notebook ID |
| `sources_file` | No | `/tmp/nlm-research-{slug}-sources.json` | Source manifest |
| `qa_file` | No | `/tmp/nlm-research-{slug}-qa.json` | Q&A results |
| `vault_folder` | No | `Research/{slug}` | Target folder in vault |
| `artifacts` | No | list of file paths | Downloaded artifact paths |

## Output Structure

```
Research/{slug}/
├── _index.md                    # Notebook overview + navigation
├── _source-dashboard.md         # Citation frequency table + topics
├── _qa-log.md                   # All Q&A with inline citations
├── sources/
│   ├── {source-1-slug}.md       # Per-source note with metadata
│   ├── {source-2-slug}.md
│   └── ...
└── artifacts/
    ├── podcast.mp3              # Audio overview
    ├── mind-map.md              # Mind map (text representation)
    └── flashcards.md            # Flashcard deck
```

## Phase 1: Index Note

Create `_index.md`:

```markdown
---
type: research-notebook
topic: "{topic}"
notebook_id: "{notebook_id}"
created: {date}
source_count: {n}
tags:
  - research
  - nlm
---

# {topic}

## Sources

| # | Type | Title | Citations |
|---|------|-------|-----------|
| 1 | youtube | [[sources/{slug}|{title}]] | {count} |
| 2 | arxiv | [[sources/{slug}|{title}]] | {count} |
| ... |

## Quick Links

- [[_qa-log|Q&A Log]] ({question_count} questions)
- [[_source-dashboard|Source Dashboard]]
- [[artifacts/podcast|Audio Overview]]
- [[artifacts/mind-map|Mind Map]]
```

Create with:
```
obsidian create name="{vault_folder}/_index" content="..."
```

## Phase 2: Source Notes

For each source in the manifest, create a note:

```markdown
---
type: research-source
source_type: "{youtube|arxiv|web}"
url: "{original_url}"
notebook_id: "{notebook_id}"
citation_count: {n}
tags:
  - source/{type}
---

# {source_title}

**Type:** {youtube|arxiv|web}
**URL:** {url}
**Added:** {date}

## Citations in This Research

> "{passage_1}" — [[_qa-log#q1|Q1]]

> "{passage_2}" — [[_qa-log#q3|Q3]]

## Related Sources

- [[{other-source}]] — shared topic: {topic}
```

Create with:
```
obsidian create name="{vault_folder}/sources/{source-slug}" content="..."
```

## Phase 3: Q&A Log

Create `_qa-log.md` with all questions and cited answers:

```markdown
---
type: research-qa-log
topic: "{topic}"
question_count: {n}
total_citations: {n}
---

# Q&A Log: {topic}

## Q1: {question_text} {#q1}

{answer_text}

**Sources cited:**
- [[sources/{source-slug}|{source_title}]]: "{cited_passage}" ^cite-q1-1
- [[sources/{source-slug}|{source_title}]]: "{cited_passage}" ^cite-q1-2

---

## Q2: {question_text} {#q2}

{answer_text}

**Sources cited:**
- [[sources/{source-slug}|{source_title}]]: "{cited_passage}" ^cite-q2-1
```

Key rules:
- Every citation links back to the source note via `[[wikilink]]`
- Block references (`^cite-q1-1`) enable granular linking from other notes
- Heading anchors (`{#q1}`) enable linking from source notes

## Phase 4: Source Dashboard

Create `_source-dashboard.md`:

```markdown
---
type: research-dashboard
topic: "{topic}"
---

# Source Dashboard: {topic}

## Citation Frequency

| Source | Type | Citations | Questions Answered | Key Topics |
|--------|------|-----------|-------------------|------------|
| [[sources/{slug}|{title}]] | youtube | 8 | Q1, Q3, Q5 | attention, scaling |
| [[sources/{slug}|{title}]] | arxiv | 5 | Q2, Q4 | flash attention |
| [[sources/{slug}|{title}]] | web | 2 | Q1 | benchmarks |

## Never-Cited Sources

These sources were uploaded but never referenced in any answer:

- [[sources/{slug}|{title}]] — consider removing

## Topic Clusters

### Cluster 1: {topic_name}
- [[sources/{s1}]]
- [[sources/{s2}]]

### Cluster 2: {topic_name}
- [[sources/{s3}]]
- [[sources/{s4}]]

## Stats

- **Total sources:** {n}
- **Cited sources:** {n} ({pct}%)
- **Total citations:** {n}
- **Avg citations per question:** {n}
- **Most-cited source:** [[sources/{slug}|{title}]] ({n}x)
```

## Phase 5: Artifacts

Copy downloaded artifacts into the vault folder:

```bash
cp /tmp/nlm-research-{slug}-podcast.mp3 "{vault_path}/artifacts/"
```

For text-based artifacts (mind map, flashcards, study guide), create Obsidian notes:

```
obsidian create name="{vault_folder}/artifacts/mind-map" content="..."
obsidian create name="{vault_folder}/artifacts/flashcards" content="..."
```

For audio:
```
obsidian create name="{vault_folder}/artifacts/podcast" content="---\ntype: audio\n---\n\n![[podcast.mp3]]"
```

## Phase 6: Graph Optimization

After all notes created, verify link integrity:

```bash
obsidian backlinks file="{vault_folder}/_index"
obsidian links file="{vault_folder}/_index"
```

Expected graph structure:
- `_index` links to all source notes + qa-log + dashboard
- Each source note links to qa-log entries where cited
- qa-log links to source notes for each citation
- dashboard links to all source notes

## Standalone Usage

Can run independently on any existing NLM notebook:

1. Get notebook details: `notebook_get(notebook_id)`
2. Query for key topics: `notebook_query(notebook_id, "What are the main topics?")`
3. Build source manifest from `notebook_get` response
4. Run Q&A queries
5. Execute Phases 1-6

## Citation Matching

When NLM returns a cited answer, parse citations:
- Extract source name from citation markers
- Match to uploaded source by title similarity (fuzzy match)
- Extract quoted passage text
- Map to source note slug for wikilink generation

If citation cannot be matched to a source (< 60% title similarity), log as "unmatched citation" in dashboard.

## Error Handling

| Error | Recovery |
|-------|----------|
| Vault folder exists | Append timestamp suffix: `{slug}-{timestamp}` |
| Obsidian CLI timeout | Retry once; if still fails, write to local filesystem |
| Source manifest missing | Rebuild from `notebook_get(notebook_id)` |
| Q&A file missing | Run queries inline before export |
| Artifact copy fails | Log warning, skip artifact, continue |
