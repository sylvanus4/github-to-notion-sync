# UX Copy Patterns

Templates and guidelines for 10 common UI element types. Each pattern defines
the structure, character limits, good/bad examples, and state variations.

---

## 1. Error Message

**Structure**: What happened + Why (if helpful) + What to do next

**Character limit**: 80–150 characters (body), 5–40 characters (title if separate)

**States**: Validation error, System error, Permission error, Network error

| Aspect | Good | Bad |
|--------|------|-----|
| Tone | Empathetic, helpful | Blaming, technical |
| Action | "Check your email and try again." | "Invalid input." |
| Specificity | "File must be under 10 MB." | "File too large." |

**Template**:
```
[Title — optional, short]: [What happened]
[Body]: [Consequence or cause, if it helps]. [Next step].
```

**Examples**:
```
Title: "Can't upload file"
Body:  "This file is larger than 10 MB. Compress it or choose a smaller file."

Inline: "Enter a valid phone number (e.g., +1 555-123-4567)."
```

---

## 2. Empty State

**Structure**: What this space is for + How to populate it

**Character limit**: 40–120 characters (headline), 60–200 characters (description)

**States**: First use, No results, Filtered empty, Error empty

| Aspect | Good | Bad |
|--------|------|-----|
| Framing | Opportunity | Emptiness |
| CTA | Specific action | Generic "Get started" without context |

**Template**:
```
[Headline]: [Describe what will appear here]
[Description]: [How to create the first item]. [Optional: benefit].
[CTA button]: [Verb + object]
```

**Examples**:
```
Headline:    "No projects yet"
Description: "Create your first project to start tracking tasks."
CTA:         "Create project"

Headline:    "No results for '[query]'"
Description: "Try different keywords or remove some filters."
```

---

## 3. Modal / Confirmation Dialog

**Structure**: Action question (title) + Consequences (body) + Action buttons

**Character limit**: 30–60 characters (title), 60–150 characters (body)

**States**: Destructive confirmation, Informational, Save/discard changes

| Aspect | Good | Bad |
|--------|------|-----|
| Title | "Delete this project?" | "Are you sure?" |
| Buttons | "Delete project" / "Keep project" | "OK" / "Cancel" |
| Consequence | States what will happen | Vague warning |

**Template**:
```
[Title]: [Verb + object]?
[Body]:  [What specifically will happen]. [Reversibility statement].
[Primary]: [Same verb + object as title]
[Secondary]: [Verb that preserves current state]
```

**Examples**:
```
Title:     "Remove team member?"
Body:      "Alex Kim will lose access to all projects in this workspace. You can re-invite them later."
Primary:   "Remove member"
Secondary: "Keep member"

Title:     "Discard unsaved changes?"
Body:      "Your edits to this document will be lost."
Primary:   "Discard changes"
Secondary: "Keep editing"
```

---

## 4. Tooltip

**Structure**: What it does (one sentence)

**Character limit**: 30–80 characters. Never exceed 120.

| Aspect | Good | Bad |
|--------|------|-----|
| Length | Single sentence | Paragraph |
| Trigger context | Adds info the icon/label cannot convey alone | Repeats the label text |

**Template**:
```
[One sentence explaining what the control does or what the term means]
```

**Examples**:
```
"Pin this item to keep it at the top of the list."
"Only workspace admins can change billing settings."
"Last updated 3 hours ago by Alex Kim."
```

---

## 5. Label / Form Field

**Structure**: Noun or noun phrase (field label) + Helper text (optional)

**Character limit**: 10–30 characters (label), 30–80 characters (helper text)

| Aspect | Good | Bad |
|--------|------|-----|
| Label | Noun phrase, sentence case | Verb phrase, ALL CAPS |
| Helper | Specific format or constraint | Restates the label |

**Template**:
```
[Label]: [Noun phrase in sentence case]
[Helper text — optional]: [Format hint, constraint, or example]
```

**Examples**:
```
Label:  "Email address"
Helper: "We'll send a verification link to this email."

Label:  "Phone number"
Helper: "Include country code (e.g., +82 10-1234-5678)."
```

---

## 6. Placeholder Text

**Structure**: Example value or short instruction

**Character limit**: 15–40 characters

| Aspect | Good | Bad |
|--------|------|-----|
| Content | Example value | Instruction that duplicates the label |
| Format | Matches expected input format | Generic text |

**Template**:
```
[Example value matching the expected format]
— or —
[Short instruction: verb + object]
```

**Examples**:
```
"name@example.com"          (email field)
"Search projects..."        (search bar)
"Enter amount"              (numeric input)
"e.g., New York, Seoul"     (location field)
```

---

## 7. CTA Button

**Structure**: Verb + Object (or just Verb for obvious context)

**Character limit**: 10–25 characters. Maximum 4 words.

| Aspect | Good | Bad |
|--------|------|-----|
| Pattern | Verb + object | Vague noun ("Submit", "Next") |
| Specificity | "Create project" | "Create" (create what?) |
| Primary CTA | Clear visual hierarchy | Multiple competing CTAs |

**Template**:
```
[Primary]: [Verb + object]
[Secondary]: [Lower-commitment alternative]
[Tertiary — text link]: [Even lower commitment]
```

**Examples**:
```
"Start free trial"      (primary)
"View pricing"          (secondary)
"Learn more"            (tertiary)

"Save changes"          (primary)
"Discard"               (secondary)
```

---

## 8. Notification / Toast

**Structure**: What happened (past tense or present confirmation)

**Character limit**: 40–80 characters. Must be scannable in 3 seconds.

**States**: Success, Info, Warning, Error

| Aspect | Good | Bad |
|--------|------|-----|
| Tense | Past tense for completed actions | Future tense |
| Action link | Optional "Undo" or "View" | No way to act |

**Template**:
```
[Icon/color for state] [What happened]. [Optional action link].
```

**Examples**:
```
Success: "Project created." [View project]
Info:    "Your export is ready." [Download]
Warning: "You're approaching your storage limit." [Upgrade plan]
Error:   "Couldn't save changes. Try again." [Retry]
```

---

## 9. Onboarding / Welcome

**Structure**: Welcome (brief) + What you can do here + First action

**Character limit**: 30–50 characters (headline), 60–120 characters (body)

| Aspect | Good | Bad |
|--------|------|-----|
| Focus | First value moment | Feature dump |
| CTA | One clear next step | Multiple competing actions |

**Template**:
```
[Headline]: Welcome or value proposition
[Body]:     [1–2 sentences about what the user can do]
[CTA]:      [Single verb + object for the first task]
```

**Examples**:
```
Headline: "Welcome to [Product]"
Body:     "Create and manage your projects in one place."
CTA:      "Create your first project"

Headline: "Your workspace is ready"
Body:     "Invite your team to start collaborating."
CTA:      "Invite team members"
```

---

## 10. Success / Completion Message

**Structure**: What was completed + Optional next step

**Character limit**: 20–60 characters (inline), 40–120 characters (full-page)

| Aspect | Good | Bad |
|--------|------|-----|
| Tone | Confirming, understated | Over-celebratory |
| Content | States the completed action | Generic "Success!" |

**Template**:
```
[Inline]:    "[Object] [past-tense verb]."
[Full-page]: "[Headline: What was done]" + "[Body: What happens next]"
```

**Examples**:
```
Inline:    "Changes saved."
Inline:    "Invitation sent to alex@example.com."

Full-page headline: "Payment confirmed"
Full-page body:     "You'll receive a receipt at your email. Your plan is now active."
Full-page CTA:      "Go to dashboard"
```

---

## Pattern Selection Guide

| User Needs To... | Pattern |
|-------------------|---------|
| Know something went wrong | Error Message |
| See there's nothing here yet | Empty State |
| Confirm a risky action | Modal / Confirmation Dialog |
| Understand a UI element | Tooltip |
| Fill in a form field | Label / Placeholder |
| Take a primary action | CTA Button |
| Know something just happened | Notification / Toast |
| Get started for the first time | Onboarding / Welcome |
| Know an action succeeded | Success / Completion Message |
