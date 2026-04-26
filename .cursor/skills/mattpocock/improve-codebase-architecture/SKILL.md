---
name: improve-codebase-architecture
description: Propose architectural improvements to the codebase with deep-module analysis. Use when user wants architecture review, reduce complexity, improve code depth, simplify interfaces, or mentions "A Philosophy of Software Design".
---

# Improve Codebase Architecture

Analyze the codebase and propose architectural improvements based on the principles in [LANGUAGE.md](./LANGUAGE.md). Focus on reducing complexity by creating deep modules with simple interfaces.

## Process

### 1. Understand Current Architecture

Before proposing changes:

- Map the module structure: what are the key modules/packages/components?
- Identify the interfaces between them: function signatures, types, config shapes
- Understand the dependency graph: who depends on whom?
- Look for existing documentation: CONTEXT.md, ADRs, architecture docs

### 2. Identify Complexity

Look for symptoms of unnecessary complexity:

**Shallow modules** — modules whose interface is nearly as complex as their implementation. These force callers to understand implementation details.

**Information leakage** — when the same knowledge is encoded in multiple places. Changes require touching many files.

**Temporal decomposition** — modules organized by "when" things happen rather than by information hiding. Results in many tiny modules that each know about the same data.

**Pass-through methods** — methods that do nothing but call another method with the same (or nearly the same) signature.

**Overexposed configuration** — forcing callers to specify details they shouldn't need to care about.

### 3. Apply the Principles

For each problem identified, apply the relevant principle from [LANGUAGE.md](./LANGUAGE.md):

- **Modules should be deep** — small interface, significant implementation
- **Information hiding** — each module encapsulates a design decision
- **Define errors out of existence** — design interfaces so errors can't happen
- **Pull complexity downward** — it's better for a module to be complex internally than to push complexity to its callers

For interface improvements, use the principles in [INTERFACE-DESIGN.md](./INTERFACE-DESIGN.md).

For deepening existing modules, use the techniques in [DEEPENING.md](./DEEPENING.md).

### 4. Propose Changes

For each proposed change:

1. **What's the problem?** — describe the current complexity clearly
2. **What's the interface change?** — show the before/after of how callers interact with the module (code examples)
3. **What moves inside?** — what complexity gets absorbed by the module
4. **What's the trade-off?** — be honest about downsides

### 5. Document Decisions

If a proposal involves architectural decisions that meet the ADR criteria (hard to reverse, surprising, real trade-off), use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

If new domain terms emerge, update CONTEXT.md using [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

## Anti-Patterns

- Don't propose changes that just move code around without reducing interface complexity
- Don't split modules for "cleanliness" — splitting increases complexity unless the resulting modules are independently deep
- Don't add abstraction layers that don't hide meaningful decisions
- Don't optimize for testability at the expense of interface simplicity
- Don't propose changes you can't explain the benefit of in one sentence

## Example

**Problem:** The `EmailService` requires callers to specify SMTP configuration, template selection, variable substitution, and retry policy for every email sent.

**Before:**
```typescript
emailService.send({
  to: user.email,
  template: "welcome",
  variables: { name: user.name, activationUrl: url },
  smtp: { host: "smtp.example.com", port: 587, auth: credentials },
  retry: { maxAttempts: 3, backoffMs: 1000 },
});
```

**After:**
```typescript
emailService.sendWelcome(user);
```

**What moves inside:** SMTP config (from environment), template selection and variable mapping (the service knows what a "welcome" email needs), retry policy (sensible default, not caller's concern).

**Trade-off:** Less flexible per-call customization. But the 99% case is "send a welcome email to this user" — the interface should optimize for that, not for the rare case where you need custom SMTP settings.
