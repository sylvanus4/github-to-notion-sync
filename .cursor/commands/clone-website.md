## Clone Website

Run the AI-powered website cloning pipeline — reverse-engineer and rebuild any website as a pixel-perfect Next.js 16 clone with real assets, exact CSS values, and interactive behaviors.

### Usage

```
/clone-website <target-url>
```

### Workflow

1. **Reconnaissance** — full-page screenshots, design token extraction, mandatory interaction sweep (scroll, click, hover, responsive), page topology mapping
2. **Foundation Build** — fonts, colors, global CSS, TypeScript types, SVG icons, asset download script
3. **Component Specification & Parallel Build** — per-component CSS extraction, spec files, parallel builder subagents in git worktrees
4. **Page Assembly** — wire all sections into `page.tsx`, page-level behaviors and scroll interactions
5. **Visual QA Diff** — side-by-side comparison at desktop and mobile, fix discrepancies

### Execution

Read and follow the `clone-website` skill (`.cursor/skills/clone-website/SKILL.md`) for detailed instructions.

### Prerequisites

- `cursor-ide-browser` MCP enabled in Cursor
- Node.js >= 18, npm
- Playwright browsers installed (`npx playwright install chromium`)
- Git (for worktree parallel builds)

### Examples

Clone a website:
```
/clone-website https://example.com
```

Clone with specific scope discussion:
```
/clone-website https://stripe.com
```
The skill will prompt you to fill in a TARGET.md for scope and fidelity level.
