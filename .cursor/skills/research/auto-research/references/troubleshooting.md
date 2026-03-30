# AutoResearchClaw — Troubleshooting

## Diagnostic Commands

```bash
cd ~/thaki/AutoResearchClaw && source .venv/bin/activate

# Health check
researchclaw doctor --config config.arc.yaml

# Validate config
researchclaw validate --config config.arc.yaml

# Generate run report
researchclaw report --run-dir artifacts/<run-id>
```

## Common Failures

### Config Validation Errors

**Symptom**: `Missing required field: llm.base_url`

**Fix**: Ensure all required fields are set in `config.arc.yaml`:
- `project.name`
- `research.topic`
- `runtime.timezone`
- `notifications.channel`
- `knowledge_base.root`
- `llm.base_url` (not needed if `llm.provider: "acp"`)
- `llm.api_key_env` (not needed if `llm.provider: "acp"`)

### LLM Preflight Failure

**Symptom**: `Preflight check... FAILED`

**Causes**:
1. API key not set: `echo $OPENAI_API_KEY`
2. Incorrect base URL: verify `llm.base_url` is reachable
3. Model not available: check `llm.primary_model` exists for your provider
4. Rate limit: wait and retry

**Fix**: Skip with `--skip-preflight` for debugging, but fix the root cause.

### Knowledge Base Directory Missing

**Symptom**: `Missing path: /path/to/docs/kb`

**Fix**: Create the directory structure:

```bash
cd ~/thaki/AutoResearchClaw
mkdir -p docs/kb/{questions,literature,experiments,findings,decisions,reviews}
```

Or disable path checking: `researchclaw validate --no-check-paths`

### Sandbox Execution Failure

**Symptom**: Stage 12 fails with `ModuleNotFoundError` or `PermissionError`

**Causes**:
1. Missing dependencies in sandbox venv
2. Incorrect `experiment.sandbox.python_path`
3. Import not in `experiment.sandbox.allowed_imports`

**Fix**:

```bash
source .venv/bin/activate
pip install numpy torch scikit-learn
```

Update allowed imports in config if custom packages are needed.

### Docker Sandbox Failure

**Symptom**: Stage 12 fails with Docker-related errors

**Causes**:
1. Docker not running
2. Image not built
3. GPU not available

**Fix**:

```bash
# Check Docker
docker ps

# Build image
docker build -t researchclaw/experiment:latest researchclaw/docker/

# Verify GPU access
docker run --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### Gate Rejection

**Symptom**: Pipeline blocks at Stage 5, 9, or 20 with `BLOCKED_APPROVAL`

**Fix options**:
1. Use `--auto-approve` to skip all gates
2. Use `--from-stage <next-stage>` to resume past the gate
3. Modify `security.hitl_required_stages` to remove gate stages

### PIVOT/REFINE Infinite Loop

**Symptom**: Pipeline keeps rolling back between Stage 8 and Stage 15

**Explanation**: Stage 15 (RESEARCH_DECISION) can trigger at most 2 PIVOT/REFINE
cycles. After that, it forces PROCEED. If both cycles produce empty metrics,
it also forces PROCEED early.

**Check**: `cat artifacts/<run-id>/decision_history.json`

### Citation Verification Failures

**Symptom**: Stage 23 reports many unverified citations

**Explanation**: The 4-layer verification checks arXiv, CrossRef, DataCite, then
LLM fallback. Hallucinated citations are stripped from the final paper.

**Check**: `cat artifacts/<run-id>/stage-23/verification_report.json`

### Paper Quality Issues

**Symptom**: Quality gate (Stage 20) gives low score

**Fix options**:
1. Use iterative pipeline mode (`execute_iterative_pipeline`) which re-runs
   paper writing stages until quality threshold is met
2. Provide better domain context in config
3. Use a more capable LLM model

### Resume After Crash

**Symptom**: Pipeline interrupted mid-run

**Fix**: Resume from last checkpoint:

```bash
researchclaw run --config config.arc.yaml --resume --output artifacts/<run-id>
```

Or resume from a specific stage:

```bash
researchclaw run --config config.arc.yaml --from-stage PAPER_OUTLINE --output artifacts/<run-id>
```

## Stage Names for `--from-stage`

```
TOPIC_INIT, PROBLEM_DECOMPOSE, SEARCH_STRATEGY, LITERATURE_COLLECT,
LITERATURE_SCREEN, KNOWLEDGE_EXTRACT, SYNTHESIS, HYPOTHESIS_GEN,
EXPERIMENT_DESIGN, CODE_GENERATION, RESOURCE_PLANNING, EXPERIMENT_RUN,
ITERATIVE_REFINE, RESULT_ANALYSIS, RESEARCH_DECISION, PAPER_OUTLINE,
PAPER_DRAFT, PEER_REVIEW, PAPER_REVISION, QUALITY_GATE, KNOWLEDGE_ARCHIVE,
EXPORT_PUBLISH, CITATION_VERIFY
```
