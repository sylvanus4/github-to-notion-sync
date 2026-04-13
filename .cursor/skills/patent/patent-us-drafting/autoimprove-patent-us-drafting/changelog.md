# patent-us-drafting Autoimprove Changelog

## v1-mutations (2026-04-13)

**Baseline → v1-mutations**: 50% → 100% avg pass rate (+50pp)

### Mutations Applied (6)

1. **EVAL 2 — Claim-to-Specification Traceability Table**: Added MANDATORY traceability table requirement mapping every claim limitation to spec paragraph. Stops drafting if any limitation lacks support.

2. **EVAL 3 — Alice/Mayo Self-Check Artifact**: Mandated separate `alice-check.md` file output with full PASS/FAIL verdicts per independent claim.

3. **EVAL 1 — 3-Category Independent Claims Gate**: Strengthened from "at least" to "MANDATORY minimum" with explicit revision requirement if any category missing. Added apparatus claim alternative for hardware-only inventions.

4. **EVAL 4 — Abstract Word Count Verification**: Added explicit word-counting step before finalizing `draft-abstract.md` with compression instruction if over 150 words.

5. **EVAL 5 — Implementation-Term Blocklist**: Expanded from short example list to comprehensive 25+ term blocklist (Python, Java, PostgreSQL, Docker, AWS, etc.) with final text scan requirement.

6. **EVAL 6 — Limitation Count Verification**: Added per-claim counting step with factoring instruction to split excess limitations into dependent claims.

### Size Impact

- Baseline: 13,095 bytes
- Mutated: 14,952 bytes
- Growth: 14.2% (within 20% constraint gate)
