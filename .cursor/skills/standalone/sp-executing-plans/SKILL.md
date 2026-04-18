---
name: executing-plans
description: >-
  Use when you have a written implementation plan to execute in a separate
  session with review checkpoints. Korean triggers: "계획 실행", "구현 플랜". Do
  NOT use for writing plans (use sp-writing-plans).
metadata:
  author: "superpowers"
  version: "1.0.0"
  category: "process"
---
# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## Flags

| Flag | Effect |
|------|--------|
| `--skip-review` | Skip Step 1 critical review. Use when the plan was pre-approved by another skill (e.g., `omc-ralplan` consensus or `ralplan-execute-bridge`). |
| `--auto-accept` | Execute all batches without pausing for "Ready for feedback" between them. Stops only on verification failure or errors. Implies continuous execution. |

Both flags can be combined: `--skip-review --auto-accept` for fully autonomous execution of pre-approved plans.

**Safety override**: regardless of flags, execution always stops on verification failures, missing dependencies, or destructive operations (`rm -rf`, `DROP`, `force-push`).

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. **If `--skip-review`**: skip critical review, create TodoWrite, proceed directly to Step 2
3. Review critically - identify any questions or concerns about the plan
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- **If `--auto-accept`**: proceed to next batch immediately (no pause)
- **Otherwise**: Say "Ready for feedback." and wait

### Step 4: Continue
**If `--auto-accept`**: automatically proceed to next batch after Step 3.

Otherwise, based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **superpowers:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **superpowers:writing-plans** - Creates the plan this skill executes
- **superpowers:finishing-a-development-branch** - Complete development after all tasks

## Examples

### Example 1: Standard workflow
**User says:** Request that triggers this skill
**Actions:** Follow the prescribed process steps in order. Verify each checkpoint before proceeding.
**Result:** Completed workflow with all verification criteria met.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Process step fails | Do not skip — diagnose the failure before proceeding to the next step |
| Verification fails | Roll back to the last passing checkpoint and retry |
| Conflicting with other processes | Follow the priority order defined in the skill |
