#!/usr/bin/env python3

"""
Check the actual status field options in Notion database.
"""

import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)


def check_status_field():
    """Check the actual status field options in Notion database."""
    logger.info("Checking Notion database status field...")
    
    # Initialize services
    notion_service = NotionService()
    
    try:
        # Get database schema
        database = notion_service.get_database()
        
        if not database:
            logger.error("Failed to get database info")
            return False
            
        # Convert to dict for easier access
        database_info = database.model_dump() if hasattr(database, 'model_dump') else database.__dict__
        
        print("\n" + "="*60)
        print("NOTION DATABASE STATUS FIELD ANALYSIS")
        print("="*60)
        
        # Find the status field
        status_property = None
        for prop_name, prop_info in database_info.get("properties", {}).items():
            if prop_info.get("type") == "status":
                status_property = prop_info
                print(f"\nStatus Property: '{prop_name}'")
                print(f"Type: {prop_info.get('type')}")
                
                # Get status options
                status_config = prop_info.get("status", {})
                options = status_config.get("options", [])
                groups = status_config.get("groups", [])
                
                print(f"\nStatus Options ({len(options)} total):")
                print("-" * 40)
                for i, option in enumerate(options, 1):
                    print(f"  {i}. '{option.get('name', 'Unknown')}' (id: {option.get('id', 'N/A')}, color: {option.get('color', 'N/A')})")
                
                if groups:
                    print(f"\nStatus Groups ({len(groups)} total):")
                    print("-" * 40)
                    for i, group in enumerate(groups, 1):
                        group_name = group.get('name', 'Unknown')
                        group_id = group.get('id', 'N/A')
                        group_color = group.get('color', 'N/A')
                        option_ids = group.get('option_ids', [])
                        print(f"  {i}. Group '{group_name}' (id: {group_id}, color: {group_color})")
                        print(f"     Option IDs: {option_ids}")
                
                break
        
        if not status_property:
            print("\n❌ No status property found in the database!")
            return False
            
        print("\n" + "="*60)
        print("GITHUB TO NOTION STATUS MAPPING SUGGESTIONS")
        print("="*60)
        
        # Current GitHub status options from analysis
        github_statuses = ['Epic', 'Todo', 'In Progress', 'Done', '25-07-Archive']
        
        print("\nCurrent GitHub Status Options:")
        for status in github_statuses:
            print(f"  - {status}")
            
        print("\nSuggested Mappings:")
        print("-" * 40)
        
        # Get available option names
        if status_property:
            available_options = [opt.get('name') for opt in status_property.get('status', {}).get('options', [])]
            
            # Create suggested mapping
            mapping_suggestions = {
                'Epic': 'Todo',  # Default fallback
                'Todo': 'Todo',
                'In Progress': 'In progress' if 'In progress' in available_options else 'Todo',
                'Done': 'Done' if 'Done' in available_options else 'Complete',
                '25-07-Archive': 'Done' if 'Done' in available_options else 'Complete'
            }
            
            for github_status, suggested_notion in mapping_suggestions.items():
                print(f"  '{github_status}' → '{suggested_notion}'")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to check status field: {e}")
        return False


if __name__ == "__main__":
    success = check_status_field()
    sys.exit(0 if success else 1) 