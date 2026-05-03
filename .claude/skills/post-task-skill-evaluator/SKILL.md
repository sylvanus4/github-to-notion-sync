---
name: post-task-skill-evaluator
description: >-
  Evaluate completed tasks for skill extraction suitability using a
  5-dimension scoring rubric (Reusability, Complexity, Non-Googleability,
  Uniqueness, Hard-Won Knowledge). Scores each dimension 1-5, computes a
  weighted composite, and routes approved candidates to create-skill (new) or
  autoskill-merger (overlap). Designed as a post-task checkpoint — invoke
  after any significant task completes. Use when the user asks to "evaluate
  this task for skill", "should this be a skill", "skill suitability check",
  "post-task evaluation", "task to skill check", "post-task-skill-evaluator",
  "이 작업 스킬로 만들까", "스킬 적합성 평가", "작업 완료 후 스킬 체크", "완료 작업 스킬 판정", "작업 평가", "스킬화
  판단", or after completing a non-trivial task. Do NOT use for evaluating
  existing SKILL.md file quality (use skill-optimizer). Do NOT use for
  autonomous prompt mutation loops (use skill-autoimprove). Do NOT use for
  extracting patterns from transcripts without a just-completed task (use
  autoskill-extractor or cursor-skill-factory). Do NOT use for creating skills
  from external repos (use skill-seekers or
  selective-external-github-to-project-skills).
---

# Post-Task Skill Evaluator

Checkpoint gate that answers: **"Should the task I just completed become a
reusable skill?"**

## When to Use

- After completing any multi-step task (3+ tool calls)
- After a significant debugging session that uncovered non-obvious knowledge
- After building a new pipeline, workflow, or integration
- After adapting an external tool/repo for internal use
- When `cursor-skill-factory` routes a proposal for structured evaluation
- When post-task-reflection.mdc suggests skill extraction

## Step 0: Short-Circuit Check

Before running the full rubric, check if the task is obviously trivial:

- **< 3 tool calls** in the session → SKIP immediately, no report needed
- **Single-file edit only** (typo fix, config change) → SKIP
- **Pure Q&A** (no artifacts produced) → SKIP
- **Already evaluated** in this session → SKIP

If any short-circuit condition matches, output a one-line note and stop:
> "Short-circuit: {reason}. Skipping skill evaluation."

## Step 1: Capture Task Summary

Extract from the current session:

```yaml
task_name: "brief descriptive name"
task_type: "pipeline | integration | debugging | analysis | automation | content"
steps_taken: 7
tools_used: ["WebFetch", "Read", "Write", "Shell", "Grep"]
duration_estimate: "30 minutes"
key_decisions:
  - "decision 1 and rationale"
  - "decision 2 and rationale"
artifacts_produced:
  - "path/to/file1"
  - "path/to/file2"
reusable_patterns:
  - "pattern description"
```

## Step 2: Score with 5-Dimension Rubric

Rate each dimension 1-5, then compute the weighted composite.

### Dimension 1: Reusability (weight: 0.25)

> "Will this exact workflow be needed again?"

| Score | Criteria |
|-------|----------|
| 1 | One-off task, will never repeat |
| 2 | Might repeat once in 6 months |
| 3 | Repeats monthly or across projects |
| 4 | Repeats weekly or is a standard operating procedure |
| 5 | Repeats daily or is a core workflow primitive |

### Dimension 2: Complexity (weight: 0.20)

> "Is there enough complexity to warrant a skill?"

| Score | Criteria |
|-------|----------|
| 1 | Single tool call, trivial |
| 2 | 2-3 steps, straightforward |
| 3 | 4-6 steps with conditional logic |
| 4 | 7-10 steps with branching or error handling |
| 5 | 10+ steps, multi-phase pipeline with dependencies |

### Dimension 3: Non-Googleability (weight: 0.25)

> "Could someone reproduce this from a Stack Overflow answer?"

| Score | Criteria |
|-------|----------|
| 1 | Standard tutorial content, well-documented |
| 2 | Common pattern with a slight twist |
| 3 | Requires combining 3+ sources of documentation |
| 4 | Requires codebase-specific knowledge not in docs |
| 5 | Requires hard-won debugging insight or undocumented behavior |

### Dimension 4: Uniqueness (weight: 0.15)

> "Does an existing skill already cover this?"

| Score | Criteria |
|-------|----------|
| 1 | Existing skill handles this exactly |
| 2 | Existing skill handles 70%+ of this |
| 3 | Existing skill handles ~50%, gaps are significant |
| 4 | Existing skill handles < 30%, mostly novel |
| 5 | No existing skill covers this capability |

### Dimension 5: Hard-Won Knowledge (weight: 0.15)

> "Did this task produce insights that were non-obvious before starting?"

| Score | Criteria |
|-------|----------|
| 1 | No surprises, everything worked as expected |
| 2 | Minor gotcha discovered |
| 3 | Significant workaround required |
| 4 | Multiple iterations needed to find the right approach |
| 5 | Fundamental insight that changes how we approach similar problems |

## Step 3: Compute Composite Score

```
composite = (reusability × 0.25) + (complexity × 0.20) +
            (non_googleability × 0.25) + (uniqueness × 0.15) +
            (hard_won × 0.15)
```

### Decision Thresholds

| Composite | Decision | Action |
|-----------|----------|--------|
| ≥ 3.5 | **CREATE** | Route to `create-skill` for full SKILL.md generation |
| 2.5 – 3.4 | **MERGE** | Route to `autoskill-merger` to enrich an existing skill |
| < 2.5 | **SKIP** | Log the evaluation but do not create a skill |

## Step 4: Overlap Check

Before routing to CREATE:

1. Search all `.cursor/skills/**/SKILL.md` descriptions for semantic overlap
2. Check trigger phrases for collision
3. If overlap > 60% with an existing skill, downgrade to MERGE regardless of score

## Step 5: Output Report

Present the evaluation to the user:

```markdown
## Post-Task Skill Evaluation

**Task**: {task_name}
**Type**: {task_type}

### Scores
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Reusability | {1-5} | {why} |
| Complexity | {1-5} | {why} |
| Non-Googleability | {1-5} | {why} |
| Uniqueness | {1-5} | {why} |
| Hard-Won Knowledge | {1-5} | {why} |

**Composite**: {score} → **{CREATE / MERGE / SKIP}**

### Overlap Check
- Nearest skill: {skill_name} ({overlap}%)
- Final decision: {CREATE / MERGE / SKIP}

### Recommended Skill Outline (if CREATE)
- Name: {proposed-skill-name}
- Category: {category}
- Key triggers: {3-5 trigger phrases}
- Workflow: {3-5 high-level steps}
```

## Step 6: Route

Based on the decision:

- **CREATE**: Invoke `create-skill` with the recommended outline as input
- **MERGE**: Invoke `autoskill-merger` with the target skill and new capabilities
- **SKIP**: Record the evaluation in the session transcript for future reference

## Rationalization Red Flags

If you catch yourself thinking any of these during scoring, you are inflating:

| Thought | Reality |
|---------|---------|
| "This could be useful someday" | Score Reusability based on evidence, not hope |
| "It was hard work so it deserves a high score" | Effort ≠ skill-worthiness. Score each dimension independently |
| "We should capture this before we forget" | That's what `omc-learner` and session transcripts are for |
| "Close enough to 3.5, let's round up" | Thresholds are hard gates. 3.4 = MERGE, not CREATE |
| "The user would want this as a skill" | Present the scores honestly and let the user decide |

## Constraints

- **Never auto-create skills** — always present the evaluation report first
- **Honest scoring** — resist inflating scores to justify skill creation
- **One evaluation per task** — do not re-evaluate the same task unless new evidence appears
- **Dimension independence** — score each dimension without being influenced by others
- **Minimum data** — require at least a task summary and list of steps before scoring

## Freedom Level

**RIGID** — Follow the scoring rubric exactly. Do not skip dimensions or override the composite score threshold.

## Gotchas

- Tasks that feel impressive may score low on Reusability (one-off heroics)
- Simple tasks that repeat daily may score high despite low Complexity
- A high Uniqueness score with low Reusability = interesting but not skill-worthy
- If the user says "skip", respect it — do not re-evaluate unless explicitly asked
- Debugging sessions often score high on Hard-Won but low on Reusability — look for
  the generalizable pattern, not the specific bug fix

## Integration Points

| Skill | Relationship |
|-------|-------------|
| `cursor-skill-factory` | Factory detects patterns → Evaluator scores candidates |
| `create-skill` | Evaluator routes CREATE decisions here |
| `autoskill-merger` | Evaluator routes MERGE decisions here |
| `autoskill-judge` | Complementary — judge evaluates transcript-mined candidates; evaluator evaluates just-completed tasks |
| `omc-learner` | Complementary — learner captures insights during session; evaluator scores after task completion |
| `post-task-reflection.mdc` | Rule suggests skill evaluation; this skill performs it |
| `skill-optimizer` | After creation, optimizer can audit the generated skill's quality |

## Example: Evaluating a Repo-to-Skills Adaptation Task

**Task**: Analyzed hermes-skill-factory GitHub repo and created two Cursor-native skills

**Scores**:
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Reusability | 4 | Adapting external repos to internal skills is a recurring need |
| Complexity | 4 | 5-phase pipeline with gap analysis and format adaptation |
| Non-Googleability | 4 | Requires knowledge of our specific skill ecosystem and conventions |
| Uniqueness | 4 | `skill-seekers` handles doc sites; this covers the evaluate+adapt pattern |
| Hard-Won Knowledge | 3 | Discovered integration points between 8+ existing skills |

**Composite**: 3.85 → **CREATE**

**Recommended Skill**: `external-repo-skill-adapter` — analyze external repos,
perform gap analysis against installed skills, and generate adapted SKILL.md files.

## Anti-Example: When NOT to Create a Skill

**Task**: Fixed a typo in a config file and restarted the dev server.

**Scores**:
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Reusability | 1 | One-off fix, unlikely to recur |
| Complexity | 1 | Single line change |
| Non-Googleability | 1 | Any developer could find this |
| Uniqueness | 1 | No existing skill overlap because it's trivial |
| Hard-Won Knowledge | 1 | No debugging effort required |

**Composite**: 1.00 → **SKIP**

This is the correct outcome. Trivial tasks should never become skills — they add noise
to the skill library and increase trigger collision risk. The evaluator should recognize
low scores early and short-circuit without producing a full report.
