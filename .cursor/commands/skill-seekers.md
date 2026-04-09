---
description: "Convert GitHub repos, doc sites, PDFs, or videos into structured Cursor skill files with conflict detection"
---

# Skill Seekers — Source-to-Skill Converter

## Skill Reference

Read and follow the skill at `.cursor/skills/automation/skill-seekers/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Source

Extract from user arguments:

- **source** (required): GitHub repo (`owner/repo`), URL, local path, or PDF
- **name** (optional): Override the skill name (default: derived from source)
- **target** (optional): `cursor` (default)
- **enhance** (optional): Enhancement preset (`security-focus`, `architecture-comprehensive`, `api-deep-dive`)
- **skip-conflicts** (optional): Skip conflict detection

If no source is provided, ask the user what they want to convert.

### Step 2: Pre-flight

1. Check `skill-seekers` CLI installation:

```bash
skill-seekers --version
```

2. If not installed:

```bash
pip install skill-seekers[all]
```

### Step 3: Detect Source Type and Execute

| Source Pattern | Action |
|---|---|
| `owner/repo` or GitHub URL | `skill-seekers github --repo <owner/repo>` |
| `https://` doc site URL | `skill-seekers create <url>` |
| `*.pdf` file path | `skill-seekers pdf --pdf <file> --name <name>` |
| YouTube URL | `skill-seekers video --url <url> --name <name>` |
| Local directory | `skill-seekers create <path>` |
| Config preset name | `skill-seekers install --config <name>` |

### Step 4: Package for Cursor

```bash
skill-seekers package output/<name> --target cursor
```

### Step 5: Conflict Detection

Unless `--skip-conflicts` was specified:

```bash
skill-seekers detect-conflicts output/<name>/ --skills-dir .cursor/skills/
```

Report any overlaps with existing skills and ask the user how to proceed.

### Step 6: Install

```bash
skill-seekers install-agent output/<name>/ --agent cursor
```

Or manually copy to `.cursor/skills/<category>/<name>/`.

### Step 7: Enhancement (Optional)

If `--enhance` was specified or user requests it:

```bash
skill-seekers enhance output/<name>/ --preset <preset>
```

### Step 8: Post-Install Verification

1. Verify SKILL.md exists at the installed location
2. Confirm frontmatter has `name`, `description`, `metadata`
3. Confirm SKILL.md is under 500 lines (excess should be in `references/`)
4. Report installed skill name, location, and trigger phrases

## Examples

```bash
/skill-seekers addyosmani/agent-skills               # GitHub repo
/skill-seekers https://docs.react.dev/                # Doc site
/skill-seekers manual.pdf --name product-manual       # PDF
/skill-seekers owner/repo --enhance api-deep-dive     # With enhancement
/skill-seekers --list-configs                         # List available presets
```

## Constraints

- Always run conflict detection before installing (unless explicitly skipped)
- Do not overwrite existing skills without user confirmation
- If the source is a large repo, warn about processing time
