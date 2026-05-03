---
name: sod-ship
description: Start-of-day git sync — commit, push, pull all 5 projects, update submodules, then cursor-sync.
disable-model-invocation: true
---

Synchronize all managed repositories at the start of the day.

## Pipeline (Sequential)

1. **Commit dirty trees**: For each repo with uncommitted changes, create domain-split commits
2. **Push unpushed**: Push any local commits not yet on remote
3. **Pull remote**: Pull latest changes from remote for all repos
4. **Submodule update**: Update git submodules (ai-suite, thaki-ui, ai-platform-webui)
5. **Cursor Sync**: Run cursor-sync to propagate .cursor/ assets across all repos
5½. **Claude Sync**: Run claude-sync to propagate .claude/ assets (rules, commands, skills, hooks) across all repos

## Managed Repositories

| Repo | Branch | Path |
|------|--------|------|
| ai-platform-strategy | dev | ~/thaki/ai-platform-strategy |
| ai-model-event-stock-analytics | dev | ~/thaki/ai-model-event-stock-analytics |
| research | dev | ~/thaki/ai-platform-strategy |
| ai-template | dev | ~/thaki/ai-template |
| github-to-notion-sync | dev | ~/thaki/github-to-notion-sync |

## Rules

- All repos use standard `dev` branch push/pull
- Skip repos that fail gracefully — report errors but continue
