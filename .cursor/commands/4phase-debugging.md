## 4-Phase Systematic Debugging

Strict sequential debugging: Reproduce → Narrow → Fix → Verify. No guessing. No shotgun edits.

### Usage

```
/4phase-debugging "Login fails silently on mobile Safari"
/4phase-debugging "Order total calculates incorrectly with discounts"
/4phase-debugging --issue "GH-#142" --phase 2
```

### Workflow

1. **Reproduce** — Create the smallest possible failing test that reliably triggers the bug. Cannot proceed without it.
2. **Narrow** — Binary search the root cause via logging, git bisect, or code path isolation until you can state it in one certain sentence.
3. **Fix** — Apply a single minimal change (1-5 lines ideal) in a dedicated commit. No refactoring mixed in.
4. **Verify** — Run the reproduction test + full test suite. Zero regressions. Document root cause and fix in the commit message.

### Execution

Read and follow the `4phase-debugging` skill (`.cursor/skills/review/4phase-debugging/SKILL.md`) for the full 4-phase methodology with iron rules and phase gates.

### Examples

Debug a reported bug:
```
/4phase-debugging "Users can't upload files larger than 5MB"
```

Resume at a specific phase:
```
/4phase-debugging --issue "GH-#287" --phase 3
```
