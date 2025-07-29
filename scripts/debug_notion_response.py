#!/usr/bin/env python3
"""
Debug Notion API response to understand parsing errors.
"""

import sys
import os
import json
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


def main():
    """Debug Notion API responses."""
    try:
        notion_service = NotionService()
        
        print("🔍 Testing Notion API connection...")
        
        # Test 1: Get all pages (raw response)
        print("\n--- Test 1: Getting all pages (raw) ---")
        try:
            pages = notion_service.get_all_pages()
            print(f"Found {len(pages)} pages")
            
            if pages:
                # Show first page structure
                first_page = pages[0]
                print(f"\nFirst page structure:")
                print(f"ID: {first_page.id}")
                print(f"Properties keys: {list(first_page.properties.keys())}")
                
                # Check specific property
                if "진행 상태" in first_page.properties:
                    status_prop = first_page.properties["진행 상태"]
                    print(f"진행 상태 property: {status_prop}")
                    print(f"Type: {type(status_prop)}")
                    print(f"Raw data: {status_prop.__dict__}")
        
        except Exception as e:
            print(f"Error getting pages: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 2: Create a simple page to see response structure
        print("\n--- Test 2: Creating test page ---")
        try:
            test_properties = {
                "작업": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "TEST PAGE - DELETE ME"}
                        }
                    ]
                },
                "진행 상태": {
                    "select": {
                        "name": "시작 전"
                    }
                }
            }
            
            response = notion_service.client.pages.create(
                parent={"database_id": notion_service.settings.notion_db_id},
                properties=test_properties
            )
            
            print(f"Created test page: {response['id']}")
            print(f"Response properties: {response.get('properties', {}).keys()}")
            
            # Check the returned property structure
            if '진행 상태' in response.get('properties', {}):
                status_prop = response['properties']['진행 상태']
                print(f"Returned 진행 상태 property: {status_prop}")
            
            # Clean up - delete the test page
            notion_service.client.pages.update(
                page_id=response['id'],
                archived=True
            )
            print("Test page cleaned up")
            
        except Exception as e:
            print(f"Error creating test page: {e}")
            import traceback
            traceback.print_exc()
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 