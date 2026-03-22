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
  version: "1.0.0"
  category: "generation"
---
# Sentence Polisher

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
- **Expected tone**: formal (-합니다체), semi-formal (-해요체), casual (-하다체), diplomatic

If invoked by another skill (e.g., `gws-email-reply`), inherit the context from the caller.

### Step 3: Error Scan

Check 4 categories. For the full error taxonomy and examples, see [references/error-taxonomy.md](references/error-taxonomy.md).

**Grammar**
- Spelling, punctuation, subject-verb agreement, tense consistency
- English: article usage (a/an/the), preposition selection
- Korean: particle errors (조사 — 은/는, 이/가, 을/를, 에/에서)

**Logic**
- Contradictions within the text
- Unsupported or vague claims ("많은", "다양한" without specifics)
- Incomplete thoughts or dangling references

**Flow**
- Choppy transitions between sentences
- Passive voice overuse (English) or unnecessary nominalization (Korean)
- Redundancy and filler phrases
- Awkward phrasing or unnatural word order

**Korean-specific**
- Honorific level consistency (존댓말/반말 mixing)
- Spacing errors (띄어쓰기)
- **Konglish detection is MANDATORY**: always replace unacceptable Konglish with Korean equivalents per the reference taxonomy. Acceptable terms (미팅, 피드백, etc.) may remain. When in doubt, prefer the Korean equivalent in formal contexts and allow Konglish in casual/tech contexts.
- Excessive English mixing where Korean equivalents exist
- Formal ending consistency (-합니다/-해요/-하다 should not mix)
- Double-subject errors (이중 주어)

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

### Example 1: Korean email polish

**User says:** "이 메일 문장 다듬어줘: 안녕하세요 김과장님, 어제 말씀하신 건에 대해서 검토해봤는데요 결론적으로는 진행하는게 좋을것 같습니다 감사합니다"

**Actions:**
1. Detect: Korean mode
2. Context: email reply, formal tone expected
3. Scan: spacing errors (3), punctuation missing (2), particle issue (1)
4. Fix and return polished version with change summary

**Result:**
```
## Polished Text

안녕하세요, 김 과장님.

어제 말씀하신 건에 대해 검토해 봤는데요, 결론적으로는 진행하는 것이 좋을 것 같습니다.

감사합니다.

## Change Summary
- Grammar: 2 fixes (punctuation: 2)
- Korean-specific: 4 fixes (spacing: 3, particle: 1)
- Total: 6 fixes applied

### Changes Applied
1. "안녕하세요 김과장님," → "안녕하세요, 김 과장님." — [punctuation: comma after greeting, period at end]
2. "검토해봤는데요" → "검토해 봤는데요," — [spacing: 본용언+보조용언, punctuation: comma]
3. "진행하는게" → "진행하는 것이" — [spacing: 의존명사 띄기]
4. "좋을것 같습니다" → "좋을 것 같습니다" — [spacing: 의존명사 띄기]
5. "감사합니다" → "감사합니다." — [punctuation: period]
6. "말씀하신 건에 대해서" → "말씀하신 건에 대해" — [particle: 불필요한 조사 제거]

## Tone Assessment
Text aligns with formal tone for business email context.
```

### Example 2: English text polish

**User says:** "proofread: We are planning to have a meeting about the new feature, it will be discuss about the timeline and also the resource that is needed."

**Actions:**
1. Detect: English mode
2. Context: inferred as internal communication
3. Scan: grammar (subject-verb: "discuss" → "discussed"), flow (run-on, passive), redundancy ("also")
4. Fix and return

**Result:**
```
## Polished Text

We are planning a meeting about the new feature to discuss the timeline and required resources.

## Change Summary
- Grammar: 1 fix (verb form)
- Flow: 2 fixes (run-on sentence merged, redundancy removed)
- Total: 3 fixes applied

### Changes Applied
1. "We are planning to have a meeting about" → "We are planning a meeting about" — [flow: reduce verbosity]
2. "it will be discuss about the timeline and also the resource that is needed" → "to discuss the timeline and required resources" — [grammar: verb form, flow: remove "also" and nominalization]
3. Run-on comma splice → single coherent sentence — [flow: sentence merge]

## Tone Assessment
Text aligns with semi-formal tone for internal communication.
```

### Example 3: Mixed Korean-English Slack message

**User says:** "문장 다듬어줘: 오늘 deployment 이슈 핸들링 하느라 수고했어요. 내일 리뷰 미팅에서 discuss 해볼게요. 일단 PR은 어사인 해놨습니다."

**Actions:**
1. Detect: Bilingual mode (mixed Korean-English)
2. Context: Slack message, semi-formal tone
3. Scan: Konglish (핸들링→처리, discuss→논의, 어사인→배정), honorific mixing (해요/합니다), spacing
4. Fix and return

**Result:**
```
## Polished Text

오늘 배포 이슈를 처리하느라 수고했어요. 내일 리뷰 미팅에서 논의해 볼게요. 일단 PR은 배정해 놨어요.

## Change Summary
- Korean-specific: 5 fixes (Konglish: 3, honorific: 1, spacing: 1)
- Total: 5 fixes applied

### Changes Applied
1. "핸들링" → "처리" — [Konglish: unacceptable term]
2. "discuss" → "논의" — [Konglish: English verb in Korean sentence]
3. "어사인" → "배정" — [Konglish: unacceptable term]
4. "해놨습니다" → "해 놨어요" — [honorific: unified to -해요체 matching rest of message]
5. "해볼게요" → "해 볼게요" — [spacing: 본용언+보조용언]

## Tone Assessment
Text aligns with semi-formal tone for team Slack communication.
```

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
