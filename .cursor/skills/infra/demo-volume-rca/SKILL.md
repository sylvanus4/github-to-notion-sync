---
name: demo-volume-rca
version: 1.0.0
category: infra/rca
description: >
  Systematic RCA for AI Platform Demo Storage (Volume/Snapshot/Restore) errors.
  Guides through PVC/VolumeSnapshot lifecycle inspection, DB status queries,
  K8s resource checks, and a decision tree mapping storage states to root causes.
triggers:
  - "debug volume"
  - "volume error"
  - "volume failed"
  - "volume RCA"
  - "PVC error"
  - "PVC failed"
  - "snapshot error"
  - "snapshot failed"
  - "restore error"
  - "restore failed"
  - "storage error"
  - "storage RCA"
  - "볼륨 에러"
  - "볼륨 장애"
  - "볼륨 원인 분석"
  - "PVC 에러"
  - "스냅샷 에러"
  - "복원 에러"
  - "스토리지 장애"
  - "스토리지 트러블슈팅"
  - "demo-volume-rca"
do_not_use:
  - "For Workload errors → use demo-workload-rca"
  - "For Serverless/Endpoint errors → use demo-serverless-rca"
  - "For Pipeline Builder errors → use demo-pipeline-rca"
  - "For Text Generation errors → use demo-text-generation-rca"
  - "For Tabular errors → use demo-tabular-rca"
  - "For Benchmark errors → use demo-benchmark-rca"
  - "For DevSpace errors → use demo-devspace-rca"
  - "For production environment troubleshooting"
---

# Demo Volume (Storage) RCA Skill

Systematic root-cause analysis for AI Platform Demo **Storage** errors covering Volumes (PVCs), VolumeSnapshots, and Restore operations.

---

## Pre-flight

```bash
# 1. VPN connected to Demo cluster
# 2. Switch kubectl context
kubectx demo

# 3. Port-forward PostgreSQL (CNPG cluster in postgresql namespace)
kubectl port-forward -n postgresql svc/ai-platform-db-rw 5432:5432 &
```

---

## Step 1 — DB Status Query (Volumes)

```sql
-- Failed / stuck volumes
SELECT id, project_id, name, status, size_gb, storage_class,
       error_message,
       to_timestamp(created_at) AS created,
       to_timestamp(updated_at) AS updated,
       ROUND(EXTRACT(EPOCH FROM NOW()) - updated_at) AS stuck_seconds
FROM storage_volumes
WHERE status IN ('CREATING', 'RESIZING', 'DELETING', 'ERROR')
ORDER BY updated_at ASC
LIMIT 30;
```

| Column | Purpose |
|--------|---------|
| `status` | Current lifecycle state: `CREATING`, `AVAILABLE`, `IN_USE`, `RESIZING`, `DELETING`, `ERROR` |
| `error_message` | Watcher or handler-written failure description |
| `size_gb` | Requested volume size in GiB |
| `storage_class` | K8s StorageClass used for PVC provisioning |
| `stuck_seconds` | Seconds since last status update — compare against watcher timeouts |

### Volume Status Distribution

```sql
SELECT status, COUNT(*) AS cnt
FROM storage_volumes
GROUP BY status
ORDER BY cnt DESC;
```

---

## Step 2 — DB Status Query (Snapshots)

```sql
-- Failed / stuck snapshots
SELECT id, volume_id, name, status,
       error_message,
       to_timestamp(created_at) AS created,
       to_timestamp(updated_at) AS updated,
       ROUND(EXTRACT(EPOCH FROM NOW()) - updated_at) AS stuck_seconds
FROM volume_snapshots
WHERE status IN ('CREATING', 'DELETING', 'ERROR')
ORDER BY updated_at ASC
LIMIT 30;
```

| Column | Purpose |
|--------|---------|
| `status` | Snapshot lifecycle: `CREATING`, `READY`, `ERROR`, `DELETING` |
| `volume_id` | Source volume reference |
| `error_message` | Snapshot creation/deletion failure reason |

### Snapshot Status Distribution

```sql
SELECT status, COUNT(*) AS cnt
FROM volume_snapshots
GROUP BY status
ORDER BY cnt DESC;
```

---

## Step 3 — DB Status Query (Restore Jobs)

```sql
-- Failed / stuck restore jobs
SELECT id, snapshot_id, target_volume_id, status,
       error_message,
       to_timestamp(created_at) AS created,
       to_timestamp(updated_at) AS updated,
       ROUND(EXTRACT(EPOCH FROM NOW()) - updated_at) AS stuck_seconds
FROM restore_jobs
WHERE status IN ('PENDING', 'RESTORING', 'FAILED')
ORDER BY updated_at ASC
LIMIT 30;
```

| Column | Purpose |
|--------|---------|
| `status` | Restore lifecycle: `PENDING`, `RESTORING`, `COMPLETED`, `FAILED` |
| `snapshot_id` | Source snapshot for the restore |
| `target_volume_id` | Newly created volume from restore |
| `error_message` | Restore failure reason |

---

## Step 4 — K8s Resource Inspection

### 4.1 PVC Status

```bash
# List PVCs in the project namespace
kubectl get pvc -n <namespace> -l project-id=<project-id>

# Describe a specific PVC for events
kubectl describe pvc <pvc-name> -n <namespace>
```

**Key fields to check:**
- `STATUS`: `Pending` = provisioner issue; `Bound` = healthy
- `CAPACITY`: matches requested `size_gb`?
- `STORAGECLASS`: matches DB record `storage_class`?
- Events: look for `ProvisioningFailed`, `WaitForFirstConsumer`, `ExternalExpanding`

### 4.2 VolumeSnapshot Status

```bash
# List VolumeSnapshots
kubectl get volumesnapshot -n <namespace>

# Describe for readiness
kubectl describe volumesnapshot <snapshot-name> -n <namespace>
```

**Key fields to check:**
- `READYTOUSE`: `true` = snapshot completed; `false` = still creating or failed
- `RESTORESIZE`: expected size
- `SNAPSHOTCLASS`: VolumeSnapshotClass configuration
- Events: look for `SnapshotCreationError`, `SnapshotContentMissing`

### 4.3 StorageClass and VolumeSnapshotClass

```bash
# Verify StorageClass exists and supports expansion
kubectl get sc
kubectl describe sc <storage-class-name>

# Verify VolumeSnapshotClass exists
kubectl get volumesnapshotclass
```

**Key fields to check:**
- `ALLOWVOLUMEEXPANSION`: must be `true` for resize operations
- `PROVISIONER`: matches the CSI driver available on the cluster
- VolumeSnapshotClass `DRIVER`: matches the StorageClass provisioner

---

## Step 5 — Failure Decision Tree

```
Volume status = ERROR
├── error_message contains "timeout" or stuck_seconds > threshold
│   ├── status was CREATING, stuck > 1800s (30 min)
│   │   → PVC provisioning stuck
│   │   → Action: kubectl describe pvc → check StorageClass, CSI driver, node capacity
│   │
│   ├── status was RESIZING, stuck > 1800s (30 min)
│   │   → PVC resize stuck
│   │   → Action: kubectl describe pvc → check ALLOWVOLUMEEXPANSION, CSI resize support
│   │
│   └── status was DELETING, stuck > 900s (15 min)
│       → PVC deletion stuck
│       → Action: kubectl describe pvc → check finalizers, attached pods, volume attachments
│
├── error_message contains "failed" (event-based recovery)
│   → Latest storage_event has failed status
│   → Action: Check storage_events table for the volume:
│   │   SELECT * FROM storage_events WHERE volume_id = '<id>' ORDER BY created_at DESC LIMIT 5;
│   → Examine handler logs for the specific NATS event failure
│
├── Snapshot status = ERROR
│   ├── VolumeSnapshot READYTOUSE = false after extended wait
│   │   → Snapshot controller issue
│   │   → Action: kubectl describe volumesnapshot → check events
│   │   → Action: kubectl logs -n kube-system -l app=snapshot-controller
│   │
│   ├── Source volume not found or in wrong state
│   │   → Volume was deleted while snapshot was being created
│   │   → Action: Verify source volume_id exists in storage_volumes
│   │
│   └── VolumeSnapshotClass not found
│       → Cluster missing required snapshot class
│       → Action: kubectl get volumesnapshotclass
│
├── Restore status = FAILED
│   ├── Source snapshot not found or not READY
│   │   → Snapshot was deleted or failed before restore completed
│   │   → Action: Check volume_snapshots table for snapshot_id status
│   │
│   ├── PVC creation from snapshot failed
│   │   → StorageClass mismatch or capacity issue
│   │   → Action: kubectl describe pvc <restored-pvc> → check dataSource reference
│   │
│   └── Handler error during restore
│       → NATS handler failed to complete restore pipeline
│       → Action: Check Task Runner logs for storage.restore.requested handling
│
└── DB status stuck but K8s resource looks healthy
    → Watcher missed the state transition (CAS conflict or watcher not running)
    → Action: Check Task Runner logs for "volume watcher" sync cycle messages
    → Action: Verify StorageRunnerEnabled = true in environment
```

---

## Step 6 — Volume Status Lifecycle

```
                 ┌──────────────────────────────────┐
                 │        storage.volume.created     │
                 │           (NATS event)            │
                 └──────────┬───────────────────────┘
                            ▼
                      ┌──────────┐
                      │ CREATING │──── PVC creation ────► kubectl create pvc
                      └────┬─────┘
                           │ PVC Bound
                           ▼
                      ┌──────────┐
                      │AVAILABLE │◄───────────────────── Resize complete
                      └────┬─────┘                       Pods detached
                           │ Pod mounts PVC
                           ▼
                      ┌──────────┐
                      │  IN_USE  │
                      └────┬─────┘
                           │ storage.volume.resized
                           ▼
                      ┌──────────┐
                      │ RESIZING │──── PVC resize ──────► kubectl patch pvc
                      └────┬─────┘
                           │
              ┌────────────┼────────────┐
              │ success    │ timeout    │ failure
              ▼            ▼            ▼
         AVAILABLE      ERROR        ERROR

    storage.volume.deleted
              │
              ▼
         ┌──────────┐
         │ DELETING │──── PVC delete ──────► kubectl delete pvc
         └────┬─────┘
              │
              ▼
         (record removed)
```

### Snapshot Lifecycle

```
    storage.snapshot.created
              │
              ▼
         ┌──────────┐
         │ CREATING │──── VolumeSnapshot create ──► kubectl create volumesnapshot
         └────┬─────┘
              │ READYTOUSE = true
              ▼
         ┌──────────┐
         │  READY   │
         └────┬─────┘
              │ storage.snapshot.deleted
              ▼
         ┌──────────┐
         │ DELETING │──── VolumeSnapshot delete ──► kubectl delete volumesnapshot
         └────┬─────┘
              ▼
         (record removed)
```

### Restore Lifecycle

```
    storage.restore.requested
              │
              ▼
         ┌──────────┐
         │ PENDING  │
         └────┬─────┘
              │ Handler starts restore
              ▼
         ┌──────────┐
         │RESTORING │──── PVC create from snapshot dataSource
         └────┬─────┘
              │
       ┌──────┴──────┐
       │ success     │ failure
       ▼             ▼
   COMPLETED       FAILED
   (new volume     (error_message
    CREATING)       logged)
```

---

## Step 7 — NATS Event Flow and Debugging

### Event Types

| Event | Handler | Description |
|-------|---------|-------------|
| `storage.volume.created` | `HandleVolumeCreated` | Creates PVC with requested size and StorageClass |
| `storage.volume.deleted` | `HandleVolumeDeleted` | Deletes PVC and removes DB record |
| `storage.volume.resized` | `HandleVolumeResized` | Patches PVC with new size via `kubectl patch` |
| `storage.snapshot.created` | `HandleSnapshotCreated` | Creates VolumeSnapshot, waits for READYTOUSE |
| `storage.snapshot.deleted` | `HandleSnapshotDeleted` | Deletes VolumeSnapshot and removes DB record |
| `storage.restore.requested` | `HandleRestoreRequested` | Creates new PVC from snapshot dataSource, new volume record, updates restore_jobs |

### NATS Debugging

```bash
# Check NATS consumer lag
nats consumer info STORAGE <consumer-name>

# Check if events are stuck in retry
nats consumer pending STORAGE <consumer-name>
```

---

## Step 8 — Common Failure Matrix

| Symptom | Root Cause | Diagnostic | Resolution |
|---------|-----------|------------|------------|
| Volume stuck in `CREATING` > 30 min | PVC not provisioning | `kubectl describe pvc` → events | Fix StorageClass, check CSI driver, node capacity |
| Volume stuck in `RESIZING` > 30 min | CSI driver resize failure | `kubectl describe pvc` → expansion events | Verify `ALLOWVOLUMEEXPANSION`, CSI support |
| Volume stuck in `DELETING` > 15 min | PVC finalizer or attachment | `kubectl describe pvc` → finalizers | Remove stuck finalizers, detach volume |
| Volume `ERROR` from failed event | Handler failed during operation | Check `storage_events` table | Retry NATS event or manual DB correction |
| Snapshot `ERROR` | VolumeSnapshot not becoming ready | `kubectl describe volumesnapshot` | Check snapshot-controller, VolumeSnapshotClass |
| Snapshot `CREATING` indefinitely | Snapshot controller not processing | `kubectl logs snapshot-controller` | Restart snapshot-controller, check CSI driver |
| Restore `FAILED` | Source snapshot not READY or deleted | Check `volume_snapshots` status | Ensure snapshot exists and is READY before restore |
| Restore `FAILED` | PVC from snapshot creation error | `kubectl describe pvc` with dataSource | Verify snapshot content exists, StorageClass compatibility |
| DB says `ERROR` but K8s PVC is `Bound` | CAS conflict in watcher | Task Runner logs for "cas conflict" | Manual DB status correction |
| All storage ops failing | StorageRunnerEnabled = false | Check env config | Enable `STORAGE_RUNNER_ENABLED` |

---

## Step 9 — VolumeWatcher Recovery Mechanisms

The VolumeWatcher uses two complementary recovery strategies:

### 9.1 Timeout-Based Recovery

Volumes stuck in transitional states beyond their configured timeouts are moved to `ERROR`:

| State | Timeout | Condition |
|-------|---------|-----------|
| `CREATING` | `StorageWatcherCreatingTimeout` (30 min) | `NOW() - updated_at > timeout` |
| `RESIZING` | `StorageWatcherResizingTimeout` (30 min) | `NOW() - updated_at > timeout` |
| `DELETING` | `StorageWatcherDeletingTimeout` (15 min) | `NOW() - updated_at > timeout` |

### 9.2 Failed Event-Based Recovery

Volumes whose latest `storage_event` has a `failed` status are also moved to `ERROR`, regardless of how long they've been in the current state.

### 9.3 Compare-And-Swap (CAS) Pattern

Both recovery mechanisms use `UpdateStatusIfCurrentWithMessage` — a CAS operation that only updates the DB row if the current status matches the expected value. This prevents race conditions between the watcher and concurrent handler operations.

**CAS conflict indicators in logs:**
- `"cas conflict, volume already transitioned"` — another process updated the volume first
- This is expected behavior, not an error

---

## Step 10 — Watcher Thresholds Reference

| Env Var | Default | Purpose |
|---------|---------|---------|
| `STORAGE_RUNNER_ENABLED` | `false` | Master switch for the storage runner |
| `STORAGE_WATCHER_INTERVAL` | `5m` | Polling interval for VolumeWatcher sync cycles |
| `STORAGE_WATCHER_CREATING_TIMEOUT` | `30m` | Max time a volume can stay in `CREATING` before recovery |
| `STORAGE_WATCHER_RESIZING_TIMEOUT` | `30m` | Max time a volume can stay in `RESIZING` before recovery |
| `STORAGE_WATCHER_DELETING_TIMEOUT` | `15m` | Max time a volume can stay in `DELETING` before recovery |
| `STORAGE_CONSUMER_NAME` | `storage-consumer` | NATS JetStream consumer identity |
| `STORAGE_WORKER_CONCURRENCY` | `1` | Number of concurrent NATS message handlers |

---

## Step 11 — Task Runner Log Analysis

```bash
# Find the Task Runner pod
kubectl get pods -n ai-platform -l app=task-runner

# Storage watcher sync cycle logs
kubectl logs -n ai-platform <task-runner-pod> | grep -i "volume watcher"

# Handler-level logs for specific operations
kubectl logs -n ai-platform <task-runner-pod> | grep -i "storage"

# Recovery action logs
kubectl logs -n ai-platform <task-runner-pod> | grep -iE "(timeout recovery|cas conflict|failed event recovery)"

# NATS consumer logs
kubectl logs -n ai-platform <task-runner-pod> | grep -i "storage.*consumer"
```

---

## Step 12 — Source Code Change Analysis

When investigating regressions, check recent changes to the storage runner:

```bash
# Recent changes to storage runner code
git log --oneline -20 -- ai-platform/backend/go/internal/runner/storage/

# Diff a specific commit
git diff <commit>^ <commit> -- ai-platform/backend/go/internal/runner/storage/
```

---

## Source Code Reference

| File | Purpose |
|------|---------|
| `ai-platform/backend/go/internal/runner/storage/volume_watcher.go` | VolumeWatcher: timeout-based and failed event-based recovery with CAS |
| `ai-platform/backend/go/internal/runner/storage/handlers.go` | NATS event handlers for 6 storage operations |
| `ai-platform/backend/go/internal/runner/storage/worker.go` | Storage Task Runner: NATS consumer + watcher orchestration |
| `ai-platform/backend/go/internal/config/taskrunner.go` | Storage watcher configuration and environment variables |
| `ai-platform/backend/go/internal/server/model/storage/volume.go` | VolumeStatus enum definition |
| `ai-platform/backend/go/internal/server/model/storage/snapshot.go` | SnapshotStatus enum definition |
| `ai-platform/backend/go/internal/server/model/storage/restore_job.go` | RestoreStatus enum definition |
