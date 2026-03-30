# AutoResearchClaw — Experiment Modes

The `experiment.mode` setting determines how generated experiment code is executed.

## Mode Comparison

| Mode | Code Execution | Real Data | GPU Support | Isolation | Use Case |
|---|---|---|---|---|---|
| `simulated` | None | No | N/A | N/A | Framework testing, dry runs |
| `sandbox` | Local subprocess | Yes | Host GPU | Process-level | Default for most research |
| `docker` | Container | Yes | GPU passthrough | Container-level | Reproducible, isolated |
| `ssh_remote` | Remote server | Yes | Remote GPU | Network-level | Large GPU workloads |

## Simulated Mode

Uses the LLM to generate synthetic experiment results without executing code.

```yaml
experiment:
  mode: "simulated"
```

**When to use**: Pipeline testing, config validation, writing-focused research.

**Warning**: Papers generated with simulated data should NOT be submitted to conferences.
The `pipeline_summary.json` will flag `experiment.mode: simulated`.

## Sandbox Mode (Default)

Executes generated Python code in a local subprocess with import whitelisting
and memory limits.

```yaml
experiment:
  mode: "sandbox"
  sandbox:
    python_path: ".venv/bin/python3"   # Must have numpy, torch, sklearn installed
    gpu_required: false
    allowed_imports:
      - math
      - random
      - json
      - csv
      - numpy
      - torch
      - sklearn
    max_memory_mb: 4096
```

**Setup**: Install experiment dependencies in the AutoResearchClaw venv:

```bash
cd ~/thaki/AutoResearchClaw
source .venv/bin/activate
pip install numpy torch scikit-learn
```

**Self-healing**: If a sandbox run fails, the CodeAgent enters an exec-fix loop:
1. Parse error traceback
2. LLM generates fix
3. Re-execute (up to `code_agent.exec_fix_max_iterations` times)

## Docker Mode

Executes experiments inside a Docker container with GPU passthrough,
network isolation, and automatic dependency installation.

```yaml
experiment:
  mode: "docker"
  docker:
    image: "researchclaw/experiment:latest"
    gpu_enabled: true
    gpu_device_ids: []              # Empty = all GPUs; [0, 1] = specific GPUs
    memory_limit_mb: 8192
    network_policy: "setup_only"    # none | setup_only | pip_only | full
    pip_pre_install:                # Pre-install packages before experiment
      - torchdiffeq
      - einops
    auto_install_deps: true         # Auto-detect and install missing imports
    shm_size_mb: 2048               # Shared memory for PyTorch DataLoader
    container_python: "/usr/bin/python3"
    keep_containers: false          # Remove containers after run
```

**Build the Docker image first**:

```bash
cd ~/thaki/AutoResearchClaw
docker build -t researchclaw/experiment:latest researchclaw/docker/
```

**Network policies**:
- `none` — No network access inside container
- `setup_only` — Network during setup (pip install), then disconnected
- `pip_only` — Only pip/conda traffic allowed
- `full` — Full network access (least secure)

## SSH Remote Mode

Executes experiments on a remote GPU server via SSH.

```yaml
experiment:
  mode: "ssh_remote"
  ssh_remote:
    host: "gpu-server.example.com"
    gpu_ids: [0, 1]
    remote_workdir: "/tmp/researchclaw_experiments"
```

**Prerequisites**:
- SSH key-based auth configured for the target host
- Python 3.11+ and experiment dependencies installed on the remote
- Sufficient GPU memory for the experiment

## Multi-Phase Code Generation Agent

The CodeAgent (Stage 10) generates experiment code using a sophisticated pipeline:

1. **Blueprint Planning** — Deep implementation blueprint with architecture decisions
2. **Sequential Generation** — One-by-one file generation following the blueprint
3. **Hard Validation** — AST-based syntax checking with auto-repair (max 2 repairs)
4. **Exec-Fix Loop** — Execute → parse error → LLM fix → re-execute (max 3 iterations)
5. **Solution Tree Search** — Generate multiple candidates, evaluate each (disabled by default)
6. **Multi-Agent Review** — Review dialog between generator and critic agents

Configure via `experiment.code_agent`:

```yaml
experiment:
  code_agent:
    enabled: true
    architecture_planning: true
    sequential_generation: true
    hard_validation: true
    exec_fix_max_iterations: 3
    tree_search_enabled: false      # Enable for higher quality, higher cost
    review_max_rounds: 2
```

## Benchmark Agent

The BenchmarkAgent (integrated into experiment design) discovers and selects
appropriate benchmarks and baselines:

```yaml
experiment:
  benchmark_agent:
    enabled: true
    enable_hf_search: true          # Search Hugging Face for datasets
    max_hf_results: 10
    tier_limit: 2                   # Benchmark difficulty tier limit
    min_benchmarks: 1
    min_baselines: 2
    prefer_cached: true             # Prefer locally cached datasets
```

## Figure Agent

Generates publication-quality figures for the paper:

```yaml
experiment:
  figure_agent:
    enabled: true
    min_figures: 3
    max_figures: 8
    max_iterations: 3               # CodeGen→Renderer→Critic retry loops
    render_timeout_sec: 30
    strict_mode: false
    dpi: 300
```
