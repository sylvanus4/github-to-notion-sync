# Meta-Harness Optimizer

Outer-loop optimization skill that iteratively improves a target skill (or skill chain) by treating it as a "harness" — the stateful code wrapping a fixed LLM. Adapts Algorithm 1 from the Meta-Harness paper (arXiv:2603.28052) using filesystem-based uncompressed execution traces, an agentic coding proposer, and Pareto multi-objective reporting.

## When to Use

Use when the user asks to "meta-harness optimize", "outer-loop optimize skill", "meta-harness", "harness optimization", "code-level skill optimization", "trace-aware optimization", "Pareto optimize skill", "메타 하네스", "하네스 최적화", "코드 레벨 스킬 최적화", "외부 루프 최적화", "파레토 최적화", or wants to optimize a skill beyond prompt-level text changes by modifying retrieval logic, state management, tool orchestration, or evaluation pipelines.

## When NOT to Use

- For prompt-text-only optimization without code changes — use `skill-autoimprove`
- For creating new skills from scratch — use `create-skill` or `harness`
- For transcript-based skill extraction — use `autoskill-evolve`
- For static quality audits without optimization — use `skill-optimizer`
- For individual skill benchmarking — use `skill-upgrade-validator`

## Prerequisites

- Target skill must have a measurable evaluation function (binary or numeric scoring)
- Python 3.11+ with `scripts/meta_harness_trace.py` available
- Sufficient disk space for trace archive (`_workspace/meta-harness/`)

## Modes

| Mode | Description | Side Effects |
|------|-------------|--------------|
| `optimize` | Full outer loop: seed → evaluate → propose → validate → iterate (default) | Writes to `_workspace/meta-harness/{run-id}/` |
| `dry-run` | Propose candidates only, skip evaluation | Writes proposals to archive, no eval execution |
| `analyze` | Read existing archive and generate Pareto report | Read-only |
| `ablate` | Compare feedback strategies: full traces vs scores+summary vs scores-only (Table 3 replication) | Writes ablation results |

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--target` | (required) | Path to the skill SKILL.md or script to optimize |
| `--eval-fn` | (required) | Evaluation function or script (returns numeric scores) |
| `--iterations` | 20 | Number of outer-loop iterations |
| `--candidates-per-iter` | 2 | New candidates generated per iteration (k) |
| `--objectives` | `accuracy,cost` | Comma-separated optimization objectives |
| `--mode` | `optimize` | One of: optimize, dry-run, analyze, ablate |
| `--run-id` | auto-generated | Identifier for this optimization run |
| `--search-split` | 0.5 | Fraction of eval data used for search (vs held-out validation) |
| `--seed-population` | auto | Initial candidates; defaults to the current target skill |

## Algorithm (adapted from Algorithm 1)

```
PROCEDURE MetaHarnessOptimize(target, eval_fn, N, k):
  run_id ← generate_uuid()
  archive ← TraceArchive("_workspace/meta-harness/{run_id}/")

  -- Phase 1: Initialize
  H ← {target}                          -- seed population (current skill)
  D_search, D_val ← split(eval_data, search_split)

  -- Phase 2: Evaluate seed
  FOR h IN H:
    scores, traces ← evaluate(h, D_search)
    archive.log_candidate(h.id, h.source, scores, traces)

  -- Phase 3: Outer loop (N iterations)
  FOR i IN 1..N:
    -- Proposer selectively reads archive
    context ← archive.query(
      pattern="scores.json AND traces/*.log",
      strategy="selective_grep"           -- not full dump
    )

    -- Generate k new candidates via code-level mutations
    candidates ← proposer.generate(
      context=context,
      mutation_types=["retrieval_logic", "state_management",
                      "prompt_construction", "tool_orchestration",
                      "evaluation_pipeline"],
      k=k
    )

    -- Validate and evaluate
    FOR c IN candidates:
      IF validate_interface(c):
        scores, traces ← evaluate(c, D_search)
        archive.log_candidate(c.id, c.source, scores, traces)

    -- Update Pareto frontier
    archive.update_pareto(objectives)

    -- Checkpoint: emit progress
    report_iteration(i, archive.get_pareto_frontier())

  -- Phase 4: Final validation on held-out set
  pareto_set ← archive.get_pareto_frontier()
  FOR h IN pareto_set:
    val_scores ← evaluate(h, D_val)
    archive.update_validation(h.id, val_scores)

  -- Phase 5: Report
  archive.generate_report()              -- markdown + Pareto chart data

  RETURN pareto_set                      -- human selects from frontier
```

## Filesystem Archive Structure

Each optimization run creates a self-contained directory:

```
_workspace/meta-harness/{run-id}/
├── manifest.json              # run metadata, config, timestamps
├── candidates/
│   ├── seed-001/
│   │   ├── SKILL.md           # or harness.py — the candidate source
│   │   ├── scores.json        # {"accuracy": 0.82, "cost_tokens": 1450}
│   │   ├── traces/            # full execution logs per eval case
│   │   │   ├── case-001.log
│   │   │   └── case-002.log
│   │   └── proposer-reasoning.md  # why this candidate was generated
│   ├── iter01-cand01/
│   │   ├── SKILL.md
│   │   ├── scores.json
│   │   ├── traces/
│   │   ├── proposer-reasoning.md
│   │   └── diff-from-parent.patch
│   └── ...
├── pareto/
│   ├── frontier.json          # current Pareto-dominant set
│   └── frontier-history.jsonl # frontier evolution per iteration
├── ablation/                  # only in ablate mode
│   ├── full-traces.json
│   ├── scores-summary.json
│   └── scores-only.json
└── report.md                  # final summary with tables and chart data
```

## Key Differentiators from `skill-autoimprove`

| Dimension | `skill-autoimprove` | `meta-harness-optimizer` |
|-----------|-------------------|------------------------|
| Mutation target | Prompt text in SKILL.md | Code: retrieval, state, tools, orchestration |
| Feedback | Binary pass/fail scores | Full execution traces (tool calls, model outputs, state) |
| Proposer context | Current SKILL.md + score history | Selective grep across uncompressed trace archive |
| Optimization surface | ~1KB prompt text | ~10-100KB code + config + pipeline logic |
| Multi-objective | Single metric | Pareto frontier (accuracy vs cost, extensible) |
| Paper reference | Karpathy autoresearch | Meta-Harness Algorithm 1, Table 3 ablation |

## Workflow

### Step 1: Identify Target

Identify the skill or script to optimize. Must have a callable evaluation function.

### Step 2: Prepare Evaluation Data

Split evaluation data into search and validation sets. The optimizer only sees the search split during iteration; the validation split is used for final Pareto candidate assessment.

### Step 3: Run Optimization

```bash
# Full optimization loop
/meta-harness --target .cursor/skills/trading/daily-stock-check/SKILL.md \
              --eval-fn scripts/eval_stock_check.py \
              --iterations 20 --candidates-per-iter 2

# Dry run (proposals only)
/meta-harness --target .cursor/skills/review/deep-review/SKILL.md \
              --eval-fn scripts/eval_review_quality.py \
              --mode dry-run

# Analyze existing archive
/meta-harness --run-id abc123 --mode analyze

# Ablation study
/meta-harness --target .cursor/skills/automation/skill-autoimprove/SKILL.md \
              --eval-fn scripts/eval_autoimprove.py \
              --mode ablate
```

### Step 4: Review Pareto Frontier

The optimizer produces a `report.md` with:
- Iteration-by-iteration progress table
- Pareto frontier visualization data (accuracy vs cost)
- Top-3 candidates with diffs from seed
- Ablation results (if run in ablate mode)

### Step 5: Human Approval Gate

No candidate replaces a production skill without explicit user approval. The skill presents the Pareto frontier and waits for the user to select which candidate (if any) to promote.

## Composability

- **Inner loop**: `skill-autoimprove --trace-aware` handles prompt-layer mutations within a Meta-Harness iteration
- **Population source**: `autoskill-evolve` candidates can seed the Meta-Harness population
- **Initial design**: `harness` skill generates the initial orchestrator that Meta-Harness then optimizes
- **Runtime traces**: `backend/app/services/orchestration/trace.py` emits events consumed by TraceArchive

## Anti-Patterns

- Do NOT run on execution skills with real side effects (Slack, DB writes, API calls) without sandboxing
- Do NOT use for skills that lack measurable evaluation criteria
- Do NOT skip the validation split — overfitting to search data defeats the purpose
- Do NOT allow the proposer to see the validation set during optimization

## Error Handling

- If evaluation fails for a candidate: log the error in traces, mark candidate as `failed`, continue with remaining candidates
- If all candidates in an iteration fail: emit warning, reduce mutation aggressiveness, retry once
- If the proposer generates invalid code: skip validation, log syntax error, do not count toward iteration budget
- If disk space is insufficient: emit error with `_workspace/` size, suggest `--iterations` reduction

## Examples

### Example 1: Optimize a trading analysis skill

```
User: meta-harness optimize daily-stock-check
Agent:
1. Reading target skill at .cursor/skills/trading/daily-stock-check/SKILL.md
2. Preparing evaluation data from outputs/screener-*.json (50 cases)
3. Split: 25 search / 25 validation
4. Seed candidate: current SKILL.md (accuracy: 0.72, cost: 3200 tokens)
5. Running 20 iterations × 2 candidates...
   Iteration 1: best accuracy 0.74 (retrieval logic change)
   Iteration 5: Pareto frontier expanded (0.78 accuracy @ 2800 tokens)
   ...
   Iteration 20: final frontier has 4 candidates
6. Report saved to _workspace/meta-harness/run-abc123/report.md
7. Top candidate: +8.3% accuracy, -12% token cost
   Approve replacement? [y/n]
```

### Example 2: Ablation study comparing feedback strategies

```
User: meta-harness ablate skill-autoimprove
Agent:
1. Running 3 parallel optimization paths:
   - Full traces: proposer sees complete execution logs
   - Scores + summary: proposer sees scores and 1-paragraph summaries
   - Scores only: proposer sees only numeric scores
2. Each path: 10 iterations × 2 candidates
3. Results:
   | Strategy        | Best Accuracy | Median Improvement |
   |-----------------|---------------|--------------------|
   | Full traces     | 0.91          | +12.4%             |
   | Scores+summary  | 0.85          | +7.1%              |
   | Scores only     | 0.79          | +3.2%              |
4. Conclusion: Full traces provide ~4x better improvement (matches Table 3)
```

### Example 3: Analyze existing optimization run

```
User: meta-harness analyze --run-id run-abc123
Agent:
1. Reading archive at _workspace/meta-harness/run-abc123/
2. 40 candidates evaluated across 20 iterations
3. Pareto frontier: 4 non-dominated solutions
4. Best accuracy: 0.91 (candidate iter15-cand02)
5. Lowest cost: 1200 tokens (candidate iter08-cand01)
6. Best balanced: 0.88 accuracy @ 1800 tokens (candidate iter12-cand01)
7. Full report: _workspace/meta-harness/run-abc123/report.md
```

## Output Contract

Every optimization run produces:
1. `manifest.json` — run config, timing, seed info
2. `candidates/` — full artifact tree per candidate
3. `pareto/frontier.json` — current Pareto-dominant set with scores
4. `report.md` — human-readable summary with iteration table, diffs, and chart data

## References

- Meta-Harness paper: arXiv:2603.28052, Section 3 (Algorithm 1), Figure 2, Table 3
- Project execution plan: `outputs/papers/2603.28052-execution-2026-04-04.md`
- PM strategy analysis: `outputs/papers/2603.28052-pm-strategy-2026-04-04.md`
