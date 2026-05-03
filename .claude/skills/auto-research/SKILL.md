---
name: auto-research
description: >-
  Run the AutoResearchClaw 23-stage autonomous research pipeline that
  transforms a research topic into a conference-ready paper with real
  literature, sandbox experiments, and LaTeX export. Use when the user asks to
  "research [topic]", "write a paper about [topic]", "autonomous research",
  "auto-research", "자율 연구", "논문 자동 생성", "연구 파이프라인", "ResearchClaw 실행", "논문 작성
  파이프라인", "연구 자동화", or mentions ResearchClaw. Do NOT use for reviewing an
  existing paper (use paper-review), discovering related papers only (use
  related-papers-scout), or general web research without paper output (use
  parallel-deep-research).
disable-model-invocation: true
---

# AutoResearchClaw — Autonomous Research Pipeline

Run the full 23-stage research pipeline: topic scoping, literature discovery,
hypothesis generation, experiment execution, paper writing, peer review, and
conference-ready LaTeX export — all from a single research topic.

## Prerequisites

- **Python 3.11+** installed (via pyenv or Homebrew)
- **AutoResearchClaw** installed at `~/thaki/AutoResearchClaw/`
- **LLM API key** set via `OPENAI_API_KEY` env var (or configured in config)
- Optional: Docker for containerized experiments
- Optional: MetaClaw for cross-run learning

### First-Time Setup

If AutoResearchClaw is not installed, run:

```bash
cd ~/thaki && git clone https://github.com/aiming-lab/AutoResearchClaw.git
cd AutoResearchClaw
/opt/homebrew/bin/python3.11 -m venv .venv && source .venv/bin/activate
pip install -e .
cp config.researchclaw.example.yaml config.arc.yaml
researchclaw --help
```

## Reference Files

Read these for phase-specific details:

- `references/pipeline-stages.md` — All 23 stages with inputs, outputs, and gate logic
- `references/configuration-guide.md` — Config templates for common scenarios
- `references/experiment-modes.md` — Sandbox, Docker, and SSH remote modes
- `references/troubleshooting.md` — Common failures and recovery patterns

## Pipeline Overview

```
Phase A: Research Scoping        → Stages 1-2  (topic decomposition)
Phase B: Literature Discovery    → Stages 3-6  (real papers from OpenAlex/S2/arXiv)
Phase C: Knowledge Synthesis     → Stages 7-8  (gap analysis, hypothesis generation)
Phase D: Experiment Design       → Stages 9-11 (code gen, resource planning)  [GATE at 9]
Phase E: Experiment Execution    → Stages 12-13 (sandbox run, self-healing)
Phase F: Analysis & Decision     → Stages 14-15 (PROCEED/REFINE/PIVOT)
Phase G: Paper Writing           → Stages 16-19 (outline→draft→review→revision)
Phase H: Finalization            → Stages 20-23 (quality gate, LaTeX, citation verify)
```

Gate stages (5, 9, 20) require human approval unless `--auto-approve` is used.
Stage 15 can trigger REFINE (→ Stage 13) or PIVOT (→ Stage 8) with max 2 attempts.

## Execution

### Phase 1: Pre-flight Check

1. Verify AutoResearchClaw installation:

```bash
cd ~/thaki/AutoResearchClaw && source .venv/bin/activate
researchclaw doctor --config config.arc.yaml
```

2. If not installed, run the First-Time Setup above.

3. Confirm `OPENAI_API_KEY` (or equivalent) is set:

```bash
echo $OPENAI_API_KEY | head -c 8
```

### Phase 2: Configure

Generate or update `config.arc.yaml` based on user inputs. Key fields:

```yaml
project:
  name: "<project-slug>"
  mode: "full-auto"

research:
  topic: "<user-provided topic>"
  domains: ["<domain1>", "<domain2>"]

llm:
  provider: "openai-compatible"
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"  # pragma: allowlist secret
  primary_model: "gpt-4o"
  fallback_models: ["gpt-4o-mini"]

experiment:
  mode: "<sandbox|docker|simulated>"
  time_budget_sec: 300
  max_iterations: 10

export:
  target_conference: "<neurips_2025|iclr_2026|icml_2026>"
  authors: "<author names>"
```

See `references/configuration-guide.md` for full config reference.

### Phase 3: Run Pipeline

```bash
cd ~/thaki/AutoResearchClaw && source .venv/bin/activate
researchclaw run \
  --config config.arc.yaml \
  --topic "<research topic>" \
  --auto-approve
```

Additional CLI flags:
- `--output <dir>` — Custom output directory
- `--from-stage <STAGE_NAME>` — Resume from specific stage (e.g., `PAPER_OUTLINE`)
- `--resume` — Resume from last checkpoint
- `--skip-noncritical-stage` — Skip non-critical stages on failure
- `--skip-preflight` — Skip LLM connection check

### Phase 4: Monitor Progress

The pipeline prints progress to stdout. Monitor the artifacts directory:

```bash
ls -la artifacts/rc-*/
cat artifacts/rc-*/pipeline_summary.json
```

Check for PIVOT/REFINE decisions:

```bash
cat artifacts/rc-*/decision_history.json 2>/dev/null
```

### Phase 5: Collect Deliverables

On completion, deliverables are packaged at:

```
artifacts/<run-id>/deliverables/
├── paper_final.md              # Final paper (Markdown)
├── paper.tex                   # Conference-ready LaTeX
├── references.bib              # Verified BibTeX references
├── code/                       # Experiment source code
├── charts/                     # Result visualizations
├── verification_report.json    # Citation verification report
└── manifest.json               # Deliverable manifest
```

Report the run results to the user and offer to run `/auto-research-distribute`
for Notion, Slack, NotebookLM, and PPTX distribution.

## Options

- `--topic "..."` — Research topic (required; overrides config)
- `--mode sandbox|docker|simulated` — Experiment execution mode (default: sandbox)
- `--conference neurips_2025|iclr_2026|icml_2026` — Target conference template
- `--approve` — Auto-approve all gate stages (5, 9, 20)
- `--skip-distribute` — Skip post-pipeline distribution offer
- `--metaclaw` — Enable MetaClaw cross-run learning
- `--from-stage <NAME>` — Resume from a specific stage
- `--iterative` — Use iterative quality improvement (re-runs paper writing until quality threshold met)

## Output Convention

- Run artifacts: `~/thaki/AutoResearchClaw/artifacts/rc-YYYYMMDD-HHMMSS-<hash>/`
- Deliverables: `<run-dir>/deliverables/`
- Knowledge base: `~/thaki/AutoResearchClaw/docs/kb/`
- Evolution lessons: `<run-dir>/evolution/`

## Examples

### Example 1: Full autonomous research

User says: "Write a paper about efficient inference for large language models"

Actions:
1. Pre-flight: verify AutoResearchClaw + API key
2. Configure `config.arc.yaml` with topic and sandbox mode
3. Run: `researchclaw run --config config.arc.yaml --topic "efficient inference for LLMs" --auto-approve`
4. Monitor 23 stages (literature → hypothesis → experiments → paper → review → LaTeX)
5. Collect deliverables from `artifacts/rc-*/deliverables/`
6. Offer `/auto-research-distribute` for Notion/Slack/PPTX distribution

Result: Conference-ready paper with real citations, experiment results, and LaTeX export.

### Example 2: Resume from checkpoint

User says: "Resume my research from the paper writing stage"

Actions:
1. Run: `researchclaw run --config config.arc.yaml --from-stage PAPER_OUTLINE --auto-approve`
2. Pipeline resumes from Stage 16 using cached experiment results

### Example 3: Simulated mode

User says: "auto-research about graph neural networks --mode simulated"

Actions:
1. Set `experiment.mode: simulated` in config
2. Pipeline generates synthetic experiment results (no sandbox/Docker needed)
3. Paper is flagged as "simulated experiments" in output

## Error Handling

For detailed diagnostics, see [references/troubleshooting.md](references/troubleshooting.md).

| Error | Resolution |
|-------|-----------|
| `researchclaw: command not found` | Run First-Time Setup (clone + venv + pip install) |
| `LLM endpoint HTTP 401` | Set `OPENAI_API_KEY` or configure in `config.arc.yaml` |
| Experiment timeout | Increase `experiment.time_budget_sec` in config |
| PIVOT loop exhausted | Max 2 pivots reached; review hypothesis quality manually |
| Python version error | Requires Python 3.11+; use `/opt/homebrew/bin/python3.11` |

## Skills Composed

| Skill | Role |
|---|---|
| `auto-research-distribute` | Post-pipeline distribution to Notion, Slack, NLM, PPTX |

## Related Skills

| Skill | When to Use Instead |
|---|---|
| `paper-review` | Reviewing an existing paper (not generating new research) |
| `related-papers-scout` | Finding related papers without running experiments |
| `parallel-deep-research` | Deep web research without paper generation |
| `nlm-arxiv-slides` | Converting an existing arXiv paper to slides |
| `alphaxiv-paper-lookup` | Quick overview of a specific arXiv paper |
