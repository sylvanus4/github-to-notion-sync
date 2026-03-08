## Skill Seekers

Convert documentation sites, GitHub repos, PDFs, and videos into structured Cursor skill files with automatic conflict detection.

### Usage

```
/skill-seekers <url>                    # Convert docs URL into a Cursor skill
/skill-seekers <owner/repo>             # Convert GitHub repo into a skill
/skill-seekers <path.pdf>               # Convert PDF into a skill
/skill-seekers --preset react           # Use a preset config
/skill-seekers --conflicts <output-dir> # Detect conflicts with existing skills
/skill-seekers --list-presets           # List available config presets
/skill-seekers --install                # Install Skill Seekers CLI
```

### Workflow

1. **Install** (first time) — Run `bash .cursor/skills/skill-seekers/scripts/install.sh`
2. **Create** — Run `skill-seekers create <source>` to scrape and build
3. **Package** — Run `skill-seekers package output/<name> --target cursor`
4. **Conflict check** — Run `skill-seekers detect-conflicts output/<name>/ --skills-dir .cursor/skills/`
5. **Install** — Copy output to `.cursor/skills/<name>/` or run `skill-seekers install-agent output/<name>/ --agent cursor`

### Execution

Read and follow the `skill-seekers` skill (`.cursor/skills/skill-seekers/SKILL.md`) for detailed CLI commands, MCP setup, and packaging guidelines.

### Examples

Convert React docs into a skill:

```
/skill-seekers https://docs.react.dev/
```

Convert a GitHub repo with conflict detection:

```
/skill-seekers facebook/react
```

List presets:

```
/skill-seekers --list-presets
```
