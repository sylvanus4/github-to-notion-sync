---
name: skill-autoimprove
description: >-
  Autonomously optimize an existing skill prompt: repeated runs, binary evals,
  one mutation at a time, keep only improvements (Karpathy-style
  autoresearch). Supports --trace-aware mode for full execution trace capture
  (tool calls, model outputs, state changes) compatible with
  meta-harness-optimizer's outer-loop code-level optimization via
  TraceArchive. Supports --harness-mode for optimizing single-file agent
  harnesses (agent.py) with Docker-isolated benchmark evaluation via
  autoagent-benchmark, operating on the editable section above the FIXED
  ADAPTER BOUNDARY. Supports --synthetic-eval mode for auto-generating
  evaluation cases from the skill text when no manual evals are provided.
  Enforces constraint gates (size limit, growth rate, trigger/boundary
  preservation) before accepting any mutation. Includes holdout evaluation
  after the mutation loop to detect overfitting. Use when the user asks
  "skill-autoimprove", "auto-improve this skill", "스킬 자동 개선", "프롬프트 자동 개선",
  "스킬 실험 루프", "스킬 최적화 루프", "run evals and fix skill", "self-improve skill",
  "harness prompt optimize", "하네스 프롬프트 최적화", or wants a loop that mutates
  SKILL.md or harness prompts until scores improve. Produces improved
  SKILL.md, results.tsv, changelog.md, and a live HTML dashboard. Do NOT use
  for static audits only (skill-optimizer audit), new skill creation
  (create-skill), single-doc polish without editing the skill
  (doc-quality-gate / workflow-patterns evaluator-optimizer), transcript
  mining (autoskill-evolve), population-based multi-variant evolution
  (hermes-skill-evolver), or paper pipelines (paper-review).
---

# Skill Auto-Improve

Most skills work about 70% of the time. The other 30% produces garbage. The fix is not to rewrite the skill from scratch — it is to let an agent run it dozens of times, score every output, and tighten the prompt until that 30% disappears.

This skill adapts Andrej Karpathy's autoresearch methodology (autonomous experimentation loops) to skill prompt optimization. Instead of optimizing ML training code, we optimize skill prompts through measured, one-mutation-at-a-time experiments.

---

## The Core Job

Take any existing skill, define what "good output" looks like as binary yes/no checks, then run an autonomous loop that:

1. Generates outputs from the skill using test inputs
2. Scores every output against the eval criteria
3. Mutates the skill prompt to fix the most common failure
4. Keeps mutations that improve the score, discards the rest
5. Repeats until the score ceiling is hit or the user stops it

**Output:** An improved SKILL.md + `results.tsv` log + `changelog.md` of every mutation attempted + a live HTML dashboard.

---

## Recommended Workflow (Integration with Existing Skills)

For best results in **ai-model-event-stock-analytics** (stock analytics / trading data platform):

1. **Pre-flight** — Run `skill-optimizer` in audit mode on the target skill to fix structural issues first (formatting, missing sections, dead triggers). Fix those before entering the mutation loop.
2. **Eval design** — Define 3-6 binary evals guided by [references/eval-guide.md](references/eval-guide.md) and **[references/eval-criteria.md](references/eval-criteria.md)** (financial terminology, signal expression, Tailwind+Radix vs TDS, POL-004 document quality, POL-001 forbidden terms). Optionally mirror patterns from `skill-optimizer` [references/eval-framework.md](../skill-optimizer/references/eval-framework.md) for runtime grading style.
3. **Autoresearch loop** — This skill's autonomous mutation cycle (the core).
4. **Post-verification** — Run `skill-optimizer` in benchmark mode with **fresh test inputs** (not the ones used during autoresearch) to verify improvements generalize and detect overfitting.

---

## Before Starting: Gather Context

**STOP. Do not run any experiments until all fields below are confirmed with the user. Ask for any missing fields before proceeding.**

1. **Target skill** — Which skill to optimize? (need the exact path to SKILL.md under `.cursor/skills/`)
2. **Test inputs** — 3-5 different prompts/scenarios to test the skill with. Variety matters — pick inputs that cover different use cases to avoid overfitting.
3. **Eval criteria** — 3-6 binary yes/no checks that define a good output. See [references/eval-guide.md](references/eval-guide.md) and [references/eval-criteria.md](references/eval-criteria.md). **Scope**: optimize **project-specific** skills for this repo unless the user explicitly names another skill; evals must include finance/domain accuracy and POL-001 forbidden-term checks when the skill produces user-facing or domain copy. **If no manual evals are available**, use `--synthetic-eval` to auto-generate eval cases from the skill text (see Synthetic Eval Mode below).
4. **Runs per experiment** — How many times to run the skill per mutation. Default: 5. More runs = more reliable scores, but slower. 5 is the sweet spot.
5. **Budget cap** — Optional. Max number of experiment cycles before stopping. Default: no cap (runs until stopped or ceiling hit).
6. **Constraint gates** — Enabled by default. Pass `--no-gates` to disable. See Constraint Gates section below for the full gate list.

---

## Step 1: Read the Skill

Before changing anything, read and understand the target skill completely.

1. Read the full SKILL.md file
2. Read any files in `references/` that the skill links to
3. Identify the skill's core job, process steps, and output format
4. Note any existing quality checks or anti-patterns already in the skill

Do NOT skip this. Understanding the skill is required before improving it.

---

## Step 2: Build the Eval Suite

Convert the user's eval criteria into a structured test. Every check must be binary — pass or fail, no scales.

**Project defaults (this repository):** When the user does not supply enough evals, merge their list with [references/eval-criteria.md](references/eval-criteria.md) so each run tests **financial terminology accuracy** (POL-001 / glossary), **signal/analytics expression** where relevant, **Tailwind+Radix** design guidance (no TDS/Figma as mandatory), **POL-004** document shape for spec/report skills, and **no new POL-001 forbidden terms** in the mutated skill body.

**Format each eval as:**

```
EVAL [number]: [Short name]
Question: [Yes/no question about the output]
Pass condition: [What "yes" looks like — be specific]
Fail condition: [What triggers a "no"]
```

**Rules for good evals:**
- Binary only. Yes or no. No "rate 1-7" scales. Scales compound variability and give unreliable results.
- Specific enough to be consistent. "Is the text readable?" is too vague. "Are all words spelled correctly with no truncated sentences?" is testable.
- Not so narrow that the skill games the eval. "Contains fewer than 200 words" will make the skill optimize for brevity at the expense of everything else.
- 3-6 evals is the sweet spot. More than that and the skill starts parroting eval criteria back instead of actually improving.
- **Session separation check:** If the target skill processes multiple items (batch loops, list iteration, multi-file scans), include an eval verifying it dispatches each item to an isolated subagent via Task tool. Example: `EVAL N: Session Isolation / Question: Does the skill instruct per-item subagent dispatch for batch processing? / Pass: Skill body contains explicit Task tool dispatch per content item / Fail: Skill iterates over items in a single session context`.

See [references/eval-guide.md](references/eval-guide.md) for detailed examples of good vs bad evals across text, visual, code, and document skills. For this repo’s domain and policy hooks, see [references/eval-criteria.md](references/eval-criteria.md).

**Max score calculation:**
```
max_score = [number of evals] × [runs per experiment]
```

Example: 4 evals × 5 runs = max score of 20.

---

## Step 3: Generate the Live Dashboard

Before running any experiments, create a live HTML dashboard at `autoimprove-[skill-name]/dashboard.html` inside the target skill's folder (or a sibling folder the user approves) and open it in the browser.

The dashboard must:
- Auto-refresh every 10 seconds (reads from results.json)
- Show a score progression line chart (experiment number on X axis, pass rate % on Y axis)
- Show a colored bar for each experiment: green = keep, red = discard, blue = baseline
- Show a table of all experiments with: experiment #, score, pass rate, status, description
- Show per-eval breakdown: which evals pass most/least across all runs
- Show current status: "Running experiment [N]..." or "Idle"

Generate the dashboard as a single self-contained HTML file with inline CSS and JavaScript. Use Chart.js loaded from CDN for the line chart. The JS should fetch `results.json` and re-render.

**Open it immediately** after creating it so the user can watch progress.

**Update `results.json`** after every experiment so the dashboard stays current. Format:

```json
{
  "skill_name": "[name]",
  "status": "running",
  "current_experiment": 3,
  "baseline_score": 70.0,
  "best_score": 90.0,
  "experiments": [
    {
      "id": 0,
      "score": 14,
      "max_score": 20,
      "pass_rate": 70.0,
      "status": "baseline",
      "description": "original skill — no changes",
      "output_tokens_approx": 1840,
      "signal_ratio": 0.65
    }
  ],
  "eval_breakdown": [
    {"name": "Eval name", "pass_count": 8, "total": 10}
  ]
}
```

When the run finishes, update `status` to `"complete"` so the dashboard shows a final summary.

---

## Step 4: Establish Baseline

Run the skill AS-IS before changing anything. This is experiment #0.

1. Create a working directory: `autoimprove-[skill-name]/` inside the skill's folder (e.g. `.cursor/skills/[skill-name]/autoimprove-[skill-name]/`)
2. Create `results.tsv` with the header row
3. Create `results.json` and `dashboard.html`, then open the dashboard
4. Back up the original SKILL.md as `SKILL.md.baseline` in `autoimprove-[skill-name]/` (or alongside SKILL.md per team convention)
5. Run the skill [N] times using the test inputs
6. Score every output against every eval
7. Record the baseline score and update both results.tsv and results.json

**results.tsv format (tab-separated):**

```
experiment	score	max_score	pass_rate	status	description	output_tokens	signal_ratio
0	14	20	70.0%	baseline	original skill — no changes	1840	0.65
```

The `output_tokens` and `signal_ratio` columns are populated when `--measure-tokens` is active; otherwise left blank.

**IMPORTANT:** After establishing baseline, confirm the score with the user before proceeding. If baseline is already 90%+, the skill may not need optimization — ask the user if they want to continue.

---

## Step 5: Run the Experiment Loop

This is the core autoresearch loop. Once started, run autonomously until stopped.

**LOOP:**

1. **Analyze failures.** Look at which evals are failing most. Read the actual outputs that failed. Identify the pattern — is it a formatting issue? A missing instruction? An ambiguous directive?

2. **Form a hypothesis.** Pick ONE thing to change. Do not change 5 things at once — you will not know what helped.

   Good mutations:
   - Add a specific instruction that addresses the most common failure
   - Reword an ambiguous instruction to be more explicit
   - Add an anti-pattern ("Do NOT do X") for a recurring mistake
   - Move a buried instruction higher in the skill (priority = position)
   - Add or improve an example that shows the correct behavior
   - Remove an instruction that causes the skill to over-optimize for one thing at the expense of others
   - Add session-isolation directive for skills that iterate over multiple items (batch loops, list processing) — instruct the skill to dispatch each item to a separate subagent via Task tool to prevent context contamination

   Bad mutations:
   - Rewriting the entire skill from scratch
   - Adding 10 new rules at once
   - Making the skill longer without a specific reason
   - Adding vague instructions like "make it better" or "be more creative"

3. **Make the change.** Edit SKILL.md with ONE targeted mutation.

4. **Run the experiment.** Execute the skill [N] times with the same test inputs. **Each test input MUST run in an isolated subagent via the Task tool** — never accumulate multiple test runs in the same session context. This prevents context contamination where earlier run outputs bias later runs and inflates apparent quality.

5. **Score it.** Run every output through every eval. Calculate total score.

6. **Measure tokens (when `--measure-tokens`).** For each run output:
   - Count approximate output tokens: `word_count × 1.3`
   - Count signal lines (lines containing data, code, or actionable findings) vs total lines → `signal_ratio`
   - Record both in the experiment entry

7. **Decide: keep or discard.**
   - Score improved → **KEEP.** Log it. This is the new baseline.
   - Score stayed the same but output tokens decreased ≥ 10% → **KEEP** (token efficiency win).
   - Score stayed the same, no token improvement → **DISCARD.** Revert SKILL.md to previous version.
   - Score got worse → **DISCARD.** Revert SKILL.md to previous version.

8. **Log the result** in results.tsv and update results.json and changelog.md.

9. **Repeat.** Go back to step 1 of the loop.

**NEVER STOP.** Once the loop starts, do not pause to ask the user if they should continue. They may be away from the computer. Run autonomously until:
- The user manually stops you
- You hit the budget cap (if one was set)
- You hit 95%+ pass rate for 3 consecutive experiments (diminishing returns)

**If you run out of ideas:** Re-read the failing outputs. Try combining two previous near-miss mutations. Try a completely different approach to the same problem. Try removing things instead of adding them. Simplification that maintains the score is a win.

---

## Step 6: Write the Changelog

After each experiment (whether kept or discarded), append to `changelog.md`:

```markdown
## Experiment [N] — [keep/discard]

**Score:** [X]/[max] ([percent]%)
**Change:** [One sentence describing what was changed]
**Reasoning:** [Why this change was expected to help]
**Result:** [What actually happened — which evals improved/declined]
**Failing outputs:** [Brief description of what still fails, if anything]
```

This changelog is the most valuable artifact. It is a research log that any future agent (or smarter future model) can pick up and continue from.

---

## Step 7: Deliver Results

When the user returns or the loop stops, present:

1. **Score summary:** Baseline score → Final score (percent improvement)
2. **Total experiments run:** How many mutations were tried
3. **Keep rate:** How many mutations were kept vs discarded
4. **Top 3 changes that helped most** (from the changelog)
5. **Remaining failure patterns** (what the skill still gets wrong, if anything)
6. **The improved SKILL.md** (already saved in place)
7. **Location of results.tsv and changelog.md** for reference

---

## Output Format

The skill produces four files in `autoimprove-[skill-name]/`:

```
autoimprove-[skill-name]/
├── dashboard.html       # live browser dashboard (auto-refreshes)
├── results.json         # data file powering the dashboard
├── results.tsv          # score log for every experiment
├── changelog.md         # detailed mutation log
└── SKILL.md.baseline    # original skill before optimization
```

Plus the improved SKILL.md saved back to its original location.

**results.tsv example:**

```
experiment	score	max_score	pass_rate	status	description	output_tokens	signal_ratio
0	14	20	70.0%	baseline	original skill — no changes	1840	0.65
1	16	20	80.0%	keep	added explicit instruction to avoid numbering in diagrams	1650	0.72
2	16	20	80.0%	discard	tried enforcing left-to-right layout — no improvement	1900	0.60
3	18	20	90.0%	keep	added color palette hex codes instead of vague description	1420	0.78
4	18	20	90.0%	discard	added anti-pattern for neon colors — no improvement	1500	0.70
5	19	20	95.0%	keep	added worked example showing correct label formatting	1380	0.82
```

---

## How This Connects to Other Skills

**What feeds into autoresearch:**
- Any existing skill under `.cursor/skills/` that needs runtime quality optimization
- `skill-optimizer` audit results (fix structural issues before entering the mutation loop)
- User-defined eval criteria (or help them define evals using the eval guide)

**What autoresearch feeds into:**
- The improved skill replaces the original (backup kept as `SKILL.md.baseline`)
- `skill-optimizer` benchmark mode (run fresh benchmarks to verify improvements generalize)
- The changelog can be passed to future models for continued optimization
- The eval suite can be reused whenever the skill is updated
- Significant findings should be captured in `AGENTS.md`, `MEMORY.md`, or `docs/ai/feedback.md` per team practice

**Related skills (different purposes):**
- `skill-optimizer` — Static audit, eval, benchmark, and A/B comparison. Use for measurement. Autoresearch uses measurement results to drive autonomous mutation.
- `create-skill` — Create skills from scratch. Autoresearch optimizes existing skills.
- `doc-quality-gate` / evaluator-optimizer workflows — Improve a specific document output; autoresearch improves the skill prompt itself.
- `autoskill-evolve` — Mines transcripts for new skill candidates. Autoresearch improves existing skills through runtime experiments.
- `meta-harness-optimizer` — Outer-loop code-level optimization. Uses `--trace-aware` data from this skill as the inner-loop feedback layer.

---

## Harness Mode (`--harness-mode`)

When invoked with `--harness-mode`, the autoresearch loop operates on a single-file agent harness (`agent.py`) instead of a SKILL.md prompt. Mutations target the editable section of the harness (above the `FIXED ADAPTER BOUNDARY` marker) while benchmark evaluation runs in Docker via `autoagent-benchmark`.

### Activation

```
skill-autoimprove --harness-mode --target agent.py --tasks data/bench/
```

Or when `autoagent-loop` invokes this skill in `prompt-only` mode, harness-mode activates automatically with the harness path and task suite forwarded.

### What Changes

| Aspect | Normal Mode | Harness Mode |
|--------|------------|--------------|
| Mutation target | SKILL.md prompt text | Editable section of `agent.py` (above fixed boundary) |
| Evaluation | Local skill execution + binary evals | Docker-isolated benchmark via `autoagent-benchmark` |
| Scoring | Pass/fail count against eval criteria | Aggregate benchmark score from `ScoreAggregator` |
| Trace format | `autoimprove-*/traces/` JSON logs | ATIF trajectories via `ATIFLogger` |
| Experiment tracking | `results.tsv` + `changelog.md` | Same + `ExperimentLedger` JSON ledger |
| Boundary enforcement | N/A | Never modify content below `FIXED ADAPTER BOUNDARY` |

### Harness Mutation Rules

1. Extract the editable section via `HarnessTemplate.extract_editable()`
2. Apply one mutation to the editable section only
3. Reassemble via `HarnessTemplate.replace_editable()`
4. Run benchmark in Docker to score
5. Keep/discard per the standard decision logic
6. Snapshot kept harness via `ExperimentLedger.record()`

### Integration with autoagent-loop

When `autoagent-loop` runs in `prompt-only` mode:
1. It invokes this skill with `--harness-mode`
2. This skill treats the harness prompt/instructions as the mutation target
3. Benchmark scores flow back to `autoagent-loop` for ledger tracking
4. ATIF trajectories are written to `outputs/autoagent-trajectories/`

### Prerequisites

- Docker installed and running (for benchmark execution)
- `scripts/autoagent/` package available
- Task suite in Harbor format (see `autoagent-benchmark` skill)

---

## Trace-Aware Mode (`--trace-aware`)

When invoked with `--trace-aware`, the autoresearch loop captures full execution traces (tool calls, model outputs, state transitions) alongside the normal binary eval scores. This bridges the inner loop (prompt-text mutation) with the outer loop (`meta-harness-optimizer` code-level mutation) by providing richer feedback than scores alone.

### Activation

Add `--trace-aware` when invoking the skill:

```
skill-autoimprove --trace-aware --target .cursor/skills/trading/daily-stock-check/SKILL.md
```

Or when `meta-harness-optimizer` invokes this skill as an inner-loop step, trace-aware mode activates automatically.

### What Changes

| Aspect | Normal Mode | Trace-Aware Mode |
|--------|------------|-----------------|
| Eval output | Binary pass/fail scores | Scores + full execution trace per eval case |
| Storage | `results.tsv` + `changelog.md` | Same + `traces/` directory via TraceArchive |
| Proposer context | Current SKILL.md + score history | Same + selective trace grep for failure patterns |
| Archive format | Flat files in `autoimprove-*/` | Compatible with `scripts/meta_harness_trace.py` TraceArchive |
| Overhead | ~1x | ~1.3x (trace serialization) |

### Trace Capture

During each eval run, the following events are captured per test case:

1. **Input context** — the test prompt/scenario provided
2. **Skill invocation** — the full prompt sent to the LLM
3. **Model response** — raw output before eval scoring
4. **Tool calls** — any tools the skill invoked during execution (with arguments and results)
5. **Eval results** — per-eval pass/fail with the specific output that was evaluated
6. **Timing** — wall-clock duration per step

Traces are written to `autoimprove-[skill-name]/traces/exp-{N}/case-{M}.log` as JSON.

### Integration with Meta-Harness

When `meta-harness-optimizer` runs this skill as an inner loop:

1. Meta-Harness sets `--trace-aware` and provides a `--archive-root` path
2. This skill writes traces to the shared TraceArchive instead of local `traces/`
3. The Meta-Harness proposer can then read uncompressed traces to propose code-level mutations
4. Both prompt-level (this skill) and code-level (meta-harness) improvements accumulate

### Trace Output Structure

```
autoimprove-[skill-name]/
├── traces/
│   ├── exp-0/              # baseline traces
│   │   ├── case-000.log
│   │   └── case-001.log
│   ├── exp-1/              # first mutation traces
│   │   ├── case-000.log
│   │   └── case-001.log
│   └── ...
├── results.tsv
├── results.json
├── changelog.md
└── dashboard.html
```

Each `case-NNN.log` is a JSON file:

```json
{
  "experiment_id": 1,
  "case_id": "case-000",
  "input": "analyze AAPL stock",
  "skill_prompt_hash": "a1b2c3",
  "steps": [
    {"type": "llm_call", "prompt_tokens": 1200, "completion_tokens": 800, "duration_ms": 2300},
    {"type": "tool_call", "tool": "WebSearch", "args": {"query": "AAPL earnings"}, "duration_ms": 450}
  ],
  "output": "... full model output ...",
  "evals": [
    {"name": "Financial terminology", "pass": true},
    {"name": "Signal expression", "pass": false, "reason": "missing RSI value"}
  ],
  "total_tokens": 2000,
  "wall_clock_ms": 3200
}
```

---

## Constraint Gates

Every mutation must pass all constraint gates before being accepted. Gates run automatically after scoring and before the keep/discard decision. If any gate fails, the mutation is discarded regardless of score improvement.

### Gate List

| Gate | Rule | Default | Override |
|------|------|---------|----------|
| **Max size** | Mutated SKILL.md must not exceed `max_chars` | 15,000 chars | `--max-chars N` |
| **Growth rate** | Mutated body length ≤ baseline body length × `growth_cap` | 1.20 (20% growth) | `--growth-cap N` |
| **Non-empty body** | The skill body (below frontmatter) must contain at least one non-whitespace line | Always on | Cannot disable |
| **Trigger preservation** | All trigger phrases from the `description` field's "Use when" clause must remain present | Always on | Cannot disable |
| **Boundary preservation** | All "Do NOT use" entries from the baseline must remain present | Always on | Cannot disable |
| **Section structure** | H2 heading count ≥ baseline H2 count × 0.5 (prevents structural collapse) | Always on | `--min-h2-ratio N` |

### Disabling Gates

Pass `--no-gates` to skip all gates (useful for exploratory runs where structural constraints are not yet established). Individual gates cannot be disabled independently except via the override flags listed above.

### Gate Failure Logging

When a gate fails, the experiment entry in `changelog.md` includes:

```markdown
**Gate failure:** [gate name] — [reason]
Example: "Growth rate — mutated body is 18,200 chars (baseline 14,500 × 1.20 = 17,400 max)"
```

The `results.tsv` entry records the status as `gate-fail` instead of `discard`.

---

## Synthetic Eval Mode (`--synthetic-eval`)

When no manual eval criteria are available, `--synthetic-eval` auto-generates evaluation cases from the target skill's text. This removes the cold-start barrier for skills that lack pre-defined test inputs.

### Activation

```
skill-autoimprove --synthetic-eval --target .cursor/skills/trading/daily-stock-check/SKILL.md
```

Or combine with other flags:

```
skill-autoimprove --synthetic-eval --trace-aware --target .cursor/skills/some-skill/SKILL.md
```

### How It Works

1. **Parse the skill** — Extract the skill's name, description, triggers, constraints, and process steps from SKILL.md.
2. **Generate eval cases** — Use an LLM subagent to produce 8-12 synthetic test cases, each containing:
   - `task_input`: A realistic user prompt that should trigger the skill
   - `expected_behavior`: What a correct execution looks like (binary-checkable)
   - `anti_behavior`: What a bad execution looks like (the inverse check)
   - `difficulty`: `easy` | `medium` | `hard` — distribution target: 30% easy, 50% medium, 20% hard
3. **Split into train/holdout** — 80% of cases go to the training set (used during the mutation loop), 20% are reserved for holdout evaluation (see Holdout Evaluation below).
4. **Convert to binary evals** — Each case becomes a binary eval following the standard format:
   ```
   EVAL [N]: [Short name from task_input]
   Question: Does the output exhibit expected_behavior and NOT exhibit anti_behavior?
   Pass condition: expected_behavior is present
   Fail condition: anti_behavior is detected OR expected_behavior is missing
   ```

### Quality Controls

- Generated cases must cover at least 3 distinct trigger phrases from the skill description
- At least one case must test a "Do NOT use" boundary (negative trigger)
- Cases are deduplicated by semantic similarity before use
- The user is shown the generated eval suite and can approve, edit, or regenerate before the loop starts

### Combining with Manual Evals

If the user provides some manual evals but fewer than 3, `--synthetic-eval` supplements with generated cases up to the 8-12 target range. Manual evals always take priority and are never replaced.

---

## Holdout Evaluation

After the mutation loop completes (either by reaching the score ceiling, budget cap, or user stop), a holdout evaluation runs to verify that improvements generalize and are not overfit to the training inputs.

### How It Works

1. **Reserve holdout set** — When `--synthetic-eval` is active, 20% of generated cases are held back and never used during the mutation loop. When manual evals are provided, the user can designate holdout inputs via `--holdout-inputs file.json` or the system reserves the last 20% of test inputs.
2. **Run baseline on holdout** — Score the original `SKILL.md.baseline` against the holdout cases.
3. **Run evolved on holdout** — Score the final evolved SKILL.md against the same holdout cases.
4. **Compare** — Calculate the delta. If the evolved skill performs ≥ baseline on holdout cases, the improvement is validated. If it performs worse, a warning is logged.

### Holdout Results

Results are appended to `results.tsv` as a special entry:

```
experiment	score	max_score	pass_rate	status	description
holdout-baseline	3	4	75.0%	holdout	baseline on unseen cases
holdout-evolved	4	4	100.0%	holdout	evolved skill on unseen cases
```

The `results.json` includes a `holdout` section:

```json
{
  "holdout": {
    "baseline_score": 3,
    "evolved_score": 4,
    "max_score": 4,
    "baseline_rate": 75.0,
    "evolved_rate": 100.0,
    "delta": 25.0,
    "verdict": "validated"
  }
}
```

### Verdicts

| Verdict | Condition | Action |
|---------|-----------|--------|
| `validated` | Evolved score ≥ baseline score on holdout | Accept the evolved skill |
| `marginal` | Evolved score = baseline score on holdout | Accept with warning — improvement may be overfit to training inputs |
| `overfit` | Evolved score < baseline score on holdout | Revert to baseline and log warning; the training-set improvements did not generalize |

When the verdict is `overfit`, the skill is automatically reverted to `SKILL.md.baseline` and the changelog records the reversion reason.

### Dashboard Integration

The holdout results appear as a separate panel in the dashboard showing baseline vs evolved comparison on unseen data, with a clear PASS/WARN/FAIL badge.

---

## The Test

A good autoresearch run:

1. **Started with a baseline** — never changed anything before measuring the starting point
2. **Used binary evals only** — no scales, no vibes, no "rate this 1-10"
3. **Changed one thing at a time** — so you know exactly what helped
4. **Kept a complete log** — every experiment recorded, kept or discarded
5. **Improved the score** — measurable improvement from baseline to final
6. **Did not overfit** — the skill got better at the actual job, not just at passing the specific test inputs
7. **Ran autonomously** — did not stop to ask permission between experiments

If the skill "passes" all evals but the actual output quality has not improved — the evals are bad, not the skill. Go back to step 2 and write better evals.

---

## Project-Specific Overrides

Applies only in **ai-model-event-stock-analytics**. Canonical policy text: `docs/policies/`.

| Override | Path |
|----------|------|
| Document standards (POL-004 alignment) | [.cursor/skills/references/project-overrides/project-document-standards.md](../references/project-overrides/project-document-standards.md) |
| Terminology / forbidden terms (POL-001) | [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) |
| UI stack (Tailwind + Radix, not TDS) | [.cursor/skills/references/project-overrides/project-design-conventions.md](../references/project-overrides/project-design-conventions.md) |

**Constraints:** Eval suites must include financial-domain checks when the skill touches markets, signals, or reports; verify **POL-001** forbidden terms are not introduced by mutations; **eval scope** defaults to **project-specific** skills under `.cursor/skills/` for this repository unless the user expands scope.

## Verification Protocol

Before reporting any review or audit complete, verify findings with evidence:

    ### Check: [what you are verifying]
    **Command run:** [exact command executed]
    **Output observed:** [actual output — copy-paste, not paraphrased]
    **Result:** PASS or FAIL (with Expected vs Actual if FAIL)

A check without a command-run block is not a PASS — it is a skip.

Before issuing PASS: must include at least one adversarial probe (boundary input, concurrent request, missing data, permission edge case).

Before issuing FAIL: check if the issue is already handled elsewhere, intentional by design, or not actionable without breaking an external contract.

End verification with: `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Rationalization Detection

Recognize these rationalizations and do the opposite:

| Rationalization | Reality |
|----------------|---------|
| "The code looks correct based on my reading" | Reading is not verification. Run it. |
| "The implementer's tests already pass" | The implementer is an LLM. Verify independently. |
| "This is probably fine" | Probably is not verified. Run it. |
| "I don't have access to test this" | Did you check all available tools? |
| "This would take too long" | Not your call. Run the check. |
| "Let me check the code structure" | No. Start the server and hit the endpoint. |

If you catch yourself writing an explanation instead of running a command, stop. Run the command.
