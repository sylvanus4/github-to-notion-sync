# Eval Test Cases for UX Writing Agent

Binary test cases for use with `skill-optimizer` eval/benchmark modes and
`skill-autoimprove` mutation loops. Each test case has a realistic prompt,
clear pass/fail criteria, and expected behavior.

---

## Test Case 1: Error Message Generation

**Prompt**: "Generate an error message for when a user tries to upload a file larger than 25 MB."

**Eval criteria (binary)**:

| # | Check | Pass Condition | Fail Condition |
|---|-------|----------------|----------------|
| 1 | States what happened | Message mentions the file size limit (25 MB) | No mention of the limit or the problem |
| 2 | Provides next step | Message tells the user what to do (compress, choose smaller file) | Only states the error with no guidance |
| 3 | Uses active voice | No passive constructions like "was rejected" or "has been exceeded" | Passive voice used |
| 4 | Under 150 characters | Total character count ≤ 150 | Exceeds 150 characters |
| 5 | No blame language | Does not say "you" + negative verb ("you exceeded", "you uploaded wrong") | Blames the user |

**Max score per run**: 5

---

## Test Case 2: Modal Confirmation Copy

**Prompt**: "Write copy for a confirmation modal when a user is about to permanently delete their account, including all associated data."

**Eval criteria (binary)**:

| # | Check | Pass Condition | Fail Condition |
|---|-------|----------------|----------------|
| 1 | Title names the action | Title contains "delete" and "account" (or clear equivalent) | Title is generic ("Are you sure?", "Confirm") |
| 2 | Body states consequences | Body mentions what will be lost (data, projects, settings, etc.) | Body is vague ("This cannot be undone") without specifics |
| 3 | Irreversibility stated | Message explicitly says the action is permanent or can't be undone | No mention of permanence |
| 4 | Buttons use verb+object | Primary button uses a verb-noun pattern ("Delete account") | Button says "OK", "Yes", "Confirm" |
| 5 | No over-dramatization | Tone is clear and calm, not alarmist | Uses exclamation marks, "WARNING", or fear-inducing language |

**Max score per run**: 5

---

## Test Case 3: Copy Review and Correction

**Prompt**: "Review and improve this error message: 'An unexpected error has occurred. Please contact support if the problem persists.'"

**Eval criteria (binary)**:

| # | Check | Pass Condition | Fail Condition |
|---|-------|----------------|----------------|
| 1 | Removes "unexpected" | The word "unexpected" or similar filler is removed | "Unexpected" or equivalent vague adjective remains |
| 2 | Before/after provided | Output shows original string alongside the improved version | Only shows the new version without comparison |
| 3 | Adds actionable guidance | Improved version tells the user what to try (refresh, try again, etc.) before escalating to support | Keeps "contact support" as the only guidance |
| 4 | Rationale included | Each change has a brief explanation of why it was made | Changes are made without explanation |
| 5 | Active voice used | Improved version uses active voice | Keeps passive "has occurred" or similar |

**Max score per run**: 5

---

## Test Case 4: Consistency Audit

**Prompt**: "Audit these button labels for consistency: 'Save', 'save changes', 'CANCEL', 'Go Back', 'close', 'Delete item', 'Remove'"

**Eval criteria (binary)**:

| # | Check | Pass Condition | Fail Condition |
|---|-------|----------------|----------------|
| 1 | Identifies casing issue | Flags the mix of Title Case, lowercase, and UPPERCASE as a problem | Does not mention casing inconsistency |
| 2 | Identifies terminology conflict | Flags "Delete" vs "Remove" as a terminology conflict | Does not mention the Delete/Remove conflict |
| 3 | Provides fixed versions | Offers corrected versions for all 7 labels | Only diagnoses problems without fixes |
| 4 | Severity classification | Assigns severity levels (Critical/High/Medium) to findings | Flat list without severity |
| 5 | Consistent fix applied | All corrected labels follow the same casing and structure rules | Corrected labels are still inconsistent with each other |

**Max score per run**: 5

---

## Test Case 5: English Quality Scoring

**Prompt**: "Score this onboarding copy for English quality: 'Welcome to our platform! Here you can manage your projects effectively. Click on New Project for starting.'"

**Eval criteria (binary)**:

| # | Check | Pass Condition | Fail Condition |
|---|-------|----------------|----------------|
| 1 | Provides numeric score | Output includes a score on the 0-10 scale | No numeric score provided |
| 2 | Scores per dimension | All 5 dimensions (Clarity, Consistency, Actionability, Tone, Naturalness) are scored individually | Fewer than 5 dimensions or only an aggregate score |
| 3 | Identifies unnatural phrasing | Flags "Click on New Project for starting" as unnatural | Does not flag the phrase |
| 4 | Suggests improvement | Provides a rewritten version of the copy | Only scores without suggesting improvements |
| 5 | Gate decision stated | Output includes PASS/REVIEW/FAIL based on the score | No gate decision |

**Max score per run**: 5

---

## Usage

### With skill-optimizer eval mode

```
/skill-optimizer eval ux-writing-agent
```

The optimizer loads these test cases, runs each through the skill with and
without the skill loaded, and grades outputs against the binary criteria.

### With skill-autoimprove

```
/skill-autoimprove ux-writing-agent
```

The autoimprove loop uses these test cases as the eval suite. Each mutation
of SKILL.md is scored against all 5 test cases × N runs. The max score is
`5 evals × 5 test cases = 25` per run.

### Baseline expectations

A well-functioning `ux-writing-agent` skill should achieve:
- **Baseline**: ≥ 70% pass rate (≥ 18/25)
- **Target**: ≥ 90% pass rate (≥ 23/25)
- **Ceiling**: 100% (25/25) — indicates the skill handles all tested scenarios correctly
