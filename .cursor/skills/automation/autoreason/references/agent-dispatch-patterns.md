# Autoreason — Agent Dispatch Patterns

Exact `Task` tool call patterns for each agent role. Every role MUST be dispatched
as an isolated subagent — no role may share context with any other.

---

## Critic Agent

```json
{
  "description": "Autoreason Critic pass N",
  "subagent_type": "generalPurpose",
  "prompt": "<Critic system prompt from prompts.md>\n\n## Task Prompt\n{task_prompt}\n\n## Current Version (A)\n{current_a}\n\n## Knowledge Context\n{knowledge_context}\n\nReturn ONLY your critique. Do NOT suggest fixes or rewrites.",
  "readonly": true
}
```

**Notes:**
- `readonly: true` — Critic produces text output only, no file writes needed.
- Model inherits from parent (or uses `author_model` if configured).
- Return instruction tells the subagent to output ONLY critique text.
- `knowledge_context` block is omitted entirely when empty.

---

## Author B Agent

```json
{
  "description": "Autoreason Author B pass N",
  "subagent_type": "generalPurpose",
  "prompt": "<Author B system prompt from prompts.md>\n\n## Task Prompt\n{task_prompt}\n\n## Current Version (A)\n{current_a}\n\n## Critique of A\n{critique}\n\n## Knowledge Context\n{knowledge_context}\n\nAddress each valid criticism. Do NOT make changes unmotivated by an identified problem. Return ONLY your complete revised version."
}
```

**Notes:**
- Author B sees BOTH current A AND the critique. This is faithful to the paper's
  `AUTHOR_B_PROMPT`, which explicitly includes both so B can make targeted improvements.
- `readonly` is NOT set — Author B produces the full revised content.
- Model inherits from parent (or uses `author_model` if configured).

---

## Synthesizer Agent

```json
{
  "description": "Autoreason Synthesizer pass N",
  "subagent_type": "generalPurpose",
  "prompt": "<Synthesizer system prompt from prompts.md>\n\n## Task Prompt\n{task_prompt}\n\n## Version X\n{version_x}\n\n## Version Y\n{version_y}\n\n## Knowledge Context\n{knowledge_context}\n\nTake the strongest elements from each version. This is NOT a compromise — pick the best approach per section. Return ONLY your synthesized version."
}
```

**Notes:**
- **Input randomization is critical.** Before dispatching, randomly assign:
  - A → "Version X" or "Version Y"
  - B → the remaining label
- Record the mapping for later reference.
- This prevents the Synthesizer from developing a position bias toward the first
  version it reads.
- Model inherits from parent (or uses `author_model` if configured).

### Randomization Logic

```
coin = random_choice(["A_first", "B_first"])

if coin == "A_first":
  version_x = current_a
  version_y = version_b
  mapping = { "X": "A", "Y": "B" }
else:
  version_x = version_b
  version_y = current_a
  mapping = { "X": "B", "Y": "A" }
```

---

## Judge Agent (single)

```json
{
  "description": "Autoreason Judge J pass N",
  "subagent_type": "generalPurpose",
  "model": "fast",
  "readonly": true,
  "prompt": "<Judge system prompt from prompts.md>\n\n## Task Prompt\n{task_prompt}\n\n## Evaluation Rubric\n{rubric_dimensions_or_default}\n\n## Proposal 1\n{proposal_1}\n\n## Proposal 2\n{proposal_2}\n\n## Proposal 3\n{proposal_3}\n\n## Knowledge Context\n{knowledge_context}\n\nRank the proposals from best to worst. Output your ranking on a single line:\nRANKING: [best], [second], [worst]\n\nUse the exact labels: Proposal 1, Proposal 2, Proposal 3."
}
```

**Notes:**
- `model: "fast"` — judges use cost-efficient model for token savings.
- `readonly: true` — judges produce ranking output only.
- Each judge gets a **unique random ordering** of candidates.
- For 2-candidate rounds (one version failed gate): use "Proposal 1" and "Proposal 2" only,
  and adjust ranking format to `RANKING: [best], [worst]`.

---

## Judge Panel (parallel dispatch)

All judges MUST be dispatched in a **single message with multiple Task tool calls**.
This ensures true parallelism and no information leakage between judges.

### Per-Judge Randomization

Each judge gets an independently shuffled order:

```
candidates = [A_text, B_text, AB_text]  # or 2 if one gate-failed
labels = ["A", "B", "AB"]               # original identity

for judge_j in range(num_judges):
  shuffled_indices = random_permutation(len(candidates))
  proposals = [candidates[i] for i in shuffled_indices]
  order_map = {
    f"Proposal {k+1}": labels[shuffled_indices[k]]
    for k in range(len(candidates))
  }
  # Save order_map to pass_{n}/judge_{j}_order.json
  # Dispatch judge_j with proposals in this order
```

### Example: 3 judges, 3 candidates

```
Judge 1 sees: Proposal 1=AB, Proposal 2=A,  Proposal 3=B
Judge 2 sees: Proposal 1=B,  Proposal 2=AB, Proposal 3=A
Judge 3 sees: Proposal 1=A,  Proposal 2=B,  Proposal 3=AB
```

All three Task calls are made in a single message block.

---

## Anti-Scope-Creep Gate Check

Run this check AFTER receiving Author B and Synthesizer outputs, BEFORE dispatching judges.

```
def gate_check(text, initial_wc, current_a_wc, max_size_multiplier, max_growth_rate):
    wc = word_count(text)
    if wc > initial_wc * max_size_multiplier:
        return "GATE_FAILED: exceeds max size"
    if wc > current_a_wc * (1 + max_growth_rate):
        return "GATE_FAILED: exceeds growth rate"
    return "PASSED"
```

Gate outcomes affect judge dispatch:
- Both B and AB pass → 3-candidate tournament (standard)
- One fails → 2-candidate tournament (adjust Borda points: 1st=2, 2nd=1)
- Both fail → A wins pass by default, skip judge dispatch, increment streak

---

## Ranking Parser

Extract the ranking line from judge output. Judges may include preamble or reasoning
before the ranking — only the `RANKING:` line matters.

```
pattern = r"RANKING:\s*\[?(.+?)\]?\s*$"

# Match examples:
#   "RANKING: [Proposal 2], [Proposal 1], [Proposal 3]"
#   "RANKING: Proposal 1, Proposal 3, Proposal 2"
#   After analysis... RANKING: [Proposal 3], [Proposal 1], [Proposal 2]

# Parse steps:
# 1. Find the line matching the pattern
# 2. Split by comma
# 3. Strip whitespace and brackets from each element
# 4. Validate: each "Proposal N" appears exactly once
# 5. Map back to original labels via judge_{j}_order.json
```

If parsing fails after one retry (re-dispatch the judge with emphasis on format),
exclude that judge from aggregation. Quorum = minimum 2 valid judge responses.

---

## Error Recovery Dispatch

When a subagent fails (timeout, crash, invalid output):

1. **First failure**: Retry the same dispatch once.
2. **Second failure**:
   - Critic fails → skip critique, Author B writes B from task_prompt alone
   - Author B fails → B is `GATE_FAILED` (only A vs AB)
   - Synthesizer fails → AB is `GATE_FAILED` (only A vs B)
   - Judge fails → exclude from panel (quorum still 2)
   - All judges fail → A wins pass by default
3. Recovery always resumes from the last `pass_{n}/result.json` on disk.
