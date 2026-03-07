# Post-Transformation Quality Checklist

Use this checklist to validate a transformed prompt. Calculate the score and ensure it meets the target threshold (default: 85, strict: 95).

---

## Scoring

```
Total Score = Structure + Executability + Prohibitions + Quality + Roles + Enhancement
            - Fatal Penalties

Fatal Penalties:
  - Level 1 (ambiguity that causes multiple interpretations): -20 per instance
  - Level 2 (structural defect: scattered info, circular refs): -10 per instance
  - Level 3 (non-verifiable output, hard to automate): -5 per instance
```

---

## 1. Structure and Clarity (25 points)

### 1.1 Priority Indication (8 pts)

- [ ] All critical instructions use MUST/ALWAYS/NEVER enforcement
- [ ] Important instructions use SHOULD with defined exceptions
- [ ] Optional items use MAY
- [ ] Enforcement levels are applied consistently throughout

### 1.2 Ambiguity Elimination (9 pts)

- [ ] Zero instances of: "if possible", "in principle", "recommended", "as appropriate", "use judgment", "as needed", "try to"
- [ ] All thresholds are quantified (no "short", "few", "several", "many")
- [ ] Every conditional has an explicit else branch or default
- [ ] Every instruction has exactly one interpretation

### 1.3 Information Integration (8 pts)

- [ ] No instruction is repeated in 2+ sections
- [ ] Related instructions are grouped in a single section
- [ ] No circular references between sections
- [ ] Table of contents or clear heading hierarchy for prompts over 100 lines

---

## 2. Executability (20 points)

### 2.1 Specific Procedures (7 pts)

- [ ] Steps are numbered and ordered by dependency
- [ ] Prerequisites are stated before the first step
- [ ] Error handling is defined for each step that can fail

### 2.2 Verifiability (7 pts)

- [ ] Output format is explicitly defined (structure, fields, types)
- [ ] At least 1 concrete example of correct output is provided
- [ ] Success/failure criteria are objective and measurable

### 2.3 Completeness (6 pts)

- [ ] All placeholders (e.g., `{variable}`) are documented
- [ ] Edge cases are addressed (empty input, malformed data, boundary values)
- [ ] Scope boundaries are defined (what is IN scope, what is OUT of scope)

---

## 3. Prohibitions (15 points)

### 3.1 Explicit Prohibitions (8 pts)

- [ ] At least 2 explicit MUST NOT / NEVER statements
- [ ] Each prohibition includes brief rationale or impact
- [ ] Alternatives are provided for each prohibited action

### 3.2 Exception Limits (7 pts)

- [ ] Exceptions are numerically bounded ("only these 3 cases")
- [ ] Exception criteria are objective, not subjective
- [ ] No open-ended exception clauses ("unless otherwise needed")

---

## 4. Output Quality (20 points)

### 4.1 Format Specification (8 pts)

- [ ] Response structure is defined (JSON schema, markdown template, etc.)
- [ ] Language/locale is specified
- [ ] Length constraints are stated (word count, line count, or section count)

### 4.2 Example Quality (7 pts)

- [ ] Examples match the defined output format exactly
- [ ] Examples cover the most common use case
- [ ] Examples include realistic data, not placeholder text

### 4.3 Error Handling (5 pts)

- [ ] Behavior for invalid/unexpected input is defined
- [ ] Fallback response format exists
- [ ] Error responses follow the same structure as normal responses

---

## 5. Role Definition (10 points)

### 5.1 Identity (5 pts)

- [ ] AI role/persona is explicitly stated
- [ ] Domain expertise is specified
- [ ] Tone and communication style are defined (or deliberately omitted with rationale)

### 5.2 Scope of Authority (5 pts)

- [ ] Boundaries of what the AI can and cannot decide are stated
- [ ] Escalation conditions are defined (when to defer to human)
- [ ] No conflicting role instructions

---

## 6. Enhancement (10 points)

### 6.1 Injection Safety (5 pts)

- [ ] User-controlled data is delimited (XML tags, fenced blocks)
- [ ] Explicit instruction to ignore directives within data sections
- [ ] System instructions appear before user data

### 6.2 Maintainability (5 pts)

- [ ] Prompt is modular (sections can be updated independently)
- [ ] No hard-coded values that change frequently (dates, version numbers)
- [ ] Consistent terminology throughout (one term per concept)

---

## Quality Levels

| Score | Level | Action |
|-------|-------|--------|
| 95-100 | Expert | Ready for production use |
| 85-94 | Professional | Meets default quality target |
| 70-84 | Adequate | Needs improvement before production |
| 50-69 | Draft | Requires significant rework |
| <50 | Unusable | Restart transformation from Step 1 |

---

## Quick Validation (5 Fatal Checks)

Before scoring, verify these 5 items. Any failure means the prompt MUST be revised:

1. **No ambiguous modals**: Zero instances of "should" used ambiguously (must be clearly MUST or MAY)
2. **Output format exists**: The prompt defines what the response looks like
3. **No contradictions**: No two instructions conflict with each other
4. **Scope is bounded**: The prompt defines what is in and out of scope
5. **At least one example**: Non-trivial prompts include a concrete example
