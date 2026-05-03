# Inventory — Pattern Coverage Audit

Generated: 2026-05-02 01:15
Goal: goal-2026-05-01-overnight-consolidation

| Pattern | Coverage | Location | Action Needed |
|---------|----------|----------|---------------|
| P1: NGC image hang / runpod-torch-v280 | OK | `.claude/skills/runpod-nvfp4-quantize/SKILL.md:73` & `:150` | — |
| P2: HF Hub org slug case sensitivity | OK | `.claude/skills/hf-hub/SKILL.md:60-70` & `.claude/skills/runpod-nvfp4-quantize/SKILL.md:34,156` | — |
| P3: Ubuntu 24.04 PEP 668 | OK | `.claude/skills/runpod-pods/SKILL.md:182-191` & `.claude/skills/runpod-nvfp4-quantize/SKILL.md:112,152` | — |
| P4: vLLM 0.7+ deep-gemm requirement | PARTIAL | `.claude/skills/runpod-nvfp4-quantize/SKILL.md:155` mentions `deep_gemm` but doesn't document 2-tier PyPI→git fallback explicitly | Add fallback strategy to runpod-nvfp4-quantize/SKILL.md Known Issues section |
| P5: ModelOpt mtq.quantize schema strictness | OK | `.claude/skills/runpod-nvfp4-quantize/SKILL.md:118-135,154` | — |
| P6: ModelOpt export omits tokenizer | OK | `.claude/skills/runpod-nvfp4-quantize/SKILL.md:136-144` | — |
| P7: build_calib_mini.py SIGABRT 134 + \|\| true workaround | OK | `.claude/skills/runpod-nvfp4-quantize/SKILL.md:116,153` & `runpod_bootstrap.sh:38` | — |
| P8: Stop hook flag-file pattern (reusable) | PARTIAL | `.claude/hooks/kb-intel-compile.py:1-13` documents pattern for intelligence KB; `.claude/skills/jarvis/hooks/goal-continuation.py` uses goal JSONs; pattern NOT generalized | Add `.claude/rules/hook-flag-file-pattern.md` with reusable template |
| P9: REPO_ROOT path-depth bug (.claude/skills/*/scripts/) | MISSING | Mentioned in pattern; `.claude/skills/claude-code-trainset-distill/scripts/extract_*.py` use `parents[4]` (line 18,25) but no documented rule | Add `.claude/rules/repo-root-path-depth.md` with checklist |
| P10: Mechanical-only (no LLM) extraction pattern | PARTIAL | `.claude/skills/claude-code-trainset-distill/SKILL.md:204-207` states "~50ms per MB, Zero token cost" but pattern not called out as a reusable archetype | Add section to SKILL.md or new `.claude/rules/mechanical-extraction-pattern.md` |
| P11: RunPod-torch vs NGC warm cache | OK | `.claude/skills/runpod-nvfp4-quantize/SKILL.md:73,93` documents warm cache angle | — |
| P12: Cross-repo intelligence dedup via intel_registry.py | OK | `.claude/skills/x-to-slack/SKILL.md:45-63`, `.claude/skills/twitter-timeline-to-slack/SKILL.md:43-62`, `scripts/intelligence/intel_registry.py:1-22` | — |

## Summary

- **OK**: 8 patterns (P1, P2, P3, P5, P6, P7, P11, P12)
- **PARTIAL**: 3 patterns (P4, P8, P10) — lack detail or generalization
- **MISSING**: 1 pattern (P9) — no documented rule yet

### Recommended Actions (Priority Order)

1. **P8** (reusable hook pattern): Create `.claude/rules/hook-flag-file-pattern.md` with boilerplate for flag-file–triggered hooks
2. **P9** (REPO_ROOT path-depth): Create `.claude/rules/repo-root-path-depth.md` with checklist for skill script locations
3. **P4** (deep-gemm 2-tier fallback): Enhance runpod-nvfp4-quantize/SKILL.md Known Issues to document PyPI → git fallback explicitly
4. **P10** (mechanical extraction): Add new section to `.claude/rules/mechanical-extraction-pattern.md` documenting cost=$0 mechanical-only skills
