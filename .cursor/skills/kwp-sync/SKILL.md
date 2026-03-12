---
name: kwp-sync
description: >-
  Sync Anthropic Knowledge Work Plugins from GitHub to Cursor IDE rules. Use
  when the user asks to "update KWP rules", "sync knowledge-work-plugins",
  "refresh KWP", "add a new KWP plugin", or "check for upstream KWP changes". Do
  NOT use for optimizing existing skills (use skill-optimizer) or creating new
  skills from scratch (use skill-creator). Korean triggers: "동기화", "최적화", "체크",
  "스킬".
metadata:
  version: "1.0.0"
  category: "execution"
  author: "anthropic-kwp"
---
# KWP Sync

Synchronize [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) into Cursor IDE skills (`.cursor/skills/kwp-*/SKILL.md`), commands (`.cursor/commands/kwp-*.md`), and the index rule (`.cursor/rules/kwp-index.mdc`). Supports full sync, incremental updates, and selective plugin import.

## Workflow

### Step 1: Clone or Pull Upstream

```bash
cd /tmp
if [ -d knowledge-work-plugins ]; then
  cd knowledge-work-plugins && git pull
else
  git clone --depth 1 https://github.com/anthropics/knowledge-work-plugins.git
fi
```

### Step 2: Detect Scope

Determine which plugins to sync. Available plugins (19 domains):

**Core plugins (14):** `bio-research`, `customer-support`, `data`, `design`, `engineering`, `enterprise-search`, `finance`, `human-resources`, `legal`, `marketing`, `operations`, `product-management`, `productivity`, `sales`

**Partner-built sub-plugins (4):** `apollo`, `brand-voice`, `common-room`, `slack` (nested under `partner-built/`)

**Meta plugin (1):** `cowork-plugin-management`

If user requests a full sync, process all 19. If selective, process only requested plugins.

### Step 3: Convert Skills and Commands

**Skills** (`{plugin}/skills/*/SKILL.md` -> `.cursor/skills/kwp-{domain}-{skill}/SKILL.md`):
1. Parse YAML frontmatter, extract `description`
2. Extract body content
3. Create skill directory with proper frontmatter (`name`, `description` with negative triggers, `metadata`)
4. Add `## Examples` and `## Troubleshooting` sections if missing
5. For skills >500 lines, extract large sections to `references/` subdirectory

**Commands** (`{plugin}/commands/*.md` -> `.cursor/commands/kwp-{domain}-{command}.md`):
1. Parse YAML frontmatter, extract `description`
2. Remove `[Command]` prefix from description
3. Format with domain/action header and body content

**Naming for partner-built:** Use sub-plugin name directly (e.g., `partner-built/apollo/skills/enrich-lead/` -> `kwp-apollo-enrich-lead`).

### Step 4: Replace Placeholders

Replace `~~category` placeholders with actual tools using the mapping in [references/placeholder-map.md](references/placeholder-map.md).

### Step 5: Strip Cowork-Specific Patterns

Remove or rewrite:
- `${CLAUDE_PLUGIN_ROOT}` path references
- `dashboard.html` file-based UI references
- `/plugin:command` slash syntax -> `@kwp-plugin-command`
- `CONNECTORS.md` references

### Step 6: Add Negative Triggers for Overlaps

Append "Do NOT use for..." clauses to skill descriptions that overlap with project-specific skills:

| KWP Skill | Overlapping Project Skills |
|-----------|---------------------------|
| engineering-code-review | backend-expert, security-expert |
| engineering-testing-strategy | qa-test-expert, e2e-testing |
| engineering-documentation | technical-writer |
| engineering-incident-response | sre-devops-expert |
| engineering-system-design | backend-expert |
| design-accessibility-review | ux-expert |
| design-design-critique | design-architect |
| operations-compliance-tracking | compliance-governance |
| operations-risk-assessment | security-expert |

### Step 7: Optimize with skill-optimizer

Run skill-optimizer on all new/changed skills to ensure:
- Proper frontmatter (`name`, `description`, `metadata`)
- Under 500 lines (extract to `references/` if needed)
- `## Examples` and `## Troubleshooting` sections present
- No redundant "When to Use" sections

### Step 8: Regenerate Index

Regenerate `.cursor/rules/kwp-index.mdc` listing all KWP skills and commands grouped by domain.

### Step 9: Cleanup

Remove `/tmp/knowledge-work-plugins/` and any temp scripts.

### Step 10: Report

Output a sync report.

## Output Format

```
KWP Sync Report
================
Date: [YYYY-MM-DD]
Domains synced: [list]
Skills added: [N]
Skills updated: [N]
Commands added: [N]
Commands updated: [N]
Total: [N] skills, [N] commands across [N] domains

Changes:
  [domain]: +[N] new skills, ~[N] updated, +[N] new commands
  ...

Optimization: [N] skills modified, all under 500 lines
```

## Examples

### Example 1: Full sync
User says: "Sync all KWP plugins from GitHub"
Actions: Clone/pull -> convert all 19 domains to skills + commands -> optimize -> regenerate index -> report.
Result: All 92 skills and 79 commands updated.

### Example 2: Add a single plugin
User says: "Add the finance plugin from KWP"
Actions: Clone/pull -> convert only finance skills + commands -> optimize -> update index -> report.
Result: Finance skills/commands added under `kwp-finance-*`.

### Example 3: Incremental upstream sync
User says: "Check for KWP updates and sync changes"
Actions: Clone/pull -> diff against local assets -> convert new + update changed -> optimize -> regenerate index -> cursor-sync to targets.
Result: Only delta changes applied, existing assets preserved.

## Troubleshooting

### Conversion script fails on multi-line YAML description
Cause: Some SKILL.md files use YAML `>` for multi-line descriptions
Solution: Use a proper YAML-aware parser (Python preferred) instead of sed/awk

### Placeholder not replaced
Cause: New `~~category` placeholder not in the mapping table
Solution: Add the new mapping to `references/placeholder-map.md` and re-run

### File too large after conversion
Cause: Skill has many reference files that get inlined
Solution: Keep only the core SKILL.md content and summarize references
