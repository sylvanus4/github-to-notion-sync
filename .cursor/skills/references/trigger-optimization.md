# Trigger Optimization Protocol

Test whether a skill activates on the right prompts, then iteratively improve the description until trigger accuracy is maximized. Adapted from Anthropic's Skill Creator 2.0 description optimization pipeline for Cursor's Task subagent system.

## Table of Contents

- [Trigger Eval Query Format](#trigger-eval-query-format)
- [Train/Test Split](#traintest-split)
- [Iterative Optimization Loop](#iterative-optimization-loop)
- [Description Improvement Heuristics](#description-improvement-heuristics)
- [Report Format](#report-format)
- [Error Handling](#error-handling)

## Trigger Eval Query Format

Create 15-20 eval queries as a JSON array — a mix of should-trigger and should-not-trigger:

```json
[
  {
    "query": "회의록 노션 링크 줬으니까 다이제스트랑 액션 아이템 정리해줘",
    "should_trigger": true,
    "note": "meeting-digest core use case"
  },
  {
    "query": "Write a Python fibonacci function with memoization",
    "should_trigger": false,
    "note": "simple coding task — unrelated to planning skills"
  }
]
```

### Query Quality Standards

Queries must be realistic — concrete, specific, and detailed. Include file paths, product context (Thaki Cloud), casual speech, typos, abbreviations, and varied lengths. Focus on edge cases, not clear-cut examples.

**Bad**: `"Review this code"`, `"Optimize my skill"`, `"Run tests"`

**Good**: `"hey can you check if my doc-quality-gate skill actually triggers when someone says '기획서 검수'? It used to work but after the last model update I think it's broken"`

### Should-Trigger Queries (8-10)

Cover different phrasings of the same intent: formal, casual, indirect. Include cases where the user doesn't name the skill explicitly but clearly needs it. Include cases where this skill competes with a neighbor but should win.

### Should-Not-Trigger Queries (8-10)

Prefer near-misses over obviously unrelated queries. Target adjacent domains, ambiguous phrasing where naive keyword matching would incorrectly trigger, and contexts where a different skill is more appropriate.

## Train/Test Split

Split the eval set to prevent description overfitting:

- **Train set (60%)**: Used during optimization — the Analyzer sees which queries failed and proposes description improvements based on these
- **Test set (40%)**: Held out — only used for final evaluation of each candidate description, never shown to the Analyzer

Selection is randomized. Both sets must contain a mix of should-trigger and should-not-trigger queries.

### Why Split Matters

Without a holdout set, the optimization loop will produce descriptions that memorize specific query patterns (listing exact phrases from the eval set) rather than generalizing to unseen user prompts. The test score is the true quality signal.

## Iterative Optimization Loop

### Step 1: Baseline Evaluation

Run each eval query 3 times against the current description to establish a reliable trigger rate:

For each query, launch an **Executor subagent** with:
- The skill's name and description in the system prompt as an available skill entry
- The eval query as the user prompt
- Instruction: "If any available skill is relevant, indicate which skill you would consult and why. If none are relevant, say NONE."

Score each query:
- `trigger_rate`: fraction of runs where the skill was selected (0/3, 1/3, 2/3, 3/3)
- **PASS**: trigger_rate >= 2/3 when `should_trigger: true`, or trigger_rate <= 1/3 when `should_trigger: false`
- **FAIL**: otherwise

### Step 2: Identify Failures

Collect all failing queries from the **train set only**. Classify failure types:

| Failure Type | Meaning |
|-------------|---------|
| False negative | should_trigger=true but skill was not selected |
| False positive | should_trigger=false but skill was incorrectly selected |

### Step 3: Generate Improved Description

Launch an **Analyzer subagent** with:
- The current description
- The list of failing queries (train set only) with their failure types
- Instructions:

```
Improve this skill description to fix the trigger failures listed below.
Do NOT list specific query text from the failures — that overfits.
Instead, generalize to broader categories of user intent.

Rules:
- Stay under 1024 characters
- Use imperative voice ("Use this skill for..." not "This skill is...")
- Include concrete component/domain names the skill handles
- Include trigger phrases users actually type
- Include explicit negative triggers ("Do NOT use for...")
- Be creative — try different sentence structures each iteration

Current description:
[description]

Failing queries:
[list with failure type and note]
```

The Analyzer returns a candidate description.

### Step 4: Re-evaluate

Run the full eval set (both train and test) against the candidate description using the same 3-run protocol from Step 1.

Record:
- Train score: pass rate on train set
- Test score: pass rate on test set

### Step 5: Iterate or Stop

Repeat Steps 2-4 up to 5 iterations. Stop early if any condition is met:

| Condition | Action |
|-----------|--------|
| Test score = 100% | Best possible — stop and use this description |
| Test score did not improve for 2 consecutive iterations | Plateau — stop and use best-so-far |
| Max iterations (5) reached | Stop and use the description with highest test score |

### Step 6: Apply Best Description

Select the description with the **highest test score** (not train score). If tied, prefer the shorter description. Update the skill's SKILL.md frontmatter.

## Description Improvement Heuristics

Common patterns that improve trigger accuracy:

### For false negatives (skill not triggering when it should)

| Problem | Fix |
|---------|-----|
| Description uses passive voice ("A skill that...") | Switch to imperative ("Use this skill for...") |
| Description lacks concrete nouns | Add specific things the skill handles (Notion, PRD, Figma, policy) |
| No trigger phrases | Add exact phrases users type ("회의 다이제스트", "기획서 검수") |
| Description is too abstract | Replace philosophy with use cases |

### For false positives (skill triggering when it shouldn't)

| Problem | Fix |
|---------|-----|
| Description too broad | Narrow scope with specific domains |
| Missing negative triggers | Add "Do NOT use for..." with explicit alternatives |
| Overlapping keywords with neighboring skills | Differentiate with unique action verbs and domain nouns |

### The "Pushy" Pattern

Models tend to under-trigger skills. Descriptions should be slightly "pushy" — proactively claiming edge cases. Example:

**Weak**: "Optimize agent skills for quality."

**Pushy**: "Use this skill for auditing, evaluating, benchmarking, and comparing agent skills. Make sure to use this skill whenever the user mentions skill quality, skill performance, skill testing, trigger accuracy, description optimization, or skill regression — even if they don't explicitly say 'optimize'."

## Report Format

```
Trigger Optimization Report
============================
Skill: [skill-name]
Date:  [YYYY-MM-DD]
Mode:  trigger

Eval Set: [N] queries ([N] should-trigger, [N] should-not-trigger)
Split:    [N] train / [N] test

Iteration Results
─────────────────
┌───────────┬─────────────┬────────────┬─────────────────────────────────┐
│ Iteration │ Train Score │ Test Score │ Description (first 80 chars)    │
├───────────┼─────────────┼────────────┼─────────────────────────────────┤
│ 0 (base)  │ [N]%        │ [N]%       │ [truncated current desc...]     │
│ 1         │ [N]%        │ [N]%       │ [truncated candidate desc...]   │
│ 2         │ [N]%        │ [N]%       │ [truncated candidate desc...]   │
│ ...       │ ...         │ ...        │ ...                             │
└───────────┴─────────────┴────────────┴─────────────────────────────────┘

Best Description (by test score)
────────────────────────────────
Iteration: [N]
Test score: [N]%
Train score: [N]%
Exit reason: [all_passed / plateau / max_iterations]

Description:
[full best description text]

Before/After
────────────
Original test score: [N]% → Best test score: [N]%
Improvement: +[N] percentage points

Failing Queries (if any remain)
───────────────────────────────
  - [query summary]: expected [trigger/no-trigger], got [rate]
```

## Error Handling

| Error | Action |
|-------|--------|
| Eval set has fewer than 10 queries | Warn user; proceed but note low confidence |
| All queries in train set pass at baseline | Description may already be optimal — run test set only and report |
| Analyzer returns description over 1024 chars | Truncate and re-run, or ask Analyzer to shorten |
| Executor subagent timeout | Treat as "did not trigger" for that run |
| No improvement after 5 iterations | Report best result with note that manual description editing may help |
| Test set has zero should-trigger or zero should-not-trigger queries | Warn: unbalanced split will skew results |
