## NotebookLM Podcast

End-to-end pipeline: create a NotebookLM notebook, add sources, generate a podcast, and download.

### Usage

```
/nlm-podcast "Topic Title" --url "https://..."                  # from a URL
/nlm-podcast "Topic Title" --file "/path/to/report.docx"        # from a local file
/nlm-podcast "Topic Title" --research "search query"             # from web research
/nlm-podcast today                                               # from today's daily stock report
```

### Execution

This command combines the `notebooklm` and `notebooklm-studio` skills:

1. Read `.cursor/skills/notebooklm/SKILL.md` for notebook/source operations
2. Read `.cursor/skills/notebooklm-studio/SKILL.md` for audio generation

### Pipeline Steps

1. **Create notebook**: `notebook_create(title="...")`
2. **Add sources**: `source_add(notebook_id, ...)` with `wait=True`
3. **Generate audio**: `studio_create(notebook_id, artifact_type="audio", format="deep_dive", confirm=True)`
4. **Poll status**: `studio_status(notebook_id)` every 30s until complete
5. **Download**: `download_artifact(notebook_id, artifact_type="audio", output_path="outputs/podcasts/<name>.mp3")`

### Examples

Podcast from today's daily stock report:
```
/nlm-podcast today
```
This creates a notebook from `outputs/reports/daily-YYYY-MM-DD.docx` and generates a deep-dive podcast.

Podcast from a URL:
```
/nlm-podcast "AI Market Analysis" --url "https://example.com/article"
```

Podcast from web research:
```
/nlm-podcast "Fed Rate Decision" --research "Federal Reserve rate decision March 2026"
```
