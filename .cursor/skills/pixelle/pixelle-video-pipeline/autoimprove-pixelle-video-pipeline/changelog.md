# pixelle-video-pipeline Autoimprove Changelog

## Iteration 1 — Mutation M1-LANG-VOICE
**Target:** EVAL-05 (Internationalization Guidance)
**Change:** Added "Language-to-Voice Mapping" section with a table mapping 5 languages (English, Korean, Japanese, Chinese, Spanish) to Edge-TTS voice names (female/male).
**Result:** EVAL-05 moved from PARTIAL → PASS. Agents can now select the correct TTS voice based on content language without guessing.

## Iteration 2 — Mutation M2-MANIFEST
**Target:** EVAL-06 (Output Schema Completeness)
**Change:** Added "Manifest Schema" section defining the required JSON structure for `manifest.json`, including `pipeline_id`, `created_at`, `topic`, `platform`, `phases` (with per-phase status/output), `final_video`, `total_duration_sec`, and optional `errors` array.
**Result:** EVAL-06 moved from FAIL → PASS. Agents now have an unambiguous contract for the manifest output file.

## Iteration 3 — Mutation M3-SUBAGENT-FAIL
**Target:** EVAL-07 (Failure Handling Granularity) + EVAL-08 (Inter-Phase Data Flow)
**Change:** Updated "Subagent Contract" table to include:
- A "Blocking?" column classifying each subagent as BLOCKING or non-blocking
- Explicit intermediate artifact paths using `{dir}` convention (e.g., `{dir}/phase1-script.md`, `{dir}/phase2-raw.mp4`)
- Failure handling rules: BLOCKING failures abort; non-blocking failures log and continue with PARTIAL status
**Result:** EVAL-07 moved from PARTIAL → PASS. EVAL-08 moved from PARTIAL → PASS. Agents now know which failures are fatal vs. recoverable, and where to find/write intermediate artifacts.

## Final Scorecard

| Eval ID | Dimension | Baseline | Final |
|---------|-----------|----------|-------|
| EVAL-01 | Phase Dependency Clarity | PASS | PASS |
| EVAL-02 | Error Recovery Guidance | PASS | PASS |
| EVAL-03 | Partial Execution Support | PASS | PASS |
| EVAL-04 | Verification Concreteness | PASS | PASS |
| EVAL-05 | Internationalization Guidance | PARTIAL | **PASS** |
| EVAL-06 | Output Schema Completeness | FAIL | **PASS** |
| EVAL-07 | Failure Handling Granularity | PARTIAL | **PASS** |
| EVAL-08 | Inter-Phase Data Flow | PARTIAL | **PASS** |

**Score: 8/8 PASS (baseline was 4 PASS + 3 PARTIAL + 1 FAIL)**
