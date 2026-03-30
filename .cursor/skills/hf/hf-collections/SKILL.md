---
name: hf-collections
description: >-
  Curate and manage collections of models, datasets, spaces, and papers on
  Hugging Face Hub via the hf CLI. Use when the user asks to create a
  collection, add items to a collection, browse collections by owner, update
  collection metadata, or organize Hub resources into curated lists.
  Do NOT use for model search (use hf-models), dataset CRUD (use hf-datasets),
  repo management (use hf-repos), or paper discovery (use hf-papers).
  Korean triggers: "컬렉션 생성", "컬렉션 관리", "HF 컬렉션", "모델 큐레이션".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "ml"
---
# Hugging Face Collections

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.

## Quick Commands

### List Collections

```bash
hf collections ls --owner nvidia --sort trending --limit 10
hf collections ls --item MODEL_ID --format json
```

| Flag | Required | Description |
|------|----------|-------------|
| `--owner TEXT` | No | Filter by owner/org |
| `--item TEXT` | No | Find collections containing this item |
| `--sort` | No | `trending`, `created_at`, `last_modified` |
| `--limit INTEGER` | No | Number of results |
| `--format [table\|json]` | No | Output format |
| `-q, --quiet` | No | Print collection slugs only |

### Get Collection Info

```bash
hf collections info COLLECTION_SLUG
hf collections info username/my-collection-123abc --format json
```

### Create Collection

```bash
hf collections create "My Research" --description "Curated models for NLP"
hf collections create "Team Models" --namespace my-org --private
```

> **Write command** — confirm with the user before creating.

| Flag | Required | Description |
|------|----------|-------------|
| `TITLE` | Yes | Collection title |
| `--description` | No | Collection description |
| `--namespace` | No | Owner namespace (user or org) |
| `--private` | No | Create as private collection |

### Add Item to Collection

```bash
hf collections add-item SLUG ITEM_ID model
hf collections add-item SLUG ITEM_ID dataset --note "High quality training data"
hf collections add-item SLUG ITEM_ID paper --note "Foundation paper"
hf collections add-item SLUG ITEM_ID space
```

> **Write command** — confirm with the user before adding.

| Flag | Required | Description |
|------|----------|-------------|
| `SLUG` | Yes | Collection slug (e.g., `user/my-collection-abc123`) |
| `ITEM_ID` | Yes | Item repo ID or paper ID |
| `ITEM_TYPE` | Yes | `model`, `dataset`, `space`, `paper`, `collection` |
| `--note` | No | Annotation note for the item |

### Update Collection

```bash
hf collections update SLUG --title "New Title" --description "Updated description"
hf collections update SLUG --private   # make private
```

### Update Item

```bash
hf collections update-item SLUG ITEM_OBJECT_ID --note "Updated annotation"
```

### Delete

```bash
hf collections delete SLUG                    # delete entire collection
hf collections delete-item SLUG ITEM_OBJECT_ID  # remove single item
```

> **DESTRUCTIVE** — confirm with the user before deleting.

## Common Patterns

```bash
# Create a research collection and populate it
SLUG=$(hf collections create "LLM Research Q1 2026" --format json | jq -r '.slug')
hf collections add-item "$SLUG" meta-llama/Llama-3.2-1B model --note "Base model"
hf collections add-item "$SLUG" tatsu-lab/alpaca dataset --note "Instruction tuning data"

# Find all collections containing a specific model
hf collections ls --item meta-llama/Llama-3.2-1B --format json

# Browse an org's collections
hf collections ls --owner nvidia --sort trending --limit 10

# Auto-curate today's trending papers into a collection
hf papers ls --date today --sort trending -q | head -5 | while read id; do
  hf collections add-item "$SLUG" "$id" paper --note "Trending $(date +%Y-%m-%d)"
done
```

## Examples

### Example 1: Create and populate a collection

**User says:** "Create a collection of the best code generation models"

**Actions:**
1. Create: `hf collections create "Best Code Generation Models" --description "Top models for code generation tasks"`
2. Search: `hf models ls --filter text-generation --search "code" --sort downloads --limit 5 -q`
3. Add each: `hf collections add-item SLUG MODEL_ID model --note "Top by downloads"`

### Example 2: Troubleshooting

**User says:** "Can't add item to collection"

**Actions:**
1. Verify collection slug: `hf collections info SLUG`
2. Check item ID exists: `hf models info ITEM_ID` (or datasets/spaces)
3. Verify auth: `hf auth whoami`
4. Ensure you own the collection or have write access

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Collection not found | Verify the full slug (format: `owner/title-hash`) |
| Item already in collection | Duplicates are rejected — check existing items first |
| Permission denied | You must own the collection to modify it |
| Invalid item type | Must be one of: `model`, `dataset`, `space`, `paper`, `collection` |
