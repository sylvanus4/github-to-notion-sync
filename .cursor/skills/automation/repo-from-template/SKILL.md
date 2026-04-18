---
name: repo-from-template
description: Create a new GitHub repository from the sylvanus4/cursor-template template, clone it to /Users/hanhyojung/thaki/, and open Cursor IDE. Use when the user asks to "create a new repo from template", "scaffold new project", "new repo from cursor-template", "template repo", "repo-from-template", "새 레포 만들어줘", "템플릿에서 레포 생성", "새 프로젝트 시작", or wants to bootstrap a new repository from the canonical Cursor template. Do NOT use for existing repo management (use github-workflow-automation), general git operations (use domain-commit), repo syncing across projects (use cursor-sync), or cloning arbitrary repos without template intent.
metadata:
  version: 1.0.0
  category: execution
  platforms: [macOS]
---

# Repo From Template

## Role

You are a GitHub repository scaffolder. You create new repositories from `sylvanus4/cursor-template`, clone them locally, and launch Cursor IDE — ready for development in under 60 seconds.

## Tools Used

`gh` (GitHub CLI), `git`, `cursor` (Cursor IDE CLI), `ls`

## Constraints

- **Low freedom** — this is a side-effect skill that creates real GitHub repos, writes to disk, and launches applications
- Requires network connectivity (GitHub API + git remote operations)
- Confirm the new repository name with the user before proceeding
- Never add, modify, or remove files beyond what the template provides
- Abort on directory collision rather than overwriting
- All repos are created under the `sylvanus4` GitHub owner as **private**

## Workflow

```
Step 0: Preflight checks
  ↓
Step 1: Enable template flag on source repo
  ↓
Step 2: Create new GitHub repo from template
  ↓ (fail → Fallback: clone + reinit)
Step 3: Clone to /Users/hanhyojung/thaki/{name}
  ↓
Step 4: Open Cursor IDE
  ↓
Report: Summary
```

### Step 0: Preflight

```bash
gh auth status
ls /Users/hanhyojung/thaki/
```

Verify:
1. `gh` CLI is authenticated with sufficient scopes
2. `/Users/hanhyojung/thaki/` exists
3. `/Users/hanhyojung/thaki/{NEW_NAME}` does NOT exist (collision guard)

If any check fails, report the specific failure and stop.

### Step 1: Enable Template Flag

```bash
IS_TEMPLATE=$(gh api repos/sylvanus4/cursor-template --jq '.is_template')

if [ "$IS_TEMPLATE" != "true" ]; then
  gh api -X PATCH repos/sylvanus4/cursor-template -f is_template=true
fi
```

If the PATCH fails (insufficient permissions), proceed to Step 2 anyway — the fallback handles this.

### Step 2: Create Repository

**Primary path:**
```bash
cd /Users/hanhyojung/thaki/
gh repo create sylvanus4/{NEW_NAME} --template sylvanus4/cursor-template --private --clone
```

`--clone` clones into CWD as `./{NEW_NAME}`, so the `cd` is required to place it at the correct path.

**If `--template` fails**, use the fallback path. See [references/fallback-clone.md](references/fallback-clone.md).

### Step 2 Fallback: Clone + Reinit

```bash
git clone https://github.com/sylvanus4/cursor-template.git /Users/hanhyojung/thaki/{NEW_NAME}
cd /Users/hanhyojung/thaki/{NEW_NAME}
rm -rf .git
git init
git add .
git commit -m "feat: Initialize from cursor-template"
gh repo create sylvanus4/{NEW_NAME} --private --source . --push
```

### Step 3: Verify Clone

```bash
ls /Users/hanhyojung/thaki/{NEW_NAME}
cd /Users/hanhyojung/thaki/{NEW_NAME}
git remote -v
```

Confirm the remote points to `sylvanus4/{NEW_NAME}`.

### Step 4: Open Cursor IDE

```bash
cursor /Users/hanhyojung/thaki/{NEW_NAME}
```

If `cursor` CLI is not available, report instructions to open manually.

## Output Format

**On success:**
```
✅ Repository Created
  - GitHub: https://github.com/sylvanus4/{NEW_NAME}
  - Local:  /Users/hanhyojung/thaki/{NEW_NAME}
  - Cursor: launched (or: manual open required)
  - Method: template (or: fallback clone+reinit)
```

**On failure:**
```
❌ Repository Creation Failed
  - Step failed: {step number and name}
  - Error: {error message}
  - State: {what was created before failure}
  - Recovery: {specific action to clean up or retry}
```

## Verification

After completion, run:
```bash
gh repo view sylvanus4/{NEW_NAME} --json name,url,isPrivate
ls /Users/hanhyojung/thaki/{NEW_NAME}
git -C /Users/hanhyojung/thaki/{NEW_NAME} remote -v
```

All three must pass for the skill to report success.

## Gotchas

1. **Template flag**: `sylvanus4/cursor-template` may have `isTemplate: false`. Step 1 handles this, with Step 2 fallback as backup
2. **Private repo auth**: `gh auth` needs `repo` scope for private template access. If clone fails with 404, check scopes with `gh auth status`
3. **Directory collision**: If `/Users/hanhyojung/thaki/{NEW_NAME}` exists, abort immediately — never overwrite
4. **`cursor` CLI**: Requires Cursor IDE's shell command to be installed (Cursor → Command Palette → "Install 'cursor' command")
5. **`--clone` flag placement**: `gh repo create --template` with `--clone` clones to CWD — the skill `cd`s to the workspace directory first so no move is needed
6. **Partial failure**: If `gh repo create` succeeds but `--clone` fails, the remote repo exists without a local clone. Delete the remote with `gh repo delete sylvanus4/{NEW_NAME} --yes` and retry, or clone manually with `git clone`

## Troubleshooting

### `gh repo create --template` fails with "is not a template"
Cause: Template flag was not enabled or the PATCH API call failed.
Solution: The fallback path (clone + reinit) runs automatically. No user action needed.

### Directory already exists
Cause: A previous run or manual clone left a directory at the target path.
Solution: Remove or rename the existing directory, then retry.

### `cursor` command not found
Cause: Cursor IDE shell integration is not installed.
Solution: Open Cursor IDE → Command Palette (Cmd+Shift+P) → "Shell Command: Install 'cursor' command in PATH"

## Examples

### Example 1: Standard new project
User says: "새 레포 만들어줘, 이름은 my-new-project"
Actions:
1. Step 0: Preflight — gh auth OK, workspace exists, no collision
2. Step 1: Enable template flag — already true, skip
3. Step 2: `cd /Users/hanhyojung/thaki/ && gh repo create sylvanus4/my-new-project --template sylvanus4/cursor-template --private --clone`
4. Step 3: Verify clone at `/Users/hanhyojung/thaki/my-new-project`
5. Step 4: `cursor /Users/hanhyojung/thaki/my-new-project`
Result: New private repo created, cloned, and Cursor opened

### Example 2: Template flag not set (fallback path)
User says: "repo-from-template new-experiment"
Actions:
1. Step 0: Preflight OK
2. Step 1: `gh api -X PATCH` fails (403)
3. Step 2: `gh repo create --template` fails → Fallback: clone + reinit
4. Step 4: Cursor opens
Result: Same outcome via fallback, user sees no difference

## Detail Guides (load when needed)

- [references/fallback-clone.md](references/fallback-clone.md) — detailed fallback clone + remote reset procedure
- [references/config.md](references/config.md) — customization: different template repo, different workspace path
