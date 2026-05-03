---
name: autoagent-diagnostics
description: >-
  Analyze agent benchmark failures from ATIF trajectories to identify
  systematic failure patterns, classify them by root cause, rank by impact,
  and suggest targeted harness mutations. Transforms raw trajectory data into
  actionable improvement priorities for the autoagent optimization loop.
---

# AutoAgent Diagnostics

Analyze agent benchmark failures from ATIF trajectories to identify systematic failure patterns, classify them by root cause, rank by impact, and suggest targeted harness mutations. Transforms raw trajectory data into actionable improvement priorities for the autoagent optimization loop.

## When to Use

Use when the user asks to "diagnose failures", "analyze trajectories", "failure patterns", "autoagent diagnostics", "benchmark failures", "trajectory analysis", "autoagent-diagnostics", "실패 패턴 분석", "트라젝토리 진단", "벤치마크 실패 분석", "에이전트 실패 분류", or wants to understand why an agent harness is failing on specific tasks and get prioritized fix suggestions.

## When NOT to Use

- For the full optimization loop — use `autoagent-loop`
- For running benchmarks without diagnosis — use `autoagent-benchmark`
- For debugging a specific code bug — use `diagnose`
- For reviewing code quality — use `deep-review` or `simplify`
- For LLM prompt evaluation — use `evals-skills`

## Prerequisites

- Python 3.11+
- `scripts/autoagent/` package (atif_logger, failure_analyzer)
- ATIF trajectory files from a previous `autoagent-benchmark` run

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--trajectories` | (required) | Path to trajectory directory or single file |
| `--format` | `report` | Output format: report, json, fixes-only |
| `--min-severity` | `low` | Minimum severity to include: critical, high, medium, low |
| `--output` | stdout | Output file path (optional) |

## Pipeline

### Phase 1: Load

1. Load ATIF trajectories from `--trajectories` path
2. Filter to failed trajectories (outcome in: failure, error, timeout)
3. Report: total trajectories, failed count, failure rate

### Phase 2: Classify

1. Run `FailureAnalyzer.analyze()` on the failed trajectories
2. Each trajectory is classified into one or more failure categories:

| Category | Description | Example |
|----------|-------------|---------|
| `tool_misuse` | Tool called with wrong arguments or high error rate | Passing string where int expected |
| `infinite_loop` | Same tool called repeatedly without progress | 4+ consecutive identical calls |
| `hallucination` | Agent generated unverified or fabricated claims | "As an AI, I cannot verify..." |
| `wrong_tool` | Correct intent but wrong tool selected | Using `read_file` for web content |
| `missing_tool` | Agent tried to use a tool not in registry | "No such tool: browse_web" |
| `timeout` | Agent exceeded time limit | Stuck in exploration loop |
| `format_error` | Output doesn't match expected format | Missing required JSON fields |
| `reasoning_error` | Logic error in agent's problem-solving | Wrong arithmetic, faulty deduction |
| `instruction_ignored` | Agent didn't follow task instruction | Skipped required verification step |
| `unknown` | No clear pattern identified | Needs manual review |

### Phase 3: Rank

1. Sort patterns by severity × count (impact score)
2. Apply severity weights: critical=4, high=3, medium=2, low=1
3. Impact score = count × severity weight

### Phase 4: Report

Generate output in the requested format:

**`report` format** (default): Human-readable markdown with:
- Summary statistics
- Ranked pattern list with descriptions and counts
- Suggested fix per pattern
- Example trajectory excerpts

**`json` format**: Machine-readable JSON for programmatic consumption

**`fixes-only` format**: Prioritized list of fixes without full analysis

## Output Artifacts

| Phase | Output |
|-------|--------|
| 4 | Report file at `--output` or stdout |

## Integration

- **autoagent-loop** invokes this skill at Step 3a to guide mutation selection
- **autoagent-benchmark** produces the ATIF trajectories consumed by this skill
- **meta-harness-optimizer** can use the fix suggestions to guide code-level mutations

## Failure Category Details

### tool_misuse (severity: medium-high)

Detected when:
- Tool returns error responses containing "invalid" or "argument"
- More than 50% of tool calls fail with errors

Fix strategy: Add argument validation examples to tool descriptions in system prompt.

### infinite_loop (severity: critical)

Detected when:
- Same tool name appears 4+ times consecutively without other tools
- No progress indicators between repeated calls

Fix strategy: Add loop detection guard — "if tool X called >3 times consecutively, try alternative approach."

### hallucination (severity: medium)

Detected when:
- Agent output contains phrases like "As an AI", "I cannot verify", "fabricat"
- Agent asserts facts without tool verification

Fix strategy: Add "verify before asserting" instruction to system prompt.

### timeout (severity: high)

Detected when:
- Trajectory outcome is "timeout"

Fix strategy: Add explicit turn limits or early-exit conditions to system prompt.

### missing_tool (severity: high)

Detected when:
- Error messages contain "not found" or "no such tool"

Fix strategy: Enumerate available tools explicitly in system prompt.

## Error Handling

- If trajectory files are malformed: skip and log, continue with valid files
- If no failures found in trajectories: report "No failures detected" (not an error)
- If trajectory directory is empty: warn and exit

## Gotchas

- Hallucination detection is heuristic-based and may produce false positives — treat as advisory
- The `unknown` category is a catch-all; high counts here indicate the classifier needs refinement
- For best results, analyze trajectories from a full benchmark run (25+ tasks), not individual tasks
- Category counts may exceed the number of failed trajectories since one trajectory can match multiple categories

## Examples

### Analyze a benchmark run

```
User: autoagent diagnostics --trajectories outputs/autoagent-trajectories/
```

### Get prioritized fixes only

```
User: autoagent diagnostics --trajectories outputs/autoagent-trajectories/ --format fixes-only
```

### Filter to critical and high severity

```
User: autoagent diagnostics --trajectories outputs/autoagent-trajectories/ --min-severity high
```

### Programmatic usage

```python
from scripts.autoagent.failure_analyzer import FailureAnalyzer
from scripts.autoagent.atif_logger import ATIFLogger

trajectories = ATIFLogger.load_directory("outputs/autoagent-trajectories/")
analyzer = FailureAnalyzer()
patterns = analyzer.analyze(trajectories)
print(analyzer.report(patterns))
fixes = analyzer.prioritized_fixes(patterns)
```
