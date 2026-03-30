# HF CLI Cheatsheet

## Top-Level Commands

| Command | Description | Skill |
|---------|-------------|-------|
| `hf auth` | Authentication management | hf-hub |
| `hf cache` | Local cache management | hf-hub |
| `hf skills` | Agent skill management | hf-hub |
| `hf extensions` | CLI extension management | hf-hub |
| `hf env` / `hf version` | Environment info | hf-hub |
| `hf models` | Model search and info | hf-models |
| `hf download` / `hf upload` | File transfer | hf-models |
| `hf datasets` | Dataset discovery and SQL | hf-models (discovery) / hf-datasets (CRUD) |
| `hf papers` | Daily paper listing | hf-papers |
| `hf collections` | Collection management | hf-collections |
| `hf discussions` | PR and discussion management | hf-discussions |
| `hf endpoints` | Inference endpoint deployment | hf-endpoints |
| `hf buckets` / `hf sync` | S3-style object storage | hf-buckets |
| `hf spaces` | Spaces management | hf-spaces |
| `hf repos` | Repository lifecycle | hf-repos |
| `hf jobs` | Cloud compute jobs | hf-jobs |
| `hf webhooks` | Webhook management | hf-hub |

## Global Flags

- `--format json` — JSON output
- `-q, --quiet` — IDs only
- `--token TEXT` — override auth token
- `--help` — show help
