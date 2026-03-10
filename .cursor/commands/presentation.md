## Presentation Strategy

Design the complete content strategy, narrative, and scripts for a presentation before building any slides.

### Usage

```
/presentation <topic>
```

### Options

- `--audience <type>`: Target audience (e.g., "Series B investors", "engineering team", "board of directors")
- `--slides <count>`: Target slide count (default: 10-15)
- `--module <1-10|all>`: Run a specific module or the full pipeline (default: all)
- `--data <paste>`: Raw data for the Data Storytelling module
- `--objections <list>`: Anticipated objections for the Objection-Proof module
- `--outline <paste>`: Existing outline for the Stress Test module
- `--render <pptx|html>`: After strategy is complete, chain to a rendering skill

### Modules

| # | Name | Phase | What It Produces |
|---|------|-------|------------------|
| 1 | Blueprint | Strategy | Objective, audience profile, key message, emotional arc, slide flow |
| 2 | Opening Hook | Content | 3 attention-capturing opening options |
| 3 | Slide Script | Content | Per-slide headlines, bullets, speaker script, transitions |
| 4 | Data Storytelling | Content | Data narrative with visual recommendations |
| 5 | Objection-Proof | Defense | Preemptive slides for anticipated resistance |
| 6 | Executive Summary | Content | Single-slide distillation under 60 words |
| 7 | Closing CTA | Content | Final slide and closing script with call to action |
| 8 | Q&A Prep | Defense | 10 hardest questions with answers and bridging phrases |
| 9 | Visual Direction | Strategy | Color palette, typography, layout rules, design principles |
| 10 | Stress Test | Quality | Adversarial review and rewrite of weakest sections |

### Execution

Read and follow the `presentation-strategist` skill (`.cursor/skills/presentation-strategist/SKILL.md`).

### Examples

Full pipeline for an investor pitch:
```
/presentation "AI Customer Service Platform" --audience "Series B investors" --slides 12
```

Single module — just opening hooks:
```
/presentation "Quarterly Business Review" --audience "board of directors" --module 2
```

Data storytelling with raw metrics:
```
/presentation "Sales Performance" --audience "executive team" --module 4 --data "Q1: $2.1M, Q2: $3.4M, Q3: $5.1M, Q4: $7.8M"
```

Strategy then render to PowerPoint:
```
/presentation "Product Roadmap 2026" --audience "engineering all-hands" --render pptx
```

Stress test an existing outline:
```
/presentation "Market Expansion" --module 10 --outline "1. Current Markets 2. Opportunity 3. Go-to-Market 4. Investment Required"
```
