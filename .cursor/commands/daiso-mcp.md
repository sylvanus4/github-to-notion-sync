## Daiso MCP

Search stores, check product inventory, and look up movie seats across Daiso, Olive Young, and Megabox via the daiso-mcp MCP server (`https://mcp.aka.page`).

### Usage

```
/daiso-mcp <query>
/daiso-mcp                    # interactive — describe what you need
```

### Supported Services

| Service | Capabilities |
|---------|-------------|
| **Daiso** | Product search, store finder, inventory check, price lookup |
| **Olive Young** | Nearby store search, product inventory check |
| **Megabox** | Theater finder, movie listings, seat availability |

### Workflow

1. **Parse intent** — Determine service (Daiso / Olive Young / Megabox) and action (search / find / check)
2. **Call MCP tool** — Use the appropriate `daiso-mcp` server tool with extracted parameters
3. **Present results** — Format in structured Korean output (tables, lists)
4. **Offer follow-up** — Suggest logical next actions (inventory check, seat lookup, etc.)

### Execution

Read and follow the `daiso-mcp` skill (`.cursor/skills/daiso-mcp/SKILL.md`) for tool tables, common patterns, REST API fallback, and error handling.

### Examples

Product search and inventory:
```
/daiso-mcp 수납박스 강남역 근처 재고 확인
```

Nearby stores:
```
/daiso-mcp 올리브영 선크림 재고
```

Movie showtimes:
```
/daiso-mcp 메가박스 코엑스 오늘 영화 목록
```

Seat availability:
```
/daiso-mcp 메가박스 강남점 잔여 좌석
```
