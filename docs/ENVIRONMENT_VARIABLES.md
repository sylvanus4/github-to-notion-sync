# Environment Variables Guide

## Required Environment Variables

Create a `.env` file in the project root with the following variables:

### GitHub Configuration

```bash
# GitHub Personal Access Token (with repo and project permissions)
GH_TOKEN=your_github_token_here

# GitHub Organization name
GH_ORG=your_github_org_name

# GitHub Project number (found in project URL)
GH_PROJECT_NUMBER=1

# Webhook secret for GitHub webhook verification
GH_WEBHOOK_SECRET=your_webhook_secret_here
```

### Notion Configuration

```bash
# Notion Integration Token
NOTION_TOKEN=your_notion_token_here

# Notion Database ID (32 characters, found in database URL)
NOTION_DB_ID=your_notion_database_id_here
```

## Optional Environment Variables

### Logging Configuration

```bash
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log format: json or text
LOG_FORMAT=json

# Environment: development, staging, production
ENVIRONMENT=development
```

### Server Configuration

```bash
# Webhook server port
WEBHOOK_PORT=8000

# Webhook server host
WEBHOOK_HOST=0.0.0.0
```

### Performance Configuration

```bash
# Batch size for sync operations
BATCH_SIZE=50

# Rate limits (requests per second/hour)
NOTION_RATE_LIMIT=3
GITHUB_RATE_LIMIT=5000

# Retry configuration
RETRY_ATTEMPTS=3
RETRY_DELAY=1
```

### Scheduling Configuration

```bash
# Full sync interval (cron format)
FULL_SYNC_INTERVAL=0 */6 * * *

# Backup configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * 0
```

### Directory Configuration

```bash
# Configuration files directory
CONFIG_DIR=config

# GraphQL queries directory
QUERIES_DIR=queries
```

## Example .env File

```bash
# Required - GitHub
GH_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GH_ORG=my-organization
GH_PROJECT_NUMBER=1
GH_WEBHOOK_SECRET=my-webhook-secret-123

# Required - Notion
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
ENVIRONMENT=development

# Optional - Server
WEBHOOK_PORT=8000
WEBHOOK_HOST=0.0.0.0

# Optional - Performance
BATCH_SIZE=50
NOTION_RATE_LIMIT=3
GITHUB_RATE_LIMIT=5000
RETRY_ATTEMPTS=3
RETRY_DELAY=1

# Optional - Scheduling
FULL_SYNC_INTERVAL=0 */6 * * *
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * 0

# Optional - Directories
CONFIG_DIR=config
QUERIES_DIR=queries
```

## How to Get Required Values

### GitHub Token (GH_TOKEN)

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with these permissions:
   - `repo` (full repository access)
   - `project` (project access)
   - `read:org` (read organization data)
3. Copy the token and use it as `GH_TOKEN`

### GitHub Organization (GH_ORG)

- Use your GitHub organization name (e.g., `microsoft`, `google`)
- Found in the organization URL: `https://github.com/YOUR_ORG`

### GitHub Project Number (GH_PROJECT_NUMBER)

- Found in the project URL: `https://github.com/orgs/YOUR_ORG/projects/PROJECT_NUMBER`
- Use the number after `/projects/`

### Webhook Secret (GH_WEBHOOK_SECRET)

- Generate a random string (at least 20 characters)
- Use a password generator or: `openssl rand -hex 20`
- This will be used when setting up GitHub webhooks

### Notion Token (NOTION_TOKEN)

1. Go to <https://www.notion.so/my-integrations>
2. Create a new integration
3. Copy the "Internal Integration Token"
4. Make sure to share your database with the integration

### Notion Database ID (NOTION_DB_ID)

- Found in the database URL: `https://www.notion.so/workspace/DATABASE_ID?v=...`
- Use the 32-character string (with or without hyphens)

## Validation

After creating your `.env` file, validate it with:

```bash
# Quick validation
python scripts/quick_test.py

# Full validation
python scripts/test_functionality.py
```

## Security Notes

1. **Never commit your `.env` file to version control**
2. **Keep your tokens secure** - they provide access to your GitHub and Notion data
3. **Use different tokens for different environments** (development, staging, production)
4. **Rotate tokens regularly** as a security best practice
5. **Use environment-specific webhook secrets**

## Troubleshooting

### Common Issues

1. **Token Permission Errors**

   - Ensure GitHub token has `repo` and `project` permissions
   - Ensure Notion integration is shared with the database

2. **Invalid Database ID**

   - Notion database ID must be exactly 32 characters
   - Remove hyphens if present in the URL

3. **Project Not Found**

   - Verify `GH_ORG` and `GH_PROJECT_NUMBER` are correct
   - Ensure the project exists and is accessible

4. **Webhook Signature Verification Failed**
   - Check that `GH_WEBHOOK_SECRET` matches the webhook configuration
   - Ensure the secret is at least 20 characters long
