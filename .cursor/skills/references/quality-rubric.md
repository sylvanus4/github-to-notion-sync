# Quality Rubric for UX Copy

5-dimension scoring system used by the `quality-check` and `audit` sub-skills.
Modeled after the ai-quality-evaluator deduction-table pattern.

---

## Scoring Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Clarity** | 25% | Can the user understand the message on the first read? |
| **Consistency** | 25% | Are tone, terms, and structure uniform across the string set? |
| **Actionability** | 20% | Does the user know what to do next? |
| **Tone** | 15% | Does the copy match the brand's tone-and-voice? |
| **Naturalness** | 15% | Does it sound like a native speaker wrote it? |

**Final score**: Weighted average on a 0–10 scale.

| Score Range | Gate Decision |
|-------------|---------------|
| 8.0–10.0 | **PASS** — publish-ready |
| 6.0–7.9 | **REVIEW** — flag issues, suggest fixes, ask for confirmation |
| 0.0–5.9 | **FAIL** — rewrite recommended |

---

## Dimension 1: Clarity (25%)

Start at 10. Apply deductions.

| Check | Method | Deduction |
|-------|--------|-----------|
| Ambiguous pronoun | "It" or "this" without a clear referent | -2 per instance |
| Jargon without context | Technical term unfamiliar to the target audience | -2 per term |
| Double negative | "Not unlikely", "Don't forget to not..." | -3 per instance |
| Sentence over 25 words | Count words in each UI string | -1 per string |
| Passive voice hiding the actor | "An error was encountered" — who encountered it? | -1 per instance |
| Multiple ideas in one string | Single string tries to communicate 2+ separate things | -2 per instance |

**Floor**: 0

---

## Dimension 2: Consistency (25%)

Start at 10. Apply deductions.

| Check | Method | Deduction |
|-------|--------|-----------|
| Terminology conflict | Same action uses different verbs (e.g., "Delete" and "Remove") | -3 per conflict |
| Casing mismatch | Title Case and Sentence case mixed for same element type | -2 per mismatch |
| Punctuation inconsistency | Some strings end with periods, others don't (same context) | -1 per pair |
| Person/voice shift | "You can..." in one string, "Users can..." in another | -2 per shift |
| Tone shift | Formal tone in one string, casual in another (same context) | -2 per shift |
| Structure mismatch | Error messages follow different patterns within the same flow | -1 per mismatch |

**Floor**: 0

---

## Dimension 3: Actionability (20%)

Start at 10. Apply deductions.

| Check | Method | Deduction |
|-------|--------|-----------|
| Error without next step | Error message states the problem but not how to fix it | -3 per instance |
| Vague CTA | Button says "OK", "Submit", or "Click here" without specifying the action | -2 per instance |
| Missing consequence | Destructive action modal doesn't state what will happen | -3 per instance |
| Dead-end message | Message provides no path forward (no button, no link, no instruction) | -2 per instance |
| Hidden action | The next step exists but is buried or unclear | -1 per instance |

**Floor**: 0

---

## Dimension 4: Tone (15%)

Start at 10. Apply deductions.

| Check | Method | Deduction |
|-------|--------|-----------|
| Blame language | "You entered wrong..." or "Your mistake..." | -3 per instance |
| Over-celebration | "Amazing!", "Awesome!", "Congratulations!" for routine actions | -2 per instance |
| Robotic language | "Operation completed successfully", "Process terminated" | -2 per instance |
| Inappropriate humor | Jokes, puns, or sarcasm in error or warning contexts | -3 per instance |
| Excessive formality | "We kindly request that you..." in a consumer product | -1 per instance |
| Missing empathy | Error affecting user data or time shows no acknowledgment | -2 per instance |

**Floor**: 0

---

## Dimension 5: Naturalness (15%)

Start at 10. Apply deductions. This dimension is especially critical for
teams where English is not the first language.

| Check | Method | Deduction |
|-------|--------|-----------|
| Unnatural phrasing | Sentence structure a native speaker would never use | -2 per instance |
| Word-for-word translation artifacts | "Please input your informations" | -3 per instance |
| Awkward preposition | "Click on the button for starting" vs "Click to start" | -2 per instance |
| Missing articles | "Open file" where "Open the file" is natural | -1 per instance |
| Unnecessary words | "In order to", "due to the fact that", "at this point in time" | -1 per instance |
| Unnatural contraction usage | Formal context uses contractions, or casual context avoids them | -1 per instance |

**Floor**: 0

---

## Scoring Procedure

1. Read every string in the input set
2. For each dimension, start at 10 and apply all applicable deductions
3. Floor each dimension score at 0
4. Calculate the weighted average:

```
final_score = (clarity × 0.25) + (consistency × 0.25) + (actionability × 0.20)
            + (tone × 0.15) + (naturalness × 0.15)
```

5. Apply the gate decision based on final_score

---

## Scoring Example 1: Error Message Review

**Input**: "Login has failed. Please try again."

| Dimension | Score | Deductions Applied |
|-----------|-------|--------------------|
| Clarity | 8 | -2: passive voice hiding actor ("has failed" — what failed?) |
| Consistency | 10 | No conflicts (single string) |
| Actionability | 7 | -3: no guidance on WHY it failed or what to check |
| Tone | 8 | -2: robotic phrasing ("Login has failed") |
| Naturalness | 8 | -1: "Please try again" is natural but "Login has failed" is stiff; -1 unnecessary "Please" |

**Final**: (8×0.25) + (10×0.25) + (7×0.20) + (8×0.15) + (8×0.15) = 2.0 + 2.5 + 1.4 + 1.2 + 1.2 = **8.3 → PASS**

**Suggested improvement**: "Couldn't sign in. Check your email and password, then try again."

---

## Scoring Example 2: Modal Confirmation

**Input**:
- Title: "Are you sure?"
- Body: "This action cannot be undone."
- Buttons: "Yes" / "No"

| Dimension | Score | Deductions Applied |
|-----------|-------|--------------------|
| Clarity | 6 | -2: "This action" is ambiguous (what action?); -2: no specific object named |
| Consistency | 10 | Single context |
| Actionability | 5 | -3: doesn't state what will happen; -2: buttons are vague ("Yes"/"No") |
| Tone | 9 | -1: slightly robotic "This action cannot be undone" |
| Naturalness | 9 | -1: "cannot" → "can't" for natural tone |

**Final**: (6×0.25) + (10×0.25) + (5×0.20) + (9×0.15) + (9×0.15) = 1.5 + 2.5 + 1.0 + 1.35 + 1.35 = **7.7 → REVIEW**

**Suggested improvement**:
- Title: "Delete this project?"
- Body: "All tasks and files in this project will be permanently deleted. This can't be undone."
- Buttons: "Delete project" / "Keep project"

---

## Scoring Example 3: Batch Audit (Buttons)

**Input**: "Save", "save changes", "CANCEL", "Go Back", "close", "Delete item", "Remove"

| Dimension | Score | Deductions Applied |
|-----------|-------|--------------------|
| Clarity | 9 | -1: "Remove" without object noun |
| Consistency | 3 | -2: casing (Title/lower/UPPER mixed); -3: "Delete" vs "Remove" terminology; -2: structure mismatch (some have objects, some don't) |
| Actionability | 8 | -2: "CANCEL" and "close" are vague |
| Tone | 8 | -2: inconsistent formality level across the set |
| Naturalness | 9 | -1: "CANCEL" in all-caps feels aggressive |

**Final**: (9×0.25) + (3×0.25) + (8×0.20) + (8×0.15) + (9×0.15) = 2.25 + 0.75 + 1.6 + 1.2 + 1.35 = **7.15 → REVIEW**

**Suggested fixes**: Normalize to sentence case, pick "Delete" as canonical term, add object nouns to all buttons.
