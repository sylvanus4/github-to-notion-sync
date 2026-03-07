# PR Template and Branch Target Mapping

## PR Body Template

```markdown
## Issue?
Resolves #${ISSUE_NUMBER}

## Changes?
- Change description 1
- Change description 2
- Change description 3

## Why we need?
Brief explanation of why these changes are necessary.

## Test?
- [ ] Test item 1
- [ ] Test item 2

## CC (Optional)
<!-- Tag reviewers if needed -->

## Anything else? (Optional)
<!-- Additional context -->
```

When updating an existing PR, preserve the original body structure and append new changes under the `## Changes?` section with a `**[NEW]**` prefix.

## PR Title Format

```
#<ISSUE_NUMBER> [<TYPE>] <Summary>
```

- Issue number extracted from branch name (`issue/{N}-*` or `epic/{N}`)
- TYPE: `feat`, `enhance`, `refactor`, `docs`, `fix`, `style`, `test`, `chore`
- Summary: English imperative, max 50 chars, no trailing period
- If no issue number in branch, omit the `#N` prefix

Examples:
- `#42 [enhance] Add user authentication`
- `#15 [docs] Update API documentation`
- `[chore] Update CI configuration` (no issue number)

## Branch-to-Target Mapping

| Branch pattern | Target branch | Example |
|----------------|---------------|---------|
| `issue/{N}-*` | `dev` | `issue/42-add-auth` → `dev` |
| `epic/{N}` | `dev` | `epic/11` → `dev` |
| `release-v*` | `main` | `release-v1.2` → `main` |
| other | `dev` | `feature/experiment` → `dev` |

Override with `--base <branch>` flag when needed.
