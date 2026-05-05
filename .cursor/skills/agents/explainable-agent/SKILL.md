# Explainable Agent

Orchestrate explanation generation by capturing reasoning traces, decomposing decisions into understandable components, and producing audience-adaptive visual explanations. Transforms complex agent outputs into transparent, verifiable narratives.

## When to Use

Use when the user asks to "explain this decision", "make it explainable", "show reasoning", "explain visually", "decision decomposition", "설명해줘", "시각적으로 설명", "의사결정 분해", "explainable-agent", or needs transparent explanations of agent reasoning, system behavior, or complex analysis results.

Do NOT use for code documentation (use technical-writer). Do NOT use for teaching/tutoring (use education-intelligence-agent). Do NOT use for slide deck creation (use presentation-strategist).

## Default Skills

| Skill | Role in This Agent | Invocation |
|-------|-------------------|------------|
| visual-explainer | Self-contained HTML pages with Mermaid diagrams and evidence sections | Visual explanation generation |
| md-to-visual-explainer | Transform markdown docs into interactive visual pages with ELI5 | Document visualization |
| architecture-diagram | Dark-themed SVG architecture diagrams with 12 layouts | System architecture explanation |
| infographic | KPI cards, timelines, comparisons, SWOT, funnels, org trees | Data visualization |
| tech-doc-translator | Translate technical docs for non-technical audiences | Audience adaptation |
| flowchart | Decision trees and process flows with Mermaid syntax | Logic flow visualization |
| long-form-compressor | Condense complex explanations to appropriate length | Compression for audience |

## MCP Tools

None (pure explanation agent).

## Workflow

```mermaid
flowchart TD
    A[Explain Request] --> B{What to Explain?}
    B -->|Decision/reasoning| C[Capture reasoning trace]
    B -->|System/architecture| D[architecture-diagram]
    B -->|Document/report| E[md-to-visual-explainer]
    B -->|Data/metrics| F[infographic]
    C --> G{Audience?}
    D --> G
    E --> G
    F --> G
    G -->|Technical| H[visual-explainer: detailed]
    G -->|Non-technical| I[tech-doc-translator + ELI5]
    G -->|Executive| J[long-form-compressor: summary]
    H --> K[Interactive Explanation]
    I --> K
    J --> K
```

## Modes

- **trace**: Capture and visualize reasoning chain
- **visual**: Generate interactive HTML explanation pages
- **adapt**: Translate for specific audience level
- **decompose**: Break complex decisions into understandable steps

## Safety Gates

- Every claim in explanation traceable to source evidence
- ELI5 mode must not oversimplify to the point of inaccuracy
- Uncertainty explicitly marked in explanations (not hidden)
- Audience level validated: no jargon for non-technical, no condescension for experts
