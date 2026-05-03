---
name: obsidian-files
description: >-
  Manage Obsidian vault files, folders, workspaces, and bookmarks via the
  Obsidian CLI — create, read, move, rename, delete notes, list vault
  contents, and manage workspaces. Use when the user asks to create a note,
  read a note, move files, list vault contents, manage workspaces, manage
  bookmarks, or perform any file operation in Obsidian. Do NOT use for daily
  notes (use obsidian-daily), search (use obsidian-search), tags or tasks (use
  obsidian-notes), plugin management (use obsidian-admin), or developer tools
  (use obsidian-dev). Korean triggers: "옵시디언 파일", "노트 생성", "노트 읽기", "볼트 관리",
  "옵시디언 폴더", "워크스페이스", "북마크", "파일 이동", "파일 삭제".
---

# Obsidian CLI — Files, Vaults & Workspaces

> **Requires:** Obsidian app running, CLI in PATH. See `obsidian-setup`.

## Prerequisites

- Obsidian CLI configured (`obsidian-setup`)
- Target vault open in Obsidian
- For multi-vault setups, use `vault=<name>` to target a specific vault

## Quick Commands

### Vault Operations

```bash
obsidian vaults                          # list all vaults
obsidian vault                           # show current vault info
obsidian vault:open name="My Vault"      # switch to / open a vault
```

### File CRUD

```bash
# Create
obsidian create name="Meeting Notes"                          # new empty note
obsidian create name="Trip" template=Travel                   # from template
obsidian create name="Notes/2024/Q1 Review"                   # with path
obsidian create name="Quick Note" content="Initial content"   # with content

# Read
obsidian read                              # read current open file
obsidian read file="Meeting Notes"         # read specific file
obsidian read file="README" --copy         # read and copy to clipboard

# Update
obsidian append file="Journal" content="- New entry"    # append to file
obsidian prepend file="Journal" content="# Header"      # prepend to file
obsidian rename file="old-name" to="new-name"           # rename file

# Delete (use with care)
obsidian trash file="Outdated Note"        # move to trash
```

### Navigation

```bash
obsidian open file="Meeting Notes"         # open file in Obsidian
obsidian open file="Note" line=42          # open at specific line
obsidian list                              # list all files in vault
obsidian list folder="Projects"            # list files in a folder
```

### Folders

```bash
obsidian folder:create path="Projects/2024"    # create folder
obsidian folder:move from="Old" to="Archive"   # move folder
obsidian folder:delete path="Empty Folder"     # delete empty folder
```

### Workspaces

```bash
obsidian workspaces                            # list workspaces
obsidian workspace:load name="Writing"         # load a workspace
obsidian workspace:save name="Current"         # save current layout
obsidian workspace:delete name="Old Layout"    # delete workspace
```

### Bookmarks

```bash
obsidian bookmarks                             # list all bookmarks
obsidian bookmark:add file="Important Note"    # bookmark a note
obsidian bookmark:remove file="Old Note"       # remove bookmark
```

### Version History

```bash
obsidian diff file="README"                    # show recent changes
obsidian diff file="README" from=1 to=3       # compare versions
```

## Discovering Commands

```bash
obsidian help vault          # vault commands
obsidian help create         # file creation options
obsidian help list           # listing options
obsidian help workspace      # workspace management
```

## Common Patterns

### Create a structured project

```bash
obsidian create name="Projects/Alpha/README" template=Project
obsidian create name="Projects/Alpha/Tasks"
obsidian create name="Projects/Alpha/Notes"
```

### Batch read for context

```bash
obsidian read file="Architecture" --copy
obsidian read file="API Design" --copy
```

### Safe file moves

Always verify the target path before moving:

```bash
obsidian list folder="Archive"                  # check destination exists
obsidian rename file="Draft" to="Archive/Draft" # move to archive
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `File not found` | Wrong path or missing `.md` extension | Use exact name without `.md` |
| `Vault not found` | Vault not open in Obsidian | Open vault in app first |
| `File already exists` | Duplicate name on create | Choose a different name |
| `Permission denied` | Vault on read-only filesystem | Check filesystem permissions |
