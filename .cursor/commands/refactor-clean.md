# Refactor Clean

Systematic refactoring pipeline: identify code smells, plan changes, execute refactors, and verify nothing breaks.

## Usage

```bash
# Refactor a specific file or directory
/refactor-clean backend/app/services/stock_service.py

# Refactor recent changes
/refactor-clean --scope diff

# Refactor with specific focus
/refactor-clean --focus "extract-method,rename,dead-code"

# Dry-run (report only, no changes)
/refactor-clean --dry-run backend/app/
```

## Instructions

1. **Scope selection**: Determine target files from args or `--scope diff` (git diff)
2. **Smell detection**: Use `simplify` skill's review agents to identify:
   - DRY violations (duplicate code blocks)
   - Long functions (>50 lines)
   - Dead code (unused imports, unreachable branches)
   - God objects / classes doing too much
   - Naming issues (unclear variable/function names)
   - Deep nesting (>3 levels)
3. **Impact analysis**: Use `refactor-simulator` skill to predict blast radius before making changes
4. **Plan**: Present the refactoring plan with estimated risk per change
5. **Execute**: Apply changes in priority order (safest first):
   a. Remove dead code / unused imports
   b. Rename for clarity
   c. Extract functions / methods
   d. Reduce nesting (early returns)
   e. Consolidate duplicates
6. **Verify**: Run lint + typecheck + tests after each batch of changes
7. **Report**: Summary of changes made, files affected, and verification results

Use `omc-ai-slop-cleaner` for AI-generated code cleanup specifically. Use `simplify` for broader code quality review without the structured refactoring pipeline.
