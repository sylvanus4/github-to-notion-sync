# tossctl Read-Only Command Reference

## Command Tree

```
tossctl
├── account
│   ├── list          [--output text|json]
│   └── summary       [--output text|json]
├── portfolio
│   ├── positions     [--output text|json]
│   └── allocation    [--output text|json]
├── quote
│   ├── get <symbol>  [--output text|json]
│   └── batch <sym…>  [--output text|json]
├── orders
│   ├── list          [--output text|json]
│   └── completed     [--market us|kr] [--output text|json]
├── watchlist
│   └── list          [--output text|json]
└── export
    ├── positions     [--output json]
    └── orders        [--market us|kr]
```

## Symbol Formats

| Market | Format | Example |
|--------|--------|---------|
| US (NASDAQ/NYSE) | Ticker symbol | `AAPL`, `MSFT`, `TSLA` |
| Korean (KRX) | 6-digit numeric code | `005930` (Samsung), `000660` (SK Hynix) |

## Output Modes

| Flag | Format | Best For |
|------|--------|----------|
| (none) | Human-readable table | Terminal display |
| `--output json` | Structured JSON | Programmatic parsing, pipeline integration |

## Market-Specific Flags

The `--market` flag on `orders completed` and `export orders`:

| Value | Scope |
|-------|-------|
| (none) | All markets |
| `us` | US market only |
| `kr` | Korean market only |

## Common Workflows

### Morning portfolio check

```bash
tossctl account summary --output json
tossctl portfolio positions --output json
tossctl orders list --output json
```

### Daily snapshot export

```bash
DATE=$(date +%Y-%m-%d)
tossctl export positions > "outputs/toss/positions-${DATE}.csv"
tossctl export orders --market us > "outputs/toss/us-orders-${DATE}.csv"
tossctl export orders --market kr > "outputs/toss/kr-orders-${DATE}.csv"
```

### Watchlist price check

```bash
SYMBOLS=$(tossctl watchlist list --output json | jq -r '.[].symbol' | tr '\n' ' ')
tossctl quote batch $SYMBOLS --output json
```
