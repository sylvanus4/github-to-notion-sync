---
name: cabinet
description: >-
  Set up, customize, and operate Cabinet — an AI-first knowledge base and startup
  OS built on Next.js 16 with markdown-on-disk architecture, AI agent workspaces,
  scheduled jobs, and wiki-style linking. Use when creating Cabinet instances,
  building agent templates, configuring job schedules, extending the editor,
  integrating with Cabinet's filesystem-based KB structure, or developing Cabinet
  plugins/apps. Do NOT use for general Next.js development without Cabinet context
  (use nextjs-best-practices). Do NOT use for generic markdown KB operations
  (use kb-orchestrator). Do NOT use for Obsidian vault management (use obsidian-*
  skills).
triggers:
  - cabinet
  - Cabinet KB
  - cabinet setup
  - cabinet agent
  - cabinet job
  - runcabinet
  - AI knowledge base on disk
  - markdown startup OS
  - 캐비넷
  - 캐비넷 설정
  - 캐비넷 에이전트
  - 지식베이스 셀프호스트
---

# Cabinet — AI-First Knowledge Base & Startup OS

An open-source, self-hosted knowledge base where everything is markdown files on disk — no database, no vendor lock-in. Built by Hila Shmuel (ex-Apple Engineering Manager).

**Repository:** [hilash/cabinet](https://github.com/hilash/cabinet) (1,487+ stars)
**Website:** [runcabinet.com](https://runcabinet.com)
**License:** Open Source
**Version:** 0.3.4 (April 2026)

## When to Use This Skill

- Setting up a new Cabinet instance or migrating data
- Creating or customizing AI agent templates (`.agents/`)
- Configuring scheduled jobs (`.jobs/` YAML)
- Building embedded apps or linked repositories inside Cabinet
- Extending the Tiptap editor or adding new content viewers
- Integrating external tools with Cabinet's API routes
- Understanding Cabinet's filesystem-based KB conventions
- Troubleshooting Cabinet daemon, terminal, or agent issues

## When NOT to Use

- General Next.js 16 App Router patterns → `nextjs-best-practices`
- Generic markdown-to-wiki KB pipelines → `kb-orchestrator`
- Obsidian vault operations → `obsidian-*` skills
- Notion-based knowledge management → `notion-*` skills
- General Tiptap/ProseMirror editor development without Cabinet context

## Core Philosophy

1. **No database** — all content is filesystem markdown in `/data/`
2. **AI-native** — agents, jobs, and conversations are first-class
3. **Self-hosted** — data never leaves the user's machine
4. **Markdown-first** — YAML frontmatter, wiki-links, directory-as-page

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16.2 (App Router) |
| Language | TypeScript 5 (strict, target ES2017) |
| UI | React 19, Tailwind CSS, shadcn/ui, @base-ui/react |
| Editor | Tiptap (ProseMirror) + toolbar, CSV/PDF/website viewers |
| State | Zustand 5 (tree, editor, ai-panel, task, app stores) |
| Terminal | xterm.js (web terminal via PTY WebSocket) |
| Daemon | `cabinet-daemon.ts` — WebSocket + job scheduler + agent executor |
| Jobs | node-cron (scheduled YAML jobs in `/data/.jobs/`) |
| Git | simple-git (auto-commit, history, diff) |
| Markdown | unified/remark (MD↔HTML), gray-matter (frontmatter), turndown (HTML→MD) |
| Desktop | Electron (optional, via @electron-forge) |
| DB (metadata only) | better-sqlite3 (internal indexing, NOT content storage) |

## Architecture

```
cabinet/
  src/
    app/api/
      tree/              → GET tree structure from /data
      pages/[...path]/   → GET/PUT/POST/DELETE/PATCH pages
      upload/[...path]/  → POST file upload to page directory
      assets/[...path]/  → GET/PUT static file serving + raw writes
      search/            → GET full-text search
      agents/
        conversations/   → Manual task/conversation CRUD
        providers/       → Provider, model, adapter metadata
        tasks/           → Task board data
        scheduler/       → Scheduler control/status
      git/               → Git log, diff, commit endpoints
    components/
      sidebar/           → Tree navigation, drag-and-drop, context menu
      editor/            → Tiptap WYSIWYG + toolbar, viewers (PDF, CSV, website)
      ai-panel/          → Right-side AI chat panel
      tasks/             → Task board + detail panel
      agents/            → Agent workspace + live/result views
      jobs/              → Jobs manager UI
      terminal/          → xterm.js web terminal
      composer/          → Shared composer + task runtime picker
      search/            → Cmd+K search dialog
      layout/            → App shell, header
    stores/              → Zustand (tree, editor, ai-panel, task, app)
    lib/
      storage/           → Filesystem ops (path-utils, page-io, tree-builder, task-io)
      markdown/          → MD↔HTML conversion
      git/               → Git service (auto-commit, history, diff)
      agents/            → Adapter runtime, conversation runner, personas, providers
      jobs/              → Job scheduler (node-cron)
  server/
    cabinet-daemon.ts    → Unified daemon: structured runs, PTY, scheduler, events
    terminal-server.ts   → Standalone PTY WebSocket (legacy/debug)
  data/                  → Content directory (KB pages, tasks, jobs, agents)
    .agents/.library/    → 20 pre-built agent templates
    .jobs/               → Scheduled job YAML files
    tasks/board.yaml     → Task board data
    getting-started/     → Default KB page
```

## KB Structure & Conventions

### Directory Layout
- All content lives in `/data/`
- Each page = a **directory** with `index.md` + optional assets (images, files)
- Leaf pages can be a single `.md` file (no directory if no assets)
- Hidden directories (`.git`, `.jobs`, `.history`) = system directories
- Tasks in `/data/tasks/board.yaml`; jobs in `/data/.jobs/`

### Page Format
```yaml
---
title: Page Title
created: 2026-03-21T00:00:00Z
modified: 2026-03-21T00:00:00Z
tags: [tag1, tag2]
order: 1
---
```

### Conventions
- `[[Page Name]]` for internal wiki-links
- Relative paths for assets (images live in the page directory)
- Always include YAML frontmatter for new content
- Markdown tables for structured data

### Supported File Types
Markdown, CSV, PDF, Mermaid diagrams, images, video, audio, code files, embedded websites (directory with `index.html`), full-screen apps (directory with `index.html` + `.app` marker), linked repos (directory with `.repo.yaml`), office/archive files.

### Embedded Apps
- Directory with `index.html` (no `index.md`) → renders as iframe
- Add `.app` marker file → full-screen mode (sidebar collapses)

### Linked Repositories
- External folders linked as symlinks into `/data/`
- `.repo.yaml` file with: `name`, `local`, `remote`, `source`, `branch`, `description`
- `.cabinet-meta` for display metadata

## Quick Start

```bash
npx create-cabinet@latest
cd cabinet
npm run dev:all
```

**Requirements:** Node.js 20+, Claude Code CLI or Codex CLI, macOS/Linux (Windows via WSL)

### Key Scripts
| Command | Purpose |
|---------|---------|
| `npm run dev` | Next.js dev server only |
| `npm run dev:all` | Full stack (Next.js + daemon) |
| `npm run build` | Production build |

## AI Agent System

Cabinet includes 20 pre-built agent templates in `.agents/.library/` covering roles like researcher, writer, analyst, and more. Agents have:
- **Goals** — what they aim to achieve
- **Skills** — capabilities they can use
- **Scheduled jobs** — recurring tasks via node-cron
- **Conversation history** — stored on disk
- **Provider adapters** — Claude, GPT, etc.

## API Routes Reference

| Route | Methods | Purpose |
|-------|---------|---------|
| `/api/tree` | GET | File tree from `/data/` |
| `/api/pages/[...path]` | GET, PUT, POST, DELETE, PATCH | Page CRUD |
| `/api/upload/[...path]` | POST | File upload |
| `/api/assets/[...path]` | GET, PUT | Static file serving |
| `/api/search` | GET | Full-text search |
| `/api/agents/conversations` | GET, POST | Agent conversations |
| `/api/agents/providers` | GET | Provider metadata |
| `/api/agents/tasks` | GET | Task board |
| `/api/agents/scheduler` | GET, POST | Scheduler control |
| `/api/git` | GET | Git log, diff, commit |

## Known Issues

- **#41**: Windows support gap
- **#40**: Typst integration request
- **#39**: Codex with pnpm support
- **#37**: Onboarding stuck state
- **#34**: Dialog sizing on small screens

See `references/issues.md` for the complete list.

## References

- `references/README.md` — Full README with installation, features, screenshots
- `references/issues.md` — GitHub issues (10 recent)
- `references/releases.md` — Release notes (v0.2.0 → v0.3.4)
- `references/file_structure.md` — Complete repository file tree (1,059 items)
