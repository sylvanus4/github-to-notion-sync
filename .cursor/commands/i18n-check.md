## i18n Check

Orchestrated workflow to verify translation completeness across all locales, generate missing translations, and commit changes.

### Usage

```
/i18n-check
```

### Workflow

1. Read the mission-control skill at `.cursor/skills/mission-control/SKILL.md`
2. Follow **WF-6: i18n Check** defined there
3. Execute sequentially:

**Step 1: Scan**
- **i18n-sync** (`.cursor/skills/i18n-sync/SKILL.md`): Load all locale files from `frontend/src/i18n/locales/`:
  - `en.json` (source of truth)
  - `ko.json` (Korean)
  - `ja.json` (Japanese)
  - `zh-CN.json` (Chinese Simplified)
- Detect missing keys, extra keys, empty values, and untranslated values in each locale

**Step 2: Generate Translations**
- For missing keys, generate translation drafts using LLM knowledge:
  - Context: Financial contact center agent assist platform
  - Korean: formal polite style
  - Japanese: polite form (です/ます)
  - Chinese: simplified, professional tone

**Step 3: User Review**
- Present the generated translations for user review
- Allow the user to approve, modify, or reject each translation
- Apply only confirmed translations

**Step 4: Validate and Commit**
- Sort all keys alphabetically at each nesting level
- Validate JSON structure of all locale files
- **domain-commit** (`.cursor/skills/domain-commit/SKILL.md`): Commit as `[enhance] Sync i18n translations for ko/ja/zh-CN`

### Output

```
i18n Sync Report
================
Source: en.json ([N] total keys)

Locale     Coverage  Missing  Extra  Empty
────────── ───────── ──────── ────── ─────
ko.json    [X]%      [N]      [N]    [N]
ja.json    [X]%      [N]      [N]    [N]
zh-CN.json [X]%      [N]      [N]    [N]

Translations generated: [N]
Translations confirmed: [N]
Files updated: [list]
```
