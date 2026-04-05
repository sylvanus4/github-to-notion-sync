# Workspace Facts

## Project Identity

- ThakiCloud is an AI GPU Cloud company; always analyze news/trends from AI infrastructure perspective
- 5 managed projects: github-to-notion-sync, ai-template, ai-model-event-stock-analytics, research, ai-platform-webui
- Primary memory file is `MEMORY.md` at project root; `AGENTS.md` is a redirect stub
- Cursor rules in `.cursor/rules/`; skills in `.cursor/skills/`; commands in `.cursor/commands/`

## GitHub Actions

- Sprint stats and sprint summary sync: Friday 14:00 KST only (cost optimization)
- All scheduled workflows: weekday-only (Mon–Fri), no weekend runs
- code-quality.yml and qa-issues-sync.yml: backed up and disabled

## GitHub Org Project & Daily Ship

- Cross-repo tracking board: ThakiCloud org GitHub Project #5 — `https://github.com/orgs/ThakiCloud/projects/5`
- `/sod-ship` and `/eod-ship` handle git sync, cursor-sync, release-ship, and Slack; they do not create issues by themselves
- Items appear on Project #5 when the ship path runs `commit-to-issue` (use pipeline mode)
- On weekends, move Done column items to Archive as board hygiene

## Sprint Configuration

- GitHub Synos project number: 5 (configured in `config/teams/synos/sprint_config.yml`)
- Sprint field name in GitHub Projects can be `"스프린트"`, `"Sprint"`, or `"Iteration"` — handle all three
- 이상민 GitHub username: `thakicloud-leesangmin` (not `sangmin.lee`)

## Git Workflows

- ai-platform-webui: commit → push to `tmp` → issue → report (no PR/merge, tmp-branch only)
- Other repos: commit → push → issue → PR → merge

## Credentials & Auth

- GWS OAuth credentials: `~/.config/gws/client_secret.json` (global)
- GWS plaintext credentials: `~/.config/gws/credentials.json` with `type: authorized_user` (macOS Keychain workaround)
- If `gh` project linking fails: run `gh auth refresh -s read:org,read:discussion`
- Virtual environment path: project root `.venv/`
- Notion API uses `NOTION_TOKEN` from `.env`
- Notion meeting database ID: `22c9eddc34e680d5beb9d2cf6c8403b4`

## Key People

- 전승훈 (Seung-Hun Jeon): Global CTO / Co-Founder, ThakiCloud
- 이한주 (HanJoo Lee): Bespin Global executive
- 윤성노 (Sungno Yun): Bespin Global, financial model / business planning
