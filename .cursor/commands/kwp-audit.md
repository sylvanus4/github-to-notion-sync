---
description: "Audit Knowledge Work Plugin rules. Check for upstream updates, list installed plugins, and report rule statistics without making changes."
---

# /kwp-audit

Read-only audit of installed KWP rules and upstream availability.

## Usage

```
/kwp-audit                   # Full audit
/kwp-audit --upstream        # Check for upstream changes
/kwp-audit --stats           # Show file size and count statistics
```

## What This Does

1. Inventory all KWP `.mdc` files in `.cursor/rules/` (matching `{plugin}-*.mdc` and `cmd-{plugin}-*.mdc` patterns)
2. Count skills vs commands per plugin
3. Report file sizes and flag any over 400 lines
4. Check for `~~` placeholder remnants
5. If `--upstream` flag: clone/pull upstream repo and diff against local rules to report new, changed, or removed files
6. Output audit report (no files are modified)

## Report Format

```
KWP Audit Report
=================
Date: YYYY-MM-DD

Installed Plugins: [N]/14
  [plugin]: [N] skills, [N] commands
  ...

File Statistics:
  Total rules: [N]
  Average size: [N] lines
  Over 400 lines: [N] files
  Placeholder remnants: [N] files

Upstream Diff (if --upstream):
  New upstream files: [N]
  Changed files: [N]
  Removed upstream: [N]
```
