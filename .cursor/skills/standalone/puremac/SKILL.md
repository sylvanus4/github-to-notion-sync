---
name: puremac
description: >-
  Operate PureMac (open-source macOS cleaner) for disk maintenance:
  Smart Scan, category cleaning, scheduling, pre/post audit, and
  developer-workflow integration. Use when the user asks to "clean
  my Mac", "free up disk space", "run PureMac", "Mac cleanup",
  "맥 정리", "디스크 정리", "PureMac", "puremac", "Smart Scan",
  "Xcode 캐시 정리", "Homebrew 캐시", "Docker 정리",
  "developer disk maintenance", "scheduled cleanup", or any macOS
  disk space recovery request. Do NOT use for Docker-specific
  operations (use Shell directly). Do NOT use for Homebrew package
  management (use Shell directly). Do NOT use for cloud
  infrastructure disk issues (use sre-devops-expert).
---

# PureMac — macOS Disk Maintenance Skill

## What Is PureMac

PureMac is a free, open-source, native SwiftUI macOS cleaner — a CleanMyMac alternative with zero telemetry. It scans and cleans 8 categories of disk waste and supports scheduled automated cleaning via LaunchAgent.

Repository: https://github.com/momenbasel/PureMac

## Installation

```bash
# Homebrew (recommended)
brew tap momenbasel/tap
brew install --cask puremac

# Verify
open -a PureMac
```

Manual: download `.dmg` from GitHub Releases, drag to `/Applications`.

## Cleaning Categories

| # | Category | What It Targets | Typical Size | Safety |
|---|----------|-----------------|-------------|--------|
| 1 | System Junk | `/Library/Caches/*`, `/System/Library/Caches/*`, system temp | 100M–2G | Safe |
| 2 | User Cache | `~/Library/Caches/*` (browser, pip, yarn, npm, poetry, etc.) | 5–30G | Safe — apps rebuild |
| 3 | Mail Attachments | `~/Library/Mail Downloads`, `~/Library/Containers/com.apple.mail/…` | 0–5G | Safe if backed up |
| 4 | Trash | `~/.Trash` | 0–10G | Safe |
| 5 | Large & Old Files | Files >100MB or untouched >90 days in ~/Downloads, ~/Documents, ~/Desktop | Varies | Review before deleting |
| 6 | Xcode Junk | `~/Library/Developer/Xcode/DerivedData`, Archives, CoreSimulator Caches | 0–50G | Safe to clean periodically |
| 7 | Homebrew Cache | `~/Library/Caches/Homebrew` | 100M–2G | Safe — `brew cleanup` equivalent |
| 8 | Purgeable Space | APFS purgeable blocks (Time Machine local snapshots, etc.) | 0–100G+ | Safe — OS reclaims on demand |

## Workflow

### 1. Pre-Cleaning Audit

Run before PureMac to capture baseline:

```bash
df -h / | tail -1
echo "---"
du -sh ~/Library/Caches 2>/dev/null
du -sh ~/Library/Developer/Xcode/DerivedData 2>/dev/null
du -sh ~/Library/Caches/Homebrew 2>/dev/null
du -sh ~/.Trash 2>/dev/null
```

### 2. Smart Scan (Recommended First Run)

1. Open PureMac
2. Click **Smart Scan** — scans all 8 categories in parallel
3. Review the results per category
4. **Deselect** anything in "Large & Old Files" you want to keep
5. Click **Clean**

### 3. Category-by-Category Cleaning

For targeted cleanup, select individual categories from the sidebar:

- **Quick wins (safe, always clean):** System Junk → User Cache → Trash → Homebrew Cache
- **Developer-specific:** Xcode Junk (after major builds)
- **Review required:** Large & Old Files (manually verify each item)
- **On-demand:** Purgeable Space (runs `diskutil apfs purgePurgeable /`)

### 4. Post-Cleaning Audit

```bash
df -h / | tail -1
```

Compare available space before vs after.

### 5. Scheduled Cleaning

PureMac supports automatic scheduled cleaning via a LaunchAgent:

1. Open PureMac → Settings/Preferences
2. Enable scheduled cleaning
3. Set interval: **Weekly** recommended for developers
4. Select categories to auto-clean: System Junk, User Cache, Trash, Homebrew Cache
5. Optionally enable auto-purge for purgeable space

The scheduler installs `~/Library/LaunchAgents/com.puremac.scheduler.plist`.

## Developer-Specific Maintenance (Beyond PureMac)

PureMac handles general macOS cache/junk. For developer workstations, add these:

### Docker Cleanup

```bash
docker system prune -a --volumes  # removes ALL unused images, containers, volumes
docker system df                   # verify after
```

### npm / pip / yarn / pnpm Cache

```bash
npm cache clean --force
pip cache purge
yarn cache clean
pnpm store prune
```

### Cursor / VS Code Extensions Data

```bash
du -sh ~/Library/Application\ Support/Cursor
du -sh ~/Library/Application\ Support/Code
```

Large Cursor data is often from extension caches and can be pruned selectively.

### Playwright Browsers

```bash
du -sh ~/Library/Caches/ms-playwright
npx playwright install --with-deps  # reinstalls only needed browsers
```

## Safety Guidelines — What NOT to Clean

| Never Delete | Why |
|-------------|-----|
| `~/Library/Application Support/*` | App data, credentials, configs |
| `~/Library/Keychains/` | Login credentials, certificates |
| `~/Library/Preferences/` | App preferences |
| `~/.ssh/`, `~/.gnupg/` | SSH keys, GPG keys |
| `~/.config/` | CLI tool configs |
| Active project `node_modules/` | Reinstallable but takes time |
| Docker named volumes with data | Check before pruning |

## Recommended Maintenance Schedule

| Cadence | Action |
|---------|--------|
| **Daily** | Empty Trash (if >1GB) |
| **Weekly** | PureMac Smart Scan (auto via scheduler) |
| **Monthly** | Docker `system prune -a --volumes`, npm/pip/yarn cache purge |
| **Quarterly** | Review Large & Old Files, Xcode DerivedData/Archives full cleanup |
| **After major installs** | Clean downloaded `.dmg` files from Downloads |

## Integration with Development Workflow

- **After Docker image builds**: Run `docker system prune` to remove dangling layers
- **After Xcode builds**: Clean DerivedData if switching between many projects
- **Before demos/presentations**: Run PureMac Smart Scan to free maximum space
- **When disk warning appears**: Run full cleanup sequence (PureMac + Docker prune + dev cache purge)
