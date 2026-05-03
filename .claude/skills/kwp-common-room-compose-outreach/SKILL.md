---
name: kwp-common-room-compose-outreach
description: >-
  Generate personalized outreach messages using Common Room signals. Triggers
  on 'draft outreach to [person]', 'write an email to [name]', 'compose a
  message for [contact]', or any outreach drafting request. Do NOT use for
  tasks outside the common-room domain. Korean triggers: "생성", "이메일".
---

# Compose Outreach

Generate three personalized outreach formats — email, call script, and LinkedIn message — grounded in Common Room signals for a specific company or contact.

## Outreach Process

### Step 1: Look Up the Target

Use Common Room MCP tools to find and retrieve data for the target (company and/or specific contact). Pull:
- Recent product activity and engagement signals
- Community activity (posts, questions, reactions)
- 3rd-party intent signals (job postings, news, funding)
- Relationship history (prior contact, meetings, email opens)

If the user specified a person, run contact-level research. If only a company was given, identify the best contact to target based on title, engagement, and role.

### Step 2: Web Search for External Hooks (If CR Signals Are Thin)

If CR returned strong signals (recent activity, engagement, product usage), those should drive personalization — skip web search. If CR signals are thin or the prospect has little CR activity, run a web search for external hooks:

**What to search:**
- `"[company name]" funding OR acquisition OR launch OR announcement` — last 30 days
- `"[contact full name]" "[company name]"` — look for recent articles, interviews, LinkedIn posts, or conference talks

**Prioritize external hooks that are:**
- Very recent (< 2 weeks) — the prospect is likely still thinking about it
- Publicly visible — they know you could have seen it
- Change-signaling — growth, new role, new product, new market

If the user explicitly asks for web search or external hooks, run it regardless of CR signal richness.

### Step 3: Spark Enrichment (If Available)

If Spark is available, run enrichment on the target contact to get persona classification, background, and influence signals. Use this to calibrate tone and message angle.

### Step 4: Identify the Best Hooks

From the signal data, identify the 1–3 strongest personalization hooks. Rank by:
1. **Recency** — happened in the last 7–14 days
2. **Specificity** — a concrete action they took, not a general trend
3. **Relevance** — connects directly to a value your product delivers

Good hooks: posted a question in the community about X, just hired 5 engineers, recently started using [feature], company just raised Series B, trial nearing expiration, champion just changed jobs.

Bad hooks: "I noticed you're a customer" or generic industry trends.

### Step 5: Generate All Three Formats

Use the strongest hooks to write all three formats. Each format has different constraints and conventions — follow the format-specific guidelines in `references/outreach-formats-guide.md`.

Always produce all three, clearly labeled.

When the user's company context is available (see `references/my-company-context.md`), ground the value bridge and pitch in the user's specific product and positioning.

### Step 6: Annotate Your Choices

After the three drafts, include a brief note (2–4 sentences) explaining:
- Which signals were used and why they were chosen
- Any assumptions made (e.g., inferred call objective)
- Alternative angles if the primary hook doesn't land

## Output Format

```
## Outreach for [Name / Company]

### 📧 Email

**Subject:** [Subject line]

[Email body — 3–5 sentences]

---

### 📞 Call Script

**Opening:**
[Opening line — conversational, 1–2 sentences]

**Value Bridge:**
[Why you're calling and why now — 2–3 sentences tied to a signal]

**Ask:**
[Single, low-friction ask — e.g., 15-minute call, specific question]

---

### 💼 LinkedIn Message

[Under 300 characters. Warm, personal, no pitch.]

---

### Signal Notes
[2–4 sentences: which signals were used, why, and any alternative angles]
```

## When Signal Data Is Sparse

If Common Room returns minimal data on the target (e.g., just name, title, tags — no activity, no scores, no Spark):

1. **Do not draft outreach from thin air.** Outreach grounded in fabricated signals is worse than no outreach.
2. **Run web search first** — this becomes your primary personalization source. Look for recent news, LinkedIn posts, conference talks, company announcements.
3. **If web search also returns little**, present what you have honestly and ask the user for context:

```
## Outreach for [Name / Company] — Limited Data

**What I found:**
[Only the real data from CR and web search]

**I don't have enough signal to draft personalized outreach yet.** To write something strong, I'd need:
- Recent activity or engagement signals
- Context you have from prior conversations
- A specific reason for reaching out now

Can you share any of the above?
```

## Quality Standards

- Every message must reference something specific — generic outreach is not acceptable output
- Match tone to context: warm and conversational for inbound/community signals; more formal for cold/executive outreach
- The LinkedIn message must be under 300 characters — no exceptions
- The call script must be speakable naturally — read it aloud mentally to check rhythm
- **Never fabricate signals** — only reference data retrieved from Common Room or web search

## Reference Files

- **`references/outreach-formats-guide.md`** — detailed format rules, examples, and tone guidelines for each channel

## Examples

### Example 1: Typical request

**User says:** "I need help with common room compose outreach"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |
