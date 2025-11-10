#!/usr/bin/env python3
"""
Quick test script to validate basic functionality.
Fast checks without full integration testing.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file
try:
    from dotenv import load_dotenv
    # Load .env from project root
    load_dotenv(dotenv_path=project_root / ".env")
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

def quick_check():
    """Quick validation check."""
    print("🔍 Quick Validation Check")
    print("=" * 40)

    # Check environment variables
    required_vars = [
        "GH_TOKEN",
        "NOTION_TOKEN",
        "GH_ORG",
        "GH_PROJECT_NUMBER",
        "NOTION_DB_ID"
    ]

    print("📋 Environment Variables:")
    missing = []
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ {var}")
            missing.append(var)

    if missing:
        print(f"\n❌ Missing variables: {', '.join(missing)}")
        return False

    # Check imports
    print("\n📦 Import Check:")
    try:
        from src.config import get_config
        print("  ✅ Config module")

        from src.services.github_service import GitHubService
        print("  ✅ GitHub service")

        from src.services.notion_service import NotionService
        print("  ✅ Notion service")

        from src.services.sync_service import SyncService
        print("  ✅ Sync service")

        from src.handlers.webhook_handler import WebhookHandler
        print("  ✅ Webhook handler")

    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False

    # Check configuration
    print("\n⚙️ Configuration Check:")
    try:
        config = get_config()
        print("  ✅ Configuration loaded")

        if config.field_mappings:
            print(f"  ✅ Field mappings: {len(config.field_mappings)}")
        else:
            print("  ❌ No field mappings")
            return False

        if 'title' in config.field_mappings:
            print("  ✅ Title field mapped")
        else:
            print("  ❌ Title field not mapped")
            return False

    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

    print("\n✅ Quick validation passed!")
    return True


if __name__ == "__main__":
    success = quick_check()
    if success:
        print("\n🎉 Ready to run full tests!")
        print("Run: python scripts/test_functionality.py")
    else:
        print("\n❌ Please fix the issues above first.")
    exit(0 if success else 1)
