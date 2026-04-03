---
description: Autonomous marketing experiment lifecycle — create, score, pacing alerts, weekly scorecards
argument-hint: "[create|log|score|playbook|suggest|scorecard|pacing] [context]"
---

## Marketing Growth Engine

Autonomous marketing experiment lifecycle: statistical scoring, pacing alerts, and weekly scorecards.

### Execution

Read and follow the `marketing-growth-engine` skill (`.cursor/skills/marketing/marketing-growth-engine/SKILL.md`) and run the Python scripts under `scripts/` as documented.

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/experiment-engine.py` | create, log, score, playbook, suggest |
| `scripts/autogrowth-weekly-scorecard.py` | weekly digest |
| `scripts/pacing-alert.py` | spend/volume pacing |

### Examples

```bash
# From repo root, with Python deps: pip install numpy scipy
python .cursor/skills/marketing/marketing-growth-engine/scripts/experiment-engine.py --help
python .cursor/skills/marketing/marketing-growth-engine/scripts/autogrowth-weekly-scorecard.py --help
python .cursor/skills/marketing/marketing-growth-engine/scripts/pacing-alert.py --help
```
