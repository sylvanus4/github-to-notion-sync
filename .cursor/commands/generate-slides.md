## Generate Slides

Generate a stunning magazine-quality slide deck as a self-contained HTML page.

### Usage

```
/generate-slides <topic or content>
```

### Workflow

1. **Read references** — Read `./templates/slide-deck.html`, `./references/slide-patterns.md`, `./references/css-patterns.md`, and `./references/libraries.md`
2. **Pick preset** — Choose from 4 slide presets (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean) or riff on existing aesthetic directions
3. **Plan narrative** — Compose a story arc (impact → context → deep dive → resolution). Plan slide sequence and assign compositions (centered, left-heavy, split, full-bleed) before writing HTML
4. **Visual richness** — Use SVG decorative accents, per-slide background gradients, inline sparklines, and small Mermaid diagrams. Visual-first, text-second
5. **Compositional variety** — Consecutive slides must vary spatial approach. No three centered slides in a row
6. **Content completeness** — Every section and data point from the source must appear. Add more slides rather than cutting content
7. **Deliver** — Write to `~/.agent/diagrams/` and open in browser

Slide output is always opt-in. Only generate slides when this command is invoked or the user explicitly asks for a slide deck.

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for workflow, CSS patterns, templates, and quality checks.

### Examples

Topic presentation:
```
/generate-slides Microservices Architecture Patterns
```

Technical deep-dive:
```
/generate-slides Our API Gateway Design Decisions
```

Also works as a flag on other commands:
```
/diff-review --slides
/project-recap --slides 3m
```
