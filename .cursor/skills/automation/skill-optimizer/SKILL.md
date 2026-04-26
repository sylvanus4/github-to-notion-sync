---
name: skill-optimizer
description: >-
  Audit, evaluate, benchmark, compare, and fitness-score existing agent skills
  (SKILL.md files) for quality assurance. Includes LLM-Judge multi-dimensional
  fitness scoring mode for pre-evolution diagnostics. Use when the user asks to
  "optimize skills", "audit skills", "check skill quality", "evaluate skill",
  "benchmark skill", "test skill effectiveness", "compare skill versions",
  "skill regression test", "measure skill impact", "fitness score", "LLM judge
  skill", "skill fitness", "스킬 최적화", "스킬 감사", "스킬 품질 점검",
  "스킬 평가", "스킬 벤치마크", "스킬 비교", "스킬 테스트", "트리거 정확도",
  "스킬 피트니스", "LLM 판사 스킬".
  Do NOT use for creating new skills from scratch (use create-skill instead),
  autonomous prompt mutation loops (use skill-autoimprove), population-based
  multi-variant evolution (use hermes-skill-evolver), transcript-based
  skill extraction (use autoskill-extractor), general code review, or non-skill
  file optimization.
metadata:
  author: "thaki"
  version: "2.1.0"
  category: "review"
---
# Skill Optimizer

Quality assurance for agent skills: static audit, runtime evaluation, quantitative benchmarking, and A/B comparison. Adapted from Anthropic's Executor/Grader/Comparator/Analyzer pattern for Cursor's Task subagent system. Use in this repo alongside `post-skill-creation.mdc` (audit after new skills) and `skill-orchestration.mdc` (registry awareness).

## Input

The user provides:
1. **Mode** (optional) — `audit` (default), `eval`, `benchmark`, or `compare`
2. **Skills directory** (optional) — defaults to `.cursor/skills/` in this workspace
3. **Scope** (optional) — "all" (default) or a specific skill name

## Modes

### audit (default) — Static Quality Analysis

Analyze skill files against Anthropic's guide without running them. See [Audit Workflow](#audit-workflow) below.

### eval — Runtime Test Cases

Write and run test cases against a skill using independent subagents. Measures whether a skill produces the intended behavioral change. See [references/eval-framework.md](references/eval-framework.md) for full protocol.

### benchmark — Quantitative Performance Measurement

Run multiple eval iterations and collect statistical metrics: pass rate, quality score, token efficiency, consistency. See [references/benchmark-protocol.md](references/benchmark-protocol.md) for full protocol.

### compare — A/B Blind Comparison

Run identical prompts through two skill versions (or skill vs no-skill) and have an independent Comparator judge outputs blindly. See [references/comparator-protocol.md](references/comparator-protocol.md) for full protocol.

### fitness-score — LLM-Judge Multi-Dimensional Fitness Scoring

Score a skill on 5 quality dimensions using an LLM-Judge rubric. Produces per-dimension scores (0-10), a weighted composite score, and natural-language feedback with improvement suggestions. Designed as a pre-evolution diagnostic that feeds into `hermes-skill-evolver`. See [Fitness-Score Workflow](#fitness-score-workflow) below.

---

## Audit Workflow

### Step 1: Discover Skills

Find all `SKILL.md` files under the target directory:

```bash
find <SKILLS_DIR> -name "SKILL.md" -type f | sort
```

For each skill, record:
- Full path to SKILL.md
- Line count (`wc -l`)
- Existing subdirectories (`references/`, `scripts/`, `assets/`)

### Step 2: Audit Each Skill

Read each SKILL.md and evaluate against the checklist in [references/audit-checklist.md](references/audit-checklist.md) across 7 categories:

1. **Frontmatter** — name, description (WHAT + WHEN + negative triggers), metadata
2. **Progressive Disclosure** — body under 500 lines, large blocks extracted to references/
3. **Structure** — Examples section, Error Handling section, no README.md in folder
4. **Composability** — self-contained, no cross-skill assumptions
5. **Accuracy** — all referenced files/skills actually exist
6. **Redundancy** — no duplicated content, no redundant fetches
7. **Content Design Pattern** — classify as Tool Wrapper / Generator / Reviewer / Inversion / Pipeline; verify pattern-specific structural requirements (see [references/anthropic-best-practices.md](references/anthropic-best-practices.md) Section 10)
8. **Session Separation** — if the skill processes multiple items (batch loops, list iteration, multi-file scans), verify it dispatches each item to an isolated subagent via Task tool. Flag skills that iterate over content items in a single session context without per-item subagent isolation as HIGH severity ("Multi-item processing without session separation — context contamination risk")

For description quality assessment, see [references/frontmatter-patterns.md](references/frontmatter-patterns.md) for good/bad examples and templates.

### Step 3: Generate Gap Report

Present findings per skill in this format:

```
Skill Audit Report
===================
Skill: [name]
Path:  [path]
Lines: [N]

[CRITICAL] Missing negative triggers in description
[HIGH]     SKILL.md body exceeds 500 lines (currently 623)
[HIGH]     References 12 non-existent skills in registry
[MEDIUM]   No ## Examples section
[LOW]      Missing metadata field (author, version)

Summary: [N] critical, [N] high, [N] medium, [N] low
```

Severity definitions:
- **Critical** — Skill will malfunction (missing frontmatter, phantom references causing failures)
- **High** — Violates core Anthropic guide principles (progressive disclosure, over/under-triggering)
- **Medium** — Missing recommended sections (examples, troubleshooting)
- **Low** — Missing optional fields (metadata), minor style issues

Ask the user for confirmation before proceeding to Step 4.

### Step 4: Apply Fixes

For each finding, apply the appropriate fix:

| Finding | Fix |
|---------|-----|
| Missing negative triggers | Add "Do NOT use for..." clause to description |
| Missing metadata | Add `metadata:` with author/version |
| Body over 500 lines | Extract large blocks (JSON schemas, command lists, tables) to `references/` |
| Missing Examples section | Add `## Examples` with 1-2 trigger-action-result examples |
| Missing Error Handling | Add `## Error Handling` or `## Troubleshooting` section |
| Phantom file/skill references | Remove or mark as "planned/unavailable" |
| Redundant content | Remove duplicated sections, keep single source of truth |
| "When to Use" in body | Remove — this belongs in frontmatter description only |
| Redundant external fetch | Remove if the fetched data is already embedded in the skill |

When extracting content to `references/`:
1. Create the `references/` directory if it doesn't exist
2. Move the content to a descriptively named `.md` file
3. Replace the original content with a link: `For [topic], see [references/audit-checklist.md](references/audit-checklist.md)` (use the actual created filename)

### Step 5: Verify

Re-audit all modified skills:

```bash
wc -l <SKILLS_DIR>/*/SKILL.md
```

Confirm:
- All SKILL.md files under 500 lines
- All `references/` files properly linked from SKILL.md
- No phantom references remain
- No XML angle brackets in frontmatter
- Folder names remain kebab-case

Present a before/after summary:

```
Optimization Summary
====================
Skills audited:  [N]
Findings fixed:  [N] / [N]
Files created:   [list of new references/ files]
Files modified:  [list of modified SKILL.md files]

Per-skill line counts:
  [skill-name]: [before] → [after] lines ([reduction]%)
```

---

## Eval Workflow

### Step 1: Select Target Skill

Read the target skill's SKILL.md and identify:
- Trigger conditions (from frontmatter description)
- Expected behavioral changes (what the skill should cause)
- Anti-behaviors (what the skill should prevent)

### Step 2: Define Test Cases

For each skill, define 3-5 test cases. Auto-generate from the skill description if the user doesn't provide them. See [references/eval-framework.md](references/eval-framework.md) for the test case format.

Each test case needs:
- A realistic user prompt that should trigger the skill
- Evaluation criteria (what to check in the output)
- Expected behavior and anti-behavior

### Step 3: Execute with Subagents

Launch two parallel Task subagents per test case:

1. **Executor WITH skill** — prompt includes: "You have access to this skill: [full SKILL.md content]. Now handle this request: [test prompt]"
2. **Executor WITHOUT skill** — prompt includes only: "Handle this request: [test prompt]"

Both subagents return their full output.

### Step 4: Grade Results

Launch a **Grader subagent** for each test case with:
- The evaluation criteria
- Both outputs (labeled "with-skill" and "without-skill")
- Instructions to score each output 1-10 per criterion and provide pass/fail

### Step 5: Present Eval Report

Use the report template in [references/eval-report-template.md](references/eval-report-template.md):

```
Skill Eval Report
=================
Skill: [name]
Test cases: [N]
Pass rate:  [N]% (with skill) vs [N]% (without skill)

Per-test results:
  [test-name]: PASS/FAIL — score [N]/10 — [one-line reason]

Skill impact: [positive/neutral/negative]
Recommendation: [keep / improve / retire]
```

---

## Benchmark Workflow

Run the eval workflow N times (default: 3) and collect statistical metrics. See [references/benchmark-protocol.md](references/benchmark-protocol.md) for the full protocol.

### Step 1: Configure

- Target skill name
- Test cases (from eval or user-provided)
- Number of iterations (default: 3)

### Step 2: Execute

Run the eval workflow for each iteration, collecting per-run:
- Pass/fail per test case
- Quality score (1-10)
- Output token count
- Elapsed time (from subagent metadata)

### Step 3: Analyze

Calculate and present:
- **Pass rate**: % of test cases passing across all iterations
- **Mean quality score**: average across iterations
- **Consistency index**: 1 - (standard deviation / mean score)
- **Token efficiency**: mean tokens / mean quality score
- **Regression flag**: if previous benchmark exists, flag score drops > 10%

---

## Compare Workflow

A/B blind comparison between two skill versions. See [references/comparator-protocol.md](references/comparator-protocol.md) for the full protocol.

### Step 1: Configure

User provides one of:
- Two skill file paths (version comparison)
- One skill path + "no-skill" flag (skill vs baseline)

### Step 2: Execute

For each test case:
1. Run Executor subagent with Version A
2. Run Executor subagent with Version B
3. Strip any skill-identifying references from both outputs

### Step 3: Blind Judge

Launch a **Comparator subagent** with:
- Two anonymized outputs labeled "Output A" and "Output B"
- Evaluation criteria
- Instructions: judge which is better per criterion, provide confidence (1-5), explain reasoning

The Comparator does NOT know which output came from which version.

### Step 4: Reveal and Report

De-anonymize results and present:

```
A/B Comparison Report
=====================
Skill: [name]
Versions: [A label] vs [B label]

Comparator verdict:
  [criterion]: Winner=[A/B/Tie] Confidence=[1-5] — [reason]

Overall winner: [A/B/Tie]
Win rate: Version A [N]% — Version B [N]%
```

---

## Fitness-Score Workflow

Score a skill across 5 weighted dimensions using an LLM-Judge prompt. This mode does not mutate the skill — it produces a diagnostic report that serves as input for `hermes-skill-evolver` or manual improvement.

### Invocation

```
skill-optimizer fitness-score <skill-path>
```

Options:
- `--output json|markdown` — Output format (default: markdown)
- `--eval-inputs file.json` — Optional test inputs to ground scoring in actual outputs rather than static analysis

### 5-Dimension Rubric

Each dimension is scored 0-10 by an LLM-Judge subagent with structured output.

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| **ACCURACY** | 30% | Factual correctness of instructions, absence of hallucinated tool names or nonexistent APIs, alignment of described workflow with actual project structure |
| **PROCEDURE** | 25% | Completeness of step-by-step workflow, logical ordering, presence of verification/checkpoint steps, error handling guidance |
| **CONCISENESS** | 15% | Information density; absence of redundant text, boilerplate, or filler paragraphs; every sentence earns its place |
| **TRIGGER_PRECISION** | 15% | Specificity and completeness of "Use when" triggers; absence of false-positive triggers; coverage of Korean trigger phrases; clear "Do NOT use" boundaries that prevent misrouting |
| **BOUNDARY_CLARITY** | 15% | Unambiguous delineation of scope; each "Do NOT use" entry names a specific alternative skill; no overlapping responsibility with sibling skills |

### Composite Score

```
composite = Σ (dimension_score × weight)
```

Range: 0.0 – 10.0. Interpretation:

| Range | Grade | Meaning |
|-------|-------|---------|
| 9.0 – 10.0 | A | Production-ready, minimal improvement needed |
| 7.0 – 8.9 | B | Good quality, targeted improvements recommended |
| 5.0 – 6.9 | C | Functional but needs significant work on weak dimensions |
| 3.0 – 4.9 | D | Below threshold — should not be used in production without rework |
| 0.0 – 2.9 | F | Fundamentally broken — consider rewriting from scratch |

### Scoring Process

1. **Read the target SKILL.md** — Parse frontmatter, description, triggers, constraints, and body.
2. **Spawn LLM-Judge subagent** — Pass the full skill text plus the 5-dimension rubric as structured evaluation criteria.
3. **Score each dimension** — The judge assigns a 0-10 score with a 1-2 sentence justification per dimension.
4. **Generate feedback** — For each dimension scoring below 7, produce specific, actionable improvement suggestions.
5. **Compute composite** — Apply weights, assign letter grade.
6. **Output report** — Structured report with per-dimension breakdown, composite score, and improvement roadmap.

### Output Format

```
Fitness Score Report
====================
Skill: [name]
Path: [skill-path]
Date: [ISO date]

Dimension Scores:
  ACCURACY (30%):         [score]/10 — [justification]
  PROCEDURE (25%):        [score]/10 — [justification]
  CONCISENESS (15%):      [score]/10 — [justification]
  TRIGGER_PRECISION (15%): [score]/10 — [justification]
  BOUNDARY_CLARITY (15%): [score]/10 — [justification]

Composite: [weighted score]/10.0 (Grade: [A-F])

Improvement Suggestions:
  [dimension]: [actionable suggestion]
  ...

Integration:
  Feed this report into `hermes-skill-evolver` to auto-evolve weak dimensions.
  Run `skill-autoimprove --target <path>` for iterative single-mutation improvement.
```

### JSON Output (`--output json`)

```json
{
  "skill": "[name]",
  "path": "[skill-path]",
  "timestamp": "[ISO 8601]",
  "dimensions": {
    "accuracy": { "score": 8, "weight": 0.30, "justification": "..." },
    "procedure": { "score": 7, "weight": 0.25, "justification": "..." },
    "conciseness": { "score": 6, "weight": 0.15, "justification": "..." },
    "trigger_precision": { "score": 9, "weight": 0.15, "justification": "..." },
    "boundary_clarity": { "score": 8, "weight": 0.15, "justification": "..." }
  },
  "composite": 7.65,
  "grade": "B",
  "suggestions": [
    { "dimension": "conciseness", "suggestion": "..." }
  ]
}
```

### Integration Points

- **Pre-evolution diagnostic**: Run `fitness-score` before `hermes-skill-evolver` to identify which dimensions need improvement, guiding the evolution toward targeted mutations.
- **Batch scoring**: Run `fitness-score` on all skills in a directory to produce a portfolio-level quality heatmap.
- **Regression guard**: Run after `skill-autoimprove` or `hermes-skill-evolver` to verify that evolution improved the target dimensions without regressing others.

---

## Examples

### Example 1: Full directory audit

User says: "Optimize all my skills"

Actions:
1. Discover skills in `.cursor/skills/`
2. Audit: find issues (critical/high/medium/low)
3. Present gap report, user confirms
4. Apply fixes: update SKILL.md files, create references/ files as needed
5. Verify: all under 500 lines, all references linked

Result: Optimized skills with progressive disclosure, negative triggers, and examples

### Example 2: Eval a specific skill

User says: "Evaluate my doc-quality-gate skill"

Actions:
1. Read doc-quality-gate SKILL.md, extract trigger/behavior expectations
2. Auto-generate 4 test cases from description
3. Run Executor subagents WITH and WITHOUT skill
4. Grade outputs against criteria
5. Present eval report: pass rate and skill impact

Result: Quantified evidence that the skill improves agent behavior on the test cases

### Example 3: Compare skill versions

User says: "Compare my old and new prd-research-factory skill"

Actions:
1. Load both versions of SKILL.md
2. Run 3 test prompts through both versions
3. Comparator blind-judges all outputs
4. De-anonymize and report wins/ties

Result: Evidence-based decision to ship the new version

### Example 4: Fitness-score a skill before evolution

User says: "Fitness score my daily-stock-check skill"

Actions:
1. Read `.cursor/skills/trading/daily-stock-check/SKILL.md`
2. Spawn LLM-Judge subagent with 5-dimension rubric
3. Score each dimension: ACCURACY=8, PROCEDURE=7, CONCISENESS=5, TRIGGER_PRECISION=9, BOUNDARY_CLARITY=7
4. Compute composite: 7.35 (Grade B)
5. Generate suggestions for CONCISENESS: "Remove redundant strategy descriptions already covered in referenced skills"
6. Present report with integration guidance

Result: Diagnostic report showing CONCISENESS as the weakest dimension, ready to feed into `hermes-skill-evolver` for targeted evolution

## Error Handling

| Error | Action |
|-------|--------|
| Skills directory not found | Ask user for the correct path |
| SKILL.md missing `---` delimiters | Flag as Critical; add delimiters and minimal frontmatter |
| YAML parse error in frontmatter | Show the malformed YAML and suggest fix |
| References directory creation fails | Report error and continue with other skills |
| No skills found | Inform user that no SKILL.md files were found in the target directory |
| Subagent timeout during eval | Report timeout, skip test case, continue with remaining |
| Insufficient test cases | Auto-generate from skill description with user confirmation |
| Previous benchmark not found | Skip regression check, establish current run as baseline |

## Further reference

- Trigger description tuning: [references/trigger-optimization.md](references/trigger-optimization.md)
- Scoring rubric: [references/optimization-checklist.md](references/optimization-checklist.md)
- ADK / portable skill layout: [references/adk-compatibility.md](references/adk-compatibility.md)


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
