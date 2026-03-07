## Public APIs

Search and discover 1,400+ free public APIs across 50+ categories (weather, finance, AI/ML, games, government data, etc.) via the public-apis MCP server.

### Usage

```
/public-apis <query>
/public-apis                    # interactive — describe what you need
```

### Capabilities

| Feature | Description |
|---------|-------------|
| **Keyword search** | Search APIs by keyword (e.g., "weather", "machine learning") |
| **Category browsing** | Browse by category (Animals, Finance, Games, etc.) |
| **Filtered search** | Filter by auth type (none, apiKey, OAuth), HTTPS, CORS |
| **Project recommendation** | Describe your project and get API recommendations |
| **Alternative finder** | Find APIs matching a functionality description |
| **Code generation** | Generate integration code (JavaScript, Python, curl) |
| **Random discovery** | Get a random API suggestion |
| **Statistics** | View API counts and auth type distribution |

### Workflow

1. **Parse intent** — Determine action: search, browse, filter, recommend, or generate code
2. **Call MCP tool** — Use the appropriate `public-apis` server tool with extracted parameters
3. **Present results** — Structured table with API name, description, auth, HTTPS, CORS, link
4. **Offer follow-up** — Suggest integration code, alternatives, or narrowing results

### Execution

Read and follow the `public-apis` skill (`.cursor/skills/public-apis/SKILL.md`) for tool tables, common patterns, and error handling.

### Examples

Search by category:
```
/public-apis show me weather APIs
```

Keyword search:
```
/public-apis find free image recognition APIs
```

No-auth filter:
```
/public-apis APIs that don't require authentication
```

Project recommendation:
```
/public-apis I'm building a weather dashboard, recommend APIs
```

Code generation:
```
/public-apis generate Python code for OpenWeatherMap API
```

Random API:
```
/public-apis surprise me with a random API
```

List categories:
```
/public-apis list all categories
```

Statistics:
```
/public-apis how many APIs are available?
```
