---
name: kb-auto-builder
description: >-
  Automate Knowledge Base construction and maintenance — watch directories for
  new sources, subscribe to RSS/Atom feeds, schedule periodic compile and lint
  cycles, and run continuous enhancement loops. Transforms the KB from a
  manually-triggered system into a self-building knowledge engine. Use when
  the user asks to "auto-build KB", "watch for new sources", "subscribe feeds
  to KB", "continuous KB build", "kb auto-builder", "automated knowledge
  base", "set up KB automation", or wants their knowledge base to grow
  automatically from configured sources. Do NOT use for one-time manual
  ingestion (use kb-ingest). Do NOT use for one-time compilation (use
  kb-compile). Do NOT use for querying the KB (use kb-query). Korean triggers:
  "KB 자동 빌드", "지식베이스 자동화", "자동 지식베이스", "KB 피드 구독", "KB 감시 모드".
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

## Step 0: Read Schema (MANDATORY — All Modes)

Before executing ANY mode, read `_schema.md` from the KB root directory. Extract:

- **Conventions**: naming patterns, frontmatter template, preferred terminology
- **Automation Rules**: default watch directories, feed filters, enhancement depth preferences
- **Quality Gates**: thresholds for auto-ingest acceptance, compile triggers, lint severity
- **Domain Rules**: topic-specific constraints affecting automated operations

If `_schema.md` does not exist, warn the user and suggest running `kb-orchestrator init` first. Proceed with defaults if the user chooses to continue.

All sub-skills (kb-ingest, kb-compile, kb-lint, kb-index) invoked by auto-builder already enforce their own Step 0 schema reads, but the auto-builder reads the schema first to configure its orchestration behavior (e.g., which depth to use, whether to auto-compile).

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

Run a periodic cycle of lint → auto-fix → drift-check → schema-review → recompile → re-index to continuously improve the KB quality.

**Input:**
- `--topic` — target KB topic slug
- `--depth` — enhancement depth: `light` (fix trivial issues), `medium` (fix + new articles + drift), `deep` (fix + new articles + web search + schema review)

**Workflow:**
1. Run kb-lint (which includes Check 9: Schema Compliance and Check 10: Raw-Wiki Drift)
2. For each fixable issue:
   a. **Broken links**: fix or create stub articles
   b. **Missing frontmatter**: infer and add using `_schema.md` template
   c. **Orphan articles**: add backlinks
   d. **Schema violations**: auto-fix naming, frontmatter, terminology
   e. **Missing coverage** (medium/deep): create new concept articles
3. **Raw-Wiki Drift Resolution** (medium/deep):
   a. Identify uncovered raw sources → queue for compile
   b. Flag stale articles with newer sources → queue for recompile
   c. Investigate orphan concepts → verify or mark as derived
4. If depth is `deep`: run kb-lint `--impute` for web-sourced gap filling
5. **Schema Review** (deep only):
   a. Collect all `SCHEMA-SUGGEST` entries from `_log.md` with `status: pending-review`
   b. Present suggestions to user or auto-apply if low-risk (e.g., adding optional frontmatter fields)
   c. Update `_schema.md` version if changes applied
   d. Log `SCHEMA-APPLIED` or `SCHEMA-REJECTED` entries
6. Run kb-compile (incremental) for any new or updated articles
7. Run kb-index to refresh all indexes
8. Generate enhancement report with schema compliance summary

### Mode 4: `full-auto` — Complete Automation Pipeline

Combine watch + feed + enhance into a single schema-guided automated run.

**Input:**
- `--topic` — target KB topic slug
- All optional flags from modes 1-3

**Workflow:**
1. **Phase 0 — Schema Load**: Read `_schema.md` for automation preferences (depth, auto-compile, feed filters)
2. **Phase 1 — Collect**: Process watch directory + fetch all feeds (schema-guided filtering)
3. **Phase 2 — Build**: Run kb-compile (incremental) → kb-index (schema-validated)
4. **Phase 3 — Enhance**: Run enhance cycle with schema compliance + drift detection
5. **Phase 4 — Schema Review**: Process pending `SCHEMA-SUGGEST` entries (deep mode only)
6. **Phase 5 — Report**: Generate automation run summary with schema compliance metrics
7. Save run log to `outputs/auto-builder/run-{date}.md`

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
      "auto_file_back": true,
      "schema_review": true,
      "drift_check": true
    },
    "schema": {
      "auto_apply_low_risk": false,
      "review_interval_runs": 5,
      "last_schema_review": "2026-04-03T14:30:00Z"
    },
    "last_auto_run": "2026-04-03T14:30:00Z"
  }
}
```

## Auto File-Back Behavior

When `auto_file_back` is true in automation config:
- All kb-query answers are automatically saved to `wiki/queries/` (subject to schema quality gates)
- All kb-output artifacts are automatically linked in `wiki/outputs/` (subject to schema quality gates)
- kb-index runs after each file-back to keep indexes current
- **Layer Separation**: primary outputs go to `outputs/`, filed-back copies go to `wiki/` subdirectories
- **Schema Quality Gate**: file-back is skipped (output still saved to `outputs/`) if the generated content fails `_schema.md` quality gates (minimum citations, frontmatter compliance, confidence thresholds)

This implements the Karpathy "filed back to wiki" feedback loop as a schema-gated default behavior rather than an unconditional opt-in flag.

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

## Operations Log

After every auto-builder run, append to `_log.md` using the **grep-parseable H2 heading format**:

```markdown
## [2026-04-05 16:00] AUTO-WATCH | new_files: 3 | ingested: 3 | compiled: yes | topic: ml-fundamentals

## [2026-04-05 16:05] AUTO-FEED | feeds_checked: 2 | new_items: 7 | ingested: 5 | filtered: 2 | topic: ml-fundamentals

## [2026-04-05 16:10] AUTO-ENHANCE | depth: medium | lint_issues: 12 | fixed: 8 | schema_violations: 3 | drift_uncovered: 2 | drift_stale: 1

## [2026-04-05 16:15] AUTO-FULL | phases: collect|build|enhance|report | sources_added: 8 | articles_updated: 5 | schema_compliant: yes
```

Format per mode:
- `AUTO-WATCH`: `## [TS] AUTO-WATCH | new_files | ingested | compiled | topic`
- `AUTO-FEED`: `## [TS] AUTO-FEED | feeds_checked | new_items | ingested | filtered | topic`
- `AUTO-ENHANCE`: `## [TS] AUTO-ENHANCE | depth | lint_issues | fixed | schema_violations | drift_uncovered | drift_stale`
- `AUTO-FULL`: `## [TS] AUTO-FULL | phases | sources_added | articles_updated | schema_compliant`

If the auto-builder detects recurring patterns worth codifying, append schema co-evolution suggestions:

```markdown
## [2026-04-05 16:20] SCHEMA-SUGGEST | source: kb-auto-builder | rule: "Add 'arxiv' as accepted source_type for auto-ingest" | status: pending-review

## [2026-04-05 16:21] SCHEMA-SUGGEST | source: kb-auto-builder | rule: "Increase max_items to 10 for cs.AI feed based on ingestion rate" | status: pending-review
```

Schema review actions are logged as:

```markdown
## [2026-04-05 16:25] SCHEMA-APPLIED | rule: "Added 'arxiv' as source_type" | version: 1.0.0 → 1.1.0

## [2026-04-05 16:26] SCHEMA-REJECTED | rule: "Increase max_items" | reason: "User prefers smaller batches"
```

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No schema | `_schema.md` missing | Warn user, suggest `kb-orchestrator init`, proceed with defaults |
| Watch dir doesn't exist | Path not found | Create `inbox/` directory |
| Feed unreachable | HTTP error | Log and continue, retry next run |
| Duplicate source | URL already in manifest | Skip silently |
| Too many new items | > 20 new sources in one run | Process first 20, queue rest |
| Compile failure | Error during incremental compile | Log error, continue with other sources |
| Large file | Source > 100KB | Warn user, ingest with truncation note |
| Schema parse error | Malformed `_schema.md` | Report parse error, fall back to defaults |
| Schema review conflict | Contradictory SCHEMA-SUGGEST entries | Present both to user, do not auto-apply |
| File-back gate failed | Quality gates not met | Save to outputs/ only, log reason |
