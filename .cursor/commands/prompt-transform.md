## Prompt Transform

Transform a rough or casual prompt into a professional-grade prompt with proper structure, clarity, and enforcement.

### Usage

```bash
/prompt-transform [--type <type>] [--strict] [--compare]
```

### Options

- None: Auto-detect prompt type, transform current file or selected text
- `--type <type>`: Force prompt type — one of: `system`, `rule`, `skill`, `task`, `generic`
- `--strict`: Apply strictest transformation (quality score target >= 95)
- `--compare`: Show before/after comparison with quality scores

### Basic Examples

```bash
# Transform selected text or current file into a professional prompt
/prompt-transform
"Transform this prompt into a professional version"

# Transform as a specific type
/prompt-transform --type system
"Transform this into a professional system prompt"

# Transform with before/after comparison
/prompt-transform --compare
"Transform and show the quality improvement"

# Strict mode for production-critical prompts
/prompt-transform --strict
"Transform this prompt to expert-level quality (score >= 95)"

# Combine options
/prompt-transform --type rule --strict --compare
"Transform this into a strict Cursor rule with comparison"
```

### Workflow

This command invokes the `prompt-transformer` skill, which executes:

1. **Classify** the prompt type (auto-detected or forced via `--type`)
2. **Structure** the prompt using the appropriate template
3. **Eliminate ambiguity** by replacing vague expressions with precise directives
4. **Enhance** with role definition, constraints, output format, examples, and edge-case handling
5. **Validate** against the quality checklist (target: 85 default, 95 with `--strict`)

### Supported Prompt Types

| Type | Description |
|------|-------------|
| `system` | System prompts for LLMs (role, constraints, output format) |
| `rule` | Cursor rules (`.mdc` files with scope, instructions, anti-patterns) |
| `skill` | SKILL.md files (frontmatter, workflow, references) |
| `task` | Task instructions (context, steps, constraints, acceptance criteria) |
| `generic` | General-purpose prompts (role, context, task, format) |

### Notes

- The original prompt is never modified in-place; the transformed version is presented for review
- For large prompts (over 500 lines), consider splitting into sections and transforming each separately
- Use `/check-prompt` after transformation for detailed quality scoring
- Use `/prompt-enhance` instead when you only need minor improvements without full restructuring
