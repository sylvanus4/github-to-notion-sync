---
name: obsidian-daily
description: >-
  Manage Obsidian daily notes via the CLI — open today's daily note, read its
  contents, append or prepend content, and get the file path. Use when the
  user asks to open daily note, add to daily note, read daily note, append
  tasks to daily, prepend content to daily, or get daily note path. Do NOT use
  for general file operations (use obsidian-files), search (use
  obsidian-search), tags or tasks across the vault (use obsidian-notes), or
  plugin management (use obsidian-admin). Korean triggers: "데일리 노트", "일일 노트",
  "오늘 노트", "데일리 추가", "옵시디언 데일리", "일지", "일기 노트", "데일리 작업 추가".
---

# Obsidian CLI — Daily Notes

> **Requires:** Obsidian app running, Daily Notes core plugin enabled. See `obsidian-setup`.

## Prerequisites

- Obsidian CLI configured (`obsidian-setup`)
- Daily Notes core plugin enabled in Obsidian settings
- Date format and folder configured in Daily Notes settings

## Quick Commands

```bash
# Open today's daily note (creates if missing)
obsidian daily

# Get the file path of today's daily note
obsidian daily:path

# Read today's daily note content
obsidian daily:read
obsidian daily:read --copy                   # read and copy to clipboard

# Append content to today's daily note
obsidian daily:append content="- [ ] Buy groceries"
obsidian daily:append content="## Meeting Notes\n- Discussed roadmap"

# Prepend content to today's daily note
obsidian daily:prepend content="# Morning Review"
obsidian daily:prepend content="**Priority:** Ship v2.0"
```

## Discovering Commands

```bash
obsidian help daily          # daily note command details
```

## Common Patterns

### Morning routine — add tasks

```bash
obsidian daily
obsidian daily:append content="## Tasks\n- [ ] Review PRs\n- [ ] Team standup\n- [ ] Write weekly report"
```

### Capture meeting notes into daily

```bash
obsidian daily:append content="## 10:00 Product Sync\n- Agreed on Q2 roadmap\n- Action: Draft PRD by Friday"
```

### Read daily for pipeline context

```bash
obsidian daily:read --copy
```

### End-of-day log

```bash
obsidian daily:append content="## EOD Summary\n- Shipped auth feature\n- 3 PRs merged\n- Blocked on API key rotation"
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Daily notes not enabled` | Core plugin disabled | Enable in Settings → Core plugins → Daily notes |
| `Template not found` | Daily note template path wrong | Check Settings → Daily notes → Template file location |
| `No active vault` | Vault not open | Open vault in Obsidian app |
