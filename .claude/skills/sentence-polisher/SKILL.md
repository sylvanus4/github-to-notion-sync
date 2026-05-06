---
name: sentence-polisher
description: >-
  Bilingual (Korean + English) sentence quality checker that detects grammar
  errors, logical inconsistencies, tone misalignment, awkward phrasing, and
  honorific/politeness level issues in Korean. Applies fixes automatically and
  returns polished text with a change summary. Designed as a final-stage
  refinement step for any text output pipeline. Based on pm-toolkit
  grammar-check methodology. Use when the user asks to "polish this text",
  "check grammar", "proofread", "sentence polish", "교정", "문장 교정", "문장 다듬기",
  "문법 체크", "글 다듬어줘", or when invoked as a pipeline stage by other skills
  (e.g., gws-email-reply). Do NOT use for full document rewriting (use
  prompt-transformer), brand voice generation from scratch (use brand voice
  guideline creation tools), or translation (handle directly).
---

# Sentence Polisher

## Output language

**Polished text** preserves the **input language**: Korean input → Korean output; English input → English output.

**Change summaries, analysis, and tone notes** default to **Korean** unless the caller specifies otherwise. Technical terms may remain in English.

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

### Step 3.5: Korean Spell-Check via 바른한글 (Optional)

When Korean text is detected (Korean mode or Bilingual mode), optionally verify spelling and grammar against 국립국어원 rules using the 바른한글 API (successor of 부산대 맞춤법 검사기). For full API details, see [references/korean-spell-check-api.md](references/korean-spell-check-api.md).

**When to run**: After Step 3 Error Scan, before Step 4 Auto-fix. Runs only in Korean/Bilingual mode.

**Procedure**:

1. **Chunk** the Korean text into segments of max 1500 characters, splitting at sentence boundaries (`.`, `!`, `?`, `\n`)
2. **POST** each chunk to `https://lab-api.bsm.klnet.kr/v1/check` with form-encoded `text` parameter
3. **Wait 1 second** between each API call (mandatory rate limit)
4. **Parse** corrections: each item has `original`, `suggestion`, `reason` fields
5. **Merge** API corrections into the Error Scan results under Korean-specific > 맞춤법 검사기 sub-category

**Graceful degradation**: If the API is unavailable, returns errors, or times out (>5s), skip this step silently and rely on LLM-based Korean-specific checks from Step 3. Log the skip reason but do not block the pipeline.

**Usage policy**: Non-commercial use only. Do not cache or redistribute API results. Keep call frequency low.

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
- Korean-specific: N fixes (spacing: N, honorific: N, ending: N, 맞춤법검사기: N, ...)
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

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:
- [project-tone-matrix.md](../references/project-overrides/project-tone-matrix.md) (POL-003 — tone by context, signal rules, formatting)
- [project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) (POL-001 — product name, domain terms, forbidden terms)

Key constraints:
- Apply financial/stock-analytics tone: cautious and non-advisory for signals and alerts; professional and consistent for reports and stakeholder copy.
- Preserve financial abbreviations (RSI, MACD, P/E) in their conventional English forms unless the glossary mandates otherwise.
- Verify Korean honorific level and audience-appropriate speech style against POL-003 for each surface (Slack, UI, email, reports).
