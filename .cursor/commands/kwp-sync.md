---
description: "Sync Knowledge Work Plugins from GitHub. Updates existing rules and adds new ones from anthropics/knowledge-work-plugins."
---

# /kwp-sync

Synchronize Anthropic Knowledge Work Plugins with this project's Cursor rules.

## Usage

```
/kwp-sync                    # Full sync — all 14 plugins
/kwp-sync engineering        # Sync only the engineering plugin
/kwp-sync finance legal      # Sync specific plugins
```

## What This Does

1. Read the `kwp-sync` skill from `.cursor/skills/kwp-sync/SKILL.md`
2. Execute the 10-step sync workflow:
   - Clone/pull upstream repo
   - Convert skills and commands to `.mdc` rules
   - Replace `~~category` placeholders (see `references/placeholder-map.md`)
   - Strip Cowork-specific patterns
   - Add negative triggers for overlap with existing project skills
   - Truncate oversized files (>400 lines)
   - Regenerate `kwp-index.mdc`
   - Clean up temp files
3. Report results (files added, updated, removed)

## Arguments

- No arguments: full sync of all 14 plugins
- Plugin name(s): sync only specified plugins

## Available Plugins

`bio-research`, `customer-support`, `data`, `design`, `engineering`, `enterprise-search`, `finance`, `human-resources`, `legal`, `marketing`, `operations`, `product-management`, `productivity`, `sales`
