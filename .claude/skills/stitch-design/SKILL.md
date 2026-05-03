---
name: stitch-design
description: >-
  Unified entry point for Google Stitch design work. Handles prompt
  enhancement, design system synthesis (.stitch/DESIGN.md), and high-fidelity
  screen generation/editing via Stitch MCP server.
---

# Stitch Design Expert

Unified entry point for Google Stitch design work. Handles prompt enhancement (UI/UX keywords, atmosphere), design system synthesis (`.stitch/DESIGN.md`), and high-fidelity screen generation/editing via Stitch MCP.

Ported from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `stitch-design`, adapted for Cursor IDE.

## Cursor & Thaki workspace

- **Read** — Load `.stitch/DESIGN.md`, `.stitch/metadata.json`, and prior `.stitch/designs/` outputs. Explore `thaki-ui/`, `ai-platform-webui/`, or the active app package when aligning copy or layout with product code.
- **Write** — Persist generated HTML, screenshots, and updated `.stitch/` docs under the repo root (e.g. `ai-platform-strategy/.stitch/` or the package you are working in).
- **Shell** — Run stitch CLI or asset download steps when the Stitch workflow requires local commands; use **Grep** / **SemanticSearch** to find design tokens, routes, and existing page patterns in Thaki monorepos.
- **Task** — Optional: parallel sub-steps (e.g. one agent refining prompts, another verifying sitemap) for large multi-page Stitch sessions.

## Triggers

Use when the user asks to "design with Stitch", "Stitch 디자인", "generate Stitch screen", "Stitch 화면 생성", "edit Stitch design", "Stitch 디자인 수정", "Stitch MCP", "create UI with Stitch", "Stitch로 UI 만들기", "stitch-design", "Stitch 프로젝트", "Stitch 프롬프트", or wants to use the Google Stitch MCP server for UI generation or editing.

Do NOT use for design-system-aligned prompt enhancement without Stitch (use refined-swiss-prompt-enhancer). Do NOT use for DESIGN.md generation from codebase analysis (use design-md-generator). Do NOT use for Figma-to-code workflows (use figma-dev-pipeline). Do NOT use for building components without Stitch (use fsd-development or implement-screen). Do NOT use for design QA (use design-qa-checklist or anti-slop-ui-guard).

## Prerequisites

- Stitch MCP server must be configured and accessible
- Run `/setup-doctor --group stitch-mcp` to verify (if that group is not yet defined, run full `setup-doctor` and ensure Stitch MCP is connected)

## Core Responsibilities

1. **Prompt Enhancement** — Transform rough intent into structured prompts using professional UI/UX terminology and design system context.
2. **Design System Synthesis** — Analyze existing Stitch projects to create `.stitch/DESIGN.md` source-of-truth documents.
3. **Workflow Routing** — Route user requests to the appropriate generation or editing workflow.
4. **Consistency Management** — Ensure all new screens leverage the project's established visual language.
5. **Asset Management** — Download generated HTML and screenshots to `.stitch/designs/`.

## Workflows

| User Intent | Workflow | Primary MCP Tool |
|:---|:---|:---|
| "Design a [page]..." | text-to-design | `generate_screen_from_text` |
| "Edit this [screen]..." | edit-design | `edit_screens` |
| "Create/Update DESIGN.md" | generate-design-md | `get_screen` + analysis |

## Prompt Enhancement Pipeline

### Step 1 — Analyze Context

- Maintain the current `projectId`. Use `list_projects` if unknown.
- Check for `.stitch/DESIGN.md`. If it exists, incorporate its tokens. If not, suggest generation.

### Step 2 — Refine UI/UX Terminology

Replace vague terms with professional descriptions:
- "Make a nice header" → "Sticky navigation bar with glassmorphism effect and centered logo"
- "Add some buttons" → "Primary CTA with 16px padding, 8px border-radius, brand color fill"

### Step 3 — Structure the Final Prompt

```markdown
[Overall vibe, mood, and purpose of the page]

**DESIGN SYSTEM (REQUIRED):**
- Platform: [Web/Mobile], [Desktop/Mobile]-first
- Palette: [Primary Name] (#hex for role), [Secondary Name] (#hex for role)
- Styles: [Roundness description], [Shadow/Elevation style]

**PAGE STRUCTURE:**
1. **Header:** [Description of navigation and branding]
2. **Hero Section:** [Headline, subtext, and primary CTA]
3. **Primary Content Area:** [Detailed component breakdown]
4. **Footer:** [Links and copyright information]
```

### Step 4 — Present AI Insights

After any Stitch MCP tool call, surface `outputComponents` (Text Description and Suggestions) to the user.

## Asset Management

After generation, download assets:
1. HTML: Save to `.stitch/designs/{page}.html`
2. Screenshot: Append `=w{width}` to the URL for full resolution. Save to `.stitch/designs/{page}.png`

## Integration

- Chain with `design-md-generator` to create `.stitch/DESIGN.md` from project analysis
- Chain with `refined-swiss-prompt-enhancer` for Refined Swiss-aligned prompts before Stitch generation
- Chain with `stitch-loop` for autonomous iterative site building
- Chain with `stitch-react-components` to convert Stitch output to React code
