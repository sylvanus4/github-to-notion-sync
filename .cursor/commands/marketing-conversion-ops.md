---
description: "Conversion rate optimization — CRO landing page audit and survey-to-lead-magnet engine"
argument-hint: "[audit|survey] [URL or CSV path]"
---

# Marketing Conversion Ops

Read and follow the skill at `.cursor/skills/marketing/marketing-conversion-ops/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the requested conversion operation:

| Command | Script | Purpose |
|---------|--------|---------|
| `audit` | `scripts/cro_audit.py` | 8-dimension CRO audit (--url or --urls) |
| `survey` | `scripts/survey_lead_magnet.py` | Survey CSV to lead magnet briefs (--csv) |

No API keys required. Optional: `--industry` for benchmark comparison, `--json` for machine-readable output.
