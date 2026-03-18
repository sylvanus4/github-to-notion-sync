# AutoResearchClaw — Configuration Guide

Config file location: `~/thaki/AutoResearchClaw/config.arc.yaml`

## Minimal Config (OpenAI)

```yaml
project:
  name: "my-research"
  mode: "full-auto"            # docs-first | semi-auto | full-auto

research:
  topic: "Your research topic here"
  domains: ["machine-learning"]

runtime:
  timezone: "Asia/Seoul"
  retry_limit: 2

notifications:
  channel: "console"

knowledge_base:
  backend: "markdown"
  root: "docs/kb"

llm:
  provider: "openai-compatible"
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"  # pragma: allowlist secret
  primary_model: "gpt-4o"
  fallback_models: ["gpt-4o-mini"]

experiment:
  mode: "sandbox"
```

## Config for Anthropic Claude

```yaml
llm:
  provider: "openai-compatible"
  base_url: "https://api.anthropic.com/v1"
  api_key_env: "ANTHROPIC_API_KEY"  # pragma: allowlist secret
  primary_model: "claude-sonnet-4-20250514"
  fallback_models: ["claude-haiku-4-20250514"]
```

## Config for ACP (Agent Client Protocol)

Uses any ACP-compatible coding agent as the LLM backend:

```yaml
llm:
  provider: "acp"
  acp:
    agent: "claude"
    cwd: "."
    session_name: "researchclaw"
    timeout_sec: 600
```

## Config Section Reference

### `project`

| Field | Type | Default | Description |
|---|---|---|---|
| `name` | string | required | Project identifier |
| `mode` | string | `"docs-first"` | `docs-first`, `semi-auto`, or `full-auto` |

### `research`

| Field | Type | Default | Description |
|---|---|---|---|
| `topic` | string | required | Research topic (can be overridden with `--topic`) |
| `domains` | list | `[]` | Research domain tags |
| `daily_paper_count` | int | `0` | Papers to process per day |
| `quality_threshold` | float | `0.0` | Minimum quality score |

### `llm`

| Field | Type | Default | Description |
|---|---|---|---|
| `provider` | string | `"openai-compatible"` | `openai-compatible` or `acp` |
| `base_url` | string | required* | API endpoint (* not needed for ACP) |
| `api_key_env` | string | required* | Env var holding API key |
| `api_key` | string | `""` | Direct API key (not recommended) |
| `primary_model` | string | `""` | Primary model name |
| `fallback_models` | list | `[]` | Fallback model names |
| `s2_api_key` | string | `""` | Semantic Scholar API key (optional, for higher rate limits) |

### `experiment`

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` | string | `"simulated"` | `simulated`, `sandbox`, `docker`, `ssh_remote` |
| `time_budget_sec` | int | `300` | Max time per experiment run |
| `max_iterations` | int | `10` | Max iterative refinement rounds |
| `metric_key` | string | `"primary_metric"` | Key metric name |
| `metric_direction` | string | `"minimize"` | `minimize` or `maximize` |

### `experiment.sandbox`

| Field | Type | Default | Description |
|---|---|---|---|
| `python_path` | string | `".venv/bin/python3"` | Python interpreter path |
| `gpu_required` | bool | `false` | Require GPU for execution |
| `allowed_imports` | list | `[math, random, ...]` | Whitelisted Python imports |
| `max_memory_mb` | int | `4096` | Memory limit in MB |

### `experiment.docker`

| Field | Type | Default | Description |
|---|---|---|---|
| `image` | string | `"researchclaw/experiment:latest"` | Docker image |
| `gpu_enabled` | bool | `true` | Enable GPU passthrough |
| `memory_limit_mb` | int | `8192` | Container memory limit |
| `network_policy` | string | `"setup_only"` | `none`, `setup_only`, `pip_only`, `full` |
| `auto_install_deps` | bool | `true` | Auto-install pip dependencies |

### `experiment.code_agent`

| Field | Type | Default | Description |
|---|---|---|---|
| `enabled` | bool | `true` | Enable multi-phase code generation |
| `architecture_planning` | bool | `true` | Phase 1: blueprint planning |
| `sequential_generation` | bool | `true` | Phase 2: sequential file gen |
| `hard_validation` | bool | `true` | Phase 2.5: AST validation gates |
| `exec_fix_max_iterations` | int | `3` | Phase 3: run→fix loop limit |
| `tree_search_enabled` | bool | `false` | Phase 4: solution tree search (expensive) |
| `review_max_rounds` | int | `2` | Phase 5: multi-agent review rounds |

### `export`

| Field | Type | Default | Description |
|---|---|---|---|
| `target_conference` | string | `"neurips_2025"` | LaTeX template |
| `authors` | string | `"Anonymous"` | Author line |
| `bib_file` | string | `"references"` | BibTeX filename (without .bib) |

### `security`

| Field | Type | Default | Description |
|---|---|---|---|
| `hitl_required_stages` | list | `[5, 9, 20]` | Stages requiring human approval |
| `allow_publish_without_approval` | bool | `false` | Skip final approval |
| `redact_sensitive_logs` | bool | `true` | Redact secrets from logs |

### `metaclaw_bridge`

| Field | Type | Default | Description |
|---|---|---|---|
| `enabled` | bool | `false` | Enable MetaClaw integration |
| `proxy_url` | string | `"http://localhost:30000"` | MetaClaw proxy URL |
| `skills_dir` | string | `"~/.metaclaw/skills"` | MetaClaw skills directory |
| `prm.enabled` | bool | `false` | PRM quality gate (LLM-as-judge) |
| `lesson_to_skill.enabled` | bool | `true` | Auto-convert lessons to skills |
