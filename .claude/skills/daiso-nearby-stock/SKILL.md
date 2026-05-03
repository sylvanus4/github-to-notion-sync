---
name: daiso-nearby-stock
description: >-
  Search a Daiso product by keyword, find nearby stores, check real-time
  inventory and pricing, and present a consolidated Korean report with visit
  recommendations. Use when the user asks "다이소 재고 확인", "근처 다이소 재고", "다이소 매장
  재고", "다이소에 XX 있어?", "다이소 XX 파는 곳", "다이소 XX 재고 있는 매장", "check Daiso stock
  nearby", or any request combining a Daiso product with location-based
  inventory lookup. Do NOT use for Olive Young, Megabox, or non-Daiso lookups
  (use daiso-mcp directly). Do NOT use for product search without inventory
  intent (use daiso-mcp daiso_search_products).
---

# Daiso Nearby Stock Finder

End-to-end pipeline: product search, nearby store inventory check, price lookup, and consolidated Korean report with visit recommendation. Composes `daiso-mcp` MCP tools.

## Prerequisites

The `user-daiso-mcp` MCP server must be connected. See `daiso-mcp` skill for setup.

## Inputs

Extract two pieces from the user's request:

| Input | Required | Example | Fallback |
|-------|----------|---------|----------|
| **Product keyword** | Yes | "골프공", "수납박스", "건전지" | -- |
| **Location** | Yes | "잠실", "강남역", "홍대" | Seoul City Hall (37.5665, 126.978) |

If the user provides a well-known landmark or apartment complex, resolve it to a `storeQuery` keyword and approximate coordinates.

### Common Seoul Landmark Coordinates

| Landmark | storeQuery | lat | lng |
|----------|------------|-----|-----|
| 잠실 아시아선수촌 | 잠실 | 37.5170 | 127.0728 |
| 강남역 | 강남 | 37.4980 | 127.0276 |
| 홍대입구역 | 홍대 | 37.5571 | 126.9246 |
| 서울역 | 서울역 | 37.5547 | 126.9707 |
| 여의도 | 여의도 | 37.5219 | 126.9245 |

For unlisted locations, use WebSearch or the user-provided address to estimate coordinates.

## Workflow

### Step 1: Search Products

```
Server: user-daiso-mcp
Tool:   daiso_search_products
Args:   { "query": "<product keyword>" }
```

From the results, **filter** to keep only relevant products:
- Exclude accessories (pouches, massagers, markers, towels, cases) unless the user asked for them
- Note `soldOut` status -- skip online-soldOut items unless `pickupAvailable: true`
- If more than **5 candidates** remain after filtering, keep only the **top 5** by relevance (prefer exact keyword matches, popular brands, and varied price points)
- Collect `productId` for each candidate

**CRITICAL:** If zero candidates remain after filtering, STOP. Inform the user and suggest broader keywords (see Error Handling). Do NOT proceed to Step 2 with an empty product list.

### Step 2: Check Inventory + Get Prices (parallel)

For each candidate `productId`, call **both** tools in parallel:

**Inventory check:**
```
Server: user-daiso-mcp
Tool:   daiso_check_inventory
Args:   {
  "productId": "<id>",
  "storeQuery": "<location keyword>",
  "latitude": <lat>,
  "longitude": <lng>
}
```

**Price lookup:**
```
Server: user-daiso-mcp
Tool:   daiso_get_price_info
Args:   { "productId": "<id>" }
```

Parallelize across products AND across the two tool types to minimize latency.

From the inventory results, **filter stores by distance**: keep only stores within **5km** of the user's location. If no stores are within 5km, expand to 10km and note the wider radius. Discard stores beyond 10km entirely.

### Step 3: Present Results

Format output in Korean with three sections:

**1) Nearby Stores Table**

| 매장명 | 주소 | 거리 | 영업시간 | 주차 |
|--------|------|------|----------|------|

**2) Product Inventory Matrix**

| 제품명 | 가격 | 매장A (거리) | 매장B (거리) | ... |
|--------|------|:-:|:-:|:-:|

Use **bold** for in-stock quantities. Show "재고 없음" for zero stock. Never silently omit zero-stock products — always display them with the "재고 없음" label so the user knows they were checked.

**3) Visit Recommendation**

Recommend the best store based on:
1. Highest variety of in-stock products
2. Closest distance to the user's location
3. Mention parking availability if relevant

Include a numbered list of top product picks with brief descriptions. **MUST** include per-unit price calculations for multi-pack products (e.g., "10개에 5,000원 → 개당 500원", "16개입 3,000원 → 개당 약 188원"). For single items, compare value across similar products (e.g., "3구 허브 3,000원 vs 4구 허브 5,000원 — 포트당 가격 비슷").

## Error Handling

| Scenario | Action |
|----------|--------|
| No products found | Suggest broader keywords (e.g., "공" instead of "골프공") |
| No stores found for location | Call `daiso_find_stores({ "storeQuery": "<broader area>" })` with a wider keyword (e.g., "송파" instead of "잠실"), then retry inventory with discovered stores |
| All inventory zero | Report honestly; suggest checking adjacent neighborhoods |
| MCP timeout | Retry once; if still failing, use REST fallback (see daiso-mcp skill) |

## Examples

### Example 1: 특정 지역 재고 확인

**User:** "잠실 아시아선수촌 근처 다이소에 골프공 재고 확인해줘"

**Step 1:** `daiso_search_products({ "query": "골프공" })` → 5 golf ball products (accessories filtered out)

**Step 2 (parallel):**
- `daiso_check_inventory({ "productId": "1027700", "storeQuery": "잠실", ... })` → 22 in stock at 잠실종합운동장역점
- `daiso_get_price_info({ "productId": "1027700" })` → 5,000원
- _(repeat for each product)_

**Step 3:** Nearby stores table + inventory matrix + recommend 잠실종합운동장역점 (0.8km, 3 types in stock)

### Example 2: 재고 없는 경우

**User:** "홍대 다이소에 USB 허브 있어?"

**Step 1:** `daiso_search_products({ "query": "USB 허브" })` → 2 products found

**Step 2:** `daiso_check_inventory(...)` → all stores show 0 stock

**Step 3:** Report "재고 없음" honestly, suggest checking 신촌/마포 인근 매장
