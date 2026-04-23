# Goose Email Sequence Architect

Design multi-step email sequences for any use case — onboarding, nurture, cold outreach, reactivation, upsell, or event follow-up. Each email gets subject lines, preview text, body structure, CTA, send timing, and branching logic based on open/click behavior. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/email-sequence-architect.

## When to Use

- "Design an email onboarding sequence"
- "Create a cold outreach email series"
- "이메일 시퀀스 설계", "온보딩 이메일 시퀀스"
- "Build a reactivation email campaign"

## Do NOT Use

- For sending actual emails (use gws-gmail or gws-email-reply)
- For email triage and inbox management (use gmail-daily-triage)
- For one-off email drafts (use kwp-brand-voice-brand-voice-enforcement)

## Methodology

### Phase 1: Sequence Architecture
- **Goal**: Primary metric (activation, conversion, reactivation)
- **Audience**: Who receives this? (segment definition)
- **Length**: Number of emails (typically 3-7)
- **Cadence**: Timing between emails
- **Exit conditions**: When to stop sending

### Phase 2: Per-Email Design
For each email in the sequence:

| Field | Description |
|-------|-------------|
| Subject line | 3 variants (curiosity, benefit, urgency) |
| Preview text | Complements subject, adds context |
| Hook | First 2 lines that stop the scroll |
| Body structure | Problem → Agitate → Solution OR Story → Lesson → CTA |
| CTA | Single, clear call-to-action |
| Send timing | Day + time relative to trigger |

### Phase 3: Branching Logic
Define conditional paths:
- **Opened but didn't click** → Follow-up with different angle
- **Clicked but didn't convert** → Send social proof email
- **No open** → Resend with new subject line
- **Converted** → Exit sequence, enter next sequence

### Phase 4: Performance Benchmarks
Set expectations for:
- Open rate targets by email position (1st: 40%+, 3rd: 25%+)
- Click rate targets (5-15% depending on type)
- Reply rate (for cold outreach: 3-8%)
- Unsubscribe threshold (>2% = problem)

## Output: Complete Email Sequence with per-email specs, branching logic, timing, and benchmark targets
