# skill-autoimprove — pipeline-builder

## Experiment 0 — baseline

**Score:** 13/20 (65.0%)

**Change:** none

**Reasoning:** Implementation detail strong; meta layer missing per canonical user intent.

**Result:** E1/E3 partial failures on cross-domain prompts.

## Experiment 1 — keep

**Score:** 20/20 (100.0%)

**Change:** Added `## Meta-Orchestration` clarifying when to defer to strategist/system/quality/context skills and how to bundle YAML/Makefile outputs.

**Reasoning:** Reduces duplicate pipelines by forcing diff against `daily-today.yml` and listing secrets explicitly.

**Result:** Full pass on all eval cells.
