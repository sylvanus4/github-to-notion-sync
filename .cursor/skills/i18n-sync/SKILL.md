---
name: i18n-sync
description: Synchronize translation keys across all locale files (en, ko, ja, zh-CN), detect missing or extra keys, generate translation drafts via LLM, and sort/deduplicate keys. Use when the user asks to check translations, sync i18n keys, add new translated strings, or audit locale files. Do NOT use for frontend component review (use frontend-expert) or general documentation writing (use technical-writer).
metadata:
  version: "1.0.0"
  category: execution
---

# i18n Sync Manager

Manages translation synchronization across 4 locales in `frontend/src/i18n/locales/`.

## When to Use

- After adding new UI strings to the frontend
- Before releases to ensure all locales are complete
- When the user asks to "add translations" or "check i18n"
- As part of the `/i18n-check` workflow (called by mission-control)

## Locale Files

| Locale | File | Role |
|--------|------|------|
| English | `frontend/src/i18n/locales/en.json` | **Source of truth** |
| Korean | `frontend/src/i18n/locales/ko.json` | Translation |
| Japanese | `frontend/src/i18n/locales/ja.json` | Translation |
| Chinese (Simplified) | `frontend/src/i18n/locales/zh-CN.json` | Translation |

English (`en.json`) is the canonical reference. All other locales must have the same key structure.

## Execution Steps

### Step 1: Load and Parse All Locale Files

Read all 4 JSON files. Parse into nested key maps.

Flatten nested keys using dot notation for comparison:

```
{ "nav": { "dashboard": "Dashboard" } }
→ "nav.dashboard" = "Dashboard"
```

### Step 2: Detect Key Mismatches

Compare each locale against `en.json`:

1. **Missing keys**: Keys in `en.json` but not in target locale
2. **Extra keys**: Keys in target locale but not in `en.json` (possibly deprecated)
3. **Empty values**: Keys present but with empty string `""`
4. **Untranslated values**: Values identical to English (possible copy-paste)

### Step 3: Generate Translation Drafts

For missing keys, generate translations using LLM knowledge:

- Context: The app is a "financial contact center agent assist platform"
- Tone: Professional, concise UI labels
- For Korean: formal polite style (합쇼체/해요체 as appropriate for UI)
- For Japanese: polite form (です/ます)
- For Chinese: simplified Chinese, professional tone

Present translations as a diff for user review before applying.

### Step 4: Sort and Deduplicate

After translations are confirmed:

1. Sort all keys alphabetically at each nesting level
2. Remove duplicate keys
3. Ensure consistent formatting (2-space indent, trailing newline)

### Step 5: Validate JSON Structure

After modifications, validate:

```bash
cd frontend && node -e "
  const fs = require('fs');
  ['en','ko','ja','zh-CN'].forEach(l => {
    try { JSON.parse(fs.readFileSync('src/i18n/locales/' + l + '.json', 'utf8')); console.log(l + ': valid'); }
    catch(e) { console.error(l + ': INVALID - ' + e.message); process.exit(1); }
  });
"
```

## Examples

### Example 1: Sync after adding new UI strings
User says: "I added new strings, sync translations"
Actions:
1. Parse all 4 locale files and flatten keys
2. Detect missing keys in ko/ja/zh-CN compared to en.json
3. Generate translation drafts and present for review
Result: i18n Sync Report with suggested translations for missing keys

### Example 2: Audit locale files
User says: "Check if all translations are complete"
Actions:
1. Compare all locales against en.json source of truth
2. Flag missing, extra, empty, and untranslated values
3. Sort and deduplicate keys
Result: Complete audit showing translation coverage per locale

## Troubleshooting

### Invalid JSON after edit
Cause: Trailing comma or missing quote in locale file
Solution: Run the JSON validation script from Step 5 to identify the exact error

### Keys out of alphabetical order
Cause: Manual edits without sorting
Solution: Run Step 4 (sort and deduplicate) to normalize all locale files

## Output Format

```
i18n Sync Report
================
Date: [YYYY-MM-DD]
Source: en.json ([N] total keys)

Locale     Total   Missing  Extra   Empty   Untranslated
────────── ─────── ──────── ─────── ─────── ────────────
ko.json    [N]     [N]      [N]     [N]     [N]
ja.json    [N]     [N]      [N]     [N]     [N]
zh-CN.json [N]     [N]      [N]     [N]     [N]

Missing Keys (require translation):
  ko.json:
    - nav.systemHealth → Suggested: "시스템 상태"
    - quality.metrics.avgScore → Suggested: "평균 점수"

  ja.json:
    - nav.systemHealth → Suggested: "システム状態"
    ...

Extra Keys (possibly deprecated):
  ko.json:
    - old.removedFeature

Actions:
  [N] translations generated (pending review)
  [N] extra keys flagged for removal
  All files JSON-valid: Yes/No
```

## Integration with Other Skills

- **mission-control**: Called during `/i18n-check` workflow
- **frontend-expert**: Works with frontend architecture; translations are part of the component layer
- **domain-commit**: After applying translations, commit as `[enhance] Sync i18n translations`
- **pr-review-captain**: Include i18n sync status in PR descriptions
