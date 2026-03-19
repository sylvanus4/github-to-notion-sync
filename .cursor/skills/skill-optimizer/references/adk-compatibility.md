# ADK Compatibility Reference

Compatibility mapping between ThakiCloud SKILL.md format and Google ADK `load_skill_from_dir()` (v1.27.2, March 2026).

## Test Results

| Skill | Pattern | Complexity | ADK Load | References | Assets | Scripts |
|-------|---------|------------|----------|------------|--------|---------|
| `alphaear-stock` | Tool Wrapper | Simple | PASS | none | none | 3 files loaded |
| `deep-review` | Reviewer | Medium | PASS | 1 file loaded | none | none |
| `today` | Pipeline | Complex (26K chars) | PASS | 1 file loaded | none | none |

All three representative skills loaded successfully via `load_skill_from_dir()`.

## Structural Compatibility

### SKILL.md (Required)

| ThakiCloud Field | ADK Frontmatter Field | Status |
|------------------|----------------------|--------|
| `name` | `name` (required) | Compatible |
| `description` | `description` (required) | Compatible |
| `metadata.version` | `metadata["version"]` | Compatible (dict passthrough) |
| `metadata.category` | `metadata["category"]` | Compatible (dict passthrough) |
| `metadata.author` | `metadata["author"]` | Compatible (dict passthrough) |
| `license` | `license` (optional) | Compatible |
| — | `compatibility` (optional) | Available but unused; consider populating |
| — | `allowed_tools` (optional) | Available but unused; consider populating |
| Body (markdown) | `instructions` (str) | Compatible — full body loaded as instructions |

### Directory Structure

| ThakiCloud Directory | ADK Support | Notes |
|---------------------|-------------|-------|
| `references/*.md` | Loaded as `resources.references` dict | Keys = filenames, values = file content |
| `assets/**/*` | Loaded as `resources.assets` dict | Keys = relative paths, values = file content |
| `scripts/*.py` | Loaded as `resources.scripts` dict | **Script execution NOT supported** — ADK loads file content but cannot run scripts |
| `tests/` | Not loaded | ADK ignores non-standard directories |

### Key Observations

1. **Full compatibility for instructions + references + assets**: ADK loads all standard SKILL.md content correctly.
2. **Scripts loaded but not executable**: ADK reads `.py` files into the `scripts` dict but has no execution runtime. Scripts serve only as reference context.
3. **Large instruction bodies work**: The `today` skill (26K chars) loads without issues.
4. **Metadata passthrough**: ADK stores custom metadata keys in a generic dict, preserving all ThakiCloud fields.
5. **No `description` field truncation**: Full multi-line descriptions are preserved.

## Incompatibilities

| Issue | Severity | Workaround |
|-------|----------|------------|
| Script execution unsupported | Medium | Skills relying on `scripts/` for runtime functionality (e.g., `alphaear-stock/scripts/database_manager.py`) cannot execute in ADK. Move critical logic to the agent's toolset or MCP. |
| `tests/` directory ignored | Low | Test files are development-only; no impact on runtime. |
| Non-`.md` reference files | Low | ADK may not load non-markdown reference files. Use `.md` format for all references. |
| `LICENSE.txt` at skill root | None | Silently ignored by ADK loader. |

## Recommendations

### For ADK-portable skills

1. Keep `SKILL.md` as the single source of truth for instructions
2. Use `references/*.md` for domain context that should be loadable by ADK agents
3. Avoid relying on `scripts/` for runtime execution — treat scripts as reference-only documentation
4. Add `compatibility: "adk-v1.27+"` to frontmatter for skills verified as ADK-compatible
5. Use `allowed_tools` frontmatter field to document MCP tools the skill requires

### Frontmatter Template (ADK-Compatible)

```yaml
---
name: skill-name
description: >-
  One-paragraph description with WHAT, WHEN, and negative triggers.
metadata:
  version: "1.0.0"
  category: "category-name"
  author: "author-name"
compatibility: "adk-v1.27+, cursor-v1.0+"
allowed_tools: "WebSearch, Shell"
---
```

## ADK SDK Reference

```python
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

skill = load_skill_from_dir(pathlib.Path("path/to/skill"))

toolset = skill_toolset.SkillToolset(skills=[skill])

agent = Agent(
    model="gemini-2.5-flash",
    tools=[toolset],
)
```

Tested with: `google-adk==1.27.2`, Python 3.12.8, macOS Darwin 25.3.0
Test date: 2026-03-19
