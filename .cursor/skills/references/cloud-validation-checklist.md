# UX Copy Validation Checklist (Cloud)

Run every generated or reviewed copy through these 10 checks during validation.
All checks are binary pass/fail. Fix any failures before delivering.

See length defaults in [cloud-copy-patterns.md](cloud-copy-patterns.md),
tone in [cloud-tone-matrix.md](cloud-tone-matrix.md), terms in
[cloud-terminology-glossary.md](cloud-terminology-glossary.md).

---

## The 10-Point Checklist

### 1. Concise

**Question:** Is the copy within the character/word limit for its category?

**Pass:** Meets or is under the length default in `cloud-copy-patterns.md`.
**Fail:** Exceeds the limit without justification.

**Fix:** Cut filler words first ("that", "just", "very", "really", "basically",
"actually", "in order to", "please note that"). Then restructure.

---

### 2. Actionable

**Question:** Does the user know what to do next after reading this?

**Pass:** Contains a clear next action, link, or CTA. Error messages include
recovery steps. Empty states include a creation prompt.
**Fail:** Ends with a problem statement and no guidance.

**Fix:** Add a specific action: "Try X", "Check Y", "Create Z", or link to
relevant documentation.

---

### 3. Consistent

**Question:** Does the copy match existing patterns in the product?

**Pass:** Uses the same terms, casing, punctuation, and structure as other
UI text in the same product area.
**Fail:** Introduces new terminology, changes casing conventions, or uses a
different structure than adjacent UI elements.

**Fix:** Align with the dominant pattern. If no pattern exists, follow the
category rules in `cloud-copy-patterns.md` and [consistency-rules.md](consistency-rules.md).

---

### 4. Accessible

**Question:** Can the copy be understood by all users regardless of cultural
background, language proficiency, or disability?

**Pass:**
- No idioms, metaphors, or slang
- No color-dependent meaning ("the red field")
- No directional references ("click the button on the right")
- Screen reader friendly (no "click here", descriptive link text)
- No abbreviations without first defining them

**Fail:** Contains any of the above anti-patterns.

**Fix:** Replace with literal, universal language. Spell out abbreviations on
first use.

---

### 5. Terminology

**Question:** Does the copy use only approved terms from the glossary?

**Pass:** All nouns, verbs, and status terms match `cloud-terminology-glossary.md`.
**Fail:** Contains a prohibited term or an inconsistent variant.

**Fix:** Replace with the approved term. If the needed term isn't in the
glossary, use the most common cloud convention and flag it for glossary update.

---

### 6. Tone

**Question:** Does the copy match the tone matrix for its category?

**Pass:** Formality, urgency, and technical depth align with the tone-by-category
matrix in `cloud-tone-matrix.md`.
**Fail:** Too formal for an empty state. Too casual for a destructive
confirmation. Too technical for an end-user error.

**Fix:** Adjust formality/urgency/technical depth to match the matrix. Re-check
against voice constants — voice never flexes.

---

### 7. Grammar

**Question:** Is the copy grammatically correct with no typos?

**Pass:** Correct spelling, grammar, punctuation. Proper use of articles,
prepositions, and verb tenses.
**Fail:** Typos, grammatical errors, or inconsistent punctuation.

**Fix:** Correct the specific error. For English: active voice, present tense
default. For Korean analysis text: standard business Korean.

---

### 8. Inclusive

**Question:** Is the copy free of gendered, ableist, or exclusionary language?

**Pass:**
- No gendered pronouns for users (use "you", "they", or the role name)
- No ableist metaphors ("blind to", "crippled", "lame")
- No age-related assumptions ("even your grandmother can use it")
- No cultural or religious references

**Fail:** Contains any exclusionary language.

**Fix:** Replace with neutral alternatives. "They" for unknown gender. Role
names ("the admin", "the developer") for specific audiences.

---

### 9. Translatable

**Question:** Can the copy be translated into other languages without
structural changes?

**Pass:**
- No concatenated strings ("Your " + count + " instances")
- No embedded variables mid-sentence that would break in SOV languages
- No puns, wordplay, or language-specific humor
- Uses standard placeholder format: `{variable_name}`
- No date/number formats hardcoded in copy

**Fail:** Contains string concatenation, hardcoded formats, or untranslatable
constructs.

**Fix:** Restructure to use complete sentences with placeholder tokens.
Use ICU MessageFormat for plurals: `{count, plural, one {1 instance} other {{count} instances}}`.

---

### 10. Scannable

**Question:** Can the user find the key information at a glance?

**Pass:**
- Most important word/concept is in the first 3 words
- No buried lead (the action isn't hidden in the middle of a paragraph)
- Lists or structured formats used for 3+ items
- Bold or formatting applied to key terms (where the UI supports it)

**Fail:** Key information is buried, or the copy requires full reading to
understand the point.

**Fix:** Front-load the critical word. Restructure long text into bulleted
lists or multiple shorter elements.

---

## Scoring

For review mode, score each check as:

| Score | Meaning |
|-------|---------|
| PASS | Meets the criterion |
| FAIL | Violates the criterion — include specific fix |

---

## Quick Reference Card

| # | Check | One-line Test |
|---|-------|---------------|
| 1 | Concise | Under the category character limit? |
| 2 | Actionable | User knows what to do next? |
| 3 | Consistent | Matches adjacent UI text patterns? |
| 4 | Accessible | No idioms, no color/direction references? |
| 5 | Terminology | All terms from the approved glossary? |
| 6 | Tone | Formality/urgency/depth match the matrix? |
| 7 | Grammar | Correct spelling, grammar, punctuation? |
| 8 | Inclusive | No gendered/ableist/exclusionary language? |
| 9 | Translatable | No concatenation, hardcoded formats? |
| 10 | Scannable | Key info in the first 3 words? |
