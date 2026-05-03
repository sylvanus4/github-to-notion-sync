---
name: autoreason
description: >-
  Generic 3-way tournament self-refinement engine inspired by
  NousResearch/autoreason. Iterates Critic → Author B → Synthesizer → Blind
  Judge Panel rounds until the incumbent A survives k consecutive rounds
  (convergence). Each role is a fresh isolated subagent with no shared
  context. Judging uses Borda count with randomized labels to prevent position
  bias and sycophantic feedback loops. Use when the user asks to "autoreason",
  "tournament refine", "adversarial refinement", "blind tournament", "3-way
  tournament", "self-refine with competition", "오토리즌", "토너먼트 정제", "적대적 정제",
  "블라인드 토너먼트", "3자 토너먼트", "자기 정제 경쟁", or wants iterative adversarial
  self-refinement of any text artifact (copy, specs, policies, proposals,
  reports) beyond simple "make it better" prompting. Do NOT use for
  single-mutation iterative prompt optimization (use skill-autoimprove). Do
  NOT use for population-based multi-variant evolution of SKILL.md files (use
  hermes-skill-evolver). Do NOT use for evaluator-optimizer 2-party loops
  without adversarial competition (use workflow-eval-opt). Do NOT use for
  scoring finished content without refinement (use marketing-content-ops or
  ai-quality-evaluator). Do NOT use for marketing-specific refinement with
  Knowledge Layer (use marketing-autoreason).
---

# Autoreason — 3-Way Tournament Self-Refinement Engine

Iterative self-refinement where each round produces three competing versions — the unchanged incumbent **A**, an adversarial revision **B**, and a synthesis **AB** — judged blindly by a fresh panel using Borda count. The incumbent advantage ("do nothing" is a first-class option) prevents gratuitous churn. Convergence occurs when A survives k consecutive rounds, meaning the output is truly stable.

Adapted from [NousResearch/autoreason](https://github.com/NousResearch/autoreason). Where standard self-refinement degrades output by hallucinating flaws and expanding scope, autoreason builds in disagreement: Author B competes with A, judges are blind, and convergence is earned.

---

## When to Use This vs Alternatives

| Scenario | Skill |
|----------|-------|
| Adversarial 3-way tournament refinement of any content | **autoreason** (this) |
| Marketing-specific refinement with KB data + marketing rubric | `marketing-autoreason` |
| Single-mutation iterative prompt optimization for SKILL.md | `skill-autoimprove` |
| Population-based multi-variant SKILL.md evolution | `hermes-skill-evolver` |
| 2-party generate-evaluate loop (no adversarial competition) | `workflow-eval-opt` |
| Scoring finished content without refinement | `marketing-content-ops`, `ai-quality-evaluator` |

---

## Configurable Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_passes` | 15 | Maximum tournament rounds |
| `convergence_k` | 2 | Consecutive A-wins required to converge |
| `num_judges` | 3 | Judge panel size (7 = ~3x faster convergence per paper) |
| `author_model` | inherit parent | Model for Critic / Author B / Synthesizer subagents |
| `judge_model` | `fast` | Model for judge subagents (cost-efficient) |
| `knowledge_context` | `""` | Optional markdown injected into all agent prompts (Knowledge Layer hook) |
| `rubric_dimensions` | `[]` | Optional evaluation dimensions for judges (e.g., Clarity, Accuracy, Tone) |
| `output_dir` | `outputs/autoreason/{timestamp}/` | Artifact persistence directory |
| `max_size_multiplier` | 2.0 | Anti-scope-creep: output must not exceed this × initial word count |
| `max_growth_rate` | 0.30 | Anti-scope-creep: per-pass winner growth cap vs previous A |

---

## Constraints

- **Freedom level: Medium** — structured procedure with configurable parameters, but flexible on content domain.
- Every agent role (Critic, Author B, Synthesizer, Judge) MUST be a separate `Task` subagent call. No role reuses another's context.
- Judges MUST receive randomized labels (Proposal 1/2/3). The mapping MUST be saved for result interpretation.
- Borda ties are broken in favor of A (incumbent advantage).
- Do NOT continue past `max_passes` even if convergence has not been reached.
- Do NOT skip the anti-scope-creep gate check — discard versions exceeding the growth limit before judging.
- All intermediate artifacts MUST be persisted to `output_dir` per phase (see Output Artifacts table).

---

## Procedure

### Step 0: Initialize

1. Accept `task_prompt` (required) and `initial_draft` (optional) from the user.
2. If no `initial_draft` is provided, generate one using a single LLM call with `task_prompt`.
3. Create the output directory: `outputs/autoreason/{timestamp}/`.
4. Save `initial_a.md` to the output directory.
5. Set `streak = 0`, `pass_num = 1`, `current_a = initial_draft`.
6. Record initial word count for anti-scope-creep gate: `initial_wc = word_count(current_a)`.

### Step 1: Critic (fresh subagent)

1. Read `references/prompts.md` for the Critic prompt template.
2. Read `references/agent-dispatch-patterns.md` for Task tool dispatch pattern.
3. Dispatch a **fresh** subagent via `Task` tool:
   - `subagent_type: generalPurpose`
   - Prompt includes: Critic system prompt + current A + `knowledge_context` (if provided)
   - **Instruction**: Find genuine weaknesses only. Do NOT suggest fixes. Do NOT hallucinate problems.
4. Receive critique text.
5. Save to `pass_{n}/critic.md`.

### Step 2: Author B (fresh subagent)

1. Read `references/prompts.md` for the Author B prompt template.
2. Dispatch a **fresh** subagent via `Task` tool:
   - `subagent_type: generalPurpose`
   - Prompt includes: Author B system prompt + `task_prompt` + current A + critique from Step 1 + `knowledge_context`
   - **Critical**: Author B sees BOTH current A and the critique (faithful to the paper's `AUTHOR_B_PROMPT`).
   - **Instruction**: Address each valid criticism directly. Do not make changes unmotivated by an identified problem.
3. Receive revision B text.
4. **Anti-scope-creep gate**: Check `word_count(B)` against limits. If `> initial_wc * max_size_multiplier` OR `> word_count(current_a) * (1 + max_growth_rate)`, discard B and mark as `GATE_FAILED`.
5. Save to `pass_{n}/version_b.md`.

### Step 3: Synthesizer (fresh subagent)

1. Read `references/prompts.md` for the Synthesizer prompt template.
2. **Randomize presentation order**: Flip a coin to assign A → "Version X" or "Version Y", B → the other. Record the mapping.
3. Dispatch a **fresh** subagent via `Task` tool:
   - `subagent_type: generalPurpose`
   - Prompt includes: Synthesizer system prompt + `task_prompt` + Version X + Version Y + `knowledge_context`
   - **Instruction**: Take the strongest elements from each version. This is NOT a compromise — pick the best approach per dimension.
4. Receive synthesis AB text.
5. **Anti-scope-creep gate**: Same check as Step 2. If failed, discard AB and mark as `GATE_FAILED`.
6. Save to `pass_{n}/version_ab.md`.
7. If BOTH B and AB are `GATE_FAILED`, increment `streak` by 1 (A wins by default), skip to Step 5.

### Step 4: Judge Panel (N parallel fresh subagents)

1. Read `references/prompts.md` for the Judge prompt template.
2. Read `references/borda-scoring.md` for scoring algorithm.
3. Collect surviving candidates (A + non-GATE_FAILED versions of B and AB).
4. For each of the `num_judges` judges:
   a. Generate a unique random ordering of the surviving candidates.
   b. Assign anonymous labels: "Proposal 1", "Proposal 2", ("Proposal 3" if 3 candidates).
   c. Record the label → original mapping in `pass_{n}/judge_{j}_order.json`.
5. Dispatch **all judges in parallel** via concurrent `Task` tool calls:
   - `subagent_type: generalPurpose`, `model: fast`, `readonly: true`
   - Prompt includes: Judge system prompt + `task_prompt` + anonymized proposals + `rubric_dimensions` (if any) + `knowledge_context`
   - Required output format: `RANKING: [best], [second], [worst]` using proposal labels.
6. Parse each judge's ranking output.
7. Save each judge's response: `pass_{n}/judge_{j}_response.md`.

### Step 5: Aggregate + Decide

1. Map each judge's rankings back to original labels (A/B/AB) using the saved order mappings.
2. Compute Borda scores: 1st place = 3 points, 2nd = 2, 3rd = 1.
   - If only 2 candidates survived gates: 1st = 2, 2nd = 1.
3. Determine winner = candidate with highest Borda score.
   - **Tie-breaking rule**: A wins ties (incumbent advantage = "do nothing" is first-class).
4. Update state:
   - If winner == A: `streak += 1`
   - Else: `streak = 0`, `current_a = winner_text` (the winner's full text becomes the new A)
5. Save `pass_{n}/result.json` with: winner label, Borda scores, judge details, streak, gate statuses.
6. **Convergence check**: If `streak >= convergence_k` → proceed to Step 6.
7. **Max passes check**: If `pass_num >= max_passes` → proceed to Step 6.
8. Else: `pass_num += 1`, return to Step 1.

### Step 6: Output

1. Save `final_output.md` with the converged (or best-so-far) text.
2. Save `history.json` with the full tournament trajectory:
   - Per-pass: winner, scores, candidates, gate failures
   - Trajectory string (e.g., `"B → AB → A → A → CONVERGED"`)
   - Total passes, convergence status, final streak
3. Report to the user:
   - Final text
   - Convergence status (converged at pass N vs hit max_passes)
   - Tournament trajectory
   - Total passes and Borda score history

---

## Output Artifacts

| Phase | Stage | Output File | Description |
|-------|-------|-------------|-------------|
| 0 | Initialize | `initial_a.md` | Starting draft |
| 1-5 | Per pass | `pass_{n}/critic.md` | Critique of current A |
| 1-5 | Per pass | `pass_{n}/version_b.md` | Adversarial revision |
| 1-5 | Per pass | `pass_{n}/version_ab.md` | Synthesis of A and B |
| 1-5 | Per pass | `pass_{n}/judge_{j}_response.md` | Each judge's ranking response |
| 1-5 | Per pass | `pass_{n}/judge_{j}_order.json` | Label → original mapping |
| 1-5 | Per pass | `pass_{n}/result.json` | Winner, Borda scores, streak |
| 6 | Final | `final_output.md` | Converged output text |
| 6 | Final | `history.json` | Full tournament trajectory |

---

## Error Recovery

- If a Critic/Author B/Synthesizer subagent fails, retry once. On second failure, skip that role for this pass (A wins the pass by default).
- If a Judge subagent fails, exclude that judge from Borda aggregation (quorum = at least 2 judges must respond).
- If all judges fail, A wins the pass by default.
- Recovery always resumes from the last `pass_{n}/result.json` on disk.

---

## Gotchas

- **Author B prompt must include current A**: The paper explicitly includes A in Author B's context so B can make targeted improvements. Omitting A makes B a blind rewrite, not an adversarial revision.
- **Randomize judge orderings independently**: Each judge must get a DIFFERENT random ordering. If all judges see the same order, position bias affects all rankings identically.
- **Parse RANKING strictly**: Judges sometimes output prose before the ranking line. Extract only the `RANKING: [x], [y], [z]` line. If unparseable after one retry, exclude that judge.
- **Scope creep is the #1 failure mode**: The paper shows that without anti-scope-creep gates, outputs bloat significantly after 10+ passes. Always enforce the growth rate check.
- **Convergence ≠ quality plateau**: Early convergence (pass 2-3) may indicate the initial draft was already strong. Very late convergence (pass 12+) may indicate over-refinement — check if the later A is actually better than the pass-5 A.

---

## References (Level 2 — load only when procedure instructs)

- `references/prompts.md` — Prompt templates for all 4 agent roles (Critic, Author B, Synthesizer, Judge)
- `references/borda-scoring.md` — Borda count algorithm, tie-breaking rules, ranking parser logic
- `references/agent-dispatch-patterns.md` — Task tool call patterns for each agent role with exact JSON structures
