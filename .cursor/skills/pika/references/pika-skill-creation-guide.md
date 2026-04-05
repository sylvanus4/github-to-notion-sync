# Pika Skill Creation Guide

How to create new skills that extend the Pika video generation capabilities within this project.

## Architecture Overview

```
.cursor/skills/pika/
├── references/
│   └── pika-skill-creation-guide.md    ← this file
├── pikastream-video-meeting/           ← adapted from upstream Pika SDK
│   ├── SKILL.md
│   ├── scripts/
│   ├── requirements.txt
│   ├── references/
│   └── assets/
├── pika-text-to-video/                 ← custom skill wrapping fal.ai
│   ├── SKILL.md
│   ├── scripts/
│   ├── requirements.txt
│   └── references/
└── pika-video-pipeline/                ← orchestrator (no scripts)
    └── SKILL.md
```

### Skill Types

| Type | Has Scripts | Example | When to use |
|------|-----------|---------|-------------|
| **Adapted** | Yes (from upstream) | `pikastream-video-meeting` | Porting a skill from the Pika Skills SDK repo |
| **Custom** | Yes (new code) | `pika-text-to-video` | Wrapping a Pika/fal.ai API not covered upstream |
| **Orchestrator** | No | `pika-video-pipeline` | Chaining existing skills into a workflow |

## Creating a New Custom Pika Skill

### Step 1 — Choose the API surface

Pika capabilities accessible through fal.ai:

| Endpoint | Use Case |
|----------|----------|
| `fal-ai/pika/v2.2/text-to-video` | Text prompt → video |
| `fal-ai/pika/v2.2/image-to-video` | Image + prompt → animated video |
| `fal-ai/pika/v2.2/pikascenes` | Multi-image composition |
| `fal-ai/pika/v2.2/pikaframes` | Keyframe interpolation (2-5 images) |
| `fal-ai/pika/v2.2/pikaffects` | 16 special effects on an image |
| `fal-ai/pika/v2.2/pikaswaps` | Replace elements in existing video |
| `fal-ai/pika/v2.2/pikadditions` | Add elements to existing video |

PikaStreaming (via Pika Developer API directly, not fal.ai):

| Endpoint | Use Case |
|----------|----------|
| PikaStreaming API | Real-time video meeting avatar |

### Step 2 — Directory structure

```bash
mkdir -p .cursor/skills/pika/{skill-name}/scripts
mkdir -p .cursor/skills/pika/{skill-name}/references
```

### Step 3 — Write the Python script

Follow these conventions established by the existing Pika skills:

```python
#!/usr/bin/env python3
"""One-line description.

Exit codes:
  0  Success
  1  General error
  2  Invalid arguments
  3  API / HTTP error
  4  Missing environment variable
"""

from __future__ import annotations

import argparse
import json
import os
import sys

def main() -> int:
    # 1. Check environment variables
    if not os.environ.get("FAL_KEY"):
        print(json.dumps({"error": "FAL_KEY not set"}), file=sys.stderr)
        return 4

    # 2. Parse arguments
    parser = argparse.ArgumentParser(description="...")
    # ... add arguments ...
    args = parser.parse_args()

    # 3. Execute API call
    # ... implementation ...

    # 4. Output JSON result to stdout
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

**Rules**:
- Print structured JSON to stdout on success
- Print error JSON to stderr on failure
- Use consistent exit codes (0-4 as documented)
- Use `fal_client` for fal.ai API calls, `requests` for Pika direct API
- Upload local files via `fal_client.upload_file()` before passing to API
- Accept both local paths and URLs for image/video inputs

### Step 4 — Write requirements.txt

```
fal-client>=0.5.0    # for fal.ai API skills
requests>=2.32.5     # for direct Pika API skills
```

Only include what the specific skill needs.

### Step 5 — Write SKILL.md

Follow the project SKILL.md conventions:

```yaml
---
name: pika-{skill-name}
description: |
  {One-paragraph description of what the skill does.}
  Use when the user asks to "{trigger 1}", "{trigger 2}", "{Korean trigger 1}",
  "{Korean trigger 2}", or {broader intent description}.
  Do NOT use for {anti-pattern 1} (use {alternative skill}).
  Do NOT use for {anti-pattern 2} (use {alternative skill}).
metadata:
  author: thakicloud
  version: 0.1.0
  category: pika
  license: Apache-2.0
  cost: ~${estimate}/video
---

# {Skill Title}

{Brief intro — 1 sentence.}

Script directory: `SKILL_DIR=.cursor/skills/pika/{skill-name}`

## Prerequisites

- Python 3.10+
- `FAL_KEY` or `PIKA_DEV_KEY` environment variable

## First-Time Setup

\```bash
pip install -r $SKILL_DIR/requirements.txt
\```

## Workflow

### Step 1 — {Gather inputs}
### Step 2 — {Execute}
### Step 3 — {Present results}

## Error Handling

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | ... |
| ... | ... | ... |

## Cross-Skill References

- For {related task}: use `{skill-name}`
```

**SKILL.md checklist**:
- [ ] YAML frontmatter with name, description, metadata
- [ ] Description includes English AND Korean trigger phrases
- [ ] Description includes "Do NOT use for" boundaries with alternatives
- [ ] `metadata.category` is `pika`
- [ ] Prerequisites section with env vars
- [ ] Workflow section with numbered steps
- [ ] Error handling table
- [ ] Cross-skill references section

### Step 6 — Validate

Run the project validation:

```bash
# Check SKILL.md structure
head -30 .cursor/skills/pika/{skill-name}/SKILL.md

# Verify script runs (dry check)
python .cursor/skills/pika/{skill-name}/scripts/{script}.py --help

# Check for import errors
python -c "import fal_client" 2>&1 || echo "Install: pip install fal-client"
```

## Adapting an Upstream Pika SDK Skill

When a new skill appears in https://github.com/Pika-Labs/Pika-Skills:

1. **Clone or fetch** the upstream repo
2. **Copy** `scripts/`, `requirements.txt`, and `assets/` to `.cursor/skills/pika/{skill-name}/`
3. **Rewrite** `SKILL.md` to match project conventions (don't copy verbatim)
4. **Create** `references/upstream-readme.md` documenting:
   - Source URL
   - License (Apache-2.0)
   - Copyright holder
   - Date cloned
   - Changes from upstream
5. **Update** `.env.example` if new environment variables are needed

## Creating an Orchestrator Skill

Orchestrator skills have no scripts — they compose existing skills.

1. Create `SKILL.md` only (no `scripts/` directory needed)
2. Define pipeline phases referencing existing skills
3. Document checkpoint/approval points between phases
4. Define output structure (files, manifests)
5. Include error recovery for each phase

## Naming Convention

| Pattern | Example | Use |
|---------|---------|-----|
| `pika-{mode}` | `pika-text-to-video` | Single API mode wrapper |
| `pika-{domain}-{action}` | `pika-marketing-reel` | Domain-specific video recipe |
| `pikastream-{purpose}` | `pikastream-video-meeting` | PikaStreaming real-time skills |
| `pika-{mode}-pipeline` | `pika-video-pipeline` | Multi-step orchestrators |

## Environment Variables

| Variable | Required By | Source |
|----------|------------|--------|
| `FAL_KEY` | fal.ai API skills | https://fal.ai/dashboard/keys |
| `PIKA_DEV_KEY` | PikaStreaming skills | https://www.pika.me/dev/ |

## Cost Awareness

Always include cost estimates in SKILL.md metadata:

| Operation | Approximate Cost |
|-----------|-----------------|
| text-to-video (5s, 720p) | ~$0.40 |
| image-to-video (5s, 720p) | ~$0.40 |
| PikaStreaming meeting | $0.275/min |
| pikaffects | ~$0.40 |

Warn users before batch operations: `This will generate {N} videos, estimated cost ~${N * 0.40}.`

## Existing Cross-Skill Integration Points

Pika skills compose well with these project skills:

| Phase | Skill | Purpose |
|-------|-------|---------|
| Pre-production | `video-script-generator` | Write scripts |
| Pre-production | `presentation-strategist` | Plan narrative |
| Pre-production | `hook-generator` | Opening hooks |
| Generation | `pika-text-to-video` | Core generation |
| Generation | `pikastream-video-meeting` | Live meetings |
| Post-production | `video-editing-planner` | Edit plans |
| Post-production | `video-compress` | Compression |
| Post-production | `caption-subtitle-formatter` | Subtitles |
| Distribution | `content-repurposing-engine` | Multi-platform |
| Distribution | `gws-drive` | Upload to Drive |
| Distribution | `md-to-notion` | Document results |

## Future Skill Ideas

Potential Pika skills not yet implemented:

1. **pika-marketing-reel** — Generate product demo reels from screenshots + copy
2. **pika-avatar-factory** — Batch avatar generation for team members
3. **pika-thumbnail-animator** — Animate YouTube thumbnails for social posts
4. **pika-stock-visualizer** — Generate market trend visualization videos from chart data
5. **pika-presentation-to-video** — Convert PPTX slides to animated video explainers
6. **pika-social-story** — Platform-optimized (9:16) story/reel generation
7. **pika-batch-effects** — Apply pikaffects to multiple images in batch
