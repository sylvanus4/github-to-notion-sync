---
name: hermes-skill-evolver
description: >-
  Population-based skill evolution inspired by
  NousResearch/hermes-agent-self-evolution. Treats SKILL.md body text as an
  optimizable parameter, generates N variant bodies per iteration, scores them
  via a 5-dimension LLM-Judge rubric, applies constraint gates (size, growth
  rate, trigger/boundary preservation), and selects the fittest via holdout
  evaluation. Produces evolved SKILL.md, results.tsv, changelog.md, and a
  dashboard. Use when the user asks "hermes evolve", "evolve skill with
  hermes", "GEPA evolve", "fitness-based skill evolution",
  "hermes-skill-evolver", "population-based skill optimization", "에르메스 진화",
  "스킬 진화", "스킬 피트니스 최적화", "population evolution", "variant-based skill
  improvement", or wants DSPy/GEPA-style multi-variant evolution for a
  SKILL.md file. Do NOT use for single-mutation iterative loops (use
  skill-autoimprove). Do NOT use for static quality audits without evolution
  (use skill-optimizer audit). Do NOT use for creating new skills from scratch
  (use create-skill). Do NOT use for transcript-based skill mining (use
  autoskill-evolve). Do NOT use for prompt framework selection (use
  prompt-architect).
---

# Hermes Skill Evolver

Population-based evolution for SKILL.md files. Where `skill-autoimprove` mutates one thing at a time and runs binary pass/fail evals, this skill generates **multiple variant bodies per iteration**, scores each against a **5-dimension LLM-Judge rubric**, enforces **constraint gates** to prevent regression, and validates the winner on a **holdout set** before committing.

Adapted from NousResearch's Hermes Agent Self-Evolution project which uses DSPy + GEPA (Genetic-Pareto Prompt Evolution). This skill replaces the DSPy dependency with LLM-native prompt optimization through Cursor's subagent infrastructure.

---

## When to Use This vs Alternatives

| Scenario | Skill |
|----------|-------|
| Evolve a skill with population-based multi-variant competition | **hermes-skill-evolver** (this) |
| Iterative single-mutation improvement with binary evals | `skill-autoimprove` |
| Static quality audit or A/B comparison | `skill-optimizer` |
| Create a skill from scratch | `create-skill` |
| Mine transcripts for new skill candidates | `autoskill-evolve` |

---

## Before Starting: Gather Context

**Confirm all fields with the user. Ask for any missing fields before proceeding.**

1. **Target skill** -- exact path to SKILL.md under `.cursor/skills/`
2. **Variants per iteration** -- how many variant bodies to generate per round. Default: 4
3. **Max iterations** -- maximum evolution rounds. Default: 3
4. **Eval source** -- one of:
   - `synthetic` (auto-generate from skill text -- default)
   - `manual` (user provides eval cases)
   - `mixed` (user provides some, auto-generate the rest)
5. **Mutation strategies** -- which to enable (default: all):
   - `rephrase` -- reword instructions for clarity
   - `restructure` -- reorder sections for better priority
   - `add-constraints` -- add missing guardrails
   - `simplify` -- remove redundant instructions
   - `specialize` -- narrow scope for precision
6. **Budget cap** -- optional max total LLM calls before stopping

---

## Step 1: Parse Target SKILL.md

Read the target SKILL.md and split into two parts:

1. **Frontmatter** (YAML between `---` delimiters) -- preserved exactly, never modified
2. **Body** (everything after the closing `---`) -- the optimization target

Record baseline metrics:
- Body character count
- Body line count
- Trigger keywords extracted from `description:` field
- "Do NOT use" boundaries extracted from `description:` field
- Section headings (H2/H3) present

Store the original body as `SKILL.md.baseline` in the working directory.

---

## Step 2: Generate Synthetic Eval Dataset

If eval source is `synthetic` or `mixed`, auto-generate evaluation cases from the skill text.

**Generation prompt (sent to LLM):**

```
Read the following skill definition and generate {N} evaluation test cases.

SKILL TEXT:
{body_text}

For each test case, produce:
- task_input: a realistic user request that should trigger this skill
- expected_behavior: what the skill output MUST contain or demonstrate
- anti_behavior: what the skill output must NOT contain
- difficulty: easy | medium | hard

Requirements:
- Cover the skill's stated workflow steps
- Include at least 2 edge cases (unusual input, minimal input)
- Include at least 1 negative test (input that should NOT trigger this skill)
- Vary difficulty levels
- Output as a JSON array
```

Generate 10-20 cases. If `mixed`, merge with user-provided cases (deduplicate by `task_input` similarity).

**Split the dataset:**
- 60% training set (used during evolution scoring)
- 20% validation set (used for variant selection)
- 20% holdout set (used only for final comparison -- never seen during evolution)

Write the full dataset to `evolution-{skill-name}/eval-dataset.json`.

---

## Step 3: Baseline Fitness Score

Score the **original** skill body against the training set using the LLM-Judge rubric.

### LLM-Judge Rubric (5 Dimensions, 0-10 each)

For each eval case, send to an LLM-Judge:

```
You are evaluating an AI agent skill's effectiveness. Given the skill text and a
test scenario, score the skill on 5 dimensions.

SKILL TEXT:
{body_text}

TEST CASE:
- Input: {task_input}
- Expected behavior: {expected_behavior}
- Anti-behavior: {anti_behavior}

Score each dimension 0-10:

1. ACCURACY: Does the skill correctly guide the agent to complete this task?
   0 = completely wrong guidance, 10 = perfect guidance
2. PROCEDURE: Does the skill define clear, ordered steps for this task?
   0 = no procedure, 10 = unambiguous step-by-step
3. CONCISENESS: Is the skill free of redundant or contradictory instructions?
   0 = bloated/contradictory, 10 = every sentence is load-bearing
4. TRIGGER_PRECISION: Would the description field correctly activate for this input?
   0 = would never trigger, 10 = perfect match
5. BOUNDARY_CLARITY: Are "Do NOT use" rules clear enough to prevent misactivation?
   0 = no boundaries, 10 = precise with alternative skill redirects

Also provide:
- feedback: one sentence describing the biggest weakness
- suggested_fix: one concrete improvement suggestion

Output as JSON:
{"accuracy": N, "procedure": N, "conciseness": N, "trigger_precision": N,
 "boundary_clarity": N, "feedback": "...", "suggested_fix": "..."}
```

**Composite score** = weighted average:
- Accuracy: 30%
- Procedure: 25%
- Conciseness: 15%
- Trigger precision: 15%
- Boundary clarity: 15%

Record baseline composite score. This is the bar to beat.

---

## Step 4: Evolution Loop

For each iteration (up to max_iterations):

### 4a. Generate Variants

Generate N variant bodies using enabled mutation strategies. Each variant uses a different strategy or combination:

**Mutation prompt template:**

```
You are optimizing an AI agent skill. The current skill body has a composite
fitness score of {baseline_score}/10.

LLM-Judge feedback from evaluation:
{aggregated_feedback}

Top failure patterns:
{top_3_weakest_dimensions_with_examples}

CURRENT SKILL BODY:
{current_body}

MUTATION STRATEGY: {strategy_name}
{strategy_description}

Generate an improved version of the skill body. Rules:
- Preserve all existing trigger keywords
- Preserve all "Do NOT use" boundaries
- Do not add YAML frontmatter (it is managed separately)
- Focus the improvement on addressing the feedback above
- Output ONLY the new skill body text, nothing else
```

**Strategy descriptions:**

| Strategy | Instruction |
|----------|-------------|
| `rephrase` | Reword ambiguous or weak instructions. Make implicit requirements explicit. Clarify terminology. Do not change the structure. |
| `restructure` | Reorder sections to put the most important instructions first. Move critical constraints earlier. Group related instructions. |
| `add-constraints` | Add missing guardrails, error handling, or edge case instructions based on the feedback. Do not remove existing content. |
| `simplify` | Remove redundant sentences, merge overlapping instructions, eliminate filler. Reduce character count while preserving all guidance. |
| `specialize` | Narrow the skill's scope where feedback indicates over-generalization. Make workflow steps more specific. Add concrete examples. |
| `add-session-isolation` | If the skill iterates over multiple items (batch loops, list processing, multi-file scans), add explicit directives to dispatch each item to a separate subagent via Task tool to prevent context contamination across items. |

### 4b. Evaluate Variants

Score each variant against the **validation set** using the same LLM-Judge rubric. **Each variant MUST be evaluated in an isolated subagent via the Task tool** — never accumulate multiple variant evaluations in the same session context. This prevents earlier variant scores from biasing later evaluations through context contamination.

### 4c. Apply Constraint Gates

Before accepting any variant, it must pass ALL gates:

| Gate | Rule | Action on Fail |
|------|------|----------------|
| **Max size** | Body ≤ 15,000 chars (configurable) | Discard variant |
| **Growth rate** | Body ≤ baseline size × 1.20 | Discard variant |
| **Non-empty** | Body length > 0 | Discard variant |
| **Trigger preservation** | All baseline trigger keywords still present | Discard variant |
| **Boundary preservation** | All baseline "Do NOT use" phrases still present | Discard variant |
| **Section structure** | H2 section count ≥ baseline H2 count × 0.5 | Discard variant |
| **Session isolation** | If skill processes multiple items, variant must contain per-item subagent dispatch directive (Task tool) | Warn (non-blocking) |

Log constraint failures in `changelog.md` with the specific gate that failed.

### 4d. Select Best Variant

Among variants that pass all gates:
- Compare composite scores against current baseline
- If best variant score > baseline score: adopt as new baseline, log as **KEEP**
- If no variant beats baseline: log all as **DISCARD**, proceed to next iteration
- If multiple variants tie: prefer the one with fewer characters (conciseness wins)

### 4e. Log Results

Append to `results.tsv`:

```
iteration	variant	strategy	accuracy	procedure	conciseness	trigger	boundary	composite	status	chars	description
0	baseline	-	7.2	6.8	5.5	8.0	7.5	7.04	baseline	4230	original skill
1	v1	rephrase	7.5	7.0	6.0	8.0	7.5	7.24	keep	4180	clarified ambiguous steps
1	v2	simplify	7.0	6.5	7.5	8.0	7.5	7.14	discard	3800	lost procedure clarity
1	v3	add-constraints	7.8	7.2	5.0	8.0	8.0	7.24	gate-fail	5200	exceeded growth rate
```

Append to `changelog.md`:

```markdown
## Iteration 1

### Variant v1 (rephrase) -- KEEP
**Score:** 7.24/10 (baseline: 7.04, +2.8%)
**Strategy:** rephrase
**Change:** Clarified Steps 3-5 with explicit input/output per step
**Judge feedback:** "Steps were previously ambiguous about when to use subagents"
**Constraint gates:** ALL PASS (4180 chars, +0% growth)

### Variant v2 (simplify) -- DISCARD
**Score:** 7.14/10 (baseline: 7.04, +1.4%)
**Strategy:** simplify
**Change:** Merged overlapping sections, removed 430 chars
**Result:** Procedure score dropped from 6.8 to 6.5
**Constraint gates:** ALL PASS

### Variant v3 (add-constraints) -- GATE FAIL
**Strategy:** add-constraints
**Gate failed:** growth_rate (5200 chars = +22.9%, limit 20%)
```

---

## Step 5: Holdout Evaluation

After all iterations complete, run the final evolved skill against the **holdout set** (never seen during evolution).

1. Score evolved body on holdout set with LLM-Judge
2. Score original baseline body on holdout set with LLM-Judge
3. Compare:
   - If evolved holdout score > baseline holdout score by ≥ 0.3 points: **ADOPT**
   - If difference < 0.3 points: **KEEP ORIGINAL** (improvement did not generalize)
   - If evolved < baseline: **KEEP ORIGINAL** (overfitting detected)

Report holdout results:

```
Holdout Evaluation
==================
Baseline holdout score: 7.10/10
Evolved holdout score:  7.85/10
Delta:                  +0.75 (10.6% improvement)
Verdict:                ADOPT -- improvement generalizes to unseen cases
```

---

## Step 6: Save Results

If verdict is ADOPT:
1. Write evolved body back to SKILL.md (preserving original frontmatter exactly)
2. Backup original as `SKILL.md.baseline` in `evolution-{skill-name}/`

If verdict is KEEP ORIGINAL:
1. Do not modify SKILL.md
2. Log the attempt in `evolution-{skill-name}/changelog.md`

Always produce:
```
evolution-{skill-name}/
├── changelog.md         # per-variant mutation log with scores
├── results.tsv          # tabular score data
├── results.json         # dashboard data
├── dashboard.html       # live browser dashboard (auto-refreshes)
├── eval-dataset.json    # full synthetic + manual eval cases
├── SKILL.md.baseline    # original skill before evolution
└── holdout-report.md    # final holdout comparison
```

---

## Step 7: Generate Dashboard

Create a self-contained HTML dashboard at `evolution-{skill-name}/dashboard.html`.

The dashboard must:
- Auto-refresh every 10 seconds from `results.json`
- Show a **radar chart** of the 5 dimensions (baseline vs evolved)
- Show a **score progression** chart across iterations
- Show a **constraint gate pass/fail** matrix per variant
- Show the holdout comparison result
- Show per-variant details expandable in a table

Use Chart.js from CDN. Open the dashboard immediately after creation.

---

## Step 8: Deliver Results

Present to the user:

1. **Score summary:** Baseline → Final (per-dimension breakdown)
2. **Iterations run / Variants evaluated / Variants kept**
3. **Constraint gate failure count and reasons**
4. **Holdout verdict:** ADOPT or KEEP ORIGINAL
5. **Top changes that helped** (from changelog)
6. **Remaining weaknesses** (from final Judge feedback)

---

## Integration with Existing Skills

**What feeds into this skill:**
- `skill-optimizer audit` results (fix structural issues before evolving)
- `skill-upgrade-validator` pattern compliance scores
- Manual or session-based eval datasets

**What this skill feeds into:**
- Evolved SKILL.md replaces the original (backup kept)
- `skill-optimizer benchmark` mode for post-evolution verification
- `autoskill-evolve` can use holdout methodology for its merge decisions
- Changelog and eval datasets persist for future evolution runs

**Complementary workflows:**
- Run `skill-optimizer audit` → fix issues → run `hermes-skill-evolver` → run `skill-optimizer benchmark` to verify
- Use `skill-autoimprove` for quick single-mutation fixes; use this skill for deeper structural evolution

---

## Constraints

- **Freedom level:** Medium -- structured evolution workflow, but flexible mutation strategies
- Never modify YAML frontmatter -- body text only
- Never remove trigger keywords present in the original description
- Never remove "Do NOT use" boundaries present in the original description
- Maximum 3 iterations by default (configurable) to prevent runaway cost
- Maximum 5 variants per iteration by default (configurable)
- All LLM-Judge calls use the same model for consistency within a run
- Holdout set is never used during the evolution loop

---

## Error Handling

| Error | Action |
|-------|--------|
| Target SKILL.md not found | Ask user for correct path |
| SKILL.md has no `---` delimiters | Flag as Critical; cannot split frontmatter/body |
| Synthetic eval generation returns < 5 cases | Warn user; ask for manual supplementation |
| All variants fail constraint gates | Log iteration as "all gated"; continue to next iteration |
| All iterations produce no improvement | Keep original; report in holdout-report.md |
| LLM-Judge returns malformed JSON | Retry once; if still malformed, score as 0 and log warning |
| Budget cap reached mid-iteration | Complete current iteration's scoring; skip remaining iterations; proceed to holdout |

---

## Gotchas

- **Trigger keyword detection is substring-based.** If the original description says "run backtest" and the evolved body says "run the backtest", the trigger check still passes. But if "backtest" disappears entirely, the gate fails.
- **Growth rate is calculated on characters, not lines.** A skill that restructures from many short lines to fewer long lines may appear to shrink in lines but grow in characters.
- **LLM-Judge scores are relative, not absolute.** A score of 7.5 from one model is not comparable to 7.5 from another model. Always compare within the same run.
- **Synthetic eval cases may cluster around happy paths.** Explicitly inject edge cases and negative tests if the auto-generator produces only straightforward scenarios.
- **Holdout set is small (20%).** With 10 total cases, the holdout is only 2 cases. Consider generating 20 cases minimum for meaningful holdout statistics.

---

## Examples

### Example 1: Evolve a trading analysis skill

```
User: hermes evolve .cursor/skills/trading/daily-stock-check/SKILL.md
```

Actions:
1. Parse SKILL.md, split frontmatter/body
2. Generate 15 synthetic eval cases (stock analysis scenarios)
3. Split: 9 train, 3 val, 3 holdout
4. Baseline score: 6.8/10 (weak on procedure: 5.5)
5. Iteration 1: 4 variants → v2 (restructure) wins at 7.3
6. Iteration 2: 4 variants → v1 (add-constraints) wins at 7.6
7. Iteration 3: 4 variants → no improvement
8. Holdout: evolved 7.4 vs baseline 6.6 → ADOPT (+12.1%)

Result: Evolved skill with clearer step ordering and missing edge case handling

### Example 2: Evolution blocked by constraints

```
User: hermes evolve .cursor/skills/review/deep-review/SKILL.md --variants 3 --max-iterations 2
```

Actions:
1. Parse, generate 12 eval cases
2. Baseline: 7.8/10
3. Iteration 1: v1 gate-fail (growth +25%), v2 keep (7.9), v3 discard
4. Iteration 2: all variants gate-fail or no improvement
5. Holdout: evolved 7.9 vs baseline 7.8 → KEEP ORIGINAL (delta 0.1 < 0.3)

Result: Original skill preserved; skill was already well-optimized
