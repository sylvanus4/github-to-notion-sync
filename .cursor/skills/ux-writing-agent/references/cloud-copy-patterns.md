# UX Copy Patterns by Category (Cloud UI)

Structural rules, length constraints, and good/bad examples for each UI copy
category. Use alongside [cloud-tone-matrix.md](cloud-tone-matrix.md) and
[cloud-service-conventions.md](cloud-service-conventions.md).

---

## Labels

Labels identify UI elements: buttons, fields, tabs, menu items, toggles.

### Rules

- **Length:** 1–5 words. If it needs more, the UI design should be reconsidered.
- **Casing:** Title Case for buttons and tabs; Sentence case for form field labels.
- **Verbs first** for action buttons: "Create instance", "Download report".
- **Noun-first** for navigation and field labels: "Instance name", "Region".
- **No articles:** "Select region" not "Select a region" (exception: disambiguation).
- **No ending punctuation.**

### Examples

| Good | Bad | Why |
|------|-----|-----|
| Create instance | Click here to create a new instance | Too long; "click here" is redundant |
| Instance name | Name of your instance | Verbose; article unnecessary |
| Delete | Remove this item | "Delete" is sufficient for a button |
| Enable logging | Turn on the logging feature | Over-described |
| Region | Deployment region selector | Label, not description |

---

## Tooltips

Tooltips provide contextual help on hover or via info icons.

### Rules

- **Length:** 1–2 sentences, max 150 characters preferred.
- **Structure:** State what the field/control does or why it matters.
- **Action-oriented:** Tell the user what happens or what to consider.
- **No repeating the label.** The tooltip adds information; it doesn't echo.
- **End with a period** (complete sentences).
- **Optional "Learn more" link** for complex topics.

### Examples

| Good | Bad | Why |
|------|-----|-----|
| The geographic location where your data is stored. Choose a region close to your users for lower latency. | Region is where you select the region for your deployment. | Repeats the label; circular |
| Limits the number of requests per second. Exceeding this value returns a 429 error. | Rate limiting setting. | Too vague; no actionable detail |
| Changing this restarts the service. Active connections will be dropped. | Be careful when changing this. | "Be careful" is not helpful |

---

## Error Messages

Error messages inform users that something went wrong and guide recovery.

### Rules

- **Structure (3-part):**
  1. **What happened** — state the failure clearly
  2. **Why it happened** — brief cause (if known)
  3. **What to do next** — specific recovery action
- **Length:** 1–3 sentences, max 250 characters for inline; longer OK for full-page errors.
- **Tone:** Neutral, calm. Never blame the user.
- **No exclamation marks.**
- **No "Oops", "Whoops", "Uh oh"** — unprofessional for cloud services.
- **Include specifics:** resource name, error code, limit value.
- **Passive where blame would land on the user:** "The file couldn't be uploaded" not "You uploaded an invalid file."

### Structure Template

```
{What happened}. {Why (if known)}. {What to do next}.
```

### Examples

| Good | Bad | Why |
|------|-----|-----|
| The instance couldn't be created. The selected region has reached its capacity limit. Try a different region or request a quota increase. | Error! Something went wrong. Please try again. | Vague; exclamation; no cause; no specific action |
| Invalid email format. Enter an email address like name@example.com. | The email you entered is invalid!!! | Blame language; multiple exclamation marks |
| Connection to the database timed out after 30 seconds. Check your network settings or try again. | Oops! Database error. | Unprofessional; no detail |
| This API key has expired. Generate a new key in Settings > API Keys. | Your API key is bad. | Blame language; vague |

---

## Descriptions

Descriptions explain features, settings, or concepts in the UI.

### Rules

- **Length:** 1–3 sentences for inline; up to a short paragraph for feature pages.
- **Structure:** What it is → What it does → Why the user cares (benefit).
- **Present tense and active voice.**
- **Avoid marketing superlatives:** "powerful", "seamless", "best-in-class".
- **End with a period.**

### Examples

| Good | Bad | Why |
|------|-----|-----|
| Auto-scaling adjusts the number of instances based on incoming traffic. You pay only for the resources you use. | Our powerful auto-scaling solution seamlessly handles any workload! | Marketing language; exclamation; no specifics |
| Tags are key-value pairs that help you organize and filter resources across your account. | Tags feature. | No useful information |
| Enable this to receive an email when monthly spending exceeds your budget threshold. | This amazing feature sends you beautiful notifications about your billing. | Superlatives; no precision |

---

## Confirmation Dialogs

Confirmation dialogs appear before destructive or significant actions.

### Rules

- **Title:** State the action as a question or imperative. "Delete instance?" or "Delete this instance".
- **Body:** Explain the consequence. Be specific about what is lost.
- **Distinguish reversible from irreversible:**
  - Reversible: "This instance will be stopped. You can restart it later."
  - Irreversible: "This permanently deletes the instance and all associated data. This action cannot be undone."
- **Include resource identifiers:** name, ID, or count.
- **Button labels:** Use the specific verb, not generic "OK" / "Yes".
  - Good: "Delete instance" / "Cancel"
  - Bad: "OK" / "Cancel"
- **No double negatives:** "Cancel deletion" not "Don't not delete".

### Template

```
Title:  {Verb} {resource}?
Body:   This {consequence}. {Reversibility statement}.
        {Resource identifier if applicable}.
Action: [{Verb} {resource}]  [Cancel]
```

### Examples

| Good | Bad | Why |
|------|-----|-----|
| **Delete "prod-api-server"?** This permanently deletes the instance and all attached volumes. This action cannot be undone. [Delete instance] [Cancel] | **Are you sure?** Do you really want to do this? [Yes] [No] | Vague; generic buttons; no consequence |
| **Revoke API key "staging-v2"?** Applications using this key will lose access immediately. You can create a new key afterward. [Revoke key] [Cancel] | **Warning!** This will revoke the key! [OK] [Cancel] | Exclamation; generic "OK" button; no resource ID |

---

## Empty States

Empty states appear when there is no data to display.

### Rules

- **Structure:** What's empty → Why it matters → How to start.
- **Tone:** Friendly, encouraging. This is one of the few categories where
  warmth is appropriate.
- **Include a primary CTA** (call to action) button or link.
- **Length:** 1–2 sentences + CTA.
- **No sad imagery or apologetic language** ("Sorry, nothing here").
- **Avoid "No X found"** as the sole message — add next steps.

### Examples

| Good | Bad | Why |
|------|-----|-----|
| No instances yet. Create your first instance to get started. [Create instance] | No data. | No guidance; no CTA |
| No results match your search. Try adjusting your filters or search terms. | Sorry, we couldn't find anything :( | Apologetic; emoji inappropriate for cloud UI |
| You haven't created any API keys. API keys let your applications authenticate with this service. [Create API key] | Empty. | No context; no action |

---

## Status Messages

Status messages report the outcome of an action or the current state.

### Rules

- **Length:** 1 sentence, max 120 characters for toasts/snackbars.
- **Structure:** {What happened} + optional {next step or detail}.
- **Tense:** Past tense for completed actions ("Instance created"), present
  for ongoing ("Deploying instance...").
- **Success messages are brief.** Don't over-celebrate.
- **Progress messages include estimates** when possible.
- **No exclamation marks** in success messages.

### Examples

| Good | Bad | Why |
|------|-----|-----|
| Instance "web-server-01" created successfully. | Congrats!!! Your instance was created! 🎉 | Over-celebration; emoji; exclamation |
| Deploying to us-east-1. This usually takes 2–3 minutes. | Deploying... | No region; no time estimate |
| Settings saved. | Your settings have been saved successfully to the database! | Verbose; implementation detail; exclamation |
| 3 resources deleted. | Done! | Vague; exclamation |

---

## Onboarding Text

Onboarding text guides first-time users through setup and orientation.

### Rules

- **Tone:** Friendly and encouraging, but still professional.
- **Structure:** Welcome → What to do first → Why it matters.
- **Keep steps numbered** and concrete.
- **Max 3 steps per screen.** If more are needed, use progressive disclosure.
- **Don't overwhelm.** Introduce one concept at a time.
- **Use "you/your"** to address the user directly.

### Examples

| Good | Bad | Why |
|------|-----|-----|
| Welcome to Thaki Cloud. Start by creating your first project to organize your resources. [Create project] | Welcome to the most powerful cloud platform ever built! Here you can do everything! | Marketing; no specific action |
| Step 1 of 3: Choose a region. Your resources will be hosted here. You can add more regions later. | Please fill in all the required fields to configure your account settings and preferences for optimal use. | Overwhelming; passive; no progressive structure |

---

## Length Defaults

When no explicit limit is provided, use these defaults:

| Category | Characters | Words |
|----------|-----------|-------|
| Label (button) | 25 | 1–4 |
| Label (field) | 30 | 1–5 |
| Tooltip | 150 | 15–30 |
| Error (inline) | 250 | 25–50 |
| Error (full-page) | 500 | 50–100 |
| Description (inline) | 200 | 20–40 |
| Description (feature) | 500 | 50–100 |
| Confirmation (body) | 200 | 20–40 |
| Empty state | 150 | 15–30 |
| Status (toast) | 120 | 10–20 |
| Onboarding (per step) | 200 | 20–40 |
