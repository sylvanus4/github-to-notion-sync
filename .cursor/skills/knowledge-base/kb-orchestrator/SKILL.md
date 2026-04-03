---
name: kb-orchestrator
description: >-
  Master orchestrator for the LLM Knowledge Base system. Coordinates all
  KB skills (ingest, compile, index, query, output, lint, search,
  auto-builder) into coherent workflows. Supports multiple modes: init
  (create new KB), build (ingest + compile), query, enhance (lint + fix
  + recompile), full-pipeline, add, status, watch (directory monitoring),
  feed (RSS subscription), and auto (continuous build cycle).
  Based on Karpathy's LLM Knowledge Bases approach.
  Use when the user asks to "create a knowledge base", "build KB",
  "knowledge base", "kb", "start a new KB", "full KB pipeline",
  "enhance KB", "watch KB", "auto-build KB", "subscribe feed to KB",
  or any high-level KB operation spanning multiple skills.
  Do NOT use for individual KB operations (invoke specific kb-* skills).
  Korean triggers: "지식베이스", "KB 생성", "KB 빌드",
  "KB 파이프라인", "지식베이스 시작", "KB 자동", "KB 감시".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "orchestration"
  tags: ["knowledge-base", "orchestrator", "pipeline", "automation"]
---

# KB Orchestrator — LLM Knowledge Base Pipeline

Master orchestrator for building and maintaining personal LLM Knowledge Bases. Implements the full lifecycle described by Karpathy: raw data collection → wiki compilation → Q&A → output generation → linting → enhancement loop.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      KB Orchestrator                          │
│                                                              │
│  ┌───────────────┐                                           │
│  │kb-auto-builder│ (watch / feed / enhance / full-auto)      │
│  └──────┬────────┘                                           │
│         ↓                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │kb-ingest │→ │kb-compile│→ │ kb-index │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
│       ↑                           ↓                           │
│  ┌──────────┐              ┌──────────┐                      │
│  │ kb-lint  │←─────────────│ kb-query │ ──→ file-back ──┐   │
│  └──────────┘              └──────────┘                  │   │
│       ↓                         ↓                        ↓   │
│  ┌──────────┐              ┌──────────┐          wiki/       │
│  │kb-search │              │kb-output │ ──→ file-back ──┘   │
│  └──────────┘              └──────────┘                      │
└──────────────────────────────────────────────────────────────┘
```

## Modes

### Mode 1: `init` — Create New Knowledge Base

Create a fresh KB topic with directory structure and manifest.

**Trigger:** "Create a new KB for {topic}", "Init KB", "Start a new knowledge base"

**Steps:**
1. Ask for topic name and optional description
2. Create directory structure:
   ```
   knowledge-bases/{topic}/
   ├── raw/
   │   └── assets/
   ├── wiki/
   │   ├── concepts/
   │   ├── references/
   │   ├── connections/
   │   ├── queries/
   │   └── images/
   └── outputs/
       ├── slides/
       ├── charts/
       ├── reports/
       ├── diagrams/
       └── explainers/
   ```
3. Create `manifest.json` with topic metadata
4. Report the created structure

### Mode 2: `build` — Ingest Sources + Compile Wiki

Full build from sources to wiki.

**Trigger:** "Build KB from these sources", "Ingest and compile", "Create wiki from articles"

**Steps:**
1. **kb-ingest**: Process all provided source URLs/files
2. **kb-compile**: Compile raw sources into structured wiki
3. **kb-index**: Generate index files
4. Report final stats

### Mode 3: `query` — Research + Answer

Answer questions against the KB.

**Trigger:** "Ask the KB about X", "Query KB", "What does my KB say about"

**Steps:**
1. **kb-search**: Find relevant articles
2. **kb-query**: Deep read + synthesize answer
3. Optionally **kb-output**: Generate formatted output
4. Optionally file result back into wiki

### Mode 4: `enhance` — Lint + Fix + Recompile

Improve wiki quality through automated health checks and fixes.

**Trigger:** "Enhance my KB", "Improve KB quality", "Clean up the wiki"

**Steps:**
1. **kb-lint**: Run health checks (`--impute` for web-enriched gaps)
2. Auto-fix trivial issues (missing frontmatter, broken links)
3. **kb-compile** (incremental): Recompile affected articles
4. **kb-index**: Rebuild indexes
5. Report improvements

### Mode 5: `full-pipeline` — End-to-End

Complete pipeline from sources to outputs.

**Trigger:** "Full KB pipeline", "Build everything", "Complete KB workflow"

**Steps:**
1. **init**: Ensure directory structure
2. **kb-ingest**: Process all sources
3. **kb-compile**: Build wiki
4. **kb-index**: Generate indexes
5. **kb-lint**: Run health checks
6. Auto-fix issues
7. **kb-output**: Generate requested outputs (slides, reports)
8. Report comprehensive summary

### Mode 6: `add` — Quick Add + Incremental Compile

Add a single source and immediately update the wiki.

**Trigger:** "Add this to my KB: {url}", "Quick add to KB"

**Steps:**
1. **kb-ingest**: Ingest the single source
2. **kb-compile** (incremental): Update affected wiki articles
3. **kb-index**: Refresh indexes
4. Report what changed

### Mode 7: `status` — KB Overview

Show the current state of a KB topic.

**Trigger:** "KB status", "How big is my KB", "KB overview"

**Steps:**
1. Read `manifest.json`
2. Count files in raw/ and wiki/
3. Read `_summary.md` for quick overview
4. Present dashboard:

```
📚 Knowledge Base: {topic}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sources:     {N} raw documents
Wiki:        {M} articles (~{W}K words)
  Concepts:  {C}
  References:{R}
  Connections:{X}
Last built:  {date}
Last lint:   {date}
Outputs:     {O} artifacts
```

### Mode 8: `watch` — Directory Watcher

Monitor a directory for new source files and auto-ingest them.

**Trigger:** "Watch my clippings folder for the KB", "Watch for new sources", "KB watch mode"

**Steps:**
1. Delegate to **kb-auto-builder** `watch` mode
2. New files → kb-ingest → kb-compile (incremental) → kb-index
3. Report what was added

### Mode 9: `feed` — RSS/Atom Feed Subscription

Subscribe to feeds and auto-ingest new entries.

**Trigger:** "Subscribe arxiv feed to my KB", "Add RSS feed to KB", "KB feed mode"

**Steps:**
1. Delegate to **kb-auto-builder** `feed` mode
2. New entries → defuddle → kb-ingest → kb-compile (incremental) → kb-index
3. Report ingested entries

### Mode 10: `auto` — Continuous Build Cycle

Run the full automation cycle: collect → build → enhance → report.

**Trigger:** "Auto-build my KB", "Run continuous KB cycle", "Full auto KB"

**Steps:**
1. Delegate to **kb-auto-builder** `full-auto` mode
2. Phase 1: Check watch dirs + fetch feeds
3. Phase 2: Compile + index
4. Phase 3: Enhance (lint + auto-fix)
5. Phase 4: Report summary
6. Save run log to `outputs/auto-builder/`

## Cross-KB Operations

### List All KBs

```bash
ls -d knowledge-bases/*/
```

### Cross-KB Query

Query across multiple KBs simultaneously:

1. Read `_index.md` from each KB
2. Identify relevant KBs for the question
3. Run kb-query on each relevant KB
4. Synthesize cross-KB answer

## Integration Points

| Skill | Integration |
|-------|------------|
| **defuddle** | Web content extraction for kb-ingest |
| **anthropic-pdf** | PDF content extraction for kb-ingest |
| **alphaxiv-paper-lookup** | Paper overview for kb-ingest |
| **cognee** | Optional graph-enhanced search for kb-search |
| **visual-explainer** | HTML output generation for kb-output |
| **anthropic-pptx** | PPTX generation for kb-output |
| **anthropic-docx** | DOCX report generation for kb-output |
| **parallel-web-search** | Web research for kb-lint --impute |
| **md-to-notion** | Publish wiki to Notion |
| **nlm-slides** | Generate NotebookLM slides from KB |
| **kb-auto-builder** | Automated ingestion via watch dirs, feeds, enhancement loops |

## Examples

### Example 1: Create and build a new KB

**User says:** "Create a knowledge base about reinforcement learning from these papers: [url1, url2, url3, url4, url5]"

**Actions:**
1. `init` mode: Create KB directories for "reinforcement-learning"
2. `build` mode: Ingest 5 papers, compile wiki, build index
3. Report: "KB ready with {N} concepts, {M} articles"

### Example 2: Daily KB enhancement

**User says:** "I added some new papers to the RL KB, update and enhance it"

**Actions:**
1. Detect new raw files not yet in manifest
2. `add` mode for each new file
3. `enhance` mode: lint + fix + recompile
4. Report improvements

### Example 3: Generate a presentation from KB

**User says:** "Create slides from my transformer-architectures KB"

**Actions:**
1. `query` mode: Read KB for key themes
2. `output` mode: Generate Marp slides
3. Report file location

### Example 4: Cross-KB research

**User says:** "Across all my KBs, what are the most promising research directions?"

**Actions:**
1. List all KBs
2. Read each `_summary.md`
3. Synthesize cross-KB themes
4. Present ranked recommendations

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| KB doesn't exist | Topic directory not found | Offer to create with `init` |
| Empty raw/ | No sources ingested | Prompt to use kb-ingest |
| Stale wiki | Wiki older than newest raw source | Suggest `enhance` or `build` |
| Missing dependencies | Skill or tool unavailable | List alternatives, degrade gracefully |
