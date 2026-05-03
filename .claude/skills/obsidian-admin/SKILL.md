---
name: obsidian-admin
description: >-
  Administer Obsidian via the CLI — manage plugins (install, enable, disable,
  reload), themes, sync, publish, vault history, and app lifecycle (reload,
  restart). Use when the user asks to install a plugin, enable/disable
  plugins, manage themes, sync vault, publish notes, view file history, reload
  Obsidian, or restart the app. Do NOT use for file CRUD (use obsidian-files),
  daily notes (use obsidian-daily), search (use obsidian-search), note
  metadata (use obsidian-notes), or developer tools (use obsidian-dev). Korean
  triggers: "옵시디언 플러그인", "플러그인 설치", "플러그인 관리", "옵시디언 테마", "옵시디언 싱크", "옵시디언
  퍼블리시", "히스토리", "옵시디언 재시작", "옵시디언 리로드".
disable-model-invocation: true
---

# Obsidian CLI — Administration

> **Requires:** Obsidian app running, CLI in PATH. See `obsidian-setup`.

## Prerequisites

- Obsidian CLI configured (`obsidian-setup`)
- Target vault open in Obsidian
- Obsidian Sync / Publish require active subscriptions

## Quick Commands

### Plugins

```bash
# Discovery
obsidian plugins                                    # list installed plugins
obsidian plugins:community                          # browse community plugins
obsidian plugin:info id="dataview"                  # plugin details

# Lifecycle
obsidian plugin:install id="dataview"               # install community plugin
obsidian plugin:enable id="dataview"                # enable plugin
obsidian plugin:disable id="dataview"               # disable plugin
obsidian plugin:uninstall id="dataview"             # uninstall plugin
obsidian plugin:update id="dataview"                # update to latest version
obsidian plugin:update-all                          # update all plugins
obsidian plugin:reload id="my-plugin"               # reload without restart
```

### Themes

```bash
obsidian themes                                     # list installed themes
obsidian themes:community                           # browse community themes
obsidian theme:install name="Minimal"               # install theme
obsidian theme:use name="Minimal"                   # switch active theme
obsidian theme:uninstall name="Old Theme"           # uninstall theme
```

### Sync (requires Obsidian Sync subscription)

```bash
obsidian sync:status                                # sync status
obsidian sync:start                                 # start syncing
obsidian sync:stop                                  # stop syncing
obsidian sync:pause                                 # pause sync
obsidian sync:resume                                # resume sync
```

### Publish (requires Obsidian Publish subscription)

```bash
obsidian publish:status                             # publish site status
obsidian publish:add file="Public Note"             # mark for publish
obsidian publish:remove file="Private Note"         # unmark from publish
obsidian publish:push                               # push changes to site
```

### History & Recovery

```bash
obsidian history file="Important Doc"               # version history
obsidian history:restore file="Doc" version=3       # restore a version
```

### App Lifecycle

```bash
obsidian reload                                     # reload vault (soft)
obsidian restart                                    # full app restart
```

## Discovering Commands

```bash
obsidian help plugins         # plugin management
obsidian help themes          # theme management
obsidian help sync            # sync commands
obsidian help publish         # publish commands
obsidian help history         # version history
```

## Common Patterns

### Plugin setup for a new vault

```bash
obsidian plugin:install id="dataview"
obsidian plugin:install id="templater-obsidian"
obsidian plugin:install id="obsidian-git"
obsidian plugin:enable id="dataview"
obsidian plugin:enable id="templater-obsidian"
obsidian plugin:enable id="obsidian-git"
```

### Keep plugins updated

```bash
obsidian plugin:update-all
obsidian reload
```

### Publish workflow

```bash
obsidian publish:add file="Guide"
obsidian publish:push
obsidian publish:status
```

### Recovery from bad edit

```bash
obsidian history file="Corrupted Doc"         # find good version
obsidian history:restore file="Corrupted Doc" version=2
```

## Safety

- `plugin:uninstall` and `theme:uninstall` are destructive — confirm before running
- `restart` closes and reopens the app — save work first
- `sync:stop` will halt active synchronization — data may diverge
- `history:restore` overwrites current content with the selected version

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Plugin not found` | Wrong plugin ID | Check exact ID in community plugins list |
| `Sync not configured` | No Sync subscription | Subscribe at obsidian.md/sync |
| `Publish not configured` | No Publish subscription | Subscribe at obsidian.md/publish |
| `Version not found` | Invalid version number | Run `obsidian history` to list versions |
