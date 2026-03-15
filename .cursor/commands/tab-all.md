---
description: "Run all 12 tab automation skills sequentially with proper dependency ordering — equivalent to the full daily pipeline"
---

# Tab All — Run Full Tab Automation Pipeline

## Skill Reference

Read and follow the skill at `.cursor/skills/today/SKILL.md`, specifically the "Tab Automation Pipeline (API-Driven)" section.

## Your Task

User input: $ARGUMENTS

Run all 12 tab automation skills in dependency order:

**Phase 1 — Data Collection (parallel):**
1. tab-stock-sync
2. tab-event-detect
3. tab-fundamental-sync
4. tab-hot-stock-discovery

**Phase 2 — Computation (after data sync):**
5. tab-technical-analysis
6. tab-turtle-refresh
7. tab-bollinger-refresh
8. tab-dualma-refresh
9. tab-screening

**Phase 3 — Analysis (after computation):**
10. tab-analysis-run
11. tab-llm-agents
12. tab-genai-features

If $ARGUMENTS contains "skip-<phase>" flags, skip the corresponding phase.

## Constraints

- Requires backend server running on port 4567
- Requires PostgreSQL running on port 5432
- Run Phase 1 skills in parallel where possible
- Phase 2 depends on Phase 1 completion
- Phase 3 depends on Phase 2 completion
