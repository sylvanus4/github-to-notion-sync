---
name: deep-review
description: >-
  Run 4 parallel domain-expert agents (Frontend, Backend/DB, Security, Test
  Coverage) to review code from multiple engineering perspectives and auto-fix
  findings. Uses code-review-graph MCP blast radius to expand review scope
  beyond git diff and prioritize high-risk files. Supports diff/today/full
  scoping with Fix-First pattern, adversarial tier scaling by diff size and
  graph risk scores, and 8/10 confidence gate. Use when the user runs
  /deep-review, asks for "full-stack review", "multi-domain review", "review
  frontend and backend", or "comprehensive code review". Do NOT use for
  single-domain review (use /refactor, /security, etc.), code quality metrics
  only (use /simplify), or general Q&A. Korean triggers: "리뷰", "테스트", "수정",
  "보안".
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "execution"
---
# Deep Review — Multi-Domain Full-Stack Review

Review code from 4 engineering perspectives simultaneously: frontend, backend/DB, security, and test coverage. Complements `/simplify` (code craftsmanship) with domain expertise.

## Scoping Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| `diff` (default) | `/deep-review` | Git diff (unstaged + staged + HEAD) |
| `today` | `/deep-review today` | All files changed today |
| `full` | `/deep-review full` | All source files in the project |

Combinable with focus: `/deep-review today focus on security`.

## Adversarial Review Tiers

Review intensity scales with diff size to catch more issues in riskier changes:

| Diff Size | Tier | Behavior |
|-----------|------|----------|
| 1-50 lines | Standard | Normal 4-agent review |
| 51-200 lines | Elevated | Agents additionally check cross-file consistency and integration points |
| 201-500 lines | Adversarial | Agents run with adversarial prompts: "Find at least 3 issues. If you find zero, explain why this code is provably correct." |
| 500+ lines | Critical | Adversarial + mandatory `--refine` loop + blast radius warning |

The tier is auto-detected from `git diff --stat` at the start of the review.

## Confidence Gate (8/10 Threshold)

Every finding must include a confidence score (1-10). Only findings with confidence >= 8 are reported to the user.

- **Confidence 8-10**: Report as a finding, eligible for auto-fix
- **Confidence 5-7**: Log internally but do not surface unless `--show-low-confidence` flag is set
- **Confidence 1-4**: Discard silently

This eliminates false-positive noise and ensures every reported finding is actionable.

## Fix-First Pattern

During review, agents categorize each finding:

| Category | Criteria | Action |
|----------|----------|--------|
| **Auto-fixable** | Single-file, mechanical fix (unused import, missing null check, wrong type, formatting) | Fix silently during Step 4, mention in report as "auto-fixed" |
| **Requires judgment** | Multi-file impact, architectural choice, ambiguous intent | Report as finding with options, let user decide |
| **Informational** | Best practice suggestion, potential future issue | Report as Low severity, never auto-fix |

The goal: reduce review friction by fixing trivial issues automatically, only surfacing decisions that require human judgment.

## Workflow

### Step 1: Identify and Classify Files

Resolve target files using the same scoping as `/simplify` (git diff, git log --since=midnight, or find).

Classify each file by domain:
- **Frontend**: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.css`, `*.scss`, files in `components/`, `pages/`, `views/`, `layouts/`
- **Backend**: `*.py`, `*.go`, `*.rs`, `*.java`, `*.kt`, files in `api/`, `routes/`, `services/`, `middleware/`
- **DB**: `*.sql`, files in `migrations/`, `models/`, `schemas/`, `db/`
- **Test**: `*.test.*`, `*.spec.*`, files in `tests/`, `__tests__/`
- **Shared**: config files, utilities — sent to all agents

### Step 1.5: Graph-Aware Context (when code-review-graph MCP is available)

Before launching domain agents, enrich the review context using the code-review-graph MCP server. If the server is unavailable, skip this step entirely and proceed with file-only context.

1. **Blast radius expansion**: Call `get_impact_radius_tool` with the list of changed files. Add any impacted files NOT already in the review scope (callers, dependents, tests with gaps). This ensures the domain agents see files that WILL break, not just files that DID change.

2. **Structural context**: Call `get_review_context_tool` with the expanded file list. This returns token-optimized structural summaries (callers, callees, inheritance, test coverage) that replace full-file reads for context. Include this summary in each domain agent's prompt.

3. **Risk-scored prioritization**: Call `detect_changes_tool` to get risk-scored change impact. Use risk scores to:
   - Assign higher adversarial tier to high-risk files regardless of diff line count
   - Prioritize Critical/High-risk files for agent attention

4. **Flow impact**: Call `get_affected_flows_tool` with changed files. Include affected execution flows in the Backend/DB agent prompt for cross-cutting concern detection.

Pass the following to each domain agent prompt:
- The expanded file list (blast radius, not just git diff)
- Structural context summary (callers, callees, test gaps per file)
- Risk scores per file
- Affected flows (Backend/DB agent only)

### Step 2: Launch 4 Parallel Review Agents

Use the Task tool to spawn 4 sub-agents. Each agent receives all files but focuses on its domain. For detailed prompts, see [references/agent-prompts.md](references/agent-prompts.md).

```
Agent 1: Frontend Agent     → UI patterns, accessibility, design system, component structure
Agent 2: Backend/DB Agent   → API design, data modeling, query safety, error handling
Agent 3: Security Agent     → OWASP Top 10, auth/authz, input validation, secrets
Agent 4: Test Coverage Agent → Missing tests, edge cases, test quality, assertion gaps
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `true`

Each agent returns findings in this structure:

```
DOMAIN: [agent domain]
TIER: [Standard|Elevated|Adversarial|Critical]
FINDINGS:
- severity: [Critical|High|Medium|Low]
  confidence: [1-10]
  category: [auto-fixable|requires-judgment|informational]
  file: [path]
  line: [number or range]
  issue: [description]
  fix: [suggested change]
```

### Step 3: Aggregate, Filter, and Deduplicate

1. Merge all agent outputs into a single findings list
2. **Apply confidence gate**: discard findings with confidence < 8 (unless `--show-low-confidence`)
3. Remove duplicates (same file + same line + similar issue)
4. Sort: Critical > High > Medium > Low
5. Group by file within same severity
6. Separate into auto-fixable vs requires-judgment buckets

### Step 4: Apply Fixes (Fix-First Pattern)

**Phase A — Silent auto-fixes** (auto-fixable findings, confidence >= 8):
1. Apply all auto-fixable fixes via StrReplace without prompting
2. Log each fix for the report's "Auto-Fixed" section

**Phase B — User-decision fixes** (requires-judgment findings):
1. Present each finding with options
2. Apply only if user approves (or skip in automated mode)

Skip if: conflict with prior fix, ambiguous change, or file already modified at that location.

### Step 5: Verify

1. Run `ReadLints` on all modified files
2. Fix any introduced lint errors

### Step 6: Re-Evaluate (Evaluator-Optimizer Loop)

**Trigger:** Runs automatically when `--refine` flag is set. Skipped by default.

**Pattern:** Evaluator-Optimizer — re-run focused domain agents on modified files to verify fixes resolved the original findings.

1. Collect the list of files modified in Step 4
2. Launch 1-2 focused domain agents (pick the domains with the most Critical/High findings) on ONLY the modified files
   - `subagent_type`: `generalPurpose`, `model`: `fast`, `readonly`: `true`
   - Prompt: "Review these files from a [domain] perspective. Focus on verifying that prior Critical/High findings are resolved."
3. Compare re-evaluation findings against the original findings list
4. If new Critical or High findings exist AND iteration count < 2:
   - Apply fixes for the new findings (same rules as Step 4)
   - Increment iteration counter
   - Return to sub-step 1 of this step
5. If quality threshold is met OR max iterations (2) reached, proceed to report

**Stopping criteria (any one sufficient):**
- No Critical or High findings remain
- Total new findings <= 2 (Low severity only)
- Max 2 refinement iterations reached
- No improvement between iterations (same or more findings)

**If max iterations exhausted with remaining findings:** Include them in the report under "Remaining Issues (post-refinement)".

### Step 7: Report

Present report:

```
Deep Review Report
==================
Scope: [diff|today|full] — [N] files reviewed
Review Tier: [Standard|Elevated|Adversarial|Critical] (diff size: [N] lines)
Confidence Gate: 8/10 (filtered [N] low-confidence findings)

Findings by Domain:
  Frontend:      [N] findings
  Backend/DB:    [N] findings
  Security:      [N] findings
  Test Coverage: [N] findings

Total: [N] (Critical: X, High: X, Medium: X, Low: X)
Auto-Fixed (Fix-First): [N]
User-Decision Fixes: [N] applied / [N] skipped
Refinement: [N] iterations (if --refine used)

Top Issues:
  1. [file] — [domain] — [what was found/fixed] (confidence: X/10)
  2. [file] — [domain] — [what was found/fixed] (confidence: X/10)
```

## Optional Arguments

```
/deep-review                          # diff mode — review uncommitted changes
/deep-review today                    # today mode — all files changed today
/deep-review full                     # full mode — entire project
/deep-review focus on security        # prioritize security findings
/deep-review src/api/                 # scope to specific directory

# Evaluator-Optimizer refinement (combinable with any mode)
/deep-review --refine                 # re-evaluate after fixes (max 2 iterations)
/deep-review today --refine           # today mode + re-evaluation loop

# Confidence and fix control
/deep-review --show-low-confidence    # include findings with confidence 5-7
/deep-review --no-auto-fix            # skip Fix-First silent fixes, report everything
```

## Examples

### Example 1: Post-feature review

User runs `/deep-review` after implementing a new API endpoint with UI.

Actions:
1. `git diff HEAD` finds 8 files (3 frontend, 3 backend, 1 migration, 1 test)
2. 4 agents review in parallel
3. Findings: 1 Critical (SQL injection), 2 High (missing auth check, no error boundary), 3 Medium
4. Apply 5/6 fixes, skip 1 (architectural)
5. Report with domain breakdown

### Example 2: Full project audit

User runs `/deep-review full` for a periodic health check.

Actions:
1. Find 65 source files across frontend/backend/tests
2. 4 agents each review all files from their perspective
3. Findings: 3 Critical, 7 High, 12 Medium, 5 Low
4. Apply fixes by severity, batch by file
5. Comprehensive project health report

### Example 3: Security-focused review

User runs `/deep-review today focus on security` after adding authentication.

Actions:
1. Find 5 files changed today
2. All 4 agents run; Security agent findings highlighted first
3. Findings: 2 High (weak token validation, missing CSRF), 1 Medium
4. All fixes applied
5. Security-focused report

## Error Handling

| Scenario | Action |
|----------|--------|
| No changes detected | Suggest `today` or `full` mode |
| No files match a domain | Agent reports "no files in my domain" and returns empty |
| Sub-agent timeout | Re-launch once; if still fails, report partial results |
| Lint errors after fix | Auto-fix; if unfixable, revert that fix |
| Conflicting fixes across domains | Apply first fix, skip subsequent with explanation |

## Troubleshooting

- **"No files for frontend agent"**: Backend-only projects skip the frontend agent automatically
- **Overlap with /simplify**: `/simplify` checks code craftsmanship; `/deep-review` checks domain correctness. Run both for comprehensive coverage.
- **Large projects**: Files are batched at 50+ files per agent round

## Gotchas

### CRG MCP Availability

Step 1.5 (Graph-Aware Context) is a powerful enhancement but MUST NOT be a hard dependency. If `code-review-graph` MCP server is not running or the graph database doesn't exist:
- Skip Step 1.5 entirely — fall back to file-only context from git diff
- Do NOT report this as a failure; log it as an informational note: "CRG graph unavailable — proceeding with file-only context"
- The review quality degrades gracefully: blast radius expansion is lost, but domain-agent reviews still produce value

### Blast Radius Inflation

`get_impact_radius_tool` can return a large number of transitive dependents. If the expanded file list exceeds 100 files:
- Prioritize files with risk score >= Medium from `detect_changes_tool`
- Cap the expanded list at 80 files (original diff files + highest-risk impacted files)
- Note truncation in the review report: "Blast radius capped at 80 files (N total impacted)"

### False Positive Noise at Scale

With 4 parallel agents and adversarial framing, large diffs (100+ lines) can produce 30+ findings. Most are Low severity noise that obscures Critical issues. Mitigation:
- The confidence gate (< 8 discarded) is the primary filter — never lower it
- For diffs > 200 lines, increase the confidence gate to 9 for Low-severity findings
- Present Critical/High findings first, separated by a clear visual break from Medium/Low

### Subagent Context Limitations

Each domain agent runs as a `fast` model subagent with limited context. For files > 500 lines:
- Provide the CRG structural summary (`get_review_context_tool`) instead of full file content
- If CRG is unavailable, include only the changed hunks (±20 lines context) rather than full files
- Never send full file content of files > 1000 lines to a fast-model subagent

### Auto-Fix Side Effects

The Fix-First Pattern can introduce new issues when auto-fixing. After all auto-fixes in Step 4:
- Run `ReadLints` on every auto-fixed file
- If a fix introduces a new lint error, revert that specific fix and report it as "requires-judgment"
- Never chain auto-fixes: fix A → introduces issue B → auto-fix B. This creates unpredictable cascades.

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, line numbers, exact changes, or concrete data points) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must state how its output is used downstream.
- **Continue vs Spawn decision:**
  - Continue (resume) when worker context overlaps with the next task or fixing a previous failure
  - Spawn fresh when verifying another worker's output or when previous approach was fundamentally wrong
- Use `model: "fast"` for exploration/read-only subagents; default model for generation/analysis

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Subagent Contract

Subagent prompts must include:
- Always use absolute file paths (subagent cwd may differ)
- Share file paths relevant to the task in the final response
- Include code snippets only when the exact text is load-bearing (a bug found, a signature needed)
- Do not recap code merely read — summarize what was learned
- Final response: concise report of what was done, key findings, and files changed
- Do not use emojis
