# Fallback: Clone + Reinit

When `gh repo create --template` fails (template flag not set, API permission issue, or GitHub API downtime), use this procedure.

## Why This Happens

The `sylvanus4/cursor-template` repo's `is_template` flag may be `false`. GitHub requires this flag for the `--template` parameter. The skill attempts to enable it via `gh api -X PATCH`, but this can fail if:

- The authenticated user lacks admin access to the source repo
- GitHub API is rate-limited or down
- The repo is in an organization with template restrictions

## Procedure

```bash
# 1. Clone the template repo content to the target directory
git clone https://github.com/sylvanus4/cursor-template.git /Users/hanhyojung/thaki/{NEW_NAME}

# 2. Enter the cloned directory
cd /Users/hanhyojung/thaki/{NEW_NAME}

# 3. Remove the original git history (fresh start)
rm -rf .git

# 4. Initialize a new git repo
git init

# 5. Stage all template files
git add .

# 6. Create the initial commit
git commit -m "feat: Initialize from cursor-template"

# 7. Create the new GitHub repo and push
gh repo create sylvanus4/{NEW_NAME} --private --source . --push
```

## Differences From Template Path

| Aspect | Template Path | Fallback Path |
|--------|--------------|---------------|
| Git history | Preserves template's commit history | Fresh single commit |
| GitHub "generated from" badge | Yes | No |
| Template repo link on GitHub | Shown | Not shown |
| Final repo content | Identical | Identical |
| Functional difference | None | None |

## Verification

After fallback, the same verification applies:

```bash
gh repo view sylvanus4/{NEW_NAME} --json name,url,isPrivate
ls /Users/hanhyojung/thaki/{NEW_NAME}
git -C /Users/hanhyojung/thaki/{NEW_NAME} remote -v
```
