## Experiment 0 (baseline)

- Scored 4/20 across 4 binary evals × 5 canonical test inputs (role/HF finance template).
- Failures: composed-skill delegation table not mandatory; strict relevance-before-body + Korean action items with 담당/기한 absent (HF skills: Korean narrative gate missing).

## Experiment 1

- Inserted **Agent Response Contract (Binary Eval Gate)** into SKILL.md.
- Maps directly to EVAL 1–4: 선행 관련도, ≥3 위임 스킬 표, 한국어 구조, 실행 액션 플랜.
- Stopped after one improving mutation; pass rate ≥ 95% (target met at 100%).
