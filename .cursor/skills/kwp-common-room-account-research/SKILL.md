---
name: kwp-common-room-account-research
description: >-
  Research a company using Common Room data. Triggers on 'research [company]',
  'tell me about [domain]', 'pull up signals for [account]', 'what's going on
  with [company]', or any account-level question. Do NOT use for tasks outside
  the common-room domain. Korean triggers: "리서치", "검색", "데이터".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Account Research

Retrieve and synthesize account information from Common Room. Handles four interaction patterns: full overviews, targeted field questions, sparse data situations, and combined MCP data + LLM reasoning.

## Step 0: Load User Context (Me)

Before researching any account, fetch the `Me` object from Common Room. This provides:
- The user's profile, title, role, and Persona in CR
- The user's segments ("My Segments")

Default all queries to the user's own segments unless the user explicitly asks for a broader view. This keeps results scoped to their territory.

## Step 1: Identify the Interaction Pattern

Determine what the user actually needs before deciding how much data to fetch:

**Pattern 1 — Full Overview:** "Tell me about Datadog" / "Summarize cloudflare.com"
→ Fetch the full field set and produce a structured briefing.

**Pattern 2 — Targeted Question:** "Who owns the Snowflake account?" / "Is acme.io showing buying signals?" / "What's the employee count for notion.so?"
→ Fetch only the relevant field(s). Return a direct, concise answer — do not produce a full brief for a simple question.

**Pattern 3 — Sparse Data:** "Tell me about tiny-startup.io"
→ If Common Room has limited data for an account, say so honestly: "There is limited information available for this account." Never speculate or fill gaps with generic statements.

**Pattern 4 — Combined Reasoning:** Fetch structured MCP data, then layer in LLM analysis — e.g., "Stripe has 8,000 employees and is hiring heavily for AI roles. Based on your ICP of 1k–10k fintech companies, this is a strong fit."

## Step 2: Look Up the Account

Search Common Room for the account by domain or company name. Exact match first; if no result, try partial match and confirm with the user before proceeding.

## Step 3: Fetch the Right Fields

Use the Common Room object catalog to see available field groups and their contents. For full overviews, request all field groups. For targeted questions, request only what's relevant.

**Key field groups to know about:**
- **Scores** — always return as raw values or percentiles, never labels
- **Summary research** — RoomieAI output; often the richest qualitative signal
- **Top contacts** — sorted by score desc; use communityMemberID for full lookups

**Choosing what to fetch:**

| User query type | Fields to request |
|-----------------|------------------|
| Full account overview | All field groups |
| "Who owns this account?" | Company profiles & links, CRM fields |
| "Is this company a good fit?" | Key fields, scores, about |
| "What signals is this account showing?" | Scores, summary research, CRM fields |
| "Who are the top contacts?" | Top contacts |
| "What does RoomieAI say about them?" | Summary research, all research |
| "Find engineers at this account" | Prospects (with title filter) |

## Step 4: Web Search (Sparse Data Only)

Common Room is the primary data source. Do not run web search when CR returns rich data.

When CR data is sparse (Pattern 3 — few fields returned, no activity, no scores), run a targeted web search to fill gaps:
- `"[company name]" news` — scoped to the last 30 days
- Look for: funding rounds, acquisitions, product launches, executive changes, press coverage

If the user explicitly asks for external context or recent news, run web search regardless of data richness.

## Step 5: Apply Reasoning (Pattern 4)

When the user's question invites synthesis — not just data retrieval — layer in analysis:
- Compare account data to known ICP criteria from session context
- Identify fit signals (size, industry, tech stack, hiring patterns)
- Note timing signals (funding, trial status, recent activity spike)
- Frame insights as clearly derived from data, not assumed

When the user's company context is available (see `references/my-company-context.md`), position findings relative to the user's value proposition and ICP.

## Step 6: Produce Output

Only include sections where Common Room returned actual data. Omit sections entirely rather than filling them with guesses.

**Full overview (when data is rich):**

```
## [Company Name] — Account Overview

**Snapshot**
[2–3 sentences: what they do, plan/stage, relationship status]

**Key Details**
[Employee count, industry, location, domain, funding — from key fields]

**CRM & Ownership** [If CRM fields returned]
[Owner, opp stage, ARR]

**Scores** [If scores returned]
[All available scores as raw values or percentiles]

**Signal Highlights** [If activity/signals exist]
[3–5 most important signals with dates]

**Top Contacts** [If contacts returned]
[Name | Title | Score — top 5 sorted by score desc]

**RoomieAI Research** [If summary research is non-null]
[Summary research output; list all available research topic names]

**Recommended Next Steps**
[2–3 specific, signal-backed actions]
```

**Targeted question:** 1–3 sentence direct answer. No full brief needed.

**Sparse data (few fields returned, most sections would be empty):**

```
## [Company Name] — Account Overview (Limited Data)

**Data available:** [List exactly what Common Room returned]

[Present only the returned fields]

**Web Search**
[Findings from web search — or "No significant recent news found"]

**Note:** Common Room has limited data on this account. The account may need enrichment in Common Room.
```

## Quality Standards

- Scores must always be raw values or percentiles — never categorical labels
- For targeted questions, answer precisely and don't over-deliver
- Be explicit when data is missing or stale — don't speculate
- Keep full briefings readable in 2–3 minutes
- **Every fact must trace to a tool call** — don't include data not returned by Common Room

## Reference Files

- **`references/signals-guide.md`** — signal type taxonomy and interpretation guide

## Examples

### Example 1: Typical request

**User says:** "I need help with common room account research"

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