# ADK Compatibility Reference

Compatibility mapping between this workspace's SKILL.md format and Google ADK `load_skill_from_dir()` (v1.27.2, March 2026).

## Test Results (representative)

| Skill | Pattern | Complexity | ADK Load | References | Assets | Scripts |
|-------|---------|------------|----------|------------|--------|---------|
| `meeting-digest` | Pipeline | Medium | PASS | loaded | optional | optional |
| `doc-quality-gate` | Reviewer | Medium | PASS | loaded | none | none |
| `prd-research-factory` | Pipeline | Complex | PASS | loaded | none | none |

Representative planning-automation skills load successfully via `load_skill_from_dir()` when frontmatter and `references/` follow standard layout.

## Structural Compatibility

### SKILL.md (Required)

| Workspace field | ADK frontmatter field | Status |
|-----------------|----------------------|--------|
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

| Workspace directory | ADK support | Notes |
|--------------------|-------------|-------|
| `references/*.md` | Loaded as `resources.references` dict | Keys = filenames, values = file content |
| `assets/**/*` | Loaded as `resources.assets` dict | Keys = relative paths, values = file content |
| `scripts/*.py` | Loaded as `resources.scripts` dict | **Script execution NOT supported** — ADK loads file content but cannot run scripts |
| `tests/` | Not loaded | ADK ignores non-standard directories |

### Key Observations

1. **Full compatibility for instructions + references + assets**: ADK loads all standard SKILL.md content correctly.
2. **Scripts loaded but not executable**: ADK reads `.py` files into the `scripts` dict but has no execution runtime. Scripts serve only as reference context.
3. **Large instruction bodies work** if within team guidelines (prefer progressive disclosure; see audit checklist).
4. **Metadata passthrough**: ADK stores custom metadata keys in a generic dict, preserving workspace fields.
5. **No `description` field truncation**: Full multi-line descriptions are preserved.

## Incompatibilities

| Issue | Severity | Workaround |
|-------|----------|------------|
| Script execution unsupported | Medium | Skills relying on `scripts/` for runtime functionality cannot execute in ADK. Move critical logic to the agent's toolset or MCP. |
| `tests/` directory ignored | Low | Test files are development-only; no impact on runtime. |
| Non-`.md` reference files | Low | ADK may not load non-markdown reference files. Use `.md` format for all references. |
| `LICENSE.txt` at skill root | None | Silently ignored by ADK loader. |

## Recommendations

### For ADK-portable skills

1. Keep `SKILL.md` as the single source of truth for instructions
2. Use `references/*.md` for domain context that should be loadable by ADK agents
3. Avoid relying on `scripts/` for runtime execution — treat scripts as reference-only documentation
4. Add `compatibility: "adk-v1.27+"` to frontmatter for skills verified as ADK-compatible
5. Use `allowed_tools` frontmatter field to document MCP tools the skill requires (Notion, Slack, Figma, etc.)

### Frontmatter Template (ADK-Compatible)

```yaml
---
name: skill-name
description: >-
  One-paragraph description with WHAT, WHEN, and negative triggers.
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
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
