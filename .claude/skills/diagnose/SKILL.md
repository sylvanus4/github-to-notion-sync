---
name: diagnose
description: >-
  Run 3 parallel analysis agents (Root Cause, Error Context, Impact) to diagnose bugs,
  errors, and performance issues, then synthesize findings and apply a fix. Includes
  blast radius warning, 3-strike escalation, and no-fix-without-investigation iron law.
  Supports --file-issue mode to create a GitHub issue instead of inline fixing.
disable-model-invocation: true
---

# Diagnose — Root Cause Analysis and Fix

When something is broken, run 3 parallel analysis agents to find the root cause from different angles, synthesize a diagnosis, and apply a fix.

## Usage

```
/diagnose                    # diagnose and fix
/diagnose --file-issue       # diagnose and create GitHub issue instead of fixing
/diagnose <error message>    # diagnose specific error
```

## Iron Laws

### No Fix Without Investigation

**NEVER propose a fix before completing Step 3 (Synthesis).** The sequence is always: gather -> analyze -> synthesize -> THEN fix.

### Blast Radius Warning

If the proposed fix touches **more than 5 files**, display a warning with affected files and risk assessment. Ask user whether to proceed, split into phases, or abort.

### 3-Strike Escalation

If 3 consecutive fix attempts fail:
1. **Strike 1**: Revert, try alternative fix approach
2. **Strike 2**: Revert, broaden investigation scope
3. **Strike 3**: **STOP.** Report all findings and ask for human guidance. Do NOT attempt a 4th fix.

## Workflow

### Step 1: Gather Evidence

Collect error context from:
- Error messages, stack traces, logs
- Recent git changes (`git log --oneline -10`, `git diff`)
- Related test failures
- Configuration/environment state

### Step 2: Fan Out 3 Analysis Agents

**Agent 1: Root Cause Analyzer**
- Trace the error to its origin in the code
- Identify the specific line/function where behavior diverges
- Check git blame for recent changes to the area

**Agent 2: Error Context Analyzer**
- Map the full execution path leading to the error
- Identify all inputs, state, and dependencies involved
- Check for environmental factors (config, deps, OS)

**Agent 3: Impact Analyzer**
- Assess blast radius: what else could be affected
- Check for related patterns elsewhere in codebase
- Identify regression risk of potential fixes

### Step 3: Synthesize Diagnosis

Merge findings from all 3 agents into a single diagnosis:

```markdown
## Diagnosis

**Root Cause**: [one-sentence description]
**Evidence**: [specific code locations and reasoning]
**Confidence**: [High/Medium/Low with justification]
**Impact**: [what's broken and what else could break]
```

### Step 4: Apply Fix (or File Issue)

**Default mode**: Apply the minimal fix, run tests, verify.

**--file-issue mode**: Create a GitHub issue with:
- Problem description with reproduction steps
- Root cause analysis
- Proposed fix approach (TDD-based RED-GREEN plan)
- Affected files and blast radius

### Step 5: Verify

After applying a fix:
1. Run the specific failing test/scenario
2. Run related test suite
3. Confirm no new errors introduced

## Output Format

```markdown
## Diagnosis Report

### Problem
[description of the observed error]

### Root Cause
[specific cause with code references]

### Fix Applied
[description of changes made]

### Verification
[test results confirming the fix]

### Remaining Risk
[any known limitations or follow-up needed]
```

## Test Invocation

```
/diagnose
/diagnose --file-issue
/diagnose "TypeError: Cannot read property 'id' of undefined"
```
