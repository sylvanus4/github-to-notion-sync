# Common Quality Gaps

Frequently found quality issues in planning documents and how to fix them.

## Structure Gaps

| Gap | Frequency | Fix |
|-----|-----------|-----|
| Missing success metrics | Very common | Add measurable KPIs with baselines and targets |
| No non-functional requirements | Common | Add sections for performance, security, accessibility |
| Missing open questions | Common | Review each requirement for unresolved decisions |
| No version history | Occasional | Add document metadata table |

## State Coverage Gaps

| Gap | Frequency | Impact |
|-----|-----------|--------|
| No error states defined | Very common | Dev team invents error handling, inconsistent UX |
| No empty state | Common | Users see broken layouts or confusing screens |
| No loading state | Common | Users think the app is frozen |
| No offline behavior | Occasional | App crashes or shows cryptic errors |

### Quick Fix Template

For each missing state, add:
```markdown
**[State Name]:**
- 화면 표시: [what the user sees]
- 사용자 액션: [what the user can do]
- 시스템 동작: [what happens next]
```

## Edge Case Gaps

| Gap | Frequency | Impact |
|-----|-----------|--------|
| No concurrent access handling | Very common | Data corruption, race conditions |
| No boundary values | Common | Crashes at limits |
| No back-button behavior | Common | Lost data, broken navigation |
| No session expiry handling | Occasional | Confusing re-auth flows |

## Policy Gaps

| Gap | Frequency | Impact |
|-----|-----------|--------|
| No privacy policy reference for data collection | Common | Compliance risk |
| Payment features without refund policy | Occasional | Legal risk |
| User-generated content without moderation policy | Occasional | Liability risk |

## Testability Gaps

| Gap | Frequency | Fix |
|-----|-----------|-----|
| Vague adjectives ("적절한", "충분한") | Very common | Replace with specific numbers |
| No acceptance criteria | Common | Add Given-When-Then format |
| Unmeasurable success metrics | Occasional | Add baselines, targets, measurement methods |
