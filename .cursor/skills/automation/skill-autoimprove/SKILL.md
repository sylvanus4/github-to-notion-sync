---
name: skill-autoimprove
description: >-
  Autonomously optimize an existing skill prompt: repeated runs, binary evals,
  one mutation at a time, keep only improvements (Karpathy-style autoresearch).
  Supports --trace-aware mode for full execution trace capture (tool calls,
  model outputs, state changes) compatible with meta-harness-optimizer's
  outer-loop code-level optimization via TraceArchive.
  Use when the user asks "skill-autoimprove", "auto-improve this skill",
  "스킬 자동 개선", "프롬프트 자동 개선", "스킬 실험 루프", "스킬 최적화 루프",
  "run evals and fix skill", "self-improve skill", or wants a loop that mutates
  SKILL.md until scores improve. Produces improved SKILL.md, results.tsv,
  changelog.md, and a live HTML dashboard.
  Do NOT use for static audits only (skill-optimizer audit), new skill creation
  (create-skill), single-doc polish without editing the skill (doc-quality-gate
  / workflow-patterns evaluator-optimizer), transcript mining (autoskill-evolve),
  or paper pipelines (paper-review).
metadata:
  author: "thaki"
  version: "2.1.0"
  category: "self-improvement"
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
3. **Eval criteria** — 3-6 binary yes/no checks that define a good output. See [references/eval-guide.md](references/eval-guide.md) and [references/eval-criteria.md](references/eval-criteria.md). **Scope**: optimize **project-specific** skills for this repo unless the user explicitly names another skill; evals must include finance/domain accuracy and POL-001 forbidden-term checks when the skill produces user-facing or domain copy.
4. **Runs per experiment** — How many times to run the skill per mutation. Default: 5. More runs = more reliable scores, but slower. 5 is the sweet spot.
5. **Budget cap** — Optional. Max number of experiment cycles before stopping. Default: no cap (runs until stopped or ceiling hit).

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
      "description": "original skill — no changes"
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
experiment	score	max_score	pass_rate	status	description
0	14	20	70.0%	baseline	original skill — no changes
```

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

   Bad mutations:
   - Rewriting the entire skill from scratch
   - Adding 10 new rules at once
   - Making the skill longer without a specific reason
   - Adding vague instructions like "make it better" or "be more creative"

3. **Make the change.** Edit SKILL.md with ONE targeted mutation.

4. **Run the experiment.** Execute the skill [N] times with the same test inputs.

5. **Score it.** Run every output through every eval. Calculate total score.

6. **Decide: keep or discard.**
   - Score improved → **KEEP.** Log it. This is the new baseline.
   - Score stayed the same → **DISCARD.** Revert SKILL.md to previous version. The change added complexity without improvement.
   - Score got worse → **DISCARD.** Revert SKILL.md to previous version.

7. **Log the result** in results.tsv and update results.json and changelog.md.

8. **Repeat.** Go back to step 1 of the loop.

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
experiment	score	max_score	pass_rate	status	description
0	14	20	70.0%	baseline	original skill — no changes
1	16	20	80.0%	keep	added explicit instruction to avoid numbering in diagrams
2	16	20	80.0%	discard	tried enforcing left-to-right layout — no improvement
3	18	20	90.0%	keep	added color palette hex codes instead of vague description
4	18	20	90.0%	discard	added anti-pattern for neon colors — no improvement
5	19	20	95.0%	keep	added worked example showing correct label formatting
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
