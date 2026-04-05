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

## Batch Field Setting Pattern — MANDATORY Script

Every issue added to Project #5 MUST have ALL 5 fields set. Use this self-contained Python script pattern. The agent MUST run this after every `gh project item-add`:

```python
import subprocess, json

PROJECT_ID = 'PVT_kwDODHOnas4A9FHM'
FIELD = {
    'status':   'PVTSSF_lADODHOnas4A9FHMzgw46Tk',
    'priority': 'PVTSSF_lADODHOnas4A9FHMzgw46qc',
    'size':     'PVTSSF_lADODHOnas4A9FHMzgw46qg',
    'sprint':   'PVTIF_lADODHOnas4A9FHMzgw46qo',
    'estimate': 'PVTF_lADODHOnas4A9FHMzgw46qk',
}
OPT = {
    'done': '98236657', 'p2': '473ded73', 's': '434b26a1',
}

def get_current_sprint():
    """Return the iteration ID whose date range contains today."""
    from datetime import date, timedelta
    q = '''query { organization(login: "ThakiCloud") {
      projectV2(number: 5) { fields(first: 50) { nodes {
        ... on ProjectV2IterationField { id configuration {
          iterations { id title startDate duration }
        }}
      }}}
    }}'''
    r = subprocess.run(['gh','api','graphql','-f',f'query={q}'],
                       capture_output=True, text=True)
    data = json.loads(r.stdout)
    today = date.today()
    for node in data['data']['organization']['projectV2']['fields']['nodes']:
        if 'configuration' in node:
            for it in node['configuration']['iterations']:
                start = date.fromisoformat(it['startDate'])
                end = start + timedelta(days=it['duration'])
                if start <= today < end:
                    return it['id']
            iters = node['configuration']['iterations']
            if iters:
                return iters[-1]['id']
    return None

def gql_mutation(item_id, field_id, value, vtype='singleSelectOptionId'):
    q = f'''mutation {{ updateProjectV2ItemFieldValue(input: {{
      projectId: "{PROJECT_ID}" itemId: "{item_id}"
      fieldId: "{field_id}" value: {{{vtype}: "{value}"}}
    }}) {{ projectV2Item {{ id }} }} }}'''
    return subprocess.run(['gh','api','graphql','-f',f'query={q}'],
                          capture_output=True, text=True).returncode == 0

def set_number(item_id, field_id, value):
    q = f'''mutation {{ updateProjectV2ItemFieldValue(input: {{
      projectId: "{PROJECT_ID}" itemId: "{item_id}"
      fieldId: "{field_id}" value: {{number: {value}}}
    }}) {{ projectV2Item {{ id }} }} }}'''
    return subprocess.run(['gh','api','graphql','-f',f'query={q}'],
                          capture_output=True, text=True).returncode == 0

def auto_size(file_count):
    """Determine Size option ID based on file count."""
    if file_count <= 2:
        return '84ca859b'   # XS
    elif file_count <= 5:
        return '434b26a1'   # S
    elif file_count <= 10:
        return 'ba4bcc7c'   # M
    elif file_count <= 20:
        return 'f38a3a9e'   # L
    else:
        return '2f3f024c'   # XL

def auto_estimate(file_count):
    """Determine story points based on file count."""
    if file_count <= 3:
        return 1
    elif file_count <= 8:
        return 2
    elif file_count <= 15:
        return 3
    else:
        return 5

def set_all_fields(item_id, sprint_id, estimate=1, label='',
                   size_id=None, priority_id=None, status_id=None,
                   file_count=0):
    """Set ALL 5 mandatory fields on a project item.

    If size_id is not given and file_count > 0, auto-determines size.
    If estimate is default (1) and file_count > 0, auto-determines estimate.
    """
    _status   = status_id   or OPT['done']
    _priority = priority_id or OPT['p2']
    _size     = size_id     or (auto_size(file_count) if file_count else OPT['s'])
    _estimate = estimate if estimate != 1 or file_count == 0 else auto_estimate(file_count)

    print(f'  Setting fields for {label or item_id}...')
    ok = all([
        gql_mutation(item_id, FIELD['status'],   _status),
        gql_mutation(item_id, FIELD['priority'],  _priority),
        gql_mutation(item_id, FIELD['size'],      _size),
        gql_mutation(item_id, FIELD['sprint'],    sprint_id, 'iterationId'),
        set_number(item_id, FIELD['estimate'], _estimate),
    ])
    print(f'  => {"OK" if ok else "PARTIAL FAILURE"}')
    return ok

def get_item_id_for_issue(repo, issue_number):
    """Find project item ID for a specific issue."""
    q = f'''query {{ organization(login: "ThakiCloud") {{
      projectV2(number: 5) {{ items(last: 30) {{ nodes {{
        id content {{ ... on Issue {{
          number repository {{ nameWithOwner }}
        }}}}
      }}}}}}
    }}}}'''
    r = subprocess.run(['gh','api','graphql','-f',f'query={q}'],
                       capture_output=True, text=True)
    data = json.loads(r.stdout)
    for item in data['data']['organization']['projectV2']['items']['nodes']:
        c = item.get('content', {})
        if c and c.get('number') == issue_number:
            r_name = c.get('repository', {}).get('nameWithOwner', '')
            if repo in r_name:
                return item['id']
    return None

# Usage in pipeline:
# sprint_id = get_current_sprint()
# item_id = get_item_id_for_issue('ThakiCloud/repo-name', 42)
# set_all_fields(item_id, sprint_id, label='#42', file_count=6)
```

### Default Assignee

All issues created by this pipeline MUST be assigned to `sylvanus4`.

### Field Defaults

| Field | Default | When to Override |
|-------|---------|-----------------|
| Status | Done (`98236657`) | Use "In Progress" for WIP issues |
| Priority | P2 (`473ded73`) | Use P1 for critical, P0 for urgent |
| Size | Auto by file count | Override with explicit size_id |
| Sprint | Current sprint (query by date) | Never override — always use current |
| Estimate | Auto by file count | Override with explicit value |

### Auto-Sizing Guide

| Files Changed | Size | Estimate (SP) |
|--------------|------|---------------|
| 1-2 | XS (`84ca859b`) | 1 |
| 3-5 | S (`434b26a1`) | 2 |
| 6-10 | M (`ba4bcc7c`) | 2 |
| 11-20 | L (`f38a3a9e`) | 3 |
| 21+ | XL (`2f3f024c`) | 5 |
