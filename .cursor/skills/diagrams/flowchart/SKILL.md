---
name: flowchart
description: Create flowcharts and decision trees using Mermaid syntax. Supports 4 directions (TB, BT, LR, RL), 8 node shapes, subgraph nesting, and conditional branching with styled edges. Best for visualizing decision logic, process flows, algorithms, and branching paths. Use when the user asks to "create flowchart", "draw decision tree", "visualize process", "diagram this flow", "algorithm diagram", "branching logic", "decision flow", "플로우차트", "결정 트리", "프로세스 흐름", "분기 로직", or needs a visual representation of sequential steps with conditions. Do NOT use for business process workflows with BPMN notation (use workflow-diagram skill). Do NOT use for state machine transitions (use state-diagram skill). Do NOT use for system architecture layers (use architecture-diagram skill). Do NOT use for data visualization (use infographic skill).
---

# Flowchart Generator

**Quick Start:** Choose direction (TD/LR) -> Define nodes with shapes -> Connect with arrows -> Add subgraphs for grouping.

## Critical Rules

### Rule 1: Always Use `flowchart` Over `graph`
Prefer `flowchart TD` over `graph TD`. The `flowchart` keyword supports newer Mermaid features like advanced arrow types.

### Rule 2: Unique Node IDs
Every node must have a unique ID within the entire diagram. Reusing the same ID changes its label globally.

```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action A]
    B -->|No| D[Action B]
```

### Rule 3: Avoid List Conflicts
If embedding Mermaid in Markdown, avoid ` - ` (dash-space) at the start of lines inside the diagram code block. This conflicts with Markdown list parsing.

### Rule 4: Special Characters
Wrap node labels containing special characters (`()`, `{}`, `[]`, `"`) in double quotes:
```
A["Node with (parens) and {braces}"]
```

### Rule 5: Subgraph Naming
When using subgraphs, always provide a display label. Do NOT use reserved keywords as subgraph IDs.

```
subgraph SG1 ["Processing Stage"]
    P1[Step 1] --> P2[Step 2]
end
```

## Directions

| Direction | Code | Best For |
|---|---|---|
| Top to Bottom | `flowchart TD` or `flowchart TB` | General processes, decision trees |
| Left to Right | `flowchart LR` | Pipelines, horizontal flows |
| Bottom to Top | `flowchart BT` | Build-up diagrams |
| Right to Left | `flowchart RL` | Reverse flows |

## Node Shapes

| Shape | Syntax | Use For |
|---|---|---|
| Rectangle | `A[Text]` | Process steps |
| Rounded | `A(Text)` | Start/End terminals |
| Stadium | `A([Text])` | Alternate terminals |
| Diamond | `A{Text}` | Decisions / conditions |
| Hexagon | `A{{Text}}` | Preparation steps |
| Parallelogram | `A[/Text/]` | Input/Output |
| Trapezoid | `A[/Text\]` | Manual operations |
| Circle | `A((Text))` | Connectors / junctions |

## Arrow Types

| Arrow | Syntax | Meaning |
|---|---|---|
| Solid | `-->` | Normal flow |
| Dotted | `-.->` | Optional / async |
| Thick | `==>` | Primary / critical path |
| Labeled | `-->|label|` | Conditional edge |

## Template: Decision Tree

```mermaid
flowchart TD
    START([Start]) --> INPUT[/Receive Request/]
    INPUT --> VALIDATE{Valid Input?}
    VALIDATE -->|Yes| AUTH{Authorized?}
    VALIDATE -->|No| REJECT([Return Error])
    AUTH -->|Yes| PROCESS[Process Request]
    AUTH -->|No| DENY([Access Denied])
    PROCESS --> RESULT{Success?}
    RESULT -->|Yes| RESPOND([Return Response])
    RESULT -->|No| RETRY{Retry Count < 3?}
    RETRY -->|Yes| PROCESS
    RETRY -->|No| FAIL([Return Failure])
```

## Template: Pipeline with Subgraphs

```mermaid
flowchart LR
    subgraph INPUT ["Input Stage"]
        A[/Raw Data/] --> B[Validate]
    end
    subgraph PROCESS ["Processing"]
        C[Transform] --> D[Enrich]
        D --> E{Quality Check}
    end
    subgraph OUTPUT ["Output Stage"]
        F[Format] --> G([Store])
    end
    B --> C
    E -->|Pass| F
    E -->|Fail| H[Log Error]
    H -.-> C
```

## Template: Error Handling Flow

```mermaid
flowchart TD
    A([API Request]) --> B{Rate Limited?}
    B -->|No| C{Auth Valid?}
    B -->|Yes| D([429 Too Many Requests])
    C -->|Yes| E[Route to Handler]
    C -->|No| F([401 Unauthorized])
    E --> G{Handler Found?}
    G -->|Yes| H[Execute Handler]
    G -->|No| I([404 Not Found])
    H --> J{Error?}
    J -->|No| K([200 OK])
    J -->|Yes| L{Retriable?}
    L -->|Yes| M[Retry with Backoff]
    M --> H
    L -->|No| N([500 Internal Error])
```

## Styling

### Node Classes
```mermaid
flowchart TD
    A[Normal]:::default --> B[Success]:::success
    B --> C[Warning]:::warning
    C --> D[Error]:::danger

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef success fill:#d4edda,stroke:#28a745,stroke-width:2px
    classDef warning fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    classDef danger fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

### Link Styling
```
linkStyle 0 stroke:#28a745,stroke-width:2px
linkStyle 1 stroke:#ffc107,stroke-width:2px
```

## Best Practices

1. **Direction matters** -- use TD for decision trees, LR for pipelines
2. **Limit branching** -- keep max 3-4 branches per decision node for readability
3. **Group related steps** -- use subgraphs to cluster logical stages
4. **Label all edges** -- especially on decision branches (Yes/No, Pass/Fail)
5. **Consistent shapes** -- decisions are always diamonds, I/O always parallelograms
6. **Output format** -- always output inside ` ```mermaid ` fenced code blocks
