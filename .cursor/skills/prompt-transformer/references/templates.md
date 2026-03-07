# Structural Templates

Apply the matching template for the classified prompt type. Each template provides the required sections and structure for that type.

## System Prompt Template

```
# Role & Identity
[Who the AI is, domain expertise, persona]

# Core Objectives
[Numbered list of primary goals]

# Constraints
[Absolute prohibitions and boundaries]

# Input Format
[What the AI receives and how to parse it]

# Output Format
[Exact structure, fields, language of response]

# Examples
[1-3 concrete input/output pairs]

# Edge Cases
[How to handle ambiguous, empty, or malformed input]
```

## Cursor Rule Template

```
# [Rule Title]

## Scope
[Files, directories, or contexts this rule applies to]

## Instructions
[Clear directives using imperative mood]

## Anti-Patterns
[What to avoid, with brief rationale]

## Examples
[Correct vs incorrect patterns]
```

## SKILL.md Template

```
---
name: [lowercase-hyphenated]
description: [What it does. When to use it. Trigger keywords.]
---

# [Skill Name]

## Workflow
[Numbered steps with clear entry/exit criteria]

## Output Format
[Expected deliverable structure]

## References
[Links to reference files with "when to read" guidance]
```

## Task Instruction Template

```
# Context
[Background information the AI needs]

# Task
[Exactly what to do, in imperative mood]

# Constraints
[Boundaries: what NOT to do, limits, requirements]

# Output Format
[Structure, language, length of expected output]

# Acceptance Criteria
[How to verify the task is done correctly]
```

## Generic Prompt Template

```
# Role
[Who the AI should act as]

# Context
[Background, domain, relevant information]

# Task
[Clear instruction in imperative mood]

# Constraints
[Prohibitions and boundaries]

# Output Format
[Expected structure and style]
```
