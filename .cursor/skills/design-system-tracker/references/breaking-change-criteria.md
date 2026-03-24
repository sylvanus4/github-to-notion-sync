# Breaking Change Criteria

Classification rules for design system changes.

## Breaking Changes

A change is **breaking** if it requires consuming code or design to be updated.

### Component Level

| Change | Breaking? | Reason |
|--------|-----------|--------|
| Component removed | YES | All instances broken |
| Component renamed | YES | Import/reference paths broken |
| Required prop added | YES | Existing instances missing required prop |
| Prop renamed | YES | Existing prop values ignored |
| Prop type changed | YES | Existing values may be invalid |
| Default prop value removed | YES | Behavior change for existing instances |
| Layout structure changed (DOM) | YES | CSS selectors and tests may break |

### Token Level

| Change | Breaking? | Reason |
|--------|-----------|--------|
| Token removed | YES | All references broken |
| Token renamed | YES | All references broken |
| Token value changed (>20% delta) | YES | Significant visual change |
| Token value changed (<20% delta) | MAYBE | Review visual impact case by case |
| Token type changed (color → spacing) | YES | Semantic mismatch |

## Non-Breaking Changes

| Change | Why Non-Breaking |
|--------|-----------------|
| New component added | Existing code unaffected |
| New optional prop added | Existing instances work without it |
| New variant added | Existing variants unchanged |
| Token value fine-tuned (<10% delta) | Minimal visual impact |
| Component documentation updated | No runtime impact |

## Deprecation

A change is a **deprecation** when:
- Component/token is marked `@deprecated` but still functional
- A replacement is available and documented
- A removal timeline is communicated

Deprecation is NOT a breaking change, but requires migration planning.

## Impact Assessment Matrix

| Change Severity | Code Impact | Design Impact | Action Required |
|----------------|-------------|---------------|-----------------|
| Breaking | Must update | Must update | Immediate migration |
| Non-breaking | No action | Review visual | Optional |
| Deprecation | Plan migration | Plan migration | Timeline-based |
