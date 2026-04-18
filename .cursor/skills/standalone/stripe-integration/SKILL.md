---
name: stripe-integration
description: Set up Stripe payment processing — products, prices, checkout sessions, webhooks, subscriptions, and customer portal — with security best practices. Use when the user asks to "add payments", "set up Stripe", "integrate Stripe", "subscription billing", "payment flow", "webhook setup", "결제 연동", "스트라이프 설정", "구독 결제", "웹훅 설정", "결제 기능 추가", or needs to process payments via Stripe. Do NOT use for non-Stripe payment providers (PayPal, Square — handle directly), general accounting (use finance skills), or fraud analysis beyond Stripe Radar defaults.
---

# Stripe Integration

Set up secure Stripe payment flows including products, prices, checkout sessions, webhooks, subscriptions, and customer portal — following Stripe's recommended patterns and security best practices.

## When to Use

- Adding payment processing to a new or existing application
- Setting up subscription billing with Stripe
- Implementing Stripe Checkout or Payment Intents
- Configuring webhooks for payment events
- Setting up Stripe Customer Portal for self-service billing
- Migrating from another payment provider to Stripe

## When NOT to Use

- General financial analysis or accounting (use finance skills)
- Payment processing with non-Stripe providers (PayPal, Square, etc.)
- Tax calculation without Stripe Tax
- Fraud analysis beyond Stripe Radar defaults

## Workflow

### Phase 1: Requirements Gathering

1. Determine payment model:
   - **One-time payments**: Products with fixed prices
   - **Subscriptions**: Recurring billing with plan tiers
   - **Usage-based**: Metered billing per unit consumed
   - **Hybrid**: Combination of the above
2. Identify required features:
   - Customer portal (self-service plan changes, cancellations)
   - Trial periods
   - Proration on plan changes
   - Multiple currencies
   - Tax collection (Stripe Tax)
   - Invoicing
3. Determine webhook events needed for your business logic

### Phase 2: Product & Price Setup

1. Define products in Stripe Dashboard or via API:
   ```
   stripe products create --name="Pro Plan" --description="Full access"
   ```
2. Attach prices to products:
   - Recurring prices for subscriptions
   - One-time prices for single purchases
   - Tiered pricing if applicable
3. Document the product catalog with IDs for code reference

### Phase 3: Backend Integration

1. **Install Stripe SDK** for your stack:
   - Node.js: `npm install stripe`
   - Python: `pip install stripe`
   - Go: `go get github.com/stripe/stripe-go/v82`
2. **Create Checkout Sessions** (recommended for most use cases):
   - Set success and cancel URLs
   - Attach customer email or existing customer ID
   - Configure line items from your product catalog
3. **Set up Stripe webhooks**:
   - Create webhook endpoint in your application
   - Register it in Stripe Dashboard or CLI
   - **Always verify webhook signatures** — never trust unverified payloads
   - Handle these critical events at minimum:
     - `checkout.session.completed`
     - `invoice.paid`
     - `invoice.payment_failed`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
4. **Implement idempotency** for all write operations using idempotency keys

### Phase 4: Security Checklist

- [ ] API keys stored in environment variables, never in code
- [ ] Webhook signature verification enabled
- [ ] HTTPS enforced on all endpoints
- [ ] Stripe.js or Stripe Elements used for card collection (never handle raw card data)
- [ ] Idempotency keys used for all create/update operations
- [ ] Test mode used for development (`sk_test_*` keys)
- [ ] Restricted API keys created for production with minimal permissions
- [ ] PCI compliance self-assessment completed (SAQ-A for Checkout/Elements)

### Phase 5: Testing

1. Use Stripe CLI for local webhook testing:
   ```
   stripe listen --forward-to localhost:3000/webhooks/stripe
   ```
2. Test with Stripe's test card numbers:
   - Success: `4242 4242 4242 4242`
   - Decline: `4000 0000 0000 0002`
   - 3D Secure: `4000 0027 6000 3184`
3. Verify all webhook handlers process events correctly
4. Test subscription lifecycle: create → upgrade → downgrade → cancel
5. Test failed payment recovery flow

### Phase 6: Customer Portal (if subscriptions)

1. Configure portal in Stripe Dashboard
2. Create portal sessions from your backend
3. Allow customers to:
   - Update payment method
   - Switch plans
   - Cancel subscription
   - View billing history

## Gotchas

1. **Currency units trap.** Stripe uses the smallest currency unit (cents for USD, yen for JPY). Passing `1000` means $10.00, not $1,000. Always confirm unit conversion.
2. **Webhook ordering is not guaranteed.** Events like `invoice.paid` may arrive before `checkout.session.completed`. Design handlers to be idempotent and order-independent.
3. **Test vs live key confusion.** The #1 production incident is using `sk_test_*` in production or `sk_live_*` in development. Double-check before every deploy.
4. **Customer portal requires products created in Dashboard.** API-only products may not appear in the portal. Verify portal configuration after product setup.

## Anti-Example

```python
# BAD: Hardcoded API key
stripe.api_key = "sk_live_abc123"  # NEVER do this

# BAD: No webhook signature verification
@app.post("/webhooks/stripe")
def handle_webhook(request):
    event = json.loads(request.body)  # Trusting unverified payload
    process_event(event)  # Attacker can forge events

# BAD: Wrong currency unit
stripe.PaymentIntent.create(
    amount=29.99,  # Should be 2999 (cents)
    currency="usd",
)
```

## Verification

After completing all phases:
1. Confirm webhook signature verification is present in the handler code
2. Verify API keys are loaded from environment variables, not hardcoded
3. Run at least one test payment with `4242 4242 4242 4242` and one decline with `4000 0000 0000 0002`
4. Confirm the security checklist in Phase 4 has all items checked
5. Verify Stripe customer ID is stored and linked to the user model in the database

## Constraints

- Never log or store raw card numbers — use Stripe Elements or Checkout
- Always verify webhook signatures before processing events
- Use test mode keys during development; never use live keys in non-production
- Implement retry logic for failed webhook deliveries
- Store Stripe customer IDs in your database, linked to your user model
- Handle currency correctly — Stripe uses smallest currency unit (cents for USD)
- Do NOT generate a complete SaaS billing system — this skill handles Stripe integration only, not pricing page UI or plan management logic

## Output

Produce the following deliverables:

1. **Product catalog document** — Table of products, prices, and Stripe IDs
2. **Integration code** — Checkout session creation, webhook handler, customer portal
3. **Webhook event map** — Which events trigger which business logic
4. **Security checklist** — Completed with pass/fail for each item
5. **Test plan** — Card numbers and scenarios to verify before go-live
