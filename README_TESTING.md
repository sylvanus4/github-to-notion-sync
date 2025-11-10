# Testing Guide

## Overview

This guide explains how to test the GitHub to Notion sync functionality after setting up your `.env` file.

## Prerequisites

1. Complete the setup in `docs/SETUP.md`
2. Configure your `.env` file with all required variables
3. Install dependencies: `pip install -r requirements.txt`

## Test Scripts

### 1. Quick Test (`scripts/quick_test.py`)

**Purpose**: Fast validation of basic setup
**Duration**: ~5 seconds
**What it checks**:

- Environment variables are set
- Python modules can be imported
- Configuration loads correctly
- Basic field mappings exist

**Usage**:

```bash
python scripts/quick_test.py
```

**Expected Output**:

```
🔍 Quick Validation Check
========================================
📋 Environment Variables:
  ✅ GH_TOKEN
  ✅ NOTION_TOKEN
  ✅ GH_ORG
  ✅ GH_PROJECT_NUMBER
  ✅ NOTION_DB_ID

📦 Import Check:
  ✅ Config module
  ✅ GitHub service
  ✅ Notion service
  ✅ Sync service
  ✅ Webhook handler

⚙️ Configuration Check:
  ✅ Configuration loaded
  ✅ Field mappings: 15
  ✅ Title field mapped

✅ Quick validation passed!

🎉 Ready to run full tests!
Run: python scripts/test_functionality.py
```

### 2. Full Functionality Test (`scripts/test_functionality.py`)

**Purpose**: Complete integration testing
**Duration**: ~30-60 seconds
**What it tests**:

- Environment variables
- Configuration loading
- GitHub API connection
- Notion API connection
- Sync service validation
- Webhook handler functionality
- Sample sync operation

**Usage**:

```bash
python scripts/test_functionality.py
```

**Expected Output**:

```
🚀 GitHub to Notion Sync - Functionality Test
============================================================

============================================================
🔍 Environment Variables Check
============================================================
✅ GH_TOKEN is set
✅ NOTION_TOKEN is set
✅ GH_ORG is set
✅ GH_PROJECT_NUMBER is set
✅ NOTION_DB_ID is set
✅ GH_WEBHOOK_SECRET is set
⚠️  LOG_LEVEL is not set (optional)
⚠️  ENVIRONMENT is not set (optional)
⚠️  BATCH_SIZE is not set (optional)

============================================================
🔍 Configuration Loading
============================================================
✅ Configuration loaded successfully
ℹ️  GitHub Org: your-org
ℹ️  GitHub Project: 1
ℹ️  Notion DB ID: 12345678...
ℹ️  Environment: development
ℹ️  Log Level: INFO
ℹ️  Batch Size: 50
✅ Field mappings loaded: 15 fields
✅ Required field 'title' is mapped
✅ Required field 'github_node_id' is mapped
✅ Webhook events configured: 3 types
⚠️  No user mappings configured

============================================================
🔍 GitHub Service Test
============================================================
✅ GitHub connection successful
ℹ️  Project: My Project
ℹ️  URL: https://github.com/orgs/your-org/projects/1
✅ GitHub project fields retrieved: 8 fields
ℹ️    - Status (SINGLE_SELECT)
ℹ️    - Priority (SINGLE_SELECT)
ℹ️    - Assignees (ASSIGNEES)
✅ GitHub project items retrieved: 12 items
ℹ️  Sample item: Fix bug in authentication
ℹ️  Type: ISSUE
ℹ️  Rate limit: 4950/5000 remaining

============================================================
🔍 Notion Service Test
============================================================
✅ Notion connection successful
ℹ️  Database: GitHub Issues
ℹ️  ID: 12345678-1234-1234-1234-123456789012
✅ Notion query successful: 3 pages found
ℹ️  Has more pages: True
✅ Field mappings validation passed
ℹ️  Mapped fields: 15

============================================================
🔍 Sync Service Test
============================================================
✅ Sync setup validation passed
✅ GitHub connection: True
✅ Notion connection: True
✅ Field mappings: True
ℹ️  Last full sync: Never
ℹ️  Total synced: 0
ℹ️  Webhook syncs: 0
ℹ️  Errors: 0

============================================================
🔍 Webhook Handler Test
============================================================
✅ Webhook signature verification working
✅ Webhook configuration validation passed
ℹ️  Webhook secret configured: True
ℹ️  Enabled events: 3
ℹ️  Total received: 0
ℹ️  Success rate: 0.0%

============================================================
🔍 Sample Sync Test
============================================================
ℹ️  Testing sync for item: Fix bug in authentication
ℹ️  Item ID: PVTI_lADOBizqqs4AcbzJzgLmTQo
✅ Properties built successfully
ℹ️  Built 8 properties
ℹ️    - Title: dict
ℹ️    - GitHub Node ID: dict
ℹ️    - Status: dict
ℹ️  Item does not exist in Notion (would be created)

============================================================
🔍 Test Summary
============================================================
✅ Environment Variables
✅ Configuration
✅ GitHub Service
✅ Notion Service
✅ Sync Service
✅ Webhook Handler
✅ Sample Sync

============================================================
Tests completed in 45.23 seconds
Passed: 7/7

✅ 🎉 All tests passed! Your setup is working correctly.
```

### 3. Pytest Integration Tests (`tests/test_integration.py`)

**Purpose**: Professional pytest-based testing
**Duration**: ~60-90 seconds
**What it tests**:

- Comprehensive test coverage
- Async functionality
- Error handling
- Edge cases

**Usage**:

```bash
# Run all integration tests
pytest tests/test_integration.py -v

# Run specific test class
pytest tests/test_integration.py::TestGitHubService -v

# Run with coverage
pytest tests/test_integration.py --cov=src --cov-report=html
```

## Common Issues and Solutions

### 1. Environment Variables Not Set

**Error**: `Missing required environment variables: ['GH_TOKEN']`
**Solution**: Check your `.env` file and ensure all required variables are set.

### 2. GitHub API Connection Failed

**Error**: `GitHub connection failed: 401 Unauthorized`
**Solution**:

- Check your `GH_TOKEN` is valid
- Ensure token has correct permissions for the organization and project
- Verify `GH_ORG` and `GH_PROJECT_NUMBER` are correct

### 3. Notion API Connection Failed

**Error**: `Notion connection failed: 401 Unauthorized`
**Solution**:

- Check your `NOTION_TOKEN` is valid
- Ensure the integration has access to the database
- Verify `NOTION_DB_ID` is correct (should be 32 characters)

### 4. Field Mapping Errors

**Error**: `Field mappings validation failed`
**Solution**:

- Check `config/field_mappings.yml` syntax
- Ensure all required fields are mapped
- Verify Notion database has the expected properties

### 5. Import Errors

**Error**: `Import error: No module named 'src.config'`
**Solution**:

- Ensure you're running from the project root directory
- Install dependencies: `pip install -r requirements.txt`
- Check Python path configuration

## Test Results Interpretation

### ✅ Success Indicators

- All environment variables are set
- API connections successful
- Field mappings validated
- Sample sync operations work

### ⚠️ Warning Indicators

- Optional environment variables not set (usually OK)
- No user mappings configured (affects assignee sync)
- Empty project or database (affects some tests)

### ❌ Error Indicators

- Missing required environment variables
- API connection failures
- Field mapping validation errors
- Import or configuration errors

## Next Steps After Testing

1. **All tests pass**: Your setup is ready! You can:

   - Run a full sync: `python scripts/full_sync.py`
   - Start the webhook server: `python -m src.main`
   - Set up GitHub webhooks using `scripts/setup_github_webhook.py`

2. **Some tests fail**: Fix the issues identified in the test output before proceeding.

3. **Need help**: Check the troubleshooting guide in `docs/TROUBLESHOOTING.md`.

## Continuous Testing

For ongoing development and maintenance:

```bash
# Run quick test before making changes
python scripts/quick_test.py

# Run full test after configuration changes
python scripts/test_functionality.py

# Run pytest for comprehensive testing
pytest tests/ -v
```

## Performance Testing

The test scripts also provide performance information:

- API response times
- Rate limit usage
- Memory usage patterns
- Sync operation duration

Monitor these metrics to ensure optimal performance in production.
