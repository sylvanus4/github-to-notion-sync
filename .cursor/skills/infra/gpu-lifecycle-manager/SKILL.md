# GPU Lifecycle Manager

Orchestrate end-to-end GPU health lifecycle for 1,016 B200 GPUs leased from SKT on the `tkai-aio-b200` cluster. Supports 6 workflow modes: collect raw telemetry, calculate health grades, generate fleet reports, apply K8s node labels, run due-diligence inspection preparation, and full pipeline execution.

## Triggers

Use when the user asks to "GPU health check", "GPU lifecycle", "GPU 수명", "GPU 건강", "GPU 상태", "fleet report", "RMA candidates", "GPU 실사", "due diligence", "GPU grading", "GPU 등급", "collect GPU data", "GPU 데이터 수집", "label GPU nodes", "GPU 노드 라벨", "gpu-lifecycle-manager", or any B200 GPU health assessment, fleet monitoring, or SKT due diligence request.

Do NOT use for:
- General GPU resource allocation or utilization queries (use `gpu-resource-inspector`)
- GPU dashboard server start/stop operations (use `gpu-dashboard-ops`)
- Non-B200 cluster GPU work (this skill targets `tkai-aio-b200` only)
- GPU driver installation or node setup (use infrastructure skills)
- Cluster context switching (use `kube-cluster-switch`)

## Constraints

- Always use `--context=tkai-aio-b200` for all `kubectl` commands
- All scripts live under `tools/gpu-lifecycle/`
- Raw output goes to `outputs/gpu-lifecycle/{date}/raw/`
- Health grades go to `outputs/gpu-lifecycle/{date}/health-grades.json`
- Fleet reports go to `outputs/gpu-lifecycle/{date}/fleet-report.docx` (or `.md` fallback)
- Never auto-apply K8s labels without explicit user confirmation
- Report in English by default; switch to Korean if user requests

## Prerequisites

Before running any mode, verify:

```bash
# Confirm cluster access
kubectl get nodes --context=tkai-aio-b200 --selector=nvidia.com/gpu.present=true -o name | head -3

# Confirm Python 3.9+ available
python3 --version
```

## Workflow Modes

### Mode 1: Collect (`collect`)

Gather raw GPU health telemetry from all B200 nodes.

```bash
cd tools/gpu-lifecycle
./collect-gpu-health.sh --context tkai-aio-b200
```

**Options**:
- `--node <name>`: Collect from a single node only
- `--output-dir <dir>`: Custom output directory
- `--timeout <sec>`: kubectl exec timeout (default: 60)

**Collects per GPU**:
- `nvidia-smi -q -x` full XML
- `nvidia-smi --query-gpu=serial,uuid,...,pcie.replay_counter --format=csv`
- `dcgmi health -g 0 -j` (JSON health check)
- `dcgmi diag -r 2 -j` (level-2 diagnostic)
- `dmesg | grep -E "Xid|NVRM|ECC"` (kernel logs)
- `nvidia-smi nvlink -s` (NVLink error counters)

**Output**: `outputs/gpu-lifecycle/{date}/raw/{node}-gpu{index}.json`

### Mode 2: Grade (`grade`)

Calculate 4-tier health grades from collected raw data.

```bash
cd tools/gpu-lifecycle
python3 calculate-health-grade.py \
  --input-dir ../../outputs/gpu-lifecycle/$(date +%Y-%m-%d)/raw \
  --output ../../outputs/gpu-lifecycle/$(date +%Y-%m-%d)/health-grades.json
```

**Options**:
- `--input-dir <dir>`: Directory containing raw JSON files
- `--output <file>`: Output path for health-grades.json
- `--config <file>`: Custom threshold config (YAML)

**Grade Definitions**:

| Grade  | Criteria | Recommendation |
|--------|----------|----------------|
| GREEN  | No uncorrectable ECC, no row remap failure/pending, no Xid in 30d, temp < 83°C, no NVLink errors | All workloads |
| YELLOW | Correctable ECC above threshold, or row remap correctable > 0, or intermittent thermal/power throttle | Monitor closely, inference OK |
| ORANGE | Uncorrectable ECC > 0, or repeated Xid (3+ in 30d), or row remap pending > 0, or NVLink errors above threshold | Inference only, no training |
| RED    | Row remap failure, or retired pages pending repeatedly, or critical Xid (48/63/64/74/79/92/94/95), or uncorrectable ECC trending up | Isolate immediately, RMA candidate |

**Output**: `outputs/gpu-lifecycle/{date}/health-grades.json`

### Mode 3: Report (`report`)

Generate a comprehensive fleet health report.

```bash
cd tools/gpu-lifecycle
python3 generate-fleet-report.py \
  --input ../../outputs/gpu-lifecycle/$(date +%Y-%m-%d)/health-grades.json \
  --output ../../outputs/gpu-lifecycle/$(date +%Y-%m-%d)/fleet-report.docx \
  --format docx
```

**Options**:
- `--input <file>`: Path to health-grades.json
- `--output <file>`: Output report path
- `--format docx|md`: Output format (default: docx, falls back to md if python-docx missing)

**Report Sections**:
1. Executive Summary with grade distribution
2. Per-node GPU health breakdown
3. Top-10 worst-scoring GPUs
4. RMA candidate list with evidence
5. Trend analysis (if historical data exists)
6. Recommendations

### Mode 4: Label (`label`)

Apply `gpu-health` labels to K8s nodes. **Requires explicit user confirmation.**

```bash
cd tools/gpu-lifecycle
./label-gpu-health.sh --context tkai-aio-b200
```

**Options**:
- `--context <ctx>`: Kubernetes context (default: tkai-aio-b200)
- `--input <file>`: Path to health-grades.json
- `--dry-run`: Show what labels would be applied without changing anything

Labels each node with the worst GPU grade found on that node:
```
gpu-health=green|yellow|orange|red
```

### Mode 5: Due Diligence (`due-diligence`)

Prepare for the SKT due diligence inspection.

1. Run `collect` mode for fresh data
2. Run `grade` mode to compute current grades
3. Run `report` mode to generate the DOCX report
4. Review checklist at `tools/gpu-lifecycle/due-diligence-checklist.md`
5. Verify all checklist items are addressed in the report

**Checklist categories**:
- Pre-inspection data collection
- Physical infrastructure verification
- Software and monitoring verification
- Health assessment review
- Contractual and warranty verification

### Mode 6: Full Pipeline (`full`)

Run all modes in sequence: collect → grade → report → label (dry-run) → display summary.

```bash
# Step 1: Collect
cd tools/gpu-lifecycle
./collect-gpu-health.sh --context tkai-aio-b200

# Step 2: Grade
python3 calculate-health-grade.py \
  --input-dir ../../outputs/gpu-lifecycle/$(date +%Y-%m-%d)/raw

# Step 3: Report
python3 generate-fleet-report.py \
  --input ../../outputs/gpu-lifecycle/$(date +%Y-%m-%d)/health-grades.json \
  --format docx

# Step 4: Label (dry-run first, ask user before applying)
./label-gpu-health.sh --dry-run --context tkai-aio-b200

# Step 5: Summary
echo "Pipeline complete. Outputs in outputs/gpu-lifecycle/$(date +%Y-%m-%d)/"
```

After dry-run, ask user: "Apply GPU health labels to nodes? (yes/no)"

## Key Monitoring Endpoints

- **Grafana**: `grafana.tkai.b200.thakicloud.site`
- **VictoriaMetrics**: `vmselect.tkai.b200.thakicloud.site`
- **Dashboard**: `localhost:3000` (start via `gpu-dashboard-ops` skill)

## Critical Xid Reference

| Xid Code | Meaning | Action |
|----------|---------|--------|
| 48 | Double-bit ECC error | Immediate RED, isolate |
| 63 | Row remapping failure | Immediate RED, RMA |
| 64 | Fallen off bus | Immediate RED, RMA |
| 74 | NVLink error | Grade ORANGE minimum |
| 79 | GPU has fallen off bus | Immediate RED, RMA |
| 92 | High single-bit ECC rate | Grade ORANGE minimum |
| 94 | Uncontained ECC error | Immediate RED, isolate |
| 95 | Uncontained ECC error | Immediate RED, isolate |

## Alert Escalation

- **GREEN → YELLOW**: Automated monitoring, no action required
- **GREEN/YELLOW → ORANGE**: Slack #gpu-alerts, restrict to inference workloads
- **Any → RED**: Slack #gpu-alerts + PagerDuty, immediate node cordon, RMA ticket
