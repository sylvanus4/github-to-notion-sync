# Learned Context

## Workspace

- ThakiCloud is an AI GPU Cloud company; always analyze news/trends from AI infrastructure perspective
- 5 managed projects: github-to-notion-sync, ai-template, ai-model-event-stock-analytics, research, ai-platform-webui
- Primary memory file is `MEMORY.md` at project root (not `AGENTS.md`); `AGENTS.md` is only for continual-learning skill output
- All skill files (`.cursor/skills/**/SKILL.md` and references) must be written in English; Korean only in user prompts or user-facing output templates
- User gives commands in Korean but requests all plans in English ("영어로 계획해줘")
- Cursor rules live in `.cursor/rules/`; skills in `.cursor/skills/`; commands in `.cursor/commands/`

## Slack

- Always post to `#효정-할일` channel (ID: `C0AA8NT4T8T`), never DM
- Slack mrkdwn: `*bold*` single asterisk only, `_italic_`, `<url|text>` for links
- Never use `**double bold**` or `## headers` in Slack messages — use `*bold text*` on its own line instead
- Use threaded replies for detailed content (colleague emails, news digest, insights as separate thread messages)
- Capture `message_ts` from main message response to post thread replies via `thread_ts`
- Slack MCP tool: `plugin-slack-slack` server, `slack_send_message` tool
- Message limit is 5000 chars per text element; split longer content into multiple thread replies

## Google Daily Pipeline

- 5-phase pipeline: Calendar → Gmail Triage → Drive Upload → Slack Notify → Memory Sync
- gws CLI: always use `format: full` to get email headers (not `metadata` — it drops From/Subject)
- gws CLI JSON output starts with "Using keyring backend: keyring" line — skip it when parsing JSON
- Gmail "Low Priority" label ID is `Label_9`
- Colleague domains: `@thakicloud.co.kr` (team-casual tone), `@bespinglobal.com` (formal business tone)
- Bespin News sender: `bespin_news@bespinglobal.com` → extract article links, summarize each, generate AI/GPU Cloud insights
- Never auto-send email replies; post draft replies to Slack threads only
- Use `cursor-ide-browser` MCP or `WebFetch` for article content fetching (not playwright-runner)
- docx generation via Node.js `docx` package: run with `NODE_PATH=$(npm root -g) node script.js`

## GitHub Actions

- Sprint stats and sprint summary sync: Friday 14:00 KST only (cost optimization)
- All scheduled workflows: weekday-only (Mon–Fri), no weekend runs
- code-quality.yml and qa-issues-sync.yml: backed up and disabled

## GitHub org project & daily ship

- Cross-repo tracking board: ThakiCloud org GitHub Project #5 — `https://github.com/orgs/ThakiCloud/projects/5`
- `/sod-ship` and `/eod-ship` handle git sync, cursor-sync, release-ship, and Slack; they do not create issues by themselves. Items appear on Project #5 when the ship path runs `commit-to-issue` (use pipeline mode in automation so confirmation gates do not skip issue creation).
- On weekends, when running sod/eod ship workflows, also move Done column items to Archive on that org project as board hygiene (user preference).

## Key People

- 전승훈 (Seung-Hun Jeon): Global CTO / Co-Founder, ThakiCloud
- 이한주 (HanJoo Lee): Bespin Global executive, frequent cross-org discussions
- 윤성노 (Sungno Yun): Bespin Global, financial model / business planning
