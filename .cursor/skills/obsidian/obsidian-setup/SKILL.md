---
name: obsidian-setup
description: >-
  Install, verify, and configure the Obsidian CLI for terminal-based vault
  control. Use when the user asks to set up Obsidian CLI, verify Obsidian
  installation, troubleshoot CLI access, check Obsidian health, or configure
  PATH for Obsidian. Do NOT use for vault operations (use obsidian-files),
  daily notes (use obsidian-daily), search (use obsidian-search), plugin
  management (use obsidian-admin), or developer commands (use obsidian-dev).
  Korean triggers: "옵시디언 설정", "옵시디언 설치", "Obsidian CLI 설정",
  "옵시디언 PATH", "옵시디언 헬스체크".
metadata:
  version: "1.0.0"
  category: "integration"
---
# Obsidian CLI — Setup & Verification

> **Requires:** Obsidian v1.12+ with Catalyst license. The Obsidian app must be running.

## Prerequisites

1. Obsidian desktop app v1.12 or later installed
2. Catalyst license (early access feature)
3. Obsidian app must be **running** when executing CLI commands
4. CLI registered in system PATH

## Installation

### macOS

The Obsidian installer registers the CLI automatically. Verify PATH includes:

```bash
export PATH="/Applications/Obsidian.app/Contents/MacOS:$PATH"
```

Add to `~/.zprofile` or `~/.zshrc` if not present.

### Linux

Add the Obsidian AppImage or install directory to PATH:

```bash
export PATH="$HOME/Applications:$PATH"  # adjust to your Obsidian location
```

### Windows

The installer adds `obsidian.exe` to PATH automatically. If not, add the installation directory to your system PATH.

## Verification

```bash
obsidian version          # prints Obsidian version (must be >= 1.12)
obsidian help             # list all available commands
obsidian help <command>   # detailed help for a specific command
```

## Health Check

Run the bundled health check script:

```bash
bash .cursor/skills/obsidian/obsidian-setup/scripts/obsidian-health.sh
```

This verifies:
- `obsidian` binary is in PATH
- Obsidian app is running
- Version is 1.12 or later
- At least one vault is accessible

## TUI Mode

Run `obsidian` without arguments to launch the interactive terminal UI:
- **Tab** — autocomplete commands
- **↑ / ↓** — navigate command history
- Type a command and press Enter to execute

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `command not found: obsidian` | Add Obsidian to PATH (see Installation above) |
| Commands hang or timeout | Ensure Obsidian desktop app is running |
| `Version mismatch` | Update Obsidian to v1.12+ via in-app updater |
| `No vaults found` | Open at least one vault in the Obsidian app |
| Permission denied (macOS) | Run `xattr -cr /Applications/Obsidian.app` |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `obsidian-files` | File/folder CRUD, vault, workspace |
| `obsidian-daily` | Daily notes |
| `obsidian-search` | Search and link graph |
| `obsidian-notes` | Tags, tasks, properties, templates |
| `obsidian-admin` | Plugins, themes, sync, publish |
| `obsidian-dev` | Developer tools and eval |
| `obsidian-kb-bridge` | Knowledge Base integration |
