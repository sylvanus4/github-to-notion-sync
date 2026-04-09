# Pandoc Skill Autoimprove Changelog

Mutation log for `.cursor/skills/standalone/pandoc/SKILL.md`

---

## Experiment 1: Quick Reference Card (KEPT)

**Hypothesis**: Adding a Quick Reference with 5 most common conversions at the top helps the LLM agent find correct commands faster.

**Mutation**: Inserted `## Quick Reference` section with 5 bash commands (MD→DOCX, MD→PDF Korean, DOCX→MD, Batch, Lua filter chain) before `## Prerequisites`.

**Score**: 25/25 (100%) -- same as baseline but qualitative improvement noted.

**Decision**: KEPT -- Quick Reference consolidates CJK+xelatex, --extract-media, and filter chain in copy-paste-ready form, reducing cognitive load. Evaluator noted it enables faster E1/E2 derivation.

---

## Experiment 2: Inline Error Recovery Callouts (KEPT)

**Hypothesis**: Adding inline "If X fails" callouts per workflow mode strengthens E3 (Verification Step) by providing immediate recovery paths without requiring the agent to scroll to a separate Error Handling section.

**Mutation**: Inserted 4 blockquote callouts:
1. Mode 1: "If PDF fails" -- install PDF engine + CJK font
2. Mode 2: "If PDF in batch fails" -- separate PDF step with `--pdf-engine`
3. Mode 3: "If reference doc not found" -- `ls` check + regeneration
4. Mode 4: "If filter not found" -- `ls` check + inline Lua not supported note

**Score**: 25/25 (100%) -- E3 qualitatively improved.

**Decision**: KEPT -- Progressive disclosure of error recovery at point-of-use. Minor duplication with Error Handling table (~200 tokens) is acceptable for improved agent recovery behavior.

---

## Experiment 3: --wrap=none for CJK Output (KEPT)

**Hypothesis**: Pandoc's default 72-char line wrapping can break CJK text mid-word. Adding `--wrap=none` explicitly to all Korean/reverse conversion commands prevents this and strengthens E2 (Format-Specific Flags).

**Mutation**: 3 changes applied:
1. Mode 1 (line 90): Added `--wrap=none` to DOCX->MD example
2. Mode 6 (lines 188-191): Added `--wrap=none` to all 4 reverse conversion commands + updated prose to explain CJK rationale
3. Defaults file (line 213): Added `wrap: none` to Korean defaults YAML example

**Score**: 25/25 (100%) -- E2 qualitatively improved.

**Decision**: KEPT -- Eliminates a real CJK text processing bug. Previously Mode 6 only mentioned `--wrap=none` in prose but did not include it in copy-paste-ready commands. The defaults file now also includes it, ensuring Korean pipeline outputs are safe by default.

---

## Experiment 4: Per-Format Verification Table (KEPT)

**Hypothesis**: Generic verification bash snippets don't guide the agent to choose format-appropriate validation commands. A per-format validation table strengthens E3 (Verification Step) by mapping each output format to its specific check.

**Mutation**: Replaced the generic verification section (4 bash commands) with a 7-row table:

| Output | Validation Command | Pass Criteria |
|--------|-------------------|---------------|
| DOCX | `pandoc output.docx --to plain \| head -50` | Readable text |
| PDF | `pdfinfo output.pdf \| grep Pages` | Pages >= 1 |
| HTML | `pandoc output.html --to plain \| wc -w` | Word count > 0 |
| MD (reverse) | `head -20 output.md` | No binary artifacts |
| PPTX | `unzip -l output.pptx \| grep -c 'ppt/slides/slide'` | Slide count >= 1 |
| EPUB | `pandoc output.epub --to plain \| wc -w` | Word count > 0 |
| All | `test -s OUTPUT \|\| echo "ERROR: Empty"` | Non-zero size |

Added Korean mojibake check guidance in the prose below the table.

**Score**: 25/25 (100%) -- E3 qualitatively improved.

**Decision**: KEPT -- Table format enables agent to index directly to the output format being produced. PPTX slide count check (via `unzip -l`) is a new capability not present in the original. Korean mojibake awareness added.

---

## Experiment 5: Project-Specific Filenames (KEPT)

**Hypothesis**: Mode 3(Template)과 Mode 4(Filter) 예제가 `templates/corporate.docx`나 `filters/a.lua` 같은 일반적 플레이스홀더를 사용하고 있어, 에이전트가 copy-paste시 존재하지 않는 파일 경로를 생성할 수 있다. 실제 프로젝트 파일명으로 교체하면 E1(CLI Correctness)이 더 강건해진다.

**Mutation**: 3개 StrReplace 적용:

1. Mode 3: `templates/corporate.docx` -> `templates/thaki-report.docx`
2. Mode 3: `templates/corporate.pptx` -> `templates/thaki-slides.pptx`
3. Mode 4: `--lua-filter=filters/a.lua --lua-filter=filters/b.lua` -> `--lua-filter=filters/fix-korean-tables.lua --lua-filter=filters/comma-numbers.lua`

**Score**: 25/25 (100%) -- E1 qualitatively improved.

**Decision**: KEPT -- Generic placeholders (`corporate.docx`, `a.lua`, `b.lua`) eliminated. Agent can now copy Mode 3/4 examples directly without encountering file-not-found errors. Quick Reference, Mode 4 single example, and defaults YAML already used real filenames from earlier experiments, so this completes the consistency pass across all modes.

---
