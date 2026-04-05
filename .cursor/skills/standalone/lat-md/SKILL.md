---
name: lat-md
version: 1.0.0
description: "Manage the lat.md code architecture knowledge graph — run lat check for drift detection, lat search for semantic architecture queries, lat refs for cross-referencing, and maintain @lat annotations in source code."
---

# lat.md Knowledge Graph Manager

Maintain and query the `lat.md/` markdown-based knowledge graph that documents code architecture with bidirectional source code links.

## Trigger Phrases

- "lat check", "check documentation drift", "문서-코드 드리프트"
- "lat search", "search architecture", "아키텍처 검색"
- "lat refs", "find code references", "코드 참조 찾기"
- "update lat.md", "add architecture page", "아키텍처 페이지 추가"
- "annotate code with lat", "add @lat annotation", "@lat 주석 추가"
- "lat section", "lat expand", "lat mcp"

## Do NOT Use For

- Operational knowledge updates (use `memory/topics/*.md` and `MEMORY.md`)
- Session summaries or decisions (use `recall` or `context-engineer`)
- General code review without architecture focus (use `deep-review` or `simplify`)
- CODEMAP.md generation (use `codemap-updater` — lat.md is a richer alternative)
- Notion or Slack documentation (use `md-to-notion` or `kwp-slack-slack-messaging`)

## Scope Boundary

| Concern | Owner | Examples |
|---------|-------|----------|
| Code architecture | `lat.md/` | Module structure, API design, data flow, service dependencies |
| Operational knowledge | `memory/` | Session summaries, preferences, decisions, runbooks |

## Prerequisites

- `lat.md` CLI installed globally: `npm i -g lat.md`
- Git repository initialized (required for `lat hook` and `lat check`)
- For `lat search`: set `LAT_LLM_KEY` environment variable with an LLM API key

## Workflow

### 1. Pre-Task: Architecture Discovery

Before modifying code that touches documented domains:

```bash
lat search "<task description>"
lat refs "<section-id>"
```

Read linked `lat.md/` pages to understand the architectural context.

### 2. Creating a New Architecture Page

When a new module, service, or domain is added:

1. Create `lat.md/<page-name>.md` with a leading paragraph (≤250 chars) and `[[src/]]` links
2. Add `[[page-name]]` to `lat.md/lat.md` entry file
3. Add `# @lat: [[page-name#Section]]` annotations to key source files
4. Run `lat check` to validate all links resolve

### Syntax Reference

```markdown
# In lat.md/ documentation files:
[[page-name]]                           # Wiki link to another page
[[src/path/to/file.py#ClassName]]       # Source code reference

# In source code files:
# @lat: [[page-name#Section Name]]     # Python annotation
// @lat: [[page-name#Section Name]]    # Go/JS/TS annotation
```

### 3. Post-Task: Drift Validation

After any code change that touches annotated files:

```bash
lat check
```

Fix any reported broken links or missing references before committing.

### 4. Querying Architecture

```bash
lat section "<section-id>"    # Read a specific section
lat expand "<section-id>"     # Section with inline code snippets
lat refs "<section-id>"       # List code files referencing a section
lat search "<query>"          # Semantic search (requires LLM key)
```

### 5. MCP Integration

The `lat mcp` server exposes 6 tools for editor integration:

- `lat_locate` — Find sections matching a query
- `lat_section` — Read section content
- `lat_search` — Semantic search
- `lat_expand` — Section with inline code
- `lat_check` — Run drift detection
- `lat_refs` — Find code references

Start the MCP server: `lat mcp` (registers in `.cursor/mcp.json`)

## Gotchas

- `lat check` requires leading paragraphs ≤250 chars for each section
- `[[src/]]` links must reference exact symbol names (class, function, variable) as they appear in code
- `lat refs` requires the annotation format `# @lat: [[page#Section]]` with double brackets — single brackets fail silently
- `lat search` fails gracefully without `LAT_LLM_KEY` — use `lat section` or `lat refs` as fallback
- `lat init` uses interactive TTY prompts — cannot be fully scripted via stdin; use `lat gen` + manual setup
- `lat hook` commands require at least one git commit in the repository
- `lat.md/` directory is project-specific and must NOT be synced via `cursor-sync`

## Verification

After any lat.md changes:

```bash
lat check
```

Expected output: `✓ All checks passed` with no errors or warnings (init version warning is acceptable).
