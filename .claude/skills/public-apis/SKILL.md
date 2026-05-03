---
name: public-apis
description: >-
  Search and discover 1,400+ free public APIs across 50+ categories (weather,
  finance, AI/ML, games, government data, cryptocurrency, etc.) via the
  public-apis MCP server. Use when the user asks to "find an API", "search for
  free APIs", "list weather APIs", "public API for X", "free API", "API 추천",
  "무료 API", "API 검색", or any API discovery/lookup task. Do NOT use for calling
  the discovered APIs directly, building MCP servers, or non-API-related
  searches.
disable-model-invocation: true
---

# Public APIs: Free API Discovery & Recommendation

Search, filter, and discover 1,400+ free public APIs across 50+ categories. Get project-based recommendations, generate integration code, and find alternatives -- all via a single MCP server.

## Prerequisites

The `public-apis` MCP server must be registered. Add to your MCP config (`~/.cursor/mcp.json` or Cursor Settings > MCP):

```json
{
  "mcpServers": {
    "public-apis": {
      "command": "npx",
      "args": ["-y", "@weilei_kyle/public-apis-mcp"],
      "env": {}
    }
  }
}
```

No API keys required. The server syncs data from the [public-apis/public-apis](https://github.com/public-apis/public-apis) GitHub repository on first use.

## Available Tools

### Search & Discovery -- 5 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `search_apis_by_category` | Search APIs within a specific category | `category` (required), `limit` (default: 10) |
| `search_apis_by_keyword` | Full-text keyword search across all APIs | `keyword` (required), `limit` (default: 10) |
| `get_api_details` | Get detailed info for a specific API by name | `apiName` (required) |
| `get_category_list` | List all available API categories | -- |
| `get_random_api` | Get a random API, optionally within a category | `category` (optional) |

### Filtering -- 3 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `filter_apis_by_auth` | Filter by authentication type | `authType` (required: `No`, `apiKey`, `OAuth`, `X-Mashape-Key`, `User-Agent`), `limit` |
| `filter_apis_by_https` | Filter APIs by HTTPS support | `httpsOnly` (default: true), `limit` |
| `filter_apis_by_cors` | Filter APIs by CORS support | `corsSupport` (required: `yes`, `no`, `unknown`), `limit` |

### Analytics -- 2 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_api_statistics` | Get total counts and category breakdown | -- |
| `analyze_auth_requirements` | Distribution of auth types across all APIs | -- |

### Recommendation & Matching -- 2 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `recommend_apis_for_project` | Recommend APIs based on project description | `projectType` (required), `requirements` (string array), `limit` (default: 5) |
| `find_alternative_apis` | Find APIs matching a functionality description | `functionality` (required), `limit` (default: 5) |

### Code Generation -- 1 tool

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `generate_api_integration_code` | Generate integration code for an API | `apiName` (required), `language` (`javascript`, `python`, `curl`; default: `javascript`) |

### Data Sync -- 2 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `sync_repository_data` | Sync latest API data from GitHub | `force` (default: false) |
| `check_new_apis` | Check recently added APIs | `days` (default: 7) |

For the full category list, see [references/categories.md](references/categories.md).

## Workflow

### Step 1: Identify User Intent

Parse the user's request into one of these categories:

| Intent | Primary Tool | Follow-up Tool |
|--------|-------------|----------------|
| Category browsing | `search_apis_by_category` | `get_api_details` |
| Keyword search | `search_apis_by_keyword` | `get_api_details` |
| Filtered search (auth/HTTPS/CORS) | `filter_apis_by_*` | `get_api_details` |
| Project recommendation | `recommend_apis_for_project` | `generate_api_integration_code` |
| Find alternatives | `find_alternative_apis` | `generate_api_integration_code` |
| Random discovery | `get_random_api` | `get_api_details` |
| Statistics overview | `get_api_statistics` | `analyze_auth_requirements` |
| Code example | `generate_api_integration_code` | -- |

### Step 2: Call the MCP Tool

Use `CallMcpTool` with server `public-apis` and the appropriate tool name:

```
Server: public-apis
Tool: <tool_name>
Arguments: { ... }
```

### Step 3: Present Results

Format results in a structured table:

| Column | Description |
|--------|-------------|
| **API** | Name with link to documentation |
| **Description** | What the API provides |
| **Auth** | Authentication requirement (No / apiKey / OAuth) |
| **HTTPS** | Whether HTTPS is supported |
| **CORS** | Cross-origin support status |

### Step 4: Offer Follow-up Actions

After presenting results, suggest logical next steps:

- Search results → "Want integration code for any of these?" (`generate_api_integration_code`)
- Category browse → "Want to filter by auth type?" (`filter_apis_by_auth`)
- Recommendation → "Want to see alternatives?" (`find_alternative_apis`)
- Any result → "Want details on a specific API?" (`get_api_details`)

## Examples

### Example 1: Category Browsing

User says: "Show me weather APIs"

Actions:
1. `search_apis_by_category` with `category: "Weather"`, `limit: 20`
2. Present results in table format (name, description, auth, HTTPS, CORS)
3. Offer follow-up: "Want integration code for any of these?"

Result: Table of 20+ weather APIs including OpenWeatherMap, WeatherAPI, Open-Meteo, etc.

### Example 2: Keyword Search with Code Generation

User says: "Find APIs for image recognition and show me Python code"

Actions:
1. `search_apis_by_keyword` with `keyword: "image recognition"`, `limit: 10`
2. Present results table
3. User picks Clarifai → `generate_api_integration_code` with `apiName: "Clarifai"`, `language: "python"`

Result: List of image recognition APIs, then Python integration code for the selected API.

### Example 3: No-Auth Filtered Search

User says: "Free APIs that don't require authentication"

Actions:
1. `filter_apis_by_auth` with `authType: "No"`, `limit: 20`
2. Present results table
3. Offer: "Want to narrow down by category?"

Result: Table of 20 APIs requiring no authentication, with HTTPS/CORS info.

### Example 4: Project-Based Recommendation

User says: "I'm building a weather dashboard app"

Actions:
1. `recommend_apis_for_project` with `projectType: "weather dashboard"`, `requirements: ["weather data", "forecast", "maps"]`
2. Present recommended APIs with reasoning
3. Offer: "Want JavaScript integration code for any of these?"

Result: 5 recommended APIs matched to project requirements with explanation.

### Example 5: Random Discovery

User says: "Surprise me with a random API"

Actions:
1. `get_random_api` (no category filter)
2. Present the API details
3. Offer: "Want another one, or integration code for this?"

Result: One randomly selected API with full details.

## Error Handling

- **MCP connection failure**: Inform the user that the public-apis MCP server is not connected. Suggest checking `~/.cursor/mcp.json` config and restarting Cursor.
- **No results**: Suggest broadening the search (different keyword, related category) or check available categories via `get_category_list`.
- **Unknown category**: Call `get_category_list` first, then suggest the closest matching category.
- **API name not found**: If `get_api_details` fails, use `search_apis_by_keyword` with the API name as keyword to find the correct name.
- **Stale data**: If results seem outdated, suggest `sync_repository_data` with `force: true`.

## MCP Tool Reference

| Tool | Server | Purpose |
|------|--------|---------|
| `search_apis_by_category` | `public-apis` | Search APIs within a category |
| `search_apis_by_keyword` | `public-apis` | Keyword search across all APIs |
| `filter_apis_by_auth` | `public-apis` | Filter by auth requirement |
| `filter_apis_by_https` | `public-apis` | Filter by HTTPS support |
| `filter_apis_by_cors` | `public-apis` | Filter by CORS support |
| `get_api_details` | `public-apis` | Get specific API details |
| `get_category_list` | `public-apis` | List all categories |
| `get_random_api` | `public-apis` | Random API suggestion |
| `get_api_statistics` | `public-apis` | API count statistics |
| `analyze_auth_requirements` | `public-apis` | Auth type distribution |
| `recommend_apis_for_project` | `public-apis` | Project-based recommendation |
| `find_alternative_apis` | `public-apis` | Find alternative APIs |
| `generate_api_integration_code` | `public-apis` | Generate integration code |
| `sync_repository_data` | `public-apis` | Sync data from GitHub |
| `check_new_apis` | `public-apis` | Check recently added APIs |
