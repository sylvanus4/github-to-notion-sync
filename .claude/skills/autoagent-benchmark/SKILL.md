---
name: autoagent-benchmark
description: >-
  Run Harbor-compatible benchmarks against an agent harness in Docker
  isolation. Builds a Docker image from the harness, executes task suites in
  sandboxed containers, collects ATIF trajectories, and produces aggregated
  score reports.
---

# AutoAgent Benchmark

Run Harbor-compatible benchmarks against an agent harness in Docker isolation. Builds a Docker image from the harness, executes task suites in sandboxed containers, collects ATIF trajectories, and produces aggregated score reports.

## When to Use

Use when the user asks to "run benchmark", "autoagent benchmark", "Harbor benchmark", "Docker benchmark", "agent benchmark", "run task suite", "autoagent-benchmark", "벤치마크 실행", "에이전트 벤치마크", "하버 벤치마크", "도커 벤치마크", or wants to evaluate an agent harness against a structured task suite in an isolated environment.

## When NOT to Use

- For the full optimization loop with mutations — use `autoagent-loop`
- For failure diagnosis from existing trajectories — use `autoagent-diagnostics`
- For Playwright browser-based testing — use `e2e-testing`
- For LLM prompt evaluation and judge prompts — use `evals-skills`
- For agent session evaluation metrics — use `ecc-eval-harness`

## Prerequisites

- Docker installed and running (`docker ps` must succeed)
- Python 3.11+
- `scripts/autoagent/` package (harbor_adapter, atif_logger)
- Task suite in Harbor JSON/YAML format
- Agent harness file (agent.py or equivalent)

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--harness` | (required) | Path to agent harness file |
| `--tasks` | (required) | Path to task suite directory or file |
| `--image-name` | `autoagent:latest` | Docker image name |
| `--output-dir` | `outputs/autoagent-bench` | Directory for results and trajectories |
| `--timeout` | 300 | Per-task timeout in seconds |
| `--run-id` | auto-generated | Identifier for this benchmark run |
| `--dockerfile` | auto-generated | Custom Dockerfile path (optional) |

## Pipeline

### Phase 1: Prepare

1. Validate harness file exists and contains the `FIXED ADAPTER BOUNDARY` marker
2. Load task suite via `TaskLoader.load_directory()` or `TaskLoader.load_file()`
3. Generate Dockerfile from `HarnessTemplate.generate_dockerfile()` if not provided

### Phase 2: Build

1. Build Docker image using `DockerBenchmarkRunner.build_image()`
2. Verify image was created: `docker images | grep {image-name}`
3. If build fails: report error with Docker build logs

### Phase 3: Execute

1. Run each task in the suite via `DockerBenchmarkRunner.run_task()`
2. Each task runs in an isolated container with:
   - Task instruction injected via environment variable
   - Stdout/stderr captured
   - Timeout enforcement
3. Log each execution as an ATIF trajectory via `ATIFLogger`
4. Collect `TaskResult` objects with pass/fail status and output

### Phase 4: Aggregate

1. Compute aggregate scores via `ScoreAggregator.aggregate()`:
   - Pass rate (passed / total)
   - Per-category breakdown
   - Average duration
2. Save raw results to `{output-dir}/{run-id}/results.json`
3. Save ATIF trajectories to `outputs/autoagent-trajectories/`

### Phase 5: Report

1. Generate markdown report with:
   - Summary statistics (total, passed, failed, pass rate)
   - Per-category breakdown table
   - Failed task details with error messages
   - Duration statistics
2. Save report to `{output-dir}/{run-id}/report.md`

## Output Artifacts

| Phase | Output File |
|-------|-------------|
| 2 | Docker image `{image-name}` |
| 3 | `outputs/autoagent-trajectories/{trajectory_id}.json` (per task) |
| 4 | `{output-dir}/{run-id}/results.json` |
| 5 | `{output-dir}/{run-id}/report.md` |

## Task Suite Format (Harbor)

Tasks are defined as JSON or YAML files:

```json
{
    "task_id": "coding-001",
    "instruction": "Write a Python function that sorts a list of integers using merge sort.",
    "expected_output": "def merge_sort(arr):",
    "category": "coding",
    "timeout_seconds": 120,
    "verification": {
        "type": "contains",
        "value": "def merge_sort"
    }
}
```

A task suite is a directory containing multiple task files, or a single file with an array of tasks.

## Integration

- **autoagent-loop** invokes this skill for benchmark execution between mutations
- **autoagent-diagnostics** consumes the ATIF trajectories produced by this skill
- **meta-harness-optimizer** can import ATIF trajectories via `ATIFLogger.to_trace_archive_format()`

## Error Handling

- Docker not running: fail fast with instructions to start Docker
- Image build failure: report full build log, suggest checking harness syntax
- Task timeout: record as `timeout` in ATIF, score as 0, continue remaining tasks
- Container crash: record as `error` in ATIF, capture stderr, continue remaining tasks

## Gotchas

- Docker must have sufficient resources allocated (at least 2GB RAM for typical agent tasks)
- Task timeouts should be generous for LLM-based agents (300s default; increase for complex tasks)
- The `expected_output` field supports partial matching — exact match is not required by default
- Building the Docker image can take 30-60s on first run; subsequent runs use cache

## Examples

### Run a benchmark suite

```
User: autoagent benchmark --harness scripts/autoagent/examples/agent.py --tasks data/bench/coding-tasks/
```

### Run with custom image name and timeout

```
User: autoagent benchmark --harness agent.py --tasks data/bench/ --image-name myagent:v2 --timeout 600
```

### Compare results against a baseline

```python
from scripts.autoagent.harbor_adapter import ScoreAggregator
baseline = {"pass_rate": 0.72, "total_tasks": 25, "passed": 18}
current = {"pass_rate": 0.80, "total_tasks": 25, "passed": 20}
comparison = ScoreAggregator.compare(baseline, current)
```
