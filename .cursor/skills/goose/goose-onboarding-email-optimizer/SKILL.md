# Goose Onboarding Email Optimizer

Audit and optimize SaaS onboarding email sequences to reduce time-to-value and improve activation rates. Analyzes existing sequences against best practices, identifies drop-off points, and recommends specific improvements. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/onboarding-email-optimizer.

## When to Use

- "Audit our onboarding emails"
- "Optimize our activation email sequence"
- "온보딩 이메일 최적화", "활성화 이메일 개선"
- "Why aren't new users activating?"

## Do NOT Use

- For designing email sequences from scratch (use goose-email-sequence-architect)
- For retention beyond onboarding (use goose-retention-playbook-builder)
- For cold outreach sequences (use kwp-sales-draft-outreach)

## Methodology

### Phase 1: Sequence Audit
Review existing onboarding emails for:
- **Timing gaps** — too many emails too fast, or gaps that lose momentum
- **Value clarity** — does each email drive toward a specific activation milestone?
- **Personalization** — is it generic or role/use-case adapted?
- **Action clarity** — single clear CTA per email?
- **Mobile readability** — short paragraphs, scannable?

### Phase 2: Activation Milestone Mapping
Map emails to key milestones:
1. Account creation → Email 1 (welcome + first action)
2. First [key action] → Email 2 (celebrate + next step)
3. Invite team / connect integration → Email 3 (expansion)
4. Regular usage pattern → Email 4 (tips + advanced features)
5. No activation after X days → Branch: reactivation sequence

### Phase 3: Drop-off Analysis
Identify where users disengage:
- Which email has lowest open rate? (subject line problem)
- Which email has lowest click rate? (CTA or value problem)
- Which milestone has lowest completion? (product friction)
- What's the average time-to-activation?

### Phase 4: Optimization Recommendations
Per email, recommend:
- Subject line A/B test variants
- Body copy improvements
- CTA optimization
- Timing adjustments
- Personalization opportunities
- Trigger-based vs time-based sending

## Output: Onboarding Email Audit with per-email analysis, drop-off diagnosis, and specific optimization recommendations with expected impact
