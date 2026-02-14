# 5. Operations

> **Note:** This entire section is not fully organized yet ("전체 아직 정리 못함").

## 5-1. Kueue

### Setting Queues Status

> **OPEN QUESTION:** Queue status types are unknown ("종류를 모르겠음"). Currently only `active` is identified.

### Kueue Components

- **ClusterQueues**
- **LocalQueues**

### Performance Metrics

| Metric | Description |
|--------|-------------|
| Avg Queue Wait Time | Average time workloads spend waiting in queue |
| Workloads per Hour (Throughput) | Number of workloads processed per hour |
| Completion Rate (Success Rate) | Rate of successfully completed workloads |
| Scheduling Efficiency (Queue Efficiency) | Overall queue scheduling efficiency |

### Scheduler Metrics

| Metric | Description |
|--------|-------------|
| Total Decisions | Total number of scheduling decisions made |
| Success Rate | Rate of successful scheduling decisions |
| Avg Queue Time (Pending?) | Average queue time |
| Avg Decision Time (Rejected?) | Average decision time |

> **OPEN QUESTION:** Metric names "Avg Queue Time (Pending?)" and "Avg Decision Time (Rejected?)" need clarification on the parenthetical labels.

### 5-1-2. Priority

| Priority Level |
|---------------|
| Default |
| Development |
| Training |
| Critical |
| Inference |
| Batch |

### 5-1-2. Kueue - Workloads Status

#### Workload Admission Status

| Status |
|--------|
| Pending |
| Admitted |
| Running |

#### Workload Execution Status

| Status |
|--------|
| Pending |
| Running |
| Suspended |
| Completed |
| Cancelled |
| Failed |

---

## 5-2. Monitoring

### 5-2-1. Nodes Status

| Status | Glance Code | Description |
|--------|-------------|-------------|
| Ready | - | Node is available (Kubernetes native status) |
| Not Ready | - | Node is unavailable (Kubernetes native status) |

---

## 5-3. Dependencies

### 5-3-1. SBOM Status

- Contains library license information.

> Detailed status values are not yet documented.

---

## 5-4. Cluster Management

### 5-4-1. Cluster Status

> Detailed status values are not yet documented.
