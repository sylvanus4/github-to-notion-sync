---
name: karpathy-coding-guard
description: >-
  Behavioral guardrails to reduce common LLM coding mistakes: surface assumptions
  before coding, enforce simplicity, make surgical changes, and define verifiable
  success criteria. Adapted from Karpathy's observations. Use when starting any
  non-trivial implementation, refactoring, or bugfix to prevent overcomplication,
  hidden assumptions, and scope creep. Do NOT use for trivial one-line fixes.
  Do NOT use for code review (use deep-review or simplify).
  Do NOT use for post-implementation cleanup (use omc-ai-slop-cleaner).
  Korean triggers: "코딩 가드레일", "구현 전 점검", "카파시 가이드", "접근법 점검".
  English triggers: "karpathy guard", "coding guardrails", "before I start coding",
  "check my approach", "implementation guard", "pre-coding check".
metadata:
  author: thaki
  version: "1.0.0"
  source: "forrestchang/andrej-karpathy-skills (adapted)"
  category: "behavioral-guardrail"
---

# Karpathy Coding Guard

Behavioral guardrails that activate **before implementation** on non-trivial tasks.
Adapted from [Andrej Karpathy's observations](https://github.com/forrestchang/andrej-karpathy-skills)
on common LLM coding mistakes, tailored to this project's Go/Fiber + React 19/FSD stack.

> **Activation:** Run this skill's gates whenever you are about to write, modify, or
> delete more than ~10 lines of code across 2+ files.

## Section 1: Pre-Implementation Gate (Think Before Coding)

Before writing any code, answer these four questions **out loud** in your response:

1. **Assumptions** — What am I assuming about the user's intent that could be wrong?
2. **Ambiguity** — Are there multiple valid interpretations? If yes, present them
   and let the user choose. Never pick silently.
3. **Simpler alternative** — Is there a simpler approach I haven't considered?
4. **Scope** — What files will change, and why each one?

### Decision Triggers

| Signal | Action |
|--------|--------|
| User request has 2+ valid interpretations | STOP — present options with tradeoffs |
| You're about to create a new file | STOP — confirm the file doesn't already exist and is truly needed |
| You're about to add a dependency | STOP — check if existing code already solves it |
| You feel "this might also need..." | STOP — that's scope creep. Ask first |

> **Cross-ref:** `critical-thinking.mdc` — apply the Opposite Direction Test to your
> chosen approach. What's the strongest argument against it?

## Section 2: Implementation Constraints (Simplicity First)

### The Senior Engineer Test

Before writing code, ask: **"Would a senior engineer say this is overcomplicated?"**

If the answer is "maybe" or "yes," simplify. Prefer:
- Fewer files over more files
- Inline logic over abstraction (until 3+ repetitions)
- Standard library over third-party package
- Existing project patterns over novel approaches

### Project-Stack Anti-Patterns

**Go/Fiber Backend:**

```go
// ❌ Over-abstracted: middleware for a single-use validation
func NewProjectOwnerMiddleware(store store.ProjectStore) fiber.Handler { ... }

// ✅ Inline check in the handler that needs it
func (h *Handler) DeleteProject(c *fiber.Ctx) error {
    project, err := h.store.GetProject(c.Context(), id)
    if project.OwnerID != userID {
        return fiber.ErrForbidden
    }
    ...
}
```

**React/FSD Frontend:**

```tsx
// ❌ Unnecessary Feature layer for a simple query
// features/project/hooks/useProjectName.ts (just wraps a single API call)

// ✅ Direct Entity-level adapter + hook when no business logic exists
// entities/project/infrastructure/api/project.adapter.ts
```

```tsx
// ❌ Strategy pattern for single-use form validation
const validators = { email: emailValidator, name: nameValidator };
const validate = (field, value) => validators[field](value);

// ✅ Simple Zod schema (project convention)
const schema = z.object({
  email: z.string().email(t('validation.email')),
  name: z.string().min(1, t('validation.required')),
});
```

**TDS Components:**

```tsx
// ❌ Wrapping TDS components in custom abstractions
function AppButton({ label, ...props }) {
  return <Button {...props}>{label}</Button>;
}

// ✅ Use TDS components directly — they are the abstraction
<Button variant="primary" size="md" isLoading={isPending}>
  {t('button.save')}
</Button>
```

### Rules

- No speculative generalization — solve the problem at hand, not hypothetical future ones
- No premature abstraction — wait for 3+ repetitions before extracting
- No unnecessary type gymnastics — `unknown` + type guard beats complex generics
  when the generic is used once
- Match the complexity of your solution to the complexity of the problem

## Section 3: Change Discipline (Surgical Changes)

### The Traceability Rule

**Every changed line must trace directly to the user's request.**

Before committing, review your diff and for each changed line ask: "Which part of
the user's request required this change?" If you can't answer, revert that line.

### Style Matching

- Read 20+ lines of surrounding code before editing
- Match existing conventions: quote style, naming (`camelCase` in TS, `snake_case`
  in Go structs), error handling patterns, import ordering
- If existing code uses `showToast('positive', msg)`, don't introduce `toast.success(msg)`
- If existing code uses `useFormWithI18n`, don't use `useForm` from react-hook-form

### Orphan Rules

- Only clean up orphans **you created** in this session
- Don't opportunistically refactor adjacent code
- Don't fix pre-existing lint warnings in files you're editing (unless explicitly asked)
- If you notice issues worth fixing, mention them — don't silently fix them

> **Cross-ref:** `bugfix-loop.mdc` — the "smallest fix" and "Must NOT Have guardrails"
> principles apply here. Declare what must NOT change before starting.

## Section 4: Verification Protocol (Goal-Driven Execution)

### Imperative-to-Declarative Transformation

Transform vague task descriptions into verifiable goals before coding:

| User says (imperative) | You define (declarative goal) |
|------------------------|-------------------------------|
| "Add user authentication" | "After this change: POST /auth/login returns a JWT; unauthorized routes return 401; tests cover both paths" |
| "Fix the form bug" | "After this change: submitting the form with valid data succeeds; submitting with invalid data shows field-level errors; the existing 3 tests pass + 1 new regression test" |
| "Improve performance" | "After this change: the target endpoint p95 drops below 200ms; no behavioral changes; before/after measurements documented" |

### Step-Verify Pattern

For multi-step tasks, verify after each step before proceeding:

1. Implement step 1
2. Run relevant tests / lint / typecheck
3. Confirm step 1 works in isolation
4. Only then proceed to step 2

Never batch all steps and verify at the end — failures compound and become
harder to diagnose.

> **Cross-ref:** `done-checklist.mdc` — use the DoD template (functional + guard +
> verification criteria) for non-trivial tasks.

## Section 5: Quick-Reference Litmus Tests

Use these four tests as a final check before responding with code:

| # | Test | Fail action |
|---|------|-------------|
| 1 | "Would a senior engineer say this is overcomplicated?" | Simplify until the answer is "no" |
| 2 | "Does every changed line trace to the user's request?" | Revert untraceable changes |
| 3 | "Did I transform the task into a verifiable goal?" | Define success criteria before coding |
| 4 | "If multiple interpretations exist, did I present them?" | Surface ambiguity, don't resolve silently |

## Composed With

- **Pre-implementation:** This skill (run first)
- **During implementation:** `bugfix-loop.mdc` for fixes, `00-core.mdc` for core principles
- **Post-implementation:** `deep-review` or `simplify` for code review
- **Cleanup:** `omc-ai-slop-cleaner` for removing accumulated slop
- **Critical thinking:** `critical-thinking.mdc` for adversarial analysis of your approach
