# Deep Understanding Question Rules

## Table of Contents

- [Core Principle](#core-principle)
- [Zero-Hint Policy](#zero-hint-policy-critical)
- [Question Types for Deep Understanding](#question-types-for-deep-understanding)
- [Difficulty Calibration](#difficulty-calibration)
- [Gap Follow-Up Protocol](#gap-follow-up-protocol)
- [AskQuestion Format](#askquestion-format)
- [Proficiency Tracking Protocol](#proficiency-tracking-protocol)
- [Language Rule](#language-rule)

## Core Principle

Every question must distinguish someone who **deeply understands** the subject from someone who **memorized facts**. Surface-level recall questions are forbidden. The goal is to expose mental model gaps, not test vocabulary.

## Zero-Hint Policy (CRITICAL)

1. **Option descriptions**: NEVER reveal correctness.
   - BAD: `label: "Attention mechanism"`, `description: "The core innovation behind Transformers"`
   - GOOD: `label: "Attention mechanism"`, `description: "Sequence-to-sequence computation method"`

2. **No "(Recommended)" tag** on any option.

3. **Randomize** correct answer position — never always first or last.

4. **Question phrasing**: Ask about reasoning and application, never hint at the answer.
   - BAD: "Which mechanism allows Transformers to process sequences in parallel?"
   - GOOD: "A researcher needs to process variable-length sequences without recurrence. What architectural choice best addresses this constraint, and why?"

5. **Plausible distractors**: Wrong options must represent genuine misconceptions or alternative expert positions, not obvious throwaway answers.

---

## Question Types for Deep Understanding

### 1. Mental Model Application [synthesis]

Test whether the student can APPLY a mental model to a novel situation.

- "Given [new scenario the sources don't directly address], which mental model from this field would you apply, and what would it predict?"
- "An expert encounters [unexpected result]. Using [mental model], how would they interpret this?"
- "Two mental models seem to give contradictory guidance for [situation]. How does an expert resolve this tension?"

### 2. Expert Disagreement Navigation [analysis]

Test understanding of WHY experts disagree, not just WHAT they disagree about.

- "Experts A and B disagree about [topic]. What underlying assumption does each side make that leads to their different conclusions?"
- "If [new evidence] emerged, which side of the [debate] would it support, and why?"
- "A colleague claims the [debate] is settled. What is the strongest counterargument they're ignoring?"

### 3. Conceptual Transfer [application]

Test whether knowledge can transfer to adjacent domains.

- "How would the [mental model] from this field apply to [adjacent field problem]?"
- "What would an expert in this field notice about [real-world scenario] that a non-expert would miss?"
- "If you had to explain [complex concept] to a practitioner in [different field], what analogy would capture the essential insight?"

### 4. Boundary Condition Reasoning [analysis]

Test understanding of WHERE concepts break down.

- "Under what conditions does [widely accepted principle] fail or produce misleading results?"
- "The consensus view is [X]. In what edge case would an expert deviate from this consensus?"
- "Two approaches are considered equivalent in most cases. When do they diverge, and which becomes superior?"

### 5. Causal Chain Reasoning [synthesis]

Test understanding of multi-step causal relationships.

- "If [upstream change] occurs, trace the chain of effects through the system. What is the non-obvious downstream consequence?"
- "Removing [component] from the system would cause [obvious effect]. What is the second-order effect most people would miss?"
- "Expert A proposes [change]. Expert B warns it will backfire because of [mechanism]. Whose reasoning is more sound?"

### 6. Epistemic Status Assessment [evaluation]

Test the ability to judge what is known vs. unknown.

- "Of these four claims about [topic], which has the strongest empirical support and which is primarily theoretical?"
- "A paper claims [result]. What would you need to see to be confident this is generalizable vs. a special case?"
- "Which of these 'facts' about [topic] is most likely to be revised in the next 5 years, and why?"

---

## Difficulty Calibration

| Round | Focus | Difficulty Mix |
|-------|-------|---------------|
| Round 1 | Mental model identification | 40% application, 40% analysis, 20% synthesis |
| Round 2 | Disagreement navigation + boundaries | 20% application, 40% analysis, 40% synthesis |
| Round 3+ | Causal chains + epistemic assessment | 10% application, 30% analysis, 60% synthesis |
| Weak-area drill | Targeted gap concepts | 100% synthesis — rephrase gaps in new contexts |

### Difficulty Definitions

- **Application**: Apply a single mental model to a clear scenario.
- **Analysis**: Compare or contrast two concepts, identify assumptions, find boundary conditions.
- **Synthesis**: Integrate multiple mental models, trace multi-step causal chains, or evaluate epistemic status across the field.

---

## Gap Follow-Up Protocol

When a student answers incorrectly:

1. **Identify the gap**: Which mental model or concept did they misapply?
2. **Explain the error**: Not just "the answer is B" but WHY their reasoning led astray.
3. **Connect to landscape**: Link the gap to the broader intellectual landscape (e.g., "This relates to the debate between X and Y — your answer aligned with the weaker position because...")
4. **Prescribe**: Point to which source material covers this concept most clearly.
5. **Rephrase**: In the next round, test the same concept from a different angle.

Query template for gap explanation:
```
"The student answered '<wrong_answer>' to: '<question>'. The correct answer is '<correct_answer>'. Explain: (1) what mental model they're missing, (2) why their reasoning was plausible but flawed, (3) how this connects to the broader debates in <subject>, (4) which source material in this notebook best explains the correct reasoning."
```

---

## AskQuestion Format

- `--questions` per round (default 5), 4 options each, single-select
- Header: max 12 chars, format `"Q1. <Topic>"`
- Option labels: concise (2-5 words)
- Option descriptions: neutral context only, never reveal answer
- After each round, always offer "Continue / Focus weak areas / Generate artifacts / Done"

---

## Proficiency Tracking Protocol

After grading each round:

1. **Update** `proficiency.md`:
   - Add new concept rows for first-time questions
   - Update existing rows (increment attempts/correct, update status)
   - Add gap notes for wrong answers under `### Gap Notes`

2. **Status mapping**:
   - Wrong: 0-39% correct rate
   - Fair: 40-69% correct rate
   - Good: 70-89% correct rate
   - Mastered: 90-100% correct rate

3. **Adaptive difficulty**: If a concept has been wrong 2+ times, increase question difficulty and change the angle of approach.

---

## Language Rule

All quiz content and proficiency tracking in the user's detected language. Concept names may remain in the source language (English technical terms are acceptable in Korean output).
