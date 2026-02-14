# 2. Infrastructure

## 2-1. Workloads

### 2-1-1. Workloads Status

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Running | `Running` | Lock Pod, Edit Pod, Stop, Restart, Terminate |
| Stopped | `Stopped` | Lock Pod, Edit Pod, Start, Terminate |
| Failed | `Failed` | Lock Pod, Edit Pod, Stop, Restart, Terminate |
| Starting | `Starting` | Lock Pod, Edit Pod, Terminate |
| Stopping | `Stopping` | Lock Pod, Edit Pod, Terminate |
| Restarting | `Restarting` | Lock Pod, Edit Pod, Stop, Terminate |
| Terminating | `Terminating` | *(none)* |

### 2-1-2. Lock Status

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Locked | `Locked` | Unlock Pod, Edit Pod, Start |
| Unlocked | `Unlocked` | Lock Pod, Edit Pod, Stop, Start, Restart, Terminate |

### 2-1-3. Deploy New Pod (Workload Pod Creation)

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Pod Name | 기본정보 | Yes | Yes | Yes | |
| NameSpace? | 기본정보 | Yes | Yes | Yes | |
| Container Image | Instance | Yes | Yes | Yes | |
| GPU Type (CPU Only, GPU) | Instance | Yes | Yes | Yes | |
| Ports | Instance | Yes | Yes | Yes | |
| Memory Request | Instance | No | Yes | Yes | |
| Memory Limit | Instance | No | Yes | Yes | |
| CPU Request | Instance | No | Yes | Yes | |
| CPU Limit | Instance | No | Yes | Yes | |
| Container Storage | Instance | No | Yes | Yes | |
| Volume (no, existing volumes) | Instance | No | Yes | Yes | |
| Environment Variables | Instance | No | Yes | Yes | |
| Max Running Time | Instance | No | Yes | Yes | |

> **OPEN QUESTION:** Field name "NameSpace?" is uncertain -- needs confirmation on whether this is the correct field name.

---

## 2-2. My Template

- My Template has no status values, but has **visibility** settings: `private`, `shared`, `public`.
- Clicking **Deploy** redirects to the Deploy New Pod page with all settings preserved.
- **Scope rules:**
  - Created at **Group** level: template is visible across all projects created by that group.
  - Created at **Project** level: template is visible only within that project.

### 2-2-1. My Template Create & Edit

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Template Name | 기본정보 | Yes | Yes | Yes | Allowed: 3-128 characters, letters, numbers, "-", "_", ".", "()", "[]" |
| Description | 기본정보 | No | Yes | Yes | A brief description of the template's purpose and usage |
| Category | 기본정보 | No | Yes | Yes | Categories: AI/ML, Development, Rendering, Scientific, Web Service, Custom Input |
| visibility (private, public) | 기본정보 | Yes | Yes | Yes | Control who can view and use this template |
| Base Image | Docker | Yes | Yes | Yes | The Docker image used as the base for this template |
| Run Commands | Docker | No | Yes | Yes | Commands to run when the container starts (multiple commands separated by spaces) |
| Registry Credentials | Docker | No | Yes | No | Credentials for pulling images from a private registry. Not required for public images |
| Minimum GPU Memory (GB) | Hardware | - | - | - | |
| Minimum CPU Cores | Hardware | - | - | - | |
| Minimum Memory (GB) | Hardware | - | - | - | |
| Volume Disk (GB) | Hardware | - | - | - | |
| Volume Mount Path | Hardware | - | - | - | |
| Container Disk (GB) | Hardware | - | - | - | |
| HTTP Ports | Hardware | - | - | - | |
| Environment Variables | Hardware | - | - | - | |

> **OPEN QUESTION:** Registry Credentials description says "내용 맞는지 확인 필요" (content needs verification).

---

## 2-3. Storage (Volumes)

### 2-3-1. Storage Volumes Status

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Available | `Available` | Snapshot, Share, Edit, Delete |
| In use | `In use` | ? |
| Creating | `Creating` | Share, Delete |
| Deleting | `Deleting` | Share |
| Error | `error` | Share, Edit, Delete |

> **OPEN QUESTION:** Available actions for "In use" status are undefined ("?").

### 2-3-2. Storage Volume Create & Edit

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Volume Name | 기본정보 | Yes | - | Yes | |
| Description | 기본정보 | Yes | - | Yes | |
| type | 기본정보 | Yes | - | No | Values: Project, My |
| Size (GB) | - | Yes | - | Yes | |
| Storage Class | - | No | - | Yes | Values: NFS-Individual, NFS-Shared |
| AccessMode | - | No | - | Yes | Values: ReadWriteMany (RWX), ReadWriteOnce (RWO), ReadOnlyMany (ROX) |
| Default Mount Path | - | No | - | Yes | |
| Enable Auto Backup | - | No | - | Yes | |

### 2-3-3. Snapshot Status

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Ready | `Ready` | - |
| Creating | `Creating` | - |
| Deleting | `Deleting` | - |

### 2-3-4. Snapshot Create & Edit

> **OPEN QUESTION:** All fields are empty / TBD. Specification not yet defined.

---

## 2-4. Serverless

- Initial status after creating an endpoint: `pending`

> **OPEN QUESTION:** Whether `public` / `private` settings should be provided on the create page is not yet confirmed ("정확하지 않음").

### 2-4-1. Serverless Status (vLLM and Docker Image share the same statuses)

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Running | `Running` | Internal URL, Logs, Pause, Edit, Delete (direct without status change), Benchmark, Send Prompt (vLLM only) |
| Paused | `Paused` | Internal URL, Resume, Edit, Delete, Benchmark *(others disabled)* |
| Pending | `pending` | Logs, Delete, Benchmark *(others disabled)* |
| Failed | `Failed` | Delete (direct without status change) *(others disabled)* |

### 2-4-2. vLLM Create & Edit

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Name | 기본정보 | Yes | Yes | Yes | Lowercase letters, numbers, and hyphens only. Must start and end with alphanumeric |
| visibility (private, public) | 기본정보 | Yes | Yes | Yes | Controls public/internal network accessibility |
| Model | Model | Yes | Yes | Yes | Select the base model to serve with this vLLM endpoint |
| Download Huggingface | Model | No | Yes | Yes | When disabled, uses local model path from Finetune response |
| Min Replicas | Instance | Yes | Yes | Yes | Minimum number of replicas to keep running |
| Max Replicas | Instance | Yes | Yes | Yes | Maximum replicas during autoscaling |
| Port | Instance | System | No | Yes | Fixed for serverless endpoints |
| GPU Type | Instance | - | - | No | |
| GPU Count | Instance | - | - | No | |
| Max context length | Instance | - | - | No | |
| Max tokens (default cap) | Instance | - | - | No | |
| Batching preset | Instance | - | - | No | |

> **OPEN QUESTION:** visibility description says "내용 맞는지 확인 필요" (content needs verification).

### 2-4-3. Docker Image Create & Edit

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Endpoint Name | Container Conf | Yes | Yes | Yes | DNS-1123 naming rules: lowercase letters, numbers, hyphens only |
| visibility (private, public) | 기본정보 | Yes | Yes | Yes | Controls public/internal network accessibility |
| Image URI | Docker Image | Yes | Yes | Yes | Specify the Docker image to deploy |
| Registry Credentials | Docker Image | No | Yes | Yes | Credentials for pulling from a private registry |
| Compute (CPU, GPU) | Container Conf | No | Yes | Yes | Compute type required to run this container |
| Ports | Container Conf | No | Yes | Yes | Ports exposed by the container |
| Env variables (row - Key, Value pair) | Container Conf | No | Yes | Yes | Add a single environment variable |
| Env variables (list - Key, Value) | Container Conf | No | Yes | Yes | Define environment variables as key-value pairs |
| Min Replicas | Autoscaling | - | - | No | |
| Max Replicas | Autoscaling | - | - | No | |
| Target Concurrency | Autoscaling | - | - | No | |
| Idle Timeout | Autoscaling | - | - | No | |

> **OPEN QUESTION:** Env variables and Registry Credentials descriptions say "내용 맞는지 확인 필요" (content needs verification).
