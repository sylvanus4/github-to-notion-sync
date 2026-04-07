---
description: "Maintain and reference multiple layers of context throughout a conversation"
argument-hint: "push <context> | pop | show | clear"
---

# Multi-Layer Context Manager

Maintain a stack of named context layers. Every subsequent response considers all active layers. Layers persist until popped or cleared.

## Usage

```
/context-stack push We are building a B2B SaaS for GPU cloud management
/context-stack push Target customer: ML teams at Series B+ startups
/context-stack push Constraint: Must support multi-region Kubernetes
/context-stack show
/context-stack pop
/context-stack clear
```

## Your Task

User input: $ARGUMENTS

### Workflow

Parse the operation from `$ARGUMENTS`:

#### `push <context>`
1. Extract the context description after "push"
2. Add as a new numbered layer on top of the stack
3. Confirm: "Layer [N] pushed: [context summary]"
4. All subsequent responses must consider this layer

#### `pop`
1. Remove the most recently pushed layer
2. Confirm: "Layer [N] removed: [context summary]"
3. Subsequent responses no longer consider this layer

#### `show`
1. Display all active context layers in stack order (newest first)
2. Format as numbered list with push time

#### `clear`
1. Remove all context layers
2. Confirm: "All context layers cleared. Starting fresh."

### Output Format

For `show`:
```
## Active Context Stack

| # | Layer | Context |
|---|-------|---------|
| 3 | (top) | [Most recent context] |
| 2 |       | [Earlier context] |
| 1 | (base)| [First context pushed] |
```

### Constraints

- Maximum 7 layers (cognitive overload prevention)
- Each layer must be a distinct, non-overlapping piece of context
- When generating responses, reference active layers explicitly if they influence the answer
- `push` with no argument is an error — prompt for context

### Execution

Reference `ce-context-fundamentals` (`.cursor/skills/ce/ce-context-fundamentals/SKILL.md`) for context management patterns. Reference `ce-context-optimization` (`.cursor/skills/ce/ce-context-optimization/SKILL.md`) for efficient context usage.
