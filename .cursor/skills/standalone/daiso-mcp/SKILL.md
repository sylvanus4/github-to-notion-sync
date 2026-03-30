---
name: daiso-mcp
description: >-
  Search stores, check product inventory, and look up movie seats across Daiso,
  Olive Young, and Megabox via the daiso-mcp MCP server. Use when the user asks
  to "find a Daiso store", "check Olive Young inventory", "search Daiso
  products", "Megabox movie seats", "근처 다이소", "올리브영 재고", "메가박스 영화", or any
  Korean retail store/inventory/movie lookup. Do NOT use for non-Korean retail
  services, general web scraping, or e-commerce purchasing.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Daiso MCP: Korean Retail & Movie Lookup

Search products, find nearby stores, check real-time inventory (Daiso, Olive Young), and browse movie showtimes with seat availability (Megabox) -- all via a single remote MCP server.

## Prerequisites

The `daiso-mcp` MCP server must be registered. Add to your MCP config (`.cursor/mcp.json` or Cursor Settings > MCP):

```json
{
  "mcpServers": {
    "daiso-mcp": {
      "url": "https://mcp.aka.page",
      "transport": "sse"
    }
  }
}
```

No API keys are required for the public server. All tools are available immediately after connection.

## Available Tools

### Daiso (다이소) -- 4 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `daiso_search_products` | Search Daiso products by keyword | `query` (required), `page`, `pageSize` |
| `daiso_find_stores` | Find Daiso stores by location or keyword | `keyword` or `sido` (one required), `gugun`, `dong`, `limit` |
| `daiso_check_inventory` | Check store-level stock for a product | `productId` (required), `storeQuery`, `latitude`, `longitude` |
| `daiso_get_price_info` | Get product price details | `productId` or `productName` (one required) |

### Olive Young (올리브영) -- 2 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `oliveyoung_find_nearby_stores` | Find nearby Olive Young stores | `latitude`, `longitude`, `keyword`, `limit` |
| `oliveyoung_check_inventory` | Check product inventory at nearby stores | `keyword` (required), `latitude`, `longitude`, `storeKeyword` |

### Megabox (메가박스) -- 3 tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `megabox_find_nearby_theaters` | Find nearby Megabox theaters | `latitude`, `longitude`, `playDate`, `areaCode`, `limit` |
| `megabox_list_now_showing` | List currently showing movies | `playDate`, `theaterId`, `movieId`, `areaCode` |
| `megabox_get_remaining_seats` | Check remaining seats per showtime | `playDate`, `theaterId`, `movieId`, `limit` |

For full parameter details, types, defaults, and caching behavior, see [references/tool-reference.md](references/tool-reference.md).

## Workflow

### Step 1: Identify User Intent

Parse the user's request into one of these categories:

| Intent | Service | Primary Tool | Follow-up Tool |
|--------|---------|-------------|----------------|
| Product search | Daiso | `daiso_search_products` | `daiso_get_price_info` |
| Store finder | Daiso / Olive Young | `daiso_find_stores` or `oliveyoung_find_nearby_stores` | -- |
| Inventory check | Daiso / Olive Young | `daiso_check_inventory` or `oliveyoung_check_inventory` | -- |
| Movie listings | Megabox | `megabox_list_now_showing` | `megabox_get_remaining_seats` |
| Theater finder | Megabox | `megabox_find_nearby_theaters` | `megabox_list_now_showing` |

### Step 2: Call the MCP Tool

Use `CallMcpTool` with server `daiso-mcp` and the appropriate tool name:

```
Server: daiso-mcp
Tool: <tool_name>
Arguments: { ... }
```

Default coordinates (Seoul City Hall) are used when the user does not specify a location:
- `latitude`: 37.5665
- `longitude`: 126.978

### Step 3: Present Results

Format results clearly in Korean:

- **Product search**: Table with product name, price, product ID
- **Store finder**: List with store name, address, distance
- **Inventory check**: Table with store name, stock status, distance
- **Movie listings**: Table with movie title, showtime, screen, format
- **Seat availability**: Table with movie, showtime, total/remaining seats

### Step 4: Offer Follow-up Actions

After presenting results, suggest logical next steps:

- Product search → "재고를 확인할까요?" (check inventory)
- Store finder → "이 매장의 재고를 확인할까요?" (check inventory at this store)
- Movie listings → "잔여 좌석을 확인할까요?" (check remaining seats)

## Common Patterns

### Pattern 1: Product Search → Inventory Check (Daiso)

User: "수납박스 강남역 근처 재고 확인"

1. `daiso_search_products` with `query: "수납박스"` to get `productId`
2. `daiso_check_inventory` with the `productId` and `storeQuery: "강남"`

### Pattern 2: Nearby Store Search (Olive Young)

User: "올리브영 선크림 재고"

1. `oliveyoung_check_inventory` with `keyword: "선크림"` (handles store lookup internally)

### Pattern 3: Movie + Seats (Megabox)

User: "메가박스 코엑스 오늘 영화"

1. `megabox_find_nearby_theaters` to find the Coex theater ID
2. `megabox_list_now_showing` with `theaterId` and today's date
3. If the user picks a movie, `megabox_get_remaining_seats` for seat availability

## REST API Fallback

When MCP transport is unavailable, use HTTP GET endpoints at `https://mcp.aka.page/api/`:

| Endpoint | Purpose |
|----------|---------|
| `/api/daiso/products?q={query}` | Product search |
| `/api/daiso/stores?keyword={keyword}` | Store search |
| `/api/daiso/inventory?productId={id}&lat={lat}&lng={lng}` | Inventory |
| `/api/oliveyoung/stores?keyword={keyword}&lat={lat}&lng={lng}` | Olive Young stores |
| `/api/oliveyoung/inventory?keyword={keyword}&lat={lat}&lng={lng}` | Olive Young inventory |
| `/api/megabox/theaters?lat={lat}&lng={lng}&playDate={date}` | Theaters |
| `/api/megabox/movies?playDate={date}&theaterId={id}` | Movies |
| `/api/megabox/seats?playDate={date}&theaterId={id}` | Seats |

Use `WebFetch` or `Shell` (curl) to call these endpoints.

## Error Handling

- **Timeout**: Olive Young tools may take longer due to Zyte API proxy. If a tool times out, retry with a higher `timeoutMs` value (default: 15000ms).
- **No results**: Inform the user and suggest broadening the search (different keyword, wider area).
- **MCP connection failure**: Fall back to the REST API endpoints listed above.
- **Invalid productId**: Re-run the product search to obtain a valid ID before checking inventory.

## MCP Tool Reference

| Tool | Server | Purpose |
|------|--------|---------|
| `daiso_search_products` | `daiso-mcp` | Search Daiso products by keyword |
| `daiso_find_stores` | `daiso-mcp` | Find Daiso stores by location |
| `daiso_check_inventory` | `daiso-mcp` | Check Daiso product stock at stores |
| `daiso_get_price_info` | `daiso-mcp` | Get Daiso product pricing |
| `oliveyoung_find_nearby_stores` | `daiso-mcp` | Find nearby Olive Young stores |
| `oliveyoung_check_inventory` | `daiso-mcp` | Check Olive Young product stock |
| `megabox_find_nearby_theaters` | `daiso-mcp` | Find nearby Megabox theaters |
| `megabox_list_now_showing` | `daiso-mcp` | List currently showing movies |
| `megabox_get_remaining_seats` | `daiso-mcp` | Check seat availability |

## Examples

### Example 1: Standard usage
**User says:** "daiso mcp" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.
