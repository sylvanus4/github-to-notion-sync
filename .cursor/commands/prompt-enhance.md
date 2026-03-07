## Prompt Enhance

Improve an existing prompt's clarity and quality without full restructuring. Keeps the original structure intact while fixing language, ambiguity, and enforcement issues.

### Usage

```bash
/prompt-enhance [--focus <area>]
```

### Options

- None: Apply all enhancement areas to current file or selected text
- `--focus <area>`: Focus on a specific area — one of: `ambiguity`, `structure`, `enforcement`, `examples`

### Focus Areas

| Area | What It Does |
|------|-------------|
| `ambiguity` | Replace vague expressions ("if possible", "try to", "as needed") with precise directives |
| `structure` | Add missing headings, reorder sections logically, consolidate scattered instructions |
| `enforcement` | Upgrade "recommended" to "mandatory" where appropriate, add MUST/SHOULD/MAY markers |
| `examples` | Add concrete input/output examples for instructions that lack them |

### Basic Examples

```bash
# Enhance all aspects of the current prompt
/prompt-enhance
"Improve this prompt's clarity and quality"

# Fix only ambiguous language
/prompt-enhance --focus ambiguity
"Replace all vague expressions with precise directives"

# Add enforcement levels
/prompt-enhance --focus enforcement
"Add MUST/SHOULD/MAY markers to all instructions"

# Add missing examples
/prompt-enhance --focus examples
"Add concrete examples where they are missing"

# Improve structure without changing content
/prompt-enhance --focus structure
"Reorganize this prompt's structure for clarity"
```

### Differences from /prompt-transform

| Aspect | `/prompt-enhance` | `/prompt-transform` |
|--------|-------------------|---------------------|
| Scope | Targeted improvements | Full restructuring |
| Structure | Preserves original layout | Applies type-specific template |
| Speed | Quick pass | Comprehensive 5-step workflow |
| Use case | Polish a decent prompt | Rebuild a rough prompt |

### Notes

- Use `/prompt-enhance` when the prompt is already structured but needs polishing
- Use `/prompt-transform` when the prompt needs fundamental restructuring
- Use `/check-prompt` to score the prompt before and after enhancement
- The enhanced version is presented for review; the original is never modified in-place
