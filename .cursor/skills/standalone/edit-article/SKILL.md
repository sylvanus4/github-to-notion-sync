---
name: edit-article
description: Deep-edit articles, blog posts, and long-form content by restructuring sections, cutting filler, sharpening arguments, and improving flow. Use when the user asks to "edit this article", "improve my draft", "tighten this post", "restructure this piece", "cut the filler", "글 다듬기", "글 편집", "글 구조 개선", "글 줄이기", "기사 편집", or has a draft that reads poorly. Do NOT use for writing from scratch (use content-researcher), grammar-only fixes (use sentence-polisher), or brand voice enforcement (use kwp-brand-voice-brand-voice-enforcement).
---

# Edit Article

Deep-edit articles, blog posts, docs, and long-form content by restructuring arguments, cutting filler, sharpening section focus, and improving flow — going far beyond grammar or spelling fixes.

## When to Use

- A draft exists but reads poorly, rambles, or lacks clear structure
- Sections feel out of order or repetitive
- The argument is buried under filler prose
- Tone is inconsistent across sections
- The piece needs to be cut by 20-50% without losing substance
- Preparing content for publication or external review

## When NOT to Use

- Writing content from scratch (use `content-researcher` or `kwp-marketing-content-creation`)
- Simple grammar/spelling check only (use `sentence-polisher`)
- Brand voice enforcement (use `kwp-brand-voice-brand-voice-enforcement`)
- Prompt or skill text refinement (use `prompt-transformer`)
- Full document rewriting that changes the author's thesis (rewrite manually)

## Workflow

### Phase 1: Diagnostic Read

1. Read the full article without making changes
2. Produce a diagnostic summary:
   - **Thesis**: What is the article's core argument or point? (1 sentence)
   - **Structure score** (1-5): How logically are sections ordered?
   - **Density score** (1-5): How much filler vs substance?
   - **Clarity score** (1-5): How easily can a target reader follow the argument?
   - **Tone consistency** (1-5): Does voice stay consistent throughout?
   - **Top 3 problems**: Ranked by impact on readability

### Phase 2: Structural Edit

1. Propose a revised outline with section reordering if needed
2. Identify sections to merge, split, or remove entirely
3. Flag paragraphs that repeat points already made elsewhere
4. Mark transitions that are weak or missing
5. Present the proposed structure for approval before proceeding

### Phase 3: Prose Edit

For each section, apply these passes in order:

1. **Cut pass**: Remove filler words, redundant qualifiers, throat-clearing sentences, and paragraphs that don't advance the argument
2. **Sharpen pass**: Make each paragraph's point land in the first or second sentence; push evidence and examples after the claim
3. **Flow pass**: Ensure transitions between paragraphs are logical; each paragraph should connect to the next
4. **Voice pass**: Normalize tone — eliminate jarring shifts between formal/casual, passive/active

### Phase 4: Final Polish

1. Verify the thesis is clear within the first 2 paragraphs
2. Ensure the conclusion echoes the thesis without repeating it verbatim
3. Check that every section heading accurately describes its content
4. Verify no orphaned references (mentioning something "above" or "below" that was moved)
5. Produce a change summary: sections reordered, paragraphs cut, word count before/after

## Constraints

- Never invent new arguments or claims not present in the original
- Preserve the author's voice — improve it, don't replace it
- Flag factual claims that seem unsupported but do not remove them without author approval
- If the article is under 500 words, skip Phase 2 (structural edit) and focus on prose
- Always show before/after word count
- Output the edited article as a complete document, not a diff
- Do NOT add new sections, examples, or content the author didn't write — only restructure and tighten what exists

## Gotchas

1. **Over-editing kills voice.** The goal is to sharpen the author's style, not to produce "AI-polished" prose. If the output reads like a different person wrote it, you went too far.
2. **Cutting != improving.** Removing a section that feels "weak" may delete a key supporting argument. Always check that cutting a paragraph doesn't create a logical gap.
3. **Structure changes can flip meaning.** Moving a caveat from before a claim to after it changes the argument. Verify logical flow after every structural change.

## Verification

After completing all phases:
1. Confirm word count delta is within the user's target range (default: 15-30% reduction)
2. Read the edited version end-to-end — each section should have exactly one clear point
3. Check that no factual claims were removed or reworded in a way that changes their meaning
4. Verify the opening paragraph sets up the article's thesis within the first 3 sentences

## Anti-Example — What a Bad Edit Looks Like

```markdown
# BAD: Rewrites the author's voice into generic AI prose
- Original: "I've been burned by Redis three times. Here's what I learned."
- Bad edit: "Redis presents several operational challenges. This article examines key lessons."
→ The personality, specificity, and hook are all destroyed.

# BAD: Cuts a section because it "doesn't flow" without checking logical dependency
- Original has: Problem → Context → Solution → Caveat
- Bad edit removes "Context" section → Reader can't understand why the solution matters.
```

## Output Format

```markdown
## Edit Summary

| Metric | Before | After |
|--------|--------|-------|
| Word count | X | Y |
| Sections | N | M |
| Structure score | X/5 | Y/5 |
| Density score | X/5 | Y/5 |

### Key Changes
1. ...
2. ...
3. ...

---

## [Edited Article]

(full edited article here)
```
