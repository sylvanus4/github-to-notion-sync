# AutoResearchClaw — Distribution Channels

## Channel Configuration Summary

| Channel | Skill Used | Target | Skip Flag |
|---|---|---|---|
| Paper Archive | `paper-archive` | `output/papers/` index | N/A (always runs) |
| Notion | `md-to-notion` | Parent: `3209eddc34e6801b8921f55d85153730` | `--skip-notion` |
| PPTX | `anthropic-pptx` | `<artifacts>/deliverables/presentation.pptx` | `--skip-pptx` |
| NotebookLM | `notebooklm` + `notebooklm-studio` | New NLM notebook | `--skip-nlm` |
| Slack | Slack MCP (`plugin-slack-slack`) | `#deep-research` (`C0A6X68LTN1`) | `--skip-slack` |

## Artifact-to-Channel Mapping

| Artifact File | Archive | Notion | PPTX | NLM | Slack |
|---|---|---|---|---|---|
| `paper_final.md` | Metadata | Full page | Source content | Text source | Summary excerpt |
| `paper.tex` | Path ref | — | — | — | File path link |
| `references.bib` | Citation count | — | — | — | Citation stats |
| `code/` | — | — | — | — | — |
| `charts/` | — | — | Embedded images | — | — |
| `verification_report.json` | Verify score | — | — | — | Stats in header |
| `manifest.json` | Run metadata | — | — | — | — |
| `pipeline_summary.json` | Quality score | Properties | — | — | Header stats |

## Paper Archive Entry Format

```json
{
  "id": "<run-id>",
  "paper_type": "generated",
  "title": "<extracted from paper_final.md H1>",
  "abstract": "<extracted abstract>",
  "domains": ["<from config.research.domains>"],
  "conference_target": "<from config.export.target_conference>",
  "quality_score": "<from pipeline_summary.json>",
  "citation_verify_score": "<from pipeline_summary.json>",
  "experiment_mode": "<from config.experiment.mode>",
  "date": "<run date>",
  "artifacts": {
    "markdown": "<path to paper_final.md>",
    "latex": "<path to paper.tex>",
    "bib": "<path to references.bib>",
    "pptx": "<path to presentation.pptx>"
  }
}
```

## Notion Page Structure

```
Research (Parent: 3209eddc34e6801b8921f55d85153730)
└── [AutoResearch] <Paper Title>
    ├── Properties:
    │   ├── Run ID: <run-id>
    │   ├── Conference: <target>
    │   ├── Quality: <score>/10
    │   ├── Citations: <verified>/<total>
    │   └── Date: <YYYY-MM-DD>
    └── Content:
        └── Full paper_final.md content
            (split into sub-pages if > 15KB)
```

## Slack Thread Format

### Message 1 (Main — Channel)

```
🔬 *AutoResearch Complete: <title>*
📊 Run: `<run-id>` | Mode: `<mode>` | Conference: `<target>`
✅ Quality: <score>/10 | Citations: <verified>/<total> verified
```

### Message 2 (Thread — Key Findings)

```
📝 *Key Findings*

1. <finding-1 from abstract/results>
2. <finding-2>
3. <finding-3>

*Abstract*: <first 500 chars of abstract>
```

### Message 3 (Thread — Deliverables & Links)

```
📎 *Deliverables*
• 📄 Notion: <notion-url>
• 📊 PPTX: `<pptx-path>`
• 📝 LaTeX: `<tex-path>`
• 🎓 NotebookLM: <nlm-url>
• 📚 Paper Archive: Registered as `<archive-id>`

*Run artifacts*: `<run-dir>/deliverables/`
```

## NotebookLM Artifacts

Generated via `notebooklm-studio` after notebook creation:

| Artifact | Type | Purpose |
|---|---|---|
| Slide deck | `slides` | Quick visual review of paper |
| Audio podcast | `audio` | Commute-friendly paper summary |

Naming convention: `[AutoResearch] <paper-title>`
