---
name: kb-auto-builder
description: >-
  Automate Knowledge Base construction and maintenance — watch directories
  for new sources, subscribe to RSS/Atom feeds, schedule periodic compile
  and lint cycles, and run continuous enhancement loops. Transforms the KB
  from a manually-triggered system into a self-building knowledge engine.
  Use when the user asks to "auto-build KB", "watch for new sources",
  "subscribe feeds to KB", "continuous KB build", "kb auto-builder",
  "automated knowledge base", "set up KB automation", or wants their
  knowledge base to grow automatically from configured sources.
  Do NOT use for one-time manual ingestion (use kb-ingest).
  Do NOT use for one-time compilation (use kb-compile).
  Do NOT use for querying the KB (use kb-query).
  Korean triggers: "KB 자동 빌드", "지식베이스 자동화",
  "자동 지식베이스", "KB 피드 구독", "KB 감시 모드".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "automation", "watch", "feeds", "continuous"]
---

# KB Auto-Builder — Automated Knowledge Base Construction

Transform a Knowledge Base from a manually-triggered collection into a self-building knowledge engine. Monitors directories for new sources, subscribes to RSS/Atom feeds, runs scheduled compile and lint cycles, and operates a continuous enhancement loop.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     KB Auto-Builder                      │
│                                                         │
│  ┌─────────────┐   ┌────────────────┐  ┌────────────┐ │
│  │ Dir Watcher  │   │ Feed Subscriber│  │  Scheduler │ │
│  │ (raw/ watch) │   │ (RSS/Atom/URL) │  │ (periodic) │ │
│  └──────┬──────┘   └───────┬────────┘  └─────┬──────┘ │
│         │                  │                  │         │
│         ▼                  ▼                  ▼         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Event Queue (manifest.json)          │  │
│  └───────────────────────┬──────────────────────────┘  │
│                          │                              │
│         ┌────────────────┼───────────────┐              │
│         ▼                ▼               ▼              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │kb-ingest │    │kb-compile│    │ kb-lint  │         │
│  └──────────┘    └──────────┘    └──────────┘         │
│                          │                              │
│                          ▼                              │
│                   ┌──────────┐                          │
│                   │ kb-index │                          │
│                   └──────────┘                          │
└─────────────────────────────────────────────────────────┘
```

## Modes

### Mode 1: `watch` — Directory Watcher

Monitor a directory (typically an Obsidian vault's clippings folder or a Downloads path) for new `.md` or `.pdf` files. When a new file appears, auto-ingest it.

**Input:**
- `--topic` — target KB topic slug
- `--watch-dir` — path to watch (default: `knowledge-bases/{topic}/inbox/`)
- `--interval` — poll interval in seconds (default: 30)
- `--auto-compile` — also run kb-compile after ingesting (default: false)

**Workflow:**
1. Read `manifest.json` to get the current source list
2. List files in the watch directory
3. Compare against manifest — identify new files
4. For each new file:
   a. Move/copy to `raw/`
   b. Run kb-ingest processing (convert, add frontmatter, download assets)
   c. Update manifest
5. If `--auto-compile`: run kb-compile (incremental) → kb-index
6. Report what was ingested

**Integration with Obsidian Web Clipper:**

Set `--watch-dir` to the Obsidian vault's web clippings path:

```bash
# Typical Obsidian Web Clipper output
--watch-dir ~/ObsidianVault/Clippings/
```

The watcher detects new clips, copies them to `raw/`, converts to the KB format, and optionally compiles them into the wiki.

### Mode 2: `feed` — RSS/Atom Feed Subscriber

Subscribe to RSS/Atom feeds and auto-ingest new articles.

**Input:**
- `--topic` — target KB topic slug
- `--feed-url` — RSS/Atom feed URL (can specify multiple)
- `--filter` — keyword filter for relevant entries (optional)
- `--max-items` — max items per fetch (default: 10)

**Workflow:**
1. Fetch the RSS/Atom feed via WebFetch
2. Parse entries (title, link, published date, summary)
3. Filter entries by `--filter` keywords if specified
4. Check against manifest to skip already-ingested URLs
5. For each new entry:
   a. Extract full content via defuddle
   b. Run kb-ingest on the extracted content
   c. Update manifest with source URL
6. Optionally run kb-compile (incremental) → kb-index
7. Report what was ingested

**Feed configuration in manifest.json:**

```json
{
  "automation": {
    "feeds": [
      {
        "url": "https://arxiv.org/rss/cs.AI",
        "filter": "transformer|attention|language model",
        "max_items": 5,
        "last_fetched": "2026-04-03"
      }
    ]
  }
}
```

### Mode 3: `enhance` — Continuous Enhancement Loop

Run a periodic cycle of lint → auto-fix → recompile → re-index to continuously improve the KB quality.

**Input:**
- `--topic` — target KB topic slug
- `--depth` — enhancement depth: `light` (fix trivial issues), `medium` (fix + new articles), `deep` (fix + new articles + web search)

**Workflow:**
1. Run kb-lint with severity threshold based on depth
2. For each fixable issue:
   a. **Broken links**: fix or create stub articles
   b. **Missing frontmatter**: infer and add
   c. **Orphan articles**: add backlinks
   d. **Missing coverage** (medium/deep): create new concept articles
3. If depth is `deep`: run kb-lint `--impute` for web-sourced gap filling
4. Run kb-compile (incremental) for any new or updated articles
5. Run kb-index to refresh all indexes
6. Generate enhancement report

### Mode 4: `full-auto` — Complete Automation Pipeline

Combine watch + feed + enhance into a single automated run.

**Input:**
- `--topic` — target KB topic slug
- All optional flags from modes 1-3

**Workflow:**
1. **Phase 1 — Collect**: Process watch directory + fetch all feeds
2. **Phase 2 — Build**: Run kb-compile (incremental) → kb-index
3. **Phase 3 — Enhance**: Run enhance cycle (light by default)
4. **Phase 4 — Report**: Generate automation run summary
5. Save run log to `outputs/auto-builder/run-{date}.md`

## Automation Configuration

The `manifest.json` gains an `automation` section:

```json
{
  "automation": {
    "watch_dirs": [
      "~/ObsidianVault/Clippings/",
      "knowledge-bases/{topic}/inbox/"
    ],
    "feeds": [
      {
        "url": "https://arxiv.org/rss/cs.AI",
        "filter": "transformer|attention",
        "max_items": 5,
        "last_fetched": "2026-04-03"
      }
    ],
    "enhance": {
      "depth": "light",
      "auto_file_back": true
    },
    "last_auto_run": "2026-04-03T14:30:00Z"
  }
}
```

## Auto File-Back Behavior

When `auto_file_back` is true in automation config:
- All kb-query answers are automatically saved to `wiki/queries/`
- All kb-output artifacts are automatically linked in `wiki/outputs/`
- kb-index runs after each file-back to keep indexes current

This implements the Karpathy "filed back to wiki" feedback loop as a default behavior rather than an opt-in flag.

## Examples

### Example 1: Watch an Obsidian clippings folder

**User says:** "Watch my Obsidian clippings for new ML articles and add them to the ML KB"

**Actions:**
1. Set up watcher on `~/ObsidianVault/Clippings/`
2. Scan for new `.md` files not in manifest
3. Ingest each new clip
4. Incrementally compile into wiki
5. Report what was added

### Example 2: Subscribe to arXiv feed

**User says:** "Subscribe the ML KB to the arXiv cs.AI feed, filter for transformer papers"

**Actions:**
1. Add feed config to manifest.json
2. Fetch the RSS feed
3. Filter for "transformer" in titles/abstracts
4. Ingest matching papers via defuddle → kb-ingest
5. Compile and index
6. Report ingested papers

### Example 3: Run full automation

**User says:** "Auto-build my ML KB: check for new clips, fetch feeds, enhance quality"

**Actions:**
1. Phase 1: Check watch dirs for new files, fetch feeds
2. Phase 2: Compile and index new content
3. Phase 3: Run light enhancement cycle
4. Phase 4: Generate summary report

### Example 4: Periodic enhancement

**User says:** "Deep enhance my KB — find gaps and fill them from the web"

**Actions:**
1. Run kb-lint with `--impute`
2. Auto-fix trivial issues
3. Create articles for top missing concepts
4. Web search for imputable gaps
5. Ingest found sources
6. Recompile and reindex

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Watch dir doesn't exist | Path not found | Create `inbox/` directory |
| Feed unreachable | HTTP error | Log and continue, retry next run |
| Duplicate source | URL already in manifest | Skip silently |
| Too many new items | > 20 new sources in one run | Process first 20, queue rest |
| Compile failure | Error during incremental compile | Log error, continue with other sources |
| Large file | Source > 100KB | Warn user, ingest with truncation note |
