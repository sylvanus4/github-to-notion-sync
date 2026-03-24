---
name: sentence-polisher
description: >-
  Bilingual (Korean + English) sentence quality checker that detects grammar
  errors, logical inconsistencies, tone misalignment, awkward phrasing, and
  honorific/politeness level issues in Korean. Applies fixes automatically and
  returns polished text with a change summary. Designed as a final-stage
  refinement step for any text output pipeline. Based on pm-toolkit
  grammar-check methodology. Use when the user asks to "polish this text",
  "check grammar", "proofread", "sentence polish", "교정", "문장 교정", "문장
  다듬기", "문법 체크", "글 다듬어줘", or when invoked as a pipeline stage by
  other skills (e.g., gws-email-reply). Do NOT use for full document rewriting
  (use prompt-transformer), brand voice generation from scratch (use
  kwp-brand-voice-guideline-generation), or translation (handle directly).
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "generation"
---
# Sentence Polisher

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Polished passages match input language (Korean in → Korean out; English in → English out). Change summaries and tone notes default to Korean for this workspace unless the caller requests otherwise.

Bilingual (Korean + English) active text fixer. Unlike pm-toolkit `grammar-check` (which only suggests), this skill APPLIES fixes and returns polished text ready for use.

## Workflow

### Step 1: Detect Language

Identify the primary language of the input text:

| Detection | Mode |
|-----------|------|
| >80% Korean characters | Korean mode |
| >80% Latin characters | English mode |
| Mixed | Bilingual mode — apply both rulesets; scan ALL Korean segments for Konglish and ALL English segments for grammar |

### Step 2: Context Analysis

Identify before scanning:
- **Text purpose**: email reply, report, Slack message, presentation, documentation
- **Target audience**: internal team, external client, executive, technical peer
- **Expected tone**: formal business, semi-formal, casual, or diplomatic (Korean speech levels when polishing Korean)

If invoked by another skill (e.g., `gws-email-reply`), inherit the context from the caller.

### Step 3: Error Scan

Check 4 categories. For the full error taxonomy and examples, see [references/error-taxonomy.md](references/error-taxonomy.md).

**Grammar**
- Spelling, punctuation, subject-verb agreement, tense consistency
- English: article usage (a/an/the), preposition selection
- Korean: particle errors (topic/object/locative and related markers)

**Logic**
- Contradictions within the text
- Unsupported or vague quantifiers without specifics
- Incomplete thoughts or dangling references

**Flow**
- Choppy transitions between sentences
- Passive voice overuse (English) or unnecessary nominalization (Korean)
- Redundancy and filler phrases
- Awkward phrasing or unnatural word order

**Korean-specific**
- Honorific level consistency (polite vs plain mixing)
- Spacing (word boundaries)
- **Konglish detection is MANDATORY**: replace unacceptable loanword usage with Korean equivalents per [references/error-taxonomy.md](references/error-taxonomy.md). Keep widely accepted loanwords when listed as acceptable. Prefer Korean in formal contexts; allow established tech loanwords in casual/technical contexts.
- Excessive English mixing where Korean equivalents exist
- Formal ending consistency (do not mix speech levels within one document)
- Double-subject constructions

### Step 4: Auto-fix

Apply all fixes directly to the text:

| Fix Type | Approach |
|----------|----------|
| Clear error (spelling, spacing, punctuation) | Fix silently |
| Grammar rule violation | Fix and count |
| Flow improvement | Rewrite the sentence preserving meaning |
| Ambiguous fix (multiple valid options) | Apply best-guess fix and mark with `[REVIEW]` |
| Voice/style choice | Preserve author's voice; only fix if clearly wrong |

MUST preserve:
- Author's intended meaning and tone
- Technical terms and proper nouns
- Intentional informal language (when context supports it)
- Code snippets, URLs, email addresses

### Step 5: Output

Return the result in this format:

```
## Polished Text

[The corrected, polished text — ready to use as-is]

## Change Summary
- Grammar: N fixes (spelling: N, punctuation: N, particle: N, ...)
- Logic: N fixes
- Flow: N fixes
- Korean-specific: N fixes (spacing: N, honorific: N, ending: N, ...)
- Total: N fixes applied

### Changes Applied
1. "original phrase" → "fixed phrase" — [category: reason]
2. ...

## Items for Review
- [REVIEW] "original phrase" → "suggested phrase" — reason for ambiguity
- (none if all fixes are unambiguous)

## Tone Assessment
Text aligns with [formal/semi-formal/casual] tone for [context type].
[One sentence on whether tone matches the intended audience.]
```

If zero errors are found, return:

```
## Polished Text

[Original text unchanged]

## Change Summary
No issues found. Text is clean.

## Tone Assessment
[Assessment]
```

## Examples

### Example 1: Korean formal email

User requests polish on a run-on Korean business email. Run Korean mode, fix spacing/punctuation/particles, unify formal endings, return **Polished Text** + **Change Summary** + **Tone Assessment** in Korean.

### Example 2: English internal note

User pastes English with grammar and flow issues. Run English mode; fix verb agreement, run-ons, redundancy; return polished English with counts.

### Example 3: Mixed Korean–English Slack

User pastes informal team Slack text mixing languages. Run bilingual mode; normalize Konglish per taxonomy; align speech level; fix spacing; return Korean-forward copy with rationale bullets.

### Example 4: Pipeline invocation (no user interaction)

**Invoked by:** `gws-email-reply` step 5

**Input:** Draft email text + context metadata (purpose: email reply, tone: formal, audience: external client)

**Actions:**
1. Skip language detection prompt — use provided context
2. Scan, fix, return polished text
3. Caller uses the polished text directly

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Empty input text | Return error: "No text provided for polishing" |
| Text is already clean (0 errors) | Return original text with "No issues found" summary |
| Cannot determine language | Default to bilingual mode; apply both rulesets |
| Ambiguous fix conflicts with context | Mark with `[REVIEW]` and preserve original in parentheses |
| Very long text (>5000 chars) | Process in chunks by paragraph; maintain cross-paragraph consistency for honorific level, tense, and terminology |
