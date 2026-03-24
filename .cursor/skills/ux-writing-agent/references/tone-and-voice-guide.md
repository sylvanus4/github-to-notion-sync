# Tone and Voice Guide for UX Writing

Reference guide for all UX writing sub-skills. Defines the default tone
attributes, audience-specific variations, and do/don't examples. Users can
override any section by providing their own tone-and-voice document.

## Default Tone Attributes

| Attribute | Target | Description |
|-----------|--------|-------------|
| **Clarity** | Always | Say exactly what you mean. Avoid ambiguity |
| **Conciseness** | Always | Use the fewest words that convey the full meaning |
| **Helpfulness** | Always | Guide the user toward resolution, not just state a problem |
| **Confidence** | High | Sound assured without being arrogant. Avoid hedging words |
| **Warmth** | Moderate | Friendly but professional. Not robotic, not overly casual |
| **Technicality** | Low–Medium | Avoid jargon unless the audience expects it |

### Tone Spectrum

```
Robotic ←──────────────────────────────────→ Overly casual
         ↑ Target zone: professional, warm, clear
```

## Audience-Specific Variations

### B2C (Consumer Products)

- Warmer, more conversational
- First person plural ("We") for the product, second person ("you") for the user
- Contractions encouraged ("can't", "won't", "you'll")
- Shorter sentences (target: 15 words or fewer)

### B2B (Business/Enterprise Products)

- More formal, but still clear
- Second person ("you") for the user; avoid first person plural unless necessary
- Contractions acceptable but not required
- Moderate sentence length (target: 20 words or fewer)

### Internal Tools

- Direct and efficient
- Can use domain-specific terminology the team already understands
- Brevity is paramount — users are repeat users
- Imperative voice preferred ("Enter the value" over "You can enter the value")

## Core Principles

### P1: Clear Over Clever

Never sacrifice clarity for wit, wordplay, or brand personality. The user must
understand the message on the first read.

- Puns, idioms, and cultural references are fragile across languages and contexts
- Clever copy that confuses 5% of users is worse than plain copy that confuses none

### P2: Lead With the Outcome

Tell the user what happened or what they can do — before explaining why.

```
Bad:  "Due to an internal server error, your request could not be processed."
Good: "Something went wrong. Please try again in a few minutes."
```

### P3: Use Active Voice

The subject performs the action. Passive voice buries responsibility and adds
words.

```
Bad:  "Your password has been changed."
Good: "You changed your password."

Bad:  "The file was uploaded successfully."
Good: "File uploaded."
```

### P4: One Idea Per Message

Each UI string should communicate exactly one thing. If you need two ideas,
use two strings or a two-sentence structure with a clear line break.

### P5: Avoid Blame

Never imply the user made a mistake, even when they did. Frame errors as
situations, not accusations.

```
Bad:  "You entered an invalid email."
Good: "That doesn't look like an email address. Check for typos."

Bad:  "Wrong password."
Good: "That password doesn't match our records. Try again or reset it."
```

## Do / Don't Examples

| # | Don't | Do | Why |
|---|-------|-----|-----|
| 1 | "An error has occurred." | "Something went wrong. Try again." | Generic → specific + actionable |
| 2 | "Invalid input." | "Enter a valid email address (e.g., name@example.com)." | Show the expected format |
| 3 | "Are you sure you want to delete?" | "Delete this project? This can't be undone." | Name the object; state the consequence |
| 4 | "Success!" | "Changes saved." | State what actually happened |
| 5 | "Please wait while we process your request." | "Processing..." | Concise; "please" is unnecessary in progress states |
| 6 | "Click here to learn more." | "Learn more about pricing" | Descriptive link text for accessibility |
| 7 | "Oops! Something went wrong :(" | "We couldn't complete your request. Try again." | Emoticons and "oops" undermine trust in errors |
| 8 | "Your session has been terminated due to inactivity." | "You've been signed out. Sign in again to continue." | Lead with outcome, provide next step |
| 9 | "No results were found for your search query." | "No results for '[query]'. Try different keywords." | Echo the input, suggest action |
| 10 | "This field is required." | "Enter your name to continue." | Specific; tells them what to enter |
| 11 | "Unauthorized. Access denied." | "You don't have access to this page. Contact your admin." | Human language, actionable |
| 12 | "Operation completed successfully." | "Done." (or describe what was done) | Don't say "operation" or "successfully" |

## Customization

When the user provides their own tone-and-voice document:

1. Parse the document for explicit tone attributes (formal/casual, technical level, etc.)
2. Override the matching attributes in this default guide
3. Preserve any default attributes not explicitly overridden
4. Apply the merged tone profile to all subsequent copy generation

When no custom guide is available, use the B2B defaults above as the baseline.
