# Consistency Rules for UX Copy

Rule set used by the `review` and `audit` sub-skills to check UI strings for
consistency. Each rule has a severity (Critical, High, Medium) and specific
check criteria.

---

## 1. Terminology Unification

**Severity**: Critical

Use one term per concept throughout the product. Never alternate between
synonyms for the same action or object.

| Concept | Preferred | Avoid |
|---------|-----------|-------|
| Removing a record permanently | "Delete" | "Remove", "Erase", "Destroy" |
| Dismissing a dialog without action | "Cancel" | "Close", "Dismiss", "Never mind" |
| Persisting changes | "Save" | "Apply", "Confirm", "Submit" (unless form submission) |
| Submitting a form | "Submit" | "Send", "Save" (unless genuinely saving a draft) |
| Returning to previous screen | "Go back" | "Return", "Back", "Previous" |
| Creating a new resource | "Create" | "Add", "New", "Make" (pick one per product) |
| Modifying an existing resource | "Edit" | "Update", "Change", "Modify" |

**How to audit**: Flag any string set where two different terms refer to the same
action on the same type of object. The first occurrence in the product's
established copy is the canonical term.

**Exception**: "Add" and "Create" may coexist if they mean different things
(e.g., "Add member" = invite existing user; "Create project" = build new resource).

---

## 2. Capitalization

**Severity**: Critical

### Rules by UI Element

| Element | Rule | Example |
|---------|------|---------|
| Page titles | Title Case | "Account Settings" |
| Section headings | Sentence case | "Notification preferences" |
| Button labels | Sentence case | "Save changes" |
| Menu items | Sentence case | "Export as CSV" |
| Tab labels | Sentence case | "Team members" |
| Tooltips | Sentence case | "Pin this item to the top" |
| Error messages | Sentence case | "Enter a valid email address." |
| Labels | Sentence case | "Email address" |
| Placeholder text | Sentence case | "Search projects..." |

### Title Case Rules

Capitalize every word except:
- Articles: a, an, the
- Conjunctions (under 4 letters): and, but, or, nor, for, yet, so
- Prepositions (under 4 letters): at, by, for, in, of, on, to, up

Always capitalize the first and last word regardless.

---

## 3. Punctuation

**Severity**: High

| Rule | Apply To | Example |
|------|----------|---------|
| End with a period | Full sentences in body text, descriptions, helper text | "We'll send you a verification email." |
| No period | Titles, headings, button labels, single phrases, list items | "Save changes" |
| No exclamation marks | Error messages, warnings, confirmations | "Something went wrong." (not "Something went wrong!") |
| Exclamation marks allowed | Success celebrations, onboarding welcomes (max 1 per screen) | "Welcome!" |
| No ellipsis for truncation | UI strings should never be truncated by the copy itself | — |
| Ellipsis for ongoing actions | Loading states, progress indicators | "Processing..." |
| Use serial comma | Lists of 3+ items in body text | "projects, tasks, and comments" |
| Straight quotes | All UI strings | "word" not "word" |
| No double spaces | All strings | — |

---

## 4. Person and Voice

**Severity**: High

### Rules

| Rule | Example |
|------|---------|
| Address the user as "you" (second person) | "You have 3 notifications." |
| Refer to the product as "we" sparingly | "We couldn't process your request." |
| Prefer implied subject (imperative) for instructions | "Enter your email" over "You should enter your email" |
| Never use "I" from the product's perspective | — |
| Never use third person for the user | "The user can..." → "You can..." |

### When "We" Is Appropriate

- Errors where the product is responsible: "We couldn't connect to the server."
- Product communications: "We've updated our privacy policy."
- Behind-the-scenes actions: "We're processing your data."

### When to Omit the Subject

- Button labels: "Save" not "You save"
- Notifications: "File uploaded." not "We uploaded your file."
- Instructions: "Choose a plan." not "You should choose a plan."

---

## 5. Active vs. Passive Voice

**Severity**: Medium

### Default: Active Voice

The subject performs the action. Active voice is shorter, clearer, and
more direct.

```
Passive: "Your settings have been updated."
Active:  "Settings updated." (or "You updated your settings.")

Passive: "An email will be sent to you."
Active:  "We'll send you an email."

Passive: "The file was not found."
Active:  "We couldn't find that file."
```

### When Passive Is Acceptable

- The actor is irrelevant: "Your account was created on March 1, 2026."
- Blame avoidance: "Your session was ended." (better than "We ended your session.")
- System-level messages where "we" feels wrong: "Data is encrypted at rest."

---

## 6. Number and Date Formatting

**Severity**: Medium

| Type | Format | Example |
|------|--------|---------|
| Numbers under 10 in prose | Spelled out | "You have three items" |
| Numbers 10+ in prose | Digits | "You have 15 items" |
| Numbers in UI elements | Always digits | "3 projects" (not "three projects") |
| Dates (US English) | MMM D, YYYY | "Mar 24, 2026" |
| Dates (international) | D MMM YYYY | "24 Mar 2026" |
| Time | h:mm AM/PM | "2:30 PM" |
| Currency | Symbol + digits, 2 decimals | "$12.00" |
| Percentages | Digits + % (no space) | "85%" |
| File sizes | KB/MB/GB with 1 decimal | "4.2 MB" |

---

## 7. Abbreviations and Acronyms

**Severity**: Medium

| Rule | Example |
|------|---------|
| Spell out on first use with acronym in parentheses | "Single Sign-On (SSO)" |
| Common tech abbreviations may be used without expansion | URL, API, PDF, CSV |
| Avoid Latin abbreviations in user-facing copy | "for example" not "e.g."; "that is" not "i.e." |
| Pluralize abbreviations without an apostrophe | "APIs" not "API's" |

---

## 8. Inclusive Language

**Severity**: Medium

| Avoid | Use Instead |
|-------|-------------|
| "Whitelist / Blacklist" | "Allowlist / Blocklist" |
| "Master / Slave" | "Primary / Replica" |
| "Guys" | "Team", "Everyone", "Folks" |
| "He/she" | "They" (singular) |
| "Sanity check" | "Quick check", "Smoke test" |
| "Dummy" (for data) | "Sample", "Test", "Placeholder" |
| "Native" (for features) | "Built-in" |
| "Crippled" | "Limited", "Restricted" |

---

## Audit Procedure

When running the `audit` sub-skill:

1. Load all strings into a single list
2. Check each rule category (1–8) against every string
3. Record violations with: rule number, severity, affected string, current value, recommended fix
4. Group findings by severity: Critical → High → Medium
5. Calculate a consistency score: `(total_strings - violation_count) / total_strings * 10`
6. Present as a structured report with before/after fix suggestions
