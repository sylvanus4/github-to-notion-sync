# AI Platform Policy Document (v0.7)

| Author | Last Updated |
|--------|-------------|
| 김해림 | 2026.01.23 (Initial) |

> **AI Platform 0.7v 기준으로 만들어진 리소스에 대한 상태값과 액션 그리고 필수/선택 여부에 대한 정책서입니다.**

This document defines the resource lifecycle policies for AI Platform v0.7, including:

- **Status definitions** for each resource type (possible states and available actions per state)
- **Create/Edit form field specifications** (field name, required/optional, editable, category, description)
- **Open questions** that still need resolution

---

## Table of Contents

| # | Category | Document | Description |
|---|----------|----------|-------------|
| 1 | Hub | [01-hub.md](01-hub.md) | Packages, Models Status, Dataset |
| 2 | Infrastructure | [02-infrastructure.md](02-infrastructure.md) | Workloads, My Template, Storage (Volumes), Serverless |
| 3 | ML Studio | [03-ml-studio.md](03-ml-studio.md) | Text Generation, Tabular |
| 4 | MLOps | [04-mlops.md](04-mlops.md) | DevSpace, Pipeline Builder, Benchmark |
| 5 | Operations | [05-operations.md](05-operations.md) | Kueue, Monitoring, Dependencies, Cluster Management |
| - | Open Questions | [open-questions.md](open-questions.md) | Consolidated list of unresolved items |

---

## Open Questions Summary

| Category | Count | Key Issues |
|----------|-------|------------|
| Infrastructure | 6 | Serverless visibility policy, Storage "In use" actions, Registry Credentials verification, NameSpace field naming, Snapshot Create fields TBD |
| ML Studio | 1 | Tabular Train Data Ratio display format |
| Operations | 3 | Entire section not fully organized, Kueue queue status types unknown, Metrics naming uncertain |
| **Total** | **10** | |

For full details, see [open-questions.md](open-questions.md).
