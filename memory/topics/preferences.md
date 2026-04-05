# User Preferences

## Language & Communication

- Plans, analysis, and architectural discussions in English
- Reports, summaries, and user-facing outputs in Korean
- All skill files (`.cursor/skills/**/SKILL.md`) in English; Korean only in user prompts or user-facing output templates
- Always respond in Korean unless explicitly asked otherwise

## Workflow Preferences

- Do not edit hidden/dotfiles directly; use shell commands to modify them
- Always use `--team synos` when running sprint-related workflows
- Use GitHub project #5 for Synos — project #22 is deprecated
- When implementing a plan, do not edit the plan file itself; mark todos as in_progress and complete all before stopping
- gws CLI requires a Desktop app OAuth client (`{"installed": {...}}`), not a Web app (`{"web": {...}}`)
- Python scripts must run with `.venv/bin/python` or `source .venv/bin/activate`

## Slack Conventions

- Always post to `#효정-할일` channel (ID: `C0AA8NT4T8T`), never DM
- Slack mrkdwn: `*bold*` single asterisk only, `_italic_`, `<url|text>` for links
- Never use `**double bold**` or `## headers` in Slack messages
- Use threaded replies for detailed content
- Capture `message_ts` from main message response to post thread replies via `thread_ts`
- Slack MCP tool: `plugin-slack-slack` server, `slack_send_message` tool
- Message limit is 5000 chars per text element; split longer content into multiple thread replies

## Document Standards

- docx generation via Node.js `docx` package: run with `NODE_PATH=$(npm root -g) node script.js`
