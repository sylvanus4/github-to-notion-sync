---
name: diagnose
description: >-
  Run 3 parallel analysis agents (Root Cause, Error Context, Impact) to
  diagnose bugs, errors, and performance issues, then synthesize findings into a
  single root cause and apply a fix. Includes blast radius warning for changes
  affecting >5 files, 3-strike escalation, and no-fix-without-investigation
  iron law. Use when the user runs /diagnose, asks to "find the bug", "debug
  this", "why is this failing", "root cause analysis", or "diagnose the error".
  Do NOT use for code review (use /simplify or /deep-review), new feature work,
  or general Q&A. Korean triggers: "진단", "리뷰", "디버깅", "수정".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Diagnose — Root Cause Analysis and Fix

When something is broken, run 3 parallel analysis agents to find the root cause from different angles, synthesize a diagnosis, and apply a fix.

## Iron Laws

### No Fix Without Investigation

**NEVER propose a fix before completing Step 3 (Synthesis).** The temptation to "just try this quick fix" is the #1 source of masking bugs. The sequence is always: gather → analyze → synthesize → THEN fix.

### Blast Radius Warning

If the proposed fix touches **more than 5 files**, display a warning:

```
⚠️ BLAST RADIUS WARNING
========================
This fix touches [N] files across [M] directories.

Files affected:
  1. [file] — [change description]
  2. [file] — [change description]
  ...

Risk: High blast radius increases regression probability.
Recommendation: Consider splitting into smaller, testable changes.
Continue? [Yes / Split into phases / Abort]
```

### 3-Strike Escalation

If 3 consecutive fix attempts fail (fix applied → new error introduced → reverted):

1. **Strike 1**: Revert, try alternative fix approach
2. **Strike 2**: Revert, broaden investigation scope (check related systems)
3. **Strike 3**: **STOP.** Report all findings and state explicitly:

```
🛑 3-STRIKE ESCALATION
=======================
3 consecutive fix attempts failed. Stopping to prevent further damage.

Attempted fixes:
  1. [fix description] → [failure reason]
  2. [fix description] → [failure reason]
  3. [fix description] → [failure reason]

Root cause is likely deeper than initially diagnosed.
Recommended next step: [manual investigation / pair debugging / architecture review]
```

Do NOT attempt a 4th fix. Present findings and ask for human guidance.

## Usage

```
/diagnose                              # analyze current error/issue in context
/diagnose "TypeError in auth module"   # diagnose specific error message
/diagnose src/api/auth.ts              # diagnose specific file
/diagnose --no-fix                     # analysis only, no auto-fix
```

## Workflow

### Step 1: Gather Error Context

Collect all available evidence:

1. **Linter errors**: Run `ReadLints` on relevant files
2. **Recent changes**: `git diff HEAD` and `git log --oneline -5`
3. **Error message**: From user input or terminal output
4. **Related files**: Read files mentioned in error traces or user input
5. **Git blame**: Check who last modified the problematic lines

If the user provides an error message, extract: file path, line number, error type, and stack trace.

### Step 2: Launch 3 Parallel Analysis Agents

Use the Task tool to spawn 3 sub-agents. Each receives the full error context.

For detailed prompts, see [references/agent-prompts.md](references/agent-prompts.md).

```
Agent 1: Root Cause Agent      → 5 Whys, systems thinking, dependency tracing
Agent 2: Error Context Agent   → Stack trace analysis, error patterns, related code
Agent 3: Impact Agent          → Side effects, regression risk, performance impact
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `true`

Each agent returns:

```
ANALYSIS: [agent type]
ROOT_CAUSE: [one-line root cause hypothesis]
CONFIDENCE: [High|Medium|Low]
EVIDENCE:
- [supporting evidence 1]
- [supporting evidence 2]
FIX:
  file: [path]
  line: [number or range]
  current: [current code]
  proposed: [fixed code]
SIDE_EFFECTS:
- [potential side effect or risk]
```

### Step 3: Synthesize Diagnosis

1. Compare root cause hypotheses from all 3 agents
2. Identify consensus (2+ agents agree = high confidence)
3. If agents disagree, weigh by evidence strength
4. Produce a single diagnosis with confidence level

### Step 4: Apply Fix (skip if `--no-fix`)

1. Select the fix proposal with highest confidence and lowest side-effect risk
2. Read the target file
3. Apply fix via StrReplace
4. Run `ReadLints` to verify no regressions

If fix introduces new errors, revert and present the fix as a suggestion instead.

### Step 5: Diagnosis Report

```
Diagnosis Report
================
Error: [error description]
Confidence: [High|Medium|Low]

Root Cause:
  [2-3 sentence explanation of the root cause]

Evidence:
  1. [evidence from Agent 1]
  2. [evidence from Agent 2]
  3. [evidence from Agent 3]

Fix Applied:
  File: [path]
  Change: [description of what was changed]

Side Effects & Risks:
  - [risk 1]
  - [risk 2]

Verification: [PASS|FAIL]

Recommended Follow-up:
  1. [additional action if needed]
  2. [test to write]
```

## Examples

### Example 1: Runtime error

User runs `/diagnose "TypeError: Cannot read property 'id' of undefined"`.

Actions:
1. Parse error: likely null reference, search for `.id` access patterns
2. Gather: recent diff shows new API endpoint, git blame on error line
3. 3 agents analyze: Root Cause finds missing null check, Error Context traces the call chain, Impact identifies 2 other similar patterns
4. Consensus: missing null guard on API response (High confidence)
5. Fix: add `?.` optional chaining and fallback
6. Lint passes, report with fix and 2 similar patterns to check

### Example 2: Performance regression

User runs `/diagnose src/api/search.ts` after noticing slow response times.

Actions:
1. Read file, check recent changes, run lint
2. 3 agents: Root Cause finds N+1 query, Error Context traces the ORM calls, Impact calculates O(n*m) complexity
3. Consensus: N+1 query in search handler (High confidence)
4. Fix: add `.include()` / join to eliminate N+1
5. Report with performance impact estimate

### Example 3: Analysis only

User runs `/diagnose --no-fix "Intermittent 500 error on /api/users"`.

Actions:
1. Gather context: recent logs, endpoint code, middleware chain
2. 3 agents analyze from different angles
3. Synthesis: race condition in connection pool (Medium confidence)
4. No fix applied; report with diagnosis and recommended fix approach

## Error Handling

| Scenario | Action |
|----------|--------|
| No error context provided | Ask user for error message, file path, or symptoms |
| No files identified | Search codebase for error-related keywords |
| Agents disagree on root cause | Present all hypotheses ranked by confidence |
| Fix introduces new errors | Revert fix, present as suggestion |
| Error is in external dependency | Report as external issue with workaround suggestion |

## Troubleshooting

- **"Not enough context"**: Provide the error message, stack trace, or file path
- **Low confidence diagnosis**: Agents may need more context; try specifying the exact file
- **Fix reverted**: The fix was unsafe; review the suggested fix manually
- **Multiple root causes**: Complex bugs may have compound causes; diagnose iteratively


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
