## Tracer Bullet

Apply unfamiliar technology, patterns, or sweeping changes to the smallest possible unit first. Validate, extract a blueprint, then expand systematically with confidence.

### Usage

```
/tracer-bullet "Apply liquidglass to SettingsView"          # new tech on one screen
/tracer-bullet "Migrate AuthService to new ORM"             # pattern migration
/tracer-bullet "Add dark mode support to ProfileCard"       # sweeping change, smallest first
/tracer-bullet --expand "Apply liquidglass to remaining"    # expand after blueprint approval
```

### Workflow

#### Phase 1: Tracer Shot

1. **Identify the smallest target** — User specifies what to try and on which minimal unit (one screen, one endpoint, one component)
2. **Apply ONLY to that target** — Do not touch anything else. Resist scope expansion.
3. **Commit with `[tracer]` tag** — `[tracer] Apply liquidglass to SettingsView`
4. **Run verification** — lint, tests, manual check if applicable

#### Phase 2: Blueprint Extraction

5. **Produce a blueprint document** summarizing:

```markdown
# Tracer Bullet Blueprint: <title>

## Target
<what was changed and where>

## What Worked
- <pattern, approach, or configuration that succeeded>

## Conflicts Found
- <what broke, clashed, or required workaround>

## Patterns for Expansion
- <repeatable steps for applying to other targets>
- <files/modules to watch out for>
- <dark mode / edge case considerations>

## Expansion Targets
- [ ] <next target 1>
- [ ] <next target 2>
- [ ] <next target 3>
```

6. **Pause for user review** — Do NOT proceed to expansion without explicit approval

#### Phase 3: Systematic Expansion (with `--expand`)

7. **Apply to remaining targets one at a time**, following the blueprint patterns
8. **Commit after each target** — `[tracer] Apply liquidglass to <TargetName>`
9. **If any target diverges from blueprint** — stop, update blueprint, get approval before continuing

### Rules

- NEVER apply to all targets in one pass — one at a time, with commits between each
- The blueprint is the primary deliverable of Phase 1, not the code change itself
- If the tracer shot reveals the approach is fundamentally flawed, report that finding instead of forcing it
- Each expansion commit should be independently revertable
- Follow the `observability.mdc` checkpoint protocol throughout

### When to Use

- Adopting a new library, framework, or design language (e.g., liquidglass, new ORM)
- Migrating patterns across many files (e.g., class components → hooks, REST → GraphQL)
- Applying design system changes across multiple screens
- Any change where "I'm not sure how this will interact with our code"

### When NOT to Use

- Well-understood changes with established patterns in the codebase
- Bug fixes (use `/diagnose` instead)
- Single-file changes that don't need expansion
