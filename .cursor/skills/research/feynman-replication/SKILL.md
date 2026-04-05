---
name: feynman-replication
description: "Plan or execute a replication of a paper, claim, or benchmark with environment selection (local, venv, Docker, HF Jobs, RunPod, Modal). Produces reproducible replication packages with scripts, data manifests, and result verification. Use when the user asks to 'replicate results', 'reproduce an experiment', 'verify a claim empirically', 'build a replication package', 'experiment replication', 'reproduce this paper', '실험 재현', '논문 재현', '결과 재현', '벤치마크 재현', 'feynman-replication', '/replicate', 'replication plan'. Do NOT use for paper-code mismatch detection without execution (use feynman-paper-audit). Do NOT use for paper review (use feynman-peer-review). Do NOT use for model training (use hf-model-trainer). Do NOT use for running existing project backtests (use trading-backtest-expert)."
---

# Experiment Replication

Plan or execute a replication of a paper, claim, or benchmark. Produces a structured replication package with environment setup, scripts, data manifests, and verification criteria.

## Prerequisites

- The user provides a paper (arXiv ID/URL), specific claim, or benchmark to replicate.
- The skill handles both "plan only" and "full execution" modes.

## Workflow

### Phase 1: Extract

Spawn a `generalPurpose` subagent to gather implementation details:

```
You are a research extraction agent. Your task:

1. Read the target paper and any linked code repository
2. Extract:
   - Implementation details (architecture, hyperparameters, training procedure)
   - Dataset requirements (source, preprocessing, splits)
   - Evaluation metrics and expected results
   - Hardware requirements (GPU type, memory, training time)
   - Dependencies and software versions
3. Identify:
   - What is explicitly documented vs inferred
   - What is missing and must be guessed or asked about
   - Which checks or test oracles determine replication success
4. Save to `outputs/feynman/<slug>-extraction.md`
```

### Phase 2: Plan

Build the replication plan:

```markdown
## Replication Plan: <paper title>

### Objective
What specific result(s) we aim to replicate.

### Success Criteria
Quantitative thresholds for declaring replication success:
- Metric A within X% of reported value
- Metric B matches qualitative behavior described in Section Y

### Environment Requirements
- GPU: <type and count>
- Memory: <RAM/VRAM>
- Estimated compute time: <hours>
- Estimated cost: <USD for cloud options>

### Data Pipeline
1. Download dataset from <source>
2. Preprocessing steps
3. Expected data shape after preprocessing

### Implementation Steps
1. Environment setup
2. Data preparation
3. Model implementation / repo clone
4. Training / inference
5. Evaluation
6. Comparison with reported results

### Risk Factors
- Missing detail X may affect reproducibility
- Random seed sensitivity
- Hardware-dependent behavior
```

Save to `outputs/feynman/<slug>-replication-plan.md` and present to the user.

### Phase 3: Environment Selection

**Ask the user** which execution environment to use. Do NOT proceed without explicit confirmation:

| Environment | Best For | Requirements |
|-------------|----------|-------------|
| **Local** | Quick tests, small models | Current machine resources |
| **Virtual env** | Isolated Python deps | Python, venv/conda |
| **Docker** | Full isolation, reproducibility | Docker Desktop |
| **HF Jobs** | Burst GPU, managed infra | `hf` CLI, HF account |
| **RunPod** | Long-running, SSH access | `runpodctl`, RUNPOD_API_KEY |
| **Modal** | Serverless GPU bursts | `modal` CLI, Modal account |
| **Plan only** | No execution, just the plan | None |

If the user selects "Plan only", skip to Phase 5.

### Phase 4: Execute

Based on the selected environment:

**Local / Virtual env:**
```bash
# Create and activate environment
python -m venv replication-<slug>
source replication-<slug>/bin/activate
pip install -r requirements.txt
# Run replication scripts
```

**Docker:**
```bash
# Build reproducible container
docker build -t replication-<slug> .
docker run --gpus all replication-<slug>
```

**HF Jobs** (preferred cloud option — uses project's existing hf-jobs skill):
```bash
hf jobs run --flavor gpu-t4-small replication-<slug>.py
```

**RunPod:**
```bash
runpodctl create pod --name replication-<slug> --gpu "NVIDIA A100" --image pytorch/pytorch:latest
runpodctl ssh <pod-id>
```

**Modal:**
```python
# modal_replication.py with @app.function(gpu="A100") decorator
modal run modal_replication.py
```

During execution:
- Save all scripts to `outputs/feynman/<slug>-scripts/`
- Log raw outputs to `outputs/feynman/<slug>-results-raw.md`
- Append progress entries to `outputs/feynman/<slug>-changelog.md`

### Phase 5: Report

```markdown
## Replication Report: <paper title>

### Results Comparison

| Metric | Paper | Replicated | Delta | Status |
|--------|-------|-----------|-------|--------|
| Accuracy | 94.2% | 93.8% | -0.4% | ✅ REPLICATED (within threshold) |
| F1 | 0.91 | 0.87 | -0.04 | ⚠️ PARTIAL (below threshold) |

### Environment Used
- Platform: <selected environment>
- Hardware: <GPU, memory>
- Total compute time: <hours>
- Total cost: <USD if cloud>

### Deviations from Paper
- List any implementation choices that differed from the paper

### Challenges Encountered
- Missing details, bugs, undocumented dependencies

### Sources
- Paper: <URL>
- Repository: <URL>
- Dataset: <URL>
```

Save to `outputs/feynman/<slug>-replication-report.md`.

## Output Structure

```
outputs/feynman/
├── <slug>-extraction.md         # Phase 1 extracted details
├── <slug>-replication-plan.md   # Phase 2 plan
├── <slug>-scripts/              # Phase 4 execution scripts
├── <slug>-results-raw.md        # Phase 4 raw outputs
├── <slug>-changelog.md          # Phase 4 progress log
└── <slug>-replication-report.md # Phase 5 final report
```

## Safety Rules

- **Never run GPU workloads without user confirmation** of environment and estimated cost
- **Never install packages** without confirming the execution environment first
- Do not claim "replicated" unless planned success criteria actually passed
- Log all commands and outputs for reproducibility audit

## Verification Before Completion

- [ ] Replication plan covers all claimed results in scope
- [ ] Success criteria are quantitative and testable
- [ ] Environment selection was explicitly confirmed by user
- [ ] All scripts and outputs saved to documented paths
- [ ] Report clearly distinguishes replicated vs partial vs failed results
