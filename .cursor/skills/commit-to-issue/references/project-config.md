# Project Configuration Reference

Default target: **ThakiCloud Project #5** (AI 플랫폼 팀)

## Project ID

```
PVT_kwDODHOnas4A9FHM
```

## Field IDs and Options

| Field | Field ID | Type |
|-------|----------|------|
| Status | `PVTSSF_lADODHOnas4A9FHMzgw46Tk` | SINGLE_SELECT |
| Priority | `PVTSSF_lADODHOnas4A9FHMzgw46qc` | SINGLE_SELECT |
| Size | `PVTSSF_lADODHOnas4A9FHMzgw46qg` | SINGLE_SELECT |
| Sprint | `PVTIF_lADODHOnas4A9FHMzgw46qo` | ITERATION |
| Estimate | `PVTF_lADODHOnas4A9FHMzgw46qk` | NUMBER |

### Status Options

| Name | Option ID |
|------|-----------|
| Epic | `ce4116bf` |
| Todo | `f75ad846` |
| In Progress | `47fc9ee4` |
| Done | `98236657` |
| 25-Archive | `bc27fa6e` |

### Priority Options

| Name | Option ID |
|------|-----------|
| P0 | `15f21a51` |
| P1 | `87367794` |
| P2 | `473ded73` |

### Size Options

| Name | Option ID |
|------|-----------|
| XS | `84ca859b` |
| S | `434b26a1` |
| M | `ba4bcc7c` |
| L | `f38a3a9e` |
| XL | `2f3f024c` |

## Sprint Query

Sprint IDs rotate. Always query current sprints before setting:

```bash
gh api graphql -f query='
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      fields(first: 50) {
        nodes {
          ... on ProjectV2IterationField {
            id name
            configuration {
              iterations { id title startDate duration }
            }
          }
        }
      }
    }
  }
}' -f owner='ThakiCloud' -F number=5
```

Pick the iteration whose date range contains today. Note: the Sprint field is named `스프린트` in project #5.

## Add Issue to Project

```bash
gh project item-add 5 --owner ThakiCloud --url $ISSUE_URL
```

## Query Project Item ID

After adding, retrieve the item ID for field edits:

```bash
gh api graphql -f query='
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      items(last: 20) {
        nodes {
          id
          content {
            ... on Issue {
              number title
              repository { nameWithOwner }
            }
          }
        }
      }
    }
  }
}' -f org='ThakiCloud' -F number=5
```

Filter results by `repository.nameWithOwner` matching the target repo.

## Set Project Fields

### Single-select fields (Status, Priority, Size)

```bash
gh project item-edit \
  --id $ITEM_ID \
  --field-id $FIELD_ID \
  --single-select-option-id $OPTION_ID \
  --project-id $PROJECT_ID
```

### Iteration field (Sprint)

```bash
gh project item-edit \
  --id $ITEM_ID \
  --field-id $SPRINT_FIELD_ID \
  --iteration-id $ITERATION_ID \
  --project-id $PROJECT_ID
```

### Number field (Estimate)

```bash
gh project item-edit \
  --id $ITEM_ID \
  --field-id $ESTIMATE_FIELD_ID \
  --number $ESTIMATE_VALUE \
  --project-id $PROJECT_ID
```

## Batch Field Setting Pattern

Use a zsh function for efficiency:

```zsh
set_fields() {
  local ITEM_ID=$1 ESTIMATE=$2 LABEL=$3
  echo "=== $LABEL (estimate: $ESTIMATE) ==="
  gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD" --single-select-option-id "$STATUS_OPTION" --project-id "$PROJECT_ID"
  gh project item-edit --id "$ITEM_ID" --field-id "$PRIORITY_FIELD" --single-select-option-id "$PRIORITY_OPTION" --project-id "$PROJECT_ID"
  gh project item-edit --id "$ITEM_ID" --field-id "$SIZE_FIELD" --single-select-option-id "$SIZE_OPTION" --project-id "$PROJECT_ID"
  gh project item-edit --id "$ITEM_ID" --field-id "$SPRINT_FIELD" --iteration-id "$SPRINT_ID" --project-id "$PROJECT_ID"
  gh project item-edit --id "$ITEM_ID" --field-id "$ESTIMATE_FIELD" --number "$ESTIMATE" --project-id "$PROJECT_ID"
}
```
