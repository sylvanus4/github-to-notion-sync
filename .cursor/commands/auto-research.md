---
description: "Run the AutoResearchClaw 23-stage autonomous research pipeline — transforms a research topic into a conference-ready paper with real literature, sandbox experiments, peer review, and LaTeX export"
---

# Auto Research — Autonomous Research Pipeline

## Skill Reference

Read and follow the skill at `.cursor/skills/auto-research/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Extract from user arguments:

- **topic** (required): The research topic to investigate
- **mode**: `sandbox` (default), `docker`, `simulated` — experiment execution mode
- **conference**: `neurips_2025` (default), `iclr_2026`, `icml_2026` — LaTeX template
- **auto-approve**: Whether to auto-approve gate stages (default: yes)
- **from-stage**: Resume from a specific stage name (e.g., `PAPER_OUTLINE`)
- **resume**: Resume from last checkpoint
- **distribute**: Whether to run distribution after completion (default: ask)

### Step 2: Pre-flight

1. Check AutoResearchClaw installation:

```bash
cd ~/thaki/AutoResearchClaw && source .venv/bin/activate && researchclaw --help
```

2. If not installed, follow the First-Time Setup in the skill reference.

3. Verify LLM API key:

```bash
echo $OPENAI_API_KEY | head -c 8
```

### Step 3: Configure

Update `~/thaki/AutoResearchClaw/config.arc.yaml` with the user's topic and preferences.
See `references/configuration-guide.md` for config section details.

### Step 4: Run Pipeline

```bash
cd ~/thaki/AutoResearchClaw && source .venv/bin/activate
researchclaw run \
  --config config.arc.yaml \
  --topic "<topic>" \
  --auto-approve
```

Add `--output <dir>`, `--from-stage <STAGE>`, `--resume`, or `--skip-noncritical-stage` as needed.

### Step 5: Report Results

1. Read `pipeline_summary.json` for overall status
2. Read `deliverables/manifest.json` for packaged files
3. Report: stages completed, failures, quality score, citation verification score
4. List deliverable files with paths

### Step 6: Offer Distribution

Unless `--skip-distribute` was specified, ask whether to run `/auto-research-distribute`
to distribute results to Notion, Slack, NotebookLM, and PPTX.

## Constraints

- Always use the venv at `~/thaki/AutoResearchClaw/.venv/`
- Never modify AutoResearchClaw source code
- Papers generated with `simulated` mode should be clearly flagged
- Monitor long-running pipelines by checking `heartbeat.json`
