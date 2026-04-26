# Project Configuration Reference

Default target: **ThakiCloud Project #5** (AI 플랫폼 팀)

## Project ID

```
PVT_kwDODHOnas4A9FHM
```

## Field IDs

| Field | Field ID | Type |
|-------|----------|------|
| Status | `PVTSSF_lADODHOnas4A9FHMzgw46Tk` | SINGLE_SELECT |
| Sprint (스프린트) | `PVTIF_lADODHOnas4A9FHMzgw46qo` | ITERATION |

## Status Options

| Name | Option ID |
|------|-----------|
| Todo | `f75ad846` |
| In Progress | `47fc9ee4` |
| Done | `98236657` |

## Default Assignee

`sylvanus4`

## Pagination

Project #5 has 400+ items. Always paginate with `first: 100` and use `pageInfo { hasNextPage endCursor }`.

## Sprint Discovery Query

Sprint IDs rotate every week. Always query current iterations before setting:

```bash
gh api graphql -f query='
query {
  organization(login: "ThakiCloud") {
    projectV2(number: 5) {
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
}'
```

Pick the iteration where `startDate ≤ today < startDate + (duration × 7 days)`.

## GraphQL Scan Query Template

```graphql
query($cursor: String) {
  organization(login: "ThakiCloud") {
    projectV2(number: 5) {
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
              ... on ProjectV2ItemFieldIterationValue {
                title
                field { ... on ProjectV2IterationField { name } }
              }
            }
          }
          content {
            ... on Issue {
              number title
              assignees(first: 5) { nodes { login } }
            }
          }
        }
      }
    }
  }
}
```

## jq Filter Template

Replace `TARGET_USER` and `TARGET_SPRINT` before use:

```jq
[.data.organization.projectV2.items.nodes[]
  | select(.content != null)
  | select(.content.assignees != null)
  | select(.content.assignees.nodes | map(.login) | index("TARGET_USER"))
  | {
      item_id: .id,
      number: .content.number,
      title: .content.title,
      status: ([.fieldValues.nodes[] | select(.field.name == "Status")] | first | .name // "none"),
      sprint: ([.fieldValues.nodes[] | select(.field.name == "스프린트")] | first | .title // "none")
    }
  | select(.status == "Todo" or .status == "In Progress")
  | select(.sprint != "TARGET_SPRINT")]
```

## Mutation Template

```graphql
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwDODHOnas4A9FHM"
    itemId: "ITEM_ID"
    fieldId: "PVTIF_lADODHOnas4A9FHMzgw46qo"
    value: { iterationId: "ITERATION_ID" }
  }) {
    projectV2Item { id }
  }
}
```
