# gws-email-reply Autoimprove Changelog

## Baseline Score: 80% (4/5 evals passing)

### Round 1: Anti-hallucination guardrail (KEPT ✅)
- **What:** Added explicit instruction to NEVER hallucinate facts; use "확인 후 안내드리겠습니다" fallback for unknown details
- **Why:** EVAL 4 (no hallucinated info) failed 3/3 — skill had no guardrail against inventing pricing, features, or capabilities
- **Impact:** EVAL 4 now passes. Score: 100%
- **Files changed:** Step 4 draft guidelines

### Round 2: Attachment and URL awareness (KEPT ✅)
- **What:** Added error handling for emails with attachments and URLs — acknowledge without claiming to have read unextracted files
- **Why:** Edge case hallucination risk — skill could claim "첨부 파일 검토했습니다" when it never read the attachment
- **Impact:** Score stable at 100%. Prevents false claims.
- **Files changed:** Error Handling table (2 new rows)

### Round 3: Time-sensitivity awareness (KEPT ✅)
- **What:** Added instruction to acknowledge delay in reply opening if email is >48 hours old
- **Why:** Ignoring email age makes replies feel robotic; a >2-day gap without "늦은 답변 죄송합니다" is socially awkward
- **Impact:** Score stable at 100%. Improves social appropriateness.
- **Files changed:** Step 1 Date extraction note

### Round 4: Reply-all default guidance (KEPT ✅)
- **What:** Added clarification that reply-all is default when original email had Cc'd participants
- **Why:** Missing Cc'd people from replies is a common social/professional error
- **Impact:** Score stable at 100%. Reduces user decision burden.
- **Files changed:** Step 7 reply-all command description

## Final Score: 100% (5/5 evals passing)
## Improvement: +20 percentage points (80% → 100%)
