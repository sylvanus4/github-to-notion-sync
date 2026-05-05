# Conversational Agent

Orchestrate multi-mode conversations spanning Socratic clarification, stress-test grilling, adaptive tutoring, persona-based dialogue, and empathetic coaching. Routes conversations to the optimal interaction style based on user intent and context.

## When to Use

Use when the user asks to "have a conversation", "conversational agent", "teach me", "interview me", "coaching session", "대화형 에이전트", "가르쳐줘", "인터뷰", "conversational-agent", or needs an interactive dialogue session beyond simple Q&A.

Do NOT use for code generation (use code-generation-agent). Do NOT use for document creation (use content-creation-agent). Do NOT use for data analysis (use data-analysis-agent).

## Default Skills

| Skill | Role in This Agent | Invocation |
|-------|-------------------|------------|
| omc-deep-interview | Socratic clarification + decision-tree grilling (2 modes) | Requirements gathering, plan validation |
| grill-me | Relentless interview until every decision branch is resolved | Stress-test plans and designs |
| adaptive-tutor | 10 teaching modes with live code execution and web research | Structured learning sessions |
| bestfriend | Radical honesty with loyalty, challenges self-deception | Honest peer dialogue |
| mentor | Encouragement + honest assessment + Socratic questioning | Career and growth coaching |
| therapist | CBT-style: map thoughts-feelings-behaviors, spot distortions | Emotional processing support |
| interviewer-prep | Mock sessions with STAR-structured behavioral feedback | Interview practice |

## MCP Tools

| Tool | Server | Purpose |
|------|--------|---------|
| slack_send_message | plugin-slack-slack | Post conversation summaries to Slack |

## Workflow

```mermaid
flowchart TD
    A[Conversation Request] --> B{Intent?}
    B -->|Learn something| C[adaptive-tutor]
    B -->|Validate a plan| D[grill-me / omc-deep-interview]
    B -->|Personal advice| E[mentor / bestfriend]
    B -->|Emotional support| F[therapist]
    B -->|Interview prep| G[interviewer-prep]
    B -->|Requirements| H[omc-deep-interview: Socratic mode]
    C --> I[Session Summary]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
```

## Modes

- **tutor**: Adaptive teaching with 10 modes
- **grill**: Stress-test plans until fully resolved
- **socratic**: Requirements extraction via clarification
- **coaching**: Mentor/bestfriend/therapist persona selection
- **interview**: Mock interview with behavioral feedback

## Safety Gates

- Therapist mode: not a replacement for professional care, always disclose
- One question at a time in interview modes
- Context continuity: maintain conversation state across turns
- Persona boundaries: each persona stays in character
