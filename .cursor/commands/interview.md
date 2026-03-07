## Interview

Socratic pre-implementation interview to surface edge cases, clarify ambiguities, and produce structured requirements before coding begins. The 5-minute investment that prevents hours of agent ping-pong.

### Usage

```
/interview "Add dark mode toggle to settings"     # interview for a feature
/interview "Refactor auth to use JWT refresh"      # interview for a refactor
/interview --append spec.md "Payment flow"         # append to existing spec
```

### Workflow

1. **User provides** a 1-2 sentence feature description
2. **Agent asks** 5-7 targeted questions across these categories:
   - **Inputs / Outputs** — What data comes in? What does the output look like? Validation rules?
   - **Design tokens** — Which design system colors, typography, spacing? Any custom values?
   - **UX behavior** — Transitions, animations, loading states, empty states?
   - **Error states** — What can go wrong? How should each failure present to the user?
   - **Edge cases** — Boundary values, concurrent access, offline scenarios, permissions?
   - **Dependencies** — What existing modules/APIs does this touch? What must NOT be modified?
   - **Security** — Authentication, authorization, data sanitization concerns?
3. **User answers** each question (can respond "default" or "skip" to use reasonable defaults)
4. **Agent produces** a structured requirements document

### Output

The agent generates a `requirements.md` (or appends to an existing spec via `--append`) with:

```markdown
# Feature: <title>

## Description
<1-2 sentence summary>

## Acceptance Criteria
- [ ] <specific, verifiable criterion>
- [ ] <specific, verifiable criterion>

## Must NOT Have (Guard Criteria)
- <boundary that must not be crossed>

## Edge Cases
- <edge case and expected behavior>

## Dependencies
- <modules/files that will be touched>
- <modules/files that must NOT be touched>
```

### Rules

- Ask questions ONE at a time using the AskQuestion tool — do not dump all questions at once
- Adapt follow-up questions based on answers (Socratic, not scripted)
- Skip categories that are clearly irrelevant (e.g., skip "Design tokens" for a CLI tool)
- Keep the total interview under 7 questions — enough to surface blind spots, not enough to be tedious
- If the user's description is already highly specific, reduce to 3-4 clarifying questions

### When to Use

- Before implementing any feature that touches 3+ files
- Before starting work that involves unfamiliar domain logic
- When requirements feel "obvious" — that's usually when the most assumptions hide
- As a replacement for jumping straight into code after a vague request

### When NOT to Use

- Trivial changes (rename, typo fix, one-liner)
- Bug fixes with clear reproduction steps
- Tasks where a full spec/PRD already exists and covers edge cases
