---
name: hf-hub
description: >-
  Install, authenticate, and configure the Hugging Face CLI (hf) for managing
  models, datasets, repos, jobs, and more from the terminal. Use when the user
  asks to set up hf CLI, authenticate with Hugging Face, manage cache, install
  agent skills, manage extensions, or check environment info. Do NOT use for
  model search (use hf-models), dataset operations (use hf-datasets), jobs
  (use hf-jobs), repo management (use hf-repos), paper discovery (use
  hf-papers), collection management (use hf-collections), discussions (use
  hf-discussions), endpoints (use hf-endpoints), buckets (use hf-buckets), or
  spaces (use hf-spaces). Korean triggers: "HF 설정", "HF 인증", "HF CLI 설치",
  "허깅페이스 설정", "hf 로그인".
---

# Hugging Face Hub CLI — Setup & Reference

One CLI for all of Hugging Face Hub. Built for humans and AI agents.

> For a quick command cheatsheet, see [references/cli-cheatsheet.md](references/cli-cheatsheet.md).

## Installation

```bash
curl -LsSf https://hf.co/cli/install.sh | bash -s
```

Alternative methods:

```bash
uvx hf                        # run directly via uv
pip install -U huggingface_hub[cli] # install via pip (includes hf CLI)
```

Verify: `hf version`

> **Note:** The modern `hf` CLI (Rust binary) replaces the older `huggingface-cli`. Both
> are installed by `pip install huggingface_hub[cli]`, but prefer `hf` for all operations.

## Authentication

### Token Login

```bash
hf auth login                 # interactive prompt for token
hf auth login --token hf_xxx  # non-interactive
```

Tokens are created at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

### Multiple Accounts

```bash
hf auth list                  # list stored tokens
hf auth switch                # switch active token
hf auth whoami                # show current user
hf auth logout                # remove stored token
```

### Org Slug Case Sensitivity (gotcha)

Model/dataset/space repo IDs use the **exact case** of the org slug as registered on the Hub. `HfApi().create_repo("thakicloud/...")` returns `403 Forbidden: don't have rights under namespace "thakicloud"` even when the user is admin of the actual org `ThakiCloud`. Always resolve the canonical case first:

```python
from huggingface_hub import HfApi
api = HfApi()
me = api.whoami()
print([o["name"] for o in me.get("orgs", [])])
# -> ['ThakiCloud']   # use this exact string in repo_id
```

This applies to model/dataset/space repos under an org. User namespaces are likewise case-sensitive but rarely a problem.

### Environment Variable (recommended for agents)

```bash
export HF_TOKEN=hf_xxx
```

## Cache Management

```bash
hf cache ls                   # list cached repos/revisions
hf cache ls --format json     # machine-readable output
hf cache prune                # remove detached revisions
hf cache rm MODEL_ID          # remove specific cached repo
hf cache verify REPO_ID       # verify checksums for cached repo
```

## Skills Management (Agent Integration)

```bash
hf skills add --cursor         # install skill for Cursor IDE
hf skills add --claude         # install skill for Claude Code
hf skills add --codex          # install skill for Codex
hf skills add --cursor --global # install globally
hf skills add --force          # regenerate and overwrite
hf skills preview              # print generated SKILL.md to stdout
```

## Extensions

```bash
hf extensions list             # list installed extensions
hf extensions install REPO_ID  # install from GitHub repo
hf extensions exec NAME        # run an extension
hf extensions remove NAME      # uninstall extension
```

## Environment Info

```bash
hf env                         # print system/library info
hf version                     # print CLI version
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--format json` | Machine-readable JSON output (on list commands) |
| `-q, --quiet` | Print only IDs (one per line) |
| `--token TEXT` | Override auth token for this command |
| `--help` | Show help for any command |

## Discovering Commands

```bash
hf --help                     # list all top-level commands
hf <command> --help            # detailed help for a command
hf <command> <subcommand> --help  # help for a subcommand
```

## Examples

### Example 1: First-time setup

**User says:** "Set up hf CLI"

**Actions:**
1. Install: `curl -LsSf https://hf.co/cli/install.sh | bash -s`
2. Verify: `hf version`
3. Authenticate: `hf auth login`
4. Confirm: `hf auth whoami`

### Example 2: Troubleshooting auth

**User says:** "hf command gives 401 error"

**Actions:**
1. Check auth: `hf auth whoami`
2. If expired/missing: `hf auth login`
3. For agents: verify `HF_TOKEN` env var is set
4. Retry the original command

## Error Handling

| Issue | Resolution |
|-------|-----------|
| `hf: command not found` | Run install script or `pip install -U huggingface_hub` |
| Authentication error (401) | Run `hf auth login` or set `HF_TOKEN` env var |
| Token expired | Run `hf auth login` to refresh |
| Cache corruption | Run `hf cache verify REPO_ID` then `hf cache prune` |
| Permission denied | Check token scopes at huggingface.co/settings/tokens |
