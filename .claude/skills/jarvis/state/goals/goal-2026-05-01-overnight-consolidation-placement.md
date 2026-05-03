# Placement Decisions — Consolidation Iter 2

Goal: goal-2026-05-01-overnight-consolidation
Generated: 2026-05-03 09:43

Decision matrix for 4 patterns needing apply (PARTIAL or MISSING).

## P4 — vLLM 0.7+ deep-gemm 2-tier fallback

**Decision**: Augment existing Known Issues section in `.claude/skills/runpod-nvfp4-quantize/SKILL.md`.
**Reason**: Already has a row for it; just lacks the explicit fallback strategy. Local touch, no rule needed (skill-specific).
**Edit**: Expand the deep_gemm row in Known Issues table with explicit "PyPI wheel → git source → warn-and-skip" sequence and reference `runpod_bootstrap.sh` lines.

## P8 — Stop hook flag-file pattern (reusable rule)

**Decision**: Create new always-on rule `.claude/rules/hook-flag-file-pattern.md`.
**Reason**: Pattern used 2x already (kb-intel-compile, jarvis goal-continuation). Future Stop-hook–driven workflows benefit from a templatized rule. Always-on (every turn) because hooks fire every turn.
**Size budget**: <2KB to satisfy token-diet-hygiene rule.
**Content**: When to use flag files vs always-run; cheap fast-path on absent flag; flag delete-after-process; safe re-entry via `stop_hook_active` check.

## P9 — REPO_ROOT path-depth rule

**Decision**: Create new always-on rule `.claude/rules/repo-root-path-depth.md`.
**Reason**: Bit us 2x in `claude-code-trainset-distill` scripts (parents[3] vs parents[4]). Pattern repeats across all `.claude/skills/<skill>/scripts/*.py` files. Always-on because it applies whenever a script under a skill needs repo root.
**Size budget**: <1.5KB.
**Content**: Reference table mapping script depth → correct `parents[N]` value; include verification one-liner.

## P10 — Mechanical-only extraction archetype

**Decision**: Add explicit "Archetype" section to `.claude/skills/claude-code-trainset-distill/SKILL.md`.
**Reason**: Skill already mentions cost=$0 but doesn't name the pattern as reusable. No new rule needed — the SKILL.md is the canonical reference for this kind of work.
**Edit**: Add `## Archetype: Mechanical-Only Extraction` section near top, list invariants (no LLM API, regex-only, idempotent, reusable for other transcript-type skills).
