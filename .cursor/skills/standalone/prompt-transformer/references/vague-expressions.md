# Vague Expression Replacements

When transforming prompts, replace ambiguous language with precise equivalents.

| Vague Expression | Replacement |
|-----------------|-------------|
| "if possible" | "always" or remove the instruction entirely |
| "in principle" | "without exception" or define the exact exceptions |
| "recommended" | "mandatory" (if important) or remove (if optional) |
| "as appropriate" | specify exact criteria |
| "use your judgment" | provide explicit decision tree or criteria |
| "depending on the situation" | enumerate all situations with specific actions |
| "as needed" | define the exact trigger condition |
| "etc." | list all items explicitly |
| "try to" | "must" or remove |
| "should" (ambiguous) | "must" (mandatory) or "may" (optional) |

Additional rules:
- Replace subjective adjectives ("good", "clean", "proper") with measurable criteria
- Quantify all thresholds ("short" → "under 50 characters", "few" → "2-3")
- Ensure every conditional has an explicit else branch
