---
name: sandbox-provider
description: >-
  Manage sandbox execution environments for agent workloads — provision
  E2B/Modal/Docker sessions, execute code in isolation, and integrate with the
  ATG sandbox endpoint.
---

# Sandbox Provider

Provision and manage isolated sandbox execution environments for agent workloads.
Implements the harness/compute separation pattern: orchestration runs locally, code
execution happens in remote sandboxes with filesystem, terminal, and optional browser.

## Role & Scope

- Create sandbox sessions via pluggable providers (E2B, Modal, Docker, etc.)
- Execute commands, read/write files, upload/download artifacts in sandboxes
- Integrate with the Agent Tool Gateway (ATG) `POST /api/v1/sandbox/execute` endpoint
- Health-check providers and list available templates

## Architecture

```
scripts/sandbox/
├── __init__.py              # Public API re-exports, auto-registers adapters
├── provider_interface.py    # Abstract SandboxProvider + SandboxSession
├── e2b_adapter.py           # E2B Code Interpreter adapter
├── modal_adapter.py         # Modal serverless sandbox adapter (GPU, snapshots)
└── benchmark.py             # Provider comparison benchmark (cold-start, I/O, exec)
```

### Key Abstractions

| Type | Purpose |
|------|---------|
| `SandboxProvider` | Factory that creates sessions for a specific backend |
| `SandboxSession` | Live session with exec, file I/O, and lifecycle methods |
| `SessionConfig` | Provisioning parameters (TTL, CPU, memory, env vars) |
| `ExecResult` | Command output (exit code, stdout, stderr, duration) |
| `SandboxCapabilities` | Provider feature matrix (filesystem, terminal, browser, GPU) |

### ATG Integration

The ATG's `POST /api/v1/sandbox/execute` accepts `ExecutionRequest` with DAG-ordered
`Step` objects. This skill's providers can serve as the backend for that endpoint, or
be used standalone from skills/harnesses.

## Workflow

### 1. Select a Provider

```python
from scripts.sandbox import get_provider, available_providers

print(available_providers())   # ['e2b', 'modal']
provider = get_provider("e2b")
```

### 2. Create a Session

```python
from scripts.sandbox import SessionConfig

config = SessionConfig(
    tenant_id="agent-123",
    ttl_seconds=300,
    env_vars={"EXAMPLE_ENV_VAR": "<set-in-your-env>"},
)

async with await provider.create_session(config) as session:
    result = await session.exec_command("python -c 'print(1+1)'")
    print(result.stdout)  # "2\n"
```

### 3. File Operations

```python
await session.write_file("/tmp/data.csv", b"a,b\n1,2\n")
content = await session.read_file("/tmp/data.csv")
await session.upload("local_script.py", "/home/user/run.py")
await session.download("/home/user/output.json", "result.json")
entries = await session.list_dir("/home/user")
```

### 4. Health Check & Templates

```python
healthy = await provider.health_check()
templates = await provider.list_templates()
```

### 5. Modal with GPU

```python
provider = get_provider("modal", gpu="T4", region="us-east")

config = SessionConfig(
    tenant_id="gpu-job-1",
    ttl_seconds=600,
    cpu_millicores=4000,
    memory_mb=16384,
    env_vars={"HF_TOKEN": "hf_..."},
)

session = await provider.create_session(config)
result = await session.exec_command("python -c 'import torch; print(torch.cuda.is_available())'")
```

### 6. Benchmark Providers

```bash
python -m scripts.sandbox.benchmark                     # all available
python -m scripts.sandbox.benchmark --provider e2b      # E2B only
python -m scripts.sandbox.benchmark --provider modal    # Modal only
python -m scripts.sandbox.benchmark --rounds 5          # more rounds
python -m scripts.sandbox.benchmark --output bench.json # JSON export
```

Benchmark measures per round: cold-start latency, `echo hello` exec, 1KB/1MB file
write and read, and session teardown. Reports p50 and p95 for each metric.

## Provider Matrix

| Provider | Status | Cold Start | Filesystem | Terminal | Browser | GPU | Snapshots | Persistent Volumes |
|----------|--------|-----------|-----------|---------|---------|-----|-----------|-------------------|
| E2B | Implemented | ~300ms | Yes | Yes | No | No | Yes | No |
| Modal | Implemented | ~50ms hot | Yes | Yes | No | Yes | Yes | Yes |
| Docker | Planned | ~1s | Yes | Yes | No | GPU passthrough | No | Bind mounts |
| Daytona | Planned | varies | Yes | Yes | Yes | No | Yes | Yes |

## Adding a New Provider

1. Create `scripts/sandbox/{name}_adapter.py`
2. Subclass `SandboxProvider` and `SandboxSession`
3. Call `register_provider("{name}", YourProvider)` at module level
4. Import the adapter in `scripts/sandbox/__init__.py`

## Constraints

- Sessions are ephemeral by default — do NOT assume persistent state across sessions
- Always set TTL; never leave sessions running indefinitely
- Treat sandbox environments as untrusted — do not inject production secrets
- Budget enforcement is handled by the ATG layer, not individual providers
- File I/O is async; use `await` consistently

## Related

| Skill / Doc | Relationship |
|-------------|-------------|
| `agent-daemon-protocol` | Daemon ↔ server protocol for agent task claiming |
| `agent-task-lifecycle` | Task queue, progress, token accounting |
| `ce-hosted-agents` | Hosted agent infrastructure patterns |
| `harness` | Harness design with compute backend field |
| ATG `sandbox/types.go` | Go types for ExecutionRequest/Step/Budget |
| PRD `agent-sandbox-platform` | Full product requirements for sandbox platform |

## Do NOT Use For

- Running the daily stock pipeline (use `today`)
- Managing RunPod GPU pods (use `runpod-pods`)
- General Docker container management without agent sandbox context
- CI/CD pipeline execution (use `ci-quality-gate`)
- Local dev environment setup (use `local-dev-runner`)
