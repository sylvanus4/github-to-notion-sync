# Pipeline Operations

## Google Daily Pipeline

5-phase pipeline: Calendar → Gmail Triage → Drive Upload → Slack Notify → Memory Sync

### Configuration

- gws CLI: always use `format: full` to get email headers (not `metadata` — it drops From/Subject)
- gws CLI JSON output starts with "Using keyring backend: keyring" line — skip it when parsing JSON
- Gmail "Low Priority" label ID is `Label_9`
- Colleague domains: `@thakicloud.co.kr` (team-casual tone), `@bespinglobal.com` (formal business tone)
- Bespin News sender: `bespin_news@bespinglobal.com` → extract article links, summarize each, generate AI/GPU Cloud insights
- Never auto-send email replies; post draft replies to Slack threads only
- Use `cursor-ide-browser` MCP or `WebFetch` for article content fetching (not playwright-runner)

## continual-learning Issue

- `continual-learning` skill (cursor-public plugin) creates `AGENTS.md` by default (Claude Code convention)
- This project uses Cursor IDE with `MEMORY.md` as the memory system
- continual-learning output target should be redirected to `MEMORY.md`
