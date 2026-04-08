---
name: runpod-setup
description: >-
  Install, authenticate, and verify the RunPod CLI (runpodctl) for managing
  GPU cloud resources from the terminal. Use when the user asks to "install
  runpodctl", "RunPod setup", "configure RunPod", "RunPod auth", "RunPod
  login", "runpod-setup", "RunPod 설치", "RunPod 설정", "RunPod 인증",
  or needs to set up RunPod CLI access for the first time.
  Do NOT use for pod lifecycle management (use runpod-pods).
  Do NOT use for network volume operations (use runpod-volumes).
  Do NOT use for file transfer (use runpod-transfer).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infra"
  upstream: "runpod/runpodctl"
---

# RunPod CLI Setup

Install, authenticate, and verify `runpodctl` for managing RunPod GPU cloud resources.

## Prerequisites

- **`RUNPOD_API_KEY`** environment variable — obtain from [runpod.io/console/user/settings](https://www.runpod.io/console/user/settings)

## Workflow

### Phase 1: Check Existing Installation

```bash
command -v runpodctl >/dev/null 2>&1 && runpodctl version || echo "NOT INSTALLED"
```

If already installed and the user just needs auth, skip to Phase 3.

### Phase 2: Install

Choose the method appropriate for the user's OS:

**macOS (Homebrew — recommended):**
```bash
brew install runpod/runpodctl/runpodctl
```

**Linux / macOS (install script):**
```bash
wget -qO- cli.runpod.net | sudo bash
```

**conda:**
```bash
conda install conda-forge::runpodctl
```

Verify installation:
```bash
runpodctl version
```

### Phase 3: Authenticate

Configure the API key from the environment variable:

```bash
runpodctl config --apiKey "$RUNPOD_API_KEY"
```

Alternatively, run the interactive doctor which prompts for the key:

```bash
runpodctl doctor
```

### Phase 4: Verify Connectivity

Confirm authentication and network connectivity by listing available GPUs:

```bash
runpodctl gpu list --output json
```

A successful response with GPU data confirms the setup is complete. An auth error means the API key is invalid or missing.

### Phase 5: Report

Present results:

```
RunPod CLI Setup
=================
Version:    <runpodctl version output>
Auth:       PASS / FAIL
GPU List:   <N> GPU types available
Status:     READY / NOT READY
```

## Output Discipline

- Report only: version, auth status, GPU count. Do not list all GPU types or suggest next steps beyond setup.
- Do not pad output with usage examples — the user will invoke `runpod-pods` when ready.

## Gotchas

- The install script (`cli.runpod.net`) requires `sudo` on Linux; on macOS Homebrew is preferred.
- `runpodctl config` writes to `~/.runpod/config.toml` — the API key is stored there, not in `.env`.
- `RUNPOD_API_KEY` in `.env` is for **agent reference** — the CLI reads from its own config file after `runpodctl config --apiKey` is run.
- If the user has multiple RunPod accounts, they must switch API keys via `runpodctl config --apiKey`.

## Error Handling

| Error | Action |
|-------|--------|
| `brew: command not found` | Use the install script method instead |
| `runpodctl: command not found` after install | Check PATH; restart shell or run `hash -r` |
| `gpu list` returns auth error | Re-run `runpodctl config --apiKey`; verify the key at runpod.io |
| `RUNPOD_API_KEY` not set | Guide user to create a key at runpod.io/console/user/settings |

## Verification Before Completion

- [ ] `runpodctl version` returns a version string
- [ ] `runpodctl gpu list` returns data without auth errors
- [ ] User informed of config file location (`~/.runpod/config.toml`)
