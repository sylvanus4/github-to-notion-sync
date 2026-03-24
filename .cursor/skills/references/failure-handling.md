# Failure Handling Strategy

How the office-template-enforcer handles errors at each stage.

## Hard Fail Conditions

These block output delivery. The file is NOT returned to the user.

| Condition | Stage | Action |
|-----------|-------|--------|
| No matching template found | Template Selection | Ask the user which template to use |
| Required placeholder unfilled | Validation | Regenerate the JSON spec for the missing slots |
| Unauthorized layout used (PPTX) | Validation | Regenerate with correct layout IDs |
| Unauthorized style used (DOCX) | Validation | Strip style and use template default |
| Template file corrupted or missing | Pre-generation | Report error, ask user to verify template path |
| Header/footer missing in output | Validation | Re-run generation from template copy |
| Residual {{MARKER}} in output | Validation | Identify unfilled markers and regenerate |

## Soft Fail Conditions

These generate warnings but the file is still returned.

| Condition | Stage | Auto-fix Strategy |
|-----------|-------|-------------------|
| Text exceeds max_chars | Validation | Truncate with "..." and warn user |
| Bullet count exceeds max_items | Validation | Group items, move overflow to notes |
| Non-standard font detected | Validation | Warn user (font may be from paste) |
| Heading level skip | Validation | Warn user about hierarchy gap |
| Excessive direct formatting | Validation | Warn user, suggest style-based approach |
| Slide count mismatch | Validation | Warn user about extra/missing slides |
| Chart area overflow | Validation | Warn user to simplify data |

## Recovery Flow

```
Generation failed?
  ├─ Hard fail
  │   ├─ Identify specific violation
  │   ├─ Adjust JSON spec to fix
  │   ├─ Re-run generation (max 2 retries)
  │   └─ If still failing: report to user with details
  └─ Soft fail
      ├─ Apply auto-fix if available
      ├─ Add warning to report
      └─ Return file with warning summary
```

## Retry Budget

- Maximum 2 automatic retries per generation
- Each retry adjusts the JSON spec based on the validation report
- After 2 failed retries, report the issue to the user with:
  - The specific violations
  - The attempted fixes
  - Suggestions for manual resolution

## User Communication

When reporting failures, always include:
1. Which rule was violated (rule ID and description)
2. Where in the document (slide number or section name)
3. What the expected behavior was
4. What actually happened
5. Suggested fix action
