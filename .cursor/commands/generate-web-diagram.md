## Generate Web Diagram

Generate a beautiful standalone HTML diagram for any topic and open it in the browser.

### Usage

```
/generate-web-diagram <topic or subject>
```

### Workflow

1. **Load skill** — Read the visual-explainer skill and follow its 4-step workflow (Think → Structure → Style → Deliver)
2. **Read references** — Read the appropriate template and CSS patterns before generating
3. **Pick aesthetic** — Choose a distinctive aesthetic that fits the content. Vary fonts, palette, and layout style from previous diagrams
4. **Generate HTML** — Create a self-contained HTML page with dark/light theme support
5. **Deliver** — Write to `~/.agent/diagrams/` and open in browser

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for workflow, CSS patterns, templates, and quality checks.

### Examples

Architecture overview:
```
/generate-web-diagram Kubernetes pod lifecycle
```

Data flow visualization:
```
/generate-web-diagram OAuth 2.0 PKCE flow
```

Comparison table:
```
/generate-web-diagram React vs Vue vs Svelte feature comparison
```
