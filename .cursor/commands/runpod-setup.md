## RunPod Setup

Install, authenticate, and verify the RunPod CLI (`runpodctl`) for managing GPU cloud resources.

### Usage

```
/runpod-setup                    # Full setup: install + auth + verify
/runpod-setup --check            # Check installation status only
/runpod-setup --fix              # Re-authenticate with current RUNPOD_API_KEY
```

### Skill Reference

Read and follow the `runpod-setup` skill (`.cursor/skills/infra/runpod-setup/SKILL.md`) for the full workflow.

### Workflow

1. Check if `runpodctl` is already installed (`command -v runpodctl`)
2. Install via Homebrew (macOS) or install script (Linux)
3. Configure API key from `RUNPOD_API_KEY` environment variable
4. Verify connectivity with `runpodctl gpu list`
5. Report status (READY / NOT READY)

### Prerequisites

- `RUNPOD_API_KEY` in `.env` -- obtain from [runpod.io/console/user/settings](https://www.runpod.io/console/user/settings)

### Examples

Full setup:
```
/runpod-setup
```

Check if already set up:
```
/runpod-setup --check
```

Re-authenticate after key rotation:
```
/runpod-setup --fix
```
