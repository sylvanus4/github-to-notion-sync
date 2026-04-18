## Stripe Integration

Set up Stripe payment processing with products, checkout, webhooks, subscriptions, and security best practices.

### Usage

```
/stripe "set up subscription billing for a SaaS app with 3 tiers"
/stripe "add one-time payment checkout for an e-commerce store"
/stripe "configure webhooks for subscription lifecycle events"
```

### Workflow

1. **Gather** — Determine payment model (one-time, subscription, usage-based), required features, and webhook events
2. **Catalog** — Define products and prices in Stripe with proper IDs
3. **Integrate** — Implement Checkout sessions, webhook handlers, and customer portal
4. **Secure** — Verify API key storage, webhook signatures, HTTPS, and PCI compliance
5. **Test** — Run through test card scenarios and subscription lifecycle

### Execution

Read and follow the `stripe-integration` skill (`.cursor/skills/standalone/stripe-integration/SKILL.md`) for the full 6-phase integration workflow.

### Examples

SaaS subscription billing:
```
/stripe "subscription billing with Free, Pro ($29/mo), and Enterprise ($99/mo) tiers"
```

One-time checkout:
```
/stripe "one-time payment for digital product downloads with Stripe Checkout"
```
