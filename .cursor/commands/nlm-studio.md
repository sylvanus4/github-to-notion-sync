## NotebookLM Studio

Generate content from NotebookLM notebooks — audio podcasts, video explainers, reports, quizzes, flashcards, mind maps, slide decks, infographics, and data tables.

### Usage

```
/nlm-studio                                    # interactive — choose notebook and content type
/nlm-studio audio <notebook>                   # generate a podcast (deep_dive format)
/nlm-studio audio <notebook> --format debate   # generate a debate-style podcast
/nlm-studio video <notebook>                   # generate a video explainer
/nlm-studio report <notebook>                  # generate a briefing doc
/nlm-studio quiz <notebook> --count 15         # generate a 15-question quiz
/nlm-studio flashcards <notebook>              # generate flashcards
/nlm-studio slides <notebook>                  # generate a slide deck
/nlm-studio infographic <notebook>             # generate an infographic
/nlm-studio download <notebook> <type>         # download generated artifact
```

### Execution

Read and follow `.cursor/skills/notebooklm-studio/SKILL.md`.

Use the `notebooklm-mcp` MCP server tools: `studio_create`, `studio_status`, `download_artifact`, `export_artifact`, `studio_revise`.

### Examples

Generate a podcast from a notebook:
```
/nlm-studio audio <notebook_id>
```

Create study materials:
```
/nlm-studio quiz <notebook_id> --count 20
/nlm-studio flashcards <notebook_id>
```

Generate and download a slide deck:
```
/nlm-studio slides <notebook_id>
```
