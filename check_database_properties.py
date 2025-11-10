#!/usr/bin/env python3
"""
Check all properties in Notion database
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.notion_service import NotionService
from src.utils.logger import get_logger, init_logging

# Initialize logging
init_logging()
logger = get_logger(__name__)


def check_database_properties():
    """Check all properties in Notion database"""
    try:
        print("🔍 Checking Notion database properties...")
        print("=" * 60)

        # Initialize Notion service
        notion_service = NotionService()

        # Get database properties
        database = notion_service.get_database()

        if not database:
            print("❌ Failed to get database info")
            return

        # Convert to dict for easier access
        database_info = database.model_dump() if hasattr(database, "model_dump") else database.__dict__

        print(f"Database Title: {database_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        print(f"Database ID: {database_info['id']}")
        print()

        print("Properties:")
        print("-" * 40)

        properties = database_info.get("properties", {})

        for prop_name, prop_config in properties.items():
            prop_type = prop_config.get("type", "unknown")
            print(f"  '{prop_name}' (type: {prop_type})")

            # Show additional details for specific types
            if prop_type == "select":
                options = prop_config.get("select", {}).get("options", [])
                if options:
                    print(f"    Options: {[opt['name'] for opt in options]}")
            elif prop_type == "multi_select":
                options = prop_config.get("multi_select", {}).get("options", [])
                if options:
                    print(f"    Options: {[opt['name'] for opt in options]}")
            elif prop_type == "status":
                options = prop_config.get("status", {}).get("options", [])
                if options:
                    print(f"    Status options: {[opt['name'] for opt in options]}")
            elif prop_type == "people":
                print("    People field")

        print()
        print(f"Total properties: {len(properties)}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    check_database_properties()
