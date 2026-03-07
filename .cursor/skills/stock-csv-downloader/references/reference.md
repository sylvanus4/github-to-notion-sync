# Stock CSV Downloader — Reference

## Full Ticker-to-Slug Mapping

### International Stocks

| Ticker | Name | Exchange | investing.com Slug | CSV Filename |
|---|---|---|---|---|
| NVDA | NVIDIA | NASDAQ | `nvidia-corp` | NVIDIA Stock Price History.csv |
| AMZN | Amazon.com | NASDAQ | `amazon-com-inc` | Amazon.com Stock Price History.csv |
| MSFT | Microsoft | NASDAQ | `microsoft-corp` | Microsoft Stock Price History.csv |
| TSLA | Tesla | NASDAQ | `tesla-motors` | Tesla Stock Price History.csv |
| META | Meta Platforms | NASDAQ | `facebook-inc` | Meta Platforms Stock Price History.csv |
| NFLX | Netflix | NASDAQ | `netflix-inc` | Netflix Stock Price History.csv |
| AVGO | Broadcom | NASDAQ | `avago-technologies` | Broadcom Stock Price History.csv |
| PLTR | Palantir | NYSE | `palantir-technologies-inc` | Palantir Stock Price History.csv |
| V | Visa A | NYSE | `visa-inc` | Visa A Stock Price History.csv |
| TSM | Taiwan Semiconductor | TWSE | `taiwan-semicon` | Taiwan Semiconductor Stock Price History.csv |
| HOOD | Robinhood Markets | NASDAQ | `robinhood-markets` | Robinhood Markets Stock Price History.csv |
| BABA | Alibaba ADR | NYSE | `alibaba` | Alibaba ADR Stock Price History.csv |
| GOOGL | Alphabet A | NASDAQ | `google-inc` | Alphabet A Stock Price History.csv |
| AAPL | Apple | NASDAQ | `apple-computer-inc` | Apple Stock Price History.csv |
| BRK.B | Berkshire Hathaway B | NYSE | `berkshire-hathaway` | Berkshire Hathaway B Stock Price History.csv |
| GS | Goldman Sachs | NYSE | `goldman-sachs-group` | Goldman Sachs Stock Price History.csv |
| JPM | JPMorgan | NYSE | `jp-morgan-chase` | JPMorgan Stock Price History.csv |
| CRWV | CoreWeave | NASDAQ | `coreweave` | CoreWeave Stock Price History.csv |

### Domestic Stocks (KRX)

| Ticker | Name | Exchange | investing.com Slug | CSV Filename |
|---|---|---|---|---|
| 005930 | Samsung Electronics | KRX | `samsung-electronics-co-ltd` | Samsung Electronics Co Stock Price History.csv |
| 000660 | SK Hynix | KRX | `sk-hynix-inc` | SK Hynix Stock Price History.csv |
| 005380 | Hyundai Motor | KRX | `hyundai-motor` | Hyundai Motor Stock Price History.csv |
| 006340 | Daewon Cable | KRX | `daewon-cable` | Daewon Cable Stock Price History.csv |
| 032820 | Woori Technology | KOSDAQ | `woori-technology-inc` | Woori Technology Stock Price History.csv |
| 001510 | SK Securities | KRX | `sk-securities` | SK Securities Stock Price History.csv |

## investing.com URL Pattern

Historical data pages follow this pattern:

```
https://www.investing.com/equities/{slug}-historical-data
```

For example:
- NVIDIA: `https://www.investing.com/equities/nvidia-corp-historical-data`
- Samsung: `https://www.investing.com/equities/samsung-electronics-co-ltd-historical-data`

### Finding New Slugs

1. Go to `https://www.investing.com`
2. Search for the stock name
3. Navigate to the "Historical Data" tab
4. The slug is the URL path between `/equities/` and `-historical-data`

## CSV Format

investing.com exports CSVs with these columns:

| Column | Description | Format | Example |
|---|---|---|---|
| Date | Trading date | MM/DD/YYYY (quoted) | "12/30/2025" |
| Price | Closing price | Number (quoted) | "187.55" |
| Open | Opening price | Number (quoted) | "188.24" |
| High | Daily high | Number (quoted) | "188.93" |
| Low | Daily low | Number (quoted) | "186.97" |
| Vol. | Volume | Number with K/M/B suffix (quoted) | "92.54M" |
| Change % | Daily change percentage | Percentage (quoted) | "-0.36%" |

- All values are double-quoted
- Rows are sorted by date descending (newest first)
- The file may have a UTF-8 BOM (byte order mark)
- Volume suffixes: K = thousands, M = millions, B = billions
- Domestic (KRX) stocks use the same format but with KRW prices

## Adding a New Ticker

1. Find the investing.com slug (see "Finding New Slugs" above)
2. Add an entry to `TICKER_SLUG_MAP` in `backend/scripts/download_stock_csv.py`:

```python
"NEW_TICKER": {
    "slug": "company-name-slug",
    "name": "Company Name",
    "csv_name": "Company Name Stock Price History",
    "exchange": "NASDAQ",
},
```

3. If the ticker also needs to work with the bulk loader, add it to `STOCK_MAPPINGS` in `backend/scripts/load_stock_data.py`

## Data Pipeline

```
investing.com (Playwright browser session)
    ↓  Extract instrument_id from __NEXT_DATA__
    ↓  API call: api.investing.com/api/financialdata/historical/{id}
    ↓  JSON response converted to CSV
data/{batch}/*.csv
    ↓  CSVParserService normalizes columns, parses dates/volumes
    ↓  StockPriceService.import_csv() upserts
PostgreSQL: tickers + stock_prices tables
    ↓  API endpoints serve data
Frontend charts and analysis
```

## API Details

The script calls the investing.com internal API:

```
GET https://api.investing.com/api/financialdata/historical/{instrument_id}
    ?start-date=YYYY-MM-DD
    &end-date=YYYY-MM-DD
    &time-frame=Daily
    &add-missing-rows=false
Headers:
    domain-id: www
```

The API requires a valid browser session (cookies/CORS). The script uses Playwright's
`page.evaluate(fetch(...))` to make the request within the browser context.

### Known instrument IDs

| Ticker | instrument_id | Notes |
|---|---|---|
| NVDA | 6497 | NVIDIA Corporation |
| AMZN | 6435 | Amazon.com Inc. |
| MSFT | 252 | Microsoft Corporation |
| TSLA | 13994 | Tesla Inc. |
| META | 26490 | Meta Platforms (slug: facebook-inc) |
| NFLX | 955716 | Netflix Inc. |
| AVGO | 13969 | Broadcom (slug: avago-technologies) |
| PLTR | 1166239 | Palantir Technologies |
| V | 8318 | Visa Inc. |
| TSM | 103240 | Taiwan Semiconductor (TWSE, TWD prices) |
| HOOD | 1175355 | Robinhood Markets |
| BABA | 941155 | Alibaba Group (ADR) |
| GOOGL | 6369 | Alphabet Inc. (slug: google-inc) |
| AAPL | 6408 | Apple Inc. |
| BRK.B | 13834 | Berkshire Hathaway B |
| GS | 266 | Goldman Sachs Group |
| JPM | 267 | JPMorgan Chase |
| CRWV | 1228090 | CoreWeave Inc. |
| 005930 | 43433 | Samsung Electronics |
| 000660 | 43430 | SK Hynix Inc. |
| 005380 | 43399 | Hyundai Motor Co. |
| 012450 | 43356 | Hanwha Aerospace (slug: samsung-techwin) |
| 017670 | 43472 | SK Telecom (slug: sk-telecom-co-ltd) |
| 034020 | 43544 | Doosan Enerbility (slug: doosan-heavy-ind.---const.) |
| 035420 | 43493 | NAVER (slug: nhn-corp) |
| 042700 | — | Hanmi Semiconductor (slug: hanmi-semicon) |
| 047810 | 43962 | Korea Aerospace Industries (slug: korea-aerospac) |
| 068270 | — | Celltrion (slug: celltrion-inc) |
| 207940 | — | Samsung Biologics (slug: samsung-biologics-co-ltd) |
| 267260 | 1010642 | HD Hyundai Electric (slug: hyundai-electric-energy-systems) |
| 272210 | — | Hanwha Systems (slug: hanwha-systems-co-ltd) |
| 326030 | — | SK Biopharmaceuticals (slug: sk-biopharmaceuticals-co-ltd) |
| 006340 | — | Daewon Cable (slug: daewon-cable) |
| 032820 | — | Woori Technology (slug: woori-technology-inc) |
| 001510 | — | SK Securities (slug: sk-securities) |
| EQIX | 13067 | Equinix (slug: equinix,-inc.) |

IDs are auto-discovered from the page's `__NEXT_DATA__` JSON.

## Gap Detection Algorithm

The `--gap-fill` mode works as follows:

1. **Query DB**: For each ticker, fetch all existing dates from `stock_prices` where `date >= gap-fill-from` (default 2021-01-01)
2. **Generate expected days**: Create a set of all weekdays (Mon–Fri) from `gap-fill-from` to today
3. **Compute missing**: `missing = expected_weekdays - existing_dates`
4. **Group into ranges**: Contiguous missing days are merged into `(start, end)` ranges (gap tolerance of 3 days to handle weekends)
5. **Filter small gaps**: Gaps with fewer than 5 missing weekdays are treated as market holidays and skipped. This prevents unnecessary API calls for tickers that are already at ~96% coverage.
6. **Chunk by year**: Remaining significant gaps are split into 1-year maximum chunks for the API
7. **Download only significant gaps**: The script fetches data only for ranges with real missing data

### Smart Holiday Filtering

US markets have ~10 holidays/year, Korean markets ~15. Since the algorithm uses a weekday check (Mon–Fri) without a holiday calendar, tickers with full coverage show ~52 "missing" days across 5 years. The 5-weekday minimum gap filter ensures these holiday gaps are skipped, while real gaps (e.g., a new ticker with no historical data) are still detected.

### Limitations

- **New tickers**: If a ticker has no data in the DB at all, the entire range from `gap-fill-from` to today is treated as one gap (which is correct behavior).
- **Pre-IPO gaps**: For tickers that started trading after `gap-fill-from` (e.g., CRWV IPO'd March 2025), the script will try to download pre-IPO ranges but the API will return empty data — this is harmless.
- **API limit**: Each API request is capped at 1 year to avoid timeouts.

## Status Output Format

The `--status` flag displays a table like:

```
Ticker     First Date   Last Date    Records  Missing  Coverage
----------------------------------------------------------------------
NVDA       2021-01-04   2026-02-20   1280        5     99.6%
AAPL       2026-01-02   2026-02-20     34     1250      2.6%
TSLA       —            —               0     1284      0.0%
...

Expected weekdays since 2021-01-01: 1284
```

- **Records**: Number of rows in the DB for this ticker since `gap-fill-from`
- **Missing**: `expected_weekdays - records` (includes market holidays)
- **Coverage**: `records / expected_weekdays * 100`

Use `--gap-fill-from` to change the analysis start date (e.g., `--status --gap-fill-from 2023-01-01`).

## Duplicate Handling (Upsert)

The database has a unique constraint `uq_ticker_date` on `(ticker_id, date)`. The import pipeline uses PostgreSQL's `INSERT ... ON CONFLICT DO UPDATE`, which:

- **Inserts** new rows for dates that don't exist
- **Overwrites** all price fields for dates that already exist
- **Never creates duplicates** regardless of how many times data is imported

This means re-downloading overlapping date ranges is always safe.

## Rate Limiting

investing.com applies rate limiting and bot detection:

- Default delay between requests: 3 seconds
- For large batches (10+ tickers), increase to 5-10 seconds
- If blocked, wait several minutes and retry
- Use `--no-headless` to debug and manually pass CAPTCHAs
