---
name: kwp-enterprise-search-source-management
description: >-
  Manages connected MCP sources for enterprise search. Detects available
  sources, guides users to connect new ones, handles source priority ordering,
  and manages rate limiting awareness. Do NOT use for tasks outside the
  enterprise-search domain. Korean triggers: "검색".
---

# Source Management


Knows what sources are available, helps connect new ones, and manages how sources are queried.

## Checking Available Sources

Determine which MCP sources are connected by checking available tools. Each source corresponds to a set of MCP tools:

| Source | Key capabilities |
|--------|-----------------|
| **Slack** | Search messages, read channels and threads |
| **Gmail** | Search messages, read individual emails |
| **Google Drive** | Search files, fetch document contents |
| **Linear** | Search tasks, typeahead search |
| **HubSpot** | Query records (accounts, contacts, opportunities) |
| **Notion** | Semantic search, keyword search |

If a tool prefix is available, the source is connected and searchable.

## Guiding Users to Connect Sources

When a user searches but has few or no sources connected:

```
You currently have [N] source(s) connected: [list].

To expand your search, you can connect additional sources in your MCP settings:
- Slack — messages, threads, channels
- Gmail — emails, conversations, attachments
- Google Drive — docs, sheets, slides
- Linear — tasks, projects, milestones
- HubSpot — accounts, contacts, opportunities
- Notion — wiki pages, knowledge base articles

The more sources you connect, the more complete your search results.
```

When a user asks about a specific tool that is not connected:

```
[Tool name] isn't currently connected. To add it:
1. Open your MCP settings
2. Add the [tool] MCP server configuration
3. Authenticate when prompted

Once connected, it will be automatically included in future searches.
```

## Source Priority Ordering

Different query types benefit from searching certain sources first. Use these priorities to weight results, not to skip sources:

### By Query Type

**Decision queries** ("What did we decide..."):
```
1. Slack (conversations where decisions happen)
2. Gmail (decision confirmations, announcements)
3. Google Drive (meeting notes, decision logs)
4. Wiki (if decisions are documented)
5. Task tracker (if decisions are captured in tasks)
```

**Status queries** ("What's the status of..."):
```
1. Task tracker (Linear — authoritative status)
2. Slack (real-time discussion)
3. Google Drive (status docs, reports)
4. Gmail (status update emails)
5. Wiki (project pages)
```

**Document queries** ("Where's the doc for..."):
```
1. Google Drive (primary doc storage)
2. Wiki / Notion (knowledge base)
3. Gmail (docs shared via email)
4. Slack (docs shared in channels)
5. Task tracker (docs linked to tasks)
```

**People queries** ("Who works on..." / "Who knows about..."):
```
1. Slack (message authors, channel members)
2. Task tracker (task assignees)
3. Google Drive (doc authors, collaborators)
4. HubSpot (account owners, contacts)
5. Gmail (email participants)
```

**Factual/Policy queries** ("What's our policy on..."):
```
1. Wiki / Notion (official documentation)
2. Google Drive (policy docs, handbooks)
3. Gmail (policy announcements)
4. Slack (policy discussions)
```

### Default Priority (General Queries)

When query type is unclear:
```
1. Slack (highest volume, most real-time)
2. Gmail (formal communications)
3. Google Drive (documents and files)
4. Wiki / Notion (structured knowledge)
5. Task tracker (work items)
6. CRM (customer data)
```

## Rate Limiting Awareness

MCP sources may have rate limits. Handle them gracefully:

### Detection

Rate limit responses typically appear as:
- HTTP 429 responses
- Error messages mentioning "rate limit", "too many requests", or "quota exceeded"
- Throttled or delayed responses

### Handling

When a source is rate limited:

1. **Do not retry immediately** — respect the limit
2. **Continue with other sources** — do not block the entire search
3. **Inform the user**:
```
Note: [Source] is temporarily rate limited. Results below are from
[other sources]. You can retry in a few minutes to include [source].
```
4. **For digests** — if rate limited mid-scan, note which time range was covered before the limit hit

### Prevention

- Avoid unnecessary API calls — check if the source is likely to have relevant results before querying
- Use targeted queries over broad scans when possible
- For digests, batch requests where the API supports it
- Cache awareness: if a search was just run, avoid re-running the same query immediately

## Source Health

Track source availability during a session:

```
Source Status:
  Slack:        ✓ Available
  Gmail:        ✓ Available
  Google Drive:  ✓ Available
  Linear:        ✗ Not connected
  HubSpot:   ✗ Not connected
  Notion:      ⚠ Rate limited (retry in 2 min)
```

When reporting search results, include which sources were searched so the user knows the scope of the answer.

## Adding Custom Sources

The enterprise search plugin works with any MCP-connected source. As new MCP servers become available, they can be added to the `.mcp.json` configuration. The search and digest commands will automatically detect and include new sources based on available tools.

To add a new source:
1. Add the MCP server configuration to `.mcp.json`
2. Authenticate if required
3. The source will be included in subsequent searches automatically

## Examples

### Example 1: Typical request

**User says:** "I need help with enterprise search source management"

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
