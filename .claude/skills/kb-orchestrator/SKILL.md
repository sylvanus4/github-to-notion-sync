---
name: kb-orchestrator
description: Master orchestrator for the LLM Knowledge Base — supports init, bootstrap, build, query, enhance, full-pipeline, and auto modes.
disable-model-invocation: true
arguments: [mode, topic]
---

Orchestrate Knowledge Base operations in `$mode` mode for topic `$topic`.

## Modes

| Mode | Description |
|------|-------------|
| init | Create new KB topic directory structure |
| bootstrap | Zero-to-working KB with auto source discovery |
| build | Ingest raw sources + compile wiki |
| query | Ask questions against compiled wiki |
| enhance | Lint + fix gaps + recompile |
| full-pipeline | init → build → index → lint → enhance |
| add | Ingest a single source into existing topic |
| status | Show KB health summary |
| watch | Monitor directory for new sources |
| auto | Continuous build cycle |

## KB Structure

```
knowledge-bases/<topic>/
├── raw/                    # Source documents (markdown + YAML frontmatter)
├── wiki/                   # LLM-compiled interconnected articles
│   ├── _index.md
│   ├── _summary.md
│   └── articles/
├── connections/            # Cross-article relationship docs
└── outputs/                # Generated artifacts
```

## Karpathy KB Approach

- Raw sources are ingested with provenance metadata
- Wiki articles are entirely LLM-authored from raw sources
- Cross-references and backlinks maintain knowledge graph
- Freshness scoring ensures content stays current
