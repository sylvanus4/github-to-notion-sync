---
description: "Design and manage autonomous agent loops with checkpoints, recovery, and progress tracking"
---

# ECC Loop — Autonomous Agent Loop Management

## Skill Reference

Read and follow the skill at `.cursor/skills/ecc-autonomous-loops/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the operation:

- **design <task>**: Design a new autonomous loop architecture for the given task
- **status**: Show status of any running or paused loops
- **checkpoint**: Create a checkpoint for the current loop iteration
- **recover <checkpoint>**: Resume from a saved checkpoint
- No arguments: Show available loop patterns and usage guide

### Step 2: Execute

For **design** mode:
1. Decompose the task into loop iterations
2. Define checkpoint frequency (every N files, every phase, or time-based)
3. Define exit criteria (all tests pass, coverage threshold, task list complete)
4. Generate the loop configuration

For **checkpoint** mode:
1. Save current progress to a structured checkpoint file
2. Include: completed work, pending items, file changes, git state
3. Store at `tasks/loop-checkpoints/`

For **recover** mode:
1. Load checkpoint state
2. Verify file integrity since checkpoint
3. Resume from the last completed step

### Step 3: Report

Show the loop design, checkpoint status, or recovery result.

## Constraints

- Maximum 20 iterations per loop (prevent runaway)
- Always create a checkpoint before risky operations
- Commit at each checkpoint to maintain rollback points
