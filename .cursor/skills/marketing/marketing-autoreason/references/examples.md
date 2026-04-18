# Example invocations

## Example A — Email subject lines (EN)

**User:** "Tournament 3 subject lines for enterprise GPU cloud waitlist re-engagement; winners had 38% open, losers ~12%."

**Orchestrator actions:**

1. `run_id`: `email-gpu-waitlist-001`
2. `task_spec`: "Produce exactly 3 email subject lines, <=60 chars each, US enterprise CTO tone, no emoji, single theme: reserved capacity spot opening."
3. `knowledge-pack.md`: user pastes anonymized subject table + open rates.
4. Run autoreason passes until convergence or max_passes.
5. Deliver `final_output.md` to user.

## Example B — One-paragraph positioning (KO)

**User:** "한국어로 B2B AI 보안 포지셔닝 한 단락; 경쟁사 A/B는 knowledge-base sales-playbook에서 인용."

**Orchestrator actions:**

1. `kb-query` or `kb-search` competitive-intel for A/B claims (with citations in pack).
2. `task_spec`: Korean, one paragraph, <=120 Korean characters (or syllable budget user gives).
3. `marketing-rubric.md` judges.
4. Output `final_output.md` in Korean.

## Example C — Ad brief hook only

**User:** "LinkedIn ad primary text hook, 125 chars, product analytics SaaS, no customer names."

**Orchestrator actions:**

1. Evidence optional; if none, `EVIDENCE: none`.
2. Strict character cap in synthesizer + judge prompts.
3. Convergence k=2 default.
