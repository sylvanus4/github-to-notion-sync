# Setup Troubleshooting Guide

This guide helps resolve common setup issues encountered during testing.

## GitHub Token Issues

### Problem: Missing `read:project` Scope

**Error**: `Your token has not been granted the required scopes to execute this query. The 'projectV2' field requires one of the following scopes: ['read:project']`

**Solution**:

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Click on your existing token or create a new one
3. Ensure the following scopes are checked:
   - ✅ `read:project` (required for GitHub Projects v2)
   - ✅ `repo` (for repository access)
   - ✅ `write:project` (if you want to modify projects)

### Problem: Token Not Found or Invalid

**Error**: `Bad credentials` or `Could not resolve to a User with the login`

**Solution**:

1. Verify your token is correctly set in environment variables:

   ```bash
   echo $GH_TOKEN  # Should show your token
   ```

2. Test your token with GitHub API:

   ```bash
   curl -H "Authorization: token $GH_TOKEN" https://api.github.com/user
   ```

## Notion Database Issues

### Problem: Provided ID is a Page, Not a Database

**Error**: `Provided ID 22a9eddc-34e6-80e4-9cfc-ef3977293e5f is a page, not a database`

**Solution**:

1. Open your Notion workspace
2. Navigate to the database (not a page containing the database)
3. Copy the database ID from the URL:
   - ✅ Correct: `https://www.notion.so/myworkspace/22a9eddc34e680e49cfcef3977293e5f?v=...`
   - ❌ Wrong: Page URL that contains the database

### Problem: Database Not Found or Access Denied

**Error**: `Object not found` or `Unauthorized`

**Solution**:

1. Verify your Notion integration has access to the database:
   - Open your database in Notion
   - Click `•••` → `Add connections`
   - Add your integration
2. Check your Notion token:

   ```bash
   curl -H "Authorization: Bearer $NOTION_TOKEN" \
        -H "Notion-Version: 2022-06-28" \
        https://api.notion.com/v1/databases/YOUR_DATABASE_ID
   ```

## Environment Configuration

### Problem: Environment Variables Not Loaded

**Error**: Variables appear as `None` or empty

**Solution**:

1. Create a `.env` file in the project root:

   ```bash
   GH_TOKEN=your_github_token_here
   NOTION_TOKEN=your_notion_token_here
   GH_ORG=your_github_org
   GH_PROJECT_NUMBER=5
   NOTION_DB_ID=your_notion_database_id
   GH_WEBHOOK_SECRET=your_webhook_secret
   ```

2. Verify the file is loaded:

   ```bash
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GH_TOKEN'))"
   ```

## Database Schema Issues

### Problem: Field Mapping Errors

**Error**: Property not found or type mismatch

**Solution**:

1. Check your Notion database properties match the field mappings
2. Run the validation script:

   ```bash
   python scripts/validate_setup.py
   ```

3. Update `config/field_mappings.yml` to match your database schema

### Problem: Required Fields Missing

**Error**: Missing required field mappings

**Solution**:
Ensure these required fields are mapped in `config/field_mappings.yml`:

- `title`: Maps to a Notion title property
- `github_node_id`: Maps to a Notion text property (unique identifier)

## GraphQL Query Issues

### Problem: Field Doesn't Exist Errors

**Error**: `Field 'description' doesn't exist on type 'ProjectV2'`

**Solution**:
This should be automatically fixed, but if you encounter it:

1. Check the GraphQL queries in `queries/` directory
2. Remove any unsupported fields from ProjectV2 queries
3. Test with GitHub's GraphQL Explorer

## Testing Commands

### Quick Test (5 seconds)

```bash
python scripts/quick_test.py
```

### Full Functionality Test (30-60 seconds)

```bash
python scripts/test_functionality.py
```

### Professional Test Suite

```bash
pytest tests/test_integration.py -v
```

## Common Solutions

### 1. Reset Environment

```bash
# Clear existing environment
unset GH_TOKEN NOTION_TOKEN GH_ORG GH_PROJECT_NUMBER NOTION_DB_ID

# Reload from .env
source .env
```

### 2. Verify API Access

```bash
# Test GitHub API
curl -H "Authorization: token $GH_TOKEN" https://api.github.com/user

# Test Notion API
curl -H "Authorization: Bearer $NOTION_TOKEN" \
     -H "Notion-Version: 2022-06-28" \
     https://api.notion.com/v1/users/me
```

### 3. Check Network Connectivity

```bash
# Test basic connectivity
ping api.github.com
ping api.notion.com

# Test with SSL
curl -I https://api.github.com
curl -I https://api.notion.com
```

## Getting Help

If you're still experiencing issues:

1. Check the logs for detailed error messages
2. Run the validation script: `python scripts/validate_setup.py`
3. Review the API documentation:
   - [GitHub Projects v2 API](https://docs.github.com/en/graphql/reference/objects#projectv2)
   - [Notion API](https://developers.notion.com/reference/intro)
4. Check the project's issue tracker for similar problems

## Version Information

- **GitHub API**: GraphQL v4
- **Notion API**: v2022-06-28
- **Python**: 3.8+
- **Required Scopes**: `read:project`, `repo`
