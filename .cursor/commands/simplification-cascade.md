## Simplification Cascade

Decompose complex functions into smaller, composable pieces through sequential, layer-by-layer refactoring passes.

### Usage

```
/simplification-cascade "src/services/orderProcessor.ts:processOrder"
/simplification-cascade "backend/handlers/billing.go" --levels 1-3
/simplification-cascade "src/legacy/reportGenerator.ts"
```

### Workflow

1. **Audit** — Measure line count, nesting depth, cyclomatic complexity, concern count, and implicit state
2. **Flatten** — Convert deep nesting to guard clauses (max depth ≤ 2)
3. **Extract** — Pull pure logic blocks into named functions (≤ 20 lines each)
4. **Separate** — Split by concern (fetch, validate, transform, persist)
5. **Explicit State** — Replace mutable shared variables with parameters and return values
6. **Pipeline** — Compose extracted functions into a readable top-level pipeline
7. **Snapshot** — Compare before/after metrics and verify all tests pass

### Execution

Read and follow the `simplification-cascade` skill (`.cursor/skills/review/simplification-cascade/SKILL.md`) for the full 5-level cascade workflow.

### Examples

Simplify a legacy handler:
```
/simplification-cascade "src/legacy/checkoutHandler.ts:handleCheckout"
```

Partial cascade (only flatten + extract):
```
/simplification-cascade "src/services/parser.ts" --levels 1-2
```
