---
name: gpu-health-report
description: >-
  Generate GPU fleet health reports (Korean) from Kubernetes clusters.
  Collects nvidia-smi XML, parses to per-GPU JSON, applies 4-tier health
  grading (GREEN/YELLOW/ORANGE/RED), produces Korean DOCX+Markdown reports to
  outputs/monitoring/{infra}/{date}/, and uploads DOCX to Google Drive. Use
  when the user asks to "GPU health report", "GPU 헬스 리포트", "GPU 상태 점검", "GPU
  fleet check", "GPU 모니터링 리포트", "generate GPU report", "GPU 건강 점검", "fleet
  health check", or needs periodic GPU health assessment for any NVIDIA GPU
  cluster. Do NOT use for GPU lifecycle management planning (use
  gpu-lifecycle-manager). Do NOT use for GPU resource availability checks (use
  mlops-k8s-access). Do NOT use for general K8s troubleshooting (use
  k8s-incident-investigator).
disable-model-invocation: true
---

# GPU Health Report

## Role

Infrastructure operations specialist that collects, grades, and reports on NVIDIA GPU fleet health across Kubernetes clusters. Produces actionable Korean health reports with 4-tier grading and uploads to Google Drive.

## Constraints

- **Freedom level: Low** — follows exact pipeline sequence, no deviation
- All report output (Markdown, DOCX) must be in Korean
- Do not add metrics beyond what nvidia-smi XML provides
- Do not modify cluster state — read-only operations only
- Do not add report sections beyond the defined template
- Do not skip collection failures silently — log warnings per node
- Match report depth to actual data — do not pad with generic GPU advice

## Prerequisites

- `kubectl` with valid kubeconfig (default: `~/.kube/tkai-merged.config`)
- GPU nodes with `nvidia-dcgm-exporter` pods (or any pod with `nvidia-smi`)
- Python 3.9+ with `python-docx` (`pip install python-docx`)
- `gws` CLI authenticated for Google Drive upload (`gws auth login`)

## Pipeline (Domain Behavior)

Entry point: `tools/gpu-lifecycle/run-gpu-health-report.sh`

```bash
tools/gpu-lifecycle/run-gpu-health-report.sh \
  --context <kube-context> \
  --infra <infra-name>
```

### Phase 1: Collect nvidia-smi XML

- Discovers GPU nodes via label `nvidia.com/gpu.present=true`
- Falls back to capacity-based detection if label missing
- Executes `nvidia-smi -x -q` inside `dcgm-exporter` pods per node
- Saves raw XML to `collected/nvidia-smi/`

### Phase 2: Parse XML → per-GPU JSON

- Runs `parse-to-json.py` on collected XML
- Produces one JSON file per GPU in `raw/`
- Extracts: ECC, retired pages, row remap, temperature, throttling, PCIe, NVLink

### Phase 3: Calculate Health Grades

- Runs `calculate-health-grade.py` on per-GPU JSON files
- Applies 4-tier grading per metric, rolls up to per-GPU grade
- Outputs `health-grades.json`

### Phase 4: Generate Report (Korean)

- Runs `generate-fleet-report.py`
- Produces fleet report as **both DOCX and Markdown** (default)
- All content in Korean: headers, tables, descriptions, recommendations
- Includes executive summary, per-GPU cards, recommendations

### Phase 5: Upload DOCX to Google Drive

- Uploads the generated DOCX to Google Drive via `gws drive upload`
- File naming: `GPU-Health-Report_{infra}_{date}.docx`
- Optional: specify target folder with `--gdrive-folder <id>`
- Skippable with `--no-gdrive`

### Execution Checklist

```
- [ ] Phase 1: nvidia-smi XML 수집 (또는 --skip-collect)
- [ ] Phase 2: XML → per-GPU JSON 파싱 완료
- [ ] Phase 3: health-grades.json 생성 확인
- [ ] Phase 4: fleet-report.docx + fleet-report.md 생성 확인 (한글)
- [ ] Phase 5: Google Drive 업로드 확인 (또는 --no-gdrive)
- [ ] 결과 파일 존재 및 크기 검증
```

## CLI Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--context` | Yes | — | Kubernetes context name |
| `--infra` | Yes | — | Infrastructure name (e.g. `demo`, `prod-a100`) |
| `--node-prefix` | No | `<infra>` | Node name prefix for JSON naming |
| `--format` | No | `both` | Report format: `docx`, `md`, or `both` |
| `--output-base` | No | `outputs/monitoring/` | Base output directory |
| `--skip-collect` | No | `false` | Skip collection, reuse existing data |
| `--no-gdrive` | No | `false` | Skip Google Drive upload |
| `--gdrive-folder` | No | — | Google Drive folder ID for upload |

**Example — Demo cluster (default: both formats + Drive upload):**
```bash
tools/gpu-lifecycle/run-gpu-health-report.sh \
  --context tkai-demo \
  --infra demo
```

**Example — Skip collection, Markdown only, no Drive upload:**
```bash
tools/gpu-lifecycle/run-gpu-health-report.sh \
  --context tkai-demo \
  --infra demo \
  --skip-collect --format md --no-gdrive
```

**Example — Upload to specific Drive folder:**
```bash
tools/gpu-lifecycle/run-gpu-health-report.sh \
  --context tkai-demo \
  --infra demo \
  --gdrive-folder 1ABC_your_folder_id
```

## Output Structure

```
outputs/monitoring/<infra>/<date>/
├── collected/nvidia-smi/    # Raw nvidia-smi XML per node
├── raw/                     # Per-GPU JSON (parsed)
├── health-grades.json       # Graded health data
├── fleet-report.md          # Korean Markdown report
└── fleet-report.docx        # Korean DOCX report (also uploaded to Drive)
```

## Component Scripts

All in `tools/gpu-lifecycle/`:

| Script | Role |
|--------|------|
| `run-gpu-health-report.sh` | Pipeline orchestrator (entry point) |
| `parse-to-json.py` | nvidia-smi XML → per-GPU JSON |
| `calculate-health-grade.py` | 4-tier health grading engine |
| `generate-fleet-report.py` | Korean DOCX/Markdown report generator |
| `collect-gpu-health.sh` | Alternative: direct kubectl collection |

## Health Grade System

| Grade | Criteria | Action |
|-------|----------|--------|
| GREEN | All metrics normal | No action |
| YELLOW | Minor anomalies (low ECC, temp near threshold) | Monitor closely |
| ORANGE | Significant issues (high ECC, retired pages) | Schedule maintenance |
| RED | Critical failure (uncorrectable ECC, thermal throttle) | Immediate replacement |

### Monitored Metrics

ECC Errors (volatile/aggregate), Retired Pages, Row Remap, GPU/HBM Temperature, Thermal/Power Throttling, PCIe Replay Counter, NVLink Error Counts.

## Verification

After pipeline completes, verify each output exists:

```bash
INFRA="demo"; DATE=$(date +%Y-%m-%d)
ls -la outputs/monitoring/$INFRA/$DATE/health-grades.json
ls -la outputs/monitoring/$INFRA/$DATE/fleet-report.md
ls -la outputs/monitoring/$INFRA/$DATE/fleet-report.docx
ls outputs/monitoring/$INFRA/$DATE/raw/ | wc -l
```

Expected: `health-grades.json` > 0 bytes, `fleet-report.md` + `fleet-report.docx` exist (Korean content), `raw/` contains ≥1 JSON file per GPU, DOCX uploaded to Google Drive.

## Gotchas

- **"No GPU nodes found"**: Demo cluster uses `nvidia.com/gpu.present=true` label. If missing, script falls back to capacity-based detection. If both fail, manually verify node labels with `kubectl get nodes --show-labels`.
- **dcgm-exporter pod not found**: The pod lookup uses label `app=nvidia-dcgm-exporter`. Some clusters use different labels — check with `kubectl get pods -n gpu-operator -l app.kubernetes.io/name=dcgm-exporter`.
- **nvidia-smi exec timeout**: Distroless dcgm-exporter containers only have `nvidia-smi` available. Commands like `curl`, `ls`, `sh` will fail. The script uses `--request-timeout=60s`.
- **Empty raw/ directory after Phase 2**: Usually means XML files weren't found. Check `collected/nvidia-smi/` for actual XML files. The parser looks for both `*.xml` patterns and `nvidia-smi/` subdirectories.
- **H100 NVL specific**: `retired_pages.double_bit_ecc.count` and `pcie.replay` are `[N/A]` on H100 NVL. The parser handles `[N/A]` gracefully with zero defaults.
- **kubeconfig path**: Defaults to `~/.kube/tkai-merged.config`. Override via `KUBECONFIG` environment variable if using a different path.
- **Google Drive upload fails**: Ensure `gws` CLI is authenticated — run `gws auth login`. Use `--no-gdrive` to skip if Drive is unavailable.

## Supported GPU Models

Auto-detected from nvidia-smi XML. Tested: NVIDIA H100 NVL, B200. Compatible with any NVIDIA datacenter GPU (A100, L40S, etc.).
