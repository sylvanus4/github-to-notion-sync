## Demo Forge

Auto-generate interactive product demos from code changes — HTML demo pages, video scripts, or slide decks for stakeholder presentations.

### Usage

```
/demo-forge                                # demo from uncommitted changes
/demo-forge HEAD~3..HEAD                   # demo from last 3 commits
/demo-forge --branch feature/auth          # demo from branch diff vs main
/demo-forge --mode html                    # interactive HTML page (default)
/demo-forge --mode script                  # video recording script
/demo-forge --mode slides                  # presentation-ready slides
/demo-forge --url http://localhost:3000    # base URL for screenshots
```

### Workflow

1. **Collect changes** — Gather diff from commits, branch, or working tree
2. **Classify** — Categorize as UI change, API change, bug fix, etc.
3. **Extract narratives** — Write non-technical feature descriptions
4. **Capture visuals** — Browser screenshots of before/after states (if available)
5. **Build output** — HTML demo page, video script, or slide deck
6. **Report** — Features showcased, screenshots captured, output path

### Execution

Read and follow the `demo-forge` skill (`.cursor/skills/demo-forge/SKILL.md`) for change classification, browser automation, and output templates.

### Examples

Sprint demo with screenshots:
```
/demo-forge --branch feature/search-v2 --url http://localhost:3000
```

Video script for stakeholder meeting:
```
/demo-forge HEAD~5..HEAD --mode script
```

Quick demo from current work:
```
/demo-forge
```
