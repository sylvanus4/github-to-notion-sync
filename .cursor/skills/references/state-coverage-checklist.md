# State Coverage Checklist

Template for tracking spec-to-code coverage in `spec-state-validator`.

## Checklist Format

Each spec artifact becomes a checklist item:

```markdown
## [Feature/Component Name]

### States
- [ ] State: [name] — Expected: [description] — Code: [file:line or "NOT FOUND"]
- [ ] State: [name] — Expected: [description] — Code: [file:line or "NOT FOUND"]

### Transitions
- [ ] [FromState] → [ToState] via [trigger] — Code: [file:line or "NOT FOUND"]
- [ ] [FromState] → [ToState] via [trigger] — Code: [file:line or "NOT FOUND"]

### Edge Cases
- [ ] EC-1: [scenario] — Expected: [behavior] — Code: [file:line or "NOT FOUND"]
- [ ] EC-2: [scenario] — Expected: [behavior] — Code: [file:line or "NOT FOUND"]

### Business Rules
- [ ] BR-1: [rule] — Code: [file:line or "NOT FOUND"]

### Error Handling
- [ ] ERR-1: [error scenario] — Expected: [handling] — Code: [file:line or "NOT FOUND"]

### Policy Constraints
- [ ] POL-1: [policy requirement] — Code: [file:line or "NOT FOUND"]
```

## Common State Patterns to Check

### CRUD Lifecycle
- [ ] Created / New / Draft
- [ ] Active / Published / Live
- [ ] Updated / Modified
- [ ] Deleted / Archived / Removed
- [ ] Restored (if soft delete)

### Approval Workflow
- [ ] Draft
- [ ] Submitted / Pending Review
- [ ] Under Review
- [ ] Approved
- [ ] Rejected
- [ ] Revision Requested
- [ ] Published / Final

### Payment / Transaction
- [ ] Initiated
- [ ] Processing
- [ ] Succeeded / Completed
- [ ] Failed
- [ ] Refunded
- [ ] Partially Refunded
- [ ] Cancelled
- [ ] Disputed

### User Account
- [ ] Unverified / Pending
- [ ] Active
- [ ] Suspended
- [ ] Banned
- [ ] Deactivated
- [ ] Deleted

## Edge Case Categories

Always check these categories when validating spec coverage:

### Data Edge Cases
- [ ] Empty/null input
- [ ] Maximum length input
- [ ] Special characters (unicode, emoji, HTML tags)
- [ ] Zero quantity / zero amount
- [ ] Negative values
- [ ] Decimal precision

### Timing Edge Cases
- [ ] Concurrent operations on same resource
- [ ] Operation timeout
- [ ] Clock skew between systems
- [ ] Scheduled action at boundary (midnight, DST transition)
- [ ] Retry during in-progress operation

### Permission Edge Cases
- [ ] Role transition during active session
- [ ] Resource ownership change
- [ ] Feature flag toggle during operation
- [ ] Multi-tenant data isolation

### Network Edge Cases
- [ ] API timeout
- [ ] Partial response
- [ ] Retry with changed data
- [ ] Offline/reconnection state
- [ ] Rate limit hit

## Code Search Patterns

Efficient grep patterns for finding spec implementations:

```bash
# Find state enums/unions
rg "enum.*Status|type.*Status|status.*=.*'" --type ts

# Find state transitions
rg "\.status\s*=|setState|dispatch.*type.*STATUS" --type ts

# Find error handling
rg "catch|throw new|Error\(|reject\(" --type ts

# Find guard clauses
rg "if\s*\(!|if\s*\(.*===\s*null|if\s*\(.*===\s*undefined" --type ts

# Find boundary checks
rg "\.length\s*(===|>|<|>=|<=)\s*\d|Math\.(min|max)" --type ts

# Find permission checks
rg "isAdmin|hasPermission|canAccess|authorize|role\s*===|checkAuth" --type ts
```

## Coverage Calculation

```
Coverage % = (Covered + Partially Covered × 0.5) / Total Artifacts × 100

Thresholds:
- 95-100%: Excellent — ready for release
- 80-94%:  Good — minor gaps acceptable for non-critical features
- 60-79%:  Needs Work — significant gaps, review before release
- Below 60%: Poor — major implementation gaps, block release
```
