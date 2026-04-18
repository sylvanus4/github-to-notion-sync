# Configuration

Default values are hardcoded in the skill for zero-config usage. Override any of these when invoking the skill.

## Defaults

| Parameter | Default | Description |
|-----------|---------|-------------|
| Template repo | `sylvanus4/cursor-template` | Source template repository |
| GitHub owner | `sylvanus4` | Owner for the new repo |
| Workspace path | `/Users/hanhyojung/thaki/` | Local clone destination |
| Visibility | `private` | New repo visibility |
| IDE command | `cursor` | CLI command to launch the editor |

## Overriding Defaults

When invoking the skill, specify overrides in natural language:

```
"새 레포 만들어줘, 이름은 my-project, public으로"
→ Overrides: visibility = public

"repo-from-template my-project --workspace ~/projects/"
→ Overrides: workspace path = ~/projects/

"create repo from sylvanus4/other-template named my-project"
→ Overrides: template repo = sylvanus4/other-template
```

## Using a Different Template Repo

If the template repo changes, the skill adjusts these commands:

1. **Step 1** (Enable template flag): targets the new repo
2. **Step 2** (Create repo): uses `--template {new-template-repo}`
3. **Fallback**: clones `{new-template-repo}` instead

No SKILL.md modification is needed — pass the override at invocation time.

## Using a Different Workspace Path

The skill checks that the target directory exists and that the repo name subdirectory does not collide. Any valid absolute path works.

## IDE Command

If `cursor` is not available, the skill reports this and provides manual instructions. Other supported editor commands:

- `code` — VS Code
- `cursor` — Cursor IDE (default)
- `zed` — Zed editor
