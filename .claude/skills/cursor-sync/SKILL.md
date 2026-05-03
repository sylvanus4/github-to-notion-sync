---
name: cursor-sync
description: N-repo bidirectional sync of .cursor/ assets (commands, skills, rules) across all 5 ThakiCloud repositories via research hub.
disable-model-invocation: true
---

Sync .cursor/ assets across all managed repositories.

## Repository Registry

1. ai-platform-strategy (this repo)
2. ai-model-event-stock-analytics
3. research (merge hub)
4. ai-template
5. github-to-notion-sync

## Sync Process

### Phase 1: Pull (absorb changes from all targets)
```bash
# For each target repo:
rsync -av --update <target>/.cursor/{commands,skills,rules}/ <research>/.cursor/
```

### Phase 2: Push (distribute merged result)
```bash
# From research hub to all targets:
rsync -av --update <research>/.cursor/{commands,skills,rules}/ <target>/.cursor/
```

## Scope

Only syncs:
- `.cursor/commands/`
- `.cursor/skills/`
- `.cursor/rules/`

Does NOT sync project-specific code, configs, or data.

## Rules

- Research repo acts as the canonical merge hub
- Use newest-wins (-u flag) for conflict resolution
- Confirm direction before bulk sync operations
- Never sync .env, credentials, or project-specific configs
