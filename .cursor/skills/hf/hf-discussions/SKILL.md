---
name: hf-discussions
description: >-
  Manage discussions and pull requests on Hugging Face Hub repos via the hf CLI.
  Use when the user asks to list discussions, create a PR on an HF repo, comment
  on a discussion, merge a pull request, view PR diffs, or manage community
  interactions on Hub repositories. Do NOT use for GitHub PRs (use gh CLI),
  repo lifecycle management (use hf-repos), model search (use hf-models),
  or dataset operations (use hf-datasets).
  Korean triggers: "HF 토론", "HF PR", "허브 풀리퀘스트", "HF 디스커션".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "ml"
---
# Hugging Face Discussions

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.

## Quick Commands

### List Discussions

```bash
hf discussions list REPO_ID
hf discussions list REPO_ID --kind pull_request --status open
hf discussions list REPO_ID --author username --format json
```

| Flag | Required | Description |
|------|----------|-------------|
| `REPO_ID` | Yes | Repository ID |
| `--kind` | No | `all` (default), `discussion`, `pull_request` |
| `--status` | No | `open`, `closed`, `merged`, `draft`, `all` |
| `--author` | No | Filter by author |
| `--type` | No | Repo type: `model`, `dataset`, `space` |
| `--format [table\|json]` | No | Output format |

### Get Discussion Info

```bash
hf discussions info REPO_ID NUM
hf discussions info REPO_ID NUM --comments   # include comments
hf discussions info REPO_ID NUM --diff        # show PR diff
```

### Create Discussion / Pull Request

```bash
hf discussions create REPO_ID --title "Fix typo in README"
hf discussions create REPO_ID --title "Update model card" --pull-request
hf discussions create REPO_ID --title "Bug report" --body "Description here"
```

> **Write command** — confirm with the user before creating.

| Flag | Required | Description |
|------|----------|-------------|
| `REPO_ID` | Yes | Target repository |
| `--title` | Yes | Discussion/PR title |
| `--pull-request` | No | Create as pull request (not discussion) |
| `--body` | No | Description body |
| `--type` | No | Repo type if ambiguous |

### Comment

```bash
hf discussions comment REPO_ID NUM --body "LGTM, merging!"
```

> **Write command** — confirm comment content with the user.

### Merge Pull Request

```bash
hf discussions merge REPO_ID NUM
hf discussions merge REPO_ID NUM --comment "Approved and merging"
```

> **Write command** — confirm merge with the user.

### Status Changes

```bash
hf discussions close REPO_ID NUM
hf discussions reopen REPO_ID NUM
hf discussions rename REPO_ID NUM "New Title"
```

### View Diff

```bash
hf discussions diff REPO_ID NUM
```

## Common Patterns

```bash
# List open PRs on a model repo
hf discussions list my-org/my-model --kind pull_request --status open --format json

# Create a PR to update model card
hf discussions create my-org/my-model \
  --title "Update model card with eval results" \
  --pull-request \
  --body "Added benchmark scores from latest evaluation run"

# Review and merge a PR
hf discussions info my-org/my-model 5 --diff --comments
hf discussions comment my-org/my-model 5 --body "Looks good!"
hf discussions merge my-org/my-model 5 --comment "Merging after review"

# Monitor community activity on a popular model
hf discussions list meta-llama/Llama-3.2-1B --status open --format json

# Close resolved discussions
hf discussions close my-org/my-model 3
```

## Examples

### Example 1: Create and manage a PR

**User says:** "Create a PR to fix the README on my model repo"

**Actions:**
1. Create PR: `hf discussions create my-org/my-model --title "Fix README formatting" --pull-request --body "Fixed markdown formatting issues"`
2. Check status: `hf discussions info my-org/my-model NUM`
3. After review: `hf discussions merge my-org/my-model NUM`

### Example 2: Monitor community discussions

**User says:** "Are there any open issues on this model?"

**Actions:**
1. List: `hf discussions list REPO_ID --kind discussion --status open`
2. Check PRs too: `hf discussions list REPO_ID --kind pull_request --status open`
3. Summarize findings for the user

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Discussion not found | Verify REPO_ID and discussion number |
| Permission denied | You need write access to create/merge on the repo |
| Merge conflict | Review diff with `hf discussions diff REPO_ID NUM`, resolve manually |
| Cannot comment | Check authentication and repo access permissions |
