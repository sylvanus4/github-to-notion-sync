---
name: demo-forge
description: >-
  Auto-generate interactive product demos from recent code changes. Reads git
  diff, classifies user-facing features, captures browser screenshots of
  before/after states, and produces a shareable HTML demo page with animations
  and annotations — or a video script with timestamps and talking points. Use
  when the user asks to "create demo", "demo forge", "generate demo", "product
  demo", "showcase changes", "데모 생성", "변경사항 데모", "stakeholder demo", "show what
  changed", or wants to present code changes to non-technical stakeholders. Do
  NOT use for static architecture diagrams (use visual-explainer), text-only
  release notes (use pr-review-captain), or video transcription (use
  transcribee).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Demo Forge — Auto-Generate Product Demos from Code Changes

Bridge the gap between "developer changelog" and "stakeholder demo". Turns git diffs into visual, interactive demo pages that non-technical stakeholders can understand.

## Usage

```
/demo-forge                                # demo from uncommitted changes
/demo-forge HEAD~3..HEAD                   # demo from last 3 commits
/demo-forge --branch feature/auth          # demo from branch diff vs main
/demo-forge --mode html                    # interactive HTML page (default)
/demo-forge --mode script                  # video recording script
/demo-forge --mode slides                  # presentation-ready slides HTML
/demo-forge --url http://localhost:3000    # base URL for screenshots
```

## Workflow

### Step 1: Collect Changes

Gather the diff based on user input:

```bash
# Uncommitted changes
git diff HEAD --name-only --stat

# Commit range
git log --oneline $RANGE
git diff $RANGE --name-only --stat

# Branch comparison
git diff main...$BRANCH --name-only --stat
git log main...$BRANCH --oneline
```

Parse commit messages for context (feature descriptions, issue references).

### Step 2: Classify Changes

Categorize each changed file into impact types:

| Category | Detection | Stakeholder Interest |
|----------|-----------|---------------------|
| **UI Change** | `.tsx`, `.css`, `.scss`, component files | HIGH — visible to users |
| **API Change** | route handlers, OpenAPI specs, endpoints | MEDIUM — affects integrations |
| **Performance** | query optimization, caching, indexing | MEDIUM — measurable improvement |
| **Bug Fix** | commit message contains "fix", test additions | LOW-MEDIUM — reliability |
| **Infrastructure** | Docker, CI, config files | LOW — internal only |
| **Refactor** | no new features, structural changes only | LOW — internal only |

Filter to stakeholder-relevant changes (HIGH and MEDIUM). If no user-facing changes found, inform the user and offer to create a technical changelog instead.

### Step 3: Extract Feature Narratives

For each user-facing change, create a narrative:

1. **Read the diff** for the changed component/endpoint
2. **Read commit messages** for intent and context
3. **Identify the user story**: what can users do now that they couldn't before?
4. **Write a 1-2 sentence description** in non-technical language

```
Feature Narratives:
  1. "Users can now filter search results by date range"
     Files: SearchFilters.tsx, SearchPage.tsx, searchApi.ts
     Type: UI Change + API Change

  2. "Login page now shows helpful error messages instead of generic errors"
     Files: LoginForm.tsx, authErrors.ts
     Type: Bug Fix (UX improvement)
```

### Step 4: Capture Visual Evidence

If `--url` is provided or a local dev server is running:

1. **Detect browser availability**: Try cursor-ide-browser MCP first (check `browser_tabs` action `list`). Fall back to agent-browser CLI if available. If neither works, skip to code-diff mode.
2. Navigate to affected pages and take screenshots of the relevant UI states
3. For before/after comparison (only when safe):
   - Check for uncommitted changes: `git status --porcelain`
   - If worktree is clean: `git stash` is safe — screenshot "before", then `git stash pop`
   - If worktree is dirty: **do NOT stash** — use `git worktree add /tmp/demo-before HEAD~1` instead, screenshot from the worktree, then `git worktree remove /tmp/demo-before`
   - If neither is feasible, skip before screenshots and use code diffs only
4. Annotate screenshots with highlights on changed areas

If no browser is available, skip screenshots and use code-based before/after diffs as visual evidence instead.

### Step 5: Build Demo Output

#### 5a. HTML Demo Page (`--mode html`, default)

Generate a self-contained HTML file using the visual-explainer pattern:

```
Structure:
  - Hero section with demo title and date
  - Feature cards (one per user-facing change):
    - Feature title and description
    - Before/after screenshot comparison (if available)
    - Key code snippets (simplified, syntax-highlighted)
    - Impact metrics (files changed, lines added/removed)
  - Summary section with overall stats
  - Technical appendix (collapsible, for developers)
```

Design guidelines:
- Bold, modern aesthetic with dark/light mode support
- Animated transitions between before/after states
- Mobile-responsive layout
- Import distinctive fonts from Google Fonts
- Use CSS animations for entrance reveals

Create the output directory if needed: `mkdir -p docs/demos`

Save to: `docs/demos/demo-{date}-{branch}.html`

#### 5b. Video Script (`--mode script`)

Generate a structured recording script:

```
Video Script: [Feature Name] Demo
Duration: ~[N] minutes
Date: [date]

[0:00 - 0:15] Introduction
  SHOW: Landing page
  SAY: "Today I'll walk you through the latest changes to [product]..."

[0:15 - 1:00] Feature 1: [name]
  SHOW: Navigate to [page]
  SAY: "[description of what changed]"
  DO: [interaction steps]
  HIGHLIGHT: [what to point out]

[1:00 - 1:30] Feature 2: [name]
  ...

[X:XX] Wrap-up
  SAY: "These changes are available in [version/branch]..."
```

Save to: `docs/demos/script-{date}-{branch}.md`

#### 5c. Slide Deck (`--mode slides`)

Generate an HTML slide deck (one feature per slide):

```
Slide 1: Title + date + branch
Slide 2-N: One feature per slide with screenshot + description
Slide N+1: Summary metrics
Slide N+2: Technical details (optional)
```

Save to: `docs/demos/slides-{date}-{branch}.html`

### Step 6: Report

```
Demo Forge Report
==================
Mode: [html|script|slides]
Changes analyzed: [N] commits, [N] files
User-facing features: [N]
Screenshots captured: [N]

Output: docs/demos/[filename]

Features Showcased:
  1. [feature name] — [1-line description]
  2. [feature name] — [1-line description]

Skipped (internal only):
  - [N] infrastructure changes
  - [N] refactors
```

## Examples

### Example 1: Sprint demo

User: `/demo-forge --branch feature/search-v2 --url http://localhost:3000`

Output: HTML demo page with 3 feature cards (date range filter, sort options, result count), each with before/after screenshots and animated transitions.

### Example 2: Video script for stakeholder meeting

User: `/demo-forge HEAD~5..HEAD --mode script`

Output: 3-minute video script with timestamps, screen navigation instructions, and talking points for each user-facing change.

### Example 3: Quick demo from uncommitted work

User: "Show me what changed visually"

Output: HTML page highlighting UI changes in the current working tree, with code diffs and feature descriptions.

## Error Handling

| Scenario | Action |
|----------|--------|
| No user-facing changes in diff | Offer technical changelog mode instead |
| Dev server not running | Skip screenshots; use code diffs as visual evidence |
| Browser automation unavailable | Fall back to code-based before/after comparison |
| Too many changes (50+ files) | Group by feature/module; show top 5 with summary |
| No commit messages (WIP commits) | Infer feature descriptions from code changes |
| Screenshots fail on specific pages | Skip that page; note in report as manual verification needed |

## Troubleshooting

- **"No user-facing changes"**: The classifier may miss changes in non-standard file extensions. Check if your UI files use `.jsx`, `.vue`, or `.svelte` instead of `.tsx`.
- **Screenshots blank or broken**: Ensure the dev server is fully loaded before capture. Add a 2-3 second wait after navigation.
- **git worktree fails**: Some git versions don't support `worktree add` with dirty index. Run `git stash` first or use `--no-checkout`.
- **HTML demo too large**: If screenshots are embedded as base64, file size grows fast. Consider linking to external image files instead.
