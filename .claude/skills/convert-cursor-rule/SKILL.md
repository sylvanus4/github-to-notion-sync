---
name: convert-cursor-rule
description: >-
  Convert Cursor rules, prompts, or workflow files into Claude Code CLAUDE.md
  instructions or project skills. Use when migrating Cursor assets to Claude Code format.
disable-model-invocation: true
arguments: [source_file, target_type]
---

# Convert Cursor Rule

Convert `$source_file` from Cursor format into Claude Code format.

Target type: `$target_type` (one of: `rule`, `skill`, `auto`)

## Usage

```
/convert-cursor-rule .cursor/rules/my-rule.mdc skill
/convert-cursor-rule .cursor/rules/my-rule.mdc rule
/convert-cursor-rule .cursor/rules/my-rule.mdc auto
```

## Classification Logic

When `$target_type` is `auto`, classify based on content:

| Content Type | Destination |
|-------------|-------------|
| Always-on project conventions, coding standards | `CLAUDE.md` or `.claude/rules/*.md` |
| Repeatable workflow with steps | `.claude/skills/<name>/SKILL.md` |
| Long reference/examples (>100 lines) | Supporting files in skill directory |

## Conversion Rules

1. **YAML Frontmatter**: Every `SKILL.md` needs `name`, `description`
2. **Side Effects**: If the workflow modifies files, commits, deploys, or calls external APIs, add `disable-model-invocation: true`
3. **Size Limit**: Keep `SKILL.md` under 500 lines; extract long content to `reference.md` or `examples.md`
4. **Intent Preservation**: Keep the original skill's purpose, constraints, and output format intact
5. **Arguments**: Map Cursor `$SELECTION` or `$FILE` to Claude Code `$ARGUMENTS`
6. **No Deletion**: Never delete the original Cursor file

## Output

1. **Classification**: rule / skill / hybrid
2. **Recommended target path**: `.claude/rules/X.md` or `.claude/skills/X/SKILL.md`
3. **Converted content**: Full file content ready to write
4. **Assumptions**: Any decisions made during conversion
5. **Test invocation**: How to verify the converted skill works

## Important

- Do NOT modify files until the user approves the conversion plan
- Do NOT delete original Cursor files
- Preserve Korean content in user-facing output templates
- All structural/instructional content in English per skill authoring convention

## Test Invocation

```
/convert-cursor-rule .cursor/rules/critical-thinking.mdc auto
/convert-cursor-rule .cursor/skills/review/deep-review/SKILL.md skill
```
