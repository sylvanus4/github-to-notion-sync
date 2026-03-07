# Daiso MCP Tool Reference

MCP Server: `daiso-mcp` | URL: `https://mcp.aka.page` | Transport: SSE

## Caching

All responses are cached at Cloudflare's edge:

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| Store locations | 24 hours | Stores rarely change |
| Product catalog | 24 hours | Catalog updates infrequently |
| Inventory / stock | 10 minutes | Balance freshness vs. load |
| Movie seats | 3 minutes | Near-real-time for booking decisions |

---

## Daiso Tools

### `daiso_search_products`

Search Daiso products by keyword.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | -- | Search keyword (Korean or English) |
| `page` | number | No | 1 | Page number for pagination |
| `pageSize` | number | No | 30 | Results per page |

Example:
```json
{
  "query": "수납박스",
  "page": 1,
  "pageSize": 10
}
```

### `daiso_find_stores`

Find Daiso stores by keyword or administrative region.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyword` | string | Conditional | -- | Store name or area keyword. Required if `sido` is not provided |
| `sido` | string | Conditional | -- | Province/city code (시/도). Required if `keyword` is not provided |
| `gugun` | string | No | -- | District (구/군) |
| `dong` | string | No | -- | Neighborhood (동) |
| `limit` | number | No | 50 | Max results |

Example (keyword):
```json
{
  "keyword": "강남"
}
```

Example (region):
```json
{
  "sido": "서울",
  "gugun": "강남구"
}
```

### `daiso_check_inventory`

Check store-level stock status for a specific product.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `productId` | string | Yes | -- | Product ID from `daiso_search_products` |
| `storeQuery` | string | No | -- | Filter stores by name/area keyword |
| `latitude` | number | No | 37.5665 | Latitude for proximity sorting |
| `longitude` | number | No | 126.978 | Longitude for proximity sorting |
| `page` | number | No | 1 | Page number |
| `pageSize` | number | No | 30 | Results per page |

Example:
```json
{
  "productId": "1234567",
  "storeQuery": "강남",
  "latitude": 37.4979,
  "longitude": 127.0276
}
```

### `daiso_get_price_info`

Get price details for a Daiso product.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `productId` | string | Conditional | -- | Product ID. Required if `productName` is not provided |
| `productName` | string | Conditional | -- | Product name for search. Required if `productId` is not provided |

Example:
```json
{
  "productId": "1234567"
}
```

---

## Olive Young Tools

### `oliveyoung_find_nearby_stores`

Find Olive Young stores near a location.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `latitude` | number | No | 37.5665 | Center latitude |
| `longitude` | number | No | 126.978 | Center longitude |
| `keyword` | string | No | -- | Store name or area keyword |
| `pageIdx` | number | No | 1 | Page index |
| `limit` | number | No | 20 | Max results |
| `timeoutMs` | number | No | 15000 | Request timeout in ms (Zyte API can be slow) |

Example:
```json
{
  "latitude": 37.4979,
  "longitude": 127.0276,
  "keyword": "강남",
  "limit": 5
}
```

### `oliveyoung_check_inventory`

Check Olive Young product inventory at nearby stores.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyword` | string | Yes | -- | Product search keyword |
| `latitude` | number | No | 37.5665 | Center latitude |
| `longitude` | number | No | 126.978 | Center longitude |
| `storeKeyword` | string | No | -- | Filter stores by keyword |
| `page` | number | No | 1 | Page number |
| `size` | number | No | 20 | Results per page |
| `sort` | string | No | "01" | Sort order |
| `includeSoldOut` | boolean | No | false | Include sold-out products |
| `storeLimit` | number | No | 10 | Max stores to check per product |
| `timeoutMs` | number | No | 15000 | Request timeout in ms |

Example:
```json
{
  "keyword": "선크림",
  "storeKeyword": "강남",
  "latitude": 37.4979,
  "longitude": 127.0276
}
```

---

## Megabox Tools

### `megabox_find_nearby_theaters`

Find Megabox theaters near a location.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `latitude` | number | No | 37.5665 | Center latitude |
| `longitude` | number | No | 126.978 | Center longitude |
| `playDate` | string | No | today | Date in YYYYMMDD format |
| `areaCode` | string | No | "11" | Area code (11 = Seoul) |
| `limit` | number | No | 10 | Max results |
| `timeoutMs` | number | No | 15000 | Request timeout in ms |

Example:
```json
{
  "latitude": 37.5116,
  "longitude": 127.0590,
  "playDate": "20260304"
}
```

### `megabox_list_now_showing`

List movies currently showing, optionally filtered by theater or movie.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `playDate` | string | No | today | Date in YYYYMMDD format |
| `theaterId` | string | No | -- | Theater ID from `megabox_find_nearby_theaters` |
| `movieId` | string | No | -- | Filter by specific movie |
| `areaCode` | string | No | -- | Area code for regional filtering |
| `timeoutMs` | number | No | 15000 | Request timeout in ms |

Example:
```json
{
  "playDate": "20260304",
  "theaterId": "0001"
}
```

### `megabox_get_remaining_seats`

Check remaining seats for movie showtimes.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `playDate` | string | No | today | Date in YYYYMMDD format |
| `theaterId` | string | No | -- | Theater ID |
| `movieId` | string | No | -- | Movie ID from `megabox_list_now_showing` |
| `areaCode` | string | No | -- | Area code |
| `limit` | number | No | 50 | Max results |
| `timeoutMs` | number | No | 15000 | Request timeout in ms |

Example:
```json
{
  "playDate": "20260304",
  "theaterId": "0001",
  "movieId": "24001234"
}
```
