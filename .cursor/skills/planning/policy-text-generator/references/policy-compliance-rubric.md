# Policy Compliance Rubric

Scoring criteria for policy-text-generator. Each dimension is binary pass/fail.

## Dimensions

### 1. Policy Adherence (Weight: 2x)

**Pass**: All mandatory keywords/phrases from the policy are present AND zero forbidden expressions appear in the text.

**Fail**: Any mandatory element is missing OR any forbidden expression is present.

Checklist:
- [ ] All "MUST include" items from policy are present
- [ ] Zero "MUST NOT include" items appear
- [ ] Required legal notices are present (if applicable)
- [ ] Regulatory language requirements are met (if applicable)

### 2. Consistency (Weight: 1x)

**Pass**: Text uses the same terminology, capitalization, and phrasing patterns as existing approved texts in the same category.

**Fail**: Text introduces new terminology or deviates from established patterns without justification.

Checklist:
- [ ] Terminology matches approved glossary
- [ ] Capitalization follows existing patterns
- [ ] Button/action labels follow established conventions
- [ ] Date/time/number formats match style guide

### 3. Clarity (Weight: 1x)

**Pass**: Text is understandable at the target reading level. No jargon unless explicitly permitted by policy. Sentences are concise.

**Fail**: Text contains unexplained jargon, ambiguous phrasing, or exceeds readability target.

Checklist:
- [ ] No unexplained technical jargon
- [ ] Active voice preferred (unless policy specifies otherwise)
- [ ] Sentence length under 40 characters for UI labels, under 80 for messages
- [ ] One idea per sentence for error messages

### 4. Completeness (Weight: 1x)

**Pass**: All required elements for the text type are present (e.g., error messages include cause + action, notifications include context + CTA).

**Fail**: Missing required structural elements.

Required elements by type:

| Text Type | Required Elements |
|-----------|-------------------|
| error-message | Cause + user action + support contact (if critical) |
| notification | Context + what happened + next action |
| ui-label | Descriptive label + accessibility text |
| terms | Legal notice + effective date + scope |
| tooltip | Explanation + link to details (if complex) |
| onboarding | Benefit statement + action prompt |

### 5. Tone Match (Weight: 1x)

**Pass**: Text tone matches the profile specified in the policy document.

**Fail**: Text tone deviates from the specified profile.

Tone profiles:

| Profile | Characteristics |
|---------|-----------------|
| Formal (격식체) | 합쇼체, no contractions, no emoji, professional distance |
| Polite (공손체) | 해요체, warm but professional, empathetic |
| Casual (친근체) | 해체/해요체 mix, conversational, approachable |
| Neutral (중립체) | 하십시오체 for instructions, factual, no emotional language |

## Scoring Calculation

```
Score = (Policy Adherence × 2) + Consistency + Clarity + Completeness + Tone Match
Max Score = 6
Threshold = 5 (auto-approval)
```

## Conflict Resolution

When policy rules conflict (e.g., "be concise" vs "include all legal notices"):
1. Legal/regulatory requirements take priority
2. Safety-critical information takes second priority
3. User experience guidelines take third priority
4. Stylistic preferences yield to all above
