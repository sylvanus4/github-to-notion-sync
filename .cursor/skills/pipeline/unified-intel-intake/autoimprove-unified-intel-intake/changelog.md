# unified-intel-intake Autoimprove Changelog

## Baseline Score: 75% (3/4 evals passing)

### Round 1: Explicit domain lists for news vs blog (KEPT ✅)
- **What:** Replaced vague "News domains" and "Blog posts, Medium, Substack" with explicit domain lists and URL path patterns
- **Why:** EVAL 1 (content type classification) failed — no way to distinguish techcrunch.com (news) from a personal blog without explicit domain lists
- **Impact:** EVAL 1 now passes. Score: 100%
- **Files changed:** Content Type Detection table

### Round 2: Unknown domain fallback (KEPT ✅)
- **What:** Added auto-detect row for unknown domains — extract with defuddle, then LLM-classify based on content structure signals (byline, dateline → news; personal voice → blog)
- **Why:** Domain lists can't cover every site; fallback ensures graceful degradation
- **Impact:** Score stable at 100%. Covers long-tail URLs.
- **Files changed:** Content Type Detection table (new row)

### Round 3: Multi-topic tiebreak rule (KEPT ✅)
- **What:** Added explicit instruction: use strongest keyword density, prefer specific topics when tied
- **Why:** Topic Classification said nothing about what happens when content matches multiple topics
- **Impact:** Score stable at 100%. Prevents random channel routing.
- **Files changed:** Topic Classification section header

### Round 4: YouTube content type detection (KEPT ✅)
- **What:** Added youtube.com/youtu.be → Video type with defuddle transcript extraction
- **Why:** YouTube URLs were missing from the content type table despite defuddle supporting YouTube transcripts
- **Impact:** Score stable at 100%. Adds missing content type.
- **Files changed:** Content Type Detection table (new row)

## Final Score: 100% (4/4 evals passing)
## Improvement: +25 percentage points (75% → 100%)
