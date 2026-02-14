# Open Questions & Unresolved Items

This document consolidates all uncertainties, undefined items, and open questions found in the AI Platform v0.7 policy specification. Each item is categorized by its source section and includes the original context.

---

## Infrastructure (6 items)

### Q1. Deploy New Pod - "NameSpace?" field naming

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-1-3. Deploy New Pod
- **Context:** The field is listed as `NameSpace?` with a question mark, suggesting the field name itself is uncertain.
- **Action needed:** Confirm the correct field name and whether namespace selection is actually required.

### Q2. Serverless - Public/Private visibility setting

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-4. Serverless
- **Original text:** "public, private: create 페이지에서 설정하도록 제공할지 정확하지 않음"
- **Context:** It is unclear whether the create endpoint page should provide public/private visibility settings.
- **Action needed:** Decide whether visibility should be configurable at endpoint creation time.

### Q3. Storage Volumes - "In use" status actions

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-3-1. Storage Volumes Status
- **Original text:** Available actions listed as "?"
- **Context:** When a storage volume is in use, the available actions have not been defined.
- **Action needed:** Define what actions (if any) are available when a volume is actively in use.

### Q4. My Template - Registry Credentials description

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-2-1. My Template Create & Edit
- **Original text:** "내용 맞는지 확인 필요"
- **Context:** The description for Registry Credentials says "Credentials used to pull images from a private registry. Not required for public images." -- this needs verification.
- **Action needed:** Verify the description accuracy with the backend/DevOps team.

### Q5. Serverless vLLM - visibility description

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-4-2. vLLM Create & Edit
- **Original text:** "내용 맞는지 확인 필요"
- **Context:** The description for visibility says "Controls whether this endpoint is accessible publicly or only within the internal network." -- this needs verification.
- **Action needed:** Verify with backend team whether this accurately describes the visibility behavior.

### Q6. Docker Image - Env variables & Registry Credentials descriptions

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-4-3. Docker Image Create & Edit
- **Original text:** "내용 맞는지 확인 필요"
- **Context:** Descriptions for both Env variables ("Add a single environment variable") and Registry Credentials ("Select credentials to pull the image from a private registry") need verification.
- **Action needed:** Verify description accuracy.

---

## Infrastructure - Snapshot (1 item)

### Q7. Snapshot Create & Edit - All fields TBD

- **Location:** [02-infrastructure.md](02-infrastructure.md) > 2-3-4. Snapshot Create & Edit
- **Context:** The entire create/edit specification for snapshots is empty. No fields have been defined yet.
- **Action needed:** Define the required and optional fields for snapshot creation and editing.

---

## ML Studio (1 item)

### Q8. Tabular - Train Data Ratio display format

- **Location:** [03-ml-studio.md](03-ml-studio.md) > 3-2-2. Tabular Create > Validation Strategy
- **Original text:** "굳이 이렇게 보여줘야하나.. 그냥 퍼센티지로 나누면 앙대나.."
- **Context:** The current Train Data Ratio shows separate Train/Validation/Test sections. The question is whether a simple percentage-based split would be more appropriate.
- **Action needed:** Decide on the UI representation -- separate ratio sections vs. simple percentage input.

---

## Operations (3 items)

### Q9. Operations section - Not fully organized

- **Location:** [05-operations.md](05-operations.md)
- **Original text:** "전체 아직 정리 못함"
- **Context:** The entire Operations section (Kueue, Monitoring, Dependencies, Cluster Management) is acknowledged as incomplete.
- **Action needed:** Complete the operations section with full status definitions, actions, and create/edit fields.

### Q10. Kueue - Queue status types unknown

- **Location:** [05-operations.md](05-operations.md) > 5-1. Kueue
- **Original text:** "종류를 모르겠음"
- **Context:** The setting queues status types are unknown. Only `active` has been identified so far.
- **Action needed:** Identify and document all possible queue status types.

### Q11. Kueue Metrics - Metric naming uncertain

- **Location:** [05-operations.md](05-operations.md) > 5-1. Kueue > Scheduler Metrics
- **Original text:** "Avg Queue Time (Pending?)", "Avg Decision Time (Rejected?)"
- **Context:** The parenthetical labels on these metrics suggest uncertainty about whether "Pending" and "Rejected" are the correct qualifiers.
- **Action needed:** Confirm the correct metric names and their definitions.

---

## Summary

| Category | Open Items | Priority |
|----------|-----------|----------|
| Infrastructure | 7 | High -- core resource creation flows affected |
| ML Studio | 1 | Medium -- UI/UX decision |
| Operations | 3 | High -- entire section incomplete |
| **Total** | **11** | |
