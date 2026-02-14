# 4. MLOps

## 4-1. DevSpace

### 4-1-1. DevSpace Status

- Initial status after creation: `pending`

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Running | `Running` | Web Access, Delete |
| Pending | `pending` | Delete |
| Succeeded | `Succeded` | - |
| Failed | `Failed` | - |
| Stopped | `Stopped` | - |

### 4-1-2. DevSpace Create

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| DevSpace Name | 기본정보 | Yes | Yes | Yes | |
| CPU Request | Instance | Yes | Yes | Yes | |
| GPU Type | Instance | - | - | Yes | Options: GPU No, NVIDIA GPU |
| Memory Request | Instance | - | - | Yes | |
| Storage Size | Instance | - | - | Yes | |

---

## 4-2. Pipeline Builder

> No detailed specification available yet.

---

## 4-3. Benchmark

- Clicking the **Benchmark** button on a Serverless endpoint creates a benchmark entry.
- No redirection occurs after benchmark creation.
