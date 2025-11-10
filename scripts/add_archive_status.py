#!/usr/bin/env python3
"""
Add '25-08-Archive' status option to Notion database status field.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger

# Initialize logging
init_logging()
logger = get_logger(__name__)


def add_archive_status_option():
    """Add '25-08-Archive' status option to Notion database."""
    try:
        print("🔧 Adding '25-08-Archive' status option to Notion database...")
        print("=" * 60)

        # Initialize Notion service
        notion_service = NotionService()

        # Get current database
        database = notion_service.get_database()
        if not database:
            print("❌ Failed to get database info")
            return False

        # Check current status options
        database_info = database.model_dump() if hasattr(database, 'model_dump') else database.__dict__
        properties = database_info.get('properties', {})

        status_property = properties.get("진행 상태")
        if not status_property:
            print("❌ '진행 상태' status field not found")
            return False

        current_options = status_property.get('status', {}).get('options', [])
        option_names = [opt.get('name', '') for opt in current_options]

        print(f"Current status options: {option_names}")

        if "25-08-Archive" in option_names:
            print("✅ '25-08-Archive' status option already exists!")
            return True

        # Add the new status option using Notion API
        database_id = notion_service.settings.notion_db_id

        # Create new options list with the additional option
        new_options = current_options + [{
            "name": "25-08-Archive",
            "color": "gray"  # Archive status typically uses gray color
        }]

        # Build the update payload
        update_payload = {
            "properties": {
                "진행 상태": {
                    "status": {
                        "options": new_options
                    }
                }
            }
        }

        def _update_database():
            return notion_service.client.databases.update(
                database_id=database_id,
                **update_payload
            )

        response = notion_service._handle_rate_limit(_update_database)

        if response:
            print("✅ Successfully added '25-08-Archive' status option!")
            print(f"   Option Name: 25-08-Archive")
            print(f"   Option Color: gray")
            return True
        else:
            print("❌ Failed to add status option")
            return False

    except Exception as e:
        logger.error(f"Error adding status option: {e}")
        print(f"❌ Error: {e}")
        return False


def verify_status_addition():
    """Verify that the status option was added successfully."""
    try:
        print("\n🔍 Verifying status option addition...")

        # Initialize Notion service
        notion_service = NotionService()

        # Get updated database info
        database = notion_service.get_database()
        if not database:
            print("❌ Failed to get database info")
            return False

        database_info = database.model_dump() if hasattr(database, 'model_dump') else database.__dict__
        properties = database_info.get('properties', {})

        status_property = properties.get("진행 상태")
        if status_property:
            current_options = status_property.get('status', {}).get('options', [])
            option_names = [opt.get('name', '') for opt in current_options]

            print(f"Updated status options: {option_names}")

            if "25-08-Archive" in option_names:
                print("✅ '25-08-Archive' status option verified!")
                return True
            else:
                print("❌ '25-08-Archive' status option not found")
                return False
        else:
            print("❌ Status field not found")
            return False

    except Exception as e:
        logger.error(f"Error verifying status option: {e}")
        print(f"❌ Verification error: {e}")
        return False


def main():
    """Main function."""
    success = add_archive_status_option()

    if success:
        verify_status_addition()
        print("\n🎉 Archive status option setup complete!")
        print("You can now re-run the complete resync to sync items with '25-08-Archive' status.")
    else:
        print("\n❌ Failed to add archive status option.")
        print("You may need to manually add '25-08-Archive' as a status option in your Notion database.")


if __name__ == "__main__":
    main()
