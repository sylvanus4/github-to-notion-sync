# Codemap

Generate or refresh the project's CODEMAP.md — a compact navigation reference for agents and developers.

## Usage

```bash
# Display current codemap (or generate if missing)
/codemap

# Full refresh from scratch
/codemap --refresh

# Show what changed since last update
/codemap --diff
```

## Instructions

Use the `codemap-updater` skill to execute this command. Read the skill at `.cursor/skills/standalone/codemap-updater/SKILL.md` and follow its workflow.

Key points:
- Output goes to `CODEMAP.md` at the project root
- Keep the file under 500 lines
- Include: architecture overview, entry points, directory map, module index, hot files, dependency overview
- On `--diff` mode, compare the existing CODEMAP.md against the actual project state and report additions/removals
