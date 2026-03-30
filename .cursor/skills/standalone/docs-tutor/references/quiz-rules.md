# Quiz Design Rules — Platform Knowledge

## Zero-Hint Policy (CRITICAL)

Every question must be answerable ONLY by someone who actually knows the material.

1. **Option descriptions**: NEVER reveal correctness.
   - BAD: `label: "Keycloak"`, `description: "The identity provider used by the platform for SSO"`
   - GOOD: `label: "Keycloak"`, `description: "Open-source identity management"`

2. **No "(Recommended)" tag** on any option.

3. **Randomize** correct answer position — never always first or last.

4. **Question phrasing**: Ask about behavior/purpose/outcome, don't hint at the answer.
   - BAD: "Which identity provider handles SSO in the platform?"
   - GOOD: "How does the platform authenticate users across services?"

5. **Plausible distractors**: Wrong options must be real concepts from the platform domain, representing common misconceptions or related but incorrect choices.

---

## Question Types for Platform Knowledge

### 1. Architecture Decisions [recall / analysis]

Test understanding of WHY the platform is designed a certain way.

- "Why does the platform use X pattern instead of Y?"
- "What is the primary trade-off of using X for this component?"
- "Which architectural pattern governs communication between service A and B?"

### 2. Operational Procedures [application / troubleshooting]

Test knowledge of how to operate and maintain the platform.

- "What is the first step in the incident response procedure when X occurs?"
- "Which runbook should be followed when service X becomes unresponsive?"
- "What monitoring metric indicates that X is degraded?"

### 3. API & Interface Behavior [recall / application]

Test understanding of API contracts and expected behavior.

- "What HTTP status code is returned when X validation fails?"
- "What happens when a request to endpoint X exceeds the rate limit?"
- "Which header is required for authenticated requests to service X?"

### 4. Infrastructure & Configuration [recall / application]

Test knowledge of deployment, Kubernetes, and configuration.

- "How would you configure X for a production deployment?"
- "Which Kubernetes resource manages X in the platform?"
- "What environment variable controls the X behavior?"

### 5. Security & Access Control [recall / analysis]

Test understanding of authentication, authorization, and security boundaries.

- "What RBAC role is required to perform X action?"
- "How does the platform handle cross-tenant data isolation?"
- "What happens when a user's JWT token expires during an active session?"

### 6. Troubleshooting Scenarios [troubleshooting]

Test diagnostic reasoning with realistic symptoms.

- "A user reports 'X error' in the UI. What is the most likely root cause?"
- "Service X is returning 503 errors. Which component should you check first?"
- "Pod X is in CrashLoopBackOff. What are the three most common causes?"

---

## Difficulty Balancing

| Session Type | Easy | Medium | Hard |
|-------------|------|--------|------|
| Diagnostic (⬜) | 40% | 40% | 20% |
| Drill weak areas (🟥/🟨) | 10% | 30% | 60% |
| Choose a section | 25% | 50% | 25% |
| Hard-mode review (🟩/🟦) | 0% | 30% | 70% |

### Difficulty Definitions

- **Easy**: Direct recall of a single fact or definition from the docs.
- **Medium**: Application of a concept to a scenario, or comparison of two related concepts.
- **Hard**: Multi-step reasoning, troubleshooting a complex scenario, or synthesizing knowledge from multiple sections.

---

## Drilling Unresolved Concepts

When targeting 🔴 concepts from concept files:

- Do NOT repeat the exact same question — rephrase in a new context.
- Test the same underlying knowledge from a different angle.
- Example: If user confused "HPA vs VPA", ask a scenario where they must choose the correct autoscaler for a new workload type.
- Increase difficulty slightly for concepts that have been wrong multiple times.

---

## AskQuestion Format

- 4 questions per round, 4 options each, single-select.
- Header: max 12 chars, format `"Q1. <Topic>"`.
- Option labels: concise (1-3 words).
- Option descriptions: neutral context only, never reveal answer.

---

## File Update Protocol

After grading:

1. **Update** `concepts/{section}.md`:
   - Add new concept rows for first-time questions.
   - Update existing rows (increment attempts/correct, change status).
   - Add/update error notes for wrong answers.

2. **Update** dashboard:
   - Recalculate section stats from concept files.
   - Badges: 🟥 0-39% · 🟨 40-69% · 🟩 70-89% · 🟦 90-100% · ⬜ no data
   - Update weakest/strongest section and unresolved/resolved counts.

---

## Language Rule

All file content and output in the user's detected language. Badge emojis are universal. Tags remain English.
