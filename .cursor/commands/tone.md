---
description: "Set the emotional register and formality level for the response"
argument-hint: "<tone> <question or content>"
---

# Tone Controller

Set the emotional register, formality level, and communication energy for the response. Affects word choice, sentence structure, and overall feel without changing factual content.

## Usage

```
/tone formal Explain our platform's multi-tenant architecture to a potential enterprise customer
/tone casual What's the deal with Kubernetes pod scheduling?
/tone encouraging Review this junior developer's first PR
/tone direct Should we cancel the legacy API?
/tone empathetic Our deployment failed and the team is stressed — write a post-mortem intro
/tone humorous Explain DNS resolution
/tone academic 트랜스포머 아키텍처의 어텐션 메커니즘 원리
/tone diplomatic We need to tell the client their timeline is unrealistic
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse tone** — Extract the tone keyword from the first token of `$ARGUMENTS`
2. **Parse question** — Everything after the tone token is the question or content
3. **Calibrate parameters:**

   | Tone | Formality | Energy | Sentence Length | Contractions | Emoji |
   |------|-----------|--------|----------------|--------------|-------|
   | `formal` | High | Measured | Long, structured | Never | Never |
   | `casual` | Low | Relaxed | Short, conversational | Freely | Sparingly |
   | `encouraging` | Medium | Warm, positive | Medium | Sometimes | Optional |
   | `direct` | Medium | Sharp, efficient | Short, declarative | Sometimes | Never |
   | `empathetic` | Medium | Warm, understanding | Medium, flowing | Sometimes | Never |
   | `humorous` | Low | Playful | Varied | Freely | Sparingly |
   | `academic` | High | Neutral, precise | Long, complex | Never | Never |
   | `diplomatic` | High | Careful, balanced | Medium, nuanced | Rarely | Never |
   | `urgent` | Medium | High, action-oriented | Short, imperative | Sometimes | Never |
   | `inspirational` | Medium-High | Elevated, motivating | Varied, rhythmic | Rarely | Never |

4. **Generate response** — Answer the question with all tone parameters applied
5. **Verify tone consistency** — Re-read the response to ensure the tone doesn't drift

### Constraints

- Tone affects style, not substance — facts and recommendations remain accurate regardless of tone
- The tone must be maintained from first sentence to last — no drift
- If the requested tone is inappropriate for the content (e.g., `humorous` for a security incident), note the tension and suggest an alternative tone before proceeding
- Unknown tone keywords: interpret naturally and state the calibration chosen

### Execution

Reference `sentence-polisher` (`.cursor/skills/standalone/sentence-polisher/SKILL.md`) for tone-aware text refinement. Reference `kwp-brand-voice-brand-voice-enforcement` (`.cursor/skills/kwp/kwp-brand-voice-brand-voice-enforcement/SKILL.md`) for brand-aligned tone calibration.
