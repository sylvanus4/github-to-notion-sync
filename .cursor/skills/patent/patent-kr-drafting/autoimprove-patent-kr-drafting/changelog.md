# patent-kr-drafting Autoimprove Changelog

## v1-mutations (2026-04-13)

### Mutations Applied (6)

1. **M1 (EVAL 1)**: Added MANDATORY file persistence instruction for `support-basis-matrix.md` — must be written to disk before claim drafting begins. Agent must STOP if file cannot be persisted.

2. **M2 (EVAL 2)**: Added **3-Category Gate** after claim drafting — agent must count independent claim categories and draft missing categories (방법/장치/기록매체) before proceeding to specification.

3. **M3 (EVAL 3)**: Added **1:1 Verification Pass** — after specification drafting, iterate every claim element to confirm mapping to (a) specification paragraph number and (b) drawing reference numeral. Unmapped elements must be resolved.

4. **M4 (EVAL 4)**: Added **"상기" Scan** — linear scan of each independent claim to verify every "상기 X" has a preceding mention of "X" in the same claim. Dangling references are flagged and rewritten.

5. **M5 (EVAL 5)**: Added **AI/SW Enforcement Gate** — for AI/ML/SW inventions, verify (1) system claim has 프로세서+메모리, (2) method claims reference HW context, (3) spec describes HW-SW cooperation. Missing elements must be added.

6. **M6 (EVAL 6)**: Added **Length Gate** for abstract — count Korean characters after drafting and trim to ≤400 if exceeded. Final character count is reported in output.

### Results

- Baseline average pass rate: 63.4%
- v1-mutations average pass rate: 100.0%
- Improvement: +36.6 percentage points
- Size growth: 12974 → 14618 bytes (+12.7%, within 20% gate)
