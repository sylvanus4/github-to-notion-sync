# Voice Constants & Tone Flex Matrix

Adapted from the "voice constant, tone flexes" model for cloud service UIs.
Voice is the product's personality — it never changes. Tone adapts to the UI
context while staying within the voice.

---

## Voice Constants: "We Are / We Are Not"

| We Are | We Are Not |
|--------|------------|
| Clear and direct | Vague or bureaucratic |
| Professional but human | Robotic or overly corporate |
| Technically precise | Jargon-heavy without explanation |
| Calm and confident | Alarmist or dismissive |
| Action-oriented | Passive or abstract |
| Honest about limitations | Overpromising or hedging |
| Respectful of the user's time | Verbose or padded |
| Helpful without being patronizing | Condescending or assuming ignorance |

### How to Use the Table

- Every piece of UI copy must align with the "We Are" column.
- If copy drifts toward a "We Are Not" attribute, revise.
- When unsure, read it aloud: does it sound like the left column or the right?

---

## Voice Attributes (Always Apply)

| Attribute | Definition | In Practice |
|-----------|-----------|-------------|
| **Clarity** | Say what you mean, simply | Short sentences. Active voice. No hedge words ("might", "possibly"). |
| **Precision** | Be specific, not generic | Use numbers, names, concrete values. Avoid "various", "many", "some". |
| **Calm authority** | State things confidently without arrogance | "This action is irreversible" not "WARNING!!! BE VERY CAREFUL!!!" |
| **Helpfulness** | Guide toward resolution | Every error includes a next step. Every empty state includes a CTA. |
| **Economy** | No unnecessary words | Cut "please note that", "it should be noted", "in order to". |

---

## Tone Flex Dimensions

Tone adapts across three dimensions. Each UI copy category maps to a specific
combination.

### Dimension 1: Formality

| Level | Characteristics | When |
|-------|----------------|------|
| **Formal** | Complete sentences, no contractions, structured | Confirmations for destructive actions, legal, compliance |
| **Neutral** | Contractions OK, direct, professional | Most UI text: errors, descriptions, tooltips, status |
| **Friendly** | Warmer phrasing, encouraging, conversational | Empty states, onboarding, success celebrations (still no emoji) |

### Dimension 2: Urgency

| Level | Characteristics | When |
|-------|----------------|------|
| **High** | Immediate, consequence-focused, clear action | Destructive confirmations, critical errors, security alerts |
| **Medium** | Informative, some time-sensitivity | Validation errors, status updates, warnings |
| **Low** | Relaxed, no time pressure | Tooltips, descriptions, empty states, onboarding |

### Dimension 3: Technical Depth

| Level | Characteristics | When |
|-------|----------------|------|
| **High** | Technical terms used freely, assumes expertise | Developer docs, API error codes, CLI output |
| **Medium** | Technical concepts explained briefly | Settings tooltips, feature descriptions |
| **Low** | Plain language, benefit-focused | Error messages for end-users, onboarding, empty states |

---

## Tone-by-Category Matrix

The primary reference for setting tone during generation and review.

| Category | Formality | Urgency | Technical Depth | Voice Notes |
|----------|-----------|---------|-----------------|-------------|
| **Label** | Neutral–Formal | Low | Low | Shortest possible. Verb-first for actions. |
| **Tooltip** | Neutral | Low | Medium | Adds context the label can't. Never repeats the label. |
| **Error (validation)** | Neutral | Medium | Low | No blame. State what's wrong + how to fix. |
| **Error (system)** | Neutral | Medium–High | Low | Include error code if available. Give specific recovery steps. |
| **Error (critical)** | Formal | High | Low | Data loss or security. State consequences clearly. |
| **Description** | Neutral | Low | Medium | What it is → What it does → Why it matters. |
| **Confirmation (reversible)** | Neutral | Medium | Low | State what will happen. Mention reversibility. |
| **Confirmation (destructive)** | Formal | High | Low | Name the resource. State permanent consequence. Specific verb on button. |
| **Empty state** | Friendly | Low | Low | Encouraging. Include a CTA to create the first item. |
| **Status (success)** | Neutral | Low | Low | Brief. Past tense. No celebration. |
| **Status (progress)** | Neutral | Medium | Low | Present tense + time estimate if possible. |
| **Status (warning)** | Neutral | Medium | Low–Medium | State what might happen. Give preventive action. |
| **Onboarding** | Friendly | Low | Low | Numbered steps. One concept per screen. "You/your". |

---

## Tone Override Rules

When the user specifies `--tone`, shift formality while keeping voice
constants intact:

| Override | Effect |
|----------|--------|
| `--tone formal` | Shift formality up one level. No contractions. Complete sentences only. |
| `--tone neutral` | Use default matrix values (no change). |
| `--tone friendly` | Shift formality down one level. Contractions OK. Warmer phrasing. Still no emoji, no exclamation marks in errors. |

**Constraints that never flex:**
- No exclamation marks in error or confirmation messages (regardless of tone)
- No emoji in any production UI copy
- No blame language ("you failed", "your mistake")
- No marketing superlatives ("powerful", "revolutionary", "best-in-class")
- No "please" in error messages (it adds guilt, not politeness)

---

## Audience Adaptation

If the UI context specifies a target audience, adjust technical depth:

| Audience | Technical Depth | Language Adjustments |
|----------|----------------|---------------------|
| **Developer** | High | Use API/CLI terms freely. Include code examples. Error codes expected. |
| **DevOps / Admin** | Medium–High | Infrastructure terms OK. Include operational context (regions, quotas). |
| **Business user** | Low | No technical terms. Benefit-focused. Analogies if helpful. |
| **Mixed / Unknown** | Low–Medium | Default safe. Explain technical terms inline on first use. |
