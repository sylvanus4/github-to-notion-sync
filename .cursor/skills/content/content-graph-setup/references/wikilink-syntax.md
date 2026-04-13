# Wikilink Syntax Reference

Wikilinks connect nodes within the Content Skill Graph, enabling the AI agent to navigate the full knowledge graph from any entry point.

## Syntax

```
[[relative/path/to/file]]
```

## Rules

1. **Relative paths only** — all paths are relative to the `content-skill-graph/` root
2. **Omit the `.md` extension** — `[[voice/brand-voice]]` not `[[voice/brand-voice.md]]`
3. **Case-sensitive** — `[[Voice/Brand-Voice]]` ≠ `[[voice/brand-voice]]`
4. **No leading slash** — `[[voice/brand-voice]]` not `[[/voice/brand-voice]]`

## Examples

### In `index.md`

```markdown
## Audience
See [[audience/segments]] for target profiles and [[audience/pain-points]] for
frustrations mapped to each segment.

## Voice
Brand voice DNA is defined in [[voice/brand-voice]] with platform-specific
tone shifts in [[voice/platform-tone]].
```

### In `platforms/x.md`

```markdown
## Tone
Follow the base voice from [[voice/brand-voice]] with the X-specific shifts
in [[voice/platform-tone]].

## Hooks
Use formulas from [[engine/hooks]] — prioritize curiosity and data hooks for X.

## Repurposing
This platform appears in the repurpose chain at [[engine/repurpose]].
```

### In `engine/repurpose.md`

```markdown
## Chain Order
1. Long-form seed (from source content)
2. [[platforms/linkedin]] — professional narrative
3. [[platforms/x]] — compressed thread
4. [[platforms/instagram]] — visual carousel
5. [[platforms/threads]] — conversational take
6. [[platforms/tiktok]] — script with hook
7. [[platforms/youtube]] — description + timestamps
8. [[platforms/facebook]] — community share
9. [[platforms/newsletter]] — curated digest
```

## Bidirectional Links

When node A links to node B, node B should also link back to node A. This ensures the AI can navigate in both directions.

```markdown
<!-- In audience/segments.md -->
Related: [[audience/pain-points]]

<!-- In audience/pain-points.md -->
Related: [[audience/segments]]
```

## Validation

The `content-graph-audit` skill checks:

- All `[[wikilinks]]` resolve to existing files
- No orphan nodes (files with zero inbound links)
- Bidirectional link coverage
- No circular-only clusters disconnected from `index.md`
