#!/usr/bin/env python3
"""
Add story points (스토리포인트) number field to Notion database.
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


def add_storypoints_field():
    """Add story points field to Notion database."""
    try:
        print("🔧 Adding 스토리포인트 field to Notion database...")
        print("=" * 60)
        
        # Initialize Notion service
        notion_service = NotionService()
        
        # Get current database
        database = notion_service.get_database()
        if not database:
            print("❌ Failed to get database info")
            return False
            
        # Check if field already exists
        database_info = database.model_dump() if hasattr(database, 'model_dump') else database.__dict__
        properties = database_info.get('properties', {})
        
        if "스토리포인트" in properties:
            print("✅ 스토리포인트 field already exists!")
            return True
        
        # Add the story points field using Notion API
        database_id = notion_service.settings.notion_db_id
        
        # Build the update payload
        update_payload = {
            "properties": {
                "스토리포인트": {
                    "number": {
                        "format": "number"
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
            print("✅ Successfully added 스토리포인트 field to Notion database!")
            print(f"   Field Type: Number")
            print(f"   Field Name: 스토리포인트")
            return True
        else:
            print("❌ Failed to add field")
            return False
            
    except Exception as e:
        logger.error(f"Error adding field: {e}")
        print(f"❌ Error: {e}")
        return False


def verify_field_addition():
    """Verify that the field was added successfully."""
    try:
        print("\n🔍 Verifying field addition...")
        
        # Initialize Notion service
        notion_service = NotionService()
        
        # Get updated database info
        database = notion_service.get_database()
        if not database:
            print("❌ Failed to get database info")
            return False
            
        database_info = database.model_dump() if hasattr(database, 'model_dump') else database.__dict__
        properties = database_info.get('properties', {})
        
        if "스토리포인트" in properties:
            field_info = properties["스토리포인트"]
            print(f"✅ 스토리포인트 field verified!")
            print(f"   Type: {field_info.get('type', 'unknown')}")
            return True
        else:
            print("❌ 스토리포인트 field not found")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying field: {e}")
        print(f"❌ Verification error: {e}")
        return False


def main():
    """Main function."""
    success = add_storypoints_field()
    
    if success:
        verify_field_addition()
        print("\n🎉 Story points field setup complete!")
        print("You can now run the complete resync to start syncing Estimate values.")
    else:
        print("\n❌ Failed to add story points field.")
        print("You may need to manually add a 'Number' field named '스토리포인트' to your Notion database.")


if __name__ == "__main__":
    main()
