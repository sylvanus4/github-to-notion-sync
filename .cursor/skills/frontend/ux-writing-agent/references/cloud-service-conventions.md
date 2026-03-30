# Cloud Service UX Writing Conventions

Patterns and conventions distilled from major cloud platforms (AWS, GCP, Azure)
and established SaaS products. Use as a reference when generating copy for
cloud infrastructure and platform UIs.

---

## Resource Lifecycle Language

Cloud products revolve around creating, managing, and destroying resources.
Use consistent language for each lifecycle phase:

| Phase | Verb | UI Pattern | Example |
|-------|------|-----------|---------|
| **Create** | Create | Form → Review → Confirm | "Create instance" |
| **Read** | View / Details | Detail page, summary card | "View instance details" |
| **Update** | Edit / Configure | Inline edit, settings page | "Edit configuration" |
| **Delete** | Delete / Terminate | Confirmation dialog | "Delete instance" |
| **Start** | Start | Action button or menu | "Start instance" |
| **Stop** | Stop | Action button or menu | "Stop instance" |
| **Restart** | Restart | Action button or menu | "Restart instance" |

### Destructive vs. Reversible Actions

Always communicate the reversibility of an action:

| Action Type | Language Pattern | Example |
|------------|----------------|---------|
| **Reversible** | "{Action}. You can {undo action} later." | "Stop this instance. You can start it again later." |
| **Irreversible** | "This permanently {action}. This action cannot be undone." | "This permanently deletes the instance and all attached storage. This action cannot be undone." |
| **Cascading** | "{Action}. This also {cascading effect}." | "Delete this project. This also deletes all instances, databases, and storage within it." |

---

## Async Operations

Cloud operations are frequently asynchronous. Communicate state transitions
clearly:

| State | Copy Pattern | Example |
|-------|-------------|---------|
| **Initiated** | "{Action} {resource}..." | "Creating instance..." |
| **In progress** | "{Resource} is being {action}. This usually takes {time estimate}." | "Your instance is being created. This usually takes 1–2 minutes." |
| **Completed** | "{Resource} {past tense action}." | "Instance created." |
| **Failed** | "{Resource} couldn't be {action}. {Reason}. {Recovery}." | "The instance couldn't be created. The selected instance type is unavailable in this region. Try a different region or instance type." |
| **Partial** | "{N} of {total} {resources} {action}. {M} failed." | "8 of 10 instances updated. 2 failed due to configuration errors." |

### Time Estimates

| Duration | Copy |
|----------|------|
| < 10 seconds | Don't show a time estimate; use a spinner |
| 10s – 1 min | "This usually takes a few seconds." |
| 1 – 5 min | "This usually takes 1–2 minutes." (be specific) |
| 5 – 30 min | "This may take up to {N} minutes." |
| > 30 min | "This may take a while. We'll notify you when it's complete." |

---

## Permissions and Access

| Scenario | Copy Pattern |
|----------|-------------|
| No permission | "You don't have permission to {action}. Contact your administrator to request {specific permission}." |
| Read-only | "You have view-only access to this {resource}. Contact the owner to request edit access." |
| Expired credentials | "Your {credential type} has expired. {How to renew}." |
| MFA required | "This action requires multi-factor authentication. Verify your identity to continue." |

---

## Quotas and Limits

| Scenario | Copy Pattern |
|----------|-------------|
| Approaching limit | "You've used {N} of {max} {resources}. {Link to increase}." |
| At limit | "You've reached the maximum of {max} {resources}. Delete existing {resources} or request a quota increase." |
| Over limit (blocked) | "{Action} blocked. Your account has reached its {resource} quota ({max}). Request a quota increase to continue." |

---

## Billing and Costs

| Scenario | Copy Pattern |
|----------|-------------|
| Cost implication | "This {resource/action} will incur charges. Estimated cost: {amount}/month." |
| Free tier | "This is included in the free tier. No charges will apply." |
| Budget alert | "Your spending has reached {N}% of your monthly budget ({amount}). {Action to take}." |
| Free trial expiry | "Your free trial ends in {N} days. Add a payment method to continue using {service}." |

---

## Tables and Lists

Cloud UIs are data-heavy. Follow these conventions for tabular data:

### Column Headers
- Sentence case
- No articles ("Name" not "The name")
- Consistent width-appropriate truncation (tooltip on hover for full value)

### Empty Table States
- "No {resources} found." + context-appropriate CTA
- If filtered: "No {resources} match your filters. Try adjusting your search criteria."
- If genuinely empty: "No {resources} yet. Create your first {resource} to get started."

### Bulk Actions
- "{N} {resources} selected" (show count)
- Confirmation: "Delete {N} {resources}? This action cannot be undone."
- Progress: "Deleting {N} {resources}..."
- Result: "{N} {resources} deleted." or "{N} deleted, {M} failed."

---

## Navigation and Page Structure

| Element | Convention | Example |
|---------|-----------|---------|
| **Page title** | Resource type or feature name | "Instances", "Network Settings" |
| **Breadcrumbs** | Hierarchy path | "Home > Project > Instances > web-server-01" |
| **Tab labels** | Feature area, Title Case | "Overview", "Monitoring", "Configuration" |
| **Section headers** | Descriptive, Sentence case | "Network configuration", "Access control" |
| **Sidebar nav** | Short labels, Title Case | "Compute", "Storage", "Networking" |

---

## Forms

### Field Labels
- Sentence case
- Concise (1–3 words)
- No colons after labels

### Helper Text (below field)
- Sentence case
- Constraints and format: "Must be 3–63 characters. Lowercase letters, numbers, and hyphens only."
- No "Please enter..."

### Required vs. Optional
- Mark optional fields with "(optional)" after the label
- Required fields are the default — don't mark them
- Never use asterisks (*) alone without explanation

### Validation Messages
- Inline, below the field
- State what's wrong + correct format
- "Enter a valid email address (e.g., name@example.com)."
- Not "Invalid!" or "Error in this field"

---

## Search

| State | Copy |
|-------|------|
| Placeholder | "Search {resources}..." |
| No results | "No results for \"{query}\". Check your spelling or try different keywords." |
| Loading | "Searching..." |
| Results | "{N} results" (or "{N} {resources}" if single type) |
| Filter applied | "Showing {N} of {total} {resources}" |

---

## Progressive Disclosure

Cloud UIs manage complexity through progressive disclosure. Apply these
copy patterns:

| Pattern | When | Copy |
|---------|------|------|
| **Expandable section** | Advanced settings | "Advanced options" (collapsed by default) |
| **Learn more link** | Concept explanation | "This determines X. [Learn more]" |
| **Tooltip** | Contextual help | Info icon (ⓘ) next to the element |
| **Inline help** | First-time feature | Brief explanation that can be dismissed |
| **Documentation link** | Deep technical detail | "For more information, see {doc title}." |

Link text rules:
- Never "Click here" or "Learn more" as standalone links
- Descriptive: "Learn more about instance types" or "View the pricing page"
- Opens in new tab: "(opens in a new tab)" appended for external links in
  accessibility-critical contexts
