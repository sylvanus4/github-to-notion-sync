# standup-digest Autoimprove Changelog

## Baseline Score: 75% (3/4 evals passing)

### Round 1: Commit completeness verification (KEPT ✅)
- **What:** Added instruction to verify total_count from API response, fetch all pages if >30 results, and log commit count per person
- **Why:** EVAL 2 (all commits included) failed — skill fetched commits but never verified the response was complete (pagination could truncate results)
- **Impact:** EVAL 2 now passes. Score: 100%
- **Files changed:** Step 2 GitHub section

### Round 2: Vacation/no-activity handling (KEPT ✅)
- **What:** Enhanced no-activity handling to check calendar for OOO events and suggest PTO/holiday explanation
- **Why:** Generic "No activity recorded" doesn't help team leads distinguish between forgotten updates and legitimate time off
- **Impact:** Score stable at 100%. Better context for managers.
- **Files changed:** Error Handling table

### Round 3: Cross-repository commit collection (KEPT ✅)
- **What:** Changed "Commits" to "Commits (across all org repos)" in data sources
- **Why:** Team members often work across multiple repositories; limiting to one repo misses activity
- **Impact:** Score stable at 100%. More complete activity capture.
- **Files changed:** Data Sources table

### Round 4: Timezone awareness (KEPT ✅)
- **What:** Added timezone specification for "yesterday" definition (default: Asia/Seoul)
- **Why:** Distributed teams need consistent time boundaries; "yesterday" is ambiguous without timezone
- **Impact:** Score stable at 100%. Prevents cross-timezone attribution errors.
- **Files changed:** Step 2 opening line

## Final Score: 100% (4/4 evals passing)
## Improvement: +25 percentage points (75% → 100%)
