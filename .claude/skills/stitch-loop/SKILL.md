---
name: stitch-loop
description: >-
  Autonomous frontend builder using an iterative baton system with
  .stitch/next-prompt.md. Enables continuous website development via Stitch
  MCP with design system consistency.
---

# Stitch Build Loop

Autonomous frontend builder using an iterative "baton" system. Each iteration reads a task from `.stitch/next-prompt.md`, generates a page via Stitch MCP, integrates it into the site, and prepares the next task.

Ported from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `stitch-loop`, adapted for Cursor IDE.

## Cursor & Thaki workspace

- **Read** — Every iteration: read `.stitch/next-prompt.md`, `.stitch/SITE.md`, `.stitch/DESIGN.md`, and the target `site/public/` (or the chosen app’s `public/`) to avoid duplicating pages.
- **Write** — Update baton, sitemap, `metadata.json`, and staged/production HTML; keep paths under the active package (e.g. `ai-platform-strategy/site/` or a Vite app under `thaki-ui/packages/`).
- **Shell** — Optional local server or build checks after integrating pages; git status/commit flows follow project `git-rules`.
- **Grep** / **SemanticSearch** — Find existing nav, layout shells, and shared partials in Thaki frontends before wiring links.
- **Task** — Optional: run baton + Stitch generation + integration in parallel for independent pages when the roadmap allows.

## Triggers

Use when the user asks to "run Stitch loop", "Stitch 루프 실행", "autonomous site build", "자율 사이트 빌드", "baton build", "배턴 빌드", "iterative Stitch generation", "반복 Stitch 생성", "stitch-loop", "continuous page generation", "연속 페이지 생성", or wants to build multiple pages autonomously using the Stitch MCP baton pattern.

Do NOT use for single page generation (use stitch-design). Do NOT use for design system document generation (use design-md-generator). Do NOT use for converting Stitch output to React (use stitch-react-components). Do NOT use for non-Stitch iterative workflows (use ralph-loop or maestro-conductor).

## Prerequisites

- Stitch MCP server configured and accessible
- `.stitch/DESIGN.md` file (generate with `design-md-generator` or `stitch-design`)
- `.stitch/SITE.md` file documenting site vision and roadmap
- `.stitch/next-prompt.md` baton file with the first task

## The Baton System

`.stitch/next-prompt.md` acts as a relay baton between iterations:

```markdown
---
page: about
---
A page describing the product's features.

**DESIGN SYSTEM (REQUIRED):**
[Copy from .stitch/DESIGN.md]

**Page Structure:**
1. Header with navigation
2. Feature grid with icons
3. Footer with links
```

## Execution Protocol

### Step 1 — Read the Baton
Parse `.stitch/next-prompt.md`: extract `page` from frontmatter and prompt content from body.

### Step 2 — Consult Context Files
Read `.stitch/SITE.md` for project ID, sitemap, and roadmap. Read `.stitch/DESIGN.md` for visual tokens. Check the sitemap to avoid recreating existing pages.

### Step 3 — Generate with Stitch
1. Get or create project (persist to `.stitch/metadata.json`)
2. Call `generate_screen_from_text` with the full prompt including design system block
3. Download HTML and screenshot to `.stitch/designs/{page}.*`

### Step 4 — Integrate into Site
1. Move HTML to `site/public/{page}.html`
2. Fix asset paths to be relative
3. Wire navigation links
4. Ensure consistent headers/footers

### Step 5 — Update Site Documentation
Update `.stitch/SITE.md` sitemap with the new page.

### Step 6 — Prepare Next Baton
Update `.stitch/next-prompt.md` with the next page task from the roadmap. Include the design system block.

## File Structure

```
project/
├── .stitch/
│   ├── metadata.json    # Stitch project & screen IDs
│   ├── DESIGN.md        # Visual design system
│   ├── SITE.md          # Site vision, sitemap, roadmap
│   ├── next-prompt.md   # Current task baton
│   └── designs/         # Staging area
└── site/public/         # Production pages
```

## Common Pitfalls

- Forgetting to update `.stitch/next-prompt.md` breaks the loop
- Recreating a page that already exists in the sitemap
- Not including the design system block from `.stitch/DESIGN.md`
- Leaving placeholder `href="#"` links
