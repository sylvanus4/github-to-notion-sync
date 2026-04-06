# Notion Schema Reference

## 1. Weekly Release Database

**Page title format**: `Weekly Release - YYYY-MM-DD` (Thursday date)

### Properties

| Property | Type | Valid Values | Required |
|---|---|---|---|
| App | Select | `AI-Platform`, `Agent Studio`, `Other` | Yes |
| Title | Title (page title) | Free text — PR title or feature name | Yes |
| GitHub Issue | URL | `https://github.com/{org}/{repo}/issues/{N}` | No |
| GitHub PR | URL | `https://github.com/{org}/{repo}/pull/{N}` | Yes |
| Assignee | Person | Notion workspace member | Yes |
| Status | Select | See status values below | Yes |
| QA Status | Select | `Not Started`, `In Progress`, `Pass`, `Fail`, `Conditional Pass` | Yes |
| Risk | Select | `Low`, `Medium`, `High` | Yes |
| Business Team Share | Checkbox | true/false | Yes |
| QA Team Share | Checkbox | true/false | Yes |
| Release Inclusion | Select | `Included`, `Excluded`, `Deferred` | Yes |
| Deploy Purpose | Select | `Feature`, `Bugfix`, `Hotfix` | Yes |
| Rollback Plan | Rich Text | Free text — rollback steps | Yes |

### Status Transition Rules

```
Draft → Collected → Ready for QA → QA Passed → Ready for Release → Released
                                  → Hold (from any QA state)
```

- `Draft`: App owner created the entry, not yet reviewed
- `Collected`: Included in Tuesday's candidate list
- `Ready for QA`: Assigned to QA, environment prepared
- `QA Passed`: QA completed with Pass result
- `Hold`: QA failed or blocked — requires resolution before release
- `Ready for Release`: Final approval given, deployment-ready
- `Released`: Successfully deployed on Thursday

### Transition Constraints

- Only items with `QA Passed` status can transition to `Ready for Release`
- Items in `Hold` must return to `Ready for QA` before progressing
- `Released` is a terminal state — no backward transitions

---

## 2. Hotfix Queue Database

**Page title**: `Hotfix Queue` (persistent, not date-based)

### Properties

| Property | Type | Valid Values | Required |
|---|---|---|---|
| App | Select | `AI-Platform`, `Agent Studio`, `Other` | Yes |
| Title | Title (page title) | Free text — hotfix summary | Yes |
| Urgency | Select | `Critical`, `High`, `Medium` | Yes |
| Customer Impact | Rich Text | Who is affected, how severely | Yes |
| Business Impact | Rich Text | Revenue, SLA, reputation risk | Yes |
| Request Background | Rich Text | Why this hotfix is needed | Yes |
| GitHub PR | URL | `https://github.com/{org}/{repo}/pull/{N}` | Yes |
| Assignee | Person | Notion workspace member | Yes |
| Status | Select | `Requested`, `In Progress`, `QA`, `Ready`, `Deployed`, `Cancelled` | Yes |
| Business Notification | Checkbox | true/false | Yes |
| QA Completion | Checkbox | true/false | Yes |
| Requested Date | Date | ISO 8601 | Yes |
| Deployed Date | Date | ISO 8601 | No |

### Status Transition Rules

```
Requested → In Progress → QA → Ready → Deployed
                              → Cancelled (from any state)
```

---

## 3. Query Patterns

### Get current week's release items
```
Filter: Status != "Released" AND Status != "Hold"
Sort: Risk DESC, App ASC
```

### Get items pending QA
```
Filter: Status == "Ready for QA" AND QA Status != "Pass"
Sort: Risk DESC
```

### Get deployment-ready items
```
Filter: Status == "Ready for Release"
Sort: App ASC
```

### Get active hotfixes
```
Filter: Status != "Deployed" AND Status != "Cancelled"
Sort: Urgency DESC
```
